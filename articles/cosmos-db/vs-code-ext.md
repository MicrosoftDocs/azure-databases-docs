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
---

# Quickstart: Use Visual Studio Code to connect and query Azure Cosmos DB instances

[!INCLUDE[NoSQL, MongoDB](includes/appliesto-nosql-mongodb.md)]

[Visual Studio Code](https://code.visualstudio.com/docs) is a versatile code editor for Linux, macOS, and Windows, supporting numerous extensions. This quickstart shows you how to connect to Azure Cosmos DB for NoSQL and Azure Cosmos DB for MongoDB Instance and then use Visual Studio Code to perform core database operations, including querying, inserting, updating, and deleting data.

## Prerequisites

Before you begin, ensure you have the following:

- An Azure Cosmos DB account configured with a database in either Azure Cosmos DB for NoSQL or Azure Cosmos DB for MongoDB. Use one of these quickstarts to set up a database:

| Action | Azure Cosmos DB for NoSQL | vCore-based Azure Cosmos DB for MongoDB |
| :--- | :--- | :--- |
| Create Database | [Portal](./nosql/quickstart-portal.md) | [Portal](./mongodb/vcore/quickstart-portal.md) |
| | [Azure CLI](./nosql/quickstart-template-bicep.md) | [Azure CLI](./mongodb/vcore/quickstart-bicep.md) |

- To connect and manage data in Azure Cosmos DB, you’ll need to install the **Azure Databases** extension for Visual Studio Code.

1. Open Visual Studio Code.
2. Access the **Extensions** pane by selecting **View > Extensions** or using the shortcut **Ctrl + Shift + X**.
3. In the search bar, type **Azure Databases** and select the extension. Then, click **Install**.
4. After installation, reload Visual Studio Code if prompted.


### [Connecting to an Azure Cosmos DB for NoSQL](#tab/nosql)

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


### [Connecting to an Azure Cosmos DB for Mongo DB vCore](#tab/MongoDB)

1. **Install the Azure Databases Extension**  
   Begin by installing the [Azure Databases extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb) from the VS Code Marketplace to manage your databases directly from Visual Studio Code.

2. **Sign in to Your Azure Account**  
After signing in to your Azure account, select the subscription you wish to work with and go to the **Azure Cosmos DB for MongoDB (vCore)** section in the side panel. When connecting, you’ll be prompted to enter your password. Once authenticated, you’ll gain access to your cluster. 

*Note: Your password is only used for authentication and is not stored.*

3. **Manage Your Databases**  
   From this interface, you can view, query, and manage your Cosmos DB databases in VS Code. Perform essential tasks like:
   - **Editing documents**: Update document content in real-time.
   - **Running queries**: Execute and test queries using MongoDB syntax.
   - **Browsing collections**: Navigate through collections and inspect documents easily.

#### Connecting to External MongoDB Clusters

1. **Install the Azure Databases Extension**  
   If not already installed, download the Azure Databases extension from the VS Code Marketplace to enable MongoDB connections.

2. **Add Your MongoDB Cluster**  
   - Select the **Azure Databases** icon in the **Resource** panel.
   - Choose **MongoDB** from the list of database types, then enter your MongoDB connection string when prompted.

Azure Cosmos DB for MongoDB and any MongoDB clusters you add are now conveniently accessible in one unified interface!

---

## Querying and Managing Data



## Extension Features

### Key Features

The Azure Databases extension offers several key features for working with Azure Cosmos DB:

- **Integrated Connection Management**: Save and manage multiple workloads.
- **Query and Data Manipulation**: Execute queries, insert, update, or delete data 
- **Export Options**: 
- **Customizable Settings**: table, json, 

## Feedback

We value your feedback. If you encounter any issues or have suggestions, please contact us at 
