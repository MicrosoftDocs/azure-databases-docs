---
title: Secure your account
titleSuffix: Azure Cosmos DB for NoSQL
description: Review the fundamentals of securing Azure Cosmos DB for NoSQL from the perspective of data and networking security.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: best-practice
ms.date: 04/11/2025
ms.custom: security-horizontal-2025
ai-usage: ai-assisted
---

# Secure your Azure Cosmos DB for NoSQL account

TODO

This article provides guidance on how to best secure your Azure Cosmos DB for NoSQL deployment.

## Secure networking

TODO

### TODO - networking focus

TODO

## Secure data in flight

When working with Azure Cosmos DB for NoSQL, it's important to ensure that authorized users and applications have access to data while preventing unintentional or unauthorized access.

[!INCLUDE[Security data overview](../includes/security-data-overview.md)]

### TODO - data access focus

TODO

## Secure data at rest

TODO

### TODO - data encryption focus

TODO

## Glossary

This section includes a glossary of common terminology used in this security guide for Azure Cosmos DB for NoSQL.

[!INCLUDE[Security glossary](../includes/security-glossary.md)]

### Scope (Azure Cosmos DB native)

In Azure Cosmos DB's native implementation of role-based access control, scope refers to the granularity of resources within an account for which you want permission applied.

At the highest level, you can scope a data plane role-based access control assignment to the entire account using the largest scope. This scope includes all databases and containers within the account:

```output
/subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/
```

Or, you can scope your data plane role assignment to a specific database:

```output
/subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/dbs/<database-name>
```

Finally, you can scope the assignment to a single container, the most granular scope:

```output
/subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/dbs/<database-name>/colls/<container-name>
```

## Related content

- [Disable key-based authentication](how-to-disable-key-based-authentication.md)
- [Grant data plane role-based access](how-to-grant-data-plane-access.md)
- [Grant data plane control-plane access](how-to-grant-control-plane-access.md)
