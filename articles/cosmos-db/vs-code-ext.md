---
title: Use Visual Studio Code to connect and query Azure Cosmos DB resources 
titleSuffix: Azure Cosmos DB for NoSQL & vCore-based Azure Cosmos DB for MongoDB
description: Learn how to connect to Azure Cosmos DB for NoSQL or Azure Cosmos DB for MongoDB Instance by using Visual Studio Code. 
author: khelanmodi
ms.author: khelanmodi
ms.reviewer: gahllevy, sasinnat, esarroyo
ms.date: 10/17/2024
ms.service: azure-cosmos-db
ms.topic: how-to
keywords: connect to cosmos db for nosql or cosmos db for mongodb database
zone_pivot_groups: azure-cosmos-db-apis-nosql-mongodb
---

# Quickstart: Use Visual Studio Code to connect and query Azure Cosmos DB instances

[!INCLUDE[NoSQL, MongoDB](includes/appliesto-nosql-mongodb.md)]

[Visual Studio Code](https://code.visualstudio.com/docs) is a versatile code editor for Linux, macOS, and Windows, supporting numerous extensions. This quickstart shows you how to connect to Azure Cosmos DB for NoSQL and Azure Cosmos DB for MongoDB Instance and then use Visual Studio Code to perform core database operations, including querying, inserting, updating, and deleting data.

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
**Note**: It is recommended to use Microsoft Entra ID when accessing your Azure Cosmos DB resources (instead of account keys) for the most secure authentication method.
3. Once you are signed in, in the Azure tree view, find your Azure Subscription and drill down to Azure Cosmos DB. 
4. Select an existing account or right-click to create a new resource.


## Create a database and collection

The following steps will create a database named **SourceDatabase** and a collection named **People**:

1. In the tree view for your account, right-click select **Create Database**.

    :::image type="content" source="media/quickstart-azure-cosmos-db-mongodb/create-database-menu-option.png" lightbox="media/quickstart-azure-cosmos-db-mongodb/create-database-menu-option.png" alt-text="Screenshot of the create database option in the Mongo DB context menu.":::

1. In the **Database** and **Collection** popup dialogs, use the details in this table.

    | Prompt | Value |
    | --- | --- |
    | **Database name** | *SourceDatabase* |
    | **Collection name** | *People* |

1. After the operation completes, the new database should appear in the list of databases.

    > [!TIP]
    > If the database does not appear in the list, select **Refresh**.

1. Expand the **SourceDatabase** and **People** nodes in the **SERVERS** sidebar.

    :::image type="content" source="media/quickstart-azure-cosmos-db-mongodb/servers-sidebar-tree.png" lightbox="media/quickstart-azure-cosmos-db-mongodb/servers-sidebar-tree.png" alt-text="Screenshot of database and collection hierarchy under the Mongo account note in the SERVERS sidebar.":::

## Create a sample collection

The following steps will populate the **People** collection with a sample data set:

1. Select **Databases** to navigate to the list of databases in your account.

    :::image type="content" source="media/quickstart-azure-cosmos-db-mongodb/navigate-databases.png" lightbox="media/quickstart-azure-cosmos-db-mongodb/navigate-databases.png" alt-text="Screenshot of option to navigate to databases view.":::

1. Select the **SourceDatabase** item in the list of databases.

    :::image type="content" source="media/quickstart-azure-cosmos-db-mongodb/database-list-item.png" lightbox="media/quickstart-azure-cosmos-db-mongodb/database-list-item.png" alt-text="Screenshot of database list item named Source Database within databases list.":::

1. In the header menu, select **Import Sample Data**. In the confirmation dialog, select **Yes**.

    :::image type="content" source="media/quickstart-azure-cosmos-db-mongodb/navigate-import.png" lightbox="media/quickstart-azure-cosmos-db-mongodb/navigate-import.png" alt-text="Screenshot of dialog option to perform an import.":::

1. Wait for the import operation to complete.

    > [!TIP]
    > The import operation may take a few minutes to finish.

::: zone-end

::: zone pivot="api-mongodb"

## Prerequisites

Before you begin, ensure you have the following:

- An Azure Cosmos DB account configured with a database in Azure Cosmos DB for MongoDB. Use one of these quickstarts to set up a database:
    - [Portal](./mongodb/vcore/quickstart-portal.md) 
    - [Azure CLI](./mongodb/vcore/quickstart-bicep.md)

- To connect and manage data in Azure Cosmos DB, you’ll need to install the **Azure Databases** extension for Visual Studio Code.
1. Open Visual Studio Code.
2. Access the **Extensions** pane by selecting **View > Extensions** or using the shortcut **Ctrl + Shift + X**.
3. In the search bar, type [Azure Databases extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb) and select the extension. Then, click **Install**.
4. After installation, reload Visual Studio Code if prompted.

- MongoDB shell (mongosh) installed for command-line interactions (optional but recommended).

---

## Connecting to a MongoDB workload

## [Connecting to a vCore-based Azure Cosmos DB for MongoDB Cluster](#tab/CBDMongovCore)

### Explore Your Resources

1. In the **Azure Databases** extension, expand the **Azure Resources** section.
2. Locate **Subscription** you have your MongoDB workload. Under the desired subscription you will notice **Azure Cosmos DB for MongoDB (vCore)** and expand it to view your clusters and databases.

### Select and Access Your Cluster

1. Choose your Azure Cosmos DB for MongoDB (vCore) cluster from the expanded list.

### Authenticate with Your Admin Password

1. When prompted, enter the admin password for your cluster.
2. Once authenticated, you’ll gain access to your cluster. 

    > [!NOTE]
    > Your password is only used for authentication and is not stored.


## [Connecting to an External MongoDB Cluster](#tab/MongoDB)

1. Select the **Attached Database accounts** in the **Workspace** panel.
1. Choose **MongoDB** from the list of database types, then enter your MongoDB connection string when prompted.

---

:::image type="content" source="./media/dev-tooling/VS-code/vCore-vs-code-screenshot.png" alt-text="Screenshot of VS-code extension of a CosmosDB for MongoDB (vCore) cluster" lightbox="./media/dev-tooling/VS-code/vCore-vs-code-screenshot.png":::

Azure Cosmos DB for MongoDB and any MongoDB clusters you add are now conveniently accessible in one unified interface!

## Features Supported

### Intuitive Data Management
Manage your databases effortlessly:
- **Create and Drop Databases/Collections**: No need to switch tools—create or delete databases and collections right in VS Code just by right-clicking on your account in the resource panel. 
- **Real-time Document Editing**: Add, view, edit, and delete documents instantly, with changes reflected in real-time.

    > [!TIP]
    > If the database does not appear in the list, select **Refresh**.

### Powerful Query Tools
Run and refine your queries with ease:
- **Execute Queries Directly**: Write and run MongoDB queries with helpful features like syntax highlighting and auto-completion.
- **Instant Results**: View query results immediately in a format that works best for you—Table, JSON, or Tree view.

### Flexible Data Views
Explore your data in multiple ways:
- **JSON View**: See the raw data structure.
- **Tree View**: Navigate nested data with ease.
- **Table View**: Quickly scan through data and drill down into details with just a double-click.

### Easy Import and Export
Move data in and out seamlessly:
- **Import from JSON**: Load your data quickly from JSON files.
- **Export Data**: Save entire collections or query results as JSON for backup or sharing.

### Mongo Shell Integration
Need the command line? You’re covered:
- **Launch `mongosh`**: Run advanced commands directly from VS Code.

    > [!NOTE]
    > We dont ship Mongo shell with the extension, you would have to install `mongosh` and sync it manually. 

### Cluster Management at Your Fingertips
Stay on top of your resources:
- **View Cluster Details**: Check your cluster’s tier, server version, and resource usage.
- **Manage Tags**: Organize your clusters with tags that sync with the Azure Portal.

## Next steps

> [!div class="nextstepaction"]
> [Migrate your MongoDB workload to Azure Cosmos DB](./mongodb/vcore/migration-options.md)

::: zone-end



