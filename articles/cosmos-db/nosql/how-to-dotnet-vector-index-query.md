---
title: Indexing and querying vector data in .NET
titleSuffix: Azure Cosmos DB for NoSQL
description: Add vector data Azure Cosmos DB for NoSQL and then query the data efficiently in your .NET application.
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

Before you use vector indexing and search, you must first enable the feature. This article covers the following steps:

1. Enabling the Vector Search in Azure Cosmos DB for NoSQL feature.
1. Setting up the Azure Cosmos DB container for vector search
1. Authoring vector embedding policy
1. Adding vector indexes to the container indexing policy
1. Creating a container with vector indexes and vector embedding policy
1. Performing a vector search on the stored data

This guide walks through the process of creating vector data, indexing the data, and then querying the data in a container.

## Prerequisites

- An existing Azure Cosmos DB for NoSQL account.
  - If you don't have an Azure subscription, [Try Azure Cosmos DB for NoSQL free](https://cosmos.azure.com/try/).
  - If you have an existing Azure subscription, [create a new Azure Cosmos DB for NoSQL account](how-to-create-account.md).
- Latest version of the Azure Cosmos DB [.NET](sdk-dotnet-v3.md) SDK (Release: 3.45.0 or later, Preview: 3.46.0-preview.0 or later).

## Enable the feature

Vector search for Azure Cosmos DB for NoSQL requires enabling the feature by completing the following steps:

1. Navigate to your Azure Cosmos DB for NoSQL resource page.
1. Select the "Features" pane under the "Settings" menu item.
1. Select for "Vector Search in Azure Cosmos DB for NoSQL."
1. Read the description of the feature to confirm you want to enable it. 
1. Select "Enable" to turn on vector search in Azure Cosmos DB for NoSQL.

> [!TIP]
> Alternatively, use the Azure CLI to update the capabilities of your account to support NoSQL vector search.
>
> ```azurecli
> az cosmosdb update \
>      --resource-group <resource-group-name> \
>      --name <account-name> \
>      --capabilities EnableNoSQLVectorSearch
> ```

> [!NOTE]
> The registration request will be autoapproved; however, it may take 15 minutes to take effect.

## Understanding the steps involved in vector search

Let’s take an example of creating a database for an internet-based bookstore and you're storing Title, Author, ISBN, and Description for each book. We also define two properties to contain vector embeddings. The first is the “contentVector” property, which contains [text embeddings](/azure/ai-services/openai/concepts/models#embeddings ) generated from the text content of the book (for example, concatenating the “title” “author” “isbn” and “description” properties before creating the embedding). The second is “coverImageVector”, which is generated from [images of the book’s cover](/azure/ai-services/computer-vision/concept-image-retrieval).

1. Create and store vector embeddings for the fields on which you want to perform vector search.
1. Specify the vector embedding paths in the vector embedding policy.
1. Include any desired vector indexes in the indexing policy for the container.

For subsequent sections of this article, we consider the below structure for the items stored in our container:

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

## Creating a vector embedding policy for your container

Next, you need to define a container vector policy. This policy provides information that is used to inform the Azure Cosmos DB query engine how to handle vector properties in the VectorDistance system functions. This policy also informs the vector indexing policy of necessary information, should you choose to specify one.
The following information is included in the contained vector policy:

- “path”: The property path that contains vectors  
- “datatype”: The type of the elements of the vector (default Float32)  
- “dimensions”: The length of each vector in the path (default 1536)  
- “distanceFunction”: The metric used to compute distance/similarity (default Cosine)  

For our example with book details, the vector policy can look like the example JSON below:

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

## Creating a vector index in the indexing policy

Once the vector embedding paths are decided, vector indexes need to be added to the indexing policy. Currently, the vector search feature for Azure Cosmos DB for NoSQL is supported only on new containers so you need to apply the vector policy during the time of container creation and it can’t be modified later.  For this example, the indexing policy would look something like this:

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
> The vector path added to the "excludedPaths" section of the indexing policy to ensure optimized performance for insertion. Not adding the vector path to "excludedPaths" will result in higher RU charge and latency for vector insertions.

## Running vector similarity search query

Once you create a container with the desired vector policy, and insert vector data into the container, you can conduct a vector search using the [Vector Distance](query/vectordistance.md) system function in a query. Suppose you want to search for books about food recipes by looking at the description, you first need to get the embeddings for your query text. In this case, you might want to generate embeddings for the query text – “food recipe”. Once you have the embedding for your search query, you can use it in the VectorDistance function in the vector search query and get all the items that are similar to your query as shown here:

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
- [Setup Azure Cosmos DB for NoSQL for vector search](../vector-search.md).
