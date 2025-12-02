---
title: Build a Rust console app
description: Connect to an Azure DocumentDB cluster by using a Rust console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.reviewer: nlarin
ms.topic: how-to
ms.date: 07/21/2025
ms.custom:
  - devx-track-rust
  - build-2025
ai-usage: ai-assisted
# Customer Intent: As a database developer, I want to build a Rust console application to quickly and securely connect to and query my database and collections.
---

# Build a Rust console app with Azure DocumentDB

[!INCLUDE[Developer console app selector](includes/selector-build-console-app-dev.md)]

In this guide, you create a Rust console application to connect to an Azure DocumentDB cluster. The guide covers setting up your development environment, using the `azure_identity` crate from the Azure SDK for Rust to authenticate, and managing documents within the database.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

[!INCLUDE[External - Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

- Microsoft Entra authentication configured for the cluster with your identity granted `root` role.

    - To enable Microsoft Entra authentication, [review the configuration guide](how-to-connect-role-based-access-control.md).

- Latest version of [Python](https://www.python.org).

## Configure your console application

Next, create a new console application project and import the necessary libraries to authenticate to your cluster.

1. Create a new Rust project using `cargo new`.

    ```bash
    cargo new mongodb-app
    cd mongodb-app
    ```

1. Add the `azure_core` crate to your dependencies.

    ```bash
    cargo add azure_core
    ```

1. Add the `azure_identity` crate for authentication.

    ```bash
    cargo add azure_identity
    ```
    
1. Add the `mongodb` driver crate to interact with your cluster.

    ```bash
    cargo add mongodb
    ```
    
1. For async operations, also add the supporting `tokio`, `futures`, and `serde` crates.
   
    ```bash
    cargo add tokio --features full
    cargo add futures
    cargo add serde --features derive
    ```

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

1. Open your **main.rs** file and import the necessary crates and modules.

    ```rust
    use azure_core::credentials::TokenCredential;
    use azure_identity::DefaultAzureCredential;
    use futures::{FutureExt, TryStreamExt};
    use mongodb::{
        Client,
        bson::doc,
        options::{
            AuthMechanism, ClientOptions, Credential,
            oidc::{self, IdpServerResponse},
        },
    };
    use serde::{Deserialize, Serialize};
    ```

1. Create the main async function with the necessary error handling.

    ```rust
    #[tokio::main]
    async fn main() -> Result<(), Box<dyn std::error::Error>> {

        Ok(())
    }
    ```

1. Create a new instance of struct `azure_identity::DefaultAzureCredential`.

    ```rust
    let credential = DefaultAzureCredential::new()?;
    ```

1. Create a credential callback to handle token requests from the MongoDB client.

    ```rust
    let azure_identity_token_credential = Credential::builder()
        .mechanism(AuthMechanism::MongoDbOidc)
        .oidc_callback(oidc::Callback::machine(move |_| {
            let azure_credential = credential.clone();
            async move {
                let access_token = azure_credential
                    .get_token(&["https://ossrdbms-aad.database.windows.net/.default"])
                    .await
                    .map_err(|e| {
                        mongodb::error::Error::custom(format!("Azure token error: {}", e))
                    })?;
                Ok(IdpServerResponse::builder()
                    .access_token(access_token.token.secret().to_owned())
                    .build())
            }
            .boxed()
        }))
        .build()
        .into();
    ```

1. Define a uniform resource indicator (URI) from your cluster using its name, scheme, and the global endpoint.

    ```rust
    let cluster_name = "<azure-documentdb-cluster-name>";

    let uri = format!(
        "mongodb+srv://{}.global.mongocluster.cosmos.azure.com/",
        cluster_name
    );
    ```

1. Construct a `mongodb::ClientOptions` instance using best practices configuration, your URI, and the credential callback.

    ```rust
    let mut client_options = ClientOptions::parse(uri).await?;

    client_options.connect_timeout = Some(std::time::Duration::from_secs(120));
    client_options.tls = Some(mongodb::options::Tls::Enabled(Default::default()));
    client_options.retry_writes = Some(true);

    client_options.credential = Some(azure_identity_token_credential);
    ```

1. Create a new instance of `mongodb::Client` using the constructed settings.

    ```rust
    let client = Client::with_options(client_options)?;

    println!("Client created");
    ```

## Perform common operations

Finally, use the official library to perform common tasks with databases, collections, and documents. Here, you use the same classes and methods you would use to interact with MongoDB or DocumentDB to manage your collections and items.

1. Create a Rust struct to represent your `Product` documents with `serde` serialization support.

    ```rust
    #[derive(Serialize, Deserialize, Debug)]
    struct Product {
        _id: String,
        category: String,
        name: String,
        quantity: i32,
        price: f64,
        clearance: bool,
    }
    ```

1. Get a reference to your database by name.

    ```rust
    let database = client.database("<database-name>");

    println!("Database pointer created");
    ```

1. Get a reference to your collection.

    ```rust
    let collection = database.collection::<Product>("<collection-name>");

    println!("Collection pointer created");
    ```

1. Create a document using `collection.update_one` and **upsert** it into the collection.

    ```rust
    let document = Product {
        _id: "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb".to_string(),
        category: "gear-surf-surfboards".to_string(),
        name: "Yamba Surfboard".to_string(),
        quantity: 12,
        price: 850.00,
        clearance: false,
    };

    let response = collection
        .update_one(
            doc! { "_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb" },
            doc! { "$set": mongodb::bson::to_document(&document)? },
        )
        .upsert(true)
        .await?;

    println!("Documents upserted count:\t{}", response.modified_count);
    ```

1. Read a specific document from the collection using `collection.find_one` and a filter.

    ```rust
    let document = collection
        .find_one(doc! { "_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb" })
        .await?;

    println!("Read document _id:\t{:#?}", document.unwrap()._id);
    ```

1. Query for multiple documents matching a filter using `collection.find`.

    ```rust
    let filter = doc! { "category": "gear-surf-surfboards" };

    let mut cursor = collection.find(filter).await?;

    while let Some(document) = cursor.try_next().await? {
        println!("Found document:\t{:#?}", document);
    }
    ```

## Related content

- [Microsoft Entra authentication overview](how-to-connect-role-based-access-control.md)
- [Microsoft Entra configuration for cluster](how-to-connect-role-based-access-control.md)
