---
title: Grant control plane access
titleSuffix: Azure Cosmos DB for Table
description: Grant access to manage account resources using role-based access control, Microsoft Entra, and Azure Cosmos DB for Table.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: how-to
ms.date: 09/09/2024
ms.custom: subject-msia
#Customer Intent: As a security user, I want to grant an identity control-plane access to Azure Cosmos DB for Table, so that my ops team can manage account resources.
---

# Grant control plane access to Azure Cosmos DB for Table

[!INCLUDE[Table](../../includes/appliesto-table.md)]

:::image type="complex" source="media/how-to-grant-control-plane-access/map.svg" border="false" alt-text="Diagram of the current location ('Role-based access control') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, and Solution. The 'Role-based access control' location is currently highlighted.
:::image-end:::

This article walks through the steps to grant an identity access to manage resources in an Azure Cosmos DB for Table account. The steps in this article only cover control plane access to manage the hierarchy of resources.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).
- An existing Azure Cosmos DB for Table account.
- One or more existing identities in Microsoft Entra ID.

## Get the account's unique identifier

TODO

1. TODO

## Create role-based access control definition

TODO

1. TODO

1. TODO. Name file *control-plane-definition.bicep*.

    ```bicep
    
    ```

1. TODO

    ```azurecli-interactive
    az group deployment create `
        --resource-group "<name-of-destination-resource-group>" `
        --template-file control-plane-definition.bicep
    ```

1. TODO

## Assign role-based access control permission

TODO

1. TODO

1. TODO. Name file *control-plane-assignment.bicep*.

    ```bicep

    ```

1. TODO. Name file *control-plane-assignment-params.json*.

    ```json

    ```

1. TODO. [`az group deployment create`](/cli/azure/group/deployment#az-group-deployment-create)

    ```azurecli-interactive
    az group deployment create `
        --resource-group "<name-of-destination-resource-group>" `
        --parameters @data-plane-assignment-params.json `
        --template-file data-plane-assignment.bicep
    ```

1. TODO

## Next step

> [!div class="nextstepaction"]
> [Grant your identity data-plane access](how-to-grant-data-plane-access.md)
