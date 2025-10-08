---
title: 'Azure Cosmos DB: Throughput buckets (preview)'
description: Learn how you can control throughput usage for different workloads by creating buckets in Azure Cosmos DB.
author: richagaur
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.author: richagaur
ms.date: 03/31/2025
---

# Throughput buckets in Azure Cosmos DB (preview)

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

When multiple workloads share the same Azure Cosmos DB container, resource contention can lead to throttling, increased latency, and potential business impact. To address this, Cosmos DB allows you to allocate throughput buckets, ensuring better isolation and governance of resource usage for multiple workloads.

#### Common Use Cases

- Multitenant workloads managed by Independent Software Vendors (ISVs)
- Bulk execution in ETL jobs
- Data ingestion and migration processes
- Execution of stored procedures
- Change feed processing

### How Throughput buckets Work

Throughput buckets help manage resource consumption for workloads sharing a Cosmos DB container by limiting the maximum throughput a bucket can consume. However, throughput isn't reserved for any bucket, it remains shared across all workloads.

- Each bucket has a maximum throughput percentage, capping the fraction of the container’s total throughput that it can consume.
- Requests assigned to a bucket can consume throughput only up to this limit.
- If the bucket exceeds its configured limit, subsequent requests are throttled.
- This mechanism helps in preventing resource contention, ensuring that no single workload consumes excessive throughput and impacts others.

> [!Note]
> Requests not assigned to a bucket will consume throughput from the container without restrictions.

### Getting started

To enable Throughput buckets, go to the **Preview features** section on your Subscription page in the Azure portal. Search for the **Throughput Buckets** feature and register for the preview. After your registration is approved, it may take up to an hour for Throughput buckets to be enabled on all accounts within the subscription. Once enabled, you can create throughput buckets for your Cosmos DB containers.

### Configuring Throughput buckets

To set up throughput buckets in the Azure portal:

1. Open **Data Explorer** and navigate to the **Scale & Settings** pane of your container.
2. Locate the **Throughput Buckets** tab.
3. Enable the desired throughput bucket by toggling it from "Inactive" to "Active."
4. Set the desired maximum throughput percentage for enabled buckets (up to five buckets per container).

### Minimum SDK version requirements

- .NET >=  [3.50.0-preview.0](https://www.nuget.org/packages/Microsoft.Azure.Cosmos/3.50.0-preview.0)
- Javascript >=[4.3.0](https://www.npmjs.com/package/@azure/cosmos/v/4.3.0)
- Python >=[4.11.0b1](https://pypi.org/project/azure-cosmos/4.11.0b1/)

### Using Throughput buckets in SDK requests

### [.NET](#tab/dotnet)

To assign a request to a specific bucket, use RequestOptions in the SDK.

```csharp
using Microsoft.Azure.Cosmos;

string itemId = "<id>";
PartitionKey partitionKey = new PartitionKey("<pkey>");

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

To apply a throughput bucket to all requests from a client application, use ClientOptions in the SDK.

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

### [Python](#tab/python)

To apply a throughput bucket to all requests from a client application, use `throughput_bucket` option when creating `cosmos_client`.

```python
# Applies throughput bucket 1 to all requests from a client application
HOST = "https://your-cosmos-db-account.documents.azure.com:443/"
credential = DefaultAzureCredential()
DATABASE_ID = "your-database-id"
allRequestsClient = cosmos_client.CosmosClient(HOST, credential=credential, throughput_bucket=1)
```

To assign a request to a specific bucket, use `throughput_bucket` at the request level.

```python
# Applies throughput bucket 2 for read item requests
client = cosmos_client.CosmosClient(HOST, credential=credential)
database = client.get_database_client(DATABASE_ID)
created_container = database.create_container(
    str(uuid.uuid4()),
    PartitionKey(path="/pk"))
created_document = created_container.create_item(body={'id': '1' + str(uuid.uuid4()), 'pk': 'mypk'})

created_container.read_item(
     item=created_document['id'],
     partition_key="mypk",
     throughput_bucket=2)
database.delete_container(created_container.id)

```

---

> [!Note]
> If bulk execution is enabled, a throughput bucket can't be assigned to an individual request using the RequestOptions.

### Bucket behavior in Data Explorer

- If **Bucket 1** is configured, all requests from Data Explorer use this bucket and adhere to its throughput limits. 
- If **Bucket 1** isn't configured, requests utilize the container’s full available throughput.

### Monitoring Throughput buckets 

You can track bucket usage in the Azure portal:

- **Total Requests (preview)**: View the number of requests per bucket by splitting the metric by ThroughputBucket.

- **Total Request Units (preview)**: Monitor RU/s consumption per bucket by splitting the metric by ThroughputBucket.

### Limitations

- Not supported for containers in a Shared Throughput Database.
- Not available for Serverless Cosmos DB accounts.
- Requests assigned to a bucket can't utilize Burst Capacity.

### Next Steps
- Read the [Frequently asked questions](throughput-buckets-faq.yml) on Throughput buckets.