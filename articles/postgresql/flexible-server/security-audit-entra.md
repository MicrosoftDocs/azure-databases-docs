---
title: Audit Logging in in Azure Database for PostgreSQL for Entra ID principals
description: Learn how to attribute actions to specific Entra ID users in PostgreSQL audit logs.
author: ajanko
ms.author: ajanko
ms.reviewer: ajanko
ms.date: 12/12/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
ms.custom:
  - horz-security
---

# Audit logging in Azure Database for PostgreSQL for Entra ID principals

Database audits are one of the important components that need to be set up based on your organization’s compliance requirements, where you can monitor the targeted activities to achieve your security baseline. In Azure database for PostgreSQL flexible server, you can achieve that by using pgaudit PG extension as described in Audit logging in [Azure Database for PostgreSQL - Flexible server](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-audit).

One of the challenges is utilizing auditing feature alongside PostgreSQL Flexible Server Entra ID authentication when you are using Entra ID groups and want to audit the actions of indvidual groups members. This is because when group members sign in, they use their personal access tokens but use the group name as the username.

Kusto Query Language (KQL) is a powerful pipeline-driven, read-only query language that enables querying Azure Service Logs. KQL supports querying Azure logs to quickly analyze a high volume of data. For this article, we will use the KQL to query Azure Postgres Logs and extract Entra ID user information from audit logs.

## Prerequisites:

1. Enable Audit logging - [Audit logging in Azure Database for PostgreSQL - Flexible server](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-audit)
1. Enable Azure Postgres logs to be sent to Azure log analytics - [Configure Log Analytics](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/howto-configure-and-access-logs#configure-diagnostic-settings)
1. Adjust “log_line_prefix” server parameter:  
* From the Server Parameters blade set the "log line prefix" to include the escapes "user=%u,db=%d,session=%c,sess_time=%s"  in the same sequence, in order to get the desired results  
  * Before:  log_line_prefix = "%t-%c-"  
  * After: log_line_prefix = "%t-%c-user=%u,db=%d,session=%c,sess_time=%s"

```kusto
let lookbackTime = ago(88d);
let opindex = 3;
let startIndex = toscalar(range thirdIndex from opindex to opindex step 1
    | project thirdIndex);
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.DBFORPOSTGRESQL"
| where TimeGenerated >= lookbackTime
| where Message contains "Microsoft Entra ID connection"
| extend SessionId = tostring(split(tostring(split(Message, "session=")[-1]), ",sess_time")[-2])
| extend UPN = iff(Message contains "UPN",tostring(split(tostring(split(Message, "UPN=")[-1]), "oid=")[-2]), "")
| extend appId = iff(Message contains "appid", tostring(split(tostring(split(Message, "appid=")[-1]), "oid=")[-2]), "") 
| extend role = tostring(split(tostring(split(Message, "user=")[-1]), ",db=")[-2])
| extend PrincipalName = strcat(UPN, appId)
| project Message, TimeGenerated, SessionId, UPN, role, appId, PrincipalName
| join kind=leftouter
    (
    AzureDiagnostics
    | where ResourceProvider == "MICROSOFT.DBFORPOSTGRESQL"
    | where TimeGenerated >= lookbackTime
    | where Message contains "AUDIT: SESSION"
    | extend UserName = tostring(split(tostring(split(Message, "user=")[-1]), ",db")[-2])
    | extend SessionId = tostring(split(tostring(split(Message, "session=")[-1]), ",sess_time")[-2])
    | where UserName !in ('azuresu', '[unknown]', 'postgres', '')
    | extend SubMessage = tostring(split(Message, "SESSION,")[-1])
    | extend splitArray = split(SubMessage, ',')
    | extend operationType = tostring(splitArray[startIndex])
    | extend SqlQueryP1 = tostring(split(tostring(split(Message, ",,,")[-1]), ",<")[-2])
    | extend SqlQueryP2 = replace_string(tostring(split(SqlQueryP1, ",\"")[-1]), '"', '')
    | extend SqlQueryP3 = tostring(split(Message, ",,,")[1])
    | extend SqlQuery = trim('"', case(operationType == "EXECUTE", SqlQueryP2, SqlQueryP1 == "", SqlQueryP3, SqlQueryP1))
    )
    on $left.SessionId == $right.SessionId
| project TimeGenerated, PrincipalName, role, SqlQuery, operationType, Message

```

Results:
# add photo here


If the user is logging in as a group role, the columns `PrincipalName` and `role` will differ. The value in the `PrincipalName` will identify the user which logged in, and the value in the `role` will identify the role in PostgreSQL into which the user logged in.

`PrincipalName` will be either the [User Principal Name (UPN) or AppId](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/security-entra-concepts#frequently-asked-questions) depending on whether the user principal or service principal was logged in.
