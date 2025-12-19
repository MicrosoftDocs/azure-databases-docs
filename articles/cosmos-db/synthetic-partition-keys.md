---
title: Create a Synthetic Partition Key
description: Learn how to use synthetic partition keys in your Azure Cosmos DB containers to distribute the data and workload evenly across the partition keys.
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 07/15/2025
author: markjbrown
ms.author: mjbrown
appliesto:
  - ✅ NoSQL
---

# Create a synthetic partition key

As a best practice, you should use a partition key that has many distinct values, such as hundreds or thousands. The goal is to distribute your data and workload evenly across the items associated with these partition key values. If such a property doesn’t exist in your data, you can construct a *synthetic partition key*.

This document describes several basic techniques for generating a synthetic partition key for your Azure Cosmos DB container.

## Concatenate multiple properties of an item

You can form a partition key by concatenating multiple property values into a single artificial `partitionKey` property. These keys are referred to as synthetic keys. For example, consider the following example document:

```JavaScript
{
"deviceId": "abc-123",
"date": 2018
}
```

For the previous document, one option is to set `/deviceId` or `/date` as the partition key field. Use this option, if you want to partition your container based on either device ID or date. Another option is to concatenate these two values into a synthetic `partitionKey` property that's used as the partition key.

```JavaScript
{
"deviceId": "abc-123",
"date": 2018,
"partitionKey": "abc-123-2018"
}
```

In real-world scenarios, you can have thousands of items in a database. Instead of adding the synthetic key manually, define client-side logic to concatenate values and insert the synthetic key into the items in your Azure Cosmos DB containers.

## Use a partition key with a random suffix

Another possible strategy to distribute the workload more evenly is to append a random number at the end of the partition key value. When you distribute items in this way, you can perform parallel write operations across partitions.

An example is if a partition key represents a date. You might choose a random number between 1 and 400, then concatenate it as a suffix to the date. This method results in partition key values like `2018-08-09.1`,`2018-08-09.2`, and so on, through `2018-08-09.400`. Because you randomize the partition key, the write operations on the container on each day are spread evenly across multiple partitions. This method results in better parallelism and overall higher throughput.

## Use a partition key with precalculated suffixes 

The random suffix strategy can greatly improve write throughput, but it's difficult to read a specific item. You don't know the suffix value that was used when you wrote the item. To make it easier to read individual items, use the precalculated suffixes strategy. Instead of using a random number to distribute the items among the partitions, use a number that is calculated based on something that you want to query.

Consider the previous example, where a container uses a date as the partition key. Now suppose that each item has a `Vehicle-Identification-Number` (`VIN`) attribute that we want to access. Further, suppose that you often run queries to find items by the `VIN`, in addition to date. Before your application writes the item to the container, it can calculate a hash suffix based on the VIN and append it to the partition key date. The calculation might generate a number between 1 and 400 that is evenly distributed. This result is similar to the results produced by the random suffix strategy method. The partition key value is then the date concatenated with the calculated result.

With this strategy, the writes are evenly spread across the partition key values, and across the partitions. You can easily read a particular item and date, because you can calculate the partition key value for a specific `Vehicle-Identification-Number`. The benefit of this method is that you can avoid creating a single hot partition key, that is, a partition key that takes all the workload.

## Next steps

You can learn more about the partitioning concept in the following articles:

* [Partitioning and horizontal scaling in Azure Cosmos DB](partitioning-overview.md)
* [Introduction to provisioned throughput in Azure Cosmos DB](set-throughput.md)
* [Provision standard (manual) throughput on a database in Azure Cosmos DB](how-to-provision-container-throughput.md)

Trying to do capacity planning for a migration to Azure Cosmos DB? You can use information about your existing database cluster for capacity planning.
* If all you know is the number of vcores and servers in your existing database cluster, read about [estimating request units using vCores or vCPUs](convert-vcore-to-request-unit.md).
* If you know typical request rates for your current database workload, read about [estimating request units using Azure Cosmos DB capacity planner](estimate-ru-with-capacity-planner.md).
