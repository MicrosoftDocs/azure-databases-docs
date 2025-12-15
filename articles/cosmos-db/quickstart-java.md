---
title: Quickstart - Azure SDK for Java
titleSuffix: Azure Cosmos DB for NoSQL
description: Deploy a Java Spring Web application that uses the Azure SDK for Java to interact with Azure Cosmos DB for NoSQL data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: java
ms.topic: quickstart-sdk
ms.date: 06/11/2025
ms.custom: devx-track-extended-java, devx-track-extended-azdevcli
appliesto:
  - ✅ NoSQL
# CustomerIntent: As a developer, I want to learn the basics of the Java library so that I can build applications with Azure Cosmos DB for NoSQL.
---

# Quickstart: Use Azure Cosmos DB for NoSQL with Azure SDK for Java

[!INCLUDE[Developer Quickstart selector](includes/quickstart/dev-selector.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for NoSQL application using the Azure SDK for Java. Azure Cosmos DB for NoSQL is a schemaless data store allowing applications to store unstructured data in the cloud. Query data in your containers and perform common operations on individual items using the Azure SDK for Java.

[API reference documentation](/java/api/overview/azure/cosmos-readme) | [Library source code](https://github.com/azure/azure-sdk-for-java/tree/main/sdk/cosmos/azure-cosmos) | [Package (Maven)](https://mvnrepository.com/artifact/com.azure/azure-cosmos) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

- Azure Developer CLI
- Docker Desktop
- Java 21

If you don't have an Azure account, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Initialize the project

Use the Azure Developer CLI (`azd`) to create an Azure Cosmos DB for NoSQL account and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

1. Open a terminal in an empty directory.

1. If you're not already authenticated, authenticate to the Azure Developer CLI using `azd auth login`. Follow the steps specified by the tool to authenticate to the CLI using your preferred Azure credentials.

    ```azurecli
    azd auth login
    ```

1. Use `azd init` to initialize the project.

    ```azurecli
    azd init --template cosmos-db-nosql-java-quickstart
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

The client library is available through Maven, as the `azure-spring-data-cosmos` package.

1. Navigate to the `/src/web` folder and open the **pom.xml** file.

1. If it doesn't already exist, add an entry for the `azure-spring-data-cosmos` package.

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-spring-data-cosmos</artifactId>
    </dependency>
    ```

1. Also, add another dependency for the `azure-identity` package if it doesn't already exist.

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-identity</artifactId>
    </dependency>
    ```

### Import libraries

Import all of the required namespaces into your application code.

```java
import com.azure.cosmos.CosmosClientBuilder;
import com.azure.cosmos.models.PartitionKey;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.spring.data.cosmos.config.AbstractCosmosConfiguration;
import com.azure.spring.data.cosmos.config.CosmosConfig;
import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;
import com.azure.spring.data.cosmos.repository.CosmosRepository;
import com.azure.spring.data.cosmos.repository.Query;
import com.azure.spring.data.cosmos.repository.config.EnableCosmosRepositories;
```

## Object model

| Name | Description |
| --- | --- |
| `EnableCosmosRepositories` | This type is a method decorator used to configure a repository to access Azure Cosmos DB for NoSQL. |
| `CosmosRepository` | This class is the primary client class and is used to manage data within a container. |
| `CosmosClientBuilder` | This class is a factory used to create a client used by the repository. |
| `Query` | This type is a method decorator used to specify the query that the repository executes. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a database](#get-a-database)
- [Get a container](#get-a-container)
- [Create an item](#create-an-item)
- [Get an item](#read-an-item)
- [Query items](#query-items)

The sample code in the template uses a database named `cosmicworks` and container named `products`. The `products` container contains details such as name, category, quantity, a unique identifier, and a sale flag for each product. The container uses the `/category` property as a logical partition key.

### Authenticate the client

First, this sample creates a new class that inherits from `AbstractCosmosConfiguration` to configure the connection to Azure Cosmos DB for NoSQL.

```java
@Configuration
@EnableCosmosRepositories
public class CosmosConfiguration extends AbstractCosmosConfiguration {
}
```

Within the configuration class, this sample creates a new instance of the `CosmosClientBuilder` class and configures authentication using a `DefaultAzureCredential` instance.

```java
@Bean
public CosmosClientBuilder getCosmosClientBuilder() {
    DefaultAzureCredential credential = new DefaultAzureCredentialBuilder()
        .build();
        
    return new CosmosClientBuilder()
        .endpoint("<azure-cosmos-db-nosql-account-endpoint>")
        .credential(credential);
}
```

### Get a database

In the configuration class, the sample implements a method to return the name of the existing database named *`cosmicworks`*.

```java
@Override
protected String getDatabaseName() {
    return "cosmicworks";
}
```

### Get a container

Use the `Container` method decorator to configure a class to represent items in a container. Author the class to include all of the members you want to serialize into JSON. In this example, the type has a unique identifier, and fields for category, name, quantity, price, and clearance.

```java
@Container(containerName = "products", autoCreateContainer = false)
public class Item {
    private String id;
    private String name;
    private Integer quantity;
    private Boolean sale;

    @PartitionKey
    private String category;

    // Extra members omitted for brevity
}
```

### Create an item

Create an item in the container using `repository.save`.

```java
Item item = new Item(
    "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
    "gear-surf-surfboards",
    "Yamba Surfboard",
    12,
    false
);
Item created_item = repository.save(item);
```

### Read an item

Perform a point read operation by using both the unique identifier (`id`) and partition key fields. Use `repository.findById` to efficiently retrieve the specific item.

```java
PartitionKey partitionKey = new PartitionKey("gear-surf-surfboards");
Optional<Item> existing_item = repository.findById("aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb", partitionKey);
if (existing_item.isPresent()) {
    // Do something
}
```

### Query items

Perform a query over multiple items in a container by defining a query in the repository's interface. This sample uses the `Query` method decorator to define a method that executes this parameterized query:

```nosql
SELECT * FROM products p WHERE p.category = @category
```

```java
@Repository
public interface ItemRepository extends CosmosRepository<Item, String> {

    @Query("SELECT * FROM products p WHERE p.category = @category")
    List<Item> getItemsByCategory(@Param("category") String category);

}
```

Fetch all of the results of the query using `repository.getItemsByCategory`. Loop through the results of the query.

```java
List<Item> items = repository.getItemsByCategory("gear-surf-surfboards");
for (Item item : items) {
    // Do something
}
```

### Explore your data

Use the Visual Studio Code extension for Azure Cosmos DB to explore your NoSQL data. You can perform core database operations including, but not limited to:

- Performing queries using a scrapbook or the query editor
- Modifying, updating, creating, and deleting items
- Importing bulk data from other sources
- Managing databases and containers

For more information, see [How-to use Visual Studio Code extension to explore Azure Cosmos DB for NoSQL data](visual-studio-code-extension.md?pivots=api-nosql).

## Clean up resources

When you no longer need the sample application or resources, remove the corresponding deployment and all resources.

```azurecli
azd down
```

## Related content

- [.NET Quickstart](quickstart-dotnet.md)
- [Node.js Quickstart](quickstart-nodejs.md)
- [java Quickstart](quickstart-java.md)
- [Go Quickstart](quickstart-go.md)
- [Rust Quickstart](quickstart-go.md)
