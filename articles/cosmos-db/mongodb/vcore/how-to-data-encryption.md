---
title: Configure encryption at rest with customer-managed key in Azure Cosmos DB for MongoDB vCore
description: Learn how to configure encryption of data in Azure Cosmos DB for MongoDB vCore databases using service-managed and customer-managed encryption keys.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 07/13/2025
appliesto:
  - ✅ MongoDB (vCore)
---

# Configure customer-managed key for data encryption at rest for an Azure Cosmos DB for MongoDB vCore cluster

[!INCLUDE[MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/notice-cmk-preview.md)]

In this article, you learn how to configure [customer-managed key (CMK)](./database-encryption-at-rest.md) for data encryption at rest in Azure Cosmos DB for MongoDB vCore. The steps in this guide configure a new Azure Cosmos DB for MongoDB vCore cluster with customer-managed key stored in an Azure Key Vault and user-assigned managed identity. 

## Prerequisites

[!INCLUDE[Prerequisite - Azure subscription](includes/prereq-azure-subscription.md)]

[!INCLUDE[Prerequisite - Azure CLI](includes/prereq-azure-cli.md)]


## Related content

- [Learn about data encryption at rest in Azure Cosmos DB for MongoDB vCore](./database-encryption-at-rest.md)
- [Migrate data to Azure Cosmos DB for MongoDB vCore](./migration-options.md)