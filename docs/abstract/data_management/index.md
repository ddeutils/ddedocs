---
icon: material/warehouse
---

# Data Management

!!! quote

    Data Management is an umbrella term that covers everything put in place by
    an organization to manage information and utilize it to make decisions.[^1]

:material-page-last: A Data Management refers to the _Practices_, _Architectural
Techniques_, _Strategies_, and _Tools_ that manage, store, and analyze data throughout
its lifecycle.
Effective data management ensures that data is accurate, available, and accessible
when needed while maintaining security and compliance with relevant regulations.

For the trend of a **Data Management** that we should follow the sharing knowledge
and research from the **[:material-chart-bell-curve: Gartner Hype Cycle for Data Management](https://www.gartner.com/en)**.
You should to know that a data management strategy can change and shift everytime
because it depend on a data service or technology that was implemented by your
organize.

<figure markdown="span">
  ![Gartner Hype Cycle for Data Management 2023](img/gartner-hype-cycle-graphic.png){ loading=lazy width="650" }
  <figcaption><a href="https://www.gartner.com/en/documents/4573399">Gartner Hype Cycle for Data Management 2023</a></figcaption>
</figure>

!!! note

    A ^^Modern Data Management^^ involves a set of practices, techniques, and
    technologies used to handle data as a valuable resource.
    Its aim is to ensure the availability, integrity, security, and usability
    of data within an organization.[^2]

---

## :material-arrow-down-right: Getting Started

:material-page-last: The buzz word that has taken over pretty much every industry
and large organization in the last decade is **"Data-Driven"**.
You can find millions of articles, studies or blogs out there on why you should
adopt a data-driven culture in your organization.
You can identify problems and opportunities faster than you could without data.
You can analyze past and sometimes even real-time data to make informed decisions
about the future.
Ultimately when you're making an important decision, you want as much information
and context as you can possibly get, so you can make the decision confidently.

Being able to make data-driven decisions gives you an incredibly strong competitive
advantage in the marketplace, because very few organizations are.
Building a data-driven business is difficult but if you pull it off, it’s way easier
to become a leader in your market because you can leverage information your competitors
just don’t have.

And on the flip side of that, if you lack any type of data management in your
company - good luck staying competitive, it’s probably not going to happen.

!!! note

    In this New Vantage Partners report from 2022 on The State of Corporate Data
    Initiatives, it states that ==only 26.5% of organizations have achieved their
    data-driven goals==.

:material-page-last: So if you're looking to get ahead and stay ahead, becoming
data-driven should 100% be part of your plan.
But building an effective data-driven culture only works when it’s built on strong
data management foundations.

**3 Pillars of a Strong Data Management Strategy**:

1. [Data Governance](#data-governance)
2. [Data Architecture](#data-architecture)
3. [Data Quality](#data-quality-and-consistency)

---

## Strategies

### Data Governance

Data Governance refers to all the organizational rules that are put in place
around data, including roles and responsibilities of team members, access control,
policies, procedures and standards.

Everything that will enforce a high quality of data securely flowing through the
organization. Governance is typically documented but looks different for every
company depending on company size, what your systems are, and what types of data
you're dealing with.

Includes policies, procedures, and standards that ensure the appropriate use,
management, and protection of data throughout its lifecycle. It also involves
establishing roles and responsibilities for data management, as well as ensuring
compliance with legal and regulatory requirements.

- Policies and Standards: Establishing clear policies for data usage, privacy, and security.
- Data Stewardship: Assigning responsibilities to ensure data quality and compliance.

Read More about [Data Governance](../data_governance/index.md)

### Data Quality and Consistency

Having accurate and up-to-date data is an essential part of being data-driven.
All systems need to be monitored and data needs to be cleaned very carefully.
The data you receive in reports needs to reflect what reality is, which is the
whole point of being data driven, so the quality of the data is super important.

Ensuring that data is accurate, complete, and consistent. It includes
defining data quality metrics, establishing data quality rules, and implementing
data profiling and cleansing tools and techniques.

- Data Cleansing: Regularly cleaning data to remove inaccuracies and inconsistencies.
- Data Validation: Implementing processes to ensure data accuracy and reliability.

### Data Integration & Transformation

Consolidating data from multiple sources into a single, unified view
of the data. It includes selecting appropriate data integration tools, defining
data mapping and transformation rules, and establishing data synchronization and
replication protocols.

- ETL/ELT Processes
- Batch and Stream Processing
- Real-Time Data Integration
- Data Transformation Techniques

Read More about [Data Integration](./data-integration.md) & [Data Transformation](./data-transformation.md)

### Data Lifecycle Management

- **Archiving and Retention**: Implementing policies for data archiving and retention
  based on data usage and legal requirements.
- **Disposal**: Securely disposing of data that is no longer needed.

### Data Security and Privacy

This involves ensuring the confidentiality, integrity, and availability of data.
It includes establishing data security policies and procedures, implementing access
controls and encryption, and complying with legal and regulatory requirements.

- Advanced Encryption: Using cutting-edge encryption techniques to protect data.
- Regulatory Compliance: Ensuring adherence to global data protection regulations
  like GDPR, CCPA, and others.
- Zero Trust Architecture: Implementing security models that verify every access
  request as if it originated from an open network.

- Data Encryption and Masking
- Access Control and Authentication
- Compliance and Regulatory Requirements
- Privacy-Preserving Data Processing

### Data Architecture

The next important pillar is Data Architecture. This is the actual design of
the systems involved in how data flows through your company and gets where it
needs to be, when it needs to be there. Broadly speaking this includes your
infrastructure which could be in the cloud or big server rooms at your company
and all the applications running on those servers which are responsible for making
the data flow from place to place.
It’s the hardware and software.

Read More about [Data Architecture](../data_architecture/index.md)

### Data Democratization

- Self-service Analytics: Providing tools and platforms that enable non-technical
  users to access and analyze data.
- Data Literacy Programs: Promoting data literacy across the organization to empower
  employees to make data-driven decisions.

### Data Storage

Data Storage on this part we will focus on below list:

- [Data Warehouse](./data-warehouse.md)
- [Data Mart](./data-mart.md)
- [Operation Data Store](./data-ods.md)
- Data Lake

|                    | EDW                                                     | ODS                                                  | DM                                                              |
|--------------------|---------------------------------------------------------|------------------------------------------------------|-----------------------------------------------------------------|
| Purpose            | Serves the entire organization                          | Supports operational reporting                       | Serves a specific business unit/department                      |
| Data Integration   | Integrates data from multiple sources                   | Integrates real-time data from transactional systems | Integrates data from a specific subject area                    |
| Data Model         | Top-down approach to design                             | Bottom-up approach to design                         | Designed based on specific business requirements                |
| Complexity         | More complex and time-consuming to design and implement | Less complex and quicker to implement                | Less complex and quicker to implement                           |
| Query and Analysis | Supports complex queries and analytics                  | Supports operational reporting and simple analysis   | Optimized for querying and reporting on a specific subject area |
| Data Volume        | Large volume of historical data                         | Real-time or near-real-time data                     | Smaller volume of data                                          |
| Users              | Business analysts, executives, data scientists          | Operational staff, business analysts                 | Business analysts, departmental staff                           |
| Cost               | Higher cost due to complexity and scale                 | Lower cost due to simpler design and implementation  | Lower cost due to simpler design and implementation             |

| Criteria          | EDW                                                     | ODS                                                      | DM                                                     |
|-------------------|---------------------------------------------------------|----------------------------------------------------------|--------------------------------------------------------|
| Scope             | Enterprise-wide                                         | Operational                                              | Departmental or functional                             |
| Data sources      | Multiple internal and external sources                  | Multiple operational sources                             | EDW, ODS, or other sources                             |
| Data integration  | High degree of integration and standardization          | Moderate degree of integration and standardization       | Low degree of integration and standardization          |
| Data granularity  | Mixed levels of granularity                             | Low level of granularity (detailed)                      | High level of granularity (aggregated or summarized)   |
| Data currency     | Historical and current data                             | Near real-time or real-time data                         | Historical and current data                            |
| Data quality      | High quality (cleansed and validated)                   | Moderate quality (some cleansing and validation)         | High quality (cleansed and validated)                  |
| Data structure    | Relational or dimensional models                        | Relational models                                        | Dimensional models                                     |
| Data volume       | Very large (terabytes or petabytes)                     | Large (gigabytes or terabytes)                           | Small or medium (megabytes or gigabytes)               |
| Query performance | Moderate to high (depends on indexing and partitioning) | Low to moderate (depends on updates and concurrency)     | High (optimized for analysis)                          |
| Query complexity  | High (supports complex and ad-hoc queries)              | Low to moderate (supports simple and predefined queries) | Moderate to high (supports complex and ad-hoc queries) |
| Query frequency   | Low to moderate (periodic or on-demand)                 | High (continuous or near-continuous)                     | Moderate to high (periodic or on-demand)               |
| User types        | Analysts, managers, executives, data scientists, etc.   | Operational staff, managers, etc.                        | Analysts, managers, etc.                               |

---

## :material-source-commit-end: Conclusion

Overall, a Data Management strategy is a comprehensive approach to managing data
that includes a range of components designed to ensure the effective use, management,
and protection of data throughout its lifecycle.

[^1]: [CNDI: What is Data Management](https://www.cndi.dev/post/what-is-data-management/)
[^2]: [Modern Data Management: 8 Things You Can Gain From It](https://atlan.com/modern-data-management/)
