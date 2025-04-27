---
title: Build a Go console app
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Connect to an Azure Cosmos DB for MongoDB (vCore) cluster by using a Go console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 04/28/2025
ms.custom: devx-track-go
ai-usage: ai-generated
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database owner, I want to use Mongo Shell to connect to and query my database and collections.
---

# Build a Go console app with Azure Cosmos DB for MongoDB vCore

[!INCLUDE[Developer console app selector](includes/build-console-app-dev-selector.md)]

In this guide, you build a console application to connect to an existing Azure Cosmos DB for MongoDB vCore cluster. This guide covers the required steps to configure the cluster for Microsoft Entra authentication and then to connect to the same cluster using the identity that you're currently signed-in with.

This guide uses the open-source `go.mongodb.org/mongo-driver/v2/mongo` package from Go.

After authenticating, you can use this library to interact with Azure Cosmos DB for MongoDB vCore using the same methods and classes you would typically use to interact with any other MongoDB or DocumentDB instance.

## Prerequisites

- An existing Azure Cosmos DB for MongoDB (vCore) cluster.
- The latest version of the [Azure CLI](/cli/azure) in [Azure Cloud Shell](/azure/cloud-shell).
  - If you prefer to run CLI reference commands locally, sign in to the Azure CLI by using the [`az login`](/cli/azure/reference-index#az-login) command.
- Latest version of [Go](https://go.dev/).

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
    go get -u github.com/Azure/azure-sdk-for-go/sdk/azidentity
    ```

1. TODO

    ```bash
    go get -u  go.mongodb.org/mongo-driver/v2/mongo
    ```

1. TODO

    ```bash

    ```
    
1. TODO

    ```bash
    
    ```
    
1. TODO
    
    ```bash
    
    ```

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

1. TODO

    ```go
    import (
    	"context"
    	"crypto/tls"
    	"encoding/json"
    	"fmt"
    	"time"
    
    	"github.com/Azure/azure-sdk-for-go/sdk/azcore/policy"
    	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    
    	"go.mongodb.org/mongo-driver/v2/bson"
    	"go.mongodb.org/mongo-driver/v2/mongo"
    	"go.mongodb.org/mongo-driver/v2/mongo/options"
    )
    ```

1. TODO

    ```go
	ctx := context.Background()
    ```

1. TODO

    ```go
	credential, err := azidentity.NewDefaultAzureCredential(nil)
	if err != nil {
		panic(err)
	}
    ```

1. TODO

    ```go
	azureIdentityTokenCallback := func(_ context.Context,
		_ *options.OIDCArgs) (*options.OIDCCredential, error) {
		accessToken, err := credential.GetToken(ctx, policy.TokenRequestOptions{
			Scopes: []string{"https://ossrdbms-aad.database.windows.net/.default"},
		})
		if err != nil {
			return nil, err
		}
		return &options.OIDCCredential{
			AccessToken: accessToken.Token,
		}, nil
	}
    ```

1. TODO

    ```go
	clusterName := "<azure-cosmos-db-mongodb-vcore-cluster-name>"
	uri := fmt.Sprintf("mongodb+srv://%s.global.mongocluster.cosmos.azure.com/", clusterName)
    ```

1. TODO

    ```go
	auth := options.Credential{
		AuthMechanism:       "MONGODB-OIDC",
		OIDCMachineCallback: azureIdentityTokenCallback,
	}
    ```

1. TODO

    ```go
	clientOptions := options.Client().
		ApplyURI(uri).
		SetConnectTimeout(2 * time.Minute).
		SetRetryWrites(true).
		SetTLSConfig(&tls.Config{}).
		SetAuth(auth)
    ```

1. TODO

    ```go
	client, err := mongo.Connect(clientOptions)
	if err != nil {
		panic(err)
	}

	fmt.Println("Client created")
    ```

1. TODO

    ```go
	defer func() {
		if err = client.Disconnect(ctx); err != nil {
			panic(err)
		}
	}()
    ```

## Perform common operations

Finally, use the official library to perform common tasks with databases, collections, and documents. Here, you use the same classes and methods you would use to interact with MongoDB or DocumentDB to manage your collections and items.

1. TODO

    ```go
	database := client.Database("cosmicworks")

	fmt.Println("Database pointer created")
    ```

1. TODO

    ```go
	collection := database.Collection("products")

	fmt.Println("Collection pointer created")
    ```

1. TODO

    ```go
	opts := options.Replace().SetUpsert(true)
	upsertFilter := bson.D{{Key: "_id", Value: "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"}}
	priceDecimal, err := bson.ParseDecimal128("850.00")
	if err != nil {
		panic(err)
	}
	document := Product{
		ID:        "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
		Category:  "gear-surf-surfboards",
		Name:      "Yamba Surfboard",
		Quantity:  12,
		Price:     priceDecimal,
		Clearance: false}

	result, err := collection.ReplaceOne(ctx, upsertFilter, document, opts)
	if err != nil {
		panic(err)
	}

	fmt.Printf("Documents upserted count:\t%d\n", result.UpsertedCount)
    ```

1. TODO

    ```go
	readFilter := bson.D{{Key: "_id", Value: "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"}, {Key: "category", Value: "gear-surf-surfboards"}}
	var target Product
	err = collection.FindOne(ctx, readFilter).Decode(&target)
	if err != nil {
		panic(err)
	}

	fmt.Printf("Read document name:\t%s\n", target.Name)
    ```

1. TODO

    ```go
	queryFilter := bson.D{{Key: "category", Value: "gear-surf-surfboards"}}
	cursor, err := collection.Find(ctx, queryFilter)
	if err != nil {
		panic(err)
	}
    ```

1. TODO

    ```go
	var products []Product
	if err = cursor.All(ctx, &products); err != nil {
		panic(err)
	}
    ```

1. TODO

    ```go
	for _, product := range products {
		json, err := json.Marshal(product)
		if err != nil {
			panic(err)
		}
		fmt.Printf("Found document:\t%s\n", string(json))
	}
    ```

## Related content

- [Microsoft Entra authentication overview](entra-authentication.md)
- [TODO](about:blank)
