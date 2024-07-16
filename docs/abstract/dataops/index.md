---
icon: material/hexagon-multiple-outline
---

# DataOps

!!! note

    **DataOps** is a collection of practices that focuses on breaking down silos
    between data producers and consumers, improving data quality and transparency
    of results.[^1]

<figure markdown="span">
  ![DataOps Flow Main](./img/dataops-flow-main.png){ loading=lazy width="550" }
  <figcaption>DataOps Flow</figcaption>
</figure>

**DataOps (Data Operations)** provides a collaboration of data engineering,
data science and operations team.
It aims to automate the delivery of the right and reliable data to appropriate
teams through a much faster approach. And this leads to better data productivity
and enhanced human communication.

<figure markdown="span">
  ![DataOps](img/dataops.png){ loading=lazy width="600" }
  <figcaption>DataOps</figcaption>
</figure>

## :material-arrow-down-right: Getting Started

### DataOps vs. DevOps

The key difference is DevOps is a methodology that brings development and
operations teams together to make software development and delivery more
efficient, while DataOps focuses on breaking down silos between data producers
and data consumers to make data more reliable and valuable.

!!! quote

    To keep a constant pulse on the overall health of their systems,
    DevOps engineers leverage observability to monitor, track, and triage incidents
    to prevent application downtime.

Software observability consists of three pillars:

- **Logs**: A record of an event that occurred at a given timestamp. Logs also provide context to that specific event that occurred.
- **Metrics**: A numeric representation of data measured over a period of time.
- **Traces**: Represent events that are related to one another in a distributed environment.

![DataOps vs. DevOps—similarities and differences](./img/dataops-vs-devops.png)


**Data Observability** is an organization’s ability to fully understand the health
of the data in their systems. It reduces the frequency and impact of data downtime
(periods of time when your data is partial, erroneous, missing or otherwise inaccurate)
by monitoring and alerting teams to incidents that may otherwise go undetected
for days, weeks, or even months.

Like software observability, data observability includes its own set of pillars:

- **Freshness**: Is the data recent? When was it last updated?
- **Distribution**: Is the data within accepted ranges? Is it in the expected format?
- **Volume**: Has all the data arrived? Was any of the data duplicated or removed from tables?
- **Schema**: What’s the schema, and has it changed? Were the changes to the schema made intentionally?
- **Lineage**: Which upstream and downstream dependencies are connected to a given data asset? Who relies on that data for decision-making, and what tables is that data in?

[Read More about Data Observability](../data_observability/index.md)

### Framework

![DataOps Flow](./img/dataops-flow.png)

To facilitate faster and more reliable insight from data, DataOps teams apply a
continuous feedback loop, also referred to as the DataOps lifecycle.

Here is what the DataOps lifecycle looks like in practice:

- **Planning**: Partnering with product, engineering, and business teams to set
  KPIs, SLAs, and SLIs for the quality and availability of data
  (more on this in the next section).

- **Development**: Building the data products and machine learning models that
  will power your data application.

- **Integration**: Integrating the code and/or data product within your existing
  tech and or data stack. (For example, you might integrate a dbt model with
  Airflow so the dbt module can automatically run.)

- **Testing**: Testing your data to make sure it matches business logic and meets
  basic operational thresholds (such as uniqueness of your data or no null values).

- **Release**: Releasing your data into a test environment.
- **Deployment**: Merging your data into production.

- **Operate**: Running your data into applications such as Looker or Tableau
  dashboards and data loaders that feed machine learning models.

- **Monitor**: Continuously monitoring and alerting for any anomalies in the data.

This cycle will repeat itself over and over again.
However, by applying similar principles of DevOps to data pipelines, data teams
can better collaborate to identify, resolve, and even prevent data quality issues
from occurring in the first place.

## Noted

- Continuous Integration/Continuous Deployment for Data
- Automated Testing for Data Pipelines
- Data Observability
- Incident Management for Data Systems

---

- Data Pipeline Orchestration
- Continuous Integration/Continuous Deployment (CI/CD) for Data
- Data Observability
- Automated Data Quality Checks

## Roles

### DataOps Engineer

**DataOps Engineer** create and implement the processes that enable successful
teamwork within the data organization.
They design the orchestrations that enable work to flow seamlessly from development
to production. They make sure that environments are aligned and that hardware,
software, data, and other resources are available on demand.

- [:simple-medium: 10 New DevOps Tools to Watch in 2024](https://medium.com/4th-coffee/10-new-devops-tools-to-watch-in-2024-a5127c0b3411)
- [:simple-medium: Is Data Observability Critical to Successful Data Analytics?](https://sanjmo.medium.com/is-data-observability-critical-to-successful-data-analytics-d09b983b95c6)

## Examples

- [:material-github: DataOps for the Modern Data Warehouse](https://github.com/Azure-Samples/modern-data-warehouse-dataops)

[^1]: [:simple-medium: Data Engineering concepts: Part 7, DevOps, DataOps and MLOps](https://medium.com/@mudrapatel17/data-engineering-concepts-part-7-devops-dataops-and-mlops-afc6f432473c)
