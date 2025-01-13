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
ms.date: 01/13/2024
ms.custom: devx-track-rust, devx-track-extended-azdevcli
appliesto:
  - ✅ NoSQL
# CustomerIntent: As a developer, I want to learn the basics of the Rust library so that I can build applications with Azure Cosmos DB for NoSQL.
---

# Quickstart: Use Azure Cosmos DB for NoSQL with Azure SDK for Rust

[!INCLUDE[Developer Quickstart selector](includes/quickstart/dev-selector.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for Table application using the Azure SDK for Rust. Azure Cosmos DB for Table is a schemaless data store allowing applications to store structured table data in the cloud. You learn how to create tables, rows, and perform basic tasks within your Azure Cosmos DB resource using the Azure SDK for Rust.

> [!IMPORTANT]
> The Rust SDK for Azure Cosmos DB is currently in public preview. This preview is provided without a service-level agreement, and we don't recommend it for production workloads. Certain features might not be supported or might have constrained capabilities.
>
> For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>

[API reference documentation](https://docs.rs/azure_data_cosmos/latest/azure_data_cosmos/index.html) | [Library source code](https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/cosmos/azure_data_cosmos#readme) | [Crate (Rust)](https://docs.rs/azure_data_cosmos) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

- Azure Developer CLI
- Docker Desktop
- Rust 1.80 or later

If you don't have an Azure account, create a [free account](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.

## Initialize the project

Use the Azure Developer CLI (`azd`) to create an Azure Cosmos DB for Table account and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

1. Open a terminal in an empty directory.

1. If you're not already authenticated, authenticate to the Azure Developer CLI using `azd auth login`. Follow the steps specified by the tool to authenticate to the CLI using your preferred Azure credentials.

    ```azurecli
    azd auth login
    ```

1. Use `azd init` to initialize the project.

    ```azurecli
    azd init --template cosmos-db-nosql-rust-quickstart
    ```

1. During initialization, configure a unique environment name.

1. Deploy the Azure Cosmos DB account using `azd up`. The Bicep templates also deploy a sample web application.

    ```azurecli
    azd up
    ```

1. During the provisioning process, select your subscription, desired location, and target resource group. Wait for the provisioning process to complete. The process can take **approximately five minutes**.

1. Once the provisioning of your Azure resources is done, a URL to the running web application is included in the output.

    ```output
    Deploying services (azd deploy)
    
      (✓) Done: Deploying service web
    - Endpoint: <https://[container-app-sub-domain].azurecontainerapps.io>
    
    SUCCESS: Your application was provisioned and deployed to Azure in 5 minutes 0 seconds.
    ```

1. Use the URL in the console to navigate to your web application in the browser. Observe the output of the running app.

:::image type="content" source="media/quickstart-rust/running-application.png" alt-text="Screenshot of the running web application.":::

### Install the client library

The client library is available through Rust, as the `azure_data_cosmos` crate.

1. Open a terminal and navigate to the `/src` folder.

    ```bash
    cd ./src
    ```

1. If not already installed, install the `azure_data_cosmos` create using ``.

    ```bash
    cargo install azure_data_cosmos
    ```

1. Also, install the `azure_identity` crate if not already installed.

    ```bash
    cargo install azure_identity
    ```

1. Open and review the **src/Cargo.toml** file to validate that the `azure_data_cosmos` and `azure_identity` entries both exist.

## Object model

| Name | Description |
| --- | --- |
| [`CosmosClient`](https://docs.rs/azure_data_cosmos/latest/azure_data_cosmos/clients/struct.CosmosClient.html) | This type is the primary client and is used to manage account-wide metadata or databases. |
| [`DatabaseClient`](https://docs.rs/azure_data_cosmos/latest/azure_data_cosmos/clients/struct.DatabaseClient.html) | This type represents a database within the account. |
| [`CollectionClient`](https://docs.rs/azure_data_cosmos/latest/azure_data_cosmos/clients/struct.CollectionClient.html) | This type is primarily used to perform read, update, and delete operations on either the container or the items stored within the container. |

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
let credential = DefaultAzureCredential::new().unwrap();

let client = match CosmosClient::new(&endpoint, credential, None) {
    Ok(client) => client,
    Err(e) => {
        eprintln!("Error creating CosmosClient: {}", e);
        return;
    }
};
```

### Get a database

Use `client.database` to retrieve the existing database named *`cosmicworks`*.

```rust
let database = client.database("database");
```

### Get a container

Retrieve the existing *`products`* container using `database.container`.

```rust
let container = database.container("products");
```

### Create an item

Build a new type with all of the members you want to serialize into JSON. In this example, the type has a unique identifier, and fields for category, name, quantity, price, and sale.

```rust
struct Item {
    id: String,
    category: String,
    name: String,
    quantity: i32,
    price: f64,
    clearance: bool,
}
```

Create an item in the container using `container.UpsertItem`. This method "upserts" the item effectively replacing the item if it already exists.

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

let _ = container.upsert_item(partition_key, item, None).await;
```

### Read an item

Perform a point read operation by using both the unique identifier (`id`) and partition key fields. Use `container.ReadItem` to efficiently retrieve the specific item.

```rust
let item_id = "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb";
let item_partition_key = "gear-surf-surfboards";

match read_response {
    Ok(r) => {
        let deserialize_response = r.deserialize_body().await;
        match deserialize_response {
            Ok(i) => {
                let read_item = i.unwrap();
                // Do something
            },
            Err(e) => {
                eprintln!("Error deserializing response: {}", e);
            },
        }
    },
    Err(e) => {
        eprintln!("Error reading item: {}", e);
    },
}
```

### Query items

Perform a query over multiple items in a container using `container.NewQueryItemsPager`. Find all items within a specified category using this parameterized query:

```nosql
SELECT * FROM products p WHERE p.category = @category
```

```rust
let item_partition_key = "gear-surf-surfboards";

let partition_key = PartitionKey::from(item_partition_key);

let query = format!("SELECT * FROM c WHERE c.category = '{}'", item_partition_key);

let pager = container.query_items::<Item>(query, partition_key, None)?;
while let Some(page_response) = pager.next.await {
    let page = page_response?.into_body().await?
    for item in page.items {
        // Do something
    }
}

## Clean up resources

When you no longer need the sample application or resources, remove the corresponding deployment and all resources.

```azurecli
azd down
```

## Related content

- [.NET Quickstart](quickstart-dotnet.md)
- [Node.js Quickstart](quickstart-nodejs.md)
- [Java Quickstart](quickstart-java.md)
- [Python Quickstart](quickstart-python.md)
- [Go Quickstart](quickstart-go.md)

## Next step

> [!div class="nextstepaction"]
> [Azure SDK for Rust samples for Azure Cosmos DB for NoSQL](https://github.com/azure-samples/azure-cosmos-rust-nosql-api-samples)
