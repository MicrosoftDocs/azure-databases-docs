---
title: Migrate Production Data
description: This article introduces the two main paths for migrating production data from a PostgreSQL database to a Citus cluster on Microsoft Azure.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
monikerRange: "citus-13 || citus-14"
---

# Migrate production data

At this time, after updating the database schema and application queries to work with Citus, you're ready for the final step. It's time to migrate data to the Citus cluster and cut over the application to its new database.

The data migration path is dependent on downtime requirements and data size, but generally falls into one of the following two categories.

## In this section

| Article | Description |
| --- | --- |
| [Small data migrations](migration-data-small.md) | For datasets that allow brief downtime during migration. |
| [Big data migrations](migration-data-big.md) | For large datasets requiring minimal or zero downtime. |

## Related content

- [Migrating an Existing App](migration.md)
- [Query migration](migration-query.md)
- [Schema migration](migration-schema.md)
