---
title: Table Types - Elastic Clusters in Azure Database for PostgreSQL Flexible Server
description: Learn about the different types of tables available in an elastic cluster on Azure Database for PostgreSQL.
#customer intent: As a user, I want to understand the different table types in an elastic cluster so that I can choose the right table type for my data.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: elastic-clusters
ms.topic: concept-article
---

# Table types on elastic clusters in Azure Database for PostgreSQL flexible server

A cluster has five types of tables. Each type stores data differently on nodes and serves different purposes.

## Distributed tables

The first type, and most common, is distributed tables. They look like normal tables to SQL statements, but they're horizontally partitioned across worker nodes. This partitioning means that the rows of the tables are stored on different nodes in fragment tables called shards.

Elastic clusters run not only SQL but also DDL (Data Definition Language) statements throughout a cluster. When you change the schema of a distributed table, the change cascades to update all the table's shards across workers. You need to perform such operations through a connection over port 5432.

### Distributed column

Elastic clusters use algorithmic sharding to assign rows to shards. The assignment is made deterministically based on the value of a table column called the distribution column. The cluster administrator must designate this column when distributing a table. Making the right choice is important for performance and functionality.

## Reference tables

A reference table is a type of distributed table whose entire contents reside in a single shard. The cluster replicates the shard on every worker. Queries on any worker can access the reference information locally, without the network overhead of requesting rows from another node. Reference tables don't have a distribution column because there's no need to distinguish separate shards per row.

Reference tables are typically small and store data that's relevant to queries running on any worker node. An example is enumerated values like order statuses or product categories.

## Local tables

When you use an elastic cluster, each node is a regular PostgreSQL database. You can create ordinary tables on them and choose not to shard them.

A good candidate for local tables is small administrative tables that don't participate in join queries. An example is a `users` table for application sign-in and authentication. This type of table is only useful when you don't plan to load balance your connection among an elastic cluster using port 7432 or 8432.

## Local managed tables

Elastic clusters might automatically add local tables to metadata if a foreign key reference exists between a local table and a reference table. In addition, you can manually create locally managed tables by executing the `citus_add_local_table_to_metadata` function on regular local tables. Tables present in metadata are considered managed tables and can be queried from any node. Citus knows to route to the node to obtain data from the local managed table. Such tables are displayed as local in the `citus_tables` view.

## Schema tables

When you use [schema-based sharding](concepts-elastic-clusters-sharding-models.md#schema-based-sharding), the system automatically associates distributed schemas with individual colocation groups. When you create tables in those schemas, the system automatically converts them to colocated distributed tables without a shard key. These tables are schema tables and appear as schema in the `citus_tables` view.

## Related content

- [Overview of elastic clusters](concepts-elastic-clusters.md).
- [Sharding models on elastic clusters in Azure Database for PostgreSQL](concepts-elastic-clusters-sharding-models.md).
- [Frequently asked questions about elastic clusters of Azure Database for PostgreSQL limitations](concepts-elastic-clusters-limitations.md).
