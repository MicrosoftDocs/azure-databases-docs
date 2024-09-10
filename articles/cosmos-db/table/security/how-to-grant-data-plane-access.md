---
title: Grant data plane access
titleSuffix: Azure Cosmos DB for Table
description: Grant access to run queries and perform operations on items using role-based access control, Microsoft Entra, and Azure Cosmos DB for Table.
author: seesharprun
ms.author: sidandrews
ms.topic: how-to
ms.date: 09/09/2024
ms.custom: subject-msia
#Customer Intent: As a security user, I want to grant an identity data-plane access to Azure Cosmos DB for Table, so that my developer team can use the SDK of their choice with minimal code change.
---

# Grant data plane access to Azure Cosmos DB for Table

[!INCLUDE[Table](../../includes/appliesto-table.md)]

:::image type="complex" source="media/how-to-grant-data-plane-access/map.svg" border="false" alt-text="Diagram of the current location ('Role-based access control') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, and Solution. The 'Role-based access control' location is currently highlighted.
:::image-end:::

This article walks through the steps to grant an identity access to manage data in an Azure Cosmos DB for Table account. The steps in this article only cover data plane access to perform operations on individual items and run queries.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).
- An existing Azure Cosmos DB for Table account.
- An existing identity in Microsoft Entra ID.

## Get the account's unique identifier

TODO

1. TODO

## Create role-based access control definition

TODO

1. TODO

## Assign role-based access control permission

TODO

1. TODO

## Next step

> [!div class="nextstepaction"]
> [Full stack secure code sample for Azure Cosmos DB for Table](/samples/azure-samples/cosmos-db-table-role-based-access-control/template/)