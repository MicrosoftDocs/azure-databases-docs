---
title: Manage indexing policies in Azure Cosmos DB
description: Learn how to manage indexing policies, include or exclude a property from indexing, how to define indexing using different Azure Cosmos DB SDKs.
author: markjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 12/03/2024
ms.author: mjbrown
ms.custom: devx-track-csharp, build-2024, ignite-2024
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
---

# Manage indexing policies in Azure Cosmos DB

In Azure Cosmos DB, data is indexed following [indexing policies](../index-policy.md) that are defined for each container. The default indexing policy for newly created containers enforces range indexes for any string or number. You can override this policy with your own custom indexing policy.

> [!NOTE]
> The method of updating indexing policies described in this article only applies to Azure Cosmos DB for NoSQL. Learn about indexing in [Azure Cosmos DB for MongoDB](../mongodb/indexing.md) and [Secondary indexing in Azure Cosmos DB for Apache Cassandra](../cassandra/secondary-indexing.md).

## Indexing policy examples

Here are some examples of indexing policies shown in [their JSON format](../index-policy.md). They're exposed on the Azure portal in JSON format. The same parameters can be set through the Azure CLI or any SDK.

### Opt-out policy to selectively exclude some property paths

```json
{
    "indexingMode": "consistent",
    "includedPaths": [
        {
            "path": "/*"
        }
    ],
    "excludedPaths": [
        {
            "path": "/path/to/single/excluded/property/?"
        },
        {
            "path": "/path/to/root/of/multiple/excluded/properties/*"
        }
    ]
}
```

### Opt-in policy to selectively include some property paths

```json
{
    "indexingMode": "consistent",
    "includedPaths": [
        {
            "path": "/path/to/included/property/?"
        },
        {
            "path": "/path/to/root/of/multiple/included/properties/*"
        }
    ],
    "excludedPaths": [
        {
            "path": "/*"
        }
    ]
}
```

> [!NOTE]
> We generally recommend that you use an *opt-out* indexing policy. Azure Cosmos DB proactively indexes any new property that might be added to your data model.

### Using a spatial index on a specific property path only

```json
{
    "indexingMode": "consistent",
    "automatic": true,
    "includedPaths": [
        {
            "path": "/*"
        }
    ],
    "excludedPaths": [
        {
            "path": "/_etag/?"
        }
    ],
    "spatialIndexes": [
        {
                    "path": "/path/to/geojson/property/?",
            "types": [
                "Point",
                "Polygon",
                "MultiPolygon",
                "LineString"
            ]
        }
    ]
}
```

## Vector indexing policy examples

In addition to including or excluding paths for individual properties, you can also specify a [vector index](../index-policy.md#vector-indexes). In general, vector indexes should be specified whenever the `VectorDistance` system function is used to measure similarity between a query vector and a vector property.

> [!NOTE]
> Before proceeding, you must enable the [Azure Cosmos DB NoSQL Vector Indexing and Search](vector-search.md#enable-the-vector-indexing-and-search-feature).

>[!IMPORTANT]
> A vector indexing policy must be on the same path defined in the container's vector policy. [Learn more about container vector policies](vector-search.md#container-vector-policies).

```json
{
    "indexingMode": "consistent",
    "automatic": true,
    "includedPaths": [
        {
            "path": "/*"
        }
    ],
    "excludedPaths": [
        {
            "path": "/_etag/?"
        },
        {
            "path": "/vector/*"
        }
    ],
    "vectorIndexes": [
        {
            "path": "/vector",
            "type": "quantizedFlat"
        }
    ]
}
```

> [!IMPORTANT]
> The vector path added to the "excludedPaths" section of the indexing policy to ensure optimized performance for insertion. Not adding the vector path to "excludedPaths" will result in higher RU charge and latency for vector insertions.

> [!IMPORTANT]
> Currently, vector policies and vector indexes are immutable after creation. To make changes, please create a new collection.

You can define the following types of vector index policies:

| Type | Description | Max dimensions |
| --- | --- |
| **`flat`** | Stores vectors on the same index as other indexed properties. | 505 |
| **`quantizedFlat`** | Quantizes (compresses) vectors before storing on the index. This can improve latency and throughput at the cost of a small amount of accuracy. | 4096 |
| **`diskANN`** | Creates an index based on DiskANN for fast and efficient approximate search. | 4096 |

The `flat` and `quantizedFlat` index types leverage Azure Cosmos DB's index to store and read each vector when performing a vector search. Vector searches with a `flat` index are brute-force searches and produce 100% accuracy. However, there is a limitation of `505` dimensions for vectors on a flat index.

The `quantizedFlat` index stores quantized or compressed vectors on the index. Vector searches with `quantizedFlat` index are also brute-force searches, however their accuracy might be slightly less than 100% since the vectors are quantized before adding to the index. However, vector searches with `quantized flat` should have lower latency, higher throughput, and lower RU cost than vector searches on a `flat` index. This is a good option for scenarios where you are using query filters to narrow down the vector search to a relatively small set of vectors. 

The `diskANN` index is a separate index defined specifically for vectors leveraging [DiskANN](https://www.microsoft.com/research/publication/diskann-fast-accurate-billion-point-nearest-neighbor-search-on-a-single-node/), a suite of highly performant vector indexing algorithms developed by Microsoft Research. DiskANN indexes can offer some of the lowest latency, highest query-per-second (QPS), and lowest RU cost queries at high accuracy. However, since DiskANN is an approximate nearest neighbors (ANN) index, the accuracy may be lower than `quantizedFlat` or `flat`.

The `diskANN` and `quantizedFlat` indexes can take optional index build parameters that can be used to tune the accuracy vs latency trade-off that applies to every Approximate Nearest Neighbors vector index.

- `quantizationByteSize`: Sets the size (in bytes) for product quantization. Min=1, Default=dynamic (system decides), Max=512. Setting this larger may result in higher accuracy vector searches at expense of higher RU cost and higher latency. This applies to both `quantizedFlat` and `DiskANN` index types.
- `indexingSearchListSize`: Sets how many vectors to search over during index build construction. Min=10, Default=100, Max=500. Setting this larger may result in higher accuracy vector searches at the expense of longer index build times and higher vector ingest latencies. This applies to `DiskANN` indexes only.

### Tuple indexing policy examples

This example indexing policy defines a tuple index on events.name and events.category

```json
{  
    "automatic":true,
    "indexingMode":"Consistent",
    "includedPaths":[  
        {"path":"/*"}, 
        {"path":"/events/[]/{name,category}/?"} 
    ],
    "excludedPaths":[],
    "compositeIndexes":[]
}
```

The above index is used for the below query.

```sql
SELECT * 
FROM root r 
WHERE 
   EXISTS (SELECT VALUE 1 FROM ev IN r.events 
           WHERE ev.name = ‘M&M’ AND ev.category = ‘Candy’) 
```

## Composite indexing policy examples

In addition to including or excluding paths for individual properties, you can also specify a composite index. To perform a query that has an `ORDER BY` clause for multiple properties, a [composite index](../index-policy.md#composite-indexes) is required on those properties. If the query includes filters along with sorting on multiple properties, you may need more than one composite index.

Composite indexes also have a performance benefit for queries that have multiple filters or both a filter and an ORDER BY clause.

> [!NOTE]
> Composite paths have an implicit `/?` since only the scalar value at that path is indexed. The `/*` wildcard is not supported in composite paths. You shouldn't specify `/?` or `/*` in a composite path. Composite paths are also case-sensitive.

### Composite index defined for (name asc, age desc)

```json
{  
    "automatic":true,
    "indexingMode":"Consistent",
    "includedPaths":[  
        {  
            "path":"/*"
        }
    ],
    "excludedPaths":[],
    "compositeIndexes":[  
        [  
            {  
                "path":"/name",
                "order":"ascending"
            },
            {  
                "path":"/age",
                "order":"descending"
            }
        ]
    ]
}
```

The composite index on name and age is required for the following queries:

Query #1:

```sql
SELECT *
FROM c
ORDER BY c.name ASC, c.age DESC
```

Query #2:

```sql
SELECT *
FROM c
ORDER BY c.name DESC, c.age ASC
```

This composite index benefits the following queries and optimizes the filters:

Query #3:

```sql
SELECT *
FROM c
WHERE c.name = "Tim"
ORDER BY c.name DESC, c.age ASC
```

Query #4:

```sql
SELECT *
FROM c
WHERE c.name = "Tim" AND c.age > 18
```

### Composite index defined for (name ASC, age ASC) and (name ASC, age DESC)

You can define multiple composite indexes within the same indexing policy.

```json
{  
    "automatic":true,
    "indexingMode":"Consistent",
    "includedPaths":[  
        {  
            "path":"/*"
        }
    ],
    "excludedPaths":[],
    "compositeIndexes":[  
        [  
            {  
                "path":"/name",
                "order":"ascending"
            },
            {  
                "path":"/age",
                "order":"ascending"
            }
        ],
        [  
            {  
                "path":"/name",
                "order":"ascending"
            },
            {  
                "path":"/age",
                "order":"descending"
            }
        ]
    ]
}
```

### Composite index defined for (name ASC, age ASC)

It's optional to specify the order. If not specified, the order is ascending.

```json
{  
    "automatic":true,
    "indexingMode":"Consistent",
    "includedPaths":[  
        {  
            "path":"/*"
        }
    ],
    "excludedPaths":[],
    "compositeIndexes":[  
        [  
            {  
               "path":"/name"
            },
            {  
               "path":"/age"
            }
        ]
    ]
}
```

### Exclude all property paths but keeping indexing active

You can use this policy where the [Time-to-Live (TTL) feature](time-to-live.md) is active but no other indexes are necessary to use Azure Cosmos DB as a pure key-value store.

```json
{
    "indexingMode": "consistent",
    "includedPaths": [],
    "excludedPaths": [{
        "path": "/*"
    }]
}
```

### No indexing

This policy turns off indexing. If `indexingMode` is set to `none`, you can't set a TTL on the container.

```json
{
    "indexingMode": "none"
}
```

## Updating indexing policy

In Azure Cosmos DB, the indexing policy can be updated using any of the following methods:

- From the Azure portal
- Using the Azure CLI
- Using PowerShell
- Using one of the SDKs

An [indexing policy update](../index-policy.md#modifying-the-indexing-policy) triggers an index transformation. The progress of this transformation can also be tracked from the SDKs.

> [!NOTE]
> When you update indexing policy, writes to Azure Cosmos DB are uninterrupted. Learn more about [indexing transformations](../index-policy.md#modifying-the-indexing-policy).

> [!IMPORTANT]
> Removing an index takes effect immediately, whereas adding a new index takes some time as it requires an indexing transformation. When replacing one index with another (for example, replacing a single property index with a composite-index) make sure to add the new index first and then wait for the index transformation to complete **before** you remove the previous index from the indexing policy. Otherwise this will negatively affect your ability to query the previous index and may break any active workloads that reference the previous index.

### Use the Azure portal

Azure Cosmos DB containers store their indexing policy as a JSON document that the Azure portal lets you directly edit.

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. Create a new Azure Cosmos DB account or select an existing account.

1. Open the **Data Explorer** pane and select the container that you want to work on.

1. Select **Scale & Settings**.

1. Modify the indexing policy JSON document, as shown in these [examples](#indexing-policy-examples).

1. Select **Save** when you're done.

:::image type="content" source="./media/how-to-manage-indexing-policy/indexing-policy-portal.png" alt-text="Manage Indexing using Azure portal":::

### Use the Azure CLI

To create a container with a custom indexing policy, see [Create a container with a custom index policy using CLI](manage-with-cli.md#create-a-container-with-a-custom-index-policy).

### Use PowerShell

To create a container with a custom indexing policy, see [Create a container with a custom index policy using PowerShell](manage-with-powershell.md#create-container-custom-index).

### Use the .NET SDK

#### [.NET SDK V3](#tab/dotnetv3)

The `ContainerProperties` object from the [.NET SDK v3](https://www.nuget.org/packages/Microsoft.Azure.Cosmos/) exposes an `IndexingPolicy` property that lets you change the `IndexingMode` and add or remove `IncludedPaths` and `ExcludedPaths`. For more information, see [Quickstart: Azure Cosmos DB for NoSQL client library for .NET](quickstart-dotnet.md).

```csharp
// Retrieve the container's details
ContainerResponse containerResponse = await client.GetContainer("database", "container").ReadContainerAsync();
// Set the indexing mode to consistent
containerResponse.Resource.IndexingPolicy.IndexingMode = IndexingMode.Consistent;
// Add an included path
containerResponse.Resource.IndexingPolicy.IncludedPaths.Add(new IncludedPath { Path = "/*" });
// Add an excluded path
containerResponse.Resource.IndexingPolicy.ExcludedPaths.Add(new ExcludedPath { Path = "/name/*" });
// Add a spatial index
SpatialPath spatialPath = new SpatialPath
{
    Path = "/locations/*"
};
spatialPath.SpatialTypes.Add(SpatialType.Point);
containerResponse.Resource.IndexingPolicy.SpatialIndexes.Add(spatialPath);
// Add a composite index
containerResponse.Resource.IndexingPolicy.CompositeIndexes.Add(new Collection<CompositePath> { new CompositePath() { Path = "/name", Order = CompositePathSortOrder.Ascending }, new CompositePath() { Path = "/age", Order = CompositePathSortOrder.Descending } });
// Update container with changes
await client.GetContainer("database", "container").ReplaceContainerAsync(containerResponse.Resource);
```

To track the index transformation progress, pass a `RequestOptions` object that sets the `PopulateQuotaInfo` property to `true`. Retrieve the value from the `x-ms-documentdb-collection-index-transformation-progress` response header.

```csharp
// retrieve the container's details
ContainerResponse containerResponse = await client.GetContainer("database", "container").ReadContainerAsync(new ContainerRequestOptions { PopulateQuotaInfo = true });
// retrieve the index transformation progress from the result
long indexTransformationProgress = long.Parse(containerResponse.Headers["x-ms-documentdb-collection-index-transformation-progress"]);
```

The SDK V3 fluent API lets you write this definition in a concise and efficient way when defining a custom indexing policy while creating a new container:

```csharp
await client.GetDatabase("database").DefineContainer(name: "container", partitionKeyPath: "/myPartitionKey")
    .WithIndexingPolicy()
        .WithIncludedPaths()
            .Path("/*")
        .Attach()
        .WithExcludedPaths()
            .Path("/name/*")
        .Attach()
        .WithSpatialIndex()
            .Path("/locations/*", SpatialType.Point)
        .Attach()
        .WithCompositeIndex()
            .Path("/name", CompositePathSortOrder.Ascending)
            .Path("/age", CompositePathSortOrder.Descending)
        .Attach()
    .Attach()
    .CreateIfNotExistsAsync();
```

#### [.NET SDK V2](#tab/dotnetv2)

The `DocumentCollection` object from the [.NET SDK v2](https://www.nuget.org/packages/Microsoft.Azure.DocumentDB/) exposes an `IndexingPolicy` property that lets you change the `IndexingMode` and add or remove `IncludedPaths` and `ExcludedPaths`.

```csharp
// Retrieve the container's details
ResourceResponse<DocumentCollection> containerResponse = await client.ReadDocumentCollectionAsync(UriFactory.CreateDocumentCollectionUri("database", "container"));
// Set the indexing mode to consistent
containerResponse.Resource.IndexingPolicy.IndexingMode = IndexingMode.Consistent;
// Add an included path
containerResponse.Resource.IndexingPolicy.IncludedPaths.Add(new IncludedPath { Path = "/*" });
// Add an excluded path
containerResponse.Resource.IndexingPolicy.ExcludedPaths.Add(new ExcludedPath { Path = "/name/*" });
// Add a spatial index
containerResponse.Resource.IndexingPolicy.SpatialIndexes.Add(new SpatialSpec() { Path = "/locations/*", SpatialTypes = new Collection<SpatialType>() { SpatialType.Point } } );
// Add a composite index
containerResponse.Resource.IndexingPolicy.CompositeIndexes.Add(new Collection<CompositePath> {new CompositePath() { Path = "/name", Order = CompositePathSortOrder.Ascending }, new CompositePath() { Path = "/age", Order = CompositePathSortOrder.Descending }});
// Update container with changes
await client.ReplaceDocumentCollectionAsync(containerResponse.Resource);
```

To track the index transformation progress, pass a `RequestOptions` object that sets the `PopulateQuotaInfo` property to `true`.

```csharp
// retrieve the container's details
ResourceResponse<DocumentCollection> container = await client.ReadDocumentCollectionAsync(UriFactory.CreateDocumentCollectionUri("database", "container"), new RequestOptions { PopulateQuotaInfo = true });
// retrieve the index transformation progress from the result
long indexTransformationProgress = container.IndexTransformationProgress;
```

---

### Use the Java SDK

The `DocumentCollection` object from the [Java SDK](https://mvnrepository.com/artifact/com.microsoft.azure/azure-cosmosdb) exposes the `getIndexingPolicy()` and `setIndexingPolicy()` methods. The `IndexingPolicy` object they manipulate lets you change the indexing mode and add or remove included and excluded paths. For more information, see [Quickstart: Build a Java app to manage Azure Cosmos DB for NoSQL data](quickstart-java.md).

```java
// Retrieve the container's details
Observable<ResourceResponse<DocumentCollection>> containerResponse = client.readCollection(String.format("/dbs/%s/colls/%s", "database", "container"), null);
containerResponse.subscribe(result -> {
DocumentCollection container = result.getResource();
IndexingPolicy indexingPolicy = container.getIndexingPolicy();

// Set the indexing mode to consistent
indexingPolicy.setIndexingMode(IndexingMode.Consistent);

// Add an included path

Collection<IncludedPath> includedPaths = new ArrayList<>();
IncludedPath includedPath = new IncludedPath();
includedPath.setPath("/*");
includedPaths.add(includedPath);
indexingPolicy.setIncludedPaths(includedPaths);

// Add an excluded path

Collection<ExcludedPath> excludedPaths = new ArrayList<>();
ExcludedPath excludedPath = new ExcludedPath();
excludedPath.setPath("/name/*");
excludedPaths.add(excludedPath);
indexingPolicy.setExcludedPaths(excludedPaths);

// Add a spatial index

Collection<SpatialSpec> spatialIndexes = new ArrayList<SpatialSpec>();
Collection<SpatialType> collectionOfSpatialTypes = new ArrayList<SpatialType>();

SpatialSpec spec = new SpatialSpec();
spec.setPath("/locations/*");
collectionOfSpatialTypes.add(SpatialType.Point);
spec.setSpatialTypes(collectionOfSpatialTypes);
spatialIndexes.add(spec);

indexingPolicy.setSpatialIndexes(spatialIndexes);

// Add a composite index

Collection<ArrayList<CompositePath>> compositeIndexes = new ArrayList<>();
ArrayList<CompositePath> compositePaths = new ArrayList<>();

CompositePath nameCompositePath = new CompositePath();
nameCompositePath.setPath("/name");
nameCompositePath.setOrder(CompositePathSortOrder.Ascending);

CompositePath ageCompositePath = new CompositePath();
ageCompositePath.setPath("/age");
ageCompositePath.setOrder(CompositePathSortOrder.Descending);

compositePaths.add(ageCompositePath);
compositePaths.add(nameCompositePath);

compositeIndexes.add(compositePaths);
indexingPolicy.setCompositeIndexes(compositeIndexes);

// Update the container with changes

 client.replaceCollection(container, null);
});
```

To track the index transformation progress on a container, pass a `RequestOptions` object that requests the quota info to be populated. Retrieve the value from the `x-ms-documentdb-collection-index-transformation-progress` response header.

```java
// set the RequestOptions object
RequestOptions requestOptions = new RequestOptions();
requestOptions.setPopulateQuotaInfo(true);
// retrieve the container's details
Observable<ResourceResponse<DocumentCollection>> containerResponse = client.readCollection(String.format("/dbs/%s/colls/%s", "database", "container"), requestOptions);
containerResponse.subscribe(result -> {
    // retrieve the index transformation progress from the response headers
    String indexTransformationProgress = result.getResponseHeaders().get("x-ms-documentdb-collection-index-transformation-progress");
});
```

### Use the Node.js SDK

The `ContainerDefinition` interface from [Node.js SDK](https://www.npmjs.com/package/@azure/cosmos) exposes an `indexingPolicy` property that lets you change the `indexingMode` and add or remove `includedPaths` and `excludedPaths`. For more information, see [Quickstart - Azure Cosmos DB for NoSQL client library for Node.js](quickstart-nodejs.md).

Retrieve the container's details:

```javascript
const containerResponse = await client.database('database').container('container').read();
```

Set the indexing mode to consistent:

```javascript
containerResponse.body.indexingPolicy.indexingMode = "consistent";
```

Add included path including a spatial index:

```javascript
containerResponse.body.indexingPolicy.includedPaths.push({
    includedPaths: [
      {
        path: "/age/*",
        indexes: [
          {
            kind: cosmos.DocumentBase.IndexKind.Range,
            dataType: cosmos.DocumentBase.DataType.String
          },
          {
            kind: cosmos.DocumentBase.IndexKind.Range,
            dataType: cosmos.DocumentBase.DataType.Number
          }
        ]
      },
      {
        path: "/locations/*",
        indexes: [
          {
            kind: cosmos.DocumentBase.IndexKind.Spatial,
            dataType: cosmos.DocumentBase.DataType.Point
          }
        ]
      }
    ]
  });
```

Add excluded path:

```javascript
containerResponse.body.indexingPolicy.excludedPaths.push({ path: '/name/*' });
```

Update the container with changes:

```javascript
const replaceResponse = await client.database('database').container('container').replace(containerResponse.body);
```

To track the index transformation progress on a container, pass a `RequestOptions` object that sets the `populateQuotaInfo` property to `true`. Retrieve the value from the `x-ms-documentdb-collection-index-transformation-progress` response header.

```javascript
// retrieve the container's details
const containerResponse = await client.database('database').container('container').read({
    populateQuotaInfo: true
});
// retrieve the index transformation progress from the response headers
const indexTransformationProgress = replaceResponse.headers['x-ms-documentdb-collection-index-transformation-progress'];
```

Add a composite index:

```javascript
 console.log("create container with composite indexes");
  const containerDefWithCompositeIndexes = {
    id: "containerWithCompositeIndexingPolicy",
    indexingPolicy: {
      automatic: true,
      indexingMode: IndexingMode.consistent,
      includedPaths: [
        {
          path: "/*",
        },
      ],
      excludedPaths: [
        {
          path: '/"systemMetadata"/*',
        },
      ],
      compositeIndexes: [
        [
          { path: "/field", order: "ascending" },
          { path: "/key", order: "ascending" },
        ],
      ],
    },
  };
  const containerWithCompositeIndexes = (
    await database.containers.create(containerDefWithCompositeIndexes)
  ).container;
```

### Use the Python SDK

#### [Python SDK V3](#tab/pythonv3)

When you use the [Python SDK V3](https://pypi.org/project/azure-cosmos/), the container configuration is managed as a dictionary. From this dictionary, you can access the indexing policy and all its attributes. For more information, see [Quickstart: Azure Cosmos DB for NoSQL client library for Python](quickstart-python.md).

Retrieve the container's details:

```python
containerPath = 'dbs/database/colls/collection'
container = client.ReadContainer(containerPath)
```

Set the indexing mode to consistent:

```python
container['indexingPolicy']['indexingMode'] = 'consistent'
```

Define an indexing policy with an included path and a spatial index:

```python
container["indexingPolicy"] = {

    "indexingMode":"consistent",
    "spatialIndexes":[
                {"path":"/location/*","types":["Point"]}
             ],
    "includedPaths":[{"path":"/age/*","indexes":[]}],
    "excludedPaths":[{"path":"/*"}]
}
```

Define an indexing policy with an excluded path:

```python
container["indexingPolicy"] = {
    "indexingMode":"consistent",
    "includedPaths":[{"path":"/*","indexes":[]}],
    "excludedPaths":[{"path":"/name/*"}]
}
```

Add a composite index:

```python
container['indexingPolicy']['compositeIndexes'] = [
                [
                    {
                        "path": "/name",
                        "order": "ascending"
                    },
                    {
                        "path": "/age",
                        "order": "descending"
                    }
                ]
                ]
```

Update the container with changes:

```python
response = client.ReplaceContainer(containerPath, container)
```

#### [Python SDK V4](#tab/pythonv4)

When you use the [Python SDK V4](https://pypi.org/project/azure-cosmos/), the container configuration is managed as a dictionary. From this dictionary, you can access the indexing policy and all its attributes.

Retrieve the container's details:

```python
database_client = cosmos_client.get_database_client('database')
container_client = database_client.get_container_client('container')
container = container_client.read()
```

Set the indexing mode to consistent:

```python
indexingPolicy = {
    'indexingMode': 'consistent'
}
```

Define an indexing policy with an included path and a spatial index:

```python
indexingPolicy = {
    "indexingMode":"consistent",
    "spatialIndexes":[
        {"path":"/location/*","types":["Point"]}
    ],
    "includedPaths":[{"path":"/age/*","indexes":[]}],
    "excludedPaths":[{"path":"/*"}]
}
```

Define an indexing policy with an excluded path:

```python
indexingPolicy = {
    "indexingMode":"consistent",
    "includedPaths":[{"path":"/*","indexes":[]}],
    "excludedPaths":[{"path":"/name/*"}]
}
```

Add a composite index:

```python
indexingPolicy['compositeIndexes'] = [
    [
        {
            "path": "/name",
            "order": "ascending"
        },
        {
            "path": "/age",
            "order": "descending"
        }
    ]
]
```

Update the container with changes:

```python
response = database_client.replace_container(container_client, container['partitionKey'], indexingPolicy)
```

Retrieve the index transformation progress from the response headers:

```python
container_client.read(populate_quota_info = True,
                      response_hook = lambda h,p: print(h['x-ms-documentdb-collection-index-transformation-progress']))
```

---

## Related content

- [Indexing overview](../index-overview.md)
- [Indexing policy](../index-policy.md)
