---
title: Data plane actions reference (preview)
titleSuffix: Azure Cosmos DB for Table
description: This article includes a list of all potential data plane actions for use with role-based access control (RBAC) in Azure Cosmos DB for Table.
author: seesharprun
ms.author: sidandrews
ms.reviewer: stefarroyo
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: reference
ms.date: 12/18/2024
appliesto:
  - ✅ Table
hidden: true
ROBOTS: NOINDEX, NOFOLLOW
---

# Azure Cosmos DB for Table data plane actions reference (preview)

:::image type="complex" source="media/reference-data-plane-actions/map.svg" border="false" alt-text="Diagram of the current location ('Reference') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, and Reference. The 'Reference' location is currently highlighted.
:::image-end:::

Azure Cosmos DB for Table exposes a unique set of data actions within its native role-based access control implementation. This article includes a list of those actions and descriptions on what permissions are granted for each action.

> [!WARNING]
> Azure Cosmos DB for Table's native role-based access control doesn't support the `notDataActions` property. Any action that is not specified as an allowed `dataAction` is excluded automatically.

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
| **`Microsoft.DocumentDB/databaseAccounts/throughputSettings/read`** | Read the current throughput |
| **`Microsoft.DocumentDB/databaseAccounts/throughputSettings/write`** | Modify the current throughput |
| **`Microsoft.DocumentDB/databaseAccounts/tables/write`** | Create or update a table |
| **`Microsoft.DocumentDB/databaseAccounts/tables/delete`** | Delete a table |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/write`** | Create or update a container |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/delete`** | Delete a container |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/readChangeFeed`** | Read from the container's change feed |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/manageConflicts`** | Manage conflicts for multi-write region accounts (list and delete items from the conflict feed) |

### Data action wildcards

The wildcard (`*`) operator is supported at the `tables`, `containers`, and `entities` levels for actions. Use the wildcard to grant broad access to a specific resource type.

| | Description |
| --- | --- |
| **`Microsoft.DocumentDB/databaseAccounts/tables/*`** | Perform all operations on tables |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/*`** | Perform all operations on containers |
| **`Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/*`** | Perform all operations on entities (items) |
| **`Microsoft.DocumentDB/databaseAccounts/throughputSettings/*`** | Perform all operations related to throughput |

## Required metadata

The Azure Cosmos DB software development kits (SDKs) issue read-only metadata requests during initialization and to serve specific data requests. These requests fetch various configuration details such as:

- The global configuration of your account, which includes the Azure regions the account is available in
- The partition key of your containers or their indexing policy
- The list of physical partitions that make a container and their addresses
- They don't fetch any of the data that stored in your account

To ensure the best transparency of our permission model, these metadata requests are explicitly covered by the `Microsoft.DocumentDB/databaseAccounts/readMetadata` data action. This action must be allowed in every situation where your Azure Cosmos DB account is accessed through one of the Azure Cosmos DB SDKs.

The action can be assigned at any level in an Azure Cosmos DB account's hierarchy including account, database, or container. The actual metadata requests allowed depend on the scope:

- **Account**
  - Listing the databases under the account
  - For each database under the account, the allowed actions at the database scope
- **Table**
  - Reading table metadata
  - Listing the containers under the table
  - For each container under the table, the allowed actions at the container scope
- **Container**
  - Reading container metadata
  - Listing physical partitions under the table
  - Resolving the address of each physical partition

> [!IMPORTANT]
> You cannot manage throughput with the `Microsoft.DocumentDB/databaseAccounts/readMetadata` data action.

## Related content

[Data plane roles](reference-data-plane-roles.md)
