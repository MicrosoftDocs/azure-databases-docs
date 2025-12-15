---
title: Performance tips for Azure Cosmos DB Python SDK
description: Learn client configuration options to improve Azure Cosmos DB database performance for Python SDK
author: kushagraThapar
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: python
ms.topic: how-to
ms.date: 04/08/2024
ms.author: kuthapar
ms.custom: devx-track-python, devx-track-extended-python
---

# Performance tips for Azure Cosmos DB Python SDK
[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

> [!div class="op_single_selector"]
> * [Python SDK](performance-tips-python-sdk.md)
> * [Java SDK v4](performance-tips-java-sdk-v4.md)
> * [Async Java SDK v2](performance-tips-async-java.md)
> * [Sync Java SDK v2](performance-tips-java.md)
> * [.NET SDK v3](performance-tips-dotnet-sdk-v3.md)
> * [.NET SDK v2](performance-tips.md)
> 

> [!IMPORTANT]  
> The performance tips in this article are for Azure Cosmos DB Python SDK only. Please see the Azure Cosmos DB Python SDK [Readme](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-cosmos/README.md#azure-cosmos-db-sql-api-client-library-for-python) [Release notes](sdk-python.md), [Package (PyPI)](https://pypi.org/project/azure-cosmos), [Package (Conda)](https://anaconda.org/microsoft/azure-cosmos/), and [troubleshooting guide](troubleshoot-python-sdk.md) for more information.
>

Azure Cosmos DB is a fast and flexible distributed database that scales seamlessly with guaranteed latency and throughput. You do not have to make major architecture changes or write complex code to scale your database with Azure Cosmos DB. Scaling up and down is as easy as making a single API call or SDK method call. However, because Azure Cosmos DB is accessed via network calls there are client-side optimizations you can make to achieve peak performance when using Azure Cosmos DB Python SDK.

So if you're asking "How can I improve my database performance?" consider the following options:

## Networking
* **Collocate clients in same Azure region for performance**

When possible, place any applications calling Azure Cosmos DB in the same region as the Azure Cosmos DB database. For an approximate comparison, calls to Azure Cosmos DB within the same region complete within 1-2 ms, but the latency between the West and East coast of the US is >50 ms. This latency can likely vary from request to request depending on the route taken by the request as it passes from the client to the Azure datacenter boundary. The lowest possible latency is achieved by ensuring the calling application is located within the same Azure region as the provisioned Azure Cosmos DB endpoint. For a list of available regions, see [Azure Regions](https://azure.microsoft.com/regions/#services).

:::image type="content" source="./media/performance-tips/same-region.png" alt-text="Illustration of the Azure Cosmos DB connection policy." border="false":::

An app that interacts with a multi-region Azure Cosmos DB account needs to configure 
[preferred locations](tutorial-global-distribution.md#preferred-locations) to ensure that requests are going to a collocated region.

**Enable accelerated networking to reduce latency and CPU jitter**

It is recommended that you follow the instructions to enable [Accelerated Networking](/azure/virtual-network/accelerated-networking-overview) in your [Windows (select for instructions)](/azure/virtual-network/create-vm-accelerated-networking-powershell) or [Linux (select for instructions)](/azure/virtual-network/create-vm-accelerated-networking-cli) Azure VM, in order to maximize performance (reduce latency and CPU jitter).

Without accelerated networking, IO that transits between your Azure VM and other Azure resources might be unnecessarily routed through a host and virtual switch situated between the VM and its network card. Having the host and virtual switch inline in the datapath not only increases latency and jitter in the communication channel, it also steals CPU cycles from the VM. With accelerated networking, the VM interfaces directly with the NIC without intermediaries; any network policy details which were being handled by the host and virtual switch are now handled in hardware at the NIC; the host and virtual switch are bypassed. Generally you can expect lower latency and higher throughput, as well as more *consistent* latency and decreased CPU utilization when you enable accelerated networking.

Limitations: accelerated networking must be supported on the VM OS, and can only be enabled when the VM is stopped and deallocated. The VM cannot be deployed with Azure Resource Manager. [App Service](/azure/app-service/overview) has no accelerated network enabled.

Please see the [Windows](/azure/virtual-network/create-vm-accelerated-networking-powershell) and [Linux](/azure/virtual-network/create-vm-accelerated-networking-cli) instructions for more details.

## High availability

For general guidance on configuring high availability in Azure Cosmos DB, see [High availability in Azure Cosmos DB](/azure/reliability/reliability-cosmos-db-nosql). 

In addition to a good foundational setup in the database platform, partition-level circuit breaker can be implemented in the Python SDK, which can help in outage scenarios. This feature provides advanced mechanisms availability challenges, going above and beyond the cross-region retry capabilities that are built into the SDK by default. This can significantly enhance the resilience and performance of your application, particularly under high-load or degraded conditions.

### Partition-level circuit breaker

The partition-level circuit breaker (PPCB) in the Python SDK improves availability and resilience by tracking the health of individual physical partitions and routing requests away from problematic ones. This feature is particularly useful for handling transient and terminal issues such as network problems, partition upgrades, or migrations.

PPCB is applicable in the following scenarios:

- Any consistency level
- Operations with partition key (point reads/writes)
- Single write region accounts with multiple read regions
- Multiple write region accounts

#### How it works

Partitions transition through four states - **Healthy**, **Unhealthy Tentative**, **Unhealthy**, and **Healthy Tentative** - based on the success or failure of requests:

1. **Failure Tracking:** The SDK monitors error rates (e.g., 5xx, 408) per partition over a one-minute window. Consecutive failures per partition are tracked indefinitely by the SDK.
2. **Marking as Unavailable:** If a partition exceeds configured thresholds, it's marked as *Unhealthy Tentative* and excluded from routing for 1 minute.
3. **Promotion to Unhealthy or Recovery:** If recovery attempts fail, the partition transitions to *Unhealthy*. After a backoff interval, a *Healthy Tentative* probe is made with a limited-time request to determine recovery.
4. **Reinstatement:** If the tentative probe succeeds, the partition returns to *Healthy*. Otherwise, it remains *Unhealthy* until the next probe.

This failover is managed internally by the SDK and ensures requests avoid known-problematic partitions until they're confirmed to be healthy again.

#### Configuration via environment variables

You can control the PPCB behavior using these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `AZURE_COSMOS_ENABLE_CIRCUIT_BREAKER` | Enables/disables PPCB | `false` |
| `AZURE_COSMOS_CONSECUTIVE_ERROR_COUNT_TOLERATED_FOR_READ` | Max consecutive read failures before marking a partition unavailable | `10` |
| `AZURE_COSMOS_CONSECUTIVE_ERROR_COUNT_TOLERATED_FOR_WRITE` | Max consecutive write failures before marking a partition unavailable | `5` |
| `AZURE_COSMOS_FAILURE_PERCENTAGE_TOLERATED` | Failure percentage threshold before marking a partition unavailable | `90` |

> [!TIP]
> Additional configuration options may be exposed in future releases for fine-tuning timeout durations and recovery backoff behavior.

### Excluded regions

The excluded regions feature enables fine-grained control over request routing by allowing you to exclude specific regions from your preferred locations on a per-request basis. This feature is available in Azure Cosmos DB Python SDK version 4.14.0 and higher.

**Key benefits:**
- **Handle rate limiting**: When encountering 429 (Too Many Requests) responses, automatically route requests to alternate regions with available throughput
- **Targeted routing**: Ensure requests are served from specific regions by excluding all others
- **Bypass preferred order**: Override the default preferred regions list for individual requests without creating separate clients

**Configuration:**

Excluded regions can be configured at both the client level and request level:

```python
from azure.cosmos import CosmosClient
from azure.cosmos.partition_key import PartitionKey

# Configure preferred locations and excluded locations at client level
preferred_locations = ['West US 3', 'West US', 'East US 2']
excluded_locations_on_client = ['West US 3', 'West US']

client = CosmosClient(
    url=HOST,
    credential=MASTER_KEY,
    preferred_locations=preferred_locations,
    excluded_locations=excluded_locations_on_client
)

database = client.create_database('TestDB')
container = database.create_container(
    id='TestContainer',
    partition_key=PartitionKey(path="/pk")
)

# Create an item (writes ignore excluded_locations in single-region write accounts)
test_item = {
    'id': 'Item_1',
    'pk': 'PartitionKey_1',
    'test_object': True,
    'lastName': 'Smith'
}
created_item = container.create_item(test_item)

# Read operations will use preferred_locations minus excluded_locations
# In this example: ['West US 3', 'West US', 'East US 2'] - ['West US 3', 'West US'] = ['East US 2']
item = container.read_item(
    item=created_item['id'],
    partition_key=created_item['pk']
)
```

**Request-level excluded regions:**

Request-level excluded regions take highest priority and override client-level settings:

```python
# Excluded locations can be specified per request, overriding client settings
excluded_locations_on_request = ['West US 3']

# Create item with request-level excluded regions
created_item = container.create_item(
    test_item,
    excluded_locations=excluded_locations_on_request
)

# Read with request-level excluded regions
# This will use: ['West US 3', 'West US', 'East US 2'] - ['West US 3'] = ['West US', 'East US 2']
item = container.read_item(
    item=created_item['id'],
    partition_key=created_item['pk'],
    excluded_locations=excluded_locations_on_request
)
```

#### Fine-tuning consistency vs availability

The excluded regions feature provides an additional mechanism for balancing consistency and availability trade-offs in your application. This capability is particularly valuable in dynamic scenarios where requirements may shift based on operational conditions:

**Dynamic outage handling**: When a primary region experiences an outage and partition-level circuit breaker thresholds prove insufficient, excluded regions enables immediate failover without code changes or application restarts. This provides faster response to regional issues compared to waiting for automatic circuit breaker activation.

**Conditional consistency preferences**: Applications can implement different consistency strategies based on operational state:
- **Steady state**: Prioritize consistent reads by excluding all regions except the primary, ensuring data consistency at the potential cost of availability
- **Outage scenarios**: Favor availability over strict consistency by allowing cross-region routing, accepting potential data lag in exchange for continued service availability

This approach allows external mechanisms (such as traffic managers or load balancers) to orchestrate failover decisions while the application maintains control over consistency requirements through region exclusion patterns.

When all regions are excluded, requests will be routed to the primary/hub region. This feature works with all request types including queries and is particularly useful for maintaining singleton client instances while achieving flexible routing behavior.

## SDK usage
* **Install the most recent SDK**

The Azure Cosmos DB SDKs are constantly being improved to provide the best performance. See the [Azure Cosmos DB SDK release notes](sdk-python.md) to determine the most recent SDK and review improvements.

* **Use a singleton Azure Cosmos DB client for the lifetime of your application**

Each Azure Cosmos DB client instance is thread-safe and performs efficient connection management and address caching. To allow efficient connection management and better performance by the Azure Cosmos DB client, it is recommended to use a single instance of the Azure Cosmos DB client for the lifetime of the application.

* **Tune timeout and retry configurations**

Timeout configurations and retry policies can be customized based on the application needs. Refer to [timeout and retries configuration](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-cosmos/docs/TimeoutAndRetriesConfig.md#cosmos-db-python-sdk--timeout-configurations-and-retry-configurations) document to get a complete list of configurations that can be customized.

* **Use the lowest consistency level required for your application**

When you create a *CosmosClient*, account level consistency is used if none is specified in the client creation. For more information on consistency levels, see the [consistency-levels](https://aka.ms/cosmos-consistency-levels) document.

* **Scale out your client-workload**

If you are testing at high throughput levels, the client application might become the bottleneck due to the machine capping out on CPU or network utilization. If you reach this point, you can continue to push the Azure Cosmos DB account further by scaling out your client applications across multiple servers.

A good rule of thumb is not to exceed >50% CPU utilization on any given server, to keep latency low.

* **OS Open files Resource Limit**
 
Some Linux systems (like Red Hat) have an upper limit on the number of open files and so the total number of connections. Run the following to view the current limits:

```bash
ulimit -a
```

The number of open files (`nofile`) needs to be large enough to have enough room for your configured connection pool size and other open files by the OS. It can be modified to allow for a larger connection pool size.

Open the limits.conf file:

```bash
vim /etc/security/limits.conf
```
    
Add/modify the following lines:

```
* - nofile 100000
```

## Query operations

For query operations see the [performance tips for queries](performance-tips-query-sdk.md?pivots=programming-language-python).

### Indexing policy
 
* **Exclude unused paths from indexing for faster writes**

Azure Cosmos DB’s indexing policy allows you to specify which document paths to include or exclude from indexing by leveraging Indexing Paths (setIncludedPaths and setExcludedPaths). The use of indexing paths can offer improved write performance and lower index storage for scenarios in which the query patterns are known beforehand, as indexing costs are directly correlated to the number of unique paths indexed. For example, the following code shows how to include and exclude entire sections of the documents (also known as a subtree) from indexing using the "*" wildcard.

```python
container_id = "excluded_path_container"
indexing_policy = {
        "includedPaths" : [ {'path' : "/*"} ],
        "excludedPaths" : [ {'path' : "/non_indexed_content/*"} ]
        }
db.create_container(
    id=container_id,
    indexing_policy=indexing_policy,
    partition_key=PartitionKey(path="/pk"))
```

For more information, see [Azure Cosmos DB indexing policies](../index-policy.md).

### Throughput

* **Measure and tune for lower request units/second usage**

Azure Cosmos DB offers a rich set of database operations including relational and hierarchical queries with UDFs, stored procedures, and triggers – all operating on the documents within a database collection. The cost associated with each of these operations varies based on the CPU, IO, and memory required to complete the operation. Instead of thinking about and managing hardware resources, you can think of a request unit (RU) as a single measure for the resources required to perform various database operations and service an application request.

Throughput is provisioned based on the number of [request units](../request-units.md) set for each container. Request unit consumption is evaluated as a rate per second. Applications that exceed the provisioned request unit rate for their container are limited until the rate drops below the provisioned level for the container. If your application requires a higher level of throughput, you can increase your throughput by provisioning additional request units.

The complexity of a query impacts how many request units are consumed for an operation. The number of predicates, nature of the predicates, number of UDFs, and the size of the source data set all influence the cost of query operations.

To measure the overhead of any operation (create, update, or delete), inspect the [x-ms-request-charge](/rest/api/cosmos-db/common-cosmosdb-rest-request-headers) header to measure the number of request units consumed by these operations.

```python
document_definition = {
    'id': 'document',
    'key': 'value',
    'pk': 'pk'
}
document = container.create_item(
    body=document_definition,
)
print("Request charge is : ", container.client_connection.last_response_headers['x-ms-request-charge'])
```

The request charge returned in this header is a fraction of your provisioned throughput. For example, if you have 2000 RU/s provisioned, and if the preceding query returns 1000 1KB-documents, the cost of the operation is 1000. As such, within one second, the server honors only two such requests before rate limiting subsequent requests. For more information, see [Request units](../request-units.md) and the [request unit calculator](https://cosmos.azure.com/capacitycalculator).

* **Handle rate limiting/request rate too large**

When a client attempts to exceed the reserved throughput for an account, there is no performance degradation at the server and no use of throughput capacity beyond the reserved level. The server will preemptively end the request with RequestRateTooLarge (HTTP status code 429) and return the [x-ms-retry-after-ms](/rest/api/cosmos-db/common-cosmosdb-rest-request-headers) header indicating the amount of time, in milliseconds, that the user must wait before reattempting the request.

```xml
HTTP Status 429,
Status Line: RequestRateTooLarge
x-ms-retry-after-ms :100
```

The SDKs all implicitly catch this response, respect the server-specified retry-after header, and retry the request. Unless your account is being accessed concurrently by multiple clients, the next retry will succeed.

If you have more than one client cumulatively operating consistently above the request rate, the default retry count currently set to 9 internally by the client might not suffice; in this case, the client throws a *CosmosHttpResponseError* with status code 429 to the application. The default retry count can be changed by passing `retry_total` configuration to the client. By default, the *CosmosHttpResponseError* with status code 429 is returned after a cumulative wait time of 30 seconds if the request continues to operate above the request rate. This occurs even when the current retry count is less than the max retry count, be it the default of 9 or a user-defined value.

While the automated retry behavior helps to improve resiliency and usability for the most applications, it might come at odds when doing performance benchmarks, especially when measuring latency. The client-observed latency will spike if the experiment hits the server throttle and causes the client SDK to silently retry. To avoid latency spikes during performance experiments, measure the charge returned by each operation and ensure that requests are operating below the reserved request rate. For more information, see [Request units](../request-units.md).

* **Design for smaller documents for higher throughput**

The request charge (the request processing cost) of a given operation is directly correlated to the size of the document. Operations on large documents cost more than operations for small documents. Ideally, architect your application and workflows to have your item size be ~1KB, or similar order or magnitude. For latency-sensitive applications large items should be avoided - multi-MB documents will slow down your application.

## Next steps

To learn more about designing your application for scale and high performance, see [Partitioning and scaling in Azure Cosmos DB](../partitioning-overview.md).

Trying to do capacity planning for a migration to Azure Cosmos DB? You can use information about your existing database cluster for capacity planning.
* If all you know is the number of vCores and servers in your existing database cluster, read about [estimating request units using vCores or vCPUs](../convert-vcore-to-request-unit.md) 
* If you know typical request rates for your current database workload, read about [estimating request units using Azure Cosmos DB capacity planner](estimate-ru-with-capacity-planner.md)
