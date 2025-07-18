---
title: 'Quickstart: Java library'
titleSuffix: Azure Cosmos DB for Apache Cassandra
description: Create a new Azure Cosmos DB for Apache Cassandra account and connect using the Java library in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: apache-cassandra
ms.topic: quickstart-sdk
ms.devlang: java
ms.custom: devx-track-java, sfi-ropc-nochange
ms.date: 07/18/2025
ai-usage: ai-generated
---

# Quickstart: Azure Cosmos DB for Apache Cassandra client library for Java

[!INCLUDE[Quickstart developer selector](includes/selector-quickstart-developer.md)]

Get started with the Azure Cosmos DB for Apache Cassandra client library for Java to store, manage, and query unstructured data. Follow the steps in this guide to create a new account, install a Java client library, connect to the account, perform common operations, and query your final sample data.

[API reference documentation](https://docs.datastax.com/en/developer/java-driver/index.html) | [Library source code](https://github.com/apache/cassandra-java-driver/tree/4.x) | [Package (Maven)](https://mvnrepository.com/artifact/org.apache.cassandra/java-driver-core)

## Prerequisites

[!INCLUDE[Prerequisites - Quickstart developer](../includes/prerequisites-quickstart-developer.md)]

- Java 21 or later

## Setting up

First, set up the account and development environment for this guide. This section walks you through the process of creating an account, getting its credentials, and then preparing your development environment.

### Create an account

[!INCLUDE[Section - Setting up](includes/section-quickstart-provision.md)]

### Get credentials

[!INCLUDE[Section - Get credentials](includes/section-quickstart-credentials.md)]

### Prepare development environment

Then, configure your development environment with a new project and the client library. This step is the last required prerequisite before moving on to the rest of this guide.

1. Start in an empty directory.

1. Generate a new Java console project using Maven.

    ```bash
    mvn archetype:generate -DgroupId=quickstart -DartifactId=console -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
    ```  

1. Import the `java-driver-core` package from Maven. Add this section to your *pom.xml* file.

    ```bash
    <dependency>
      <groupId>org.apache.cassandra</groupId>
      <artifactId>java-driver-core</artifactId>
      <version>[4.,)</version>
    </dependency>
    ```

1. Open the */console/src/main/java/quickstart/App.java* file.

1. Observe the existing Java application boilerplate.

    ```java
    package quickstart;
    
    /**
     * Hello world!
     *
     */
    public class App 
    {
        public static void main( String[] args )
        {
            System.out.println( "Hello World!" );
        }
    }
    ```

1. Remove the comments and console output from the boilerplate. This code block is the starting point for the remainder of this guide.

    ```java
    package quickstart;
    
    public class App 
    {
        public static void main(String[] args)
        {
        }
    }
    ```

1. Import the `java.security.NoSuchAlgorithmException` namespace.
    
    ```java
    import java.security.NoSuchAlgorithmException;
    ```

1. Update the `main` method signature to indicate that it could throw the `NoSuchAlgorithmException` exception.

    ```java
    public static void main(String[] args) throws NoSuchAlgorithmException
    {    
    }
    ```

    > [!IMPORTANT]
    > The remaining steps within this guide assume that you're adding your code within the `main` method.

1. Build the project.

    ```bash
    mvn compile
    ```

## Object model

| | Description |
| --- | --- |
| **`CqlSession`** | Represents a specific connection to a cluster |
| **`PreparedStatement`** | Represents a precompiled CQL statement that can be executed multiple times efficiently |
| **`BoundStatement`** | Represents a prepared statement with bound parameters |
| **`Row`** | Represents a single row of a query result |

## Code examples

- [Authenticate client](#authenticate-client)
- [Upsert data](#upsert-data)
- [Read data](#read-data)
- [Query data](#query-data)

### Authenticate client

Start by authenticating the client using the credentials gathered earlier in this guide.

1. Open the */console/src/main/java/quickstart/App.java* file in your integrated development environment (IDE).

1. Import the following types:

    - `java.net.InetSocketAddress`
    - `javax.net.ssl.SSLContext`
    - `com.datastax.oss.driver.api.core.CqlIdentifier`
    - `com.datastax.oss.driver.api.core.CqlSession`
    - `com.datastax.oss.driver.api.core.cql.BoundStatement`
    - `com.datastax.oss.driver.api.core.cql.PreparedStatement`
    - `com.datastax.oss.driver.api.core.cql.ResultSet`
    - `com.datastax.oss.driver.api.core.cql.Row`

    ```java
    import java.net.InetSocketAddress;    

    import javax.net.ssl.SSLContext;

    import com.datastax.oss.driver.api.core.CqlIdentifier;
    import com.datastax.oss.driver.api.core.CqlSession;
    import com.datastax.oss.driver.api.core.cql.BoundStatement;
    import com.datastax.oss.driver.api.core.cql.PreparedStatement;
    import com.datastax.oss.driver.api.core.cql.ResultSet;
    import com.datastax.oss.driver.api.core.cql.Row;
    ```

1. Create string variables for the credentials collected earlier in this guide. Name the variables `username`, `password`, and `contactPoint`. Also create a string variable named `region` for the local data center.

    ```java
    String username = "<username>";
    String password = "<password>";
    String contactPoint = "<contact-point>";
    ```

1. Create another string variable for the region where you created your Azure Cosmos DB for Apache Cassandra account. Name this variable `region`.

    ```javascript
    String region = "<region>";
    ```

1. Create an `SSLContext` object to ensure that you're using the transport layer security (TLS) protocol.

    ```java
    SSLContext sslContext = SSLContext.getDefault();
    ```

1. Create a new `CqlSession` object using the credential and configuration variables created in the previous steps. Set the contact point, local data center, authentication credentials, keyspace, and Transport Layer Security (TLS) context.

    ```java
    CqlSession session = CqlSession.builder()
        .addContactPoint(new InetSocketAddress(contactPoint, 10350))
        .withLocalDatacenter(region)
        .withAuthCredentials(username, password)
        .withKeyspace(CqlIdentifier.fromCql("cosmicworks"))
        .withSslContext(sslContext)
        .build();
    ```

[!INCLUDE[Section - Transport Layer Security disabled warning](../includes/section-transport-layer-security-disabled-warning.md)]

### Upsert data

Next, upsert new data into a table. Upserting ensures that the data is created or replaced appropriately depending on whether the same data already exists in the table.

1. Define a new class named `Product` with fields corresponding to the table created earlier in this guide.

    ```java
    class Product {
        public String id;
        public String name;
        public String category;
        public int quantity;
        public boolean clearance;

        public Product(String id, String name, String category, int quantity, boolean clearance) {
            this.id = id;
            this.name = name;
            this.category = category;
            this.quantity = quantity;
            this.clearance = clearance;
        }

        @Override
        public String toString() {
            return String.format("Product{id='%s', name='%s', category='%s', quantity=%d, clearance=%b}",
                    id, name, category, quantity, clearance);
        }
    }
    ```

    > [!TIP]
    > In Java, you can create this type in another file or create it at the end of the existing file.

1. Create a new object of type `Product`. Store the object in a variable named `product`.

    ```java
    Product product = new Product(
        "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        "Yamba Surfboard",
        "gear-surf-surfboards",
        12,
        false
    );
    ```

1. Create a new string variable named `insertQuery` with the Cassandra Query Language (CQL) query for inserting a new row.

    ```java
    String insertQuery = "INSERT INTO product (id, name, category, quantity, clearance) VALUES (?, ?, ?, ?, ?)";
    ```

1. Prepare the insert statement and bind the product properties as parameters.

    ```java
    PreparedStatement insertStmt = session.prepare(insertQuery);
    BoundStatement boundInsert = insertStmt.bind(
        product.id,
        product.name,
        product.category,
        product.quantity,
        product.clearance
    );
    ```

1. Upsert the product by executing the bound statement.

    ```java
    session.execute(boundInsert);
    ```

### Read data

Then, read data that was previously upserted into the table.

1. Create a new string variable named `readQuery` with a CQL query that matches items with the same `id` field.

    ```java
    String readQuery = "SELECT * FROM product WHERE id = ? LIMIT 1";
    ```

1. Create a string variable named `id` with the same value as the product created earlier in this guide.

    ```go
    String id = "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb";
    ```

1. Prepare the statement and bind the product's `id` field as a parameter.

    ```java
    PreparedStatement readStmt = session.prepare(readQuery);
    BoundStatement boundRead = readStmt.bind(id);
    ```

1. Execute the bound statement and store the result in a variable named `readResult`.

    ```java
    ResultSet readResult = session.execute(boundRead);
    ```

1. Retrieve the first row from the result set and map it to a `Product` object if found.

    ```java
    Row row = readResult.one();
    Product matchedProduct = new Product(
        row.getString("id"),
        row.getString("name"),
        row.getString("category"),
        row.getInt("quantity"),
        row.getBoolean("clearance")
    );
    ```

### Query data

Now, use a query to find all data that matches a specific filter in the table.

1. Create a new string variable named `findQuery` with a CQL query that matches items with the same `category` field.

    ```java
    String findQuery = "SELECT * FROM product WHERE category = ? ALLOW FILTERING";
    ```

1. Create a string variable named `id` with the same value as the product created earlier in this guide.

    ```java
    String category = "gear-surf-surfboards";
    ```

1. Prepare the statement and bind the product category as a parameter.

    ```java
    PreparedStatement findStmt = session.prepare(findQuery);
    BoundStatement boundFind = findStmt.bind(category);
    ```

1. Execute the bound statement and store the result in a variable named `findResults`.

    ```java
    ResultSet results = session.execute(boundFind);
    ```

1. Iterate over the query results and map each row to a `Product` object.

    ```java
    for (Row result : results) {
        Product queriedProduct = new Product(
            result.getString("id"),
            result.getString("name"),
            result.getString("category"),
            result.getInt("quantity"),
            result.getBoolean("clearance")
        );
        // Do something here with each result
    }
    ```

### Close session

In Java, you're required to close the session after you're done with any queries and operations.

```java
session.close();
```

## Run the code

Run the newly created application using a terminal in your application directory.

```bash
mvn compile
mvn exec:java -Dexec.mainClass="quickstart.App"
```

> [!TIP]
> Ensure that you're running this command within the */console* path created within this guide.

## Clean up resources

[!INCLUDE[Section - Quickstart cleanup](includes/section-quickstart-credentials.md)]

## Next step

> [!div class="nextstepaction"]
> [Overview of Azure Cosmos DB for Apache Cassandra](introduction.md)
