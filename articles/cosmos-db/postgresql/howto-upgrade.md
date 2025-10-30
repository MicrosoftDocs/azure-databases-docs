---
title: Upgrade cluster - Azure Cosmos DB for PostgreSQL
description: See how you can upgrade PostgreSQL and Citus in Azure Cosmos DB for PostgreSQL.
ms.author: nlarin
author: niklarin
ms.service: azure-cosmos-db
ms.subservice: postgresql
ms.topic: how-to
ms.date: 07/04/2024
appliesto:
  - ✅ PostgreSQL
---

# Upgrade cluster in Azure Cosmos DB for PostgreSQL

[!INCLUDE [Note - Recommended services](includes/note-recommended-services.md)]

These instructions describe how to upgrade to a new major version of PostgreSQL
on all cluster nodes.

## Test the upgrade first

Upgrading PostgreSQL causes more changes than you might imagine, because
Azure Cosmos DB for PostgreSQL will also upgrade the [database
extensions](reference-extensions.md), including the Citus extension. Upgrades
also require downtime in the database cluster.

We strongly recommend you to test your application with the new PostgreSQL and
Citus version before you upgrade your production environment.  Also, see
our list of [upgrade precautions](concepts-upgrade.md).

A convenient way to test is to make a copy of your cluster using
[point-in-time restore](concepts-backup.md#restore). Upgrade the
copy and test your application against it. Once you've verified everything
works properly, upgrade the original cluster.

## Upgrade a cluster in the Azure portal

1. In the **Overview** section of a cluster, select the
   **Upgrade** button.
1. A dialog appears, showing the current version of PostgreSQL and Citus.
   Choose a new PostgreSQL version in the **PostgreSQL version to upgrade** list.
1. Verify that the value in **Citus version to upgrade** is what you expect.
   This value changes based on the PostgreSQL version you selected.
1. Select the **Upgrade** button to continue.

> [!NOTE]
> If you're already running the latest PostgreSQL version, the selection and button are grayed out.

## Post-upgrade tasks

After a major PostgreSQL version upgrade, run the `ANALYZE` operation to refresh the `pg_statistic` table. `pg_statistic` is a system catalog table in PostgreSQL that stores statistical data about the content of table columns and index expressions. Entries in `pg_statistic` are created by the [ANALYZE](https://www.postgresql.org/docs/16/sql-analyze.html) command and used by the query planner.

Run the `ANALYZE` command without any parameters to generate statistics for the tables in the database on your cluster. The default database name is 'citus'. If custom database name was used at the cluster creation time, you can find it on the **Overview** page of your cluster's properties. Using the optional `VERBOSE` flag allows you to see the progress.

```sql
ANALYZE VERBOSE;
```

> [!NOTE]
> Database performance might be impacted if you don't run `ANALYZE` operation after the major PostgreSQL version upgrade on your cluster.

## Next steps

* Learn about [supported PostgreSQL versions](reference-versions.md).
* See [which extensions](reference-extensions.md) are packaged with
  each PostgreSQL version in a cluster.
* Learn more about [upgrades](concepts-upgrade.md)
