---
title: Quickstart - Azure portal
titleSuffix: Azure Cosmos DB for NoSQL
description: Deploy an Azure Cosmos DB account, database, and container using the Azure portal and Data Explorer.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: quickstart
ms.date: 09/18/2024
# CustomerIntent: As a cloud user, I want to create a new Azure Cosmos DB account, so that I can manage resources and data.
---

# Quickstart: Create an Azure Cosmos DB for NoSQL account using the Azure portal

APPLIES TO: :::image type="icon" source="~/reusable-content/ce-skilling/azure/media/cosmos-db/yes-icon.svg" border="false":::
NoSQL

> [!div class="op_single_selector"]
>
> - [Azure portal](quickstart-portal.md)
> - [Bicep](quickstart-template-bicep.md)
> - [Terraform](quickstart-terraform.md)
> - [Azure Resource Manager (JSON)](quickstart-template-json.md)
>

In this quickstart, you create a new Azure Cosmos DB for NoSQL account in the Azure portal. You then use the Data Explorer experience within the Azure portal to create a database and container configuring all required settings. Finally, you add sample data to the container and issue a basic query.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

## Create an account

Start by creating a new Azure Cosmos DB for NoSQL account

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Enter *Azure Cosmos DB* in the global search bar.

    :::image source="media/quickstart-portal/search-bar.png" lightbox="media/quickstart-portal/search-bar.png" alt-text="Screenshot of the global search bar in the Azure portal.":::

1. Within **Services**, select **Azure Cosmos DB**.

    :::image source="media/quickstart-portal/search-menu.png" alt-text="Screenshot of the Azure Cosmos DB option selected in the search menu.":::

1. In the **Azure Cosmos DB** pane, select **Create**, and then **Azure Cosmos DB for NoSQL**.

    :::image source="media/quickstart-portal/create-resource-option.png" alt-text="Screenshot of the Create option within the pane for an Azure service.":::

    :::image source="media/quickstart-portal/api-nosql-option.png" alt-text="Screenshot of the Azure Cosmos DB API selection pane with the API for NoSQL highlighted.":::

1. Within the **Basics** pane, configure the following options, and then select **Review + create**:

    | | Value |
    | --- | --- |
    | **Subscription** | Select your Azure subscription |
    | **Resource Group** | Create a new resource group or select an existing resource group |
    | **Account Name** | Provide a globally unique name |
    | **Availability Zones** | *Disable* |
    | **Location** | Select an Azure region that's supported by your subscription |

    :::image source="media/quickstart-portal/basics-pane.png" alt-text="Screenshot of the Azure Cosmos DB for NoSQL resource creation 'Basics' pane.":::

    > [!TIP]
    > You can leave any unspecified options to their default values.

1. On the **Review + create** pane, wait for validation of your account to finish successfully, and then select **Create**.

    :::image source="media/quickstart-portal/resource-validation.png" alt-text="Screenshot of the resource validation step in the creation experience.":::

1. The portal will automatically navigate to the **Deployment** pane. Wait for the deployment to complete.

    :::image source="media/quickstart-portal/deployment-pending.png" alt-text="Screenshot of the deployment pane with a currently pending deployment.":::

1. Once the deployment is complete, select **Go to resource** to navigate to the new Azure Cosmos DB for NoSQL account.

    :::image source="media/quickstart-portal/deployment-finalized.png" alt-text="Screenshot of a fully deployed resource with the 'Go to resource' option highlighted.":::

## Create a database and container

Next, use the Data Explorer to create a database and container in-portal.

1. TODO

    :::image source="media/quickstart-portal/" alt-text="TODO4":::

1. TODO

    :::image source="media/quickstart-portal/" alt-text="TODO5":::

## Add and query sample data

Finally, use the Data Explorer to create a sample item and then issue a basic query to the container.

1. TODO

    :::image source="media/quickstart-portal/" alt-text="TODO6":::

1. TODO

    :::image source="media/quickstart-portal/" alt-text="TODO7":::

## Related content

- [Data Explorer](../data-explorer.md)
- [NoSQL query syntax](query/index.yml)
- [Resource model](../resource-model.md)
