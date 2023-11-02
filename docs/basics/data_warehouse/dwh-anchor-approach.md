# Data Warehouse: Anchor Approach

The Anchor Model further normalizes the data vault model. The initial intention of Lars.
Rönnbäck was to design a highly scalable model. His core concept is that all expansion
involves adding rather than modifying. Therefore, he normalized the model to 6NF,
and it becomes a K-V structural model.

The Anchor Model consists of the following:

* Anchors: Anchors are similar to Hubs in the Data Vault Model. They stand for business entities and have only primary keys.
* Attributes: Attributes are similar to satellites in the Data Vault Model but are more normalized. They are in the K-V structure. Each table describes attributes of only one anchor.
* Ties: Ties indicate the relationship between Anchors and get described using a table. Ties are similar to links in the Data Vault Model and can improve the general model expansion capability.
* Knots: Knots stand for the attributes that may be shared by multiple anchors, for example, enumerated and public attributes such as gender and state.

We can further subdivide these four basic objects into historical and non-historical
objects, where historical objects record changes in the data using timestamps and
keeping multiple records.

This division allowed the author of the Anchor Model to achieve high scalability.
However, this model also increases the number of join query operations. The creator
believes that analysis and query in a data warehouse are performed only based on
a small section of fields. This is similar to the array storage structure, which
can significantly reduce data scanning and reduce the impact on query performance.
Some databases with the table elimination feature, for example, MariaDB, can greatly
reduce the number of join operations. However, this is still open to discussion.

## References

- [Alibaba Cloud: Comparison of Data Modeling Methods for BigData](https://www.alibabacloud.com/blog/acomparison-of-data-modeling-methods-for-bigdata_593761)
