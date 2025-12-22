---
title: Audit Logging
description: Concepts for `pgaudit` audit logging in Azure Database for PostgreSQL.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 08/08/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: concept-article
ms.custom:
  - horz-security
---

# Audit logging in Azure Database for PostgreSQL

Audit logging of database activities in Azure Database for PostgreSQL is available through the [`pgaudit`](https://www.pgaudit.org/) extension. `pgaudit` provides detailed session and/or object audit logging.

If you want Azure resource-level logs for operations like compute and storage scaling, see the [Azure Activity Log](/azure/azure-monitor/essentials/platform-logs-overview).

## Usage considerations

By default, `pgaudit` logs statements and your regular log statements are emitted using Postgres's standard logging facility. In the Azure Database for PostgreSQL, you can configure all logs to be sent to the Azure Monitor Log store for later analysis in Log Analytics. If you enable Azure Monitor resource logging, your logs are automatically sent (in JSON format) to Azure Storage, Event Hubs, and/or Azure Monitor logs, depending on your choice.

To learn how to set up logging to Azure Storage, Event Hubs, or Azure Monitor logs, visit the resource logs section of the [server logs article](../monitor/concepts-logging.md).

## Installing the extension

To be able to use `pgaudit` extension, you need to [allowlist](../extensions/how-to-allow-extensions.md#allow-extensions), [load](../extensions/how-to-load-libraries.md), and [create](../extensions/how-to-create-extensions.md) the extension in the database on which you plan to use it.

## Configure extension settings

`pgaudit` allows you to configure session or object audit logging. [Session audit logging](https://github.com/pgaudit/pgaudit/blob/master/README.md#session-audit-logging) emits detailed logs of executed statements. [Object audit logging](https://github.com/pgaudit/pgaudit/blob/master/README.md#object-audit-logging) is audit scoped to specific relations. You can choose to set up one or both types of logging.

Once you [enable `pgaudit`](#installing-the-extension), you can configure its parameters to start logging.

To configure `pgaudit`, you can follow these instructions:

### [Portal](#tab/portal)

Using the [Azure portal](https://portal.azure.com):

1. Select your instance of Azure Database for the PostgreSQL.

1. From the resource menu, under **Settings**, select **Server parameters**.

1. Search for the `pgaudit` parameters.

1. Pick the appropriate parameter to edit. For example to start logging `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`, and `COPY` statements, set `pgaudit.log` to `WRITE`.

1. Select **Save** button to save changes.

### [CLI](#tab/cli)

You can set the value of any of the `pgaudit` server parameters via the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command.

```azurecli-interactive
az postgres flexible-server parameter set --resource-group <resource_group> --server-name <server> --source user-override --name <parameter> --value <value>
```

---

The official [documentation](https://github.com/pgaudit/pgaudit/blob/master/README.md#settings) of `pgaudit` provides the definition of each parameter. Test the parameters first and confirm that you're getting the expected behavior.

For example, setting `pgaudit.log_client` to `ON` not only writes audit events to the server log, but also sends them to client processes (like psql). This setting should generally be left disabled.<br /><br />
`pgaudit.log_level` is only enabled when `pgaudit.log_client` is on.

In Azure Database for PostgreSQL, `pgaudit.log` can't be set using a `-` (minus) sign shortcut as described in the `pgaudit` documentation. All required statement classes (`READ`, WRITE, etc.) should be individually specified.

If you set the `log_statement` parameter to `DDL` or `ALL` and run a `CREATE ROLE/USER ... WITH PASSWORD ... ;` or `ALTER ROLE/USER ... WITH PASSWORD ... ;`, command, then PostgreSQL creates an entry in the PostgreSQL logs where password is logged in clear text, which might cause a potential security risk. It's the expected behavior per the PostgreSQL engine design.

You can, however, use the `pgaudit` extension and set `pgaudit.log` to `DDL`, which doesn't record any `CREATE/ALTER ROLE` statement in Postgres server log, unlike it does when you set `log_statement` to `DDL`. If you need to log these statements, you can also set `pgaudit.log`to `ROLE`, which redacts the password from logs while logging `CREATE/ALTER ROLE`.

## Audit log format

Each audit entry begins with `AUDIT:`. The format of the rest of the entry is detailed in the [documentation](https://github.com/pgaudit/pgaudit/blob/master/README.md#format) of `pgaudit`.

## Getting started

To start quickly, set `pgaudit.log` to `ALL`, and open your server logs to review the output.

## Viewing audit logs

The way you access the logs depends on which endpoint you choose. See the [logs storage account](/azure/azure-monitor/essentials/resource-logs#send-to-azure-storage) article for Azure Storage. See the [stream Azure logs](/azure/azure-monitor/essentials/resource-logs#send-to-azure-event-hubs) article for Event Hubs.

For Azure Monitor Logs, logs are sent to the workspace you selected. The Postgres logs use the **AzureDiagnostics** collection mode, so they can be queried from the AzureDiagnostics table. Learn more about querying and alerting in the [Azure Monitor Logs query](/azure/azure-monitor/logs/log-query-overview) overview.

You can use this query to get started. You can configure alerts based on queries.

Search for all `pgaudit` entries in Postgres logs for a particular server on the last day

```kusto
AzureDiagnostics
| where Resource =~ "<flexible-server-name>"
| where Category == "PostgreSQLLogs"
| where TimeGenerated > ago(1d)
| where Message contains "AUDIT:"
```

## Major Version Upgrade with pgaudit extension installed

During a major version upgrade, the pgaudit extension is automatically dropped and then recreated after the upgrade completes. While the extension is restored, any custom configurations set in `pgaudit.log` or other related parameters aren't automatically preserved.

## Related content

- [Logging in Azure Database for PostgreSQL](../monitor/concepts-logging.md)
- [Configure logging and access logs in Azure Database for PostgreSQL](../monitor/how-to-configure-and-access-logs.md)
