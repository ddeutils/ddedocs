# Sensor

**SensorOperator** is an Operator that will block our DAG by keep checking a
certain condition until that condition was met.

## :material-arrow-down-right: Getting Started

### FileSensor

!!! note

    **FileSensor** is a sensor that will keep checking if the target file exists
    or not.

This is an example to use the **FileSensor** to check `/home/hello.txt`.
The task `waiting_for_file` will keep running until the target file exists.

```python
from airflow.models import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.empty import EmptyOperator
from pendulum import datetime, now

with DAG(
    dag_id='medium_file_sensor',
    schedule='@daily',
    catchup=False,
    start_date=datetime(2024,3,1),
    max_active_runs=1
):
    start = EmptyOperator(task_id='start')
    waiting_for_file = FileSensor(
        task_id='waiting_for_file',
        filepath='/home/hello.txt'
    )
    end = EmptyOperator(task_id='end')

    start >> waiting_for_file >> end
```

### DateTimeSensor

!!! note

    **DateTimeSensor** is a sensor that will keep checking if current time pass
    the target datetime or not.

This is an example to use the **DateTimeSensor** to check if current time pass
`2024-03-10 4:35 PM (UTC+7)`. The task waiting_for_datetime will keep running
until pass the target time.

```python
from airflow.models import DAG
from airflow.sensors.date_time import DateTimeSensor
from airflow.operators.empty import EmptyOperator
from pendulum import datetime, now


with DAG(
    dag_id='medium_datetime_sensor',
    schedule='@daily',
    catchup=False,
    start_date=datetime(2024,3,1),
    max_active_runs=1
):
    start = EmptyOperator(task_id='start')
    waiting_for_datetime = DateTimeSensor(
        task_id='waiting_for_datetime',
        target_time=datetime(2024,3,10,16,36,tz= 'Asia/Bangkok')
    )
    end = EmptyOperator(task_id='end')

    start >> waiting_for_datetime >> end
```

### PythonSensor

!!! note

    **PythonSensor** is a sensor that will execute Python to do something to return
    Boolean value, if it’s `True` then process to the next step.

!!! note

    Additionally, PythonSensor also able to pass a value to Airflow’s XCom.

This is an example of how to **PythonSensor** to check if current time pass
`2024-03-10 4:35 PM (UTC+7)` just like **DateTimeSensor** and it will also send
the string Hello word to Airflow's XCom for the next task.

```python
from airflow.models import DAG
from airflow.decorators import task
from airflow.sensors.base import PokeReturnValue
from airflow.operators.empty import EmptyOperator
from pendulum import datetime, now


with DAG(
    dag_id='medium_python_sensor',
    schedule='@daily',
    catchup=False,
    start_date=datetime(2024,3,1),
    max_active_runs=1
):
    start= EmptyOperator(task_id='start')

    @task.sensor(task_id='check_datetime_python')
    def check_datetime_python_task() -> PokeReturnValue:
        # Check current > target
        condition_met = now() >= datetime(2024,3,10,16,36,tz= 'Asia/Bangkok')
        if condition_met :
            # Return Something
            operator_return_value = 'hello world'
        else:
            # Return Value as None if condition doesn't met
            operator_return_value = None
        # Return Poke Value
        return PokeReturnValue(
            is_done=condition_met,
            xcom_value=operator_return_value,
        )

    @task(task_id= 'print_value')
    def print_value_task(content) :
        print(content)

    check_datetime_python = check_datetime_python_task()
    print_value = print_value_task(check_datetime_python)

    # End
    end = EmptyOperator(task_id='end')
    # Set Dependencies Flow
    start >> check_datetime_python >> print_value >> end
```

### ExternalTaskSensor

!!! note

    **ExternalTaskSensor** is a sensor that will keep checking one of these:

    - Check if a certain task in the upstream DAG is finish or not.
    - Check if the upstream DAG is finish or not.

!!! note

    *DAG Run Date of both upstream DAG and Sensor must be the same.

This is an example to use the **ExternalTaskSensor** if the upstream DAG named
`medium_datetime_sensor` from the previous example finish or not.
One good thing about this sensor is that we can re-direct into the upstream DAG
using the External DAG button in the UI.

```python
from airflow.models import DAG
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.empty import EmptyOperator
from pendulum import datetime, now


with DAG(
    dag_id='medium_external_sensor',
    schedule='@daily',
    catchup=False,
    start_date=datetime(2024, 3, 1),
    max_active_runs=1
):
    start = EmptyOperator(task_id='start')
    waiting_for_upstream = ExternalTaskSensor(
        task_id='waiting_for_upstream',
        external_dag_id='medium_datetime_sensor',
        # None for DAG finish, Task_id for specific task
        external_task_id=None
    )
    end = EmptyOperator(task_id= 'end')

    start >> waiting_for_upstream >> end
```

!!! warning

    Something to be aware of is that the default **ExternalTaskSensor** will only
    check the upstream DAG’s status only when the current DAG and the upstream
    DAG have exactly the same DAG execution date.

    But we can make some adjustments with the `execution_date_fn` parameter.

    This is an example if we want the current DAG to check the upstream DAG from
    previous date.

    ```python
    waiting_for_upstream = ExternalTaskSensor(
        task_id='waiting_for_upstream',
        external_dag_id='medium_datetime_sensor',
        # None for DAG finish, Task_id for specific task
        external_task_id=None,
        # Input of function is DAG execution date (pendulum datetime)
        execution_date_fn=(lambda dt : dt.add(days= -1))
    )
    ```

### Idempotent SensorOperator

!!! note

    From my previous article about Idempotent DAG [HERE](https://medium.com/@chanon.krittapholchai/apache-airflow-useful-practices-idempotent-dag-6d52b1594704).

We also want our **SensorOperator** to has an Idempotent behavior too.
That could be done with the same template method as the previous article.

This is an example of a simple DAG with **Idempotent FileSensor** and
**Idempotent DateTimeSensor**. It will create a DAG which apply the Idempotent
concept into sensors.

```python
from airflow.models import DAG
from airflow.sensors.date_time import DateTimeSensor
from airflow.sensors.filesystem import FileSensor
from airflow.operators.empty import EmptyOperator
from pendulum import datetime, now


with DAG(
    dag_id='medium_idempotent_sensor',
    schedule='@daily',
    catchup=False,
    start_date=datetime(2024,3,1),
    max_active_runs=1
):
    start = EmptyOperator(task_id='start')
    waiting_for_datetime= DateTimeSensor(
        task_id='waiting_for_datetime',
        target_time='{{ data_interval_end.in_tz("Asia/Bangkok").replace(hour= 23) }}'
    )
    waiting_for_file= FileSensor(
        task_id='waiting_for_file',
        # File name is hello_YYYYMMDD.txt
        filepath='/home/hello_{{ data_interval_end.in_tz("Asia/Bangkok").strftime("%Y%m%d") }}.txt',
    )
    end = EmptyOperator(task_id= 'end')

    start >> [waiting_for_datetime, waiting_for_file] >> end
```

## :material-arrow-right-bottom: Others

There are many useful things that we can apply to optimize our Sensor.

### SensorOperator PokeInterval & Timeout

Every SensorOperators are built-in with these parameters.

1) `poke_interval`: After check, how long should the Sensor wait before check again.
2) `timeout`: How long can this Sensor wait before raise an error.

Here is the sample of these parameters.

```python
FileSensor(
    task_id='waiting_for_file',
    filepath='/home/hello.txt',
    poke_interval=30, # Check every 30 seconds
    timeout=3600 # After 1st poke, will wait for 1 hour before raise an error
)
```

### SensorOperator Mode

Mode is the behavior of the Sensor during the poke_interval, there are 3 different
modes.

1) `poke` : Sensor will be active, it’s fast but it will consume resources.

2) `reschedule` : Sensor will be inactive, slower but consume less resources.

3) `deferrable` : Consume even less resource and even slower than reschedule.
   (Don’t forget to `airflow triggerer` before use deferrable.)

!!! note

    **Deferrable** is more complicate than poke and reschedule. If you want to
    understand how it works, I suggest taking this free course from Astronomer:
    [Airflow: Deferrable Operators (astronomer.io)](https://academy.astronomer.io/astro-runtime-deferrable-operators)

Here is the example of how to use each mode with DateTimeSensor.

```python
from airflow.models import DAG
from airflow.sensors.date_time import DateTimeSensor, DateTimeSensorAsync
from pendulum import datetime, now


with DAG(
    dag_id='medium_poke',
    schedule='@daily',
    catchup=True,
    start_date=datetime(2024,1,1),
):
    poke = DateTimeSensor(
        task_id='waiting_for_datetime',
        target_time="{{ data_interval_end.add(years= 1) }}",
        mode='poke'
    )


with DAG(
    dag_id='medium_reschedule',
    schedule='@daily',
    catchup=True,
    start_date=datetime(2024,1,1),
):
    reschedule = DateTimeSensor(
        task_id='waiting_for_datetime',
        target_time="{{ data_interval_end.add(years= 1) }}",
        mode='reschedule'
    )


with DAG(
    dag_id='medium_deferrable',
    schedule='@daily',
    catchup=True,
    start_date=datetime(2024,1,1),
):
    deferrable = DateTimeSensorAsync(
        task_id='waiting_for_datetime',
        target_time="{{ data_interval_end.add(years= 1) }}"
    )
```

## :material-playlist-plus: Read Mores

- [Airflow - Sensor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html)
- [Astronomer - Airflow Sensor](https://www.astronomer.io/docs/learn/what-is-a-sensor)
- [Apache Airflow Useful Practices: Sensor Operator](https://medium.com/@chanon.krittapholchai/apache-airflow-useful-practices-sensor-operator-ead91b9f3884)
