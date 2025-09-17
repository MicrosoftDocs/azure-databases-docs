---
title: Logs
description: Describes logging configuration, storage and analysis in Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 9/16/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Logs in Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL flexible server allows you to configure and access Postgres' standard logs. The logs can be used to identify, troubleshoot, and repair configuration errors and suboptimal performance. Logging information you can configure and access includes errors, query information, autovacuum records, connections, and checkpoints. (Access to transaction logs is not available).

Audit logging is made available through a Postgres extension, `pgaudit`. To learn more, visit the [auditing concepts](security-audit.md) article.

## Configure logging

You can configure Postgres standard logging on your server using the logging server parameters. To learn more about Postgres log parameters, visit the [When To Log](https://www.postgresql.org/docs/current/runtime-config-logging.html#RUNTIME-CONFIG-LOGGING-WHEN) and [What To Log](https://www.postgresql.org/docs/current/runtime-config-logging.html#RUNTIME-CONFIG-LOGGING-WHAT) sections of the Postgres documentation. Most, but not all, Postgres logging parameters are available to configure in Azure Database for PostgreSQL flexible server.

To learn how to configure parameters in Azure Database for PostgreSQL flexible server, see the [portal documentation](how-to-configure-server-parameters.md) or the [CLI documentation](how-to-configure-server-parameters.md).

> [!NOTE]
> Configuring a high volume of logs, for example statement logging, can add significant performance overhead. 

## Accessing logs

Azure Database for PostgreSQL flexible server is integrated with Azure Monitor diagnostic settings. Diagnostic settings allow you to send PostgreSQL flexible server logs in JSON format to Azure Monitor Logs for analytics and alerting. You can also stream them to Event Hubs or archive them in Azure Storage.

### Access control for logs

Access to server logs is controlled through Azure Role-Based Access Control (RBAC). Any role that provides read access to the server will also allow downloading logs. This includes built-in roles such as:

- Reader
- Monitoring Reader
- Log Analytics Reader
- Or equivalent custom roles

> [!WARNING]
> Logs may contain sensitive information, such as credentials, depending on your logging configuration.

## Data Retention Policy and Pricing

For logs sent to Event Hubs or a Storage account, you can set up a retention policy to automatically delete data after a certain period. Log Analytics costs depend on two factors:

- **Data Ingestion:** Charges are based on the volume of data that is ingested into the workspace.
- **Data Retention:** Logs stored in your Log Analytics workspace are kept free of charge for the first 31 days. Beyond this free retention period, there is a fee for storing data, calculated on a daily pro-rata basis, based on the amount of data (in GB) retained each month.

For a breakdown of the costs associated with data ingestion and retention, please visit the [Azure Monitor pricing page](https://azure.microsoft.com/pricing/details/monitor/).

### Log format

The following table describes the fields for the **PostgreSQLLogs** type. Depending on the output endpoint you choose, the fields included and the order in which they appear may vary. 

|**Field** | **Description** |
|---|---|
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

- **Log Event Size**: Query plans or log messages larger than 65 KB will not be captured in Azure Monitor Logs. This is a platform-wide Azure Monitor limit. As a result, very complex queries (for example, those involving nested views) may generate incomplete or missing query plan output in server logs. 
- **Other Constraints**: Other platform-wide limits apply to Azure Monitor Logs, such as alert rule quotas and query result size. For the complete list, refer to the [Azure Monitor service limits](/azure/azure-monitor/fundamentals/service-limits) documentation for details.


## Related content

- [Configure and access logs in Azure Database for PostgreSQL flexible server](how-to-configure-and-access-logs.md).
- [Azure Monitor pricing](https://azure.microsoft.com/pricing/details/monitor/).
- [Audit logging in Azure Database for PostgreSQL flexible server](concepts-audit.md).
