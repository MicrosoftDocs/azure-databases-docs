---
title: Quickstart - Azure SDK for Rust
titleSuffix: Azure Cosmos DB for NoSQL
description: Deploy a Rust web application that uses the Azure SDK for Rust to interact with Azure Cosmos DB for NoSQL data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: rust
ms.topic: quickstart-sdk
ms.date: 07/03/2025
ms.custom: devx-track-rust
appliesto:
  - ✅ NoSQL
# CustomerIntent: As a developer, I want to learn the basics of the Rust library so that I can build applications with Azure Cosmos DB for NoSQL.
---

# Quickstart: Use Azure Cosmos DB for NoSQL with Azure SDK for Rust

[!INCLUDE[Developer Quickstart selector](includes/quickstart/dev-selector.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for NoSQL application using the Azure SDK for Rust. Azure Cosmos DB for NoSQL is a schemaless data store allowing applications to store unstructured data in the cloud. Query data in your containers and perform common operations on individual items using the Azure SDK for Rust.

> [!IMPORTANT]
> The Rust SDK for Azure Cosmos DB is currently in public preview. This preview is provided without a service-level agreement, and we don't recommend it for production workloads. Certain features aren't supported or have limited support with constrained capabilities.
>
> For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>

[API reference documentation](https://docs.rs/azure_data_cosmos/latest/azure_data_cosmos/index.html) | [Library source code](https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/cosmos/azure_data_cosmos#readme) | [Crate (Rust)](https://docs.rs/azure_data_cosmos) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

- Docker Desktop
- Rust 1.80 or later

If you don't have an Azure account, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

### Install the client library

The client library is available through Rust, as the `azure_data_cosmos` crate.

1. If not already installed, install the `azure_data_cosmos` create using `cargo install`.

    ```bash
    cargo add azure_data_cosmos
    ```

1. Also, install the `azure_identity` crate if not already installed.

    ```bash
    cargo add azure_identity
    ```

### Import libraries

Import the `DefaultAzureCredential`, `CosmosClient`, `PartitionKey`, and `Query` types into your application code.

```rust
use azure_data_cosmos::{CosmosClient, PartitionKey, Query};
use azure_identity::DefaultAzureCredential;
```

## Object model

| Name | Description |
| --- | --- |
| [`CosmosClient`](https://docs.rs/azure_data_cosmos/latest/azure_data_cosmos/clients/struct.CosmosClient.html) | This type is the primary client and is used to manage account-wide metadata or databases. |
| [`DatabaseClient`](https://docs.rs/azure_data_cosmos/latest/azure_data_cosmos/clients/struct.DatabaseClient.html) | This type represents a database within the account. |
| [`ContainerClient`](https://docs.rs/azure_data_cosmos/latest/azure_data_cosmos/clients/struct.ContainerClient.html) | This type is primarily used to perform read, update, and delete operations on either the container or the items stored within the container. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a database](#get-a-database)
- [Get a container](#get-a-container)
- [Create an item](#create-an-item)
- [Get an item](#read-an-item)
- [Query items](#query-items)

The sample code in the template uses a database named `cosmicworks` and container named `products`. The `products` container contains details such as name, category, quantity, a unique identifier, and a sale flag for each product. The container uses the `/category` property as a logical partition key.

### Authenticate the client

This sample creates a new instance of `CosmosClient` using `CosmosClient::new` and authenticates using a `DefaultAzureCredential` instance.

```rust
let credential = DefaultAzureCredential::new()?;

let client = CosmosClient::new(&endpoint, credential, None)?;
```

### Get a database

Use `client.database` to retrieve the existing database named *`cosmicworks`*.

```rust
let database = client.database_client("cosmicworks");
```

### Get a container

Retrieve the existing *`products`* container using `database.container`.

```rust
let container = database.container_client("products");
```

### Create an item

Build a new type with all of the members you want to serialize into JSON. In this example, the type has a unique identifier, and fields for category, name, quantity, price, and sale. Derive the `serde::Serialize` trait on this type, so that it can be serialized to JSON.

```rust
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct Item {
    pub id: String,
    pub category: String,
    pub name: String,
    pub quantity: i32,
    pub price: f64,
    pub clearance: bool,
}
```

Create an item in the container using `container.upsert_item`. This method "upserts" the item effectively replacing the item if it already exists.

```rust
let item = Item {
    id: "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb".to_string(),
    category: "gear-surf-surfboards".to_string(),
    name: "Yamba Surfboard".to_string(),
    quantity: 12,
    price: 850.00,
    clearance: false,
};

let partition_key = PartitionKey::from(item.category.clone());
        
let partition_key = PartitionKey::from(item.category.clone());

container.upsert_item(partition_key, item.clone(), None).await?;
```

### Read an item

Perform a point read operation by using both the unique identifier (`id`) and partition key fields. Use `container.ReadItem` to efficiently retrieve the specific item.

```rust
let item_id = "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb";
let item_partition_key = "gear-surf-surfboards";

let response = container.read_item(item_partition_key, item_id, None).await?;

let item: Item = response.into_json_body().await?;
```

### Query items

Perform a query over multiple items in a container using `container.NewQueryItemsPager`. Find all items within a specified category using this parameterized query:

```nosql
SELECT * FROM products p WHERE p.category = @category
```

```rust
let item_partition_key = "gear-surf-surfboards";

let query = Query::from("SELECT * FROM c WHERE c.category = @category")
    .with_parameter("@category", item_partition_key)?;

let mut pager = container.query_items::<Item>(query, item_partition_key, None)?;

while let Some(page_response) = pager.next().await {

    let page = page_response?.into_body().await?;

    for item in page.items {
        // Do something
    }

}
```

### Explore your data

Use the Visual Studio Code extension for Azure Cosmos DB to explore your NoSQL data. You can perform core database operations including, but not limited to:

- Performing queries using a scrapbook or the query editor
- Modifying, updating, creating, and deleting items
- Importing bulk data from other sources
- Managing databases and containers

For more information, see [How-to use Visual Studio Code extension to explore Azure Cosmos DB for NoSQL data](../visual-studio-code-extension.md?pivots=api-nosql).

## Related content

- [.NET Quickstart](quickstart-dotnet.md)
- [Node.js Quickstart](quickstart-nodejs.md)
- [Java Quickstart](quickstart-java.md)
- [Python Quickstart](quickstart-python.md)
- [Go Quickstart](quickstart-go.md)

## Next step

> [!div class="nextstepaction"]
> [Azure SDK for Rust samples for Azure Cosmos DB for NoSQL](https://github.com/azure-samples/azure-cosmos-rust-nosql-api-samples)
