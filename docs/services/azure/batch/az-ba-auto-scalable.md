# Azure Batch: _Auto Scalable_

**Autoscale** is not (currently) intended as a sub 1M response to changes but
rather to adjust the size of your pool gradually as you run a workload.

!!! quote

    The Batch uses your formula to determine the target number of
    compute nodes in the pool for the next interval of processing.

Since we only evaluate the formula every ~15m it is not like your pool is going
to immediately respond to new task pressure if left to its own devices. On the
other hand if you are running a long-lived pool, and you want to respond to
changes over the course of a day (for example day/night discrepancies in task
load) then autoscale is a good fit :partying_face:.

## Examples

Simaple re-scale dedicate node (`$TargetDedicated`) that base on running and active
tasks that exists on the Pool,

```cs
$NodeDeallocationOption = taskcompletion;

minNodes = 1;
maxNodes = 10;

activeTasks = $ActiveTasks.GetSample(1);
runningTasks = $RunningTasks.GetSample(1);

totalTasks = activeTasks + runningTasks;

nodes = min(max(minNodes, totalTasks), maxNodes);
$TargetDedicated = nodes;
```

!!! note

    If you want to scale low-priority node, you have change variable to `$TargetLowPriorityNodes`

### Auto Scale Target Low-Priority Nodes

Set autoscale evaluation interval to `15m 00s`.

=== "Using Working Hour and Weekday"

    ```cs
    // Fix dedicate target node to zero value
    $TargetDedicatedNodes = 0;

    // Get pending tasks for the past 15 minutes.
    samples = $PendingTasks.GetSamplePercent(TimeInterval_Minute * 15);

    // Catch current value of low-priority node.
    Curr_TargetLowPriorityNodes = $TargetLowPriorityNodes;

    // Get current time with timezone that add 7 hours.
    $CurTime = time() + 7 * TimeInterval_Hour;

    // Set working hours (8 - 19) and weekday (Mon - Fri) flag.
    $WorkHours = $CurTime.hour >= 8 && $CurTime.hour < 20;
    $IsWeekday = $CurTime.weekday >= 1 && $CurTime.weekday <= 5;
    $IsWorkingWeekdayHour = $WorkHours && $IsWeekday;

    // If we have less than 70% data points, we use the last sample point,
    // otherwise we use the average of last sample point between 1 and 2 minutes.
    AvgActiveTask = samples < 70 ? max(0, $ActiveTasks.GetSample(1)) : avg($ActiveTasks.GetSample(1 * TimeInterval_Minute, 2 * TimeInterval_Minute));

    // Fix capacity of the pool sizes for low-priority node.
    Capped_TargetLowPriorityNodes = 1;

    // Set calculation low-priority target node value by the minimum value of
    // this capacity and average task value.
    Cal_TargetLowPriorityNodes = min(Capped_TargetLowPriorityNodes, AvgActiveTask);

    // Set low-priority target node.
    $TargetLowPriorityNodes = $IsWorkingWeekdayHour ? max(Cal_TargetLowPriorityNodes, Curr_TargetLowPriorityNodes) : 0;

    // Set node de-allocation mode - keep nodes active only until tasks finish.
    $NodeDeallocationOption = taskcompletion;
    ```

=== "Use Running Task Sample"

    ```cs
    // Fix dedicate target node to zero value
    $TargetDedicatedNodes = 0;

    // Get pending tasks for the past 5 minutes.
    Samples = $PendingTasks.GetSamplePercent(TimeInterval_Minute * 5);

    // Fix capacity of the pool sizes
    Capped_PoolSize = 1;

    // If we have less than 70% data points, we use the last sample point,
    // otherwise we use the average of last sample point between 1 and 2 minutes.
    // (for running task we use last sample point between 1 and 10 minutes).
    AvgActiveTask = Samples < 70 ? max(0, $ActiveTasks.GetSample(1)) : avg($ActiveTasks.GetSample(1 * TimeInterval_Minute, 2 * TimeInterval_Minute));
    AvgRunningTask = Samples < 70 ? max(0, $RunningTasks.GetSample(1)) : avg($RunningTasks.GetSample(1 * TimeInterval_Minute, 10 * TimeInterval_Minute));

    ActiveTask = AvgActiveTask > 0 ? 1 : 0;
    RunningTask = AvgRunningTask > 0 ? 1 : 0;

    // Set low-priority target node by the minimum value
    $TargetLowPriorityNodes = min(Capped_PoolSize, max(ActiveTask, RunningTask));

    // Set node de-allocation mode - keep nodes active only until tasks finish
    $NodeDeallocationOption = taskcompletion;
    ```

### Auto Scale Target Dedicated Nodes

=== "Using Active and Running Task Sample"

    ```cs
    // Get the average of last sample point between 1 and 2 minutes.
    AvgActiveTask = $ActiveTasks.GetSample(60 * TimeInterval_Second, 120 * TimeInterval_Second);
    AvgRunningTask = $RunningTasks.GetSample(60 * TimeInterval_Second, 120 * TimeInterval_Second);

    // Combine the average of active and running tasks together.
    TotalTasksVector = AvgActiveTask + AvgRunningTask;

    vmsRequiredVector = TotalTasksVector / 4;
    vmsRequired = avg(vmsRequiredVector);

    // Set dedicated target node by the minimum value from the vsm required
    // value and capacity of 60 nodes.
    $TargetDedicated = min(max(vmsRequired, 1), 60);
    ```

    !!! warning

        We strongly recommend you avoid of using `GetSample(1)` in your autoscale formulas. \
        This is because `GetSample(1)` is just saying "give me the last sample you have,
        no matter how long ago you got it"  \
        Since you will use these samples to grow/shrink your pool (and your pool costs
        you money) we recommend that you base the formula on more than 1 samples worth
        of data. Instead, we suggest you do some trending type analysis and grow your
        pool based on that.

    In addition to the best practices comments that mentioned above, you have hit 2
    different bugs:

    - The last 1-2 samples of `$RunningTasks` are almost always `0`, so `.GetSamples(1)`
      on `RunningTasks` often will return `0` even if there are some running tasks.
      We will investigate this and work on a fix, but in the meantime adhering to the
      best practice of avoiding `GetSamples(1)` will help you avoid this issue

    - This one is more painful -- right now there is a bug where even when `MultipleTasksPerVM`
      is not set to the default of 1, `$RunningTasks` will only report 1 running task
      (even though there may be up to `N`, where `N == MaxTasksPerVM`).

      We're already tracking this bug in our backlog and will get to it ASAP.

      In the meantime, you can probably edit your formula to think of `$RunningTasks`
      as `RunningVMs` instead -- which should be able to get you close to what you
      want.

      See the following formula for an example of what I mean:

      ```cs
      AvgActiveTask = $ActiveTasks.GetSample(60 * TimeInterval_Second, 120 * TimeInterval_Second);
      AvgRunningTask = $RunningTasks.GetSample(60 * TimeInterval_Second, 120 * TimeInterval_Second);

      vmsRequiredVector = AvgActiveTask / 4 + AvgRunningTask;
      vmsRequired = avg(vmsRequiredVector);

      // Set dedicated target node by the minimum value from the vsm required
      // value and capacity of 60 nodes.
      $TargetDedicated = min(max(vmsRequired, 1), 60);
      ```

    !!! note

        You can use the `.GetSample(Interval Lookback Start, Interval Lookback End)` API
        to get a vector of samples, for example:

        ```cs
        AvgRunningTask = $RunningTasks.GetSample(60 * TimeInterval_Second, 120 * TimeInterval_Second);
        ```

        Might return:

        ```cs
        AvgRunningTask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1];
        ```

        Or, if you would like more certainty, you can force the evaluation to fail if
        there are less than a certain percentage of samples (here percentage means that
        if in a given time interval there were supposed to be `60` samples, but actually
        due to networking failures or other issues we were only able to gather 30 samples,
        the percentage would be 50%).

        This is how you specify a percentage (note the `60` as the 3rd parameter):

        ```cs
        AvgRunningTask = $RunningTasks.GetSample(60 * TimeInterval_Second, 120 * TimeInterval_Second, 60);
        ```

        When specifying a time range, always start with the time range starting at least
        1m ago, since it takes about 1m for samples to propagate through the system, so
        samples in the range `(0 * TimeInterval_Second, 60 * TimeInterval_Second)` will
        often not be available. Again you can use the percentage API to force a particular
        sample percentage.

        Read More: [Autoscale Formula Improvements Needed](https://social.msdn.microsoft.com/Forums/azure/en-US/21161846-6b6b-4e34-85fc-333663414714/autoscaleformula-improvements-needed?forum=azurebatch)

=== "Using Working Hour and Weekday"

    ```cs
    // Get current time with timezone that add 7 hours.
    $CurTime = time() + 7 * TimeInterval_Hour;

    // Set working hours (8 - 17) and weekday (Mon - Fri) flag.
    $WorkHours = $CurTime.hour >= 8 && $CurTime.hour < 18;
    $IsWeekday = $CurTime.weekday >= 1 && $CurTime.weekday <= 5;
    $IsWorkingWeekdayHour = $WorkHours && $IsWeekday;

    // Set dedicated target node to 20 if datetime in range else 10.
    $TargetDedicated = $IsWorkingWeekdayHour ? 20 : 10;
    ```

=== "Using Pending Task Sample"

    ```cs
    // Get pending tasks for the past 15 minutes.
    Samples = $PendingTasks.GetSamplePercent(TimeInterval_Minute * 15);

    // If we have less than 70% data points, we use the last sample point,
    // otherwise we use the maximum of last sample point and the history average.
    $Tasks = Samples < 70 ? max(0, $ActiveTasks.GetSample(1)) : max($ActiveTasks.GetSample(1), avg($ActiveTasks.GetSample(TimeInterval_Minute * 15)));

    // If number of pending tasks is not 0, set target node to pending tasks,
    // otherwise half of current dedicated target node.
    $TargetVMs = $Tasks > 0 ? $Tasks : max(0, $TargetDedicated / 2);

    // The pool size is capped at 20, if target node value is more than that,
    // set it to 20. This value should be adjusted according to your use case.
    $TargetDedicated = max(0, min($TargetVMs, 20));

    // Set node de-allocation mode - keep nodes active only until tasks finish
    $NodeDeallocationOption = taskcompletion;
    ```

=== "Using Max Task Per Node"

    Another example that adjusts the pool size based on the number of tasks, this
    formula also takes into account the `MaxTasksPerComputeNode` value that has been
    set for the pool. This is particularly useful in situations where parallel task
    execution on compute nodes is desired.

    ```cs
    // Determine whether 70% of the samples have been recorded in the past 15 minutes.
    // If not, use last sample.
    Samples = $ActiveTasks.GetSamplePercent(TimeInterval_Minute * 15);
    $Tasks = Samples < 70 ? max(0,$ActiveTasks.GetSample(1)) : max( $ActiveTasks.GetSample(1),avg($ActiveTasks.GetSample(TimeInterval_Minute * 15)));

    // Set the number of nodes to add to one-fourth the number of active tasks
    // (the MaxTasksPerComputeNode property on this pool is set to 4, adjust
    // this number for your use case)
    $Cores = $TargetDedicated * 4;
    $ExtraVMs = (($Tasks - $Cores) + 3) / 4;
    $TargetVMs = ($TargetDedicated + $ExtraVMs);

    // Attempt to grow the number of compute nodes to match the number of active
    // tasks, with a maximum of 3
    $TargetDedicated = max(0, min($TargetVMs, 3));

    // Set node de-allocation mode - keep nodes active only until tasks finish
    $NodeDeallocationOption = taskcompletion;
    ```

=== "Using Working Hour and Weekday with Minimum"

    ```cs
    // Set maximum node limit to 10.
    $MaxComputeNodeLimit = 10;

    // Get current time with timezone that add 7 hours.
    $CurTime = time() + 7 * TimeInterval_Hour;

    // Set working hours (8 - 17) and weekday (Mon - Fri) flag.
    $WorkHours = $CurTime.hour >= 8 && $CurTime.hour < 18;
    $IsWeekday = $CurTime.weekday >= 1 && $CurTime.weekday <= 5;
    $IsWorkingWeekdayHour = $WorkHours && $IsWeekday;

    // Set minimum capacity of target node to 1 if datetime in range else 0
    $MinCapacity = $IsWorkingWeekdayHour ? 1 : 0;

    // Get the last sample point of active and running tasks.
    $LastSampledActiveTasks = $ActiveTasks.GetSample(1);
    $LastSampledRunningTasks = $RunningTasks.GetSample(1);
    $RunningAndWaiting = max($LastSampledActiveTasks, 1) + max($LastSampledRunningTasks, 1);

    $NeedCompute = $RunningAndWaiting >= 1;

    $NodesToAllocate = $RunningAndWaiting > $MaxComputeNodeLimit ? $MaxComputeNodeLimit : $RunningAndWaiting;
    $TargetDedicated = $NeedCompute ? $NodesToAllocate : $MinCapacity;
    ```

## References

- [Microsoft Azure Batch Automatic Scaling](https://learn.microsoft.com/en-us/azure/batch/batch-automatic-scaling)
- [Azure Batch Pool Auto Scale Formulas](https://gordon.byers.me/azure/azure-batch-pool-auto-scale-forumulas/)
- [Azure Content: Batch Automatic Scaling](https://github.com/Huachao/azure-content/blob/master/articles/batch/batch-automatic-scaling.md)
