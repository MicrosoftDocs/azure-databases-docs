---
title: Get signed in identity
titleSuffix: Azure Cosmos DB for Table
description: Get the unique identifier for the currently signed in account for Azure CLI so that you can use this identity with role-based access control in Azure to connect to Azure Cosmos DB for Table.
author: seesharprun
ms.author: sidandrews
ms.reviewer: stefarroyo
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: how-to
ms.date: 02/05/2025
zone_pivot_groups: azure-interface-portal-cli-powershell
appliesto:
  - ✅ Table
#Customer Intent: As a developer, I want to get my current signed-in identity for Azure CLI, so that my security team can grant me role-based access control permissions to access Azure resources.
---

# Get the signed in account's identity to use with Azure services to connect to Azure Cosmos DB for Table

:::image type="complex" source="media/how-to-get-signed-in-identity/map.svg" border="false" alt-text="Diagram of the current location ('Prepare') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, and Reference. The 'Prepare' location is currently highlighted.
:::image-end:::

This article gives simple steps to get the identity of the currently signed in account. You can use this identity information later to grant role-based access control access to the signed in account to either manage data or resources in Azure Cosmos DB for Table.

[!INCLUDE[Get signed in identity](../../includes/get-signed-in-identity.md)]

## Next step

> [!div class="nextstepaction"]
> [Create managed identities](how-to-create-managed-identities.md)
