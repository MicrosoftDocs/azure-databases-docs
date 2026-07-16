---
title: Logs in Azure Database for PostgreSQL Flexible Server
description: Describes logging configuration, storage, and analysis in Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to configure standard logging on my Azure Database for PostgreSQL flexible server, so that I can capture errors, connections, and checkpoints.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: how-to
---

# Logs in Azure Database for PostgreSQL flexible server

Azure Database for PostgreSQL enables you to configure and access Postgres' standard logs. Use the logs to identify, troubleshoot, and fix configuration errors and suboptimal performance. You can configure and access logging information for errors, query information, autovacuum records, connections, and checkpoints. (Access to transaction logs isn't available).

Audit logging is available through a Postgres extension, `pgaudit`. To learn more, see the [auditing concepts](../security/security-audit.md) article.

## Configure logging

Configure Postgres standard logging on your server by using the logging parameters. To learn more about Postgres log parameters, see the [When To Log](https://www.postgresql.org/docs/current/runtime-config-logging.html#RUNTIME-CONFIG-LOGGING-WHEN) and [What To Log](https://www.postgresql.org/docs/current/runtime-config-logging.html#RUNTIME-CONFIG-LOGGING-WHAT) sections of the Postgres documentation. You can configure most, but not all, Postgres logging parameters in Azure Database for PostgreSQL.

To learn how to configure parameters in Azure Database for PostgreSQL, see the [portal documentation](../parameters/how-to-parameters-list-all.md) or the [CLI documentation](../parameters/how-to-parameters-list-all.md).

> [!NOTE]
> Configuring a high volume of logs can add significant performance overhead. For example, statement logging can affect performance.

## Access logs

Azure Database for PostgreSQL flexible server is integrated with Azure Monitor diagnostic settings. Diagnostic settings allow you to send PostgreSQL logs in JSON format to Azure Monitor Logs for analytics and alerting. You can also stream them to Event Hubs or archive them in Azure Storage.

### Access control for logs

Control access to server logs through Azure Role-Based Access Control (RBAC). Any role that provides read access to the server also grants permission to download logs. This access includes built-in roles such as:

- Reader
- Monitoring Reader
- Log Analytics Reader
- Or equivalent custom roles

> [!WARNING]
> Depending on your logging configuration, logs might contain sensitive information, such as credentials.

## Data retention policy and pricing

For logs sent to Event Hubs or a Storage account, set up a retention policy to automatically delete data after a certain period. Log Analytics costs depend on two factors:

- **Data ingestion:** Charges are based on the volume of data that is ingested into the workspace.
- **Data retention:** Logs stored in your Log Analytics workspace are kept free of charge for the first 31 days. Beyond this free retention period, there's a fee for storing data, calculated on a daily pro-rata basis, based on the amount of data (in GB) retained each month.

For a breakdown of the costs associated with data ingestion and retention, visit the [Azure Monitor pricing page](https://azure.microsoft.com/pricing/details/monitor/).

### Log format

The following table describes the fields for the **PostgreSQLLogs** type. Depending on the output endpoint you choose, the fields included and the order in which they appear might vary. 

| **Field** | **Description** |
| --- | --- |
| TenantId | Your tenant ID |
| SourceSystem | `Azure` |
| TimeGenerated [UTC] | Time stamp when the log was recorded in UTC |
| Type | Type of the log. Always `AzureDiagnostics` |
| SubscriptionId | GUID for the subscription that the server belongs to |
| ResourceGroup | Name of the resource group the server belongs to |
| ResourceProvider | Name of the resource provider. Always `MICROSOFT.DBFORPOSTGRESQL` |
| ResourceType | `FlexibleServers` |
| ResourceId | Resource URI |
| Resource | Name of the server |
| Category | `PostgreSQLLogs` |
| OperationName | `LogEvent` |
| errorLevel_s | Logging level, example: LOG, ERROR, NOTICE |
| processId_d | Process ID of the PostgreSQL backend |
| sqlerrcode_s | PostgreSQL Error code that follows the SQL standard's conventions for SQLSTATE codes |
| Message | Primary log message | 
| Detail | Secondary log message (if applicable) |
| ColumnName | Name of the column (if applicable) |
| SchemaName | Name of the schema (if applicable) |
| DatatypeName | Name of the datatype (if applicable) |
| _ResourceId | Resource URI |

## Known limitations

- **Log Event Size**: Azure Monitor Logs doesn't capture query plans or log messages larger than 65 KB. This limit applies to all of Azure Monitor. As a result, complex queries (for example, those involving nested views) might generate incomplete or missing query plan output in server logs. 
- **Other Constraints**: Other platform-wide limits apply to Azure Monitor Logs, such as alert rule quotas and query result size. For the complete list, see the [Azure Monitor service limits](/azure/azure-monitor/fundamentals/service-limits) documentation.


## Related content

- [Configure and access logs in Azure Database for PostgreSQL](how-to-configure-and-access-logs.md).
- [Azure Monitor pricing](https://azure.microsoft.com/pricing/details/monitor/).
- [Audit logging in Azure Database for PostgreSQL](../security/security-audit.md).
