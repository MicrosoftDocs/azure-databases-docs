---
title: 'Tutorial: Java App to Load Sample Data into an API for Cassandra Table in Azure Cosmos DB'
description: This tutorial shows how to load sample user data to an API for a Cassandra table in Azure Cosmos DB by using a Java application.
ms.service: azure-cosmos-db
ms.subservice: apache-cassandra
ms.topic: tutorial
ms.date: 05/20/2019
author: TheovanKraay
ms.author: thvankra
ms.devlang: java
ms.custom: devx-track-extended-java
#Customer intent: As a developer, I want to build a Java application to load data to an API for Cassandra table in Azure Cosmos DB. Customers want to store and manage the key/value data and use the global distribution, elastic scaling, multiregion, and other capabilities that are offered by Azure Cosmos DB.
---

# Tutorial: Load sample data into an API for Cassandra table in Azure Cosmos DB
[!INCLUDE[Cassandra](../includes/appliesto-cassandra.md)]

As a developer, you might have applications that use key/value pairs. You can use an API for Cassandra account in Azure Cosmos DB to store and manage key/value data. This tutorial shows you how to load sample user data to a table in an API for Cassandra account in Azure Cosmos DB by using a Java application. The Java application uses the [Java driver](https://github.com/datastax/java-driver) and loads user data such as the user ID, username, and user city.

This tutorial covers the following tasks:

> [!div class="checklist"]
> * Load data into a Cassandra table.
> * Run the app.

## Prerequisites

* If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.
* This article belongs to a multipart tutorial. Before you start with this article, make sure to [create the API for Cassandra account, keyspace, and table](create-account-java.md).

## Load data into the table

To load data into your API for Cassandra table, follow these steps:

1. Open the `UserRepository.java` file under the `src\main\java\com\azure\cosmosdb\cassandra` folder. Append the code to insert the `user_id`, `user_name`, and `user_bcity` fields into the table.

   ```java
   /**
   * Insert a row into user table
   *
   * @param id   user_id
   * @param name user_name
   * @param city user_bcity
   */
   public void insertUser(PreparedStatement statement, int id, String name, String city) {
        BoundStatement boundStatement = new BoundStatement(statement);
        session.execute(boundStatement.bind(id, name, city));
   }

   /**
   * Create a PrepareStatement to insert a row to user table
   *
   * @return PreparedStatement
   */
   public PreparedStatement prepareInsertStatement() {
      final String insertStatement = "INSERT INTO  uprofile.user (user_id, user_name , user_bcity) VALUES (?,?,?)";
   return session.prepare(insertStatement);
   }
   ```

1. Open the `UserProfile.java` file under the `src\main\java\com\azure\cosmosdb\cassandra` folder. This class contains the main method that calls the `createKeyspace` and `createTable` methods that you defined earlier. Now append the following code to insert some sample data into the API for Cassandra table.

   ```java
   //Insert rows into user table
   PreparedStatement preparedStatement = repository.prepareInsertStatement();
     repository.insertUser(preparedStatement, 1, "JohnH", "Seattle");
     repository.insertUser(preparedStatement, 2, "EricK", "Spokane");
     repository.insertUser(preparedStatement, 3, "MatthewP", "Tacoma");
     repository.insertUser(preparedStatement, 4, "DavidA", "Renton");
     repository.insertUser(preparedStatement, 5, "PeterS", "Everett");
   ```

## Run the app

Open a command prompt or terminal window and change the folder path to where you created the project. Run the `mvn clean install` command to generate the `cosmosdb-cassandra-examples.jar` file within the target folder and run the application.

```bash
cd "cassandra-demo"

mvn clean install

java -cp target/cosmosdb-cassandra-examples.jar com.azure.cosmosdb.cassandra.examples.UserProfile
```

You can now open Data Explorer in the Azure portal to confirm that the user information was added to the table.

## Next step

In this tutorial, you learned how to load sample data to an API for Cassandra account in Azure Cosmos DB. You can now proceed to the next article:

> [!div class="nextstepaction"]
> [Query data from the API for Cassandra account](query-data.md)
