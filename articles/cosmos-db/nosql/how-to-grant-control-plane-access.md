---
title: Use control plane role-based access control
titleSuffix: Azure Cosmos DB for NoSQL
description: Grant access to manage account resources using role-based access control, Microsoft Entra, and Azure Cosmos DB for NoSQL.
author: seesharprun
ms.author: sidandrews
ms.reviewer: skhera
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 04/18/2025
zone_pivot_groups: azure-interface-portal-cli-powershell-bicep
appliesto:
  - ✅ NoSQL
#Customer Intent: As a security user, I want to grant an identity control-plane access to Azure Cosmos DB for NoSQL, so that my developer team can use the SDK of their choice with minimal code change.
---

# Use control plane role-based access control with Azure Cosmos DB for NoSQL

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

This article walks through the steps to grant an identity access to manage an Azure Cosmos DB for NoSQL account and its resources.

> [!IMPORTANT]
> The steps in this article only cover control plane access to perform operations on the account itself of any resources in the account's hierarchy. To learn how to manage items and execute queries for the data plane, see [grant data plane role-based access](how-to-grant-data-plane-access.md).

[!INCLUDE[Grant control plane role-based access](../includes/grant-control-plane-role-based-access.md)]

[!INCLUDE[Validate control plane role-based access](../includes/validate-control-plane-role-based-access.md)]

## Related content

- [Security best practices](security.md)
- [Disable key-based authentication](how-to-disable-key-based-authentication.md)
- [Grant data plane role-based access](how-to-grant-data-plane-access.md)
