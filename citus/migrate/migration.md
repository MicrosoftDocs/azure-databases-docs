---
title: Migrating an Existing App
description: This article describes the steps needed to migrate an existing application a Citus cluster on Microsoft Azure.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
monikerRange: "citus-13 || citus-14"
---

# Migrate an existing application to Citus

Migrating an existing application to Citus sometimes requires adjusting the schema and queries for optimal performance. Citus extends PostgreSQL with distributed functionality, but row-based sharding isn't a drop-in replacement that scales out all workloads. A performant Citus cluster involves thinking about the data model, tooling, and the choice of SQL features to use.

There's another mode of operation in Citus called schema-based sharding. While row-based sharding results in the best performance and hardware efficiency, consider schema-based sharding if you need a more drop-in approach.

## Step 1: Optimize the schema

The first steps are to optimize the existing database schema so that it can work efficiently across multiple computers.

[Schema migration](migration-schema.md)

## Step 2: Update application queries

Next, update your application code and queries to deal with the schema changes.

[Query migration](migration-query.md)

## Step 3: Migrate production data

After you test the changes in a development environment, the last step is to migrate production data to a Citus cluster and switch over the production app. We have techniques to minimize downtime for this step.

[Data migration](migration-data.md)

## Related content

- [What is Citus?](../what-is-citus.md)
- [PostgreSQL at any scale with Citus](../postgresql-citus-scale.md)
