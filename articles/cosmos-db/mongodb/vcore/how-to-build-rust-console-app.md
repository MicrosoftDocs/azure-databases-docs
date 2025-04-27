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
ai-usage: ai-assisted
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database owner, I want to use Mongo Shell to connect to and query my database and collections.
---

# Build a Rust console app with Azure Cosmos DB for MongoDB vCore

[!INCLUDE[Developer console app selector](includes/build-console-app-dev-selector.md)]

In this guide, you build a Rust console application to connect to an existing Azure Cosmos DB for MongoDB vCore cluster. This guide covers the required steps to configure the cluster for Microsoft Entra authentication and then to connect to the same cluster using the identity that you're currently signed-in with.

This guide uses the open-souce `mongodb` crate from Rust.

After authenticating, you can use this library to interact with Azure Cosmos DB for MongoDB vCore using the same methods and classes you would typically use to interact with any other MongoDB or DocumentDB instance.

## Prerequisites

- An existing Azure Cosmos DB for MongoDB (vCore) cluster.
- The latest version of the [Azure CLI](/cli/azure) in [Azure Cloud Shell](/azure/cloud-shell).
  - If you prefer to run CLI reference commands locally, sign in to the Azure CLI by using the [`az login`](/cli/azure/reference-index#az-login) command.
- Latest version of [Python](https://www.python.org).

## Grant your identity access

First, get the unique identifier for your currently signed-in identity. Then, use the Azure CLI to configure your existing cluster to support Microsoft Entra authentication directly with your identity.

1. Get the details for the currently logged-in account using `az ad signed-in-user`.

    ```azurecli-interactive
    az ad signed-in-user show
    ```

1. The command outputs a JSON response containing various fields.

    ```json
    {
      "@odata.context": "<https://graph.microsoft.com/v1.0/$metadata#users/$entity>",
      "businessPhones": [],
      "displayName": "Kai Carter",
      "givenName": "Kai",
      "id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
      "jobTitle": "Senior Sales Representative",
      "mail": "<kai@adventure-works.com>",
      "mobilePhone": null,
      "officeLocation": "Redmond",
      "preferredLanguage": null,
      "surname": "Carter",
      "userPrincipalName": "<kai@adventure-works.com>"
    }
    ```

1. Record the value of the `id` property. This property is the unique identifier for your principal and is sometimes referred to as the **principal ID**. You use this value in the next series of steps.

1. Now, get the `authConfig` property from your existing cluster using `az resource show`.

    ```azurecli-interactive
    az resource show \
        --resource-group "<resource-group-name>" \
        --name "<azure-cosmos-db-mongodb-vcore-cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --query "properties.authConfig" \
        --latest-include-preview
    ```

1. Observe the output. If Microsoft Entra authentication isn't configured, the output includes only the `NativeAuth` value in the `allowedModes` array.

    ```json
    {
      "allowedModes": [
        "NativeAuth"
      ]
    }
    ```

1. Create a new JSON file named *properties.json*. In the file, define the new value for the `authConfig` property.

    ```json
    {
      "authConfig": {
        "allowedModes": [
          "MicrosoftEntraID",
          "NativeAuth"
        ]
      }
    }
    ```

1. Then, update the existing cluster with an HTTP `PATCH` operation by adding the `MicrosoftEntraID` value to `allowedModes`.

    ```azurecli-interactive
    az resource patch
        --resource-group "<resource-group-name>" \
        --name "<azure-cosmos-db-mongodb-vcore-cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --properties @properties.json \
        --latest-include-preview
    ```

1. Validate that the configuration was successful by using `az resource show` again and observing the `properties.authConfig` property.

    ```azurecli-interactive
    az resource show \
        --resource-group "<resource-group-name>" \
        --name "<azure-cosmos-db-mongodb-vcore-cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --latest-include-preview
    ```

1. Now, create a new JSON file named *user.json*. In this file, define a user to register for Microsoft Entra authentication.

    ```json
    {
      "identityProvider": {
        "type": "MicrosoftEntraID",
        "properties": {
          "principalType": "User"
        }
      },
      "roles": [
        {
          "db": "admin",
          "role": "dbOwner"
        }
      ]
    }
    ```

    > [!TIP]
    > If you're registering a service principal, like a managed identity, you would replace the `identityProvider.properties.principalType` property's value with `ServicePrincipal`.

1. Use `az resource create` to create a new resource of type `Microsoft.DocumentDB/mongoClusters/users`. Compose the name of the resource by concatenating the **name of the parent cluster** and the **principal ID** of your identity.

    ```azurecli-interactive
    az resource create \
        --resource-group "<resource-group-name>" \
        --name "<azure-cosmos-db-mongodb-vcore-cluster-name>/users/<principal-id>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters/users" \
        --properties @user.json \
        --latest-include-preview
    ```

    > [!NOTE]
    > For example, if your parent resource is named `example-cluster` and your principal ID was `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb`, the name of the resource would be:
    >
    > ```json
    > "example-cluster/users/aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"
    > ```
    >

1. Get the details for the currently logged-in Azure subscription using `az account show`.

    ```azurecli-interactive
    az account show
    ```

1. The command outputs a JSON response containing various fields.

    ```json
    {
      "environmentName": "AzureCloud",
      "homeTenantId": "eeeeffff-4444-aaaa-5555-bbbb6666cccc",
      "id": "dddd3d3d-ee4e-ff5f-aa6a-bbbbbb7b7b7b",
      "isDefault": true,
      "managedByTenants": [],
      "name": "example-azure-subscription",
      "state": "Enabled",
      "tenantId": "eeeeffff-4444-aaaa-5555-bbbb6666cccc",
      "user": {
        "cloudShellID": true,
        "name": "kai@adventure-works.com",
        "type": "user"
      }
    }
    ```

1. Record the value of the `tenantId` property. This property is the unique identifier for your Microsoft Entra tenant and is sometimes referred to as the **tenant ID**. You use this value in steps within a subsequent section.

> [!TIP]
> These same steps can be followed to configure Microsoft Entra authentication for a managed identity, workload identity, application identity, or service principal.

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
