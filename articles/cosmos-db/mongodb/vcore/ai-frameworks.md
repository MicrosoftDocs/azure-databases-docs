---
title: Integrations for AI apps
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Integrate Azure Cosmos DB for MongoDB with AI and large language model (LLM) orchestration packages like Semantic Kernel and LangChain.
author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 08/06/2025
ms.author: khelanmodi
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ MongoDB vCore
---

# Azure Cosmos DB for MongoDB integrations for AI applications

Azure Cosmos DB for MongoDB (vCore) seamlessly integrates with leading large language model (LLM) orchestration packages like [Semantic Kernel](https://github.com/microsoft/semantic-kernel) and [LangChain](https://www.langchain.com/), enabling developers to harness the power of advanced AI capabilities within their applications. These orchestration packages can streamline the management and use of LLMs, embedding models, and databases, making it even easier to develop Generative AI applications.

| Integration Tool | Description | Language | Type of Integration |
| --- | --- | --- | --- |
| **[LangChain](https://www.langchain.com/)** | A framework for building context-aware and reasoning-based applications powered by large language models. It provides a comprehensive set of tools for common AI workflows. | [Python](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db/) | Vector Store, Chat History, Semantic Cache |
| | | [JavaScript](https://js.langchain.com/docs/integrations/vectorstores/azure_cosmosdb_mongodb/) | Vector Store, Chat History |
| | | [Java](https://docs.langchain4j.dev/integrations/embedding-stores/azure-cosmos-mongo-vcore/) | Chat History |
| **[Semantic Kernel](https://github.com/microsoft/semantic-kernel)** | An open-source framework by Microsoft that integrates conventional programming languages with AI models. It's designed for orchestrating complex AI workflows and agents. | [Python](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-mongodb-connector?pivots=programming-language-python) | Vector Store |
| | | [.NET](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-mongodb-connector?pivots=programming-language-csharp) | Vector Store |
| **[LlamaIndex](https://www.llamaindex.ai/)** | A data framework for LLM applications that connects your custom data sources to large language models. It's ideal for building RAG (Retrieval-Augmented Generation) applications over private or domain-specific data. | [Python](https://docs.llamaindex.ai/en/stable/examples/vector_stores/AzureCosmosDBMongoDBvCoreDemo/) | Vector Store |
| | | TypeScript | Vector Store |
| **[CosmosAIGraph](https://aka.ms/cosmosaigraph)** | A solution that leverages Azure Cosmos DB for creating AI-powered knowledge graphs. It helps uncover complex relationships and insights within semi-structured data. | | [Quickstart](https://github.com/AzureCosmosDB/CosmosAIGraph/tree/main/impl) |

## Related content

- [Azure Cosmos DB Samples Gallery](https://aka.ms/AzureCosmosDB/Gallery)
- [Vector Search with Azure Cosmos DB for MongoDB](./vector-search.md)
- [Tokens](../../gen-ai/tokens.md)
- [Vector Embeddings](../../gen-ai/vector-embeddings.md)
- [Retrieval Augmented Generated (RAG)](../../gen-ai/rag.md)
- [30-day Free Trial without Azure subscription](https://azure.microsoft.com/try/cosmosdb/)

## Next step

> [!div class="nextstepaction"]
> [Use lifetime free tier of Integrated Vector Database in Azure Cosmos DB for MongoDB](free-tier.md)
