---
title: Manage Consistency
description: "Learn how to configure and manage consistency levels in Azure Cosmos DB using Azure portal, .NET SDK, Java SDK, and various other SDKs."
author: markjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 07/09/2025
ms.author: mjbrown
ms.devlang: csharp
# ms.devlang: csharp, java, javascript

ms.custom: devx-track-js, devx-track-csharp, devx-track-azurecli, devx-track-azurepowershell, devx-track-dotnet, devx-track-extended-java
appliesto:
  - ✅ NoSQL
---

# Manage consistency levels in Azure Cosmos DB

This article explains how to manage consistency levels in Azure Cosmos DB. You learn how to configure the default consistency level, override the default consistency, manually manage session tokens, and understand the Probabilistically Bounded Staleness (PBS) metric.

As you change your account level consistency, ensure you redeploy your applications and make any necessary code modifications to apply these changes.

[!INCLUDE [updated-for-az](~/reusable-content/ce-skilling/azure/includes/updated-for-az.md)]

## Configure the default consistency level

To learn more about the default consistency level, see [Consistency levels in Azure Cosmos DB](consistency-levels.md).

# [Azure portal](#tab/portal)

To view or modify the default consistency level:

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Find your Azure Cosmos DB account, and open the **Default consistency** pane.

1. Select the level of consistency you want as the new default, and then select **Save**.

The Azure portal also provides a visualization of different consistency levels with music notes.

:::image type="content" source="./media/how-to-manage-consistency/consistency-settings.png" alt-text="Screenshot of the consistency menu in the Azure portal." lightbox="./media/how-to-manage-consistency/consistency-settings.png":::

# [CLI](#tab/cli)

Create an Azure Cosmos DB account with *Session* consistency, then update the default consistency.

```azurecli
# Create a new account with Session consistency
az cosmosdb create --name $accountName --resource-group $resourceGroupName --default-consistency-level Session

# Update an existing account's default consistency
az cosmosdb update --name $accountName --resource-group $resourceGroupName --default-consistency-level Strong
```

# [PowerShell](#tab/powershell)

Create an Azure Cosmos DB account with *Session* consistency, then update the default consistency.

```azurepowershell-interactive
# Create a new account with Session consistency
New-AzCosmosDBAccount -ResourceGroupName $resourceGroupName `
  -Location $locations -Name $accountName -DefaultConsistencyLevel "Session"

# Update an existing account's default consistency
Update-AzCosmosDBAccount -ResourceGroupName $resourceGroupName `
  -Name $accountName -DefaultConsistencyLevel "Strong"
```

---

## Override the default consistency level

The service sets the default consistency level, but clients can override it. The consistency level can be set on a per-request basis, which overrides the default consistency level set at the account level.

> [!TIP]
> Consistency can only be **relaxed** at the SDK instance or request level. To move from weaker to stronger consistency, update the default consistency for the Azure Cosmos DB account.

> [!TIP]
> Overriding the default consistency level only applies to reads within the SDK client. An account configured for strong consistency by default still writes and replicates data synchronously to every region in the account. When the SDK client instance or request overrides this level with Session or weaker consistency, reads are performed using a single replica. For more information, see [Consistency levels and throughput](consistency-levels.md#consistency-levels-and-throughput).

### <a id="override-default-consistency-dotnet"></a>.NET SDK

# [.NET SDK V2](#tab/dotnetv2)

```csharp
// Override consistency at the client level
documentClient = new DocumentClient(new Uri(endpoint), authKey, connectionPolicy, ConsistencyLevel.Eventual);

// Override consistency at the request level via request options
RequestOptions requestOptions = new RequestOptions { ConsistencyLevel = ConsistencyLevel.Eventual };

var response = await client.ReadDocumentAsync(collectionUri, document, requestOptions);
```

# [.NET SDK V3](#tab/dotnetv3)

```csharp
// Override consistency at the request level via request options
ItemRequestOptions requestOptions = new ItemRequestOptions { ConsistencyLevel = ConsistencyLevel.Eventual };

var response = await client.GetContainer(databaseName, containerName)
    .ReadItemAsync(
        item,
        new PartitionKey(itemPartitionKey),
        requestOptions);
```
---

### <a id="override-default-consistency-javav4"></a> Java V4 SDK

# [Async](#tab/api-async)

   Java SDK V4 (Maven com.azure::azure-cosmos) Async API

   [!code-java[](~/azure-cosmos-java-sql-api-samples/src/main/java/com/azure/cosmos/examples/documentationsnippets/async/SampleDocumentationSnippetsAsync.java?name=ManageConsistencyAsync)]

# [Sync](#tab/api-sync)

   Java SDK V4 (Maven com.azure::azure-cosmos) Sync API

   [!code-java[](~/azure-cosmos-java-sql-api-samples/src/main/java/com/azure/cosmos/examples/documentationsnippets/sync/SampleDocumentationSnippets.java?name=ManageConsistencySync)]

--- 

### <a id="override-default-consistency-javav2"></a> Java V2 SDKs

# [Async](#tab/api-async)

Async Java V2 SDK (Maven com.microsoft.azure::azure-cosmosdb)

```java
// Override consistency at the client level
ConnectionPolicy policy = new ConnectionPolicy();

AsyncDocumentClient client =
        new AsyncDocumentClient.Builder()
                .withMasterKey(this.accountKey)
                .withServiceEndpoint(this.accountEndpoint)
                .withConsistencyLevel(ConsistencyLevel.Eventual)
                .withConnectionPolicy(policy).build();
```

# [Sync](#tab/api-sync)

Sync Java V2 SDK (Maven com.microsoft.azure::azure-documentdb)

```java
// Override consistency at the client level
ConnectionPolicy connectionPolicy = new ConnectionPolicy();
DocumentClient client = new DocumentClient(accountEndpoint, accountKey, connectionPolicy, ConsistencyLevel.Eventual);
```
---

### <a id="override-default-consistency-javascript"></a>Node.js/JavaScript/TypeScript SDK

```javascript
// Override consistency at the client level
const client = new CosmosClient({
  /* other config... */
  consistencyLevel: ConsistencyLevel.Eventual
});

// Override consistency at the request level via request options
const { body } = await item.read({ consistencyLevel: ConsistencyLevel.Eventual });
```

### <a id="override-default-consistency-python"></a>Python SDK

```python
# Override consistency at the client level
connection_policy = documents.ConnectionPolicy()
client = cosmos_client.CosmosClient(self.account_endpoint, {
                                    'masterKey': self.account_key}, connection_policy, documents.ConsistencyLevel.Eventual)
```

### <a id="override-default-consistency-go"></a>Go SDK

Define consistency level at the request:

```go
container, _ := c.NewContainer("moviesdb", "movies")

container.NewQueryItemsPager("select * from c", azcosmos.NewPartitionKey(), &azcosmos.QueryOptions{
		ConsistencyLevel: azcosmos.ConsistencyLevelEventual.ToPtr(),
})

container.ReadItem(context.Background(), azcosmos.NewPartitionKeyString("Quentin Tarantino"), "Pulp Fiction", &azcosmos.ItemOptions{
		ConsistencyLevel: azcosmos.ConsistencyLevelStrong.ToPtr(),
})
```

## Utilize session tokens

One of the consistency levels in Azure Cosmos DB is *session* consistency. This level is the default level applied to Azure Cosmos DB accounts. When working with session consistency, every new write request to Azure Cosmos DB is assigned a new SessionToken. The CosmosClient uses this token internally with each read/query request to ensure that the set consistency level is maintained.

In some scenarios, you need to manage this session yourself. Consider a web application with multiple nodes, each node has its own instance of CosmosClient. If you want these nodes to participate in the same session (to be able to read your own writes consistently across web tiers) you would have to send the SessionToken from FeedResponse\<T\> of the write action to the end-user using a cookie or some other mechanism, and have that token flow back to the web tier and ultimately the CosmosClient for subsequent reads. If you're using a round-robin load balancer that doesn't maintain session affinity between requests, such as the Azure Load Balancer, the read could potentially land on a different node to the write request, where the session was created.

If you don't flow the Azure Cosmos DB SessionToken across, you could end up with inconsistent read results for a while.

Session tokens in Azure Cosmos DB are partition-bound, meaning they're exclusively associated with one partition. In order to ensure you can read your writes, use the session token that was last generated for the relevant items. To manage session tokens manually, get the session token from the response and set them per request. If you don't need to manage session tokens manually, you don't need to use these samples. The SDK keeps track of session tokens automatically. If you don't set the session token manually, by default, the SDK uses the most recent session token.

### <a id="utilize-session-tokens-dotnet"></a>.NET SDK

# [.NET SDK V2](#tab/dotnetv2)

```csharp
var response = await client.ReadDocumentAsync(
                UriFactory.CreateDocumentUri(databaseName, collectionName, "SalesOrder1"));
string sessionToken = response.SessionToken;

RequestOptions options = new RequestOptions();
options.SessionToken = sessionToken;
var response = await client.ReadDocumentAsync(
                UriFactory.CreateDocumentUri(databaseName, collectionName, "SalesOrder1"), options);
```

# [.NET SDK V3](#tab/dotnetv3)

```csharp
Container container = client.GetContainer(databaseName, collectionName);
ItemResponse<SalesOrder> response = await container.CreateItemAsync<SalesOrder>(salesOrder);
string sessionToken = response.Headers.Session;

ItemRequestOptions options = new ItemRequestOptions();
options.SessionToken = sessionToken;
ItemResponse<SalesOrder> response = await container.ReadItemAsync<SalesOrder>(salesOrder.Id, new PartitionKey(salesOrder.PartitionKey), options);
```
---

### <a id="override-default-consistency-javav4"></a> Java V4 SDK

# [Async](#tab/api-async)

   Java SDK V4 (Maven com.azure::azure-cosmos) Async API

   [!code-java[](~/azure-cosmos-java-sql-api-samples/src/main/java/com/azure/cosmos/examples/documentationsnippets/async/SampleDocumentationSnippetsAsync.java?name=ManageConsistencySessionAsync)]

# [Sync](#tab/api-sync)

   Java SDK V4 (Maven com.azure::azure-cosmos) Sync API

   [!code-java[](~/azure-cosmos-java-sql-api-samples/src/main/java/com/azure/cosmos/examples/documentationsnippets/sync/SampleDocumentationSnippets.java?name=ManageConsistencySessionSync)]

--- 

### <a id="utilize-session-tokens-javav2"></a>Java V2 SDKs

# [Async](#tab/api-async)

Async Java V2 SDK (Maven com.microsoft.azure::azure-cosmosdb)

```java
// Get session token from response
RequestOptions options = new RequestOptions();
options.setPartitionKey(new PartitionKey(document.get("mypk")));
Observable<ResourceResponse<Document>> readObservable = client.readDocument(document.getSelfLink(), options);
readObservable.single()           // we know there will be one response
  .subscribe(
      documentResourceResponse -> {
          System.out.println(documentResourceResponse.getSessionToken());
      },
      error -> {
          System.err.println("an error happened: " + error.getMessage());
      });

// Resume the session by setting the session token on RequestOptions
RequestOptions options = new RequestOptions();
requestOptions.setSessionToken(sessionToken);
Observable<ResourceResponse<Document>> readObservable = client.readDocument(document.getSelfLink(), options);
```

# [Sync](#tab/api-sync)

Sync Java V2 SDK (Maven com.microsoft.azure::azure-documentdb)

```java
// Get session token from response
ResourceResponse<Document> response = client.readDocument(documentLink, null);
String sessionToken = response.getSessionToken();

// Resume the session by setting the session token on the RequestOptions
RequestOptions options = new RequestOptions();
options.setSessionToken(sessionToken);
ResourceResponse<Document> response = client.readDocument(documentLink, options);
```
---

### <a id="utilize-session-tokens-javascript"></a>Node.js/JavaScript/TypeScript SDK

```javascript
// Get session token from response
const { headers, item } = await container.items.create({ id: "meaningful-id" });
const sessionToken = headers["x-ms-session-token"];

// Immediately or later, you can use that sessionToken from the header to resume that session.
const { body } = await item.read({ sessionToken });
```

### <a id="utilize-session-tokens-python"></a>Python SDK

```python
// Get the session token from the last response headers
item = client.ReadItem(item_link)
session_token = client.last_response_headers["x-ms-session-token"]

// Resume the session by setting the session token on the options for the request
options = {
    "sessionToken": session_token
}
item = client.ReadItem(doc_link, options)
```

### <a id="utilize-session-tokens-go"></a>Go SDK

```go
// Get the session token from the create item response
resp, _ := container.CreateItem(context.Background(), azcosmos.NewPartitionKeyString("Quentin Tarantino"), movie, &azcosmos.ItemOptions{
	ConsistencyLevel: azcosmos.ConsistencyLevelSession.ToPtr(),
})

// Use the session token to read the item
container.ReadItem(context.Background(), azcosmos.NewPartitionKeyString("Quentin Tarantino"), movieId, &azcosmos.ItemOptions{
	SessionToken: resp.SessionToken,
})
```

## Monitor Probabilistically Bounded Staleness metric

How eventual is eventual consistency? For the average case, we can offer staleness bounds with respect to version history and time. The [Probabilistically Bounded Staleness (PBS)](http://pbs.cs.berkeley.edu/) metric tries to quantify the probability of staleness and shows it as a metric.

To view the PBS metric:

1. Go to your Azure Cosmos DB account in the Azure portal.

1. Open the **Metrics (Classic)** pane, and select the **Consistency** tab.

1. Look at the graph named **Probability of strongly consistent reads based on your workload (see PBS)**.

  :::image type="content" source="./media/how-to-manage-consistency/pbs-metric.png" alt-text="Screenshot of the Probabilistically Bounded Staleness graph in the Azure portal.":::

## Next steps

Learn more about how to manage data conflicts, or move on to the next key concept in Azure Cosmos DB.

* [Consistency Levels in Azure Cosmos DB](consistency-levels.md)
* [Partitioning and horizontal scaling](partitioning.md)
* [Manage conflict resolution policies](how-to-manage-conflicts.md)
* [Consistency tradeoffs in modern distributed database systems design](https://www.computer.org/csdl/magazine/co/2012/02/mco2012020037/13rRUxjyX7k)
* [High availability (Reliability) in Azure Cosmos DB for NoSQL](/azure/reliability/reliability-cosmos-db-nosql)
* [Azure Cosmos DB service level agreements](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services)
