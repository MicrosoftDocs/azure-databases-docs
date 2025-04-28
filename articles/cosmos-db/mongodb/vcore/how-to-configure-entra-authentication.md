---
title: Configure Microsoft Entra authentication
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn how to manage authentication and set up Microsoft Entra ID users for authentication on Azure Cosmos DB for MongoDB vCore clusters.
author: seesharprun
ms.author: sidandrews
ms.reviewer: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 04/28/2025
ms.custom: devx-track-rust
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database developer, I want to build a Rust console application to quickly and securely connect to and query my database and collections.
---

# Configure Microsoft Entra authentication for an Azure Cosmos DB for MongoDB vCore cluster

[!INCLUDE[Notice - Entra Authentication preview](includes/notice-entra-authentication-preview.md)]

In this article, you learn how to configure Microsoft Entra authentication for an Azure Cosmos DB for MongoDB vCore. Microsoft Entra authentication enables secure and seamless access to your database by using your organization's existing identities. This guide goes through the steps to set up authentication, register users or service principals, and validate the configuration.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prereq-existing-cluster.md)]

[!INCLUDE[Prerequisite - Azure CLI](includes/prereq-azure-cli.md)]

- [Mongo Shell](https://mongodb.com/try/download/shell) command-line interface.

## Get signed-in identity metadata

First, get the unique identifier for your currently signed-in identity.

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

## Configure existing cluster for authentication
When you create an Azure Cosmos DB for MongoDB vCore cluster, the cluster is configured for native authentication by default. Use the Azure CLI to configure your existing cluster to support Microsoft Entra authentication. Then, configure the cluster to map a user to your signed-in identity.

> [!TIP]
> These same steps can be followed to configure Microsoft Entra authentication for a managed identity, workload identity, application identity, or service principal.

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
    az resource patch \
        --resource-group "<resource-group-name>" \
        --name "<azure-cosmos-db-mongodb-vcore-cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --properties @properties.json \
        --latest-include-preview
    ```

1. Validate that the configuration was successful by using `az resource show` again and observing the entire cluster's configuration which includes `properties.authConfig`.

    ```azurecli-interactive
    az resource show \
        --resource-group "<resource-group-name>" \
        --name "<azure-cosmos-db-mongodb-vcore-cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --latest-include-preview
    ```

    ```json
    {
      ...
      "properties": {
        ...
        "authConfig": {
          "allowedModes": [
            "MicrosoftEntraID",
            "NativeAuth"
          ]
        },
        ...
      },
      ...
    }
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

> [!NOTE]
> Microsoft Entra ID users added to the cluster are going to be in addition to native DocumentDB users defined on the same cluster. An Azure Cosmos DB for MongoDB vCore cluster is created with at least one built-in native DocumentDB user. You can add more native DocumentDB users after cluster provisioning is completed.

## Related content

- [Microsoft Entra authentication overview](entra-authentication.md)
- [Connect using a console application](how-to-build-dotnet-console-app.md)
