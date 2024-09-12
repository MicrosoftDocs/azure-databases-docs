---
title: Data actions reference
titleSuffix: Azure Cosmos DB for Table
description: This article includes a list of all potential data actions for use with role-based access control (RBAC) in Azure Cosmos DB for Table.
author: seesharprun
ms.author: sidandrews
ms.reviewer: stefarroyo
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: reference
ms.date: 09/11/2024
---

# Azure Cosmos DB for Table data actions reference

[!INCLUDE[Table](../../includes/appliesto-table.md)]

:::image type="complex" source="media/reference-data-actions/map.svg" border="false" alt-text="Diagram of the current location ('Reference') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, and Reference. The 'Reference' location is currently highlighted.
:::image-end:::

Azure Cosmos DB for Table exposes a unique set of data actions within its native role-based access control implementation. This article includes a list of those actions and descriptions on what permissions are granted for each action.

## Data actions

Here's a list of data actions that can be individually set in a role definition.

| | Description |
| --- | --- |
| **`Microsoft.DocumentDB/databaseAccounts/readMetadata`** | Read some account metadata |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/executeQuery`** | Executes a query against a table |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/executeStoredProcedure`** | Executes a table transaction (procedure) |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/create`** | Creates a new entity (item) |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/read`** | Point reads an individual entity (item) using the row and partition keys |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/replace`** | Entirely replaces an existing entity (item) |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/upsert`** | Creates an entity (item) if it doesn't exist or replaces the entity if it already exists |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/delete`** | Deletes an entity (item) |

### Wildcards

The wildcard (`*`) operator is supported at the `tables`, `containers`, and `entities` levels for actions. Use the wildcard to grant broad access to a specific resource type.

| | Description |
| --- | --- |
| **`Microsoft.DocumentDB/databaseAccounts/tables/*`** | Perform all operations on tables |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/*`** | Perform all operations on containers |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/*`** | Perform all operations on entities (items) |

## Related content

- [Microsoft Identity platform](/entra/identity-platform)
- [Azure role-based access control](/azure/role-based-access-control)
- [Azure SDK](https://github.com/azure/azure-sdk)
