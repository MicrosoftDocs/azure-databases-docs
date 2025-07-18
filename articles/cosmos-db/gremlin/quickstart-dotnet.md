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

1. Import the `Gremlin.Net` package from NuGet.

    ```bash
    dotnet add package Gremlin.Net
    ```

1. Build the project.

    ```dotnetcli
    dotnet build
    ```

## Object model

| | Description |
| --- | --- |
| **`GremlinClient`** | Represents the client used to connect and interact with the Gremlin server |
| **`GraphTraversalSource`** | Used to construct and execute Gremlin traversals |

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

    ```csharp
    using Gremlin.Net.Driver;
    using Gremlin.Net.Structure.IO.GraphSON;
    using System;
    using System.Threading.Tasks;
    ```

1. Create string variables for the credentials collected earlier in this guide. Name the variables `hostname`, `port`, and `primaryKey`.

    ```csharp
    var hostname = "<endpoint>";
    var port = 443;
    var primaryKey = "<key>";
    ```

1. Create a Gremlin client using the credentials and configuration variables created in the previous steps.

    ```csharp
    var gremlinServer = new GremlinServer(
        hostname,
        port,
        enableSsl: true,
        username: "/dbs/cosmicworks/colls/products",
        password: primaryKey
    );
    var gremlinClient = new GremlinClient(gremlinServer, new GraphSON2Reader(), new GraphSON2Writer(), GremlinClient.GraphSON2MimeType);
    ```

### Upsert data

Next, upsert new data into the graph. Upserting ensures that the data is created or replaced appropriately depending on whether the same data already exists in the graph.

1. Add a vertex (upsert data) for a product:

    ```csharp
    await gremlinClient.SubmitAsync("g.addV('product').property('id', 'surfboard1').property('name', 'Kiama classic surfboard').property('category', 'surf').property('price', 699.99)");
    ```

1. Add another product vertex:

    ```csharp
    await gremlinClient.SubmitAsync("g.addV('product').property('id', 'surfboard2').property('name', 'Montau Turtle Surfboard').property('category', 'surf').property('price', 799.99)");
    ```

1. Create an edge between the two products:

    ```csharp
    await gremlinClient.SubmitAsync("g.V('surfboard2').addE('replaces').to(g.V('surfboard1'))");
    ```

### Read data

Then, read data that was previously upserted into the graph.

1. Read a vertex by ID:

    ```csharp
    var result = await gremlinClient.SubmitAsync<dynamic>("g.V('surfboard1')");
    foreach (var item in result)
        Console.WriteLine(item);
    ```

1. Read all vertices:

    ```csharp
    var allVertices = await gremlinClient.SubmitAsync<dynamic>("g.V()");
    foreach (var item in allVertices)
        Console.WriteLine(item);
    ```

### Query data

Finally, use a query to find all data that matches a specific traversal or filter in the graph.

1. Query for all products in the 'surf' category:

    ```csharp
    var surfProducts = await gremlinClient.SubmitAsync<dynamic>("g.V().hasLabel('product').has('category', 'surf')");
    foreach (var item in surfProducts)
        Console.WriteLine(item);
    ```

1. Query for all products that replace another product:

    ```csharp
    var replaces = await gremlinClient.SubmitAsync<dynamic>("g.V().hasLabel('product').outE('replaces').inV()");
    foreach (var item in replaces)
        Console.WriteLine(item);
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
