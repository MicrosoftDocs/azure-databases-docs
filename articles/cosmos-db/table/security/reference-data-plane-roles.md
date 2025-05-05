---
title: Data plane built-in roles reference (preview)
titleSuffix: Azure Cosmos DB for Table
description: This article includes a list of all built-in data plane roles for use with role-based access control (RBAC) in Azure Cosmos DB for Table.
author: seesharprun
ms.author: sidandrews
ms.reviewer: iriaosara
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: reference
ms.date: 02/05/2025
appliesto:
  - ✅ Table
---

# Azure Cosmos DB for Table data plane built-in roles reference (preview)

:::image type="complex" source="media/reference-data-plane-roles/map.svg" border="false" alt-text="Diagram of the current location ('Reference') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, Network, and Reference. The 'Reference' location is currently highlighted.
:::image-end:::

Azure Cosmos DB for Table includes built-in data plane roles within its native role-based access control implementation. This article includes a list of those roles and descriptions on what permissions are granted for each role.

## Built-in data plane roles

Azure Cosmos DB for Table defines data plane-specific role definitions. These roles are distinct from Azure role-based access control role definitions.

### Cosmos DB Built-in Data Reader

**ID**: `00000000-0000-0000-0000-000000000001`

- **Included actions**
  - `Microsoft.DocumentDB/databaseAccounts/readMetadata`
  - `Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/read`

### Cosmos DB Built-in Data Contributor

**ID**: `00000000-0000-0000-0000-000000000002`

- **Included actions**
  - `Microsoft.DocumentDB/databaseAccounts/readMetadata`
  - `Microsoft.DocumentDB/databaseAccounts/tables/*`
  - `Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/*`

## Related content

- [Data plane actions](reference-data-plane-actions.md)
