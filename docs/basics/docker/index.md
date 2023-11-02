---
icon: material/docker
---

# Docker

Docker container use only cloud native application which the code can run on container
software. The large package software such as CRM, ERP, or SAP can not run on container
yet, so it still run on VM.

Docker is not compatible manage the large resource such as 128 Core with 1 memory 1TB.

!!! note

    The Production database should not run on Docker or any container services.
    You able to go this way, but it has many problems, like maintain solution.

## Docker Concepts

Docker has concept Build, Ship, and Run. This concept make Docker be the most popular
container software in this world.

**Components for concepts**:

- Image

The basic of a Docker container.

- Container
- Engine
- Registry
