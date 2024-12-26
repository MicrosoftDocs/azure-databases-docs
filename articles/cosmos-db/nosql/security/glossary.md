---
title: Security terminology glossary
titleSuffix: Azure Cosmos DB for NoSQL
description: Explore common glossary terminology used when describing how to managed role-based access control within Azure Cosmos DB for NoSQL.
author: seesharprun
ms.author: sidandrews
ms.reviewer: iriaosara
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: glossary
ms.date: 10/01/2024
ai-usage: ai-assisted
---

# Security glossary for Azure Cosmos DB for NoSQL

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

:::image type="complex" source="media/glossary/map.svg" border="false" alt-text="Diagram of the current location ('Concepts') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, Network, and Reference. The 'Concepts' location is currently highlighted.
:::image-end:::

This article includes a glossary of common terminology used in this security guide for Azure Cosmos DB for NoSQL.

[!INCLUDE[Security glossary](../../includes/security-glossary.md)]

## Scope (Azure Cosmos DB native)

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

## Next step

> [!div class="nextstepaction"]
> [Get signed in account's identity](how-to-get-signed-in-identity.md)
