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
---

# Quickstart: Azure Cosmos DB for Apache Cassandra client library for Java

[!INCLUDE[Quickstart developer selector](includes/selector-quickstart-developer.md)]

Get started with the Azure Cosmos DB for Apache Cassandra client library for Java to store, manage, and query unstructured data. Follow the steps in this guide to create a new account, install a Java client library, connect to the account, perform common operations, and query your final sample data.

[API reference documentation]() | [Library source code]() | [Package (Maven)]()

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

1. Start in an empty folder.

1. Generate a new Java console project.

    ```bash
     
    ```

1. Import the `` package from Maven.

    ```bash
     
    ```

1. Open the **** file.

1. Observe the existing Java application boilerplate.

    ```java
    
    ```

    > [!IMPORTANT]
    > The remaining steps within this guide assume that you're adding your code within the `main` method.

## Object model

| | Description |
| --- | --- |
| **``** | |
| **``** | |

## Code examples

- [Authenticate client](#authenticate-client)
- [Upsert data](#upsert-data)
- [Read data](#read-data)
- [Query data](#query-data)

### Authenticate client

Start by authenticating the client using the credentials gathered earlier in this guide.

1. Open the **** file in your integrated development environment (IDE).

1. Import `` and `` from the `` module.

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

1. TODO

    ```java
    
    ```

### Upsert data

Next, upsert new data into a table. Upserting ensures that the data is created or replaced appropriately depending on whether the same data already exists in the table.

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

1. TODO

    ```java
    
    ```

### Read data

Then, read data that was previously upserted into the table.

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

1. TODO

    ```java
    
    ```

### Query data

Finally, use a query to find all data that matches a specific filter in the table.

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

1. TODO

    ```java
    
    ```

## Run the code

Run the newly created application using a terminal in your application directory.

```bash

```

## Clean up resources

[!INCLUDE[Section - Quickstart cleanup](includes/section-quickstart-credentials.md)]

## Next step

> [!div class="nextstepaction"]
> [Overview of Azure Cosmos DB for Apache Cassandra](introduction.md)
