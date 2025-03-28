---
title: 'Azure Cosmos DB: Throughput buckets'
description: Learn how you can control throughput usage for different workloads by creating buckets in Azure Cosmos DB.
author: richagaur
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: conceptual
ms.author: richagaur

---

[!INCLUDE[NoSQL](includes/appliesto-nosql.md)]

# Throughput buckets in Azure Cosmos DB

When multiple workloads share the same Azure Cosmos DB container, resource contention can lead to throttling, increased latency, and potential business impact. To address this, Cosmos DB allows you to allocate throughput buckets, ensuring better isolation and governance of resource usage for multiple workloads.

#### Common Use Cases

- Multi-tenant workloads managed by ISVs
- Bulk execution in ETL jobs
- Data ingestion and migration processes
- Execution of stored procedures
- Change feed processing

### How Throughput buckets Work

Each bucket is assigned a maximum throughput percentage, which determines the fraction of the container's total throughput allocated to that bucket.

- Requests assigned to a bucket consume throughput only from that bucket.
- If the total usage within a bucket exceeds its assigned percentage, additional requests will be throttled.
- This ensures that high-usage workloads do not impact other workloads sharing the container.

> [!Note]
> Requests that do not belong to a configured bucket will consume throughput from the overall container without restrictions.

### Configuring Throughput buckets

To set up throughput buckets in the Azure Portal:

1. Open **Data Explorer** and navigate to the **Scale & Settings** pane of your container.
2. Locate the **Throughput Buckets** tab.
3. Enable the feature by toggling the switch from inactive to active.
4. Set the desired throughput percentage for each bucket (up to five buckets per container).

### Using Throughput buckets in SDK requests

To assign a request to a specific bucket, use the RequestOption API in the SDK.

#### [.NET SDK v3](#tab/net-v3)

```csharp
using Microsoft.Azure.Cosmos;

string itemId = "<id>";
PartitionKey partitionKey = new PartitionKey("p<key>");

// Define request options with Throughput Bucket 1 for read operation
ItemRequestOptions readRequestOptions = new ItemRequestOptions{ThroughputBucket = 1};

// Send read request using Bucket ID 1
ItemResponse<Product> readResponse = await container.ReadItemAsync<Product>(
    itemId,
    partitionKey,
    readRequestOptions);

Product product = readResponse.Resource;

// Define request options with Throughput Bucket 2 for update operation
ItemRequestOptions updateRequestOptions = new ItemRequestOptions{ThroughputBucket = 2};

// Send update request using Bucket ID 2
ItemResponse<Product> updateResponse = await container.ReplaceItemAsync(
    product,
    itemId,
    partitionKey,
    updateRequestOptions);
```

To apply a throughput bucket to all requests from a client application, use the ClientOptions API in the SDK.

#### [.NET SDK v3](#tab/net-v3)

```csharp
using Microsoft.Azure.Cosmos;
using Azure.Identity;

var credential = new DefaultAzureCredential();

// Create CosmosClient with Bulk Execution and Throughput Bucket 1
CosmosClient cosmosClient = new CosmosClientBuilder("<endpointUri>", credential)
    .WithBulkExecution(true)   // Enable bulk execution
    .WithThroughputBucket(1)   // Assign throughput bucket 1 to all requests
    .Build();

// Get container reference
Container container = cosmosClient.GetContainer("<DatabaseId>", "<ContainerId>");

// Prepare bulk operations
List<Task> tasks = new List<Task>();
for (int i = 1; i <= 10; i++)
{
    var item = new
    {
        id = Guid.NewGuid().ToString(),
        partitionKey = $"pkey-{i}",
        name = $"Item-{i}",
        timestamp = DateTime.UtcNow
    };

    tasks.Add(container.CreateItemAsync(item, new PartitionKey(item.partitionKey)));
}

// Execute bulk insertions with throughput bucket 1
await Task.WhenAll(tasks);

//Read item with throughput bucket 1
ItemResponse<Product> response = await container.ReadItemAsync<Product>(partitionKey: new PartitionKey("pkey1"), id: "id1");

```

> [!Note]
> If bulk execution is enabled, a throughput bucket cannot be assigned to an individual request using the RequestOptions API.

### Bucket behavior in Data Explorer

- If **Bucket 1** is configured, all requests from Data Explorer will use this bucket and adhere to its throughput limits. 
- If **Bucket 1** is not configured, requests will utilize the container’s full available throughput.

### Monitoring Throughput buckets 

You can track bucket usage in the Azure Portal:

- **Total Requests (preview)**: View the number of requests per bucket by splitting the metric by ThroughputBucket.

- **Total Request Units (preview)**: Monitor RU/s consumption per bucket by splitting the metric by ThroughputBucket.

### Limitations

- Not supported for containers in a Shared Throughput Database.
- Not available for Serverless Cosmos DB accounts.
- Requests assigned to a bucket cannot utilize Burst Capacity.

### Next Steps
- Read the [Frequently asked questions](throughput-buckets-faq.md) on Throughput buckets.