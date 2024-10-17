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

[Visual Studio Code](https://code.visualstudio.com/docs) is a graphical code editor for Linux, macOS, and Windows. It supports extensions, including the [Azure Database]() for querying NoSQL and MongoDB instances on Azure Cosmos DB. In this quickstart, you use Visual Studio Code to connect to Azure Cosmos DB Instance and then run commands to query, insert, update, and delete data.

## Prerequisites

- A database in Azure Cosmos DB for NoSQL or Azure Cosmos DB for MongoDB Instance. You can use one of these quickstarts to create and then configure a database in Azure SQL Database:

  | Action | Azure Cosmos DB for NoSQL | Azure Cosmos DB for MongoDB |
  | :--- | :--- | :--- |
  | Create | [Portal]() | [Portal](./mongodb/vcore/quickstart-portal.md) |
  | | [CLI]() | [CLI]() |


## Install Visual Studio Code

Make sure you have installed the latest [Visual Studio Code](https://code.visualstudio.com/Download). 

## Configure Visual Studio Code

To configure Visual Studio Code for connecting to Azure Cosmos DB, you need to install the necessary extensions and dependencies based on your operating system. Follow the steps below for your specific OS to get started.

### abc

1. Open Visual Studio Code.
1. Open the Extensions pane (or **Ctrl + Shift + X**).
1. Search for `Azure Databases` and then install the **Azure Databases** extension.

For additional installation guidance, see [mssql for Visual Studio Code]().