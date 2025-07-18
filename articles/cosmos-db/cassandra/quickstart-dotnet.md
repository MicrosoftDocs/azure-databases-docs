---
title: 'Quickstart: .NET & C# library'
titleSuffix: Azure Cosmos DB for Apache Cassandra
description: Create a new Azure Cosmos DB for Apache Cassandra account and connect using the .NET library and C# in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: apache-cassandra
ms.topic: quickstart-sdk
ms.devlang: csharp
ms.custom: devx-track-csharp, devx-track-dotnet, sfi-ropc-nochange
ms.date: 07/18/2025
---

# Quickstart: Azure Cosmos DB for Apache Cassandra client library for .NET

[!INCLUDE[Quickstart developer selector](includes/selector-quickstart-developer.md)]

Get started with the Azure Cosmos DB for Apache Cassandra client library for .NET to store, manage, and query unstructured data. Follow the steps in this guide to create a new account, install a .NET client library, connect to the account, perform common operations, and query your final sample data.

[API reference documentation](https://docs.datastax.com/en/developer/csharp-driver/index.html) | [Library source code](https://github.com/datastax/csharp-driver) | [Package (NuGet)](https://www.nuget.org/packages/CassandraCSharpDriver)

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

1. Start in an empty directory.

1. Create a new .NET console application

    ```bash
    dotnet new console
    ```

1. Add the `CassandraCSharpDriver` package from NuGet.

    ```bash
    dotnet add package CassandraCSharpDriver
    ```

1. Build the project.

    ```bash
    dotnet build
    ```

## Object model

| | Description |
| --- | --- |
| **`Cluster`** | Represents the connection state to a cluster |
| **`ISession`** | Thread-safe entities that hold a specific connection to a cluster |
| **`Mapper`** | Cassandra Query Language (CQL) client used to run queries |

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

    - `System.Security.Authentication`
    - `Cassandra`
    - `Cassandra.Mapping`

    ```csharp
    using System.Security.Authentication;
    using Cassandra;
    using Cassandra.Mapping;
    ```

1. Create string constant variables for the credentials collected earlier in this guide. Name the variables `username`, `password`, and `contactPoint`.

    ```csharp
    const string username = "<username>";
    const string password = "<password>";
    const string contactPoint = "<contact-point>";
    ```

1. Create a new `SSLoptions` object to ensure that you're using the transport layer security (TLS) 1.2 protocol, checking for certificate revocation, and not performing any extra client-side certification validation.

    ```csharp
    SSLOptions sslOptions = new(
        sslProtocol: SslProtocols.Tls12,
        checkCertificateRevocation: true,
        remoteCertValidationCallback: (_, _, _, _) => true);
    ```

1. Construct a new `Cluster` object using the fluent `Cluster.Builder()` syntax. Use the credential and configuration variables created in the previous steps.

    ```csharp
    Cluster cluster = Cluster.Builder()
        .WithCredentials(username, password)
        .WithPort(10350)
        .AddContactPoint(contactPoint)
        .WithSSL(sslOptions)
        .Build();
    ```

1. Create a new `session` variable using the `ConnectAsync` method passing in the name of the target keyspace (`cosmicworks`).

    ```csharp
    using ISession session = await cluster.ConnectAsync("cosmicworks");
    ```

1. Create a new `mapper` variable by using the `Mapper` class constructor passing in the recently created `session` variable.

    ```csharp
    Mapper mapper = new(session);
    ```

[!INCLUDE[Section - Transport Layer Security disabled warning](../includes/section-transport-layer-security-disabled-warning.md)]

### Upsert data

Next, upsert new data into a table. Upserting ensures that the data is created or replaced appropriately depending on whether the same data already exists in the table.

1. Define a new record type named `Product` with fields corresponding to the table created earlier in this guide.

    | | Type |
    | --- | --- |
    | **`Id`** | `string` |
    | **`Name`** | `string` |
    | **`Category`** | `string` |
    | **`Quantity`** | `int` |
    | **`Price`** | `decimal` |
    | **`Clearance`** | `bool` |

    ```csharp
    record Product
    {
        public required string Id { get; init; }
    
        public required string Name { get; init; }
    
        public required string Category { get; init; }
    
        public required int Quantity { get; init; }
    
        public required decimal Price { get; init; }
    
        public required bool Clearance { get; init; }
    }
    ```

    > [!TIP]
    > In .NET, you can create this type in another file or create it at the end of the existing file.

1. Create a new object of type `Product`. Store the object in a variable named `product`.

    ```csharp
    Product product = new()
    {
        Id = "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        Name = "Yamba Surfboard",
        Category = "gear-surf-surfboards",
        Quantity = 12,
        Price = 850.00m,
        Clearance = false
    };
    ```

1. Asynchronously invoke the `InsertAsync` method passing in the `product` variable created in the previous step.

    ```csharp
    await mapper.InsertAsync(product);
    ```

### Read data

Then, read data that was previously upserted into the table.

1. Create a new string variable named `readQuery` with a CQL query that matches items with the same `id` field.

    ```csharp
    string readQuery = "SELECT * FROM product WHERE id = ? LIMIT 1";
    ```

1. Create a string variable named `id` with the same value as the product created earlier in this guide.

    ```csharp
    string id = "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb";
    ```

1. Use the `SingleAsync<>` generic method to run the query stored in `readQuery`, pass in the `id` variable as an argument, and map the output to the `Product` type. Store the result of this operation in a variable of type `Product`.

    ```csharp
    Product matchedProduct = await mapper.SingleAsync<Product>(readQuery, [id]);
    ```

### Query data

Finally, use a query to find all data that matches a specific filter in the table.

1. Create string variables named `findQuery` and `category` with the CQL query and required parameter.

    ```csharp
    string findQuery = "SELECT * FROM product WHERE category = ? ALLOW FILTERING";
    string category = "gear-surf-surfboards";
    ```

1. Use the two string variables and the `FetchAsync<>` generic method to asynchronously query multiple results. Store the result of this query in a variable of type `IEnumerable<Product>` named `queriedProducts`.

    ```csharp
    IEnumerable<Product> queriedProducts = await mapper.FetchAsync<Product>(findQuery, [category]);
    ```

1. Use a `foreach` loop to iterate over the query results.

    ```csharp
    foreach (Product queriedProduct in queriedProducts)
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

## Next step

> [!div class="nextstepaction"]
> [Overview of Azure Cosmos DB for Apache Cassandra](introduction.md)
