---
title: 'Quickstart: Go library'
titleSuffix: Azure Cosmos DB for Apache Cassandra
description: Create a new Azure Cosmos DB for Apache Cassandra account and connect using the Go library in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: apache-cassandra
ms.topic: quickstart-sdk
ms.devlang: golang
ms.custom: devx-track-go, sfi-ropc-nochange
ms.date: 07/21/2025
appliesto:
  - ✅ Apache Cassanda
---

# Quickstart: Azure Cosmos DB for Apache Cassandra client library for Go

[!INCLUDE[Quickstart developer selector](includes/selector-quickstart-developer.md)]

Get started with the Azure Cosmos DB for Apache Cassandra client library for Go to store, manage, and query unstructured data. Follow the steps in this guide to create a new account, install a Go client library, connect to the account, perform common operations, and query your final sample data.

[API reference documentation](https://pkg.go.dev/github.com/apache/cassandra-gocql-driver/v2#pkg-overview) | [Library source code](https://github.com/apache/cassandra-gocql-driver) | [Package (Go)](https://pkg.go.dev/github.com/apache/cassandra-gocql-driver/v2)

## Prerequisites

[!INCLUDE[Prerequisites - Quickstart developer](../includes/prerequisites-quickstart-developer.md)]

- `Go` 1.24 or newer

## Setting up

First, set up the account and development environment for this guide. This section walks you through the process of creating an account, getting its credentials, and then preparing your development environment.

### Create an account

[!INCLUDE[Section - Setting up](includes/section-quickstart-provision.md)]

### Get credentials

[!INCLUDE[Section - Get credentials](includes/section-quickstart-credentials.md)]

### Prepare development environment

Then, configure your development environment with a new project and the client library. This step is the last required prerequisite before moving on to the rest of this guide.

1. Start in an empty directory.

1. Create a new Go module.

    ```bash
    go mod init quickstart
    ```

1. Import the `github.com/apache/cassandra-gocql-driver/v2` package from Go.

    ```bash
    go get github.com/apache/cassandra-gocql-driver/v2
    ```

1. Create the *main.go* file.

1. Add the Go application boilerplate.

    ```go
    package main
    
    func main() {    
    }
    ```

    > [!IMPORTANT]
    > The remaining steps within this guide assume that you're adding your code within the `main` function.

## Object model

| | Description |
| --- | --- |
| **`Cluster`** | Represents a specific connection to a cluster |
| **`Session`** | Entities that hold a specific connection to a cluster |

## Code examples

- [Authenticate client](#authenticate-client)
- [Upsert data](#upsert-data)
- [Read data](#read-data)
- [Query data](#query-data)

### Authenticate client

Start by authenticating the client using the credentials gathered earlier in this guide.

1. Open the *main.go* file in your integrated development environment (IDE).

1. Within the `main` function, import the following packages along with the `github.com/apache/cassandra-gocql-driver/v2` package:

    - `context`
    - `crypto/tls`

    ```go
    import (
        "context"
        "crypto/tls"
        "github.com/apache/cassandra-gocql-driver/v2"
    )
    ```

1. Create string variables for the credentials collected earlier in this guide. Name the variables `username`, `password`, and `contactPoint`.

    ```go
    username := "<username>"
    password := "<password>"
    contactPoint := "<contact-point>"
    ```

1. Configure an instance of the `PasswordAuthenticator` type with the credentials specified in the previous steps. Store the result in a variable named `authentication`.

    ```go
    authentication := gocql.PasswordAuthenticator{
        Username: username,
        Password: password,
    }
    ```

1. Configure an instance of `SslOptions` with a minimum version of Transport Layer Security (TLS) 1.2 and the `contactPoint` variable as the target server name. Store the result in a variable named `sslOptions`.

    ```go
    sslOptions := &gocql.SslOptions{
        Config: &tls.Config{
            MinVersion: tls.VersionTLS12,
            ServerName: contactPoint,
        },
    }
    ```

1. Create a new cluster specification using `NewCluster` and the `contactPoint` variable.

    ```go
    cluster := gocql.NewCluster(contactPoint)
    ```

1. Configure the cluster specification object by using the credential and configuration variables created in the previous steps. 

    ```go
    cluster.SslOpts = sslOptions
    cluster.Authenticator = authentication
    ```

1. Configure the remainder of the cluster specification object with these static values.

    ```go
    cluster.Keyspace = "cosmicworks"
    cluster.Port = 10350
    cluster.ProtoVersion = 4    
    ```

1. Create a new session that connects to the cluster using `CreateSession`.

    ```go
    session, _ := cluster.CreateSession()
    ```

1. Configure the session to invoke the `Close` function after the `main` function returns.

    ```go
    defer session.Close()
    ```

1. Create a new `Background` context object and store it in the `ctx` variable.

    ```go
    ctx := context.Background()
    ```

[!INCLUDE[Section - Transport Layer Security disabled warning](../includes/section-transport-layer-security-disabled-warning.md)]

### Upsert data

Next, upsert new data into a table. Upserting ensures that the data is created or replaced appropriately depending on whether the same data already exists in the table.

1. Define a new type named `Product` with fields corresponding to the table created earlier in this guide.

    ```go
    type Product struct {
        id        string
        name      string
        category  string
        quantity  int
        clearance bool
    }
    ```

    > [!TIP]
    > In Go, you can create this type in another file or create it at the end of the existing file.

1. Create a new object of type `Product`. Store the object in a variable named `product`.

    ```go
    product := Product {
        id:        "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        name:      "Yamba Surfboard",
        category:  "gear-surf-surfboards",
        quantity:  12,
        clearance: false,
    }
    ```

1. Create a new string variable named `insertQuery` with the Cassandra Query Language (CQL) query for inserting a new row.

    ```go
    insertQuery := `
        INSERT INTO
            product (id, name, category, quantity, clearance)
        VALUES
            (?, ?, ?, ?, ?)
    `
    ```

1. Use the `Query` and `ExecContext` functions to run the query. Pass in various properties of the `product` variable as query parameters.

    ```go
    _ = session.Query(
        insertQuery,
        product.id, 
        product.name, 
        product.category, 
        product.quantity, 
        product.clearance,
    ).ExecContext(ctx)
    ```

### Read data

Then, read data that was previously upserted into the table.

1. Create a new string variable named `readQuery` with a CQL query that matches items with the same `id` field.

    ```go
    readQuery := `
        SELECT
            id,
            name,
            category,
            quantity,
            clearance
        FROM
            product
        WHERE id = ?
        LIMIT 1
    `
    ```

1. Create a string variable named `id` with the same value as the product created earlier in this guide.

    ```go
    id := "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb" 
    ```

1. Create another variable named `matchedProduct` to store the result of this operation in.

    ```go
    var matchedProduct Product
    ```

1. Use the `Query`, `Consistency`, `IterContext`, and `Scan` functions together to find the single item that matches the query and assign its properties to the `matchedProduct` variable.

    ```go
    session.Query(
        readQuery,
        &id,
    ).Consistency(gocql.One).IterContext(ctx).Scan(
        &matchedProduct.id,
        &matchedProduct.name,
        &matchedProduct.category,
        &matchedProduct.quantity,
        &matchedProduct.clearance,
    )
    ```

### Query data

Finally, use a query to find all data that matches a specific filter in the table.

1. Create string variables named `findQuery` and `category` with the CQL query and required parameter.

    ```go
    findQuery := `
        SELECT
            id,
            name,
            category,
            quantity,
            clearance
        FROM
            product
        WHERE
            category = ?
        ALLOW FILTERING
    `
    
    category := "gear-surf-surfboards"
    ```

1. Use the `Query`, `Consistency`, `IterContext`, and `Scanner` functions together to create a scanner that can iterate over multiple items that matches the query.

    ```go
    queriedProducts := session.Query(
        findQuery, 
        &category,
    ).Consistency(gocql.All).IterContext(ctx).Scanner()
    ```

1. Use the `Next` and `Scan` functions to iterate over the query results and assign the properties of each result to the inner `queriedProduct` variable.

    ```go
    for queriedProducts.Next() {
        var queriedProduct Product
        queriedProducts.Scan(
            &queriedProduct.id,
            &queriedProduct.name,
            &queriedProduct.category,
            &queriedProduct.quantity,
            &queriedProduct.clearance,
        )
        // Do something here with each result
    }
    ```

## Run the code

Run the newly created application using a terminal in your application directory.

```bash
go run .
```

## Clean up resources

[!INCLUDE[Section - Quickstart cleanup](includes/section-quickstart-credentials.md)]

## Next step

> [!div class="nextstepaction"]
> [Overview of Azure Cosmos DB for Apache Cassandra](introduction.md)
