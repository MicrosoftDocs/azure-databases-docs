---
title: 'Tutorial: Query Data from an API for Cassandra Account in Azure Cosmos DB'
description: This tutorial shows how to query user data from Azure Cosmos DB for an Apache Cassandra account by using a Java application.
ms.service: azure-cosmos-db
author: TheovanKraay
ms.author: thvankra
ms.subservice: apache-cassandra
ms.custom: devx-track-extended-java
ms.topic: tutorial
ms.date: 09/24/2018
#Customer intent: As a developer, I want to build a Java application to query data stored in an API for Cassandra account in Azure Cosmos DB. Customers want to manage the key/value data and use the global distribution, elastic scaling, multiple write regions, and other capabilities offered by Azure Cosmos DB.
---

# Tutorial: Query data from an API for Cassandra account in Azure Cosmos DB
[!INCLUDE[Cassandra](../includes/appliesto-cassandra.md)]

As a developer, you might have applications that use key/value pairs. You can use an API for Cassandra account in Azure Cosmos DB to store and query the key/value data. This tutorial shows you how to query user data from an API for Cassandra account in Azure Cosmos DB by using a Java application. The Java application uses the [Java driver](https://github.com/datastax/java-driver) and queries user data such as the user ID, username, and user city.

This tutorial covers the following tasks:

> [!div class="checklist"]
> * Query data from a Cassandra table.
> * Run the app.

## Prerequisites

* If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.
* This article belongs to a multipart tutorial. Before you start, make sure to complete the previous steps to create the API for Cassandra account, keyspace, and table. Also [load sample data into the table](load-data-table.md).

## Query data

To query data from your API for Cassandra account, follow these steps:

1. Open the `UserRepository.java` file under the folder `src\main\java\com\azure\cosmosdb\cassandra`. Append the following code block. This code provides three methods to:

   * Query all users in the database.
   * Query a specific user filtered by the user ID.
   * Delete a table.

   ```java
   /**
   * Select all rows from user table
   */
   public void selectAllUsers() {

     final String query = "SELECT * FROM uprofile.user";
     List<Row> rows = session.execute(query).all();

     for (Row row : rows) {
        LOGGER.info("Obtained row: {} | {} | {} ", row.getInt("user_id"), row.getString("user_name"), row.getString("user_bcity"));
     }
   }

   /**
   * Select a row from user table
   *
   * @param id user_id
   */
   public void selectUser(int id) {
      final String query = "SELECT * FROM uprofile.user where user_id = 3";
      Row row = session.execute(query).one();

      LOGGER.info("Obtained row: {} | {} | {} ", row.getInt("user_id"), row.getString("user_name"), row.getString("user_bcity"));
   }

   /**
   * Delete user table.
   */
   public void deleteTable() {
     final String query = "DROP TABLE IF EXISTS uprofile.user";
     session.execute(query);
   }
   ```

1. Open the `UserProfile.java` file under the folder `src\main\java\com\azure\cosmosdb\cassandra`. This class contains the main method that calls the `createKeyspace` and `createTable` insert data methods that you defined earlier. Append the following code that queries all users or a specific user:

   ```java
   LOGGER.info("Select all users");
   repository.selectAllUsers();

   LOGGER.info("Select a user by id (3)");
   repository.selectUser(3);

   LOGGER.info("Delete the users profile table");
   repository.deleteTable();
   ```

## Run the Java app

1. Open a command prompt or terminal window. Paste the following code block.

   This code changes the directory (cd) to the folder path where you created the project. Then, it runs the `mvn clean install` command to generate the `cosmosdb-cassandra-examples.jar` file within the target folder. Finally, it runs the Java application.

   ```bash
   cd "cassandra-demo"
   
   mvn clean install
   
   java -cp target/cosmosdb-cassandra-examples.jar com.azure.cosmosdb.cassandra.examples.UserProfile
   ```

1. Now, in the Azure portal, open **Data Explorer** and confirm that the user table is deleted.

## Clean up resources

When resources are no longer needed, you can delete the resource group, Azure Cosmos DB account, and all the related resources. To do so, select the resource group for the virtual machine, select **Delete**, and then confirm the name of the resource group to delete.

## Next step

In this tutorial, you learned how to query data from an API for Cassandra account in Azure Cosmos DB. You can now proceed to the next article:

> [!div class="nextstepaction"]
> [Migrate data to an API for Cassandra account](migrate-data.md)
