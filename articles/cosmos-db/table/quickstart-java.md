---
title: Quickstart - Azure SDK for Java
titleSuffix: Azure Cosmos DB for Table
description: Deploy a Java web application that uses the Azure SDK for Java to interact with Azure Cosmos DB for Table data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.reviewer: sasinnat
ms.service: azure-cosmos-db
ms.subservice: table
ms.devlang: java
ms.topic: quickstart-sdk
ms.date: 04/08/2025
ms.custom: devx-track-java, devx-track-extended-azdevcli
# CustomerIntent: As a developer, I want to learn the basics of the Java library so that I can build applications with Azure Cosmos DB for Table.
---

# Quickstart: Use Azure Cosmos DB for Table with Azure SDK for Java

[!INCLUDE[Developer Quickstart selector](includes/quickstart/dev-selector.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for Table application using the Azure SDK for Java. Azure Cosmos DB for Table is a schemaless data store allowing applications to store structured table data in the cloud. You learn how to create tables, rows, and perform basic tasks within your Azure Cosmos DB resource using the Azure SDK for Java.

[API reference documentation](/java/api/com.azure.data.tables) | [Library source code](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/tables/azure-data-tables) | [Package (Maven)](https://mvnrepository.com/artifact/com.azure/azure-data-tables) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

- Azure Developer CLI
- Docker Desktop
- Java 21

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
    azd init --template cosmos-db-table-java-quickstart
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

:::image type="content" source="media/quickstart-java/running-application.png" alt-text="Screenshot of the running web application.":::

### Install the client library

The client library is available through Maven, as the `azure-data-tables` package.

1. Navigate to the `/src/web` folder and open the **pom.xml** file.

    ```bash
    cd ./src
    ```

1. If it doesn't already exist, add an entry for the `azure-data-tables` package.

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-data-tables</artifactId>
    </dependency>
    ```

### Import libraries

Import all of the required namespaces into your application code.

```java
import com.azure.core.http.rest.PagedFlux;
import com.azure.data.tables.TableAsyncClient;
import com.azure.data.tables.TableClientBuilder;
import com.azure.data.tables.models.ListEntitiesOptions;
import com.azure.data.tables.models.TableEntity;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
```

## Object model

| Name | Description |
| --- | --- |
| [`TableServiceAsyncClient`](/java/api/com.azure.data.tables.tableserviceasyncclient) | This type is the primary client type and is used to manage account-wide metadata or databases. |
| [`TableAsyncClient`](/java/api/com.azure.data.tables.tableasyncclient) | This type represents the client for a table within the account. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a table](#get-a-table)
- [Create an entity](#create-an-entity)
- [Get an entity](#get-an-entity)
- [Query entities](#query-entities)

The sample code in the template uses a table named `cosmicworks-products`. The `cosmicworks-products` table contains details such as name, category, quantity, price, a unique identifier, and a sale flag for each product. The container uses a *unique identifier** as the row key and *category* as a partition key.

### Authenticate the client

This sample creates a new instance of the `TableServiceAsyncClient` class.

```java
DefaultAzureCredential azureTokenCredential = new DefaultAzureCredentialBuilder()
    .build();

TableServiceAsyncClient client = new TableServiceClientBuilder()
    .endpoint("<azure-cosmos-db-table-account-endpoint>")
    .credential(credential)
    .buildAsyncClient();
```

### Get a table

This sample creates an instance of the `TableAsyncClient` class using the `GetTableClient` method of the `TableServiceClient` class.

```java
TableAsyncClient table = client
    .getTableClient("<azure-cosmos-db-table-name>");
```

### Create an entity

The easiest way to create a new entity in a table is to use `createEntity`.

```java
String rowKey = "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb";
String partitionKey = "gear-surf-surfboards";

TableEntity entity = new TableEntity(partitionKey, rowKey)
        .addProperty("Name", "Yamba Surfboard")
        .addProperty("Quantity", 12)
        .addProperty("Price", 850.00)
        .addProperty("Sale", false);
```

Create an entity in the collection using `upsertEntity`.

```java
Mono<Void> response = table.upsertEntity(entity);
```

### Get an entity

You can retrieve a specific entity from a table using `getEntity`.

```java
String rowKey = "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb";
String partitionKey = "gear-surf-surfboards";

TableEntity entity = table.getEntity(partitionKey, rowKey);
```

### Query entities

After you insert an entity, you can also run a query to get all entities that match a specific filter by using `listEntities` and the `ListEntitiesOptions` class. Use the `setFilter` method to specify a string OData filter.

```java
ListEntitiesOptions options = new ListEntitiesOptions()
    .setFilter("PartitionKey eq 'gear-surf-surfboards'");

PagedFlux<TableEntity> tableEntities = table.listEntities(options, null, null);
```

Parse the paginated results of the query by using a subscription.

```java
tableEntities
    .DoOnNext(entity -> {
        // Do something
    });
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
- [Go Quickstart](quickstart-go.md)
