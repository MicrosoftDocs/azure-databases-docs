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
ms.date: 07/22/2025
ai-usage: ai-generated
---

# Quickstart: Azure Cosmos DB for Apache Gremlin client library for .NET

[!INCLUDE[Quickstart developer selector](includes/selector-quickstart-developer.md)]

[!INCLUDE[Note - Recommended services](includes/note-recommended-services.md)]

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
- [Insert data](#insert-data)
- [Read data](#read-data)
- [Query data](#query-data)

### Authenticate client

Start by authenticating the client using the credentials gathered earlier in this guide.

1. Open the *Program.cs* file in your integrated development environment (IDE).

1. Delete any existing content within the file.

1. Add using directives for the following namespaces:

    - `Gremlin.Net.Driver`
    - `Gremlin.Net.Structure.IO.GraphSON`

    ```csharp
    using Gremlin.Net.Driver;
    using Gremlin.Net.Structure.IO.GraphSON;
    ```

1. Create string variables for the credentials collected earlier in this guide. Name the variables `hostname` and `primaryKey`.

    ```csharp
    string hostname = "<host>";
    string primaryKey = "<key>";
    ```

1. Create a `GremlinServer` using the credentials and configuration variables created in the previous steps. Name the variable `server`.

    ```csharp
    GremlinServer server = new(
        $"{hostname}.gremlin.cosmos.azure.com",
        443,
        enableSsl: true,
        username: "/dbs/cosmicworks/colls/products",
        password: primaryKey
    );
    ```

1. Now, create a `GremlinClient` using the `server` variable and the `GraphSON2MessageSerializer` configuration.

    ```csharp
    GremlinClient client = new(
        server,
        new GraphSON2MessageSerializer()
    );
    ```

### Insert data

Next, insert new vertex and edge data into the graph. Before creating the new data, clear the graph of any existing data.

1. Run the `g.V().drop()` query to clear all vertices and edges from the graph.

    ```csharp
    await client.SubmitAsync("g.V().drop()");
    ```

1. Create a Gremlin query that adds a vertex.

    ```csharp
    string insertVertexQuery = """
        g.addV('product')
            .property('id', prop_id)
            .property('name', prop_name)
            .property('category', prop_category)
            .property('quantity', prop_quantity)
            .property('price', prop_price)
            .property('clearance', prop_clearance)
    """;
    ```

1. Add a vertex for a single product.

    ```csharp
    await client.SubmitAsync(insertVertexQuery, new Dictionary<string, object>
    {
        ["prop_id"] = "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        ["prop_name"] = "Yamba Surfboard",
        ["prop_category"] = "gear-surf-surfboards",
        ["prop_quantity"] = 12,
        ["prop_price"] = 850.00,
        ["prop_clearance"] = false
    });
    ```

1. Add two more vertices for two extra products.

    ```csharp
    await client.SubmitAsync(insertVertexQuery, new Dictionary<string, object>
    {
        ["prop_id"] = "bbbbbbbb-1111-2222-3333-cccccccccccc",
        ["prop_name"] = "Montau Turtle Surfboard",
        ["prop_category"] = "gear-surf-surfboards",
        ["prop_quantity"] = 5,
        ["prop_price"] = 600.00,
        ["prop_clearance"] = true
    });

    await client.SubmitAsync(insertVertexQuery, new Dictionary<string, object>
    {
        ["prop_id"] = "cccccccc-2222-3333-4444-dddddddddddd",
        ["prop_name"] = "Noosa Surfboard",
        ["prop_category"] = "gear-surf-surfboards",
        ["prop_quantity"] = 31,
        ["prop_price"] = 1100.00,
        ["prop_clearance"] = false
    });
    ```

1. Create another Gremlin query that adds an edge.

    ```csharp
    string insertEdgeQuery = """
        g.V([prop_partition_key, prop_source_id])
            .addE('replaces')
            .to(g.V([prop_partition_key, prop_target_id]))
    """;
    ```

1. Add two edges.

    ```csharp
    await client.SubmitAsync(insertEdgeQuery, new Dictionary<string, object>
    {
        ["prop_partition_key"] = "gear-surf-surfboards",
        ["prop_source_id"] = "bbbbbbbb-1111-2222-3333-cccccccccccc",
        ["prop_target_id"] = "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"
    });

    await client.SubmitAsync(insertEdgeQuery, new Dictionary<string, object>
    {
        ["prop_partition_key"] = "gear-surf-surfboards",
        ["prop_source_id"] = "bbbbbbbb-1111-2222-3333-cccccccccccc",
        ["prop_target_id"] = "cccccccc-2222-3333-4444-dddddddddddd"
    });
    ```

### Read data

Then, read data that was previously inserted into the graph.

1. Create a query that reads a vertex using the unique identifier and partition key value.

    ```csharp
    string readVertexQuery = "g.V([prop_partition_key, prop_id])";
    ```

1. Then, read a vertex by supplying the required parameters.

    ```csharp
    ResultSet<Dictionary<string, object>> readResults = await client.SubmitAsync<Dictionary<string, object>>(readVertexQuery, new Dictionary<string, object>
    {
        ["prop_partition_key"] = "gear-surf-surfboards",
        ["prop_id"] = "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"
    });

    Dictionary<string, object> matchedItem = readResults.Single();
    ```

### Query data

Finally, use a query to find all data that matches a specific traversal or filter in the graph.

1. Create a query that finds all vertices that traverse out from a specific vertex.

    ```csharp
    string findVerticesQuery = """
        g.V().hasLabel('product')
            .has('category', prop_partition_key)
            .has('name', prop_name)
            .outE('replaces').inV()
    """;
    ```

1. Execute the query specifying the `Montau Turtle Surfboard` product.

    ```csharp
    ResultSet<Dictionary<string, object>> findResults = await client.SubmitAsync<Dictionary<string, object>>(findVerticesQuery, new Dictionary<string, object>
    {
        ["prop_partition_key"] = "gear-surf-surfboards",
        ["prop_name"] = "Montau Turtle Surfboard"
    });
    ```

1. Iterate over the query results.

    ```csharp
    foreach (Dictionary<string, object> result in findResults)
    {
        // Do something here with each result
    }
    ```

## Run the code

Run the newly created application using a terminal in your application directory.

```bash
dotnet run
```

## Clean up resources

[!INCLUDE[Section - Quickstart cleanup](includes/section-quickstart-cleanup.md)]
