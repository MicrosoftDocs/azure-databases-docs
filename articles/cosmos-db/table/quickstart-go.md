---
title: Quickstart - Azure SDK for Go
titleSuffix: Azure Cosmos DB for Table
description: Deploy a Go web application that uses the Azure SDK for Go to interact with Azure Cosmos DB for Table data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.reviewer: sasinnat
ms.service: azure-cosmos-db
ms.subservice: table
ms.devlang: golang
ms.topic: quickstart-sdk
ms.date: 04/08/2025
ms.custom: devx-track-go, devx-track-extended-azdevcli
# CustomerIntent: As a developer, I want to learn the basics of the Go library so that I can build applications with Azure Cosmos DB for Table.
---

# Quickstart: Use Azure Cosmos DB for Table with Azure SDK for Go

[!INCLUDE[Developer Quickstart selector](includes/quickstart/dev-selector.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for Table application using the Azure SDK for Go. Azure Cosmos DB for Table is a schemaless data store allowing applications to store structured table data in the cloud. You learn how to create tables, rows, and perform basic tasks within your Azure Cosmos DB resource using the Azure SDK for Go.

[Library source code](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/aztables#pkg-types) | [Package (Go)](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/aztables) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

- Azure Developer CLI
- Docker Desktop
- `Go` 1.21 or newer

If you don't have an Azure account, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Initialize the project

Use the Azure Developer CLI (`azd`) to create an Azure Cosmos DB for Table account and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

1. Open a terminal in an empty directory.

1. If you're not already authenticated, authenticate to the Azure Developer CLI using `azd auth login`. Follow the steps specified by the tool to authenticate to the CLI using your preferred Azure credentials.

    ```azurecli
    azd auth login
    ```

1. Use `azd init` to initialize the project.

    ```azurecli
    azd init --template cosmos-db-table-go-quickstart
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

:::image type="content" source="media/quickstart-go/running-application.png" alt-text="Screenshot of the running web application.":::

### Install the client library

The client library is available through Go, as the `aztables` package.

1. Open a terminal and navigate to the `/src` folder.

    ```bash
    cd ./src
    ```

1. If not already installed, install the `aztables` package using `go install`.

    ```bash
    go install github.com/Azure/azure-sdk-for-go/sdk/data/aztables
    ```

1. Open and review the **src/go.mod** file to validate that the `github.com/Azure/azure-sdk-for-go/sdk/data/aztables` entry exists.

### Import libraries

Import the `github.com/Azure/azure-sdk-for-go/sdk/azidentity` and `github.com/Azure/azure-sdk-for-go/sdk/data/aztables` packages into your application code.

```go
import (
	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	"github.com/Azure/azure-sdk-for-go/sdk/data/aztables"
)
```

## Object model

| Name | Description |
| --- | --- |
| [`ServiceClient`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/aztables#ServiceClient) | This type is the primary client type and is used to manage account-wide metadata or databases. |
| [`Client`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/aztables#Client) | This type represents the client for a table within the account. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a table](#get-a-table)
- [Create an entity](#create-an-entity)
- [Get an entity](#get-an-entity)
- [Query entities](#query-entities)

The sample code in the template uses a table named `cosmicworks-products`. The `cosmicworks-products` table contains details such as name, category, quantity, price, a unique identifier, and a sale flag for each product. The container uses a *unique identifier* as the row key and *category* as a partition key.

### Authenticate the client

This sample creates a new instance of the `ServiceClient` type.

```go
credential, err := azidentity.NewDefaultAzureCredential(nil)
if err != nil {
    return err
}

client, err := aztables.NewServiceClient("<azure-cosmos-db-table-account-endpoint>", credential)
if err != nil {
    log.Fatal(err)
}
```

### Get a table

This sample creates an instance of the `Client` type using the `NewClient` function of the `ServiceClient` type.

```go
table, err := client.NewClient("<azure-cosmos-db-table-name>")
if err != nil {
    log.Fatal(err)
}
```

### Create an entity

The easiest way to create a new entity in a table is to create an instance of type `aztables.EDMEntity`. Set the `RowKey` and `PartitionKey` properties using the `aztables.Entity` type and then set any extra properties using a string map.

```go
entity := aztables.EDMEntity{
    Entity: aztables.Entity{
        RowKey:       "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        PartitionKey: "gear-surf-surfboards",
    },
    Properties: map[string]any{
        "Name":      "Yamba Surfboard",
        "Quantity":  12,
        "Price":     850.00,
        "Clearance": false,
    },
}
```

Conver the entity into a byte array using `json.Marshal` and then create the entity in the table using `UpsertEntity`.

```go
bytes, err := json.Marshal(entity)
if err != nil {
    panic(err)
}

_, err = table.UpsertEntity(context.TODO(), bytes, nil)
if err != nil {
    panic(err)
}
```

### Get an entity

You can retrieve a specific entity from a table using `GetEntity`. You can then use `json.Unmarshal` to parse it using the `aztables.EDMEntity` type.

```go
rowKey := "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"
partitionKey := "gear-surf-surfboards"

response, err := table.GetEntity(context.TODO(), partitionKey, rowKey, nil)
if err != nil {
    panic(err)
}

var entity aztables.EDMEntity
err = json.Unmarshal(response.Value, &entity)
if err != nil {
    panic(err)
}
```

### Query entities

After you insert an entity, you can also run a query to get all entities that match a specific filter by using `NewListEntitiesPager` along with a string filter.

```go
category := "gear-surf-surfboards"
// Ensure the value is OData-compliant by escaping single quotes
safeCategory := strings.ReplaceAll(category, "'", "''")
filter := fmt.Sprintf("PartitionKey eq '%s'", safeCategory)

options := &aztables.ListEntitiesOptions{
    Filter: &filter,
}

pager := table.NewListEntitiesPager(options)
```

Parse the paginated results of the query by using the `More` function of the pager to determine if there are more pages, and then the `NextPage` function to get the next page of results.

```go
for pager.More() {
    response, err := pager.NextPage(context.TODO())
    if err != nil {
        panic(err)
    }
    for _, entityBytes := range response.Entities {
        var entity aztables.EDMEntity
        err := json.Unmarshal(entityBytes, &entity)
        if err != nil {
            panic(err)
        }
        
        writeOutput(fmt.Sprintf("Found entity:\t%s\t%s", entity.Properties["Name"], entity.RowKey))
    }
}
```

## Clean up resources

When you no longer need the sample application or resources, remove the corresponding deployment and all resources.

```azurecli
azd down
```

## Related content

- [.NET Quickstart](quickstart-dotnet.md)
- [Node.js Quickstart](quickstart-nodejs.md)
- [Python Quickstart](quickstart-python.md)
- [Java Quickstart](quickstart-java.md)
