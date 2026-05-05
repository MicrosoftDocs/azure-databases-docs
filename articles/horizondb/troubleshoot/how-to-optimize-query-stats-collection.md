---
title: Optimize Query Stats Collection in Azure HorizonDB
description: This article describes how you can optimize query stats collection in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.subservice: performance
ms.topic: how-to
---

# Optimize query statistics collection in Azure HorizonDB

This article describes how to optimize query statistics collection on an Azure HorizonDB using pg_stat_statements extension

## Use pg_stat_statements

**Pg_stat_statements** is a PostgreSQL extension that can be enabled in Azure HorizonDB. The extension provides a means to track execution statistics for all SQL statements executed by a server. This module hooks into every query execution and comes with a non-trivial performance cost. Enabling **pg_stat_statements** forces query text writes to files on disk.

> [!NOTE]  
> `pg_stat_statements.track` is by default to NONE (i.e. disabled).

If you want to start tracking the execution statistics of all SQL statements executed by a server, then enable **pg_stat_statements**. To do so, set the value to `TOP` or `ALL`, depending on whether you want to track top-level queries or also nested queries (those executed inside a function or procedure).

To set **pg_stat_statements.track** = `TOP`

- In the Azure portal, go to the [Parameters in Azure HorizonDB](../server-parameters/concepts-server-parameters.md).
- Use the [Quickstart: Connect and query with Azure CLI in Azure HorizonDB](../connectivity/connect-azure-cli.md) az postgres server configuration set to `--name pg_stat_statements.track --resource-group myresourcegroup --server mydemoserver --value TOP`.

## Use the Query Store

Using the [Query store in Azure HorizonDB](../monitor/concepts-query-store.md) feature in Azure HorizonDB offers a different way to monitor query execution statistics. To prevent performance overhead, it's recommended to utilize only one mechanism, either the pg_stat_statements extension or the Query Store.

## Related content

- [Usage scenarios for query store in Azure HorizonDB](../monitor/concepts-query-store-scenarios.md)
- [Best practices for query store in Azure HorizonDB](../monitor/concepts-query-store-best-practices.md)
