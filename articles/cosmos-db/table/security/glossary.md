---
title: Security terminology glossary
titleSuffix: Azure Cosmos DB for Table
description: Explore common glossary terminology used when describing how to managed role-based access control within Azure Cosmos DB for Table.
author: seesharprun
ms.author: sidandrews
ms.reviewer: stefarroyo
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: glossary
ms.date: 02/05/2025
ai-usage: ai-assisted
appliesto:
  - ✅ Table
---

# Security glossary for Azure Cosmos DB for Table

:::image type="complex" source="media/glossary/map.svg" border="false" alt-text="Diagram of the current location ('Concepts') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, and Reference. The 'Concepts' location is currently highlighted.
:::image-end:::

This article includes a glossary of common terminology used in this security guide for Azure Cosmos DB for Table.

[!INCLUDE[Security glossary](../../includes/security-glossary.md)]

## Scope (Azure Cosmos DB native)

In Azure Cosmos DB's native implementation of role-based access control, scope refers to the granularity of resources within an account for which you want permission applied.

At the highest level, you can scope a data plane role-based access control assignment to the entire account using the largest scope. This scope includes all databases and containers within the account:

```output
/subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/
```

Or, you can scope your data plane role assignment to the default database:

```output
/subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/dbs/TablesDB
```

> [!IMPORTANT]
> The default database, `TablesDB`, is case-sensitive. If you use the wrong casing in a scope, the scope will be truncated to the largest scope allowed (account level).

Finally, you can scope the assignment to a single container (table), the most granular scope:

```output
/subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/dbs/TablesDB/colls/<container-name>
```

## Next step

> [!div class="nextstepaction"]
> [Disable key-based authentication](how-to-disable-key-based-authentication.md)
