---
title: Connect Using Azure Cloud Shell
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: Connect to an Azure Cosmos DB for MongoDB (vCore) cluster by using Azure Cloud Shell to query data.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 09/25/2025
ms.custom:
  - sfi-image-nochange
  - sfi-ropc-nochange
---

# Connect to Azure Cosmos DB for MongoDB (vCore) using Azure portal

[!INCLUDE[MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

MongoDB Shell (`mongosh`) is a JavaScript and Node.js environment for interacting with MongoDB deployments. It's a popular community tool to test queries and interact with the data in your Azure Cosmos DB for MongoDB (vCore) cluster. The Azure portal contains multiple tools to query MongoDB data including the Azure Cloud Shell. Azure Cloud Shell is an interactive, authenticated, browser-accessible terminal for managing Azure resources. This article explains how to connect to an Azure Cosmos DB for MongoDB (vCore) cluster using MongoDB Shell within Azure Cloud Shell.

## Prerequisites

- An existing Azure Cosmos DB for MongoDB (vCore) cluster.

- Firewall rules that allow clients within your networks to connect to the cluster. For more information, see [configure firewall](how-to-configure-firewall.md).

- (*Optional*) These prerequisites are only required if you're using Azure Cloud Shell within a virtual network that's the same or peered with Azure Cosmos DB for MongoDB vCore.

  - One or more existing Azure Virtual Networks with subnets for Azure Cloud Shell and Azure Cosmos DB for MongoDB vCore deployment.
  
  - A private endpoint for the Azure Cosmos DB for MongoDB (vCore) cluster. For more information, see [configure private link](how-to-private-link.md).
  
  - Azure Cloud Shell deployed to the same or a peered virtual network with connectivity to the Azure Cosmos DB for MongoDB (vCore) private endpoint. For more information, see [deploy Cloud Shell to virtual network](/azure/cloud-shell/vnet/deployment).

## Enable access to your cluster from Azure Cloud Shell

First, ensure that Azure Cloud Shell can access your Azure Cosmos DB for MongoDB (vCore) cluster by allowing its IP addresses in the firewall.

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Navigate to the Azure Cosmos DB for MongoDB (vCore) cluster.

1. Select **Networking** from the navigation menu.

1. On the **Networking** page within the **Public access** section, select the **+ Add Azure Cloud Shell IPs** option to automatically add your current IP address to the allowed list.

1. Select **Save** to apply the changes.

[!INCLUDE[Note - Connectivity IP Addresses](includes/note-connectivity-ip-addresses.md)]

## Connect using Azure Cloud Shell from Quick Start

Now, use the Quick Start experience in the resource's page on the Azure portal to connect directly to Azure Cosmos DB for MongoDB (vCore) using MongoDB Shell.

1. In the cluster resource page, select **Quick start (preview)** from the navigation menu.

1. Then, select **Open MongoDB (vCore) shell**.

1. Wait for the MongoDB Shell environment to start.

1. Once the environment is ready, enter **Y** to accept the notice.

    > [!NOTE]
    > If you're experiencing an issue connecting using MongoDB Shell after accepting the notice, make sure Azure Cloud Shell has access to your cluster. For more information, see [enable access to your cluster](#enable-access-to-your-cluster-from-azure-cloud-shell).

1. Now, enter your password to connect your cluster to Cloud Shell.

## Get cluster credentials

[!INCLUDE[Section - Connect cluster credentials](includes/section-connect-cluster-credentials.md)]

## Configure MongoDB Shell in Azure Cloud Shell manually

Install the MongoDB Shell (`mongosh`) client to your Azure Cloud Shell instance using Node Package Manager (npm).

1. Open the Azure Cloud Shell configured with a Bash scripting environment.

1. Install version **1** of the MongoDB Shell locally in your user directory.

    ```azurecli-interactive
    npm install mongosh@1
    ```

1. Wait for the installation to complete.

1. Verify that the installation was successful by getting the version of the `mongosh` tool.

    ```azurecli-interactive
    npx mongosh --version
    ```

## Connect to the cluster

Connect to your cluster by using the MongoDB Shell with a connection string that doesn't include a password. Use the interactive password prompt to enter your password as part of the connection steps.

1. Connect by entering the password in the MongoDB Shell prompt. For this step, use a connection string without the password.

    ```azurecli-interactive
    npx mongosh "mongodb+srv://<username>@<cluster-name>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
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

- [Connect using MongoDB shell](how-to-connect-mongo-shell.md)
- [Configure firewall](how-to-configure-firewall.md)
- [Migration options](migration-options.md)
