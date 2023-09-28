# Azure Batch: _Auto Scalable_

**Autoscale** is not (currently) intended as a sub 1m response to changes but
rather to adjust the size of your pool gradually as you run a workload.

!!! quote

    The Batch service uses your formula to determine the target number of
    compute nodes in the pool for the next interval of processing.

Since we only evaluate the formula every ~15m it is not like your pool is going
to immediately respond to new task pressure if left to its own devices.  On the
other hand if you are running a long-lived pool, and you want to respond to
changes over the course of a day (for example day/night discrepancies in task
load) then autoscale is a good fit :partying_face:.

## Example Use-cases

### Method 01: Auto Scale Target Low-Priority Nodes

Autoscale evaluation interval: `15m 00s`

=== "Version 01"

    Use Weekday and Business Time

    ```cs
    // Get pending tasks for the past 15 minutes.
    samples = $PendingTasks.GetSamplePercent(TimeInterval_Minute * 15);

    // Catch current value of low-priority and dedicate nodes
    Curr_TargetLowPriorityNodes = $TargetLowPriorityNodes;
    Curr_TargetDedicatedNodes = $TargetDedicatedNodes;

    // Get current time with timezone that add 7 hours
    $curTime = time() + 7 * TimeInterval_Hour;

    // Set working hours and weekday flag
    $workHours = $curTime.hour >= 8 && $curTime.hour < 20;
    $isWeekday = $curTime.weekday >= 1 && $curTime.weekday <= 5;
    $isWorkingWeekdayHour = $workHours && $isWeekday;

    // If we have less than 70% data points, we use the last sample point, otherwise we use the average of
    // last sample point between 1 and 2 minutes.
    AvgActiveTask = samples < 70 ? max(0, $ActiveTasks.GetSample(1)) : avg($ActiveTasks.GetSample(1 * TimeInterval_Minute, 2 * TimeInterval_Minute));

    // Fix capacity of the pool sizes for low-priority and dedicate nodes
    Capped_TargetLowPriorityNodes = 1;
    Capped_TargetDedicatedNodes = 0;

    // Set calculation low-priority target node value by the minimum value of this capacity and average task value
    Cal_TargetLowPriorityNodes = min(Capped_TargetLowPriorityNodes, AvgActiveTask);

    // Set low-priority target node
    $TargetLowPriorityNodes = $isWorkingWeekdayHour ? max(Cal_TargetLowPriorityNodes, Curr_TargetLowPriorityNodes) : 0;

    // Set node de-allocation mode - keep nodes active only until tasks finish
    $NodeDeallocationOption = taskcompletion;
    ```

=== "Version 02"

    Use Running Task Sample

    ```cs
    // Fix dedicate target node to zero value
    $TargetDedicatedNodes = 0;

    // Get pending tasks for the past 5 minutes.
    samples = $PendingTasks.GetSamplePercent(TimeInterval_Minute * 5);

    // Fix capacity of the pool sizes
    cappedPoolSize = 1;

    // If we have less than 70% data points, we use the last sample point, otherwise we use the average of
    // last sample point between 1 and 2 minutes
    // (for running task we use last sample point between 1 and 10 minutes).
    AvgActiveTask = samples < 70 ? max(0, $ActiveTasks.GetSample(1)) : avg($ActiveTasks.GetSample(1 * TimeInterval_Minute, 2 * TimeInterval_Minute));
    AvgRunningTask = samples < 70 ? max(0, $RunningTasks.GetSample(1)) : avg($RunningTasks.GetSample(1 * TimeInterval_Minute, 10 * TimeInterval_Minute));

    ActiveTask = AvgActiveTask > 0 ? 1 : 0;
    RunningTask = AvgRunningTask > 0 ? 1 : 0;

    // Set low-priority target node by the minimum value
    $TargetLowPriorityNodes = min(cappedPoolSize, max(ActiveTask, RunningTask));

    // Set node de-allocation mode - keep nodes active only until tasks finish
    $NodeDeallocationOption = taskcompletion;
    ```

## Method 02: Auto Scale

```text
activeTasksSampleVector = $ActiveTasks.GetSample(60 * TimeInterval_Second, 120 * TimeInterval_Second);
runningTasksSampleVector = $RunningTasks.GetSample(60 * TimeInterval_Second, 120 * TimeInterval_Second);

totalTasksVector = activeTasksSampleVector + runningTasksSampleVector;

vmsRequiredVector = totalTasksVector / 4;
vmsRequired = avg(vmsRequiredVector);

// Set dedicated target node by the minimum value from the vsm required value and capacity of 60 nodes
$TargetDedicated = min(max(vmsRequired, 1), 60);
```

> **Warning**: \
> We strongly recommend you avoid of using `GetSample(1)` in your autoscale formulas. \
> This is because `GetSample(1)` is just saying "give me the last sample you have,
> no matter how long ago you got it"  \
> Since you will use these samples to grow/shrink your pool (and your pool costs
> you money) we recommend that you base the formula on more than 1 samples worth
> of data. Instead, we suggest you do some trending type analysis and grow your
> pool based on that.

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

  ```text
  activeTasksSampleVector = $ActiveTasks.GetSample(60 * TimeInterval_Second, 120 * TimeInterval_Second);
  runningVMsSampleVector = $RunningTasks.GetSample(60 * TimeInterval_Second, 120 * TimeInterval_Second);

  vmsRequiredVector = activeTasksSampleVector / 4 + runningVMsSampleVector;
  vmsRequired = avg(vmsRequiredVector);

  // Set dedicated target node by the minimum value from the vsm required value and capacity of 60 nodes
  $TargetDedicated = min(max(vmsRequired, 1), 60);
  ```

!!! note

    You can use the `.GetSample(Interval Lookback Start, Interval Lookback End)` API
    to get a vector of samples, for example:

    ```text
    runningTasksSample = $RunningTasks.GetSample(60 * TimeInterval_Second, 120 * TimeInterval_Second);
    ```

    Might return:

    ```text
    runningTasksSample = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1];
    ```

    Or, if you would like more certainty, you can force the evaluation to fail if
    there are less than a certain percentage of samples (here percentage means that
    if in a given time interval there were supposed to be `60` samples, but actually
    due to networking failures or other issues we were only able to gather 30 samples,
    the percentage would be 50%).

    This is how you specify a percentage (note the `60` as the 3rd parameter):

    ```text
    runningTasksSample = $RunningTasks.GetSample(60 * TimeInterval_Second, 120 * TimeInterval_Second, 60);
    ```

    When specifying a time range, always start with the time range starting at least
    1m ago, since it takes about 1m for samples to propagate through the system, so
    samples in the range `(0 * TimeInterval_Second, 60 * TimeInterval_Second)` will
    often not be available. Again you can use the percentage API to force a particular
    sample percentage.

    Read More: [Autoscale Formula Improvements Needed](https://social.msdn.microsoft.com/Forums/azure/en-US/21161846-6b6b-4e34-85fc-333663414714/autoscaleformula-improvements-needed?forum=azurebatch)

## Method 03: Other Use-cases

Perhaps you want to adjust the pool size based on the day of the week and time
of day, increasing or decreasing the number of nodes in the pool accordingly:

```text
$CurTime = time();
$WorkHours = $CurTime.hour >= 8 && $CurTime.hour < 18;
$IsWeekday = $CurTime.weekday >= 1 && $CurTime.weekday <= 5;
$IsWorkingWeekdayHour = $WorkHours && $IsWeekday;
$TargetDedicated = $IsWorkingWeekdayHour ? 20 : 10;
```

This formula first obtains the current time. If it's a weekday (1-5) and within
working hours (8AM-6PM), the target pool size is set to 20 nodes. Otherwise, the
pool size is targeted at 10 nodes.

## Method 04: Other Use-cases

In this example, the pool size is adjusted based on the number of tasks in the
queue. Note that both comments and line breaks are acceptable in formula strings.

```text
// Get pending tasks for the past 15 minutes.
$Samples = $ActiveTasks.GetSamplePercent(TimeInterval_Minute * 15);

// If we have less than 70% data points, we use the last sample point, otherwise we use the maximum of
// last sample point and the history average.
$Tasks = $Samples < 70 ? max(0, $ActiveTasks.GetSample(1)) : max( $ActiveTasks.GetSample(1), avg($ActiveTasks.GetSample(TimeInterval_Minute * 15)));

// If number of pending tasks is not 0, set targetVM to pending tasks, otherwise half of current dedicated.
$TargetVMs = $Tasks > 0 ? $Tasks : max(0, $TargetDedicated/2);

// The pool size is capped at 20, if target VM value is more than that, set it to 20. This value
// should be adjusted according to your use case.
$TargetDedicated = max(0, min($TargetVMs, 20));

// Set node de-allocation mode - keep nodes active only until tasks finish
$NodeDeallocationOption = taskcompletion;
```

## Method 05: Other Use-cases

Another example that adjusts the pool size based on the number of tasks, this
formula also takes into account the `MaxTasksPerComputeNode` value that has been
set for the pool. This is particularly useful in situations where parallel task
execution on compute nodes is desired.

```text
// Determine whether 70% of the samples have been recorded in the past 15 minutes; if not, use last sample
$Samples = $ActiveTasks.GetSamplePercent(TimeInterval_Minute * 15);
$Tasks = $Samples < 70 ? max(0,$ActiveTasks.GetSample(1)) : max( $ActiveTasks.GetSample(1),avg($ActiveTasks.GetSample(TimeInterval_Minute * 15)));

// Set the number of nodes to add to one-fourth the number of active tasks (the MaxTasksPerComputeNode
// property on this pool is set to 4, adjust this number for your use case)
$Cores = $TargetDedicated * 4;
$ExtraVMs = (($Tasks - $Cores) + 3) / 4;
$TargetVMs = ($TargetDedicated+$ExtraVMs);

// Attempt to grow the number of compute nodes to match the number of active tasks, with a maximum of 3
$TargetDedicated = max(0,min($TargetVMs,3));

// Keep the nodes active until the tasks finish
$NodeDeallocationOption = taskcompletion;
```

## Method 06: Other Use-cases

This example shows an autoscale formula that sets the pool size to a certain
number of nodes for an initial time period, then adjusts the pool size based on
the number of running and active tasks after the initial time period has elapsed.

```text
string now = DateTime.UtcNow.ToString("r");
string formula = string.Format(@"
  $TargetDedicated = {1};
  lifespan         = time() - time(""{0}"");
  span             = TimeInterval_Minute * 60;
  startup          = TimeInterval_Minute * 10;
  ratio            = 50;
  $TargetDedicated = (lifespan > startup ? (max($RunningTasks.GetSample(span, ratio), $ActiveTasks.GetSample(span, ratio)) == 0 ? 0 : $TargetDedicated) : {1});
  ", now, 4);
```
The formula in the above code snippet has the following characteristics:

- Sets the initial pool size to 4 nodes
- Does not adjust the pool size within the first 10 minutes of the pool's lifecycle
- After 10 minutes, obtains the max value of the number of running and active tasks within the past 60 minutes
  - If both values are 0 (indicating no tasks were running or active in the last 60 minutes) the pool size is set to 0
  - If either value is greater than zero, no change is made

## Method 07: Other Use-cases

```text
$maxComputeNodeLimit=10;

$CurTime = time();
$WorkHours = $CurTime.hour>=8 && $CurTime.hour<18;
$IsWeekday = $CurTime.weekday>=1 && $CurTime.weekday<=1;
$IsWorkingWeekdayHour = $WorkHours && $IsWeekday;
$minCapacity = $IsWorkingWeekdayHour?1:0;

$LastSampledActiveTasks = $ActiveTasks.GetSample(1);
$LastSampledRunningTasks = $RunningTasks.GetSample(1);
$RunningAndWaiting = max($LastSampledActiveTasks,1) + max($LastSampledRunningTasks,1);
$needCompute = $RunningAndWaiting>=1;

$nodesToAllocate = $RunningAndWaiting>$maxComputeNodeLimit?$maxComputeNodeLimit:$RunningAndWaiting;
$TargetDedicated = $needCompute ? $nodesToAllocate : $minCapacity;
```

## References

- [Microsoft Azure Batch Automatic Scaling](https://learn.microsoft.com/en-us/azure/batch/batch-automatic-scaling)
- https://gordon.byers.me/azure/azure-batch-pool-auto-scale-forumulas/
- https://github.com/Huachao/azure-content/blob/master/articles/batch/batch-automatic-scaling.md
