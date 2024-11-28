---
title: Table types - Elastic Clusters
description: Learn about the different types of tables available in an Elastic Cluster on Azure Database for PostgreSQL.
author: mulander
ms.author: adamwolk
ms.reviewer: maghan
ms.date: 11/19/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Table types in Elastic Clusters on Azure Database for PostgreSQL

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

There are five types of tables in a cluster, each stored differently on nodes and used for different purposes.

## Distributed tables

The first type, and most common, is distributed tables. They
appear to be normal tables to SQL statements, but they're horizontally
partitioned across worker nodes. What this means is that the rows
of the table are stored on different nodes, in fragment tables called
shards.

Elastic Clusters run not only SQL but DDL (Data Definition Language) statements throughout a cluster.
Changing the schema of a distributed table cascades to update
all the table's shards across workers. Such operations need to be done through a connection over port 5432.

### Distributed column

Elastic Clusters use algorithmic sharding to assign rows to shards. The assignment is made deterministically based on the value
of a table column called the distribution column. The cluster
administrator must designate this column when distributing a table.
Making the right choice is important for performance and functionality.

## Reference tables

A reference table is a type of distributed table whose entire
contents are concentrated into a single shard. The shard is replicated on every worker. Queries on any worker can access the reference information locally, without the network overhead of requesting rows from another node. Reference tables have no distribution column
because there's no need to distinguish separate shards per row.

Reference tables are typically small and are used to store data that's
relevant to queries running on any worker node. An example is enumerated
values like order statuses or product categories.

## Local tables

When you use Elastic Cluster, each node is a regular PostgreSQL database. You can create ordinary tables on them and choose not to shard them.

A good candidate for local tables would be small administrative tables that don't participate in join queries. An example is a `users` table for application sign-in and authentication. This type of table is only useful when you don't plan to load balance your connection among an Elastic Cluster using port 7432.

## Local managed tables

Elastic Clusters might automatically add local tables to metadata if a foreign key reference exists between a local table and a reference table. In addition, locally managed tables can be manually created by executing citus_add_local_table_to_metadata function on regular local tables. Tables present in metadata are considered managed tables and can be queried from any node. Citus knows to route to the node to obtain data from the local managed table. Such tables are displayed as local in `citus_tables` view.

## Schema tables

With [schema-based sharding](./concepts-elastic-clusters-sharding-models.md#schema-based-sharding), distributed schemas are automatically associated with individual colocation groups. Tables created in those schemas are automatically converted to colocated distributed tables without a shard key. Such tables are considered schema tables and are displayed as schema in `citus_tables` view.

## Related content

- [Sharding models - Elastic Clusters](./concepts-elastic-clusters-sharding-models.md)
- [Sharding tradeoffs - Elastic Clusters](./concepts-elastic-clusters-sharding-models.md#sharding-tradeoffs)
- [Limitations of Elastic Clusters with Azure Database for PostgreSQL](./concepts-elastic-clusters-limitations.yml)
