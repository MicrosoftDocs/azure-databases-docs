---
title: Configure Firewall
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: Learn how to connect to an Azure Cosmos DB for MongoDB (vCore) cluster using Azure Cloud Shell to query data. Follow this guide for step-by-step instructions.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 09/18/2025
ms.custom:
  - sfi-image-nochange
  - sfi-ropc-nochange
ai-usage: ai-generated
---

# Configure firewall for Azure Cosmos DB for MongoDB (vCore)

Azure Cosmos DB for MongoDB (vCore) allows you to configure firewall settings to secure database access. This article explains how to grant access from specific IP addresses, Azure services, or IP ranges to ensure secure connectivity.

## Prerequisites

- An existing Azure Cosmos DB for MongoDB (vCore) cluster.

## Grant access from your IP address

To allow access to your Azure Cosmos DB account from your current IP address, you need to configure the firewall settings. This configuration ensures that only your current IP address can interact with the database securely.

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Navigate to the Azure Cosmos DB for MongoDB (vCore) cluster.

1. Select **Networking** from the navigation menu.

1. On the **Networking** page, select the **Add current client IP address** option to automatically add your current IP address to the allowed list.

1. Select **Save** to apply the changes.

## Grant access from Azure services

Azure services can be granted access to your Azure Cosmos DB account by enabling specific settings. This configuration allows services like Azure Functions or Stream Analytics to interact with your database seamlessly.

1. In the **Networking** section of your cluster, locate the **Allow public access from Azure resources and services** option.

1. Toggle the switch to enable access for Azure services.

1. **Save** the changes to ensure Azure services can connect to your account.

## Grant access to specific IP address ranges

You can configure the firewall to allow access from specific IP address ranges. This option is useful for granting access to multiple machines or services within a defined network.

1. Go to the **Networking** section in the Azure portal for your Azure Cosmos DB account.

1. Under **Firewall and virtual networks**, add the desired IP ranges in Classless Inter-Domain Routing (CIDR) format (for example, `192.168.1.0/24`).

1. Optionally, select the **Add 0.0.0.0 - 255.255.255.255** option to 

    > [!WARNING]
    > This option configures the firewall to allow all requests from Azure, including requests from the subscriptions of other customers deployed in Azure. The list of IPs allowed by this option is wide, so it limits the effectiveness of a firewall policy. Use this option with caution.

1. Confirm the entries and then select **Save** to update the firewall rules.

## Related content

- [Connect using MongoDB shell](how-to-connect-mongo-shell.md)
- [Connect using Azure Cloud Shell](how-to-connect-cloud-shell.md)
