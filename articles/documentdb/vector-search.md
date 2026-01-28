---
title: Integrated Vector Store
description: Store, index, and query vector embeddings in Azure DocumentDB for AI applications. Learn to use DiskANN, HNSW, and IVF indexing with code examples.
author: gahl-levy
ms.author: gahllevy
ms.topic: concept-article
ms.date: 11/05/2025
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
ms.custom:
  - sfi-ropc-blocked
ai-usage: ai-assisted
---

# Integrated vector store in Azure DocumentDB

Use the integrated vector database in Azure DocumentDB to seamlessly connect AI-based applications with your data stored in Azure DocumentDB. This integration can include apps that you built by using [Azure OpenAI embeddings](/azure/ai-services/openai/tutorials/embeddings). The natively integrated vector database enables you to efficiently store, index, and query high-dimensional vector data stored directly in Azure DocumentDB, along with the original data from which the vector data is created. It eliminates the need to transfer your data to alternative vector stores and incur extra costs.

## What is a vector store?

A vector store or vector database is a database designed to store and manage vector embeddings, which are mathematical representations of data in a high-dimensional space. In this space, each dimension corresponds to a feature of the data, and tens of thousands of dimensions might be used to represent sophisticated data. A vector's position in this space represents its characteristics. Words, phrases, or entire documents, and images, audio, and other types of data can all be vectorized. 

## How does a vector store work?

In a vector store, vector search algorithms are used to index and query embeddings. Some well-known vector search algorithms include Hierarchical Navigable Small World (HNSW), Inverted File (IVF), and DiskANN. Vector search is a method that helps you find similar items based on their data characteristics rather than by exact matches on a property field. This technique is useful in applications such as searching for similar text, finding related images, making recommendations, or even detecting anomalies. It's used to query the [vector embeddings](/azure/ai-services/openai/concepts/understand-embeddings) (lists of numbers) of your data that you created by using a machine learning model by using an embeddings API. Examples of embeddings APIs are [Azure OpenAI embeddings](/azure/ai-services/openai/how-to/embeddings) or [Hugging Face on Azure](https://azure.microsoft.com/solutions/hugging-face-on-azure/). Vector search measures the distance between the data vectors and your query vector. The data vectors that are closest to your query vector are the ones that are found to be most similar semantically.

In the integrated vector database in Azure DocumentDB, you can store, index, and query embeddings alongside the original data. This approach eliminates the extra cost of replicating data in a separate pure vector database. Moreover, this architecture keeps the vector embeddings and original data together, which better facilitates multimodal data operations, and enables greater data consistency, scale, and performance.

## Vector database use cases

Vector databases are used in many areas of AI and data analysis. They help with tasks like understanding natural language, recognizing images and videos, building recommendation systems, and powering search features. You can find them in both analytical AI and generative AI applications.

For example, you can use a vector database to:

- Identify similar images, documents, and songs based on their contents, themes, sentiments, and styles.
- Identify similar products based on their characteristics, features, and user groups.
- Recommend contents, products, or services based on individuals' preferences.
- Recommend contents, products, or services based on user groups' similarities.
- Identify the best-fit potential options from a large pool of choices to meet complex requirements.
- Identify data anomalies or fraudulent activities that are dissimilar from predominant or normal patterns.
- Implement persistent memory for AI agents.
- Enable retrieval-augmented generation (RAG).

## Integrated vector database vs. pure vector database

Two common types of vector database implementations exist: pure vector database and integrated vector database in a NoSQL or relational database.

A *pure vector database* efficiently stores and manages vector embeddings along with a small amount of metadata. It's separate from the data source from which the embeddings are derived.

A vector database that integrates in a highly performant NoSQL or relational database provides extra capabilities. The *integrated vector database* in a NoSQL or relational database can store, index, and query embeddings alongside the corresponding original data. This approach eliminates the extra cost of replicating data in a separate pure vector database. Moreover, keeping the vector embeddings and original data together better facilitates multimodal data operations and enables greater data consistency, scale, and performance.

## Open-source vector databases

When developers select vector databases, the open-source options provide numerous benefits. *Open source* means that the software's source code is available freely, enabling users to customize the database according to their specific needs. This flexibility is beneficial for organizations that are subject to unique regulatory requirements for data, such as companies in the financial services industry.

Another advantage of open-source vector databases is the strong community support they enjoy. Active user communities often contribute to the development of these databases, provide support, and share best practices, promoting innovation.

Some individuals opt for open-source vector databases because they're "free," meaning there's no cost to acquire or use the software. An alternative is using the free tiers offered by managed vector database services. These managed services provide not only cost-free access up to a certain usage limit but also simplify the operational burden by handling maintenance, updates, and scalability. Therefore, by using the free tier of managed vector database services, you can achieve cost savings while reducing management overhead. This approach allows you to focus more on your core activities rather than on database administration.

### Select the best open-source vector database

Choosing the best open-source vector database requires considering several factors. Performance and scalability of the database are crucial, as they affect whether the database can handle your specific workload requirements. Databases with efficient indexing and querying capabilities usually offer optimal performance. Another factor is the community support and documentation available for the database. A robust community and ample documentation can provide valuable assistance. For example, [DocumentDB](https://github.com/documentdb/documentdb) is a popular open-source vector database:

The most popular option might not be the best option for you. Thus, you should compare different options based on features, supported data types, and compatibility with existing tools and frameworks you use. You should also keep in mind the challenges of open-source vector databases.

### Challenges of open-source vector databases

Most open-source vector databases, including the ones listed previously, are pure vector databases. In other words, they're designed to store and manage vector embeddings only, along with a small amount of metadata. Since they work separately from your original data, you need to move data between different services. This complexity adds extra cost, makes things more complex, and can slow down your production systems.

They also pose the challenges that are typical of open-source databases:

- Setup: You need in-depth knowledge to install, configure, and operate the database, especially for complex deployments. Optimizing resources and configuration while scaling up operation requires close monitoring and adjustments.
- Maintenance: You must manage your own updates, patches, and maintenance. Machine learning expertise isn't enough; you must also have extensive experience in database administration.
- Support: Official support can be limited compared to managed services, relying more on community assistance.

Therefore, while free initially, open-source vector databases incur significant costs when scaling up. Expanding operations necessitates more hardware, skilled IT staff, and advanced infrastructure management, leading to higher expenses in hardware, personnel, and operational costs. Scaling open-source vector databases can be financially demanding despite the lack of licensing fees.

### Addressing the challenges of open-source vector databases

A fully managed vector database that integrates in a highly performant NoSQL or relational database avoids the extra cost and complexity of open-source vector databases. Such a database stores, indexes, and queries embeddings alongside the corresponding original data. This approach eliminates the extra cost of replicating data in a separate pure vector database. Moreover, keeping the vector embeddings and original data together better facilitates multimodal data operations, and enables greater data consistency, scale, and performance. Meanwhile, the fully managed service helps developers avoid the hassles from setting up, maintaining, and relying on community assistance for an open-source vector database. Moreover, some managed vector database services offer a lifetime free tier.

An example is the integrated vector database in Azure DocumentDB. This setup allows developers to save money like they would with open-source vector databases. But unlike open-source options, the service provider takes care of maintenance, updates, and scaling for you. Upgrading is quick and easy while keeping a low total cost of ownership (TCO) when it's time to scale up operations. You can also use this service to conveniently scale MongoDB applications that are already in production.

## Perform vector similarity search

Azure DocumentDB provides robust vector search capabilities, allowing you to perform high-speed similarity searches across complex datasets. To perform vector search in Azure DocumentDB, you first need to create a vector index. While Azure DocumentDB offers multiple options, here are some general guidelines to help you get started based on the size of your dataset:

| | **IVF** | **HNSW** | **DiskANN (recommended)** |
| --- | --- | --- | --- |
| **Description** | An IVFFlat index divides vectors into lists, then searches a subset closest to the query vector. | An HNSW index creates a multilayer graph. | DiskANN is an approximate nearest neighbor search algorithm designed for efficient vector search at any scale. |
| **Key trade-offs** | **Pros:** Faster build times, lower memory use. <br> **Cons:** Lower query performance (in terms of speed-recall tradeoff). | **Pros:** Better query performance (in terms of speed-recall tradeoff) can be created on an empty table. <br>**Cons:** Slower build times, higher memory use. | **Pros:** Efficient at any scale, high recall, high throughput, low latency. |
| **Vector count** | Under 10,000 | Up to 50,000 | Up to 500,000+ |
| **Recommended cluster tier** | M10 or M20 | M30 and higher | M30 and higher |

### [DiskANN](#tab/diskann)

You can use DiskANN indexes on M30 and higher tiers. To create the DiskANN index, set the `"kind"` parameter to `"vector-diskann"` following this template:

```javascript
{ 
    "createIndexes": "<collection_name>",
    "indexes": [
        {
            "name": "<index_name>",
            "key": {
                "<path_to_property>": "cosmosSearch"
            },
            "cosmosSearchOptions": { 
                "kind": "vector-diskann", 
                "dimensions": <integer_value>,
                "similarity": <string_value>,
                "maxDegree" : <integer_value>, 
                "lBuild" : <integer_value>, 
            } 
        } 
    ] 
}
```

| Field | Type | Description |
| --- | --- | --- |
| `index_name` | string | Unique name of the index. |
| `path_to_property` | string | Path to the property that contains the vector. This path can be a top-level property or a dot notation path to the property. Vectors must be a `number[]` to be indexed and used in vector search results. A vector using another type, such as `double[]`,  prevents the document from being indexed. Nonindexed documents aren't returned in the result of a vector search. |
| `kind` | string | Type of vector index to create. The options are `vector-ivf`, `vector-hnsw`, and `vector-diskann`. |
| `dimensions` | integer | Number of dimensions for vector similarity. DiskANN supports up to 16,000 dimensions (with [product quantization](./product-quantization.md)), with future support planned for 40,000+. |
| `similarity` | string | Similarity metric to use with the index. Possible options are `COS` (cosine distance), `L2` (Euclidean distance), and `IP` (inner product). |
| `maxDegree` | integer | Maximum number of edges per node in the graph. This parameter ranges from 20 to 2048 (default is 32). Higher `maxDegree` is suitable for datasets with high dimensionality and/or high accuracy requirements. |
| `lBuild` | integer | Sets the number of candidate neighbors evaluated during DiskANN index construction. This parameter, which ranges from 10 to 500 (default is 50), balances accuracy and computational overhead: higher values improve index quality and accuracy but increase build time |

### Perform a vector search with DiskANN

To perform a vector search, use the `$search` aggregation pipeline stage, and query with the `cosmosSearch` operator. DiskANN enables high-performance searches across massive datasets with **optional** filtering such as geospatial or text-based filters.

```javascript
{
  "$search": {
    "cosmosSearch": {
      "path": "<path_to_property>",
      "query": "<query_vector>",  
      "k": <num_results_to_return>,  
      "filter": {"$and": [
        { "<attribute_1>": { "$eq": <value> } },
        {"<location_attribute>": {"$geoWithin": {"$centerSphere":[[<longitude_integer_value>, <latitude_integer_value>], <radius>]}}}
      ]}
    }
  }
},
```

| Field | Type | Description |
| --- | --- | --- |
| `lSearch` | integer | Specifies the size of the dynamic candidate list for search. The default value is 40, with a configurable range from 10 to 1000. Increasing the value enhances recall but might reduce search speed. |
| `k` | integer | Defines the number of search results to return. The `k` value must be less than or equal to `lSearch`. |

## Example using a DiskANN index with filtering

### Add vectors to your database

To use vector search with geospatial filters, add documents that include both vector embeddings and location coordinates. You can create the [embeddings](/azure/ai-services/openai/concepts/understand-embeddings) by using your own model, [Azure OpenAI embeddings](/azure/cognitive-services/openai/tutorials/embeddings), or an API like [Hugging Face on Azure](https://azure.microsoft.com/solutions/hugging-face-on-azure/).

```python
from pymongo import MongoClient

client = MongoClient("<your_connection_string>")
db = client["test"]
collection = db["testCollection"]

documents = [
    {"name": "Eugenia Lopez", "bio": "CEO of AdventureWorks", "is_open": 1, "location": [-118.9865, 34.0145], "contentVector": [0.52, 0.20, 0.23]},
    {"name": "Cameron Baker", "bio": "CFO of AdventureWorks", "is_open": 1, "location": [-0.1278, 51.5074], "contentVector": [0.55, 0.89, 0.44]},
    {"name": "Jessie Irwin", "bio": "Director of Our Planet initiative", "is_open": 0, "location": [-118.9865, 33.9855], "contentVector": [0.13, 0.92, 0.85]},
    {"name": "Rory Nguyen", "bio": "President of Our Planet initiative", "is_open": 1, "location": [-119.0000, 33.9855], "contentVector": [0.91, 0.76, 0.83]}
]

collection.insert_many(documents)
```

### Create a DiskANN vector index

The following example demonstrates how to set up a DiskANN vector index with filtering capabilities. This example includes creating the vector index for similarity search, adding documents with vector and geospatial properties, and indexing fields for more filtering.

```python
db.command({
    "createIndexes": "testCollection",
    "indexes": [
        {
            "name": "DiskANNVectorIndex",
            "key": {
                "contentVector": "cosmosSearch"
            },
            "cosmosSearchOptions": {
                "kind": "vector-diskann",
                "dimensions": 3,
                "similarity": "COS",
                "maxDegree": 32,
                "lBuild": 64
            }
        },
        { 
            "name": "is_open",
            "key": { 
                "is_open": 1 
            }      
        },
        {
            "name": "locationIndex",
            "key": {
                "location": 1
            }
        }
    ]
})
```

This command creates a DiskANN vector index on the `contentVector` field in `exampleCollection`, enabling similarity searches. It also adds:
- An index on the `is_open` field, so you can filter results based on whether businesses are open.
- A geospatial index on the `location` field to filter by geographic proximity.

### Perform a vector search

To find documents with similar vectors within a specific geographic radius, specify the `queryVector` for similarity search and include a geospatial filter.

```python
query_vector = [0.52, 0.28, 0.12]
pipeline = [
    {
        "$search": {
            "cosmosSearch": {
                "path": "contentVector",
                "vector": query_vector,
                "k": 5,
                "filter": {
                    "$and": [
                        {"is_open": {"$eq": 1}},
                        {"location": {"$geoWithin": {"$centerSphere": [[-119.7192861804, 34.4102485028], 100 / 3963.2]}}}
                    ]
                }
            }
        }
    }
]

results = list(collection.aggregate(pipeline))
for result in results:
    print(result)
```

In this example, the vector similarity search returns the top `k` closest vectors based on the specified `COS` similarity metric, while filtering results to include only open businesses within a 100-mile radius.

```python
[
  {
    similarityScore: 0.9745354109084544,
    document: {
      _id: ObjectId("645acb54413be5502badff94"),
      name: 'Eugenia Lopez',
      bio: 'CEO of AdventureWorks',
      is_open: 1,
      location: [-118.9865, 34.0145],
      contentVector: [0.52, 0.20, 0.23]
    }
  },
  {
    similarityScore: 0.9006955671333992,
    document: {
      _id: ObjectId("645acb54413be5502badff97"),
      name: 'Rory Nguyen',
      bio: 'President of Our Planet initiative',
      is_open: 1,
      location: [-119.7302, 34.4005],
      contentVector: [0.91, 0.76, 0.83]
    }
  }
]
```

This result shows the top similar documents to `queryVector`; constrained to a 100-mile radius and open businesses. Each result includes the similarity score and metadata, demonstrating how DiskANN in Azure DocumentDB supports combined vector and geospatial queries for enriched, location-sensitive search experiences.

### [HNSW](#tab/hnsw)

You can create HNSW indexes on M30 and higher cluster tiers. To create the Hierarchical navigable small world (HNSW) index, you need to create a vector index with the `"kind"` parameter set to `"vector-hnsw"` following this template:

```javascript
{ 
    "createIndexes": "<collection_name>",
    "indexes": [
        {
            "name": "<index_name>",
            "key": {
                "<path_to_property>": "cosmosSearch"
            },
            "cosmosSearchOptions": { 
                "kind": "vector-hnsw", 
                "m": <integer_value>, 
                "efConstruction": <integer_value>, 
                "similarity": "<string_value>", 
                "dimensions": <integer_value> 
            } 
        } 
    ] 
}
```

| Field | Type | Description |
| --- | --- | --- |
| `m` | integer | The max number of connections per layer (16 by default, minimum value is 2, maximum value is 100). Higher m is suitable for datasets with high dimensionality and/or high accuracy requirements. |
| `efConstruction` | integer | the size of the dynamic candidate list for constructing the graph (64 by default, minimum value is 4, maximum value is 1000). Higher `efConstruction` results in better index quality and higher accuracy, but it also increases the time required to build the index. `efConstruction` has to be at least `2 * m` |

### Perform a vector search with HNSW

To perform a vector search, use the `$search` aggregation pipeline stage and the `cosmosSearch` operator.

```javascript
{
    "$search": {
        "cosmosSearch": {
            "vector": <query_vector>,
            "path": "<path_to_property>",
            "k": <num_results_to_return>,
            "efSearch": <integer_value>
        },
    }
}
```

| Field | Type | Description |
| --- | --- | --- |
| `efSearch` | integer | The size of the dynamic candidate list for search (40 by default). A higher value provides better recall at the cost of speed. |

> [!NOTE]
> Creating an HNSW index with large datasets can result in your Azure DocumentDB resource running out of memory, or can limit the performance of other operations running on your database. If you encounter such issues, scale your resource to a higher cluster tier, or create a new DiskANN vector index.

## Example using an HNSW index

The following examples show you how to index vectors, add documents that have vector properties, perform a vector search, and retrieve the index configuration.

```javascript
use test;

db.createCollection("exampleCollection");

db.runCommand({ 
    "createIndexes": "exampleCollection",
    "indexes": [
        {
            "name": "VectorSearchIndex",
            "key": {
                "contentVector": "cosmosSearch"
            },
            "cosmosSearchOptions": { 
                "kind": "vector-hnsw", 
                "m": 16, 
                "efConstruction": 64, 
                "similarity": "COS", 
                "dimensions": 3
            } 
        } 
    ] 
});
```

This command creates an HNSW index against the `contentVector` property in the documents that are stored in the specified collection, `exampleCollection`. The `cosmosSearchOptions` property specifies the parameters for the HNSW vector index. If your document has the vector stored in a nested property, you can set this property by using a dot notation path. For example, you might use `text.contentVector` if `contentVector` is a subproperty of `text`.

### Add vectors to your database

To add vectors to your database's collection, you first need to create the [embeddings](/azure/ai-services/openai/concepts/understand-embeddings) by using your own model, [Azure OpenAI embeddings](/azure/cognitive-services/openai/tutorials/embeddings), or an API such as [Hugging Face on Azure](https://azure.microsoft.com/solutions/hugging-face-on-azure/). In this example, you add new documents through sample embeddings:

```javascript
db.exampleCollection.insertMany([
  {name: "Eugenia Lopez", bio: "Eugenia is the CEO of AdvenureWorks.", contentVector: [0.51, 0.12, 0.23]},
  {name: "Cameron Baker", bio: "Cameron Baker CFO of AdvenureWorks.", contentVector: [0.55, 0.89, 0.44]},
  {name: "Jessie Irwin", bio: "Jessie Irwin is the former CEO of AdventureWorks and now the director of the Our Planet initiative.", contentVector: [0.13, 0.92, 0.85]},
  {name: "Rory Nguyen", bio: "Rory Nguyen is the founder of AdventureWorks and the president of the Our Planet initiative.", contentVector: [0.91, 0.76, 0.83]},
]);
```

### Perform a vector search

Continuing with the last example, create another vector, `queryVector`. Vector search measures the distance between `queryVector` and the vectors in the `contentVector` path of your documents. You can set the number of results that the search returns by setting the parameter `k`, which is set to 2 here. You can also set `efSearch`, which is an integer that controls the size of the candidate vector list. A higher value might improve accuracy, but the search is slower as a result. This parameter is optional with a default value of 40.

```javascript
const queryVector = [0.52, 0.28, 0.12];
db.exampleCollection.aggregate([
  {
    "$search": {
        "cosmosSearch": {
            "vector": queryVector,
            "path": "contentVector",
            "k": 2,
            "efSearch": 40
        },
    }
  }
}
]);
```

In this example, you perform a vector search by using `queryVector` as an input via the Mongo shell. The search result is a list of two items that are most similar to the query vector, sorted by their similarity scores.

```javascript
[
  {
    similarityScore: 0.9465376,
    document: {
      _id: ObjectId("645acb54413be5502badff94"),
      name: 'Eugenia Lopez',
      bio: 'Eugenia is the CEO of AdvenureWorks.',
      vectorContent: [ 0.51, 0.12, 0.23 ]
    }
  },
  {
    similarityScore: 0.9006955,
    document: {
      _id: ObjectId("645acb54413be5502badff97"),
      name: 'Rory Nguyen',
      bio: 'Rory Nguyen is the founder of AdventureWorks and the president of the Our Planet initiative.',
      vectorContent: [ 0.91, 0.76, 0.83 ]
    }
  }
]
```

### [IVF](#tab/IVF)

To create a vector index using the IVF algorithm, use the following `createIndexes` template and set the `"kind"` parameter to `"vector-ivf"`:

```json
{
  "createIndexes": "<collection_name>",
  "indexes": [
    {
      "name": "<index_name>",
      "key": {
        "<path_to_property>": "cosmosSearch"
      },
      "cosmosSearchOptions": {
        "kind": "vector-ivf",
        "numLists": <integer_value>,
        "similarity": "<string_value>",
        "dimensions": <integer_value>
      }
    }
  ]
}
```

| Field | Type | Description |
| --- | --- | --- |
| `numLists` | integer | This integer is the number of clusters that the IVF index uses to group the vector data. Set `numLists` to `documentCount/1000` for up to 1 million documents and to `sqrt(documentCount)` for more than 1 million documents. Using a `numLists` value of 1 is akin to performing brute-force search, which has limited performance. |

> [!IMPORTANT]
> Setting the `numLists` parameter correctly is important for achieving good accuracy and performance. Set `numLists` to `documentCount/1000` for up to 1 million documents. For more than 1 million documents, use DiskANN vector index for optimal results. 
>
> As the number of items in your database grows, you should tune `numLists` to be larger in order to achieve good latency performance for vector search.
>
> If you're experimenting with a new scenario or creating a small demo, you can start with `numLists` set to 1 to perform a brute-force search across all vectors. This setting provides the most accurate results from the vector search, but the search speed and latency are slower. After your initial setup, tune the `numLists` parameter using the preceding guidance.

### Perform a vector search with IVF

To perform a vector search, use the `$search` aggregation pipeline stage in a MongoDB query. To use the `cosmosSearch` index, use the new `cosmosSearch` operator.

```json
{
  {
  "$search": {
    "cosmosSearch": {
        "vector": <query_vector>,
        "path": "<path_to_property>",
        "k": <num_results_to_return>,
      },
      "returnStoredSource": True }},
  {
    "$project": { "<custom_name_for_similarity_score>": {
           "$meta": "searchScore" },
            "document" : "$$ROOT"
        }
  }
}
```

To retrieve the similarity score (`searchScore`) along with the documents found by the vector search, use the `$project` operator to include `searchScore` and rename it as `<custom_name_for_similarity_score>` in the results. Then the document is also projected as nested object. The similarity score is calculated using the metric defined in the vector index.

> [!IMPORTANT]
> Vectors must be a `number[]` to be indexed. A vector using another type, such as `double[]`, prevents the document from being indexed. Nonindexed documents aren't returned in the result of a vector search.

## Example using an IVF index

Inverted File (IVF) indexing is a method that organizes vectors into clusters. During a vector search, the query vector is first compared against the centers of these clusters. The search is then conducted within the cluster whose center is closest to the query vector.

The `numLists` parameter determines the number of clusters to be created. A single cluster implies that the search is conducted against all vectors in the database; akin to a brute-force or kNN search. This setting provides the highest accuracy but also the highest latency.

Increasing the `numLists` value results in more clusters, each containing fewer vectors. For instance, if `numLists=2`, each cluster contains more vectors than if `numLists=3`, and so on. Fewer vectors per cluster speed-up the search (lower latency, higher queries per second). However, this increase the likelihood of missing the most similar vector in your database to the query vector. This issue is due to the imperfect nature of clustering, where the search might focus on one cluster while the actual "closest" vector resides in a different cluster.

The `nProbes` parameter controls the number of clusters to search. By default, the value is 1, meaning it searches only the cluster with the center closest to the query vector. Increasing this value allows the search to cover more clusters, improving accuracy but also increasing latency (thus decreasing queries per second) as more clusters and vectors are being searched.

The following examples show you how to index vectors, add documents that have vector properties, perform a vector search, and retrieve the index configuration.

### Create a vector index

```javascript
use test;

db.createCollection("exampleCollection");

db.runCommand({
  createIndexes: 'exampleCollection',
  indexes: [
    {
      name: 'vectorSearchIndex',
      key: {
        "vectorContent": "cosmosSearch"
      },
      cosmosSearchOptions: {
        kind: 'vector-ivf',
        numLists: 3,
        similarity: 'COS',
        dimensions: 3
      }
    }
  ]
});
```

This command creates a `vector-ivf` index against the `vectorContent` property in the documents that are stored in the specified collection, `exampleCollection`. The `cosmosSearchOptions` property specifies the parameters for the IVF vector index. If your document has the vector stored in a nested property, you can set this property by using a dot notation path. For example, you might use `text.vectorContent` if `vectorContent` is a subproperty of `text`.

### Add vectors to your database

To add vectors to your database's collection, you first need to create the [embeddings](/azure/ai-services/openai/concepts/understand-embeddings) by using your own model, [Azure OpenAI embeddings](/azure/cognitive-services/openai/tutorials/embeddings), or an API such as [Hugging Face on Azure](https://azure.microsoft.com/solutions/hugging-face-on-azure/). In this example, you add new documents through sample embeddings:

```javascript
db.exampleCollection.insertMany([
  {name: "Eugenia Lopez", bio: "Eugenia is the CEO of AdvenureWorks.", vectorContent: [0.51, 0.12, 0.23]},
  {name: "Cameron Baker", bio: "Cameron Baker CFO of AdvenureWorks.", vectorContent: [0.55, 0.89, 0.44]},
  {name: "Jessie Irwin", bio: "Jessie Irwin is the former CEO of AdventureWorks and now the director of the Our Planet initiative.", vectorContent: [0.13, 0.92, 0.85]},
  {name: "Rory Nguyen", bio: "Rory Nguyen is the founder of AdventureWorks and the president of the Our Planet initiative.", vectorContent: [0.91, 0.76, 0.83]},
]);
```

### Perform a vector search

To perform a vector search, use the `$search` aggregation pipeline stage in a MongoDB query. To use the `cosmosSearch` index, use the new `cosmosSearch` operator.

```json
{
  {
  "$search": {
    "cosmosSearch": {
        "vector": <vector_to_search>,
        "path": "<path_to_property>",
        "k": <num_results_to_return>,
      },
      "returnStoredSource": True }},
  {
    "$project": { "<custom_name_for_similarity_score>": {
           "$meta": "searchScore" },
            "document" : "$$ROOT"
        }
  }
}
```

To retrieve the similarity score (`searchScore`) along with the documents found by the vector search, use the `$project` operator to include `searchScore` and rename it as `<custom_name_for_similarity_score>` in the results. Then the document is also projected as nested object. The similarity score is calculated using the metric defined in the vector index.

### Query vectors and vector distances (similarity scores) using $search

Continuing with the last example, create another vector, `queryVector`. Vector search measures the distance between `queryVector` and the vectors in the `vectorContent` path of your documents. You can set the number of results that the search returns by setting the parameter `k`, which is set to 2 here. You can also set `nProbes`, which is an integer that controls the number of nearby clusters that are inspected in each search. A higher value might improve accuracy however the search is slower as a result. This parameter is optional with a default value of 1 and can't be larger than the `numLists` value specified in the vector index.

```javascript
const queryVector = [0.52, 0.28, 0.12];
db.exampleCollection.aggregate([
  {
    $search: {
      "cosmosSearch": {
        "vector": queryVector,
        "path": "vectorContent",
        "k": 2
      },
    "returnStoredSource": true }},
  {
    "$project": { "similarityScore": {
           "$meta": "searchScore" },
            "document" : "$$ROOT"
        }
  }
]);
```

In this example, you perform a vector search by using `queryVector` as an input via the Mongo shell. The search result is a list of two items that are most similar to the query vector, sorted by their similarity scores.

```javascript
[
  {
    similarityScore: 0.9465376,
    document: {
      _id: ObjectId("645acb54413be5502badff94"),
      name: 'Eugenia Lopez',
      bio: 'Eugenia is the CEO of AdvenureWorks.',
      vectorContent: [ 0.51, 0.12, 0.23 ]
    }
  },
  {
    similarityScore: 0.9006955,
    document: {
      _id: ObjectId("645acb54413be5502badff97"),
      name: 'Rory Nguyen',
      bio: 'Rory Nguyen is the founder of AdventureWorks and the president of the Our Planet initiative.',
      vectorContent: [ 0.91, 0.76, 0.83 ]
    }
  }
]
```

---

### Get vector index definitions

To retrieve your vector index definition from the collection, use the `listIndexes` command:

``` javascript
db.exampleCollection.getIndexes();
```

In this example, `vectorIndex` is returned with all the `cosmosSearch` parameters that were used to create the index:

```javascript
[
  { v: 2, key: { _id: 1 }, name: '_id_', ns: 'test.exampleCollection' },
  {
    v: 2,
    key: { vectorContent: 'cosmosSearch' },
    name: 'vectorSearchIndex',
    cosmosSearch: {
      kind: <index_type>, // options are `vector-ivf`, `vector-hnsw`, and `vector-diskann`
      numLists: 3,
      similarity: 'COS',
      dimensions: 3
    },
    ns: 'test.exampleCollection'
  }
]
```

## Filtered vector search

You can now execute vector searches with any supported query filter such as `$lt`, `$lte`, `$eq`, `$neq`, `$gte`, `$gt`, `$in`, `$nin`, and `$regex`. 

To use prefiltering, you first need to define a standard index on the property you want to filter by, in addition to your vector index. Here's an example of creating a filter index:

```javascript
db.runCommand({
  "createIndexes": "<collection_name>",
  "indexes": [ {
    "key": {
      "<property_to_filter>": 1
    },
    "name": "<name_of_filter_index>"
  }
  ]
});
```

Once your filter index is in place, you can add the `"filter"` clause directly into your vector search query. This example shows how to filter results where the `"title"` property's value isn't present in the provided list:

```javascript
db.exampleCollection.aggregate([
  {
    '$search': {
      "cosmosSearch": {
        "vector": "<query_vector>",
        "path": <path_to_vector>,
        "k": num_results,
        "filter": {<property_to_filter>: {"$nin": ["not in this text", "or this text"]}}
      },
      "returnStoredSource": True }},
  {'$project': { 'similarityScore': { '$meta': 'searchScore' }, 'document' : '$$ROOT' }
}
]);
```

> [!IMPORTANT]
> To optimize the performance and accuracy of your prefiltered vector searches, consider adjusting your vector index parameters. For **DiskANN** indexes, increasing `maxDegree` or `lBuild` might yield better results. For **HNSW** indexes, experimenting with higher values for `m`, `efConstruction`, or `efSearch` can improve performance. Similarly, for **IVF** indexes, tuning `numLists` or `nProbes` could lead to more satisfactory outcomes. It's crucial to test your specific configuration with your data to ensure the results meet your requirements. These parameters influence the index structure and search behavior, and optimal values can vary based on your data characteristics and query patterns.

## Use large language model (LLM) orchestration tools

### Use as a vector database with Semantic Kernel

Use Semantic Kernel to orchestrate your information retrieval from Azure DocumentDB and your LLM. For more information, see the [GitHub repo](https://github.com/microsoft/semantic-kernel/tree/main/python/semantic_kernel/connectors/memory_stores/azure_cosmosdb).

###  Use as a vector database with LangChain

Use LangChain to orchestrate your information retrieval from Azure DocumentDB and your LLM. For more information, see [LangChain integrations for Azure DocumentDB](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db/).

### Use as a semantic cache with LangChain

Use LangChain and Azure DocumentDB to orchestrate Semantic Caching, using previously recorded LLM responses that can save you LLM API costs and reduce latency for responses. For more information, see [LangChain integration with Azure DocumentDB](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db/).

## Features and limitations

- Supported distance metrics: L2 (Euclidean), inner product, and cosine.
- Supported indexing methods: IVFFLAT, HNSW, and DiskANN.
- With DiskANN and [product quantization](./product-quantization.md), you can index vectors up to 16,000 dimensions.
- Using HNSW or IVF with [half-precision](./half-precision.md) allows indexing of vectors up to 4,000 dimensions.
- Without any compression, the default maximum vector dimension for indexing is 2,000.
- Indexing applies to only one vector per path.
- You can create only one index per vector path.

## Summary

This guide shows how to create a vector index, add documents that have vector data, perform a similarity search, and retrieve the index definition. By using our integrated vector database, you can efficiently store, index, and query high-dimensional vector data directly in Azure DocumentDB. It enables you to unlock the full potential of your data via [vector embeddings](/azure/ai-services/openai/concepts/understand-embeddings), and it empowers you to build more accurate, efficient, and powerful applications.

## Related content

- [.NET RAG pattern retail reference solution](https://github.com/Azure/Vector-Search-AI-Assistant-MongoDBvCore)
- [C# RAG pattern - Integrate OpenAI Services with Cosmos](https://github.com/microsoft/AzureDataRetrievalAugmentedGenerationSamples/tree/main/C%23/CosmosDB-MongoDBvCore)
- [Python RAG pattern - Azure product chatbot](https://github.com/microsoft/AzureDataRetrievalAugmentedGenerationSamples/tree/main/Python/CosmosDB-MongoDB-vCore)
- [Python notebook tutorial - Vector database integration through LangChain](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db)
- [Python notebook tutorial - LLM Caching integration through LangChain](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db/)
- [Python - LlamaIndex integration](https://developers.llamaindex.ai/python/examples/vector_stores/azurecosmosdbmongodbvcoredemo/)
- [Python - Semantic Kernel memory integration](https://github.com/microsoft/semantic-kernel/tree/main/python/semantic_kernel/connectors/memory_stores/azure_cosmosdb)

## Next step

> [!div class="nextstepaction"]
> [Create a lifetime free-tier cluster for Azure DocumentDB](free-tier.md)
