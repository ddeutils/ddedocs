---
icon: material/engine-outline
---

# Data Observability

**Data Observability** is an organization’s ability to fully understand the health of
the data in their systems. Data observability eliminates data downtime by applying
best practices learned from DevOps to data pipeline observability.

## Getting Started

Data observability tools use automated monitoring, automated root cause analysis,
data lineage and data health insights to detect, resolve, and prevent data anomalies.
This leads to healthier pipelines, more productive teams, better data management,
and happier customers.

For data engineers and developers, data observability is important because data
downtime means wasted time and resources; for data consumers, it erodes confidence
in your decision-making.

!!! quote

    **Data Downtime**: periods of time when data is partial, erroneous, missing,
    or otherwise inaccurate. Only multiplies as data systems become increasingly
    complex, supporting an endless ecosystem of sources and consumers.

**The 5 pillars of data observability**:

1.  **Freshness**:

    Freshness seeks to understand how up-to-date your data tables are, as well as
    the cadence at which your tables are updated. Freshness is particularly important
    when it comes to decision-making; after all, stale data is basically synonymous
    with wasted time and money.

2.  **Quality**:

    Your data pipelines might be in working order but the data flowing through them
    could be garbage. The quality pillar looks at the data itself and aspects such
    as percent NULLS, percent uniques and if your data is within an accepted range.
    Quality gives you insight into whether or not your tables can be trusted based
    on what can be expected from your data.

3.  **Volume**:

    Volume refers to the completeness of your data tables and offers insights on the
    health of your data sources. If 200 million rows suddenly turns into 5 million,
    you should know.

4.  **Schema**:

    Changes in the organization of your data, in other words, schema, often indicates
    broken data. Monitoring who makes changes to these tables and when is foundational
    to understanding the health of your data ecosystem.

5.  **Lineage**:

    When data breaks, the first question is always “where?” Data lineage provides
    the answer by telling you which upstream sources and downstream ingestors were
    impacted, as well as which teams are generating the data and who is accessing it.
    Good lineage also collects information about the data (also referred to as metadata)
    that speaks to governance, business, and technical guidelines associated with
    specific data tables, serving as a single source of truth for all consumers.

Together, these components provide valuable insight into the quality and reliability
of your data. Let’s take a deeper dive.

## The key features of data observability tools

Evaluation criteria can be tricky when you may not even have a strong answer to
the basic question, "what are data observability tools?" A great data observability
platform has the following features:

- **It connects to your existing stack quickly and seamlessly** and does not require
  modifying your data pipelines, writing new code, or using a particular programming
  language. This allows quick time to value and maximum testing coverage without
  having to make substantial investments.

- **It monitors your data at-rest** and does not require extracting the data from where
  it is currently stored. This allows the data observability solution to be performant,
  scalable and cost-efficient. It also ensures that you meet the highest levels
  of security and compliance requirements.

- **It requires minimal configuration** and practically no threshold-setting. Data
  observability tools should use machine learning models to automatically learn
  your environment and your data. It uses anomaly detection techniques to let you
  know when things break. It minimizes false positives by taking into account not
  just individual metrics, but a holistic view of your data and the potential impact
  from any particular issue. You do not need to spend resources configuring and
  maintaining noisy rules within your data observability platform.

- **It requires no prior mapping** of what needs to be monitored and in what way.
  It helps you identify key resources, key dependencies and key invariants so that
  you get broad data observability with little effort.

- **It provides rich context** that enables rapid triage and troubleshooting, and
  effective communication with stakeholders impacted by data reliability issues.
  Data observability tools should not stop at “field X in table Y has values lower
  than Z today.”

- **It prevents issues from happening in the first place** by exposing rich information
  about data assets so that changes and modifications can be made responsibly and
  proactively.

## References

- [MontecarloData: What is Data Observability](https://www.montecarlodata.com/blog-what-is-data-observability/)
- https://www.montecarlodata.com/blog-data-observability-tools/
- https://snowplow.io/blog/data-observability-dashboard/
- https://www.youtube.com/watch?v=4K33fP46vDw
- https://www.montecarlodata.com/blog-what-is-data-observability/
