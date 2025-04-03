---
title: Troubleshoot service request time out exceptions
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to diagnose and fix Azure Cosmos DB for NoSQL service request time out exceptions.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: troubleshooting
ms.date: 04/03/2025
appliesto:
  - ✅ NoSQL
---

# Diagnose and troubleshoot Azure Cosmos DB for NoSQL request time out exceptions

Azure Cosmos DB for NoSQL returned an HTTP 408 request time out.

## Troubleshooting steps

The following list contains known causes and solutions for request time out exceptions.

### Check the service level agreement (SLA)

Check [Azure Cosmos DB for NoSQL monitoring](../monitor.md) to see if the number of 408 exceptions violates the Azure Cosmos DB for NoSQL SLA.

#### Solution 1: It didn't violate the Azure Cosmos DB for NoSQL SLA

The application should handle this scenario and retry on these transient failures.

#### Solution 2: It did violate the Azure Cosmos DB for NoSQL SLA

Contact [Azure Support](https://aka.ms/azure-support).
 
### Hot partition key

Azure Cosmos DB for NoSQL distributes the overall provisioned throughput evenly across physical partitions. When there's a hot partition, one or more logical partition keys on a physical partition are consuming all the physical partition's Request Units per second (RU/s). At the same time, the RU/s on other physical partitions are going unused. As a symptom, the total RU/s consumed are less than the overall provisioned RU/s at the database or container. You could still see throttling (429 errors) on the requests against the hot logical partition key. Use the [Normalized RU Consumption metric](../monitor-normalized-request-units.md) to see if the workload is encountering a hot partition. 

#### Solution

Choose a good partition key that evenly distributes request volume and storage. Learn how to [change your partition key](https://devblogs.microsoft.com/cosmosdb/how-to-change-your-partition-key/).

## Related content

- [Diagnose and troubleshoot](troubleshoot-dotnet-sdk.md) issues when you use the Azure Cosmos DB for NoSQL .NET SDK.
- Learn about performance guidelines for [.NET v3](performance-tips-dotnet-sdk-v3.md) and [.NET v2](performance-tips.md).
- [Diagnose and troubleshoot](troubleshoot-java-sdk-v4.md) issues when you use the Azure Cosmos DB for NoSQL Java v4 SDK.
- Learn about performance guidelines for [Java v4 SDK](performance-tips-java-sdk-v4.md).
