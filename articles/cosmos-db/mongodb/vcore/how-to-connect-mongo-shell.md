---
title: Connect Using MongoDB Shell
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: Learn how to connect to an Azure Cosmos DB for MongoDB (vCore) cluster using MongoDB Shell to query data. Follow this guide for step-by-step instructions.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 09/19/2025
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

[!INCLUDE[Section - Connect cluster credentials](includes/section-connect-cluster-credentials.md)]

## Connect with interactive password authentication

Connect to your cluster by using the MongoDB Shell with a connection string that doesn't include a password. Use the interactive password prompt to enter your password as part of the connection steps.

1. Open a terminal.

1. Connect by entering the password in the MongoDB Shell prompt. For this step, use a connection string without the password.

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
    ------
       Warning: Non-Genuine MongoDB Detected
       This server or service appears to be an emulation of MongoDB rather than an official MongoDB product.
    ------
    ```

    > [!TIP]
    > You can safely ignore this warning. This warning is generated because the connection string contains `cosmos.azure`. Azure Cosmos DB for MongoDB (vCore) is a native Azure platform as a service (PaaS) offering.

## Perform test queries

[!INCLUDE[Section - Connect test queries](includes/section-connect-test-queries.md)]

## Related content

- [Connect using Azure Cloud Shell](how-to-connect-cloud-shell.md)
- [Configure firewall](how-to-configure-firewall.md)
- [Migration options](migration-options.md)
