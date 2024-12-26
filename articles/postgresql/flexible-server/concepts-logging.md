---
title: Logs
description: Describes logging configuration, storage and analysis in Azure Database for PostgreSQL - Flexible Server.
author: varun-dhawan
ms.author: varundhawan
ms.date: 7/11/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Logs in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL flexible server allows you to configure and access Postgres' standard logs. The logs can be used to identify, troubleshoot, and repair configuration errors and suboptimal performance. Logging information you can configure and access includes errors, query information, autovacuum records, connections, and checkpoints. (Access to transaction logs is not available).

Audit logging is made available through a Postgres extension, `pgaudit`. To learn more, visit the [auditing concepts](concepts-audit.md) article.

## Configure logging

You can configure Postgres standard logging on your server using the logging server parameters. To learn more about Postgres log parameters, visit the [When To Log](https://www.postgresql.org/docs/current/runtime-config-logging.html#RUNTIME-CONFIG-LOGGING-WHEN) and [What To Log](https://www.postgresql.org/docs/current/runtime-config-logging.html#RUNTIME-CONFIG-LOGGING-WHAT) sections of the Postgres documentation. Most, but not all, Postgres logging parameters are available to configure in Azure Database for PostgreSQL flexible server.

To learn how to configure parameters in Azure Database for PostgreSQL flexible server, see the [portal documentation](howto-configure-server-parameters-using-portal.md) or the [CLI documentation](howto-configure-server-parameters-using-cli.md).

> [!NOTE]
> Configuring a high volume of logs, for example statement logging, can add significant performance overhead. 

## Accessing logs

Azure Database for PostgreSQL flexible server is integrated with Azure Monitor diagnostic settings. Diagnostic settings allows you to send your Azure Database for PostgreSQL flexible server logs in JSON format to Azure Monitor Logs for analytics and alerting, Event Hubs for streaming, and Azure Storage for archiving. 

## Data retention policy and pricing

If you select Event Hubs or a Storage account, you can specify a retention policy. This policy deletes data that is older than a selected time period. If you specify Log Analytics, the retention policy depends on the selected pricing tier. Logs ingested into your **Log Analytics** workspace can be retained at no charge for up to first 31 days. Logs retained beyond these no-charge periods will be charged for each GB of data retained for a month (pro-rated daily). For more details, refer [Azure Monitor pricing](https://azure.microsoft.com/pricing/details/monitor/).

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

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Configure and access logs in Azure Database for PostgreSQL - Flexible Server](how-to-configure-and-access-logs.md).
- [Azure Monitor pricing](https://azure.microsoft.com/pricing/details/monitor/).
- [Audit logging in Azure Database for PostgreSQL - Flexible Server](concepts-audit.md).
