---
title: kNN and ANN Algorithm Comparison
titleSuffix: Azure Cosmos DB
description: Compare and contrast k-Nearest Neighbors (kNN) and Approximate Nearest Neighbors (ANN) algorithms in relation to Azure Cosmos DB.
author: wmwxwa
ms.author: wangwilliam
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 09/10/2025
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
  - ✅ PostgreSQL
---

# Compare kNN and ANN

Two major categories of vector search algorithms are k-Nearest Neighbors (kNN) and Approximate Nearest Neighbors (ANN, not to be confused with Artificial Neural Network). kNN is precise but computationally intensive, making it less suitable for large datasets. ANN, on the other hand, offers a balance between accuracy and efficiency, making it better suited for large-scale applications.

## How kNN works

- Vectorization: Each data point in the dataset is represented as a vector in a multi-dimensional space.
- Distance calculation: To classify a new data point (query point), the algorithm calculates the distance between the query point and all other points in the dataset using a [distance function](distance-functions.md).
- Finding neighbors: The algorithm identifies the k closest data points (neighbors) to the query point based on the calculated distances. The value of k (the number of neighbors) is crucial. A small k can be sensitive to noise, while a large k can smooth out details.
- Making predictions:
    - Classification: For classification tasks, kNN assigns the class label to the query point that's most common among the k neighbors. Essentially, it performs a *majority vote*.
    - Regression: For regression tasks, kNN predicts the value for the query point as the average (or sometimes weighted average) of the values of the k neighbors.

## How ANN works

- Vectorization: Each data point in the dataset is represented as a vector in a multi-dimensional space.
- Indexing and data structures: ANN algorithms use advanced data structures (for example, KD-trees, locality-sensitive hashing, or graph-based methods) to index the data points, allowing for faster searches.
- Distance calculation: Instead of calculating the exact distance to every point, ANN algorithms use heuristics to quickly identify regions of the space that are likely to contain the nearest neighbors.
- Finding neighbors: The algorithm identifies a set of data points that are likely to be close to the query point. These neighbors aren't guaranteed to be the exact closest points but are close enough for practical purposes.
- Making predictions:
    - Classification: For classification tasks, ANN assigns the class label to the query point that's most common among the identified neighbors, similar to kNN.
    - Regression: For regression tasks, ANN predicts the value for the query point as the average (or weighted average) of the values of the identified neighbors.

## Related content

- [What is a vector database?](../vector-database.md)
- [Retrieval-augmented generation (RAG)](rag.md)
- [Vector database in Azure Cosmos DB NoSQL](../nosql/vector-search.md)
- [Vector database in Azure Cosmos DB for MongoDB](../mongodb/vcore/vector-search.md)
- [What is vector search?](vector-search-overview.md)
- [What are tokens?](tokens.md)
- [Vector embeddings](vector-embeddings.md)
- [Distance functions](distance-functions.md)
