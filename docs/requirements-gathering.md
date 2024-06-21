---
icon: material/comment-search-outline
---

# Requirements Gathering

## :material-arrow-down-right: Getting Started

One of the mistakes you’ll make as a Data Engineer is not truly understanding the
business requirements.

!!! quote

    The business will come to you and ask for a real-time dashboard.[^1]

But they mean they want the data updated 3-4x a day, or maybe they only look at
the report once a week; at that moment, the data should be as up-to-date as
possible.

### Identify the End-Users

Begin by identifying the end-users, crucial stakeholders who utilize the project's
output. Understanding the capabilities and preferences of the end-user is crucial
for designing an appropriate solution.

End-users (& their preferences) for data projects are usually one of:

- Data analysts/Scientists: SQL, CSV files
- Business users: Dashboards, reports, Excel files
- Software engineers: SQL, APIs, CRMs
- External clients: Cloud storage, SFTP/FTP, APIs

### Help End-Users Define Requirements

!!! note

    Understand The Business - Not Just The Technical Requirements

Assist end-users in defining requirements by engaging in conversations about their
objectives and challenges. Understand their current operations to gain valuable
insights. Use the following questions to refine requirements:

- Business impact:

  How does having this data impact the business? What is the measurable improvement in the bottom line, business OKR, etc? Knowing the business impact helps in determining if this project is worth doing.

  Evaluate how the data impacts the business and quantify the improvements.

- Semantic understanding:

  What does the data represent? What business process generates this data? Knowing this will help you model the data and understand its relation to other tables in your warehouse.

  Grasp the data's representation and its relation to other warehouse tables.

- Data source: Where does the data originate? (an application DB, external vendor via SFTP/Cloud store dumps, API data pull, manual upload, etc).

- Frequency of data pipeline: How fresh does the data need to be? (n minutes, hourly, daily, weekly, etc). Is there a business case for not allowing a higher frequency? What is the highest frequency of data load acceptable by end-users?

- Historical data: Does historical data need to be stored? When loading data into a warehouse, the answer is usually yes.

- Data caveats: Does the data have any caveats? (e.g. seasonality affecting size, data skew, inability to join, or data unavailability). Are there any known issues with upstream data sources, such as late arriving data, or missing data?

- Access pattern: How will the end user access the data? Is access via SQL, dashboard tool, APIs, or cloud storage? In the case of SQL or dashboard access, What are the commonly used filter columns (e.g. date, some business entity)? What is the expected access latency?

- Business rules check (QA): What data quality metrics do the end-users care about? What are business logic-based data quality checks? Which numeric fields should be checked for divergence (e.g. can’t differ by more than x%) across data pulls?

- Data output requirements: What is the data output schema? (column names, API field names, Cloud storage file name/size, etc)

Show appreciation to end-users for their time, keep them updated on progress,
incorporate their feedback, suggest solutions for common issues, and acknowledge
their expertise when presenting the project to a wider audience.

Answering the above questions will give you a good starting point.

Help the end-users feel invested in the project by following the steps below.

Thank end-users for their time/expertise

- Update them on progress
- Ask & incorporate their feedback
- Recommend solutions(or different ways to do things) for their common issues
- Acknowledge their help & expertise when presenting the project to a wider audience

End-users who feel invested will root for the project, and help evangelize it. Having end-users who root for the project helps a lot with resource allocation.

Clearly define the requirements, record them (e.g. JIRA, etc), and get sign-off from the stakeholders.

### End-User Validation

Provide end-users with sample data for analysis, allowing them to validate its
accuracy and usability. Record any new requirements or changes, getting sign-off
from stakeholders before proceeding.

Record any new requirements or changes (e.g. JIRA, etc), and get sign-off from
the stakeholders. Do not start work on the transformation logic until you get a
sign-off from the stakeholders.

### Deliver Iteratively

Break down large projects into smaller, manageable parts and work with stakeholders
to set timelines and priorities.
This approach facilitates a short feedback cycle, making it easier to adapt to
changing requirements. Track progress with clear acceptance criteria.

E.g. If you are building an ELT pipeline (REST API => dashboard), you can split
it into modeling the data, pulling data from a REST API, loading it into a raw
warehouse table, & building a dashboard for the modeled data.

Delivering in small chunks enables a short feedback cycle from the end-user making
changing requirements easy to handle. Track your work (tickets, etc) with clear
acceptance criteria.

### Handling Changing Requirements/New Features

Establish a process for handling change or feature requests, ensuring end-users
can request modifications.
Prioritize requests with stakeholder input, communicate delivery timelines, and
educate end-users on the request process to prevent scope creep and maintain
timely delivery.

Do not accept Adhoc change/feature requests!(unless it’s an emergency). Create a process to

- Allow end-users to request changes/features
- Prioritize the change/feature requests with help from stakeholders
- Decide and communicate delivery timelines to end-users

Educate the end-user on the process of requesting a new feature/change.
Following a process will prevent scope creep and allow you to deliver on time.

## Conclusion

Effectively managing ever-changing requirements is a challenging aspect of a
data engineer's role. By following the steps outlined in this article, you can
navigate these challenges, ensuring timely project delivery, making a significant
impact, enjoying your work on data projects, and fostering supportive end-users.

The next time you start a data project, follow the steps shown above to

- Deliver on time
- Make a huge impact
- Make working on the data projects a joy, and
- Build supportive end-users

[^1]: [Becoming a Better Data Engineer Tips](https://seattledataguy.substack.com/p/becoming-a-better-data-engineer-tips)
[^2]: https://www.startdataengineering.com/post/n-questions-data-pipeline-req/
