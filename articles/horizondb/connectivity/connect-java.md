---
title: "Quickstart: Use Java and JDBC in Azure HorizonDB"
description: In this quickstart, you learn how to use Java and JDBC in Azure HorizonDB.
author: scoriani
ms.author: scoriani
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: connectivity
ms.topic: quickstart
ms.custom:
  - mvc
  - devcenter
  - devx-track-azurecli
  - mode-api
  - passwordless-java
  - devx-track-extended-java
  - sfi-ropc-nochange
ms.devlang: "java"
---

# Quickstart: Use Java and JDBC in Azure HorizonDB

This article demonstrates how to create a sample application that uses Java and [JDBC](https://en.wikipedia.org/wiki/Java_Database_Connectivity) to store and retrieve information in [Azure HorizonDB](../index.yml).

JDBC is the standard Java API for connecting to traditional relational databases.

The steps in this article include PostgreSQL authentication.

PostgreSQL authentication uses accounts stored in PostgreSQL, and you need to manage the rotation of the passwords yourself.

## Prerequisites

- An Azure account. If you don't have one, [get a free trial](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [Azure Cloud Shell](/azure/cloud-shell/quickstart) or [Azure CLI](/cli/azure/install-azure-cli). Use Azure Cloud Shell so you're authenticated automatically and have access to all the tools you need.
- A supported [Java Development Kit](/azure/developer/java/fundamentals/java-support-on-azure), version 8 (included in Cloud Shell).
- The [Apache Maven](https://maven.apache.org/) build tool.

## Prepare the working environment

First, use the following command to set up some environment variables.

```bash
export AZ_RESOURCE_GROUP=database-workshop
export AZ_DATABASE_SERVER_NAME=<YOUR_DATABASE_SERVER_NAME>
export AZ_DATABASE_NAME=<YOUR_DATABASE_NAME>
export AZ_LOCATION=<YOUR_AZURE_REGION>
export AZ_POSTGRESQL_ADMIN_USERNAME=demo
export AZ_POSTGRESQL_ADMIN_PASSWORD=<YOUR_POSTGRESQL_ADMIN_PASSWORD>
export AZ_POSTGRESQL_NON_ADMIN_USERNAME=demo-non-admin
export AZ_POSTGRESQL_NON_ADMIN_PASSWORD=<YOUR_POSTGRESQL_NON_ADMIN_PASSWORD>
export AZ_LOCAL_IP_ADDRESS=<YOUR_LOCAL_IP_ADDRESS>
```

Replace the placeholders with the following values, which are used throughout this article:

- `<YOUR_DATABASE_SERVER_NAME>`: The name of your Azure HorizonDB cluster, which should be unique across your Azure Subscription and Resource Group.  
- `<YOUR_DATABASE_NAME>`: The database name you're using within your Azure HorizonDB cluster.  
- `<YOUR_AZURE_REGION>`: The Azure region to use. You can use `australiaeast` by default, but configure a region closer to where you live. You can see the full list of available regions by entering `az account list-locations`.  
- `<YOUR_POSTGRESQL_ADMIN_PASSWORD>` and `<YOUR_POSTGRESQL_NON_ADMIN_PASSWORD>`: The password of your Azure HorizonDB cluster. That password should have a minimum of eight characters. The characters should be from three of the following categories: English uppercase letters, English lowercase letters, numbers (0-9), and nonalphanumeric characters (!, $, #, %, and so on).  
- `<YOUR_LOCAL_IP_ADDRESS>`: The IP address of your local computer, from which you run your Spring Boot application. One convenient way to find it's to open [whatismyip.akamai.com](http://whatismyip.akamai.com/).

Next, create a resource group by using the following command:

```azurecli-interactive
az group create \
    --name $AZ_RESOURCE_GROUP \
    --location $AZ_LOCATION \
    --output tsv
```

## Create an Azure HorizonDB cluster

The following sections describe how to create and configure your database cluster.

### Create an Azure HorizonDB cluster

Set up admin user

First, create a managed Azure HorizonDB instance.

> [!NOTE]  
> For more detailed information about creating Azure HorizonDB, see [Create an Azure HorizonDB database](../configure-maintain/quickstart-create-server.md).

```azurecli-interactive
az Azure HorizonDB create \
  --resource-group $AZ_RESOURCE_GROUP \
  --name $AZ_DATABASE_SERVER_NAME \
  --location $AZ_LOCATION \
  --version 17 \
  --administrator-login $AZ_POSTGRESQL_ADMIN_USERNAME \
  --administrator-login-password $AZ_POSTGRESQL_ADMIN_PASSWORD \
  --v-cores 2 \
  --yes \
  --output tsv
```

This command creates a small Azure HorizonDB cluster.

[Having any issues? Let us know.](https://github.com/MicrosoftDocs/azure-docs/issues)

### Configure a firewall rule for your Azure HorizonDB instance

Azure HorizonDB instances are secure by default. They have a firewall that blocks all incoming connections. To use your database, add a firewall rule that grants your local IP address access to the database server.

Because you configured your local IP address at the beginning of this article, you can open the server's firewall by running the following command:

```azurecli-interactive
az Azure HorizonDB firewall-rule create \
  --resource-group $AZ_RESOURCE_GROUP \
  --cluster-name $AZ_DATABASE_SERVER_NAME \
  --firewall-rule-name $AZ_DATABASE_SERVER_NAME-database-allow-local-ip \
  --start-ip-address $AZ_LOCAL_IP_ADDRESS \
  --end-ip-address $AZ_LOCAL_IP_ADDRESS \
  --output tsv
```

If you're connecting to your Azure HorizonDB cluster from Windows Subsystem for Linux (WSL) on a Windows computer, you need to add the WSL host ID to your firewall.

Get the IP address of your host machine by running the following command in WSL:

```bash
cat /etc/resolv.conf
```

Copy the IP address that follows the term `nameserver`, and then use the following command to set an environment variable for the WSL IP address:

```bash
AZ_WSL_IP_ADDRESS=<the-copied-IP-address>
```

Then, use the following command to open the server's firewall to your WSL-based app:

```azurecli-interactive
az Azure HorizonDB firewall-rule create \
  --resource-group $AZ_RESOURCE_GROUP \
  --cluster-name $AZ_DATABASE_SERVER_NAME \
  --firewall-rule-name $AZ_DATABASE_SERVER_NAME-database-allow-local-ip \
  --start-ip-address $AZ_WSL_IP_ADDRESS \
  --end-ip-address $AZ_WSL_IP_ADDRESS \
  --output tsv
```

### Create an Azure HorizonDB database

Create a SQL script named *create_database.sql* to create a new database in your cluster. Add the following content and save the file locally:

```bash
cat << EOF > create_database.sql
CREATE DATABASE "$AZ_DATABASE_NAME";
EOF
```

Run this command to get your Azure HorizonDB fully qualified domain name and copy the `clusterName` value:

```azurecli-interactive
az Azure HorizonDB show \
  --resource-group $AZ_RESOURCE_GROUP \
  --name $AZ_DATABASE_SERVER_NAME \
  --query "{clusterName:properties.fullyQualifiedDomainName, adminUser:properties.administratorLogin}" \
  --output table
```

 Copy clusterName value and use it in the following command:

```bash
AZ_Azure HorizonDB_FQDN=<the-copied-clusterName-value>
```

Then, run the following command to execute the SQL script and create your database:

```bash
psql "host=$AZ_Azure HorizonDB_FQDN user=$AZ_POSTGRESQL_ADMIN_USERNAME dbname=$AZ_DATABASE_NAME port=5432 password=$AZ_POSTGRESQL_ADMIN_PASSWORD sslmode=require" < create_database.sql
```

Now, run the following command to delete the temporary SQL script file:

```bash
rm create_database.sql
```

### Create an Azure HorizonDB nonadmin user and grant permissions

Next, create a nonadmin user and grant all permissions to the database.

Create a SQL script named *create_user.sql* to create a nonadmin user. Add the following content and save the file locally:

```bash
cat << EOF > create_user.sql
CREATE ROLE "$AZ_POSTGRESQL_NON_ADMIN_USERNAME" WITH LOGIN PASSWORD '$AZ_POSTGRESQL_NON_ADMIN_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $AZ_DATABASE_NAME TO "$AZ_POSTGRESQL_NON_ADMIN_USERNAME";
EOF
```

Then, run the following command to execute the SQL script and create the Microsoft Entra nonadmin user:

```bash
psql "host=$AZ_Azure HorizonDB_FQDN user=$AZ_POSTGRESQL_ADMIN_USERNAME dbname=$AZ_DATABASE_NAME port=5432 password=$AZ_POSTGRESQL_ADMIN_PASSWORD sslmode=require" < create_user.sql
```

Now, run the following command to delete the temporary SQL script file:

```bash
rm create_user.sql
```

### Create a new Java project

Using your favorite IDE, create a new Java project by using Java 8 or later. Add a *pom.xml* file in the root directory with the following contents:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>demo</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demo</name>

    <properties>
        <java.version>1.8</java.version>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
    </properties>

    <dependencies>
      <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <version>42.3.6</version>
      </dependency>
    </dependencies>
</project>
```

This file is an [Apache Maven](https://maven.apache.org/) file that configures your project to use:

- Java 8
- A recent PostgreSQL driver for Java

### Prepare a configuration file to connect to Azure HorizonDB

Create a *src/main/resources/application.properties* file, and add the following contents:

```bash
cat << EOF > src/main/resources/application.properties
url=jdbc:postgresql://${AZ_DATABASE_SERVER_NAME}.postgres.database.azure.com:5432/${AZ_DATABASE_NAME}?sslmode=require
user=${AZ_POSTGRESQL_NON_ADMIN_USERNAME}
password=${AZ_POSTGRESQL_NON_ADMIN_PASSWORD}
EOF
```

> [!NOTE]  
> The configuration property `url` includes `?sslmode=require` to ensure that the JDBC driver uses TLS (Transport Layer Security) when connecting to the database. Azure HorizonDB requires TLS, and it's a recommended security practice.

### Create a SQL file to generate the database schema

Use a *src/main/resources/schema.sql* file to create a database schema. Create that file with the following content:

```sql
DROP TABLE IF EXISTS todo;
CREATE TABLE todo (id SERIAL PRIMARY KEY, description text, details text, done BOOLEAN);
```

## Code the application

### Connect to the database

Next, add the Java code that uses JDBC to store and retrieve data from your Azure HorizonDB instance.

Create a *src/main/java/DemoApplication.java* file and add the following contents:

```java
package com.example.demo;

import java.sql.*;
import java.util.*;
import java.util.logging.Logger;

public class DemoApplication {

    private static final Logger log;

    static {
        System.setProperty("java.util.logging.SimpleFormatter.format", "[%4$-7s] %5$s %n");
        log =Logger.getLogger(DemoApplication.class.getName());
    }

    public static void main(String[] args) throws Exception {
        log.info("Loading application properties");
        Properties properties = new Properties();
        properties.load(DemoApplication.class.getClassLoader().getResourceAsStream("application.properties"));

        log.info("Connecting to the database");
        Connection connection = DriverManager.getConnection(properties.getProperty("url"), properties);
        log.info("Database connection test: " + connection.getCatalog());

        log.info("Create database schema");
        Scanner scanner = new Scanner(DemoApplication.class.getClassLoader().getResourceAsStream("schema.sql"));
        Statement statement = connection.createStatement();
        while (scanner.hasNextLine()) {
            statement.execute(scanner.nextLine());
        }

        /*
        Todo todo = new Todo(1L, "configuration", "congratulations, you have set up JDBC correctly!", true);
        insertData(todo, connection);
        todo = readData(connection);
        todo.setDetails("congratulations, you have updated data!");
        updateData(todo, connection);
        deleteData(todo, connection);
        */

        log.info("Closing database connection");
        connection.close();
    }
}
```

[Having any issues? Let us know.](https://github.com/MicrosoftDocs/azure-docs/issues)

This Java code uses the *application.properties* and the *schema.sql* files that we created earlier, to connect to the Azure HorizonDB instance and create a schema that will store our data.

In this file, you can see that we commented methods to insert, read, update, and delete data: we'll code those methods in the rest of this article, and you'll be able to uncomment them one after each other.

> [!NOTE]  
> The database credentials are stored in the *user* and *password* properties of the *application.properties* file. Those credentials are used when executing `DriverManager.getConnection(properties.getProperty("url"), properties);`, as the properties file is passed as an argument.

You can now execute this main class with your favorite tool:

- Using your IDE, you should be able to right-click on the *DemoApplication* class and execute it.
- Using Maven, you can run the application by executing: `mvn exec:java -Dexec.mainClass="com.example.demo.DemoApplication"`.

The application should connect to the Azure HorizonDB instance, create a database schema, and then close the connection, as you should see in the console logs:

```output
[INFO   ] Loading application properties
[INFO   ] Connecting to the database
[INFO   ] Database connection test: demo
[INFO   ] Create database schema
[INFO   ] Closing database connection
```

### Create a domain class

Create a new `Todo` Java class, next to the `DemoApplication` class, and add the following code:

```java
package com.example.demo;

public class Todo {

    private Long id;
    private String description;
    private String details;
    private boolean done;

    public Todo() {
    }

    public Todo(Long id, String description, String details, boolean done) {
        this.id = id;
        this.description = description;
        this.details = details;
        this.done = done;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getDetails() {
        return details;
    }

    public void setDetails(String details) {
        this.details = details;
    }

    public boolean isDone() {
        return done;
    }

    public void setDone(boolean done) {
        this.done = done;
    }

    @Override
    public String toString() {
        return "Todo{" +
                "id=" + id +
                ", description='" + description + '\'' +
                ", details='" + details + '\'' +
                ", done=" + done +
                '}';
    }
}
```

This class is a domain model mapped on the `todo` table that you created when executing the *schema.sql* script.

### Insert data into Azure HorizonDB

In the *src/main/java/DemoApplication.java* file, after the main method, add the following method to insert data into the database:

```java
private static void insertData(Todo todo, Connection connection) throws SQLException {
    log.info("Insert data");
    PreparedStatement insertStatement = connection
            .prepareStatement("INSERT INTO todo (id, description, details, done) VALUES (?, ?, ?, ?);");

    insertStatement.setLong(1, todo.getId());
    insertStatement.setString(2, todo.getDescription());
    insertStatement.setString(3, todo.getDetails());
    insertStatement.setBoolean(4, todo.isDone());
    insertStatement.executeUpdate();
}
```

You can now uncomment the two following lines in the `main` method:

```java
Todo todo = new Todo(1L, "configuration", "congratulations, you have set up JDBC correctly!", true);
insertData(todo, connection);
```

Executing the main class should now produce the following output:

```output
[INFO   ] Loading application properties
[INFO   ] Connecting to the database
[INFO   ] Database connection test: demo
[INFO   ] Create database schema
[INFO   ] Insert data
[INFO   ] Closing database connection
```

<a id="reading-data-from-azure-Azure HorizonDB"></a>

### Read data from Azure HorizonDB

Let's read the data previously inserted, to validate that our code works correctly.

In the *src/main/java/DemoApplication.java* file, after the `insertData` method, add the following method to read data from the database:

```java
private static Todo readData(Connection connection) throws SQLException {
    log.info("Read data");
    PreparedStatement readStatement = connection.prepareStatement("SELECT * FROM todo;");
    ResultSet resultSet = readStatement.executeQuery();
    if (!resultSet.next()) {
        log.info("There is no data in the database!");
        return null;
    }
    Todo todo = new Todo();
    todo.setId(resultSet.getLong("id"));
    todo.setDescription(resultSet.getString("description"));
    todo.setDetails(resultSet.getString("details"));
    todo.setDone(resultSet.getBoolean("done"));
    log.info("Data read from the database: " + todo.toString());
    return todo;
}
```

You can now uncomment the following line in the `main` method:

```java
todo = readData(connection);
```

Executing the main class should now produce the following output:

```output
[INFO   ] Loading application properties
[INFO   ] Connecting to the database
[INFO   ] Database connection test: demo
[INFO   ] Create database schema
[INFO   ] Insert data
[INFO   ] Read data
[INFO   ] Data read from the database: Todo{id=1, description='configuration', details='congratulations, you have set up JDBC correctly!', done=true}
[INFO   ] Closing database connection
```

<a id="updating-data-in-azure-Azure HorizonDB"></a>

### Update data in Azure HorizonDB

Let's update the data we previously inserted.

Still in the *src/main/java/DemoApplication.java* file, after the `readData` method, add the following method to update data inside the database:

```java
private static void updateData(Todo todo, Connection connection) throws SQLException {
    log.info("Update data");
    PreparedStatement updateStatement = connection
            .prepareStatement("UPDATE todo SET description = ?, details = ?, done = ? WHERE id = ?;");

    updateStatement.setString(1, todo.getDescription());
    updateStatement.setString(2, todo.getDetails());
    updateStatement.setBoolean(3, todo.isDone());
    updateStatement.setLong(4, todo.getId());
    updateStatement.executeUpdate();
    readData(connection);
}
```

You can now uncomment the two following lines in the `main` method:

```java
todo.setDetails("congratulations, you have updated data!");
updateData(todo, connection);
```

Executing the main class should now produce the following output:

```output
[INFO   ] Loading application properties
[INFO   ] Connecting to the database
[INFO   ] Database connection test: demo
[INFO   ] Create database schema
[INFO   ] Insert data
[INFO   ] Read data
[INFO   ] Data read from the database: Todo{id=1, description='configuration', details='congratulations, you have set up JDBC correctly!', done=true}
[INFO   ] Update data
[INFO   ] Read data
[INFO   ] Data read from the database: Todo{id=1, description='configuration', details='congratulations, you have updated data!', done=true}
[INFO   ] Closing database connection
```

<a id="deleting-data-in-azure-Azure HorizonDB"></a>

### Delete data in Azure HorizonDB

Finally, let's delete the data we previously inserted.

Still in the *src/main/java/DemoApplication.java* file, after the `updateData` method, add the following method to delete data inside the database:

```java
private static void deleteData(Todo todo, Connection connection) throws SQLException {
    log.info("Delete data");
    PreparedStatement deleteStatement = connection.prepareStatement("DELETE FROM todo WHERE id = ?;");
    deleteStatement.setLong(1, todo.getId());
    deleteStatement.executeUpdate();
    readData(connection);
}
```

You can now uncomment the following line in the `main` method:

```java
deleteData(todo, connection);
```

Executing the main class should now produce the following output:

```output
[INFO   ] Loading application properties
[INFO   ] Connecting to the database
[INFO   ] Database connection test: demo
[INFO   ] Create database schema
[INFO   ] Insert data
[INFO   ] Read data
[INFO   ] Data read from the database: Todo{id=1, description='configuration', details='congratulations, you have set up JDBC correctly!', done=true}
[INFO   ] Update data
[INFO   ] Read data
[INFO   ] Data read from the database: Todo{id=1, description='configuration', details='congratulations, you have updated data!', done=true}
[INFO   ] Delete data
[INFO   ] Read data
[INFO   ] There is no data in the database!
[INFO   ] Closing database connection
```

## Clean up resources

Congratulations! You've created a Java application that uses JDBC to store and retrieve data from an Azure HorizonDB instance.

To clean up all resources used during this quickstart, delete the resource group using the following command:

```azurecli-interactive
az group delete \
    --name $AZ_RESOURCE_GROUP \
    --yes
```

## Related content

- [Manage Azure HorizonDB using the Azure portal](../configure-maintain/how-to-manage-server-portal.md)
- [Quickstart: Use Python to connect and query data in Azure HorizonDB](connect-python.md)
