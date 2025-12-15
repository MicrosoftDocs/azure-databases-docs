---
title: Azure Cosmos DB Performance Tips for .NET SDK v3
description: Learn client configuration options to help improve Azure Cosmos DB .NET v3 SDK performance.
author: markjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 07/14/2025
ms.author: mjbrown
ms.devlang: csharp
ms.custom: devx-track-dotnet
---

# Performance tips for Azure Cosmos DB and .NET
[!INCLUDE[NoSQL](includes/appliesto-nosql.md)]

> [!div class="op_single_selector"]
> * [.NET SDK v3](performance-tips-dotnet-sdk-v3.md)
> * [.NET SDK v2](performance-tips.md)
> * [Java SDK v4](performance-tips-java-sdk-v4.md)
> * [Async Java SDK v2](performance-tips-async-java.md)
> * [Sync Java SDK v2](performance-tips-java.md)
> * [Python SDK](performance-tips-python-sdk.md)

Azure Cosmos DB is a fast, flexible distributed database that scales seamlessly with guaranteed latency and throughput levels. You don't have to make major architecture changes or write complex code to scale your database with Azure Cosmos DB. Scaling up and down is as easy as making a single API call. To learn more, see [provision container throughput](how-to-provision-container-throughput.md) or [provision database throughput](how-to-provision-database-throughput.md). 

Because Azure Cosmos DB is accessed via network calls, you can make client-side optimizations to achieve peak performance when you use the [SQL .NET SDK](sdk-dotnet-v3.md).

If you're trying to improve your database performance, consider the options presented in the following sections.

## Hosting recommendations

**Turn on server-side garbage collection**

Reducing the frequency of garbage collection can help in some cases. In .NET, set [gcServer](/dotnet/core/run-time-config/garbage-collector#flavors-of-garbage-collection) to `true`.

**Scale out your client workload**

If you're testing at high throughput levels, or at rates that are greater than 50,000 Request Units per second (RU/s), the client application could become a workload bottleneck because the machine might cap out on CPU or network utilization. If you reach this point, you can continue to push the Azure Cosmos DB account further by scaling out your client applications across multiple servers.

> [!NOTE] 
> High CPU usage can cause increased latency and request timeout exceptions.

## <a id="metadata-operations"></a> Metadata operations

Don't verify that a database or container exists by calling `Create...IfNotExistsAsync` or `Read...Async` in the hot path or before doing an item operation. The validation should only be done on application startup when it's necessary, if you expect them to be deleted (otherwise it's not needed). These metadata operations generate extra end-to-end latency, have no SLA, and have their own separate [limitations](./troubleshoot-request-rate-too-large.md#rate-limiting-on-metadata-requests) that don't scale like data operations.

## <a id="logging-and-tracing"></a> Logging and tracing

Some environments have the [.NET DefaultTraceListener](/dotnet/api/system.diagnostics.defaulttracelistener) enabled. The DefaultTraceListener poses performance issues on production environments causing high CPU and I/O bottlenecks. Check and make sure that the DefaultTraceListener is disabled for your application by removing it from the [TraceListeners](/dotnet/framework/debug-trace-profile/how-to-create-and-initialize-trace-listeners) on production environments.

SDK versions greater than 3.23.0 automatically remove it when detected. With older versions, you can remove it by using the following commands:

# [.NET 6 / .NET Core](#tab/trace-net-core)

```csharp
if (!Debugger.IsAttached)
{
    Type defaultTrace = Type.GetType("Microsoft.Azure.Cosmos.Core.Trace.DefaultTrace,Microsoft.Azure.Cosmos.Direct");
    TraceSource traceSource = (TraceSource)defaultTrace.GetProperty("TraceSource").GetValue(null);
    traceSource.Listeners.Remove("Default");
    // Add your own trace listeners
}
```

# [.NET Framework](#tab/trace-net-fx)

Edit your `app.config` or `web.config` files:

```xml
<configuration>
  <system.diagnostics>
    <sources>
      <source name="DocDBTrace" switchName="SourceSwitch" switchType="System.Diagnostics.SourceSwitch" >
        <listeners>
          <remove name="Default" />
          <!--Add your own trace listeners-->
          <add name="myListener" ... />
        </listeners>
      </source>
    </sources>
  </system.diagnostics>
<configuration>
```

---

## High availability

For general guidance on configuring high availability in Azure Cosmos DB, see [High availability in Azure Cosmos DB](/azure/reliability/reliability-cosmos-db-nosql). 

In addition to a good foundational setup in the database platform, there are specific techniques that can be implemented in the .NET SDK itself, which can help in outage scenarios. Two notable strategies are the threshold-based availability strategy and the partition-level circuit breaker.

### Threshold-based availability strategy

The threshold-based availability strategy can improve tail latency and availability by sending parallel read requests to secondary regions (as defined in `ApplicationPreferredRegions`) and accepting the fastest response. This approach can drastically reduce the effect of regional outages or high-latency conditions on application performance. 

**Example configuration:**

Configuring this can be done using `CosmosClientBuilder`:

```Csharp
CosmosClient client = new CosmosClientBuilder("connection string")
    .WithApplicationPreferredRegions(
        new List<string> { "East US", "East US 2", "West US" } )
    .WithAvailabilityStrategy(
        AvailabilityStrategy.CrossRegionHedgingStrategy(
        threshold: TimeSpan.FromMilliseconds(500),
        thresholdStep: TimeSpan.FromMilliseconds(100)
     ))
    .Build();
```

Or by configuring options and adding them to `CosmosClient`:

```Csharp
CosmosClientOptions options = new CosmosClientOptions()
{
    AvailabilityStrategy
     = AvailabilityStrategy.CrossRegionHedgingStrategy(
        threshold: TimeSpan.FromMilliseconds(500),
        thresholdStep: TimeSpan.FromMilliseconds(100)
     )
      ApplicationPreferredRegions = new List<string>() { "East US", "East US 2", "West US"},
};

CosmosClient client = new CosmosClient(
    accountEndpoint: "account endpoint",
    authKeyOrResourceToken: "auth key or resource token",
    clientOptions: options);
```

**How it works:**

1. **Initial request:** At time T1, a read request is made to the primary region (for example, East US). The SDK waits for a response for up to 500 milliseconds (the `threshold` value).
  
1. **Second request:** If there's no response from the primary region within 500 milliseconds, a parallel request is sent to the next preferred region (for example, East US 2).
  
1. **Third request:** If neither the primary nor the secondary region responds within 600 milliseconds (500 ms + 100 ms, the `thresholdStep` value), the SDK sends another parallel request to the third preferred region (for example, West US).

1. **Fastest response wins:** Whichever region responds first, that response is accepted, and the other parallel requests are ignored.

> [!NOTE]
> If the first preferred region returns a nontransient error status code (for example, document not found, authorization error, or conflict), the operation itself fails fast, as availability strategy doesn't have any benefit in this scenario.

### Partition-level circuit breaker

The partition-level circuit breaker (PPCB) is a feature in the .NET SDK that enhances availability and latency by tracking unhealthy physical partitions. When enabled, it helps route requests to healthier regions, preventing cascading failures due to regional or partition-specific issues. The feature is independent of backend-triggered failover and is controlled through environment variables.

This feature is **disabled by default**, but is **enabled automatically** when partition-level failover is enabled.

#### How it works

1. **Failure detection:** When specific errors such as `503 Service Unavailable`, `408 Request Timeout`, or cancellation tokens are observed, the SDK counts consecutive failures for a partition.
1. **Triggering failover:** Once a configured threshold of consecutive failures is reached, the SDK redirects requests for that partition key range to the next preferred region using `GlobalPartitionEndpointManagerCore.TryMarkEndpointUnavailableForPartitionKeyRange`.
1. **Background Recovery:** A background task is initiated during failover to periodically reevaluate the health of the failed partition by trying to connect to all four replicas. Once healthy, the SDK removes the override and returns to the primary region.

#### Behavior by account type

- **Single-region write (single master):** Only **read** requests participate in PPCB failover logic.
- **Multi-region write (multi master):** Both **read and write** requests use PPCB failover logic.

#### Configuration options

Use the following environment variables to configure PPCB:

| Environment variable | Description | Default |
|----------------------|-------------|---------|
| `AZURE_COSMOS_CIRCUIT_BREAKER_ENABLED` | Enables or disables the PPCB feature. | `false` |
| `AZURE_COSMOS_PPCB_CONSECUTIVE_FAILURE_COUNT_FOR_READS` | Consecutive read failures to trigger failover. | `10` |
| `AZURE_COSMOS_PPCB_CONSECUTIVE_FAILURE_COUNT_FOR_WRITES` | Consecutive write failures to trigger failover. | `5` |
| `AZURE_COSMOS_PPCB_ALLOWED_PARTITION_UNAVAILABILITY_DURATION_IN_SECONDS` | Time before reevaluating partition health. | `5` seconds |
| `AZURE_COSMOS_PPCB_STALE_PARTITION_UNAVAILABILITY_REFRESH_INTERVAL_IN_SECONDS` | Interval for background refresh of partition health. | `60` seconds |

> [!NOTE]
> The SDK doesn't currently have a reliable failback trigger for reads. Instead, a background health checker gradually attempts to re-enable the original region when all four replicas are responsive.

### Comparing availability optimizations

- **Threshold-based availability strategy**: 
  - **Benefit**: Reduces tail latency by sending parallel read requests to secondary regions, and improves availability by preempting requests that result in network timeouts.
  - **Trade-off**: Incurs extra Request Units (RUs) costs compared to circuit breaker, due to additional parallel cross-region requests (though only during periods when thresholds are breached).
  - **Use case**: Optimal for read-heavy workloads where reducing latency is critical and some extra cost (both in terms of RU charge and client CPU pressure) is acceptable. Write operations can also benefit, if opted into nonidempotent write retry policy and the account has multi-region writes.

- **Partition-level circuit breaker**: 
  - **Benefit**: Improves availability and latency by avoiding unhealthy partitions, ensuring requests are routed to healthier regions.
  - **Trade-off**: Doesn't incur more RU costs, but can still allow some initial availability loss for requests that result in network timeouts. 
  - **Use case**: Ideal for write-heavy or mixed workloads where consistent performance is essential, especially when dealing with partitions that might intermittently become unhealthy.

Both strategies can be used together to enhance read and write availability and reduce tail latency. Partition-level circuit breaker can handle various transient failure scenarios, including those that could result in slow performing replicas, without the need to perform parallel requests. Additionally, adding threshold-based availability strategy further minimizes tail latency and eliminates availability loss, if extra RU cost is acceptable.

By implementing these strategies, developers can ensure their applications remain resilient, maintain high performance, and provide a better user experience even during regional outages or high-latency conditions.

### Excluded regions

The excluded regions feature enables fine-grained control over request routing by allowing you to exclude specific regions from your preferred locations on a per-request basis. This feature is available in Azure Cosmos DB .NET SDK version 3.37.0 and higher.

**Key benefits:**
- **Handle rate limiting**: When encountering 429 (Too Many Requests) responses, automatically route requests to alternate regions with available throughput
- **Targeted routing**: Ensure requests are served from specific regions by excluding all others
- **Bypass preferred order**: Override the default preferred regions list for individual requests without creating separate clients

**Configuration:**

Excluded regions can be configured at the request level using the `ExcludeRegions` property:

```csharp
CosmosClientOptions clientOptions = new CosmosClientOptions()
{
    ApplicationPreferredRegions = new List<string> {"West US", "Central US", "East US"}
};

CosmosClient client = new CosmosClient(connectionString, clientOptions);

Database db = client.GetDatabase("myDb");
Container container = db.GetContainer("myContainer");

//Request will be served out of the West US region
await container.ReadItemAsync<dynamic>("item", new PartitionKey("pk"));

//By using ExcludeRegions, we are able to bypass the ApplicationPreferredRegions list
// and route a request directly to the East US region
await container.ReadItemAsync<dynamic>(
  "item", 
  new PartitionKey("pk"),
  new ItemRequestOptions()
  {
    ExcludeRegions = new List<string>() { "West US", "Central US" }
  });
```

**Use case example - handling rate limiting:**

```csharp
ItemResponse<CosmosItem> item;
item = await container.ReadItemAsync<CosmosItem>("id", partitionKey);

if (item.StatusCode == HttpStatusCode.TooManyRequests)
{
    ItemRequestOptions requestOptions = new ItemRequestOptions()
    {
        ExcludeRegions = new List<string>() { "East US" }
    };

    item = await container.ReadItemAsync<CosmosItem>("id", partitionKey, requestOptions);
}
```

The feature also works with queries and other operations:

```csharp
QueryRequestOptions queryRequestOptions = new QueryRequestOptions()
{
    ExcludeRegions = new List<string>() { "East US" }
};

using (FeedIterator<CosmosItem> queryFeedIterator = container.GetItemQueryIterator<CosmosItem>(
    queryDefinition, 
    requestOptions: queryRequestOptions))
{
    while(queryFeedIterator.HasMoreResults)
    {
        var item = await queryFeedIterator.ReadNextAsync();
    }
}
```

#### Fine-tuning consistency vs availability

The excluded regions feature provides an additional mechanism for balancing consistency and availability trade-offs in your application. This capability is particularly valuable in dynamic scenarios where requirements may shift based on operational conditions:

**Dynamic outage handling**: When a primary region experiences an outage and partition-level circuit breaker thresholds prove insufficient, excluded regions enables immediate failover without code changes or application restarts. This provides faster response to regional issues compared to waiting for automatic circuit breaker activation.

**Conditional consistency preferences**: Applications can implement different consistency strategies based on operational state:
- **Steady state**: Prioritize consistent reads by excluding all regions except the primary, ensuring data consistency at the potential cost of availability
- **Outage scenarios**: Favor availability over strict consistency by allowing cross-region routing, accepting potential data lag in exchange for continued service availability

This approach allows external mechanisms (such as traffic managers or load balancers) to orchestrate failover decisions while the application maintains control over consistency requirements through region exclusion patterns.

When all regions are excluded, requests will be routed to the primary/hub region. This feature works with all request types including queries and is particularly useful for maintaining singleton client instances while achieving flexible routing behavior.

## Networking
<a id="direct-connection"></a>

**Connection policy: Use direct connection mode**

.NET V3 SDK default connection mode is direct with TCP protocol. You configure the connection mode when you create the `CosmosClient` instance in `CosmosClientOptions`. To learn more about different connectivity options, see the [connectivity modes](sdk-connection-modes.md) article.

```csharp
CosmosClient client = new CosmosClient(
  "<nosql-account-endpoint>",
  tokenCredential
  new CosmosClientOptions
  {
      ConnectionMode = ConnectionMode.Gateway // ConnectionMode.Direct is the default
  }
);
```

**Ephemeral port exhaustion**

If you see a high connection volume or high port usage on your instances, first verify that your client instances are singletons. In other words, the client instances should be unique for the lifetime of the application.

When it's running on the TCP protocol, the client optimizes for latency by using the long-lived connections. This is in contrast with the HTTPS protocol, which terminates the connections after two minutes of inactivity.

In scenarios where you have sparse access, and if you notice a higher connection count when compared to Gateway mode access, you can:

* Configure the [CosmosClientOptions.PortReuseMode](/dotnet/api/microsoft.azure.cosmos.cosmosclientoptions.portreusemode) property to `PrivatePortPool` (effective with framework versions 4.6.1 and later and .NET Core versions 2.0 and later). This property allows the SDK to use a small pool of ephemeral ports for various Azure Cosmos DB destination endpoints.
* Configure the [CosmosClientOptions.IdleTcpConnectionTimeout](/dotnet/api/microsoft.azure.cosmos.cosmosclientoptions.idletcpconnectiontimeout) property as greater than or equal to 10 minutes. The recommended values are from 20 minutes to 24 hours.

<a id="same-region"></a>

**For performance, collocate clients in the same Azure region**

When possible, place any applications that call Azure Cosmos DB in the same region as the Azure Cosmos DB database. Here's an approximate comparison: calls to Azure Cosmos DB within the same region finish within 1 millisecond (ms) to 2 ms, but the latency between the West and East coast of the US is more than 50 ms. This latency can vary from request to request, depending on the route taken by the request as it passes from the client to the Azure datacenter boundary. 

You can get the lowest possible latency by ensuring that the calling application is located within the same Azure region as the provisioned Azure Cosmos DB endpoint. For a list of available regions, see [Azure regions](https://azure.microsoft.com/regions/#services).

:::image type="content" source="./media/performance-tips/same-region.png" alt-text="Diagram that shows collocated clients in the same region.":::

   <a id="increase-threads"></a>

**Increase the number of threads/tasks**

Because calls to Azure Cosmos DB are made over the network, you might need to vary the degree of concurrency of your requests so that the client application spends minimal time waiting between requests. For example, if you're using the .NET [Task Parallel Library](/dotnet/standard/parallel-programming/task-parallel-library-tpl), create on the order of hundreds of tasks that read from or write to Azure Cosmos DB.

**Enable accelerated networking to reduce latency and CPU jitter**

It's recommended that you follow the instructions to enable [Accelerated Networking](/azure/virtual-network/accelerated-networking-overview) in your [Windows or Linux Azure VM](/azure/virtual-network/create-virtual-machine-accelerated-networking) in order to maximize performance.

Without accelerated networking, IO that transits between your Azure VM and other Azure resources might be unnecessarily routed through a host and virtual switch situated between the VM and its network card. Having the host and virtual switch inline in the datapath not only increases latency and jitter in the communication channel, it also steals CPU cycles from the VM. With accelerated networking, the VM interfaces directly with the NIC without intermediaries; any network policy details that were handled by the host and virtual switch are now handled in hardware at the NIC; the host and virtual switch are bypassed. Generally you can expect lower latency and higher throughput, as well as more *consistent* latency and decreased CPU utilization when you enable accelerated networking.

Limitations: accelerated networking must be supported on the VM OS, and can only be enabled when the VM is stopped and deallocated. The VM can't be deployed with Azure Resource Manager. [App Service](/azure/app-service/overview) has no accelerated network enabled.

For more details, see the [Windows and Linux](/azure/virtual-network/create-virtual-machine-accelerated-networking) instructions.

## <a id="sdk-usage"></a> SDK usage

**Install the most recent SDK**

The Azure Cosmos DB SDKs are constantly being improved to provide the best performance. To determine the most recent SDK and review improvements, see [Azure Cosmos DB SDK](sdk-dotnet-v3.md).

**Use stream APIs**

[.NET SDK V3](https://github.com/Azure/azure-cosmos-dotnet-v3) contains stream APIs that can receive and return data without serializing. 

Middle-tier applications that don't consume responses directly from the SDK but relay them to other application tiers can benefit from the stream APIs. For examples of stream handling, see the [item management](https://github.com/Azure/azure-cosmos-dotnet-v3/blob/master/Microsoft.Azure.Cosmos.Samples/Usage/ItemManagement) samples.

**Use a singleton Azure Cosmos DB client for the lifetime of your application**

Each `CosmosClient` instance is thread-safe and performs efficient connection management and address caching when it operates in direct mode. To allow efficient connection management and better SDK client performance, we recommend that you use a single instance per `AppDomain` for the lifetime of the application for each account your application interacts with.

For multitenant applications handling multiple accounts, see the [related best practices](best-practice-dotnet.md#best-practices-for-multi-tenant-applications).

When you're working on Azure Functions, instances should also follow the existing [guidelines](/azure/azure-functions/manage-connections#static-clients) and maintain a single instance.

**Avoid blocking calls**

Azure Cosmos DB SDK should be designed to process many requests simultaneously. Asynchronous APIs allow a small pool of threads to handle thousands of concurrent requests by not waiting on blocking calls. Rather than waiting on a long-running synchronous task to complete, the thread can work on another request.

A common performance problem in apps using the Azure Cosmos DB SDK is blocking calls that could be asynchronous. Many synchronous blocking calls lead to [thread pool starvation](/archive/blogs/vancem/diagnosing-net-core-threadpool-starvation-with-perfview-why-my-service-is-not-saturating-all-cores-or-seems-to-stall) and degraded response times.

**Do not**:

* Block asynchronous execution by calling [Task.Wait](/dotnet/api/system.threading.tasks.task.wait) or [Task.Result](/dotnet/api/system.threading.tasks.task-1.result).
* Use [Task.Run](/dotnet/api/system.threading.tasks.task.run) to make a synchronous API asynchronous.
* Acquire locks in common code paths. Azure Cosmos DB .NET SDK is most performant when architected to run code in parallel.
* Call [Task.Run](/dotnet/api/system.threading.tasks.task.run) and immediately await it. ASP.NET Core already runs app code on normal Thread Pool threads, so calling Task.Run only results in extra unnecessary thread pool scheduling. Even if the scheduled code would block a thread, Task.Run doesn't prevent that.
* Don't use ToList() on `Container.GetItemLinqQueryable<T>()`, which uses blocking calls to synchronously drain the query. Use [ToFeedIterator()](https://github.com/Azure/azure-cosmos-dotnet-v3/blob/e2029f2f4854c0e4decd399c35e69ef799db9f35/Microsoft.Azure.Cosmos/src/Resource/Container/Container.cs#L1143) to drain the query asynchronously.

**Do**:

* Call the Azure Cosmos DB .NET APIs asynchronously.
* The entire call stack is asynchronous in order to benefit from [async/await](/dotnet/csharp/programming-guide/concepts/async/) patterns.

A profiler, such as [PerfView](https://github.com/Microsoft/perfview), can be used to find threads frequently added to the [thread pool](/windows/desktop/procthread/thread-pools). The `Microsoft-Windows-DotNETRuntime/ThreadPoolWorkerThread/Start` event indicates a thread added to the thread pool.

**Disable content response on write operations**

For workloads that have heavy create payloads, set the `EnableContentResponseOnWrite` request option to `false`. The service no longer returns the created or updated resource to the SDK. Normally, because the application has the object that's being created, it doesn't need the service to return it. The header values are still accessible, like a request charge. Disabling the content response can help improve performance, because the SDK no longer needs to allocate memory or serialize the body of the response. It also reduces the network bandwidth usage to further help performance.  

```csharp
ItemRequestOptions requestOptions = new ItemRequestOptions() { EnableContentResponseOnWrite = false };
ItemResponse<Book> itemResponse = await this.container.CreateItemAsync<Book>(book, new PartitionKey(book.pk), requestOptions);
// Resource will be null
itemResponse.Resource
```

**Enable Bulk to optimize for throughput instead of latency**

Enable *Bulk* for scenarios where the workload requires a large amount of throughput, and latency isn't as important. For more information about how to enable the Bulk feature, and to learn which scenarios it should be used for, see [Introduction to Bulk support](https://devblogs.microsoft.com/cosmosdb/introducing-bulk-support-in-the-net-sdk).

<a id="max-connection"></a>**Increase System.Net MaxConnections per host when you use Gateway mode**

Azure Cosmos DB requests are made over HTTPS/REST when you use Gateway mode. They're subject to the default connection limit per hostname or IP address. You might need to set `MaxConnections` to a higher value (from 100 through 1,000) so that the client library can use multiple simultaneous connections to Azure Cosmos DB. In .NET SDK 1.8.0 and later, the default value for [ServicePointManager.DefaultConnectionLimit](/dotnet/api/system.net.servicepointmanager.defaultconnectionlimit) is 50. To change the value, you can set [`Documents.Client.ConnectionPolicy.MaxConnectionLimit`](/dotnet/api/microsoft.azure.cosmos.cosmosclientoptions.gatewaymodemaxconnectionlimit) to a higher value.

**Increase the number of threads/tasks**

See [Increase the number of threads/tasks](#increase-threads) in the Networking section of this article.

## Managing Newtonsoft.Json Dependencies

[!INCLUDE [dotnet-json-dependency](includes/dotnet-json-dependency.md)]

## Query operations

For query operations, see the [performance tips for queries](performance-tips-query-sdk.md?tabs=v3&pivots=programming-language-csharp).

## <a id="indexing-policy"></a> Indexing policy
 
**Exclude unused paths from indexing for faster writes**

The Azure Cosmos DB indexing policy also allows you to specify which document paths to include or exclude from indexing by using indexing paths (*IndexingPolicy.IncludedPaths* and *IndexingPolicy.ExcludedPaths*). 

Indexing only the paths you need can improve write performance, reduce RU charges on write operations, and reduce index storage for scenarios in which the query patterns are known beforehand. This is because indexing costs correlate directly to the number of unique paths indexed. For example, the following code shows how to exclude an entire section of the documents (a subtree) from indexing by using the `*` wildcard:

```csharp
var containerProperties = new ContainerProperties(id: "excludedPathCollection", partitionKeyPath: "/pk" );
containerProperties.IndexingPolicy.IncludedPaths.Add(new IncludedPath { Path = "/*" });
containerProperties.IndexingPolicy.ExcludedPaths.Add(new ExcludedPath { Path = "/nonIndexedContent/*");
Container container = await this.cosmosDatabase.CreateContainerAsync(containerProperties);
```

For more information, see [Azure Cosmos DB indexing policies](index-policy.md).

## Throughput
<a id="measure-rus"></a>

**Measure and tune for lower RU/s usage**

Azure Cosmos DB offers a rich set of database operations. These operations include relational and hierarchical queries with user-defined functions (UDFs), stored procedures, and triggers, all operating on the documents within a database collection. 

The costs associated with each of these operations vary depending on the CPU, IO, and memory that are required to complete the operation. Instead of thinking about and managing hardware resources, you can think of a Request Unit as a single measure for the resources that are required to perform various database operations and service an application request.

Throughput is provisioned based on the number of [Request Units](request-units.md) set for each container. RU consumption is evaluated as a units-per-second rate. Applications that exceed the provisioned RU rate for their container are limited until the rate drops below the provisioned level for the container. If your application requires a higher level of throughput, you can increase your throughput by provisioning more RUs.

The complexity of a query affects how many RUs are consumed for an operation. The number of predicates, the nature of the predicates, the number of UDF files, and the size of the source dataset all influence the cost of query operations.

To measure the overhead of any operation (create, update, or delete), inspect the [x-ms-request-charge](/rest/api/cosmos-db/common-cosmosdb-rest-response-headers) header (or the equivalent `RequestCharge` property in `ResourceResponse<T>` or `FeedResponse<T>` in the .NET SDK) to measure the number of RUs consumed by the operations:

```csharp
// Measure the performance (Request Units) of writes
ItemResponse<Book> response = await container.CreateItemAsync<Book>(myBook, new PartitionKey(myBook.PkValue));
Console.WriteLine("Insert of item consumed {0} request units", response.RequestCharge);
// Measure the performance (Request Units) of queries
FeedIterator<Book> queryable = container.GetItemQueryIterator<ToDoActivity>(queryString);
while (queryable.HasMoreResults)
    {
        FeedResponse<Book> queryResponse = await queryable.ExecuteNextAsync<Book>();
        Console.WriteLine("Query batch consumed {0} request units", queryResponse.RequestCharge);
    }
```

The request charge that's returned in this header is a fraction of your provisioned throughput (that is, 2,000 RU/s). For example, if the preceding query returns 1,000 1-KB documents, the cost of the operation is 1,000. So, within one second, the server honors only two such requests before it rate-limits later requests. For more information, see [Request Units](request-units.md) and the [Request Unit calculator](https://cosmos.azure.com/capacitycalculator).
<a id="429"></a>

**Handle rate limiting/request rate too large**

When a client attempts to exceed the reserved throughput for an account, there's no performance degradation at the server and no use of throughput capacity beyond the reserved level. The server preemptively ends the request with RequestRateTooLarge (HTTP status code 429). It returns an [x-ms-retry-after-ms](/rest/api/cosmos-db/common-cosmosdb-rest-response-headers) header that indicates the amount of time, in milliseconds, that the user must wait before attempting the request again.

```xml
    HTTP Status 429,
    Status Line: RequestRateTooLarge
    x-ms-retry-after-ms :100
```

The SDKs all implicitly catch this response, respect the server-specified retry-after header, and retry the request. Unless your account is being accessed concurrently by multiple clients, the next retry will succeed.

If you have more than one client cumulatively operating consistently above the request rate, the default retry count that's currently set to 9 internally by the client might not suffice. In this case, the client throws a CosmosException with status code 429 to the application. 

You can change the default retry count by setting the `RetryOptions` on the `CosmosClientOptions` instance. By default, the CosmosException with status code 429 is returned after a cumulative wait time of 30 seconds if the request continues to operate above the request rate. This error is returned even when the current retry count is less than the maximum retry count, whether the current value is the default of 9 or a user-defined value.

The automated retry behavior helps improve resiliency and usability for most applications. But it might not be the best behavior when you're doing performance benchmarks, especially when you're measuring latency. The client-observed latency will spike if the experiment hits the server throttle and causes the client SDK to silently retry. To avoid latency spikes during performance experiments, measure the charge that's returned by each operation, and ensure that requests are operating below the reserved request rate. 

For more information, see [Request Units](request-units.md).

**For higher throughput, design for smaller documents**

The request charge (that is, the request-processing cost) of a specified operation correlates directly to the size of the document. Operations on large documents cost more than operations on small documents.

## Next steps

- [Measure Azure Cosmos DB for NoSQL performance with a benchmarking framework](benchmarking-framework.md)
- [Partitioning and horizontal scaling in Azure Cosmos DB](partitioning-overview.md)
