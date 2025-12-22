---
title: Vector Stores in Azure Database for PostgreSQL
description: Enhance AI-based applications by using the integrated vector store functionality in Azure Database for PostgreSQL.
author: abeomor
ms.author: abeomorogbe
ms.date: 03/17/2025
ms.update-cycle: 180-days
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.collection: ce-skilling-ai-copilot
ms.custom:
  - build-2025
ms.topic: concept-article
---

# Vector stores in Azure Database for PostgreSQL

Vector stores are used in numerous domains and situations across analytical and generative AI, including natural language processing, video and image recognition, recommendation systems, and search.

## What is a vector store?

A vector store (also called a vector database) is a database that stores and manages vector embeddings. Vector embeddings are mathematical representations of data in a high-dimensional space.

In this space, each dimension corresponds to a feature of the data. Tens of thousands of dimensions might be used to represent sophisticated data. A vector's position in this space represents its characteristics. Words, phrases, entire documents, images, audio, and other types of data can all be vectorized.

## How does a vector store work?

In a vector store, you use vector search algorithms to index and query embeddings. Well-known vector search algorithms include [Disk Approximate Nearest Neighbor (DiskANN)](../extensions/how-to-optimize-performance-pgvector.md#disk-approximate-nearest-neighbor-diskann), [Hierarchical Navigable Small World (HNSW)](../extensions/how-to-optimize-performance-pgvector.md#hierarchical-navigable-small-worlds-hnsw), and [Inverted File with Flat Compression (IVFFlat)](../extensions/how-to-optimize-performance-pgvector.md#inverted-file-with-flat-compression-ivfflat).

Vector search is a method that helps you find similar items based on their data characteristics rather than by exact matches on a property field. This technique is useful in applications such as searching for similar text, finding related images, making recommendations, or even detecting anomalies.

Vector search is used to query the [vector embeddings](/azure/ai-services/openai/concepts/understand-embeddings) of your data that you created by using a machine learning model, via an embeddings API. Examples of embeddings APIs are [Azure OpenAI Embeddings](/azure/ai-services/openai/how-to/embeddings) and [Hugging Face on Azure](https://azure.microsoft.com/solutions/hugging-face-on-azure/).

Vector search measures the distance between the data vectors and your query vector. The data vectors that are closest to your query vector are the ones that are most similar semantically.

When you're using [Azure Database for PostgreSQL as a vector store](../extensions/../extensions/how-to-use-pgvector.md), you can store, index, and query embeddings alongside the original data. This approach eliminates the extra cost of replicating data in a separate, pure vector database.

This architecture also keeps the vector embeddings and original data together. Keeping the embeddings and the data together better facilitates multimodal data operations. It also enables greater data consistency, scale, and performance.

## Related content

- [Enable the vector store and search feature](../extensions/../extensions/how-to-use-pgvector.md)
- [Optimize the performance of a vector store](../extensions/how-to-optimize-performance-pgvector.md)
