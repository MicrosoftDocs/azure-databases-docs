---
title: Create managed identities
titleSuffix: Azure Cosmos DB for NoSQL
description: Review the steps required to create user-assigned or system-assigned managed identities for use with Azure hosting services that connect to Azure Cosmos DB for NoSQL.
author: seesharprun
ms.author: sidandrews
ms.reviewer: iriaosara
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 10/01/2024
ms.custom: subject-msia
zone_pivot_groups: azure-interface-portal-cli-powershell-bicep
#Customer Intent: As a security user, I want to create managed identities for use with Azure hosting services, so that my developer team can write portable authentication code for their client.
---

# How to use managed identities with Azure services to connect to Azure Cosmos DB for NoSQL

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

:::image type="complex" source="media/how-to-create-managed-identities/map.svg" border="false" alt-text="Diagram of the current location ('Prepare') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, Network, and Reference. The 'Prepare' location is currently highlighted.
:::image-end:::

This article reviews the steps required to create managed identities to use with a deployed application connected to Azure Cosmos DB for NoSQL.

[!INCLUDE[Managed identities](../../includes/managed-identities.md)]

## Next step

> [!div class="nextstepaction"]
> [Disable key-based authentication with Azure Cosmos DB for NoSQL](how-to-disable-key-based-authentication.md)
