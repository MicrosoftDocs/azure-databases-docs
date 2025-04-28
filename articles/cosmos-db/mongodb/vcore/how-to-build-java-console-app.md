---
title: Build a Java console app
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Connect to an Azure Cosmos DB for MongoDB (vCore) cluster by using a Java console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.reviewer: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 04/28/2025
ms.custom: devx-track-java
ai-usage: ai-assisted
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database developer, I want to build a Java console application to quickly and securely connect to and query my database and collections.
---

# Build a Java console app with Azure Cosmos DB for MongoDB vCore

[!INCLUDE[Developer console app selector](includes/selector-build-console-app-dev.md)]

[!INCLUDE[Notice - Entra Authentication preview](includes/notice-entra-authentication-preview.md)]

In this guide, you develop a Java console application to connect to an Azure Cosmos DB for MongoDB vCore cluster. The guide includes steps to set up your development environment, authenticate using the `azure-identity` package from the Azure SDK for Java, and interact with the database and collection to manage documents.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prereq-existing-cluster.md)]

[!INCLUDE[Prerequisite - Azure CLI](includes/prereq-azure-cli.md)]

- Microsoft Entra authentication configured for the cluster with your identity granted `dbOwner` role.

    - To enable Microsoft Entra authentication, [review the configuration guide](how-to-configure-entra-authentication.md).

- Latest version of [Java](/java/openjdk).

## Configure your console application

Next, create a new console application project and import the necessary libraries to authenticate to your cluster.

1. Create a new Maven project using your favorite IDE or the Maven command-line tools:

    ```bash
    mvn archetype:generate -DgroupId=com.cosmicworks -DartifactId=mongodb-console-app -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
    ```

1. Navigate to your project directory:

    ```bash
    cd mongodb-console-app
    ```

1. Create a new Main class in the appropriate package directory:

    ```bash
    mkdir -p src/main/java/com/cosmicworks
    touch src/main/java/com/cosmicworks/App.java
    ```
    
1. Add the Azure Identity dependency to your pom.xml file:

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-identity</artifactId>
        <version>1.15.4</version>
    </dependency>
    ```
    
1. Add the MongoDB Java driver dependency to your pom.xml file:
    
    ```xml
    <dependency>
        <groupId>org.mongodb</groupId>
        <artifactId>mongodb-driver-sync</artifactId>
        <version>5.4.0</version>
    </dependency>
    ```

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

1. Start by importing the required classes at the top of your Java file:

    ```java
    import java.util.concurrent.TimeUnit;
    
    import org.bson.Document;
    import org.bson.conversions.Bson;
    
    import com.azure.core.credential.TokenCredential;
    import com.azure.core.credential.TokenRequestContext;
    import com.azure.identity.DefaultAzureCredentialBuilder;
    import com.mongodb.MongoClientSettings;
    import com.mongodb.MongoCredential;
    import com.mongodb.MongoCredential.OidcCallbackContext;
    import com.mongodb.MongoCredential.OidcCallbackResult;
    import com.mongodb.client.MongoClient;
    import com.mongodb.client.MongoClients;
    import com.mongodb.client.MongoCollection;
    import com.mongodb.client.MongoDatabase;
    import com.mongodb.client.model.Filters;
    import com.mongodb.client.model.ReplaceOptions;
    import com.mongodb.client.result.UpdateResult;
    ```

1. In your main method, create a DefaultAzureCredential and set up the OIDC callback to fetch tokens:

    ```java
    TokenCredential credential = new DefaultAzureCredentialBuilder().build();

    MongoCredential.OidcCallback oidcCallback = new MongoCredential.OidcCallback() {
        @Override
        public OidcCallbackResult onRequest(OidcCallbackContext context) {
            TokenRequestContext tokenRequestContext = new TokenRequestContext()
                    .addScopes("https://ossrdbms-aad.database.windows.net/.default");
            String token = credential.getTokenSync(tokenRequestContext).getToken();
            return new OidcCallbackResult(token);
        }
    };

    MongoCredential mongoCredential = MongoCredential.createOidcCredential(null)
            .withMechanismProperty("OIDC_CALLBACK", oidcCallback);

    String clusterName = "<azure-cosmos-db-mongodb-vcore-cluster-name>";
    String host = clusterName + ".global.mongocluster.cosmos.azure.com";

    MongoClientSettings settings = MongoClientSettings.builder()
            .applyToClusterSettings(builder -> builder
                    .srvHost(host))
            .applyToSocketSettings(builder -> builder
                    .connectTimeout(2, TimeUnit.MINUTES))
            .applyToSslSettings(builder -> builder
                    .enabled(true))
            .retryWrites(true)
            .credential(mongoCredential)
            .build();

    MongoClient client = MongoClients.create(settings);

    System.out.println("Client created");
    ```

1. Create a Product class to represent your documents:

    ```java
    public class Product {
        private String _id;
        private String category;
        private String name;
        private int quantity;
        private double price;
        private boolean clearance;
        
        // Getters and setters
    }
    ```

1. Make sure to handle exceptions properly with try-catch blocks:

    ```java
    try {
        // Your MongoDB operations here
    } catch (Exception e) {
        System.err.println("An error occurred: " + e.getMessage());
        e.printStackTrace();
    }
    ```

1. Don't forget to close your client connection when you're done:

    ```java
    finally {
        if (client != null) {
            client.close();
            System.out.println("Client closed");
        }
    }
    ```

## Perform common operations

Finally, use the official library to perform common tasks with databases, collections, and documents. Here, you use the same classes and methods you would use to interact with MongoDB or DocumentDB to manage your collections and items.

1. Get references to your database and collection:

    ```java
    MongoDatabase database = client.getDatabase("<database-name>");

    System.out.println("Database pointer created");

    MongoCollection<Document> collection = database.getCollection("<collection-name>");

    System.out.println("Collection pointer created");

    Document document = new Document()
            .append("_id", "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb")
            .append("category", "gear-surf-surfboards")
            .append("name", "Yamba Surfboard")
            .append("quantity", 12)
            .append("price", 850.00)
            .append("clearance", false);

    Bson match = Filters.eq("_id", "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb");

    ReplaceOptions options = new ReplaceOptions().upsert(true);
    UpdateResult result = collection.replaceOne(match, document, options);

    System.out.println("Document upserted with _id:\\t" + result.getUpsertedId().asString().getValue());

    Bson filter = Filters.eq("_id", "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb");

    collection.find(filter).forEach(doc -> {
        System.out.println("Read document _id:\\t" + doc.toJson());
    });

    Bson query = Filters.eq("category", "gear-surf-surfboards");

    collection.find(query).forEach(doc -> {
        System.out.println("Found document:\\t" + doc.toJson());
    });

    client.close();

    System.out.println("Client closed");
    ```

1. You can also create, update, or delete multiple documents in a single operation:

    ```java
    List<Document> documents = new ArrayList<>();
    // Add documents to the list
    collection.insertMany(documents);
    ```

1. To update multiple documents matching a specific criterion:

    ```java
    Bson filter = Filters.eq("category", "gear-surf-surfboards");
    Bson update = new Document("$set", new Document("clearance", true));
    collection.updateMany(filter, update);
    ```

1. For deleting documents that match a specific condition:

    ```java
    Bson filter = Filters.eq("clearance", true);
    collection.deleteMany(filter);
    ```

1. You can also perform aggregation operations:

    ```java
    List<Bson> pipeline = Arrays.asList(
        Aggregates.match(Filters.eq("category", "gear-surf-surfboards")),
        Aggregates.group("$category", Accumulators.sum("total", 1))
    );
    collection.aggregate(pipeline).forEach(doc -> System.out.println(doc.toJson()));
    ```

## Related content

- [Microsoft Entra authentication overview](entra-authentication.md)
- [TODO](about:blank)
