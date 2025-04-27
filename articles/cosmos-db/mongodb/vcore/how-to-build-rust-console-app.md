---
title: Build a Rust console app
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Connect to an Azure Cosmos DB for MongoDB (vCore) cluster by using a Rust console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 04/28/2025
ms.custom: devx-track-rust
ai-usage: ai-generated
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database owner, I want to use Mongo Shell to connect to and query my database and collections.
---

# Build a Rust console app with Azure Cosmos DB for MongoDB vCore

[!INCLUDE[Developer console app selector](includes/build-console-app-dev-selector.md)]

[!INCLUDE[Console app introduction](includes/console-app-introduction.md)]

This guide uses the open-souce `mongodb` crate from Rust.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prereq-existing-cluster.md)]

[!INCLUDE[Prerequisite - Azure CLI](includes/prereq-azure-cli.md)]

- Latest version of [Python](https://www.python.org).

## Grant your identity access

[!INCLUDE[Console app identity access](includes/console-app-identity-access.md)]

## Configure your console application

Next, create a new console application project and import the necessary libraries to authenticate to your cluster.

1. TODO

    ```bash
    cargo add azure_core
    ```

1. TODO

    ```bash
    cargo add azure_identity
    ```

1. TODO

    ```bash
    cargo add mongodb
    ```

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

1. TODO

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

1. TODO

    ```rust
    #[tokio::main]
    async fn main() -> Result<(), Box<dyn std::error::Error>> {
        let credential = DefaultAzureCredential::new()?;
    
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
    
        let cluster_name = "<azure-cosmos-db-mongodb-vcore-cluster-name>";
    
        let uri = format!(
            "mongodb+srv://{}.global.mongocluster.cosmos.azure.com/",
            cluster_name
        );
    
        let mut client_options = ClientOptions::parse(uri).await?;
    
        client_options.connect_timeout = Some(std::time::Duration::from_secs(120));
        client_options.tls = Some(mongodb::options::Tls::Enabled(Default::default()));
        client_options.retry_writes = Some(true);
    
        client_options.credential = Some(azure_identity_token_credential);
    
        let client = Client::with_options(client_options)?;
    
        println!("Client created");

        Ok(())
    }
    ```

## Perform common operations

Finally, use the official library to perform common tasks with databases, collections, and documents. Here, you use the same classes and methods you would use to interact with MongoDB or DocumentDB to manage your collections and items.

1. TODO

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

1. TODO

    ```rust
    let database = client.database("<database-name>");

    println!("Database pointer created");
    ```

1. TODO

    ```rust
    let collection = database.collection::<Product>("<collection-name>");

    println!("Collection pointer created");
    ```

1. TODO

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

1. TODO

    ```rust
    let document = collection
        .find_one(doc! { "_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb" })
        .await?;

    println!("Read document _id:\t{:#?}", document.unwrap()._id);
    ```

1. TODO

    ```rust
    let filter = doc! { "category": "gear-surf-surfboards" };

    let mut cursor = collection.find(filter).await?;

    while let Some(document) = cursor.try_next().await? {
        println!("Found document:\t{:#?}", document);
    }
    ```

## Related content

- [Microsoft Entra authentication overview](entra-authentication.md)
- [TODO](about:blank)
