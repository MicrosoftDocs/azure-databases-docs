---
title: Audit Logging in Azure Database for PostgreSQL for Microsoft Entra ID principals
description: Learn how to attribute actions to specific Microsoft Entra ID users in PostgreSQL audit logs.
author: ak800i
ms.author: ajanko
ms.reviewer: ajanko
ms.date: 12/12/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
ms.custom:
  - horz-security
---

# Audit logging in Azure Database for PostgreSQL for Microsoft Entra ID principals

Database audits are one of the important components that need to be set up based on your organization’s compliance requirements, where you can monitor the targeted activities to achieve your security baseline. In Azure database for PostgreSQL flexible server, you can achieve that by using pgaudit PG extension as described in [Audit logging in Azure Database for PostgreSQL - Flexible server](./security-audit.md).

One of the challenges is utilizing auditing feature alongside Microsoft Entra ID authentication when you're using Microsoft Entra ID groups and want to audit the actions of individual groups members. This is because when group members sign in, they use their personal access tokens but use the group name as the username.

Kusto Query Language (KQL) is a powerful pipeline-driven, read-only query language that enables querying Azure Service Logs. KQL supports querying Azure logs to quickly analyze a high volume of data. For this article, we'll use the KQL to query Azure Postgres Logs and extract Microsoft Entra ID user information from audit logs.

## Prerequisites

1. Enable Audit logging - [Audit logging in Azure Database for PostgreSQL - Flexible server](./security-audit.md)
1. Enable Azure Postgres logs to be sent to Azure log analytics - [Configure Log Analytics](./how-to-configure-and-access-logs.md#configure-diagnostic-settings)
1. Adjust the `log_line_prefix` server parameter:  
  From the Server Parameters blade set the `log_line_prefix` to include the escapes `user=%u,db=%d,session=%c,sess_time=%s`  in the same sequence, in order to get the desired results.  
    * Before:  `log_line_prefix` = `%t-%c-`  
    * After: `log_line_prefix` = `%t-%c-user=%u,db=%d,session=%c,sess_time=%s`

## Kusto query

The following Kusto query queries the `AzureDiagnostics` two times.  
The first subquery finds all lines, which contain the string `Microsoft Entra ID connection authorized` and extracts the `PrincipalName` from these log lines, alongside the `SessionId`.  
The second subquery finds all audit logs.  
Finally, these two sub-queries are joined on the `SessionId`.

```kusto
let lookbackTime = ago(3d);
let opindex = 3;
let startIndex = toscalar(range thirdIndex from opindex to opindex step 1
    | project thirdIndex);
AzureDiagnostics
| where ResourceProvider == 'MICROSOFT.DBFORPOSTGRESQL'
| where TimeGenerated >= lookbackTime
| where Message contains 'Microsoft Entra ID connection authorized'
| extend SessionId = tostring(split(tostring(split(Message, 'session=')[-1]), ',sess_time')[-2])
| extend UPN = iff(Message contains 'UPN',tostring(split(tostring(split(Message, 'UPN=')[-1]), 'oid=')[-2]), '')
| extend appId = iff(Message contains 'appid', tostring(split(tostring(split(Message, 'appid=')[-1]), 'oid=')[-2]), '') 
| extend PrincipalName = strcat(UPN, appId)
| project SessionId, PrincipalName
| join kind=leftouter
    (
    AzureDiagnostics
    | where ResourceProvider == 'MICROSOFT.DBFORPOSTGRESQL'
    | where TimeGenerated >= lookbackTime
    | where Message contains 'AUDIT: SESSION'
    | extend RoleName = tostring(split(tostring(split(Message, 'user=')[-1]), ',db')[-2])
    | where RoleName !in ('azuresu', '[unknown]', 'postgres', '')
    | extend SessionId = tostring(split(tostring(split(Message, 'session=')[-1]), ',sess_time')[-2])
    | extend SubMessage = tostring(split(Message, 'SESSION,')[-1])
    | extend splitArray = split(SubMessage, ',')
    | extend SqlQueryP1 = tostring(split(tostring(split(Message, ',,,')[-1]), ',<')[-2])
    | extend SqlQueryP2 = replace_string(tostring(split(SqlQueryP1, ',\"')[-1]), '"', '')
    | extend SqlQueryP3 = tostring(split(Message, ',,,')[1])
    | extend OperationType = tostring(splitArray[startIndex])
    | extend SqlQuery = trim('"', case(OperationType == 'EXECUTE', SqlQueryP2, SqlQueryP1 == '', SqlQueryP3, SqlQueryP1))
    )
    on $left.SessionId == $right.SessionId
| project TimeGenerated, PrincipalName, RoleName, OperationType, SqlQuery 
```

## Example results
The resulting table looks like this:

| TimeGenerated | PrincipalName | RoleName | OperationType | SqlQuery |
| --- | --- | --- | --- | --- |
| 2025-12-12T16:25:05.104Z | user@example.com | ExampleGroupName | SELECT | select * from pg_seclabels; |
| 2025-12-12T16:25:04.000Z | user@example.com | user@example.com | SELECT | select * from pg_seclabels; |

If the user is logging in as a group role, the columns `PrincipalName` and `role` differ (like in the first row of the example).  
The value in the `PrincipalName` identifies the user which logged in, and the value in the `role` identifies the role in PostgreSQL into which the user logged in.

`PrincipalName` will be either the [User Principal Name (UPN) or AppId](./security-entra-concepts.md#frequently-asked-questions) depending on whether the user principal or service principal was logged in.
