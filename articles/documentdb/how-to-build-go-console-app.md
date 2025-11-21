---
title: Build a Go console app
description: Connect to an Azure DocumentDB cluster by using a Go console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.reviewer: nlarin
ms.topic: how-to
ms.date: 07/21/2025
ms.custom:
  - devx-track-go
  - build-2025
ai-usage: ai-assisted
# Customer Intent: As a database developer, I want to build a Go console application to quickly and securely connect to and query my database and collections.
---

# Build a Go console app with Azure DocumentDB

[!INCLUDE[Developer console app selector](includes/selector-build-console-app-dev.md)]

This guide explains how to build a Go console application to connect to an Azure DocumentDB cluster. You set up your development environment, use the `azidentity` package from the Azure SDK for Go to authenticate, and perform common operations on documents in the database.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

[!INCLUDE[External - Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

- Microsoft Entra authentication configured for the cluster with your identity granted `root` role.

    - To enable Microsoft Entra authentication, [review the configuration guide](how-to-connect-role-based-access-control.md).

- Latest version of [Go](https://go.dev/).

## Configure your console application

Next, create a new console application project and import the necessary libraries to authenticate to your cluster.

1. Create a new Go module for your project using the `go mod init` command.

    ```bash
    go mod init cosmicworks
    ```

1. Install the `azidentity` package to handle authentication with Microsoft Entra ID.

    ```bash
    go get -u github.com/Azure/azure-sdk-for-go/sdk/azidentity
    ```

1. Install the `mongo` package interact with your cluster.

    ```bash
    go get -u  go.mongodb.org/mongo-driver/v2/mongo
    ```
    
1. Create a new file named `main.go` in your project directory.

    ```bash
    touch main.go
    ```

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

1. Start by importing the required packages at the top of your `main.go` file.

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

1. Create a background context that is used throughout your application.

    ```go
	ctx := context.Background()
    ```

1. Create an instance of `DefaultAzureCredential` that is used to authenticate with Microsoft Entra ID.

    ```go
	credential, err := azidentity.NewDefaultAzureCredential(nil)
	if err != nil {
		panic(err)
	}
    ```

1. Create a callback function that obtains access tokens when the MongoDB driver needs to authenticate.

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

1. Set your cluster name and construct the connection URI.

    ```go
	clusterName := "<azure-documentdb-cluster-name>"
	uri := fmt.Sprintf("mongodb+srv://%s.global.mongocluster.cosmos.azure.com/", clusterName)
    ```

1. Configure the authentication credentials for the MongoDB client.

    ```go
	auth := options.Credential{
		AuthMechanism:       "MONGODB-OIDC",
		OIDCMachineCallback: azureIdentityTokenCallback,
	}
    ```

1. Set up the client options with connection parameters, transport layer security (TLS) configuration, and authentication.

    ```go
	clientOptions := options.Client().
		ApplyURI(uri).
		SetConnectTimeout(2 * time.Minute).
		SetRetryWrites(true).
		SetTLSConfig(&tls.Config{}).
		SetAuth(auth)
    ```

1. Create a MongoDB client instance using the configured options.

    ```go
	client, err := mongo.Connect(clientOptions)
	if err != nil {
		panic(err)
	}

	fmt.Println("Client created")
    ```

1. Add a defer statement to ensure the client is properly disconnected when your application exits.

    ```go
	defer func() {
		if err = client.Disconnect(ctx); err != nil {
			panic(err)
		}
	}()
    ```

## Perform common operations

Finally, use the official library to perform common tasks with databases, collections, and documents. Here, you use the same classes and methods you would use to interact with MongoDB or DocumentDB to manage your collections and items.

1. Get a reference to your database by name.

    ```go
	database := client.Database("<database-name>")

	fmt.Println("Database pointer created")
    ```

1. Get a reference to your collection within the database.

    ```go
	collection := database.Collection("<collection-name>")

	fmt.Println("Collection pointer created")
    ```

1. Define a Product struct to represent your document structure.
    
    ```bash
    type Product struct {
        ID        string `bson:"_id"`
        Category  string `bson:"category"`
        Name      string `bson:"name"`
        Quantity  int    `bson:"quantity"`
        Price     decimal128.Decimal128 `bson:"price"`
        Clearance bool   `bson:"clearance"`
    }
    ```

1. Create or update a document using the `collection.ReplaceOne` operation configured for **upsert**.

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

1. Read a specific document using `collection.FindOne` and a filter with `_id` and `category`.

    ```go
	readFilter := bson.D{{Key: "_id", Value: "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"}, {Key: "category", Value: "gear-surf-surfboards"}}
	var target Product
	err = collection.FindOne(ctx, readFilter).Decode(&target)
	if err != nil {
		panic(err)
	}

	fmt.Printf("Read document name:\t%s\n", target.Name)
    ```

1. Query for multiple documents matching a specific `category` using `collection.Find`.

    ```go
	queryFilter := bson.D{{Key: "category", Value: "gear-surf-surfboards"}}
	cursor, err := collection.Find(ctx, queryFilter)
	if err != nil {
		panic(err)
	}
    ```

1. Retrieve all matching documents from the cursor.

    ```go
	var products []Product
	if err = cursor.All(ctx, &products); err != nil {
		panic(err)
	}
    ```

1. Iterate through and display all the products found in the query.

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

- [Microsoft Entra authentication overview](how-to-connect-role-based-access-control.md)
- [Microsoft Entra configuration for cluster](how-to-connect-role-based-access-control.md)
