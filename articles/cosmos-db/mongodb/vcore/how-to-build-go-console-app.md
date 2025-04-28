---
title: Build a Go console app
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Connect to an Azure Cosmos DB for MongoDB (vCore) cluster by using a Go console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.reviewer: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 04/28/2025
ms.custom: devx-track-go
ai-usage: ai-assisted
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database developer, I want to build a Go console application to quickly and securely connect to and query my database and collections.
---

# Build a Go console app with Azure Cosmos DB for MongoDB vCore

[!INCLUDE[Developer console app selector](includes/selector-build-console-app-dev.md)]

[!INCLUDE[Notice - Entra Authentication preview](includes/notice-entra-authentication-preview.md)]

This guide explains how to build a Go console application to connect to an Azure Cosmos DB for MongoDB vCore cluster. You set up your development environment, use the `azidentity` package from the Azure SDK for Go to authenticate, and perform common operations on documents in the database.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prereq-existing-cluster.md)]

[!INCLUDE[Prerequisite - Azure CLI](includes/prereq-azure-cli.md)]

- Microsoft Entra authentication configured for the cluster with your identity granted `dbOwner` role.

    - To enable Microsoft Entra authentication, [review the configuration guide](how-to-configure-entra-authentication.md).

- Latest version of [Go](https://go.dev/).

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
