---
title: Integrations for AI apps
description: Integrate Azure DocumentDB with AI and large language model (LLM) orchestration packages like Semantic Kernel and LangChain.
author: khelanmodi
ms.topic: how-to
ms.date: 08/06/2025
ms.author: khelanmodi
ms.collection:
  - ce-skilling-ai-copilot
---

# Azure DocumentDB integrations for AI applications

Azure DocumentDB seamlessly integrates with leading large language model (LLM) orchestration packages like [Semantic Kernel](https://github.com/microsoft/semantic-kernel) and [LangChain](https://www.langchain.com/), enabling developers to harness the power of advanced AI capabilities within their applications. These orchestration packages can streamline the management and use of LLMs, embedding models, and databases, making it even easier to develop Generative AI applications.

| Integration Tool | Description | Language | Type of Integration |
| --- | --- | --- | --- |
| **[LangChain](https://www.langchain.com/)** | A framework for building context-aware and reasoning-based applications powered by large language models (LLM). | [Python](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db/) | Vector Store, Chat History, [Semantic Cache](https://python.langchain.com/docs/integrations/llm_caching/#azure-cosmos-db-semantic-cache) |
| | | [JavaScript](https://js.langchain.com/docs/integrations/vectorstores/azure_cosmosdb_mongodb/) | Vector Store, Semantic Cache, [Chat History](https://js.langchain.com/docs/integrations/platforms/microsoft#azure-cosmos-db-mongodb-vcore-chat-message-history) |
| | | [Java](https://docs.langchain4j.dev/integrations/embedding-stores/azure-cosmos-mongo-vcore/) | Chat History |
| **[LangChain-azure](https://github.com/langchain-ai/langchain-azure)** | A framework for building context-aware and reasoning-based applications powered by large language models (LLM) on Azure. | [Python](https://github.com/langchain-ai/langchain-azure/blob/main/libs/azure-ai/langchain_azure_ai/vectorstores/azure_cosmos_db_mongo_vcore.py) | Vector Store, Semantic Cache |
| **[Semantic Kernel](https://github.com/microsoft/semantic-kernel)** | An open-source framework by Microsoft that integrates conventional programming languages with AI models. It's designed for orchestrating complex AI agents. | [Python](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-mongodb-connector?pivots=programming-language-python) | Vector Store |
| | | [.NET](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-mongodb-connector?pivots=programming-language-csharp) | Vector Store |
| **[LlamaIndex](https://www.llamaindex.ai/)** | A data framework for LLM applications that connects your custom data sources to large language models (LLM). It's ideal for building RAG (Retrieval-Augmented Generation) applications over domain-specific data. | [Python](https://developers.llamaindex.ai/python/examples/vector_stores/azurecosmosdbmongodbvcoredemo/) | Vector Store, Document Store, Index Store |
| | | [TypeScript](https://developers.llamaindex.ai/python/examples/vector_stores/azurecosmosdbmongodbvcoredemo/) | Vector Store |
| **[DocumentDBAIGraph](https://aka.ms/cosmosaigraph)** | A solution that leverages Azure DocumentDB for creating AI-powered knowledge graphs. It helps uncover complex relationships within semi-structured data. | | [Quickstart](https://github.com/AzureCosmosDB/CosmosAIGraph/tree/main/impl) |

## Related content

- [Azure DocumentDB Samples Gallery](https://aka.ms/AzureCosmosDB/Gallery)
- [Vector Search with Azure DocumentDB](./vector-search.md)
- [30-day Free Trial without Azure subscription](https://azure.microsoft.com/try/cosmosdb/)

## Next step

> [!div class="nextstepaction"]
> [Get started for free](free-tier.md)
