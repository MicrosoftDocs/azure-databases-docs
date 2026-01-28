---
title: Vector Distance Functions
description: Learn about Manhattan, Euclidean, cosine similarity, and dot product vector distance functions in Azure Cosmos DB for NoSQL.
author: wmwxwa
ms.author: wangwilliam
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 09/09/2025
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
---

# What are distance functions?

Distance functions are mathematical formulas used to measure the similarity or dissimilarity between vectors. Common examples include Manhattan distance, Euclidean distance, cosine similarity, and dot product. These measurements are crucial for determining how closely related two pieces of data are.

To learn more about vectors, see [vector search](vector-search-overview.md).

## Manhattan distance

*Manhattan distance* measures the distance between two points by adding up the absolute differences between their coordinates. Imagine walking in a grid-like city, such as the many neighborhoods in Manhattan; it's the total number of blocks you walk north-south and east-west.

## Euclidean distance

*Euclidean distance* measures the straight-line distance between two points. It's named after the ancient mathematician Euclid, who is often referred to as the "father of geometry."

## Cosine similarity

*Cosine similarity* measures the cosine of the angle between two vectors projected in a multidimensional space. Two documents might be far apart by Euclidean distance because of document sizes, but they could still have a smaller angle between them and therefore high cosine similarity.

## Dot product

*Dot product* is the result of two vectors that are multiplied to return a single number. It combines the two vectors' magnitudes, and the cosine of the angle between them, showing how much one vector goes in the direction of another.

## Related content

- [VectorDistance system function](/cosmos-db/query/vectordistance) in Azure Cosmos DB NoSQL
- [What is a vector database?](../vector-database.md)
- [Retrieval-augmented generation (RAG)](rag.md)
- [Vector search in Azure Cosmos DB](vector-search-overview.md)
- [Vector search in Azure Cosmos DB for NoSQL](../vector-search.md)
- [Vector store in Azure Cosmos DB for MongoDB vCore](../mongodb/vcore/vector-search.md)
- [Large language model tokens](tokens.md)
- [Vector embeddings in Azure Cosmos DB](vector-embeddings.md)
- [kNN vs ANN vector search algorithms](knn-vs-ann.md)
