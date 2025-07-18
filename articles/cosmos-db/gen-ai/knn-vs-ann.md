---
title: kNN and ANN algorithm comparison
titleSuffix: Azure Cosmos DB
description: Compare and contrast k-Nearest Neighbors (kNN) and Approximate Nearest Neighbors (ANN) algorithms in relation to Azure Cosmos DB.
author: wmwxwa
ms.author: wangwilliam
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 12/03/2024
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB vCore
  - ✅ PostgreSQL
---

# kNN vs ANN

Two major categories of vector search algorithms are k-Nearest Neighbors (kNN) and Approximate Nearest Neighbors (ANN, not to be confused with Artificial Neural Network). kNN is precise but computationally intensive, making it less suitable for large datasets. ANN, on the other hand, offers a balance between accuracy and efficiency, making it better suited for large-scale applications.

## How kNN works

1. Vectorization: Each data point in the dataset is represented as a vector in a multi-dimensional space.
1. Distance Calculation: To classify a new data point (query point), the algorithm calculates the distance between the query point and all other points in the dataset using a [distance function](distance-functions.md).
1. Finding Neighbors: The algorithm identifies the k closest data points (neighbors) to the query point based on the calculated distances. The value of k (the number of neighbors) is crucial. A small k can be sensitive to noise, while a large k can smooth out details.
1. Making Predictions:
  - Classification: For classification tasks, kNN assigns the class label to the query point that is most common among the k neighbors. Essentially, it performs a "majority vote."
  - Regression: For regression tasks, kNN predicts the value for the query point as the average (or sometimes weighted average) of the values of the k neighbors.

## How ANN works

1. Vectorization: Each data point in the dataset is represented as a vector in a multi-dimensional space.
1. Indexing and Data Structures: ANN algorithms use advanced data structures (e.g., KD-trees, locality-sensitive hashing, or graph-based methods) to index the data points, allowing for faster searches.
1. Distance Calculation: Instead of calculating the exact distance to every point, ANN algorithms use heuristics to quickly identify regions of the space that are likely to contain the nearest neighbors.
1. Finding Neighbors: The algorithm identifies a set of data points that are likely to be close to the query point. These neighbors are not guaranteed to be the exact closest points but are close enough for practical purposes.
1. Making Predictions:
  - Classification: For classification tasks, ANN assigns the class label to the query point that is most common among the identified neighbors, similar to kNN.
  - Regression: For regression tasks, ANN predicts the value for the query point as the average (or weighted average) of the values of the identified neighbors.

## Related content

- [What is a vector database?](../vector-database.md)
- [Retrieval Augmented Generation (RAG)](rag.md)
- [Vector database in Azure Cosmos DB NoSQL](../nosql/vector-search.md)
- [Vector database in Azure Cosmos DB for MongoDB](../mongodb/vcore/vector-search.md)
- [What is vector search?](vector-search-overview.md)
- LLM [tokens](tokens.md)
- Vector [embeddings](vector-embeddings.md)
- [Distance functions](distance-functions.md)
