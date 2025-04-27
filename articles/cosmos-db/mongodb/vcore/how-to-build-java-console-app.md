---
title: Build a Java console app
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Connect to an Azure Cosmos DB for MongoDB (vCore) cluster by using a Java console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 04/28/2025
ms.custom: devx-track-java
ai-usage: ai-assisted
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database owner, I want to use Mongo Shell to connect to and query my database and collections.
---

# Build a Java console app with Azure Cosmos DB for MongoDB vCore

[!INCLUDE[Developer console app selector](includes/build-console-app-dev-selector.md)]

[!INCLUDE[Console app introduction](includes/console-app-introduction.md)]

This guide uses the open-source `mongodb-driver-sync` library from Maven.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prereq-existing-cluster.md)]

[!INCLUDE[Prerequisite - Azure CLI](includes/prereq-azure-cli.md)]

- Latest version of [Java](/java/openjdk).

## Grant your identity access

[!INCLUDE[Console app identity access](includes/console-app-identity-access.md)]

## Configure your console application

Next, create a new console application project and import the necessary libraries to authenticate to your cluster.

1. TODO

    ```bash

    ```

1. TODO

    ```bash

    ```

1. TODO

    ```bash

    ```
    
1. TODO

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-identity</artifactId>
        <version>1.15.4</version>
    </dependency>
    ```
    
1. TODO
    
    ```xml
    <dependency>
        <groupId>org.mongodb</groupId>
        <artifactId>mongodb-driver-sync</artifactId>
        <version>5.4.0</version>
    </dependency>
    ```

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

1. TODO

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

1. TODO

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

1. TODO

    ```java
    
    ```

1. TODO

    ```java
    
    ```

1. TODO

    ```java
    
    ```

## Perform common operations

Finally, use the official library to perform common tasks with databases, collections, and documents. Here, you use the same classes and methods you would use to interact with MongoDB or DocumentDB to manage your collections and items.

1. TODO

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

1. TODO

    ```java
    
    ```

1. TODO

    ```java
    
    ```

1. TODO

    ```java
    
    ```

1. TODO

    ```java
    
    ```

## Related content

- [Microsoft Entra authentication overview](entra-authentication.md)
- [TODO](about:blank)
