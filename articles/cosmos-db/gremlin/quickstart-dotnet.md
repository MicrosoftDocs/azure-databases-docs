---
title: 'Quickstart: .NET library'
titleSuffix: Azure Cosmos DB for Apache Gremlin
description: Create a new Azure Cosmos DB for Apache Gremlin account and connect using the .NET library and C# in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: apache-gremlin
ms.topic: quickstart-sdk
ms.devlang: csharp
ms.custom: devx-track-csharp, devx-track-dotnet, sfi-ropc-nochange
ms.date: 07/21/2025
ai-usage: ai-generated
---

# Quickstart: Azure Cosmos DB for Apache Gremlin client library for .NET

[!INCLUDE[Quickstart developer selector](includes/selector-quickstart-developer.md)]

Get started with the Azure Cosmos DB for Apache Gremlin client library for .NET to store, manage, and query unstructured data. Follow the steps in this guide to create a new account, install a .NET client library, connect to the account, perform common operations, and query your final sample data.

[Library source code](https://github.com/apache/tinkerpop/tree/master/gremlin-dotnet) | [Package (NuGet)](https://www.nuget.org/packages/Gremlin.Net)

## Prerequisites

[!INCLUDE[Prerequisites - Quickstart developer](../includes/prerequisites-quickstart-developer.md)]

- .NET SDK 9.0 or later

## Setting up

First, set up the account and development environment for this guide. This section walks you through the process of creating an account, getting its credentials, and then preparing your development environment.

### Create an account

[!INCLUDE[Section - Setting up](includes/section-quickstart-provision.md)]

### Get credentials

[!INCLUDE[Section - Get credentials](includes/section-quickstart-credentials.md)]

### Prepare development environment

Then, configure your development environment with a new project and the client library. This step is the last required prerequisite before moving on to the rest of this guide.

1. Start in an empty folder.

1. Create a new .NET console application

    ```dotnetcli
    dotnet new console
    ```

1. Import the `` package from NuGet.

    ```bash
     
    ```

1. Build the project.

    ```dotnetcli
    dotnet build
    ```

## Object model

| | Description |
| --- | --- |
| **``** | |
| **``** | |

## Code examples

- [Authenticate client](#authenticate-client)
- [Upsert data](#upsert-data)
- [Read data](#read-data)
- [Query data](#query-data)

### Authenticate client

Start by authenticating the client using the credentials gathered earlier in this guide.

1. Open the *Program.cs* file in your integrated development environment (IDE).

1. Delete any existing content within the file.

1. Add using directives for the following namespaces:

    - ``

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

### Upsert data

Next, upsert new data into the graph. Upserting ensures that the data is created or replaced appropriately depending on whether the same data already exists in the graph.

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

### Read data

Then, read data that was previously upserted into the graph.

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

### Query data

Finally, use a query to find all data that matches a specific traversal or filter in the graph.

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

1. TODO

    ```csharp
    
    ```

## Run the code

Run the newly created application using a terminal in your application directory.

```bash
dotnet run
```

## Clean up resources

[!INCLUDE[Section - Quickstart cleanup](includes/section-quickstart-cleanup.md)]

## Next step

> [!div class="nextstepaction"]
> [Overview of Azure Cosmos DB for Apache Gremlin](introduction.md)
