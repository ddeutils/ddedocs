# 2.9.0

Apache Airflow 2.9.0 contains over 550 commits, which include 38 new features,
70 improvements, 31 bug fixes, and 18 documentation changes.

Airflow 2.9.0 is also the first release that supports Python 3.12.
However, Pendulum 2 does not support Python 3.12, so you’ll need to use Pendulum 3
if you upgrade to Python 3.12.

## Data Aware Scheduling

### Logical operators and conditional expressions

```python
with DAG(schedule=((dataset_1 | dataset_2) & dataset_3), ...):
    ...
```

### Combining Dataset and Time-Based Schedules

```python
with DAG(
    schedule=DatasetOrTimeSchedule(
        timetable=CronTriggerTimetable("0 0 * * *", timezone="UTC"),
        datasets=[dag1_dataset],
    ),
    ...
):
    ...
```

## Task log grouping

```python
@task
def big_hello():
    print("::group::Setup our big Hello")
    greeting = ""
    for c in "Hello Airflow 2.9":
        greeting += c
        print(f"Adding {c} to our greeting. Current greeting: {greeting}")
    print("::endgroup::")
    print(greeting)
```

## References

- [Apache Airflow 2.9.0: Dataset and UI Improvements](https://medium.com/apache-airflow/apache-airflow-2-9-0-dataset-and-ui-improvements-dfed574ed530)
- [GitHub - Apache Airflow 2.9.0](https://github.com/apache/airflow/releases/tag/2.9.0)
