---
title: Connect Using MongoDB Shell
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: Learn how to connect to an Azure Cosmos DB for MongoDB (vCore) cluster using MongoDB Shell to query data. Follow this guide for step-by-step instructions.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 09/18/2025
ms.custom:
  - sfi-image-nochange
  - sfi-ropc-nochange
---

# Connect to Azure Cosmos DB for MongoDB (vCore) using MongoDB Shell

[!INCLUDE[MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

MongoDB Shell (`mongosh`) is a JavaScript and Node.js environment for interacting with MongoDB deployments. It's a popular community tool to test queries and interact with the data in your Azure Cosmos DB for MongoDB (vCore) cluster. This article explains how to connect to an Azure Cosmos DB for MongoDB (vCore) cluster using MongoDB Shell.

## Prerequisites

- An existing Azure Cosmos DB for MongoDB (vCore) cluster.

- MongoDB Shell. For more information, see [install MongoDB shell](https://www.mongodb.com/try/download/shell)

- Firewall rules that allow your client to connect to the cluster. For more information, see [configure firewall](how-to-configure-firewall.md).
  
## Get cluster credentials

Get the connection string you need to connect to this cluster.

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Navigate to the Azure Cosmos DB for MongoDB (vCore) cluster.

1. Select the **Connection strings** navigation menu option.

1. Copy or record the value from the **Connection string** field.

   :::image type="content" source="media/how-to-connect-mongo-shell/cluster-connection-string.png" alt-text="Screenshot of the connection strings option on the page for a cluster.":::

## Connect with interactive password authentication

Connect to your cluster by using the MongoDB Shell with a connection string that doesn't include a password. Use the interactive password prompt to enter your password as part of the connection steps.

1. Open a terminal.

1. Connect by entering the password in the Mongo Shell prompt. For this step, use a connection string without the password.

     ```shell
     mongosh "mongodb+srv://<username>@<cluster-name>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
     ```

1. After you provide the password and are successfully authenticated, observe the warning that appears

    ```output
    This server or service appears to be an emulation of MongoDB.
    ```

    > [!TIP]
    > You can safely ignore this warning. This warning is generated because the connection string contains `cosmos.azure`. Azure Cosmos DB for MongoDB (vCore) is a native Azure platform as a service (PaaS) offering.

1. **Exit** the shell context.

## Connect with connection string and password

Now, connect to your cluster from the MongoDB Shell with a connection string and parameters that includes a password.

1. Connect by using a connection string and the `--username` and `--password` arguments.

     ```shell
     mongosh "mongodb+srv://<cluster-name>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000" --username "<username>" -password "<password>"
     ```

1. After you provide the password and are successfully authenticated, observe the warning that appears

    ```output
    This server or service appears to be an emulation of MongoDB.
    ```

    > [!TIP]
    > You can safely ignore this warning. This warning is generated because the connection string contains `cosmos.azure`. Azure Cosmos DB for MongoDB (vCore) is a native Azure platform as a service (PaaS) offering.

## Perform test queries

Verify that you're successfully connected to your cluster by performing a series of test commands and queries.

1. Check your connection status by running the `connectionStatus` command.

    ```mongo
    db.runCommand({connectionStatus: 1})
    ```

1. List the databases in your cluster.

    ```mongo
    show dbs
    ```

1. Switch to a specific database. Replace the `<database-name>` placeholder with the name of any database in your cluster.

    ```mongo
    use <database-name>
    ```

    > [!TIP]
    > For example, if the database name is `inventory`, then the command would be `use inventory`.

1. List the collections within the database.

    ```mongo
    show collections
    ```

1. Find five items within a specific collection. Replace the `<collection-name>` placeholder with the name of any collection in your cluster.

    ```mongo
    db.<collection-name>
    ```

    > [!TIP]
    > For example, if the collection name is `equipment`, then the command would be `db.equipment.find().limit(5)`.

## Related content

- [Connect using Azure Cloud Shell](how-to-connect-cloud-shell.md)
- [Configure firewall](how-to-configure-firewall.md)
- [Migration options](migration-options.md)
