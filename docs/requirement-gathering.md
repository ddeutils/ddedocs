# Requirement Gathering

One of the mistakes you’ll make as a Data Engineer is not truly understanding the
^^**Business Requirements**^^.

!!! example

    !!! quote

        The business will come to you and ask for a real-time dashboard.[^1]

    But they mean they want the data updated 3-4x a day, or maybe they only look at
    the report once a week; at that moment, the data should be as up-to-date as
    possible.

## :material-arrow-down-right: Getting Started

### Identify the End-Users

:material-page-last: Begin by identifying the end-users, crucial stakeholders
who utilize the project's output
(Understanding the capabilities and preferences of the end-user is crucial
for designing an appropriate solution).

End-users (& their preferences) for data projects are usually one of;

<div class="grid cards" markdown>

-   **Data Analysts/Data Scientists**

    _SQL, No-SQL, CSV files_

-   **Business Users**

    _Dashboards, Reports, Excel files_

-   **Software Engineers**

    _SQL, APIs, CRMs, JSON files_

-   **External Clients**

    _Cloud storage, SFTP/FTP, APIs, SQL_

</div>

!!! warning

    If you do not know who is the end users, you can ask the Solution Architect
    in that data project.

---

### Help End-Users Define Requirements

!!! note

    Understand The Business - Not Just The Technical Requirements

:material-page-last: Assist end-users in defining requirements by engaging in
conversations about their objectives and challenges.
Understand their current operations to gain valuable insights.

Use the following questions to refine requirements:

-   **Business Impact**

    Evaluate how the data impacts the business and quantify the improvements.

    - ^^How does having this data impact the business?^^
    - What is the measurable improvement in the bottom line, business OKR, etc?
      Knowing the business impact helps in determining if this project is worth
      doing.

-   **Semantic Understanding**

    - What does the data represent? What business process generates this data?
      Knowing this will help you model the data and understand its relation to other
      tables in your warehouse.

    Grasp the data's representation and its relation to other warehouse tables.

-   **Data Source**

    Where does the data originate?
    (an application database, external vendor via SFTP/Cloud store dumps,
    API data pull, manual upload, etc).

-   **Frequency of Data Pipeline**

    - How fresh does the data need to be? (n minutes, hourly, daily, weekly, etc).
    - Is there a business case for not allowing a higher frequency?
    - What is the highest frequency of data load acceptable by end-users?

-   **Data Output Requirements**

    - What is the data output schema? (table name, column names, API field names,
      Cloud storage file name/size, etc)

-   **Historical Data**

    - Does historical data need to be stored? When loading data into a warehouse,
      the answer is usually yes.

-   **Data Caveats**

    - Does the data have any caveats? (e.g. seasonality affecting size, data skew,
      inability to join, or data unavailability).
    - Are there any known issues with upstream data sources, such as late arriving
      data, or missing data?

-   **Access Pattern**

    - How will the end user access the data? Is access via SQL, dashboard tool,
      APIs, or cloud storage? In the case of SQL or dashboard access, What are the
      commonly used filter columns (e.g. date, some business entity)?
    - What is the expected access latency?

-   **Business Rules Check (QA)**

    - What data quality metrics do the end-users care about?
    - What are business logic-based data quality checks? Which numeric fields
      should be checked for divergence (e.g. can’t differ by more than x%) across
      data pulls?

:material-page-last: Show appreciation to end-users for their time, keep them
updated on progress, incorporate their feedback, suggest solutions for common
issues, and acknowledge their expertise when presenting the project to a wider
audience.

Clearly define the requirements, record them (e.g. JIRA, etc), and get sign-off
from the stakeholders.

---

### End-User Validation

:material-page-last: Provide end-users with sample data for analysis, allowing
them to validate its accuracy and usability.
Record any new requirements or changes, getting sign-off from stakeholders before
proceeding.

Record any new requirements or changes (e.g. JIRA, etc), and get sign-off from
the stakeholders. Do not start work on the transformation logic until you get a
sign-off from the stakeholders.

---

### Deliver Iteratively

:material-page-last: Break down large projects into smaller, manageable parts and
work with stakeholders to set timelines and priorities.
This approach facilitates a short feedback cycle, making it easier to adapt to
changing requirements. Track progress with clear acceptance criteria.

!!! example

    If you are building an ELT pipeline (REST API => dashboard), you can split
    it into modeling the data, pulling data from a REST API, loading it into a
    raw warehouse table, & building a dashboard for the modeled data.

Delivering in small chunks enables a short feedback cycle from the end-user making
changing requirements easy to handle. Track your work (tickets, etc) with clear
acceptance criteria.

---

### Handling Changing Requirements/New Features

:material-page-last: Establish a process for handling change or feature requests,
ensuring end-users can request modifications.
Prioritize requests with stakeholder input, communicate delivery timelines, and
educate end-users on the request process to prevent scope creep and maintain
timely delivery.

!!! warning

    Do not accept Adhoc change/feature requests! (unless it’s an emergency).

Create a process to ...

- Allow end-users to request changes/features
- Prioritize the change/feature requests with help from stakeholders
- Decide and communicate delivery timelines to end-users

Educate the end-user on the process of requesting a new feature/change.
Following a process will prevent scope creep and allow you to deliver on time.

---

## Examples

### Project Starter

| Question                                                 | Answer                                                                         |
|----------------------------------------------------------|--------------------------------------------------------------------------------|
| What responsibility of a data engineer on this project?  | Load all data sources from RDBMS to the warehouse for making dashboards by DA. |

### Data Component

| Question                                                        | Answer                                                                                                                                   |
|-----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| What is the data source system type?                            | RDBMS (Postgres, MySQL, SQL Server, etc.),<br>NO-SQL (MongoDB, Elastic),<br>API                                                          |
| What is data compute service to extract from the source system? | Docker Application (FastAPI), Batch job via Cloud services (Azure Batch, AWS Batch, etc.) ETL Services (Azure Databricks, AWS Glue etc.) |
| How to authenticate to the data source system?                  | Use user and password. Use service account on that cloud provider.                                                                       |

### Data Source

These questions use per data source.

| Question                                                                 | Answer                                                                                  |
|--------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| What is data source name?                                                |                                                                                         |
| What is the schema of this source (column and data type docs)?           |                                                                                         |
| What is the primary of this data source?                                 |                                                                                         |
| How to ingest data to this data source?                                  |                                                                                         |
| How to incremental load of this data source?                             | The filter fields for filter period of changed data like create_date, updated_date etc. |
| What is loading type of this data source?                                | Incremental via Merge or Append.<br>Full-dump load.                                     |
| When to load this data source that does not effect to the source system? | Every 1:30 AM to 3:00AM is good or not?                                                 |
| What is the rule check for this data?                                    |                                                                                         |

## :material-source-commit-end: Conclusion

Effectively managing ever-changing requirements is a challenging aspect of a
data engineer's role. By following the steps outlined in this article, you can
navigate these challenges, ensuring timely project delivery, making a significant
impact, enjoying your work on data projects, and fostering supportive end-users.

The next time you start a data project, follow the steps shown above to

<div class="grid cards" markdown>

- Deliver on Time
- Make a Huge Impact
- Make working on the data projects a Joy
- Build supportive end-users

</div>

[^1]: [Becoming a Better Data Engineer Tips](https://seattledataguy.substack.com/p/becoming-a-better-data-engineer-tips)
[^2]: [How to gather requirements for your data project](https://www.startdataengineering.com/post/n-questions-data-pipeline-req/)
