---
title: Retrieval Augmented Generation
titleSuffix: Azure Cosmos DB
description: Learn about retrieval-augmented generation (RAG) in the context of Azure Cosmos DB for NoSQL's vector search capabilities.
author: TheovanKraay
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: concept-article
ms.date: 09/10/2025
ms.update-cycle: 180-days
ms.author: thvankra
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
  - ✅ PostgreSQL
---

# Retrieval-augmented generation (RAG) in Azure Cosmos DB

Retrieval-augmented generation (RAG) combines the power of large language models (LLMs) with robust information retrieval systems to create more accurate and contextually relevant responses. Unlike traditional generative models that rely solely on pretrained data, RAG architectures enhance an LLM's capabilities by integrating real-time information retrieval. This augmentation ensures responses aren't only generative but also grounded in the most relevant, up-to-date data available.

Azure Cosmos DB, an operational database that supports vector search, stands out as an excellent platform for implementing RAG. Its ability to handle both operational and analytical workloads in a single database, along with advanced features such as multitenancy and hierarchical partition keys, provides a solid foundation for building sophisticated generative AI applications.

## Key advantages of using Azure Cosmos DB

### Unified data storage and retrieval

Azure Cosmos DB enables seamless integration of [vector search](../nosql/vector-search.md) capabilities within a unified database system. This means that your operational data and vectorized data coexist, eliminating the need for separate indexing systems. 

### Real-time data ingestion and querying

Azure Cosmos DB supports real-time ingestion and querying, making it ideal for AI applications. This is crucial for RAG architectures, where the freshness of data can significantly affect the relevance of generated responses.

### Scalability and global distribution

Designed for large-scale applications, Azure Cosmos DB offers global distribution and [instant autoscale](../../cosmos-db/provision-throughput-autoscale.md). This ensures that your RAG-enabled application can handle high query volumes and deliver consistent performance irrespective of user location.

### High availability and reliability

Azure Cosmos DB offers comprehensive SLAs for throughput, latency, and [availability](/azure/reliability/reliability-cosmos-db-nosql). This reliability ensures that your RAG system is always available to generate responses with minimal downtime.

### Multitenancy with hierarchical partition keys

Azure Cosmos DB supports [multitenancy](../nosql/multi-tenancy-vector-search.md) through various performance and security isolation models, making it easier to manage data for different clients or user groups within the same database. This feature is particularly useful for SaaS applications where separation of tenant data is crucial for security and compliance.

### Comprehensive security features

With built-in features such as end-to-end encryption, role-based access control (RBAC), and virtual network integration, Azure Cosmos DB ensures that your data remains secure. These security measures are essential for enterprise-grade RAG applications that handle sensitive information.

## Implement RAG with Azure Cosmos DB

> [!TIP]
> For RAG samples, visit: [AzureDataRetrievalAugmentedGenerationSamples](https://github.com/microsoft/AzureDataRetrievalAugmentedGenerationSamples)

Here's a streamlined process for building a RAG application with Azure Cosmos DB:

1. **Data ingestion**: Store your documents, images, and other content types in Azure Cosmos DB. Utilize the database's support for vector search to index and retrieve vectorized content.
1. **Query execution**: When a user submits a query, Azure Cosmos DB can quickly retrieve the most relevant data using its vector search capabilities.
1. **LLM integration**: Pass the retrieved data to an LLM (for example, Azure OpenAI) to generate a response. The well-structured data provided by Cosmos DB enhances the quality of the model's output.
1. **Response generation**: The LLM processes the data and generates a comprehensive response, which is then delivered to the user.

## Related content

- [What is a vector database?](../vector-database.md)
- [Vector database in Azure Cosmos DB NoSQL](../nosql/vector-search.md)
- [Vector database in Azure Cosmos DB for MongoDB](../mongodb/vcore/vector-search.md)
- [What are tokens?](tokens.md)
- [Vector embeddings](vector-embeddings.md)
- [What are distance functions?](distance-functions.md)
- [kNN vs ANN vector search algorithms](knn-vs-ann.md)
- [Multitenancy for vector search](../nosql/multi-tenancy-vector-search.md)
