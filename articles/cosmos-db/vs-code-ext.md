---
title: Use Visual Studio Code to connect and query Azure Cosmos DB resources 
titleSuffix: Azure Cosmos DB for NoSQL & vCore-based Azure Cosmos DB for MongoDB
description: Learn how to connect to Azure Cosmos DB for NoSQL or Azure Cosmos DB for MongoDB Instance by using Visual Studio Code. 
author: khelanmodi
ms.author: khelanmodi
ms.reviewer: gahllevy, sasinnat, esarroyo
ms.date: 10/17/2024
ms.service: azure-cosmos-db
ms.topic: quickstart
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
  | | [Azure CLI](./nosql/quickstart-cli.md) | [Azure CLI](./mongodb/vcore/quickstart-cli.md) |

- To connect and manage data in Azure Cosmos DB, you’ll need to install the **Azure Databases** extension for Visual Studio Code.

1. Open Visual Studio Code.
2. Access the **Extensions** pane by selecting **View > Extensions** or using the shortcut **Ctrl + Shift + X**.
3. In the search bar, type **Azure Databases** and select the extension. Then, click **Install**.
4. After installation, reload Visual Studio Code if prompted.

## Connect to Azure Cosmos DB

### Connecting to an Azure Cosmos DB for NoSQL

1. In Visual Studio Code, go to the **Azure** pane (select the **Azure** icon in the Activity Bar).
2. Under **Azure: Databases**, click **Add Connection**.
3. Follow the prompts to enter your connection details:
   - **Account Name**: Enter the account name for your Azure Cosmos DB.
   - **Connection String**: For MongoDB, use the MongoDB connection string. For NoSQL, use the primary or secondary key with your connection endpoint.
   - **Database Name**: Specify the database you want to connect to. If left blank, the default database will be used.
4. Save the connection profile by naming it appropriately (e.g., "CosmosDB NoSQL Dev").

### Connection Options

- **Azure Cosmos DB for NoSQL**: Uses an endpoint URL and primary/secondary key for authentication.
- **Azure Cosmos DB for MongoDB**: Uses a MongoDB-compatible connection string (e.g., ).

If you encounter connection errors, refer to the [troubleshooting guide](./troubleshoot-connections.md) for common solutions.

## Querying and Managing Data

With the **Azure Databases** extension, you can perform essential database operations directly from Visual Studio Code.

1. **Open a Query Editor**: Right-click on your connected database and select **New Query**.
2. **Execute Queries**:
   - **NoSQL**: Use SQL-like syntax for querying JSON data.
   - **MongoDB**: Use MongoDB query operators to interact with collections.
3. **View and Modify Data**:
   - Query results are displayed in an interactive grid, where you can view, edit, or delete records as needed.
   - Use commands like **Insert**, **Update**, and **Delete** to manage data directly from the editor.

Supported query languages and operations may differ depending on whether you’re connected to a NoSQL or MongoDB instance. Refer to [Azure Cosmos DB SQL syntax](./nosql-sql-query-syntax.md) and [MongoDB query syntax](./mongodb-query-syntax.md) for details.

## Extension Features

### Key Features

The Azure Databases extension offers several key features for working with Azure Cosmos DB:

- **Integrated Connection Management**: Save and manage multiple workloads.
- **Query and Data Manipulation**: Execute queries, insert, update, or delete data 
- **Export Options**: 
- **Customizable Settings**: table, json, 

## Troubleshooting

## Supported Platforms

The Azure Databases extension and Visual Studio Code are supported on the following operating systems:

- **Windows**: 10, 11, Windows Server 2016+
- **macOS**: 10.15 (Catalina) and newer
- **Linux**: Ubuntu 18.04+, Debian 10+, Red Hat 8+

## Feedback

We value your feedback. If you encounter any issues or have suggestions, please contact us at 
