---
title: Use control plane role-based access control
titleSuffix: Azure Cosmos DB for Table
description: Grant access to manage account resources using role-based access control, Microsoft Entra, and Azure Cosmos DB for Table.
author: seesharprun
ms.author: sidandrews
ms.reviewer: iriaosara
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: how-to
ms.date: 02/05/2025
zone_pivot_groups: azure-interface-portal-cli-powershell-bicep
appliesto:
  - ✅ Table
#Customer Intent: As a security user, I want to grant an identity control-plane access to Azure Cosmos DB for Table, so that my developer team can use the SDK of their choice with minimal code change.
---

# Use control plane role-based access control with Azure Cosmos DB for Table

:::image type="complex" source="media/how-to-grant-control-plane-role-based-access/map.svg" border="false" alt-text="Diagram of the current location ('Role-based access control') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, Network, and Reference. The 'Role-based access control' location is currently highlighted.
:::image-end:::

This article walks through the steps to grant an identity access to manage an Azure Cosmos DB for Table account and its resources.

> [!IMPORTANT]
> The steps in this article only cover control plane access to perform operations on the account itself of any resources in the account's hierarchy. To learn how to manage roles, definitions, and assignments for the control plane, see [grant data plane role-based access](how-to-grant-data-plane-role-based-access.md).

[!INCLUDE[Grant control plane role-based access](../../includes/grant-control-plane-role-based-access.md)]

[!INCLUDE[Validate control plane role-based access](../../includes/validate-control-plane-role-based-access.md)]

## Next step

> [!div class="nextstepaction"]
> [Grant your identity data plane role-based access](how-to-grant-data-plane-role-based-access.md)
