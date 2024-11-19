---
title: Audit Logging
description: Concepts for `pgaudit` audit logging in Azure Database for PostgreSQL - Flexible Server.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 11/19/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Audit logging in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Audit logging of database activities in Azure Database for PostgreSQL flexible server is available through the PostgreSQL Audit extension: [`pgaudit`](https://www.pgaudit.org/). `pgaudit` provides detailed session and/or object audit logging.

If you want Azure resource-level logs for operations like compute and storage scaling, see the [Azure Activity Log](/azure/azure-monitor/essentials/platform-logs-overview).

## Usage considerations

By default, `pgaudit` log statements and your regular log statements are emitted using Postgres's standard logging facility. In the Azure Database for PostgreSQL flexible server, you can configure all logs to be sent to the Azure Monitor Log store for later analytics in Log Analytics. If you enable Azure Monitor resource logging, your logs are automatically sent (in JSON format) to Azure Storage, Event Hubs, and/or Azure Monitor logs, depending on your choice.

To learn how to set up logging to Azure Storage, Event Hubs, or Azure Monitor logs, visit the resource logs section of the [server logs article](concepts-logging.md).

## Installing `pgaudit`

Before you can install `pgaudit` extension in Azure Database for PostgreSQL flexible server, you need to allowlist `pgaudit` extension for use.

Using the [Azure portal](https://portal.azure.com):

   1. Select your Azure Database for PostgreSQL flexible server instance.
   1. On the sidebar, select **Server Parameters**.
   1. Search for the `azure.extensions` parameter.
   1. Select `pgaudit` as the extension you wish to allowlist.

:::image type="content" source="media/concepts-audit/allow-list.png" alt-text="Screenshot of allowlist in Azure Database for PostgreSQL." lightbox="media/concepts-audit/allow-list.png":::

Using [Azure CLI](/cli/azure/):

You can allowlist extensions via CLI parameter set [command](/cli/azure/postgres/flexible-server/parameter).

```azurecli
 az postgres flexible-server parameter set --resource-group <your resource group>  --server-name <your server name> --subscription <your subscription id> --name azure.extensions --value `pgaudit`
 ```

To install `pgaudit`, you must include it in the server's shared preload libraries. A change to Postgres's `shared_preload_libraries` parameter requires a server restart to take effect. You can change parameters using the [Azure portal](how-to-configure-server-parameters-using-portal.md), [Azure CLI](how-to-configure-server-parameters-using-cli.md), or [REST API](/rest/api/postgresql/singleserver/configurations/createorupdate).

Using the [Azure portal](https://portal.azure.com):

   1. Select your Azure Database for PostgreSQL flexible server instance.

   1. On the sidebar, select **Server Parameters**.

   1. Search for the `shared_preload_libraries` parameter.

   1. Select `pgaudit`.

      :::image type="content" source="media/concepts-audit/shared-preload-libraries.png" alt-text="Screenshot showing Azure Database for PostgreSQL flexible server enabling shared_preload_libraries for `pgaudit`." lightbox="media/concepts-audit/shared-preload-libraries.png":::

   1. You can check that `pgaudit`is loaded in shared_preload_libraries by executing the following query in psql:

```sql
      show shared_preload_libraries;
 ```
You should see `pgaudit`in the query result that will return shared_preload_libraries.

   1. Connect to your server using a client (like psql) and enable the `pgaudit` extension.

```sql
      CREATE EXTENSION `pgaudit`;
 ```

> [!TIP]  
> If you see an error, confirm that you restarted your server after saving `shared_preload_libraries`.

## `pgaudit` settings

`pgaudit` allows you to configure session or object audit logging. [Session audit logging](https://github.com/`pgaudit`/`pgaudit`/blob/master/README.md#session-audit-logging) emits detailed logs of executed statements. [Object audit logging](https://github.com/`pgaudit`/`pgaudit`/blob/master/README.md#object-audit-logging) is audit scoped to specific relations. You can choose to set up one or both types of logging.

Once you have [enabled `pgaudit`](#installing-pgaudit), you can configure its parameters to start logging.  
To configure `pgaudit` you can follow below instructions.  
Using the [Azure portal](https://portal.azure.com):

   1. Select your Azure Database for the PostgreSQL server.

   1. On the sidebar, select **Server Parameters**.

   1. Search for the `pgaudit` parameters.

   1. Pick the appropriate settings parameter to edit. For example to start logging set `pgaudit.log` to `WRITE`

   1. Select **Save** button to save changes

The [`pgaudit` documentation](https://github.com/`pgaudit`/`pgaudit`/blob/master/README.md#settings) provides the definition of each parameter. Test the parameters first and confirm that you're getting the expected behavior.

Setting `pgaudit.log_client` to ON will redirect logs to a client process (like psql) instead of being written to the file. This setting should generally be left disabled. <br> <br>
`pgaudit.log_level` is only enabled when `pgaudit.log_client` is on.

In Azure Database for PostgreSQL flexible server, `pgaudit.log` can't be set using a `-` (minus) sign shortcut as described in the `pgaudit` documentation. All required statement classes (READ, WRITE, etc.) should be individually specified.

If you set the log_statement parameter to DDL or ALL and run a `CREATE ROLE/USER ... WITH PASSWORD ... ; ` or `ALTER ROLE/USER ... WITH PASSWORD ... ;`, command, then PostgreSQL creates an entry in the PostgreSQL logs, where password is logged in clear text, which might cause a potential security risk. This is the expected behavior per the PostgreSQL engine design.

You can, however, use the `pgaudit` extension and set the `pgaudit.log=DDL` parameter in the server parameters page, which doesn't record any `CREATE/ALTER ROLE` statement in Postgres Log, unlike Postgres `log_statement=DDL` setting. If you need to log these statements, you can add `pgaudit.log ='ROLE'` in addition, which redacts the password from logs while logging `CREATE/ALTER ROLE`.

## Audit log format

Each audit entry is indicated by `AUDIT:` near the beginning of the log line. The format of the rest of the entry is detailed in the [`pgaudit` documentation](https://github.com/`pgaudit`/`pgaudit`/blob/master/README.md#format).

## Getting started

To start quickly, set `pgaudit.log` to `WRITE`, and open your server logs to review the output.

## Viewing audit logs

The way you access the logs depends on which endpoint you choose. See the [logs storage account](/azure/azure-monitor/essentials/resource-logs#send-to-azure-storage) article for Azure Storage. See the [stream Azure logs](/azure/azure-monitor/essentials/resource-logs#send-to-azure-event-hubs) article for Event Hubs.

For Azure Monitor Logs, logs are sent to the workspace you selected. The Postgres logs use the **AzureDiagnostics** collection mode, so they can be queried from the AzureDiagnostics table. The fields in the table are described below. Learn more about querying and alerting in the [Azure Monitor Logs query](/azure/azure-monitor/logs/log-query-overview) overview.

You can use this query to get started. You can configure alerts based on queries.

Search for all `pgaudit` entries in Postgres logs for a particular server on the last day

```kusto
AzureDiagnostics
| where Resource =~ "myservername"
| where Category == "PostgreSQLLogs"
| where TimeGenerated > ago(1d)
| where Message contains "AUDIT:"
```

## Related content

- [Learn about logging in Azure Database for PostgreSQL flexible server](concepts-logging.md)
- [Learn how to set logging in Azure Database for PostgreSQL flexible server and how to access logs](how-to-configure-and-access-logs.md)
