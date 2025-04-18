---
title: Security terminology glossary
titleSuffix: Azure Cosmos DB for NoSQL
description: Explore common glossary terminology used when describing how to managed role-based access control within Azure Cosmos DB for NoSQL.
author: seesharprun
ms.author: sidandrews
ms.reviewer: skhera
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: glossary
ms.date: 04/18/2025
ai-usage: ai-assisted
appliesto:
  - ✅ NoSQL
---

# Security glossary

This article includes a glossary of common terminology used in this security guide for Azure Cosmos DB for NoSQL.

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

> [!TIP]
> In many cases, you can use the relative scope instead of the fully qualified scope. For example, you can use this relative scope to grant data plane role-based access control permissions to a specific database and container from an Azure CLI command:
>
> ```output
> /dbs/<database-name>/colls/<container-name>
> ```
>
> You can also grant universal access to all databases and containers using the relative scope:
>
> ```output
> /
> ```
>

## Related content

- [Security overview](security.md)
- [Disable key-based authentication](how-to-disable-key-based-authentication.md)
- [Grant data plane role-based access](how-to-grant-data-plane-access.md)
