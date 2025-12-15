---
title: Build a Java console app
description: Connect to an Azure DocumentDB cluster by using a Java console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.reviewer: nlarin
ms.topic: how-to
ms.date: 07/21/2025
ms.custom:
  - devx-track-java
  - build-2025
ai-usage: ai-assisted
# Customer Intent: As a database developer, I want to build a Java console application to quickly and securely connect to and query my database and collections.
---

# Build a Java console app with Azure DocumentDB

[!INCLUDE[Developer console app selector](includes/selector-build-console-app-dev.md)]

In this guide, you develop a Java console application to connect to an Azure DocumentDB cluster. The guide includes steps to set up your development environment, authenticate using the `azure-identity` package from the Azure SDK for Java, and interact with the database and collection to manage documents.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

[!INCLUDE[External - Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

- Microsoft Entra authentication configured for the cluster with your identity granted `root` role.

    - To enable Microsoft Entra authentication, [review the configuration guide](how-to-connect-role-based-access-control.md).

- Latest version of [Java](/java/openjdk).

## Configure your console application

Next, create a new console application project and import the necessary libraries to authenticate to your cluster.

1. Create a new Maven project using the Maven command-line tools.

    ```bash
    mvn archetype:generate -DgroupId=com.cosmicworks -DartifactId=mongodb-console-app -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
    ```

1. Navigate to the project directory.

    ```bash
    cd mongodb-console-app
    ```

1. Create a new *App.java* file with a `Main` class in the appropriate package directory.

    ```bash
    mkdir -p src/main/java/com/cosmicworks
    touch src/main/java/com/cosmicworks/App.java
    ```
    
1. Add the `azure-identity` dependency to your *pom.xml* file.

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-identity</artifactId>
        <version>1.15.4</version>
    </dependency>
    ```
    
1. Add the `mongodb-driver-sync` dependency to your *pom.xml* file.
    
    ```xml
    <dependency>
        <groupId>org.mongodb</groupId>
        <artifactId>mongodb-driver-sync</artifactId>
        <version>5.4.0</version>
    </dependency>
    ```

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

1. Start by importing the required classes at the top of your Java class file.

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

1. In your main method, create a `DefaultAzureCredential` instance and set up the OpenID Connect (OIDC) callback to fetch tokens.

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
    ```

1. Create a new instance of `MongoCredential` using your previously defined callback.

    ```java
    MongoCredential mongoCredential = MongoCredential.createOidcCredential(null)
            .withMechanismProperty("OIDC_CALLBACK", oidcCallback);
    ```

1. Create variables for the name of the cluster and the entire host endpoint.

    ```java
    String clusterName = "<azure-documentdb-cluster-name>";
    String host = clusterName + ".global.mongocluster.cosmos.azure.com";
    ```

1. Construct a `MongoClientSettings` instance using the host, connection best practices, and the credential.

    ```java
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
    ```

1. Create a new `MongoClient` using the constructed settings.

    ```java
    MongoClient client = MongoClients.create(settings);

    System.out.println("Client created");
    ```

## Perform common operations

Finally, use the official library to perform common tasks with databases, collections, and documents. Here, you use the same classes and methods you would use to interact with MongoDB or DocumentDB to manage your collections and items.

1. Get references to your `database` and `collection`.

    ```java
    MongoDatabase database = client.getDatabase("<database-name>");

    System.out.println("Database pointer created");

    MongoCollection<Document> collection = database.getCollection("<collection-name>");

    System.out.println("Collection pointer created");
    ```


1. Represent your documents using a `Product` class.

    ```java
    public class Product {
        private String _id;
        private String category;
        private String name;
        private int quantity;
        private double price;
        private boolean clearance;
        
        // Getters and setters ommitted for brevity
    }
    ```

1. Create a new document using `collection.replaceOne` with **upsert** enabled.

    ```java
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
    ```

1. Perform a lookup of a single document using `collection.find` and the unique identifier.

    ```java
    Bson filter = Filters.eq("_id", "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb");

    collection.find(filter).forEach(doc -> {
        System.out.println("Read document _id:\\t" + doc.toJson());
    });
    ```

1. Perform a general query using a binary JSON (BSON) filter.

    ```java
    Bson query = Filters.eq("category", "gear-surf-surfboards");

    collection.find(query).forEach(doc -> {
        System.out.println("Found document:\\t" + doc.toJson());
    });
    ```

1. Deleting documents using a filter and `collection.deleteMany`.

    ```java
    Bson filter = Filters.eq("clearance", true);
    collection.deleteMany(filter);
    ```

## Related content

- [Microsoft Entra authentication overview](how-to-connect-role-based-access-control.md)
- [Microsoft Entra configuration for cluster](how-to-connect-role-based-access-control.md)
