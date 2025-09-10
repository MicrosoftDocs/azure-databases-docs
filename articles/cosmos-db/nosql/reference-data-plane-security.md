---
title: Data plane security reference
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn about data plane actions and built-in roles for role-based access control in Azure Cosmos DB for NoSQL. See which permissions are available and how to use them.
author: seesharprun
ms.author: sidandrews
ms.reviewer: skhera
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.date: 09/10/2025
appliesto:
  - ✅ NoSQL
---

# Azure Cosmos DB for NoSQL data plane security reference

Azure Cosmos DB for NoSQL exposes a unique set of data actions and roles within its native role-based access control implementation. This article includes a list of those actions and roles with descriptions on what permissions are granted for each resource.

> [!WARNING]
> Azure Cosmos DB for NoSQL's native role-based access control doesn't support the `notDataActions` property. Any action that isn't specified as an allowed `dataAction` is excluded automatically.

## Built-in actions

Here's a list of data actions that can be individually set in a role definition.

| | Description |
| --- | --- |
| **`Microsoft.DocumentDB/databaseAccounts/readMetadata`** | Read [required metadata](#required-metadata) from account for data plane operations |
| **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/create`** | Creates new items |
| **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/read`** | Reads specific items by performing a point read using the partition key and unique identifier |
| **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/replace`** | Replaces existing items |
| **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/upsert`** | Creates a new item if it doesn't exist or replaces an existing item |
| **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/delete`** | Deletes an item |
| **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/executeQuery`** | Executes a NoSQL query |
| **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/readChangeFeed`** | Reads from the container's change feed |
| **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/executeStoredProcedure`** | Executes stored procedures |
| **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/manageConflicts`** | Manage conflicts for accounts using the conflict feed |

> [!NOTE]
> To perform NoSQL queries using the software development kits (SDKs), you must have both the `Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/executeQuery` and `Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/readChangeFeed` permissions.

### Data action wildcards

Wildcards are supported at both containers and items levels.

| | Description |
| --- | --- |
| **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*`** | Perform all container-specific operations like executing queries, reading the change feed, managing conflicts, and executing stored procedures |
| **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*`** | Perform all item-specific operations like creating, reading, updating, replacing, and deleting items |

## Built-in roles

Azure Cosmos DB for NoSQL defines data plane-specific role definitions. These roles are distinct from Azure role-based access control role definitions.

### Cosmos DB Built-in Data Reader

**ID**: `00000000-0000-0000-0000-000000000001`

- **Included actions**
  - `Microsoft.DocumentDB/databaseAccounts/readMetadata`
  - `Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/read`
  - `Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/executeQuery`
  - `Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/readChangeFeed`

### Cosmos DB Built-in Data Contributor

**ID**: `00000000-0000-0000-0000-000000000002`

- **Included actions**
  - `Microsoft.DocumentDB/databaseAccounts/readMetadata`
  - `Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*`
  - `Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*`

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
- **Database**
  - Reading database metadata
  - Listing the containers under the database
  - For each container under the database, the allowed actions at the container scope
- **Container**
  - Reading container metadata
  - Listing physical partitions under the container
  - Resolving the address of each physical partition

> [!IMPORTANT]
> You can't manage throughput with the `Microsoft.DocumentDB/databaseAccounts/readMetadata` data action.

## Related content

- [Security best practices](security.md)
