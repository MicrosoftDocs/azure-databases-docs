---
title: Vector Databases and Azure Database for PostgreSQL
description: Enhance AI-based applications using the integrated vector store functionality in Azure Database for PostgreSQL
author: abeomor
ms.author: abeomorogbe
ms.date: 03/17/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.collection: ce-skilling-ai-copilot
ms.custom:
  - build-2025
ms.topic: conceptual
---

# Vector search in Azure Database for PostgreSQL

Vector databases are used in numerous domains and situations across analytical and generative AI, including natural language processing, video and image recognition, recommendation system, and search, among others.

## What is a vector store?

A vector store or vector database is a database designed to store and manage vector embeddings, which are mathematical representations of data in a high-dimensional space. In this space, each dimension corresponds to a feature of the data, and tens of thousands of dimensions might be used to represent sophisticated data. A vector's position in this space represents its characteristics. Words, phrases, or entire documents, and images, audio, and other types of data can all be vectorized.

## How does a vector store work?

In a vector store, vector search algorithms are used to index and query embeddings. Some well-known vector search algorithms include [DiskANN](how-to-optimize-performance-pgvector.md#disk-approximate-nearest-neighbor-diskann), [Hierarchical Navigable Small World (HNSW)](how-to-optimize-performance-pgvector.md#hierarchical-navigable-small-worlds-hnsw), [Inverted File (IVF)](how-to-optimize-performance-pgvector.md#inverted-file-with-flat-compression-ivfflat), etc. Vector search is a method that helps you find similar items based on their data characteristics rather than by exact matches on a property field. This technique is useful in applications such as searching for similar text, finding related images, making recommendations, or even detecting anomalies. It's used to query the [vector embeddings](/azure/ai-services/openai/concepts/understand-embeddings) of your data that you created by using a machine learning model by using an embeddings API. Examples of embeddings APIs are [Azure OpenAI Embeddings](/azure/ai-services/openai/how-to/embeddings) or [Hugging Face on Azure](https://azure.microsoft.com/solutions/hugging-face-on-azure/). Vector search measures the distance between the data vectors and your query vector. The data vectors that are closest to your query vector are the ones that are found to be most similar semantically.

When using [Azure Database for Postgres as a vector store](how-to-use-pgvector.md), embeddings can be stored, indexed, and queried alongside the original data. This approach eliminates the extra cost of replicating data in a separate pure vector database. Moreover, this architecture keeps the vector embeddings and original data together, which better facilitates multi-modal data operations, and enables greater data consistency, scale, and performance.


## Related content
- [Enable the vector store and search feature](how-to-use-pgvector.md)
- [Optimize performance of Vector Database](how-to-optimize-performance-pgvector.md).
