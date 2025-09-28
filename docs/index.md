# **Data Develop & Engineer**

> **_Disclaimer_**: This docs add-on my opinion from a data engineer experiences
> and experiments since 2019.

!!! warning "Important"

    I do not have much proper _English_ grammar because I am in the middle level
    (I try to practice on writing and reading more and more).
    Please understand this problem and open your mind before continue to read this
    documents :face_holding_back_tears:

This project will deliver all Practice and Knowledge in **Data Developer and Engineer**.

---

## :material-arrow-down-right: Getting Started

&nbsp;&nbsp;&nbsp;&nbsp; :material-page-last: First, ^^**Data Engineering** is a
crucial part of the ==Data Lifecycle==, enabling organizations to process and manage
large volumes of data efficiently, reliably, and at scale.^^[^3]

In this context, a **Data Engineer** is responsible for designing and implementing
**Data Pipelines** and **Data Management Strategies** that align with organizational
requirements and KPIs, ensuring data is handled _consistently_ and _reliably_.

!!! quote "What does a Data Engineer do?"

    A **Data Engineer** is someone who can ==_**Develop**_, _**Implement**_,
    _**Operate**_, and _**Maintain**_== the tools and systems that form the
    organization’s **Data Infrastructure**—whether on-premises or in the cloud.
    This infrastructure includes databases, storage systems, compute engines,
    and data pipelines that power data-driven operations.[^1]

<figure markdown="span">
  ![Life Cycle of Data Engineering](img/life-cycle-of-data-engineering.png){ loading=lazy width="650" }
  <figcaption><a href="https://www.techment.com/unlocking-the-power-of-data-a-beginners-guide-to-data-engineering/">Life Cycle of Data Engineering</a></figcaption>
</figure>

!!! quote "Fundamentals of Data Engineering"

    **Data Engineering** is the development, implementation, and maintenance of
    systems and processes that transform raw data into high-quality, consistent
    information. This information then powers downstream use cases such as
    analytics and machine learning.

    At its core, **data engineering** sits at the intersection of security,
    data management, DataOps, data architecture, orchestration, and software
    engineering.

    A **Data Engineer** manages the ^^Data Engineering Lifecycle^^, starting
    with ingesting data from source systems and ending with serving it for
    consumption—whether for reporting, analytics, or machine learning.

    — Joe Reis and Matt Housley, [*Fundamentals of Data Engineering*](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/)

The stages of this lifecycle typically include **Data Ingestion**,
**Data Transformation**, **Data Storage**, and **Data Serving**.

| Best practice               | Why it matters                                                                                                 |
|-----------------------------|----------------------------------------------------------------------------------------------------------------|
| Proactive data monitoring   | Detects anomalies and ensures data integrity by flagging missing, duplicate, or inconsistent records.          |
| Schema drift management     | Handles structural changes in data to prevent pipeline failures and maintain compatibility.                    |
| Continuous documentation    | Improves discoverability and understanding by capturing descriptive information about data assets.             |
| Data security measures      | Protects sensitive information by controlling access and enforcing compliance standards.                       |
| Version control and backups | Preserves historical states of data for reproducibility, auditing, and recovery in case of corruption or loss. |

:material-page-last: As I’ve grown into this role, I’ve realized how quickly the
**data engineering landscape evolves**. Just three years ago, I was working with
MapReduce on **Hadoop HDFS**. Today, the focus has shifted toward in-memory
processing engines like **Impala** and **Apache Spark**.

The key takeaway? While tools may come and go, the fundamental skills and
concepts—such as distributed processing, data modeling, and lifecycle management—
remain invaluable :boom:.

![The 2023 MAD (ML/AI/DATA) Landscape](img/mad-data-landscape.png){ loading=lazy width="370" align=right }
The right picture, the [**2023 MAD (ML/AI/Data) Landscape** :material-land-plots:](https://mad.firstmark.com/)[^2],
that show about how many possibility tools that able to use on your project.
It has many area that you should to choose which one that match with the current
architect or fit with your cost planing model.

---

:material-page-last: Finally, the below diagram shows ^^how the focus areas of
**Data Engineering Shift** as the analytics organization evolves^^.
That mean Data Engineer does not create a part of data ingestion or serving only.
When data engineering tools change very quickly, The focus of data engineers has
changed as well.

<figure markdown="span">
  ![Data Engineering Shifting](img/data-engineering-shift.png){ loading=lazy width="700" }
  <figcaption><a href="https://medium.com/@AnalyticsAtMeta/the-future-of-the-data-engineer-part-i-32bd125465be">Data Engineering Shift</a></figcaption>
</figure>

Based upon this illustration, we can observe three distinct focus areas for the
role:

- **Data Infrastructure**: One example of a problem being solved in this instance might
  be setting up a spark cluster for users to issue HQL queries against data on S3.

- **Data Integration**: An example task would be creating a dataset via SQL query,
  joining tens of other datasets, and then scheduling the query to run daily using
  the orchestration framework.

- **Data Accessibility**: An example could be enabling end-users to analyze significant
  metrics movements in a self-serve manner.

---

:material-page-last: The trend of ^^**Modern Data Stack**^^ will make a data
engineering process so easy to implement and maintenance that making you have
the time to focus on **business problem** instead technical problem.

In the another side, **Business users** able to use less of technical knowledge
to interact the serving data in their **data contract platform**.
It decreases SLA to require the **data engineer** for need support a lot! :partying_face:

You can follow the modern data stack on the below topics:

<div class="grid cards" markdown>

- [**Services**](./services/index.md)
- [**Tools**](./tools/index.md)

</div>

---

## :material-account-arrow-right-outline: Roles

:material-page-last: In the future, if I do not in love with communication or management
skill that make me be :material-face-agent: [**Lead Data Engineer**](lead-data-engineer.md),
I will go to any specialize roles such as,

<div class="grid cards" markdown>

-   :material-face-man: **Data Platform Engineer**

    ---
    Data Platform Engineer

    [Read More about **Data Architect**](./abstract/data_architecture/index.md)

-   :material-face-man-shimmer: **DataOps Engineer**

    ---
    DataOps Engineer

    [Read More about **DataOps**](./abstract/dataops/index.md)

-   :material-face-man-profile: **MLOps Engineer**

    ---
    MLOps Engineers Build and Maintain a platform to enable the development
    and deployment of machine learning models. They typically do that
    through standardization, automation, and monitoring.

    MLOps Engineers reiterate the platform and processes to make the machine
    learning model development and deployment quicker, more reliable, reproducible,
    and efficient.

    [Read More about **MLOps**](./abstract/mlops/index.md)

-   :material-face-woman: **Analytic Engineer**

    ---
    Analytic Engineer is who make sure that companies can understand their data
    and use it to _Solve Problems_, _Answer Questions_, or _Make Decisions_.

    [Read More about **Analytic Engineer**](https://towardsdatascience.com/analytics-engineering-8b0ed0883379)

</div>

The role from above, I reference from ^^Types of Data Professionals^^[^4].

---

## :material-account-supervisor-outline: Communities

:material-page-last: This below is the list of Communities that you must join for
keep update knowledge for [Developer and Data Engineer trends](./abstract/emerging_trends/index.md).

<div class="grid cards" markdown>

-   [:simple-medium: **Data Engineering**](https://medium.com/tag/data-engineering)

    ---
    The **Medium Tag** for Data Engineering knowledge and solutions :octicons-share-android-24:

-   [:material-coffee-to-go-outline: **Data Engineer Cafe**](https://discuss.dataengineercafe.io/)

    ---
    An **Area of Discussing Blog** for Data Engineer like talk to your close friend
    at the Cafe :material-coffee-maker-outline:

-   [:simple-medium: **ODDS Team**](https://medium.com/tag/data-engineering)

    ---
    The **Medium Group** that believes software development should be joyful and
    advocates deliberate practice :material-human-greeting-proximity:

-   [:material-map-marker-path: **TPA Roadmap**](https://roadmap.thaiprogrammer.org/)

    ---
    **Community Driven Roadmaps, Articles and Resources** for developers in Thailand

-   [:material-package-variant-plus: **TestDriven**](https://testdriven.io/)

    ---
    Learn to build high-quality web apps with **best practices**

-   [:material-brain: **Second Brain**](https://www.ssp.sh/brain/data-engineering/)

    ---
    My inspiration Data Engineering document website.

</div>

[^1]: Information of this quote reference from [:simple-medium: What is Data Engineering?](https://medium.com/codex/what-is-data-engineering-407bcf860baf)
[^2]: [:material-land-plots: The 2023 MAD (ML/AI/DATA) Landscape](https://mad.firstmark.com/)
[^3]: Unlocking the Power of Data: [:material-web:A Beginner’s Guide to Data Engineering](https://www.techment.com/unlocking-the-power-of-data-a-beginners-guide-to-data-engineering/)
[^4]: Types of Data Professionals, credit to [:material-linkedin: Kevin Rosamont Prombo](https://www.linkedin.com/in/krosamont/) for creating the [Infographic](https://kevros.shinyapps.io/radar_skills/)
