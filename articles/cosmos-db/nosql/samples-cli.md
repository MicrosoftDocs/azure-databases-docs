---
title: Azure CLI samples
titleSuffix: Azure Cosmos DB for NoSQL
description: Review several Azure CLI code samples available for interacting with Azure Cosmos DB for NoSQL.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: sample
ms.date: 04/08/2025
ms.custom: devx-track-azurecli, seo-azure-cli
appliesto:
  - ✅ NoSQL
---

# Azure CLI samples for Azure Cosmos DB for NoSQL

This guide includes links to sample Azure CLI scripts for the Azure Cosmos DB for NoSQL.

[!INCLUDE [azure-cli-prepare-your-environment](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

## Samples

| | Description |
| --- | --- |
| **[Add or fail over regions](https://github.com/azure-samples/azure-cli-samples/blob/master/cosmosdb/common/regions.sh)** | Add a region, change failover priority, trigger a manual failover. |
| **[Perform account key operations](https://github.com/azure-samples/azure-cli-samples/blob/master/cosmosdb/common/keys.sh)** | List account keys, read-only keys, regenerate keys and list connection strings. |
| **[Secure with IP firewall](https://github.com/azure-samples/azure-cli-samples/blob/master/cosmosdb/common/ipfirewall.sh)** | Create an Azure Cosmos DB account with IP firewall is configured. |
| **[Secure new account with service endpoints](../scripts/cli/common/service-endpoints.md)** | Create an Azure Cosmos DB account and secure with service-endpoints. |
| **[Secure existing account with service endpoints](../scripts/cli/common/service-endpoints-ignore-missing-vnet.md)** | Update an Azure Cosmos DB account to secure with service-endpoints when the subnet is eventually configured. |
| **[Find existing free-tier account](../scripts/cli/common/free-tier.md)** | Find whether there's an existing free-tier account in your subscription. |
| **[Create an Azure Cosmos DB account, database, and container](https://github.com/azure-samples/azure-cli-samples/blob/master/cosmosdb/sql/create.sh)** | Creates an Azure Cosmos DB account, database, and container for API for NoSQL. |
| **[Create a serverless Azure Cosmos DB account, database, and container](https://github.com/azure-samples/azure-cli-samples/blob/master/cosmosdb/sql/serverless.sh)** | Creates a serverless Azure Cosmos DB account, database, and container for API for NoSQL. |
| **[Create an Azure Cosmos DB account, database, and container with autoscale](https://github.com/azure-samples/azure-cli-samples/blob/master/cosmosdb/sql/autoscale.sh)** | Creates an Azure Cosmos DB account, database, and container with autoscale for API for NoSQL. |
| **[Perform throughput operations](https://github.com/azure-samples/azure-cli-samples/blob/master/cosmosdb/sql/throughput.sh)** | Read, update, and migrate between autoscale and standard throughput on a database and container.|
| **[Lock resources from deletion](https://github.com/azure-samples/azure-cli-samples/blob/master/cosmosdb/sql/lock.sh)** | Prevent resources from being deleted with  resource locks.|

## Next step

  > [!div class="nextstepaction"]
  > [Azure CLI Reference](/cli/azure/cosmosdb)
