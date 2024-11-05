---
title: Use Visual Studio Code to connect and Manage Azure Cosmos DB resources 
description: Learn how to connect to Azure Cosmos DB for NoSQL or Azure Cosmos DB for MongoDB (vCore) cluster by using Visual Studio Code. 
author: khelanmodi
ms.author: khelanmodi
ms.reviewer: gahllevy, sasinnat, esarroyo
ms.date: 11/05/2024
ms.service: azure-cosmos-db
ms.topic: how-to
keywords: connect to cosmos db for nosql or cosmos db for mongodb database
zone_pivot_groups: azure-cosmos-db-apis-nosql-mongodb
---

# Quickstart: Use Visual Studio Code to connect and query Azure Cosmos DB instances

[!INCLUDE[NoSQL, MongoDB](includes/appliesto-nosql-mongodb.md)]

[Visual Studio Code](https://code.visualstudio.com/docs) is a versatile code editor for Linux, macOS, and Windows, supporting numerous extensions. This quickstart shows you how to connect to Azure Cosmos DB for NoSQL and Azure Cosmos DB for MongoDB (vCore) cluster using Visual Studio Code. It covers performing core database operations, including querying, inserting, updating, and deleting data.

::: zone pivot="api-nosql"

## Prerequisites

Before you begin, ensure you have the following:

- An Azure Cosmos DB account configured with a database in either Azure Cosmos DB for NoSQL. Use one of these quickstarts to set up a database:
    - [Portal](./nosql/quickstart-portal.md) 
    - [Azure CLI](./nosql/quickstart-template-bicep.md) 

- To connect and manage data in Azure Cosmos DB, you’ll need to install the **Azure Databases** extension for Visual Studio Code.

1. Open Visual Studio Code.
2. Access the **Extensions** pane by selecting **View > Extensions** or using the shortcut **Ctrl + Shift + X**.
3. In the search bar, type [Azure Databases extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb) and select the extension. Then, click **Install**.
4. After installation, reload Visual Studio Code if prompted.

### Connecting to an Azure Cosmos DB for NoSQL

1. In Visual Studio Code, go to the **Azure** pane (select the **Azure** icon in the Activity Bar).
2. Sign in to your Azure account via Entra ID:
**Note**: It is recommended to always use Microsoft Entra ID RBAC when accessing your Azure Cosmos DB resources (instead of account keys) for the most secure authentication method.
3. Once you are signed in, in the Azure tree view, find your Azure Subscription and drill down to Azure Cosmos DB. 
4. Select an existing account or right-click to create a new resource.

## Query and display your data
The following steps will use the Query Editor to execute a query and view the results of the query:

1. In the menu for your collection, right-click on the collection to open the Query Editor in Preview.

     :::image type="content" source="media/dev-tooling/VS-code/open-query-editor.png" lightbox="media/dev-tooling/VS-code/open-query-editor.png" alt-text="Screenshot of the query editor in VS Code.":::

2. Run the query provided in the query editor to display your data in **Table View**:

    :::image type="content" source="media/dev-tooling/VS-code/view-query-editor-results.png" lightbox="media/dev-tooling/VS-code/view-query-editor-results.png" alt-text="Screenshot of the query editor results in VS Code.":::

3. Explore your data in other supported views:

- **JSON View**: See the raw data structure.
    :::image type="content" source="media/dev-tooling/VS-code/view-json-view.png" lightbox="media/dev-tooling/VS-code/view-json-views.png" alt-text="Screenshot of the query editor results in json view.":::
- **Tree View**: Navigate nested data with ease.
    :::image type="content" source="media/dev-tooling/VS-code/view-tree-view.png" lightbox="media/dev-tooling/VS-code/view-tree-view.png" alt-text="Screenshot of the query editor results in tree view.":::


## View query and index metrics
Within the query editor, view additional query and index metrics to better help optimize your query performance.

1. Select the **Stats** tab next to the  query **Results**.
    :::image type="content" source="media/dev-tooling/VS-code/view-query-stats.png" lightbox="media/dev-tooling/VS-code/view-query-stats.png" alt-text="Screenshot of the query stats in VS Code.":::

2. For more information on the metric definitions view the [query metrics documentation](./nosql/query-metrics.md).


## Insert, Edit and Delete documents
- **Real-time document editing**: Add, view, edit, and delete documents instantly, with changes reflected in real-time.
- **Import from JSON**: Load your data quickly from JSON files.
- **Export Data**: Save entire collections or query results as JSON for backup or sharing.


 ## Export query results
Move data in and out seamlessly:
- **Import from JSON**: Load your data quickly from JSON files.
- **Export Data**: Save entire collections or query results as JSON for backup or sharing.



## Next steps
In this tutorial, you've learned how to query data in VS Code, export query results, view query and index metrics for tuning query performance and display data in the multiple supported views. You can now use the Azure Databases VS Code Extension to review real data in your database.

- [Get started with the API for NoSQL](nosql/quickstart-dotnet.md)
- [Node.js Quickstart](quickstart-nodejs.md)
- [Python Quickstart](quickstart-python.md)
- [Java Quickstart](quickstart-java.md)
- [Go Quickstart](quickstart-go.md)

::: zone-end

::: zone pivot="api-mongodb"

## Prerequisites

Before you begin, ensure you have the following:
- An Azure Cosmos DB account configured with a database in Azure Cosmos DB for MongoDB. Use one of these quickstarts to set up a database:
    - [Portal](./mongodb/vcore/quickstart-portal.md) 
    - [Azure CLI](./mongodb/vcore/quickstart-bicep.md)
- To connect and manage data in Azure Cosmos DB, you need to install the **Azure Databases** extension for Visual Studio Code.
    1. Open Visual Studio Code.
    2. Access the **Extensions** pane by selecting **View > Extensions** or using the shortcut **Ctrl + Shift + X**.
    3. In the search bar, type [Azure Databases extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb) and select the extension. Then, click **Install**.
    4. After installation, reload Visual Studio Code if prompted.
- MongoDB shell (mongosh) installed for command-line interactions (optional but recommended).

---

## Connecting to a MongoDB workload

## [Connecting to Azure Cosmos DB for MongoDB (vCore) cluster](#tab/CBDMongovCore)

1. In the **Azure Databases** extension, expand the **Azure Resources** section.
1. Locate **Subscription** you have your MongoDB workload. Under the desired subscription, you will notice **Azure Cosmos DB for MongoDB (vCore)** branch. Expand the branch to view your clusters and databases.
1. Choose your Azure Cosmos DB for MongoDB (vCore) cluster from the expanded list.
1. When prompted, enter the admin password for your cluster.
1. Once authenticated, you’ll gain access to your cluster. 

> [!NOTE]
> Your password is only used for authentication and is not stored.

>[!NOTE]
>In many corporate environments, developer machine IP addresses are hidden due to a VPN or other corporate network settings. In these cases, it's recommended to start with [allowing access to all IP addresses](./mongodb/vcore/quickstart-portal.md) by adding the 0.0.0.0 - 255.255.255.255 firewall rule for connection testing initially before refining the allow-list.

:::image type="content" source="./mongodb/vcore/media/quickstart-portal/networking-settings-at-provisioning.png" alt-text="Screenshot of networking and firewall options for a cluster.":::

## [Connecting to any MongoDB cluster](#tab/MongoDB)

1. In the **Workspace** panel, expand the **MongoDB accounts** section.
2. Here, you can view all your MongoDB accounts. To connect to a new MongoDB account using a connection string, click **New Connection** and enter the connection string when prompted. 
   - Optionally, you may be asked to provide your username and password for authentication. 

>[!Note]
>All successfully connected MongoDB clusters will remain listed in the MongoDB accounts section, even after closing VS Code.

---

## Intuitive Data Management
Manage your databases effortlessly:
- **Create and Drop Databases/Collections**: Create or delete databases and collections directly in Visual Studio Code by right-clicking on your account in the resource panel.
- **Import from JSON**: Load your data quickly from JSON files.
- **Export Data**: Save entire collections or query results as JSON for backup or sharing.
- **Real-time Document Editing**: Add, view, edit, and delete documents instantly, with changes reflected in real-time.
:::image type="content" source="./media/dev-tooling/VS-code/vCore-vs-code-screenshot.png" alt-text="Screenshot of VS-code extension of a CosmosDB for MongoDB (vCore) cluster" lightbox="./media/dev-tooling/VS-code/vCore-vs-code-screenshot.png":::

Azure Cosmos DB for MongoDB (vCore) and any MongoDB clusters you add are now conveniently accessible in one unified interface!

## Powerful Query Tools
Run and refine your queries with ease:
- **Execute Queries Directly**: Write and run MongoDB queries with helpful features like syntax highlighting and auto-completion.
- **Instant Results**: View query results immediately in a format that works best for you—Table, JSON, or Tree view.

## Flexible Data Views
Explore your data in multiple ways:
- **JSON View**: See the raw data structure.
:::image type="content" source="./media/dev-tooling/VS-code/vCore-vs-code-json-view.png" alt-text="Screenshot of VS-code extension of a CosmosDB for MongoDB (vCore) cluster in JSON view" lightbox="./media/dev-tooling/VS-code/vCore-vs-code-json-view.png":::
- **Tree View**: Navigate nested data with ease.
:::image type="content" source="./media/dev-tooling/VS-code/vCore-vs-code-tree-view.png" alt-text="Screenshot of VS-code extension of a CosmosDB for MongoDB (vCore) cluster in Tree view" lightbox="./media/dev-tooling/VS-code/vCore-vs-code-tree-view.png":::
- **Table View**: Quickly scan through data and drill down into nested data with just a double-click.
:::image type="content" source="./media/dev-tooling/VS-code/vCore-vs-code-table-view.png" alt-text="Screenshot of VS-code extension of a CosmosDB for MongoDB (vCore) cluster in Table view" lightbox="./media/dev-tooling/VS-code/vCore-vs-code-table-view.png":::

## Mongo Shell Integration

Command-line functionality is available:
- **Launch `mongosh`**: Execute advanced MongoDB commands directly from Visual Studio Code.
> [!Note] 
>The MongoDB shell (`mongosh`) is not included with the extension. It must be installed separately and configured manually.

## Cluster Management at Your Fingertips
Stay on top of your resources:
- **View Cluster Details**: Check your cluster’s tier, server version, and resource usage.
- **Manage Tags**: Organize your clusters with tags that sync with the Azure Portal.

## Next steps

> [!div class="nextstepaction"]
> [Migrate your MongoDB workload to Azure Cosmos DB](./mongodb/vcore/migration-options.md)

::: zone-end



