---
title: Index and Query Vector Data in .NET
titleSuffix: Azure Cosmos DB for NoSQL
description: Add vector data in Azure Cosmos DB for NoSQL and then query the data efficiently in your .NET application.
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 12/03/2024
ms.custom: query-reference, devx-track-dotnet, build-2024, ignite-2024
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
---

# Index and query vectors in Azure Cosmos DB for NoSQL in .NET

This article walks you through the process of how to create vector data, index the data, and then query the data in a container.

Before you use vector indexing and search, you must first enable vector search in Azure Cosmos DB for NoSQL. After you set up the Azure Cosmos DB container for vector search, you create a vector embedding policy. Next, you add vector indexes to the container indexing policy. Then you create a container with vector indexes and a vector embedding policy. Finally, you perform a vector search on the stored data.

## Prerequisites

- An existing Azure Cosmos DB for NoSQL account.
  - If you don't have an Azure subscription, [try Azure Cosmos DB for NoSQL for free](https://cosmos.azure.com/try/).
  - If you have an existing Azure subscription, [create a new Azure Cosmos DB for NoSQL account](how-to-create-account.md).
- The latest version of the Azure Cosmos DB [.NET](sdk-dotnet-v3.md) SDK (Release: 3.45.0 or later, Preview: 3.46.0-preview.0 or later).

## Enable the feature

To enable vector search for Azure Cosmos DB for NoSQL, follow these steps:

1. Go to your Azure Cosmos DB for NoSQL resource page.
1. On the left pane, under **Settings**, select **Features**.
1. Select **Vector Search in Azure Cosmos DB for NoSQL**.
1. Read the description of the feature to confirm that you want to enable it.
1. Select **Enable** to turn on vector search in Azure Cosmos DB for NoSQL.

> [!TIP]
> Alternatively, use the Azure CLI to update the capabilities of your account to support Azure Cosmos DB for NoSQL vector search.
>
> ```azurecli
> az cosmosdb update \
>      --resource-group <resource-group-name> \
>      --name <account-name> \
>      --capabilities EnableNoSQLVectorSearch
> ```

The registration request is autoapproved, but it might take 15 minutes to take effect.

## Understand the steps involved in vector search

The following steps assume that you know how to [set up an Azure Cosmos DB for NoSQL account and create a database](quickstart-portal.md). The vector search feature is currently not supported on the existing containers. You need to create a new container. When you create the container, you specify the container-level vector embedding policy and the vector indexing policy.

Let's take an example of how to create a database for an internet-based bookstore. You want to store title, author, ISBN, and description information for each book. You also need to define the following two properties to contain vector embeddings:

- The `contentVector` property contains [text embeddings](/azure/ai-services/openai/concepts/models#embeddings ) that are generated from the text content of the book. For example, you concatenate the `title`, `author`, `isbn`, and `description` properties before you create the embedding.
- The `coverImageVector` property is generated from [images of the book's cover](/azure/ai-services/computer-vision/concept-image-retrieval).

To perform a vector search, you:

1. Create and store vector embeddings for the fields on which you want to perform vector search.
1. Specify the vector embedding paths in the vector embedding policy.
1. Include any vector indexes that you want in the indexing policy for the container.

For subsequent sections of this article, consider the following structure for the items stored in your container:

```json
{
"title": "book-title", 
"author": "book-author", 
"isbn": "book-isbn", 
"description": "book-description", 
"contentVector": [2, -1, 4, 3, 5, -2, 5, -7, 3, 1], 
"coverImageVector": [0.33, -0.52, 0.45, -0.67, 0.89, -0.34, 0.86, -0.78] 
} 
```

## Create a vector embedding policy for your container

Now you need to define a container vector policy. This policy provides information that's used to inform the Azure Cosmos DB query engine about how to handle vector properties in the `VectorDistance` system functions. This policy also provides necessary information to the vector indexing policy, if you choose to specify one.

The following information is included in the container vector policy:

| Parameter | Description |
| --- | --- |
| `path` | The property path that contains vectors. |
| `datatype` | The type of the elements of the vector. (The default is `Float32`.) |
| `dimensions` | The length of each vector in the path. (The default is `1536`.) |
| `distanceFunction` | The metric used to compute distance/similarity. (The default is `Cosine`.) |

For the example with book details, the vector policy might look like the following example:

```csharp
  Database db = await client.CreateDatabaseIfNotExistsAsync("vector-benchmarking");
  List<Embedding> embeddings = new List<Embedding>()
  {
      new Embedding()
      {
          Path = "/coverImageVector",
          DataType = VectorDataType.Float32,
          DistanceFunction = DistanceFunction.Cosine,
          Dimensions = 8,
      },
      new Embedding()
      {
          Path = "/contentVector",
          DataType = VectorDataType.Float32,
          DistanceFunction = DistanceFunction.Cosine,
          Dimensions = 10,
      }
  };
```

## Create a vector index in the indexing policy

After you decide on the vector embedding paths, you must add vector indexes to the indexing policy. Currently, the vector search feature for Azure Cosmos DB for NoSQL is supported only on new containers. When you create the container, you apply the vector policy. You can't modify the policy later. The indexing policy looks something like the following example:

```csharp
    Collection<Embedding> collection = new Collection<Embedding>(embeddings);
    ContainerProperties properties = new ContainerProperties(id: "vector-container", partitionKeyPath: "/id")
    {   
        VectorEmbeddingPolicy = new(collection),
        IndexingPolicy = new IndexingPolicy()
        {
            VectorIndexes = new()
            {
                new VectorIndexPath()
                {
                    Path = "/vector",
                    Type = VectorIndexType.QuantizedFlat,
                }
            }
        },
    };
    properties.IndexingPolicy.IncludedPaths.Add(new IncludedPath { Path = "/*" });    
    properties.IndexingPolicy.ExcludedPaths.Add(new ExcludedPath { Path = "/vector/*" });
```

> [!IMPORTANT]
> The vector path is added to the `excludedPaths` section of the indexing policy to ensure optimized performance for insertion. Not adding the vector path to `excludedPaths` results in a higher request unit charge and latency for vector insertions.

## Run a vector similarity search query

After you create a container with the vector policy that you want and insert vector data into the container, use the [VectorDistance](query/vectordistance.md) system function in a query to conduct a vector search.

Suppose that you want to search for books about food recipes by looking at the description. You first need to get the embeddings for your query text. In this case, you might want to generate embeddings for the query text `food recipe`. After you have the embedding for your search query, you can use it in the `VectorDistance` function in the vector search query to get all the items that are similar to your query:

```sql
SELECT TOP 10 c.title, VectorDistance(c.contentVector, [1,2,3,4,5,6,7,8,9,10]) AS SimilarityScore   
FROM c  
ORDER BY VectorDistance(c.contentVector, [1,2,3,4,5,6,7,8,9,10])   
```

This query retrieves the book titles along with similarity scores with respect to your query. Here's an example in .NET:

```csharp
  float[] embedding = {1f,2f,3f,4f,5f,6f,7f,8f,9f,10f};
  var queryDef = new QueryDefinition(
      query: $"SELECT c.title, VectorDistance(c.contentVector,@embedding) AS SimilarityScore FROM c ORDER BY VectorDistance(c.contentVector,@embedding)"
      ).WithParameter("@embedding", embedding);
  using FeedIterator<Object> feed = container.GetItemQueryIterator<Object>(
      queryDefinition: queryDef
  );
  while (feed.HasMoreResults) 
  {
      FeedResponse<Object> response = await feed.ReadNextAsync();
      foreach ( Object item in response)
      {
          Console.WriteLine($"Found item:\t{item}");
      }
  }
```

## Related content

- [VectorDistance system function](query/vectordistance.md)
- [Vector indexing](../index-policy.md)
- [Set up Azure Cosmos DB for NoSQL for vector search](../vector-search.md)
