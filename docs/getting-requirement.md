---
icon: material/comment-search-outline
---

# Getting Requirement

One of the mistakes you’ll make as a data engineer is not truly understanding the
business requirements.

!!! quote

    The business will come to you and ask for a real-time dashboard.[^1]

But they mean they want the data updated 3-4x a day, or maybe they only look at
the report once a week; at that moment, the data should be as up-to-date as
possible.

## Getting Started

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

Assist end-users in defining requirements by engaging in conversations about their
objectives and challenges. Understand their current operations to gain valuable
insights. Use the following questions to refine requirements:

- Business impact: How does having this data impact the business? What is the measurable improvement in the bottom line, business OKR, etc? Knowing the business impact helps in determining if this project is worth doing.
- Semantic understanding: What does the data represent? What business process generates this data? Knowing this will help you model the data and understand its relation to other tables in your warehouse.
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

### End-User Validation

[^1]: [Becoming a Better Data Engineer Tips](https://seattledataguy.substack.com/p/becoming-a-better-data-engineer-tips)
