---
title: Troubleshoot conflict exceptions
titleSuffix: Azure Cosmos DB for NoSQL
description: Diagnose and fix various causes for conflict exceptions that can occur when working with Azure Cosmos DB for NoSQL.
author: gauravsaini-ms
ms.author: gauravsaini
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: troubleshooting
ms.date: 02/18/2025
---

# Diagnose and troubleshoot Azure Cosmos DB conflict exceptions

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

The HTTP status code 409 represents the request had a conflict while processing.

## Partition Key Collision

Azure Cosmos DB uses hash-based partitioning scheme to achieve horizontal scaling of data. All Azure Cosmos DB containers created before May 3, 2019 use a hash function that computes hash based on the first 101 bytes of the partition key. If there are multiple partition keys that have the same first 101 bytes, then those logical partitions are considered as the same logical partition by the service, which creates a partition key collision. This can lead to issues like partition key collisions, partition size quota being incorrect, unique indexes being incorrectly applied across the partition keys, and uneven distribution of storage. Large partition keys are introduced to solve this issue. Azure Cosmos DB now supports large partition keys with values up to 2 KB.
 
Large partition keys are supported by enabling an enhanced version of the hash function, which can generate a unique hash from large partition keys up to 2 KB. 

### Solution

Use large partition key. Enabling large partition keys can only be done at time of container creation. If you have an existing container that does not use large partition keys, you will have to create a new container and [migrate your data](../../container-copy.md) to it.

## Related content

- [IP Firewall](../how-to-configure-firewall.md).
- [Virtual networks](../how-to-configure-vnet-service-endpoint.md).
- [Private endpoints](../how-to-configure-private-endpoints.md).