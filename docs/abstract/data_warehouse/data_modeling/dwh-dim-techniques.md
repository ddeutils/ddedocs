# Dimensional Modeling Techniques

**Table of Contents**:

- [Dimension Hierarchy Techniques](#dimension-hierarchy-techniques)

## Dimension Hierarchy Techniques

### Fixed Depth Positional Hierarchies

A fixed depth hierarchy is a series of many-to-one relationships, such as product
to brand to category to department. When a fixed depth hierarchy is defined and
the hierarchy levels have agreed upon names, the hierarchy levels should appear
as separate positional attributes in a dimension table. A fixed depth hierarchy
is by far the easiest to understand and navigate as long as the above criteria are met.
It also delivers predictable and fast query performance. When the hierarchy is
not a series of many-to-one relationships or the number of levels varies such
that the levels do not have agreed upon names, a ragged hierarchy technique must
be used.

### Slightly Ragged/Variable Depth Hierarchies

Slightly ragged hierarchies don’t have a fixed number of levels, but the range in
depth is small. Geographic hierarchies often range in depth from perhaps three
levels to six levels. Rather than using the complex machinery for unpredictably
variable hierarchies, you can force-fit slightly ragged hierarchies into a fixed
depth positional design with separate dimension attributes for the maximum number
of levels, and then populate the attribute value based on rules from the business.

## References

- https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/
