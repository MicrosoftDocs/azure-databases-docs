---
title: Sharded DiskANN Focused Vector Search for Better Performance and Lower Cost
titleSuffix: Azure Cosmos DB
description: Learn how to set up Sharded DiskANN for focused vector search with improved performance and lower costs
author: jcodella
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: concept-article
ms.author: jacodel
ms.date: 04/22/2025
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
---

# Sharded DiskANN: Focused vector search

Sharded DiskANN is a feature that allows a user to manually shard (or partition) a DiskANN vector index into smaller or more manageable indexes that are more efficient to search through. You can define an optional parameter in your container’s indexing policy, the `vectorIndexShardKey`, which points to a property in your documents. This essentially creates multiple distinct DiskANN vector indexes for your container, one for each unique value that the property can take. 

Sharded DiskANN offers many benefits including:
- **Lower latency.** Each sharded DiskANN vector index  is smaller in size than one larger index. This can mean that vector search completes in less time.
- **Lower cost.** Searching on a smaller index requires less computational work and can lead to lower RU charges.
- **Improved Recall.** By isolating search to a smaller DiskANN index defined for the VectorIndexShardKey, you’re able to achieve higher recall and accuracy in search results, as the search is performed on a more focused subset of data.
- **Scalability.** Sharding allows the system to handle larger datasets by distributing the data across multiple shards, making it easier to scale as the dataset grows.
- **Isolation of Vector Data.** Sharded DiskANN ensures that vector data can be isolated based on specific attributes (shard keys), providing better data management, and security. Your searches are constrained to data items only matching that shard key.

## Use cases

Sharded DiskANN is useful in the following scenarios:
- **Multi-Tenant Environments.** In multitenant scenarios, Sharded DiskANN allows for the isolation of data for different tenants, ensuring that each tenant's data is queried independently.
- **Category-Specific Searches.** Sharded DiskANN enables efficient category-specific vector search by partitioning the index based on a property that defines a category of your data. Then vector searches can be executed exclusively for that category. 


## How to use Sharded DiskANN
### Use DiskANN without sharding
As the VectorIndexShard key is an optional parameter, omitting it creates one DiskANN index per physical partition as usual.

```json
  "vectorIndexes": [
    {"path": "/vector2", "type": "DiskANN} 
]
```

### Use a vectorIndexShardKey
Here, we can see an example of defining the shard key based on a tenantID property. This can be any property of the data item, even the partition key. The single string needs to be enclosed in an array. 

```json
"vectorIndexes": [
    {
        "path": "/vector2",
        "type": "DiskANN",
        "vectorIndexShardKey": ["/tenantID"]
    }
]
```

### Write a vector search query focused to a shard key
To focus a vector search query on the specific shard key value, simply filter the path to the value using a WHERE clause as in the following example:

```sql
SELECT TOP 10 *
FROM c
ORDER BY VectorDistance(c.vector, {queryVector})
WHERE c.tenantID = "tenant1"
```

## Related content

- [What is a vector database?](../vector-database.md)
- [Retrieval Augmented Generation (RAG)](rag.md)
- [Vector database in Azure Cosmos DB NoSQL](../vector-search.md)
