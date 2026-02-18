---
title: Determining Application Type
description: Learn how to determine which Citus application type most resembles your application, so you can run the most efficient queries on your Citus cluster.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
monikerRange: "citus-13 || citus-14"
---

# Determining application type

Running efficient queries on a Citus cluster requires that data be properly distributed across machines. The distribution varies by the type of application and its query patterns.

There are broadly two kinds of applications that work well on Citus. The first step in data modeling is to identify which of them more closely resembles your application.

## At a glance

| Multitenant Applications | Real-Time Applications |
| --- | --- |
| Sometimes dozens or hundreds of tables in schema | Small number of tables |
| Queries relating to one tenant (company/store) at a time | Relatively simple analytics queries with aggregations |
| Online transactional processing (OLTP) workloads for serving web clients | High ingest volume of mostly immutable data |
| Online analytical processing (OLAP) workloads that serve per-tenant analytical queries | Often centering around a large table of events |

## Examples and characteristics

**Multi-Tenant Application**

These applications are typically SaaS applications that serve other companies, accounts, or organizations. Most SaaS applications are inherently relational. They have a natural dimension on which to distribute data across nodes: just shard by tenant_id.

Citus enables you to scale out your database to millions of tenants without having to rearchitect your application. You can keep the relational semantics you need, like joins, foreign key constraints, transactions, ACID, and consistency.

- **Examples**: Websites which host store-fronts for other businesses, such as a digital marketing solution, or a sales automation tool.
- **Characteristics**: Queries relating to a single tenant rather than joining information across tenants. Including OLTP workloads for serving web clients, and OLAP workloads that serve per-tenant analytical queries. Having dozens or hundreds of tables in your database schema is also an indicator for the multitenant data model.

Scaling a multitenant app with Citus also requires minimal changes to application code. We have support for popular frameworks like Ruby on Rails and Django.

**Real-Time Analytics**

Applications needing massive parallelism, coordinating hundreds of cores for fast results to numerical, statistical, or counting queries. By sharding and parallelizing SQL queries across multiple nodes, Citus makes it possible to perform real-time queries across billions of records in under a second.

If your situation resembles either of these cases, then the next step is to decide how to shard your data in the Citus cluster. As explained in the `citus_concepts` section, Citus assigns table rows to shards according to the hashed value of the table's distribution column. The database administrator's choice of distribution columns needs to match the access patterns of typical queries to ensure performance.

## Related content

- [Migration overview](migrate/migrating.md)
- [Data modeling](data-modeling.md)
- [What is Azure Cosmos DB for PostgreSQL?](what-is-citus.md)
