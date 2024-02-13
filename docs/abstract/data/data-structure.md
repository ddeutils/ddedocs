---
icon: material/newspaper-variant-multiple
---

# Data Structure

## Directed Acyclic Graph (DAG)

A DAG is a specific type of graph. It can be seen as a graphical representation
of causal effects i.e. a node in a DAG is the result of an action/relation of its
predecessor node. It has the following properties.

* Has Nodes, Edges & Direction
* No cycle
* Topologically sorted/ordered
* Idempotent

!!! note

    * Node -> Entity/Process
    * Edges -> Relationship
    * Direction -> Flow

Owing to the above-mentioned properties, DAGs are useful when it comes to optimization.
We can optimize the flow by transitive reduction (removing unnecessary edges).

DAGs are used in workflow engines like `Airflow`, real-time data computation engines
like `Storm`, and data processing engines like `Spark`.

## References

* [5 Data Structures That You Probably Aren’t Familiar With](https://levelup.gitconnected.com/5-data-structures-that-you-probably-are-unfamiliar-with-but-are-extremely-useful-6d3b47f51b0c)
* [:simple-medium: Advance Data Structures for Data Engineering — Part II](https://blog.devgenius.io/advance-data-structures-for-data-engineering-part-ii-71e9901f1b3d)
