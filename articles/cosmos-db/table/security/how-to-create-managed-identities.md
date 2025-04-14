---
title: Create managed identities
titleSuffix: Azure Cosmos DB for Table
description: Review the steps required to create user-assigned or system-assigned managed identities for use with Azure hosting services that connect to Azure Cosmos DB for Table.
author: seesharprun
ms.author: sidandrews
ms.reviewer: stefarroyo
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: how-to
ms.date: 02/05/2025
ms.custom: subject-msia
zone_pivot_groups: azure-interface-portal-cli-powershell-bicep
appliesto:
  - ✅ Table
#Customer Intent: As a security user, I want to create managed identities for use with Azure hosting services, so that my developer team can write portable authentication code for their client.
---

# How to use managed identities with Azure services to connect to Azure Cosmos DB for Table

:::image type="complex" source="media/how-to-create-managed-identities/map.svg" border="false" alt-text="Diagram of the current location ('Prepare') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, and Reference. The 'Prepare' location is currently highlighted.
:::image-end:::

This article reviews the steps required to create managed identities to use with a deployed application connected to Azure Cosmos DB for Table.

[!INCLUDE[Managed identities](../../includes/managed-identities.md)]

## Next step

> [!div class="nextstepaction"]
> [Disable key-based authentication with Azure Cosmos DB for Table](how-to-disable-key-based-authentication.md)
