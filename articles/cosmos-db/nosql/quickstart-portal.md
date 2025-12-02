---
title: Quickstart - Azure portal
titleSuffix: Azure Cosmos DB for NoSQL
description: Deploy an Azure Cosmos DB account, database, and container using the Azure portal and Data Explorer.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: quickstart
ms.date: 11/03/2025
ms.custom: sfi-image-nochange
# CustomerIntent: As a cloud user, I want to create a new Azure Cosmos DB account, so that I can manage resources and data.
---

# Quickstart: Create an Azure Cosmos DB for NoSQL account using the Azure portal

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

[!INCLUDE[Interface Quickstart selector](includes/quickstart/interface-selector.md)]

In this quickstart, you create a new Azure Cosmos DB for NoSQL account in the Azure portal. You then use the Data Explorer experience within the Azure portal to create a database and container configuring all required settings. Finally, you add sample data to the container and issue a basic query.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

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
    | **Location** | Select a supported Azure region for your subscription |

    :::image source="media/quickstart-portal/basics-pane.png" alt-text="Screenshot of the Azure Cosmos DB for NoSQL resource creation 'Basics' pane.":::

    > [!TIP]
    > You can leave any unspecified options to their default values. You can also configure the account to limit total account throughput to 1,000 request units per second (RU/s) and enable free tier to minimize your costs.

1. On the **Review + create** pane, wait for validation of your account to finish successfully, and then select **Create**.

    :::image source="media/quickstart-portal/resource-validation.png" alt-text="Screenshot of the resource validation step in the creation experience.":::

1. The portal automatically navigates to the **Deployment** pane. Wait for the deployment to complete.

    :::image source="media/quickstart-portal/deployment-pending.png" alt-text="Screenshot of the deployment pane with a currently pending deployment.":::

1. Once the deployment is complete, select **Go to resource** to navigate to the new Azure Cosmos DB for NoSQL account.

    :::image source="media/quickstart-portal/deployment-finalized.png" alt-text="Screenshot of a fully deployed resource with the 'Go to resource' option highlighted.":::

## Create a database and container

Next, use the Data Explorer to create a database and container in-portal.

1. In the account resource pane, select **Data Explorer** in the service menu.

    :::image source="media/quickstart-portal/service-menu-data-explorer.png" alt-text="Screenshot of the Data Explorer option in the service menu for the account.":::

1. In the **Data Explorer** pane, select the **New Container** option.

    :::image source="media/quickstart-portal/new-container-option.png" alt-text="Screenshot of the 'New Container' option in the Data Explorer.":::

1. In the **New Container** dialog, configure the following values and then select **OK**:

    | | Value |
    | --- | --- |
    | **Database** | *Create new* |
    | **Database id** | `cosmicworks` |
    | **Share throughput across containers** | Don't select |
    | **Container id** | `employees` |
    | **Partition key** | `department/name` |
    | **Container throughput (autoscale)** | *Autoscale* |
    | **Container Max RU/s** | `1000` |

    :::image source="media/quickstart-portal/new-container-dialog.png" alt-text="Screenshot of the dialog to create a new database and container with the specified options filled.":::

1. Create a new file named *demo.bicepparam* or (`demo.bicepparam`).

1. Observe the newly created database and container in the Data Explorer's hierarchy.

    :::image source="media/quickstart-portal/data-explorer-tree.png" alt-text="Screenshot of the Data Explorer hierarchy with a database container present.":::

    > [!TIP]
    > Optionally, you can expand the container node to observe extra properties and configuration settings.

## Add and query sample data

Finally, use the Data Explorer to create a sample item and then issue a basic query to the container.

1. Expand the node for the **employees** container in the tree of the Data Explorer. Then, select the **Items** option.

    :::image source="media/quickstart-portal/data-explorer-container-items.png" alt-text="Screenshot of the 'Items' option within a container in the Data Explorer hierarchy.":::

1. In the Data Explorer's menu, select **New Item**.

    :::image source="media/quickstart-portal/data-explorer-container-new-item.png" alt-text="Screenshot of the 'New Item' option within the Data Explorer menu.":::

1. Now, insert the following JSON for a new item in the **employees** container and then select **Save**:

    ```json
    {
      "id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
      "name": {
        "first": "Kai",
        "last": "Carter"
      },
      "email": "<kai@adventure-works.com>",
      "department": {
        "name": "Logistics"
      }
    }
    ```

    :::image source="media/quickstart-portal/data-explorer-new-item.png" alt-text="Screenshot of the JSON content for a new item within the Data Explorer.":::

1. In the Data Explorer's menu, select **New SQL Query**.

    :::image source="media/quickstart-portal/data-explorer-new-query.png" alt-text="Screenshot of the 'New SQL Query' option within the Data Explorer menu.":::

1. Now, insert the following NoSQL query to get all items for the `logistics` department using a case-insensitive search. The query then formats the output as a structured JSON object. Run the query by selecting **Execute Query**:

    ```nosql
    SELECT VALUE {
        "name": CONCAT(e.name.last, " ", e.name.first),
        "department": e.department.name,
        "emailAddresses": [
            e.email
        ]
    }
    FROM
        employees e
    WHERE
        STRINGEQUALS(e.department.name, "logistics", true)
    ```

    :::image source="media/quickstart-portal/data-explorer-query.png" alt-text="Screenshot of NoSQL query text within the Data Explorer.":::

1. Observe the JSON array output from the query.

    ```json
    [
      {
        "name": "Carter Kai",
        "department": "Logistics",
        "emailAddresses": [
          "kai@adventure-works.com"
        ]
      }
    ]
    ```

    :::image source="media/quickstart-portal/data-explorer-query-results.png" alt-text="Screenshot of the results of the previous NoSQL query's execution in the Data Explorer.":::

### Explore more setup and optimization guidance

After you create and query your data, use the **Overview** section to try different features of Azure Cosmos DB.

1. In the account resource pane, select **Overview** in the service menu.

1. Review the resources in the **Overview Hub** including, but not limited to:

    - **Quickstarts** to help you build and test your application.

    - **Setup & Optimization guidance** to support every stage of your journey from learning to production. Sections include partitioning, indexing, modeling, cost control, backup configuration, and performance tuning.

    - **Containers & Data access** for querying your data, adjusting throughput, and opening containers in Data Explorer or Visual Studio Code.

    - **Monitoring tools** such as Insights, Metrics, Alerts, and Diagnostic settings, plus a scorecard that surfaces availability, alerts, and Azure Advisor recommendations.

    - **Learning resources** like video tutorials, sample apps, and documentation.

    - **Actionable recommendations** personalized to your account for reliability, security, and cost efficiency.

    :::image source="media/quickstart-portal/overview-setup.png" lightbox="media/quickstart-portal/overview-setup.png" alt-text="Screenshot of the setup and optimization section of the Overview Hub in the Azure portal.":::

> [!TIP]
> The content shown in the Overview Hub adapts to your activity and workload type to make it easier to find what's most relevant to you.

## Related content

- [Data Explorer](../data-explorer.md)
- [NoSQL query syntax](/cosmos-db/query)
- [Resource model](../resource-model.md)
