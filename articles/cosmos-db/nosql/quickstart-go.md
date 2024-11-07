---
title: Quickstart - Go client library
titleSuffix: Azure Cosmos DB for NoSQL
description: Deploy a Go web application that uses the Azure SDK for Go to interact with Azure Cosmos DB for NoSQL data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: golang
ms.topic: quickstart-sdk
ms.date: 11/07/2024
ms.custom: devx-track-go, devx-track-extended-azdevcli
zone_pivot_groups: azure-cosmos-db-quickstart-env
appliesto:
  - ✅ NoSQL
# CustomerIntent: As a developer, I want to learn the basics of the Go library so that I can build applications with Azure Cosmos DB for NoSQL.
---

# Quickstart: Azure Cosmos DB for NoSQL library for Go

[!INCLUDE[Developer Quickstart selector](includes/quickstart/dev-selector.md)]

Get started with the Azure Cosmos DB for NoSQL client library for Go to query data in your containers and perform common operations on individual items. Follow these steps to deploy a minimal solution to your environment using the Azure Developer CLI.

[API reference documentation](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos) | [Library source code](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/data/azcosmos#readme) | [Package (Go)](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

[!INCLUDE[Developer Quickstart prerequisites](includes/quickstart/dev-prereqs.md)]

## Setting up

Deploy this project's development container to your environment. Then, use the Azure Developer CLI (`azd`) to create an Azure Cosmos DB for NoSQL account and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

::: zone pivot="devcontainer-codespace"

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://codespaces.new/azure-samples/cosmos-db-nosql-go-quickstart?template=false&quickstart=1&azure-portal=true)

::: zone-end

::: zone pivot="devcontainer-vscode"

[![Open in Dev Container](https://img.shields.io/static/v1?style=for-the-badge&label=Dev+Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/azure-samples/cosmos-db-nosql-go-quickstart)

::: zone-end

[!INCLUDE[Developer Quickstart setup](includes/quickstart/dev-setup.md)]

### Install the client library

The client library is available through Go, as the `azcosmos` package.

1. Open a terminal and navigate to the `/src` folder.

    ```bash
    cd ./src
    ```

1. If not already installed, install the `azcosmos` package using `go install`.

    ```bash
    go install github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos
    ```

1. Also, install the `azidentity` package if not already installed.

    ```bash
    go install github.com/Azure/azure-sdk-for-go/sdk/azidentity
    ```

1. Open and review the **src/go.mod** file to validate that the `github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos` and `github.com/Azure/azure-sdk-for-go/sdk/azidentity` entries both exist.

## Object model

| Name | Description |
| --- | --- |
| [`CosmosClient`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos#CosmosClient) | This class is the primary client class and is used to manage account-wide metadata or databases. |
| [`CosmosDatabase`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos#CosmosDatabase) | This class represents a database within the account. |
| [`CosmosContainer`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos#CosmosContainer) | This class is primarily used to perform read, update, and delete operations on either the container or the items stored within the container. |
| [`PartitionKey`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos#PartitionKey) | This class represents a logical partition key. This class is required for many common operations and queries. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a database](#get-a-database)
- [Get a container](#get-a-container)
- [Create an item](#create-an-item)
- [Get an item](#read-an-item)
- [Query items](#query-items)

[!INCLUDE[Developer Quickstart sample explanation](includes/quickstart/dev-sample-primer.md)]

### Authenticate the client

[!INCLUDE[Developer Quickstart authentication explanation](includes/quickstart/dev-auth-primer.md)]

This sample creates a new instance of `CosmosClient` using `azcosmos.NewClient` and authenticates using a `DefaultAzureCredential` instance.

```go
credential, err := azidentity.NewDefaultAzureCredential(nil)
if err != nil {
    return err
}

clientOptions := azcosmos.ClientOptions{
    EnableContentResponseOnWrite: true,
}

client, err := azcosmos.NewClient("<azure-cosmos-db-nosql-account-endpoint>", credential, &clientOptions)
if err != nil {
    return err
}
```

### Get a database

Use `client.NewDatabase` to retrieve the existing database named *`cosmicworks`*.

```go
database, err := client.NewDatabase("cosmicworks")
if err != nil {
    return err
}
```

### Get a container

Retrieve the existing *`products`* container using `database.NewContainer`.

```go
container, err := database.NewContainer("products")
if err != nil {
    return err
}
```

### Create an item

Build a Go type with all of the members you want to serialize into JSON. In this example, the type has a unique identifier, and fields for category, name, quantity, price, and sale.

```go
type Item struct {
  Id        string  `json:"id"`
  Category  string  `json:"category"`
  Name      string  `json:"name"`
  Quantity  int     `json:"quantity"`
  Price     float32 `json:"price"`
  Clearance bool    `json:"clearance"`
}
```

Create an item in the container using `container.UpsertItem`. This method "upserts" the item effectively replacing the item if it already exists.

```go
item := Item {
    Id:        "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
    Category:  "gear-surf-surfboards",
    Name:      "Yamba Surfboard",
    Quantity:  12,
    Price:     850.00,
    Clearance: false,
}

partitionKey := azcosmos.NewPartitionKeyString("gear-surf-surfboards")

context := context.TODO()

bytes, err := json.Marshal(item)
if err != nil {
    return err
}

response, err := container.UpsertItem(context, partitionKey, bytes, nil)
if err != nil {
    return err
}
```

### Read an item

Perform a point read operation by using both the unique identifier (`id`) and partition key fields. Use `container.ReadItem` to efficiently retrieve the specific item.

```go
partitionKey := azcosmos.NewPartitionKeyString("gear-surf-surfboards")

context := context.TODO()

itemId := "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"

response, err := container.ReadItem(context, partitionKey, itemId, nil)
if err != nil {
    return err
}

if response.RawResponse.StatusCode == 200 {
    read_item := Item{}
    err := json.Unmarshal(response.Value, &read_item)
    if err != nil {
        return err
    }
}
```

### Query items

Perform a query over multiple items in a container using `container.NewQueryItemsPager`. Find all items within a specified category using this parameterized query:

```nosql
SELECT * FROM products p WHERE p.category = @category
```

```go
partitionKey := azcosmos.NewPartitionKeyString("gear-surf-surfboards")

query := "SELECT * FROM products p WHERE p.category = @category"

queryOptions := azcosmos.QueryOptions{
    QueryParameters: []azcosmos.QueryParameter{
        {Name: "@category", Value: "gear-surf-surfboards"},
    },
}

pager := container.NewQueryItemsPager(query, partitionKey, &queryOptions)
```

Parse the paginated results of the query by looping through each page of results using `pager.NextPage`. Use `pager.More` to determine if there are any results left at the start of each loop.

```go
items := []Item{}

for pager.More() {
    response, err := pager.NextPage(context.TODO())
    if err != nil {
        return err
    }

    for _, bytes := range response.Items {
        item := Item{}
        err := json.Unmarshal(bytes, &item)
        if err != nil {
            return err
        }
        items = append(items, item)
    }
}
```

## Clean up resources

[!INCLUDE[Developer Quickstart cleanup](includes/quickstart/dev-cleanup.md)]

## Related content

- [.NET Quickstart](quickstart-dotnet.md)
- [Node.js Quickstart](quickstart-nodejs.md)
- [Java Quickstart](quickstart-java.md)
- [Python Quickstart](quickstart-python.md)
