---
title: Integrations for AI
description: Learn how to integrate Azure Cosmos DB with AI and large language model (LLM) orchestration frameworks like Semantic Kernel, LangChain, and LlamaIndex for building intelligent applications.
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 10/20/2025
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
---

# Azure Cosmos DB integrations for AI applications

Azure Cosmos DB integrates seamlessly with popular AI and large language model (LLM) orchestration frameworks to help you build intelligent applications. This article provides an overview of the available integrations with Semantic Kernel, LangChain, and LlamaIndex, along with links to their respective connectors and documentation.

## Integrations

| | Description | Azure Cosmos DB Resources | 
| --- | --- | --- |
| **[Semantic Kernel](https://github.com/microsoft/semantic-kernel)** | An open-source framework by Microsoft that combines AI agents with languages like C#, Python, and Java, enabling seamless orchestration of code and AI models. | [Python Connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-nosql-connector?pivots=programming-language-python) <br> [.NET Connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-nosql-connector?pivots=programming-language-csharp) |
| **[LangChain](https://www.langchain.com/)** | A framework that simplifies the creation of applications powered by large language models (LLMs), offering tools for context-aware reasoning applications in Python, JavaScript, and Java. | [Python](https://developers.llamaindex.ai/python/examples/vector_stores/azurecosmosdbnosqldemo/) <br> [JavaScript](https://js.langchain.com/docs/integrations/vectorstores/azure_cosmosdb_nosql/) <br> [Java](https://docs.langchain4j.dev/integrations/embedding-stores/azure-cosmos-nosql/) | 
| **[LangGraph](https://www.langchain.com/langgraph)** | A library from LangChain for building stateful, multi-actor applications with LLMs, used to create agent and multi-agent workflows. | [Python Checkpoint Saver](https://pypi.org/project/langgraph-checkpoint-cosmosdb/) |
| **[LlamaIndex](https://www.llamaindex.ai/)** | A framework for building context-augmented AI applications that can integrate private or domain-specific data with LLMs for complex workflows. | [Python](https://developers.llamaindex.ai/python/examples/vector_stores/azurecosmosdbnosqldemo/) |
| **[Spring AI](https://spring.io/projects/spring-ai)** | A Spring-based framework that provides a consistent API for AI engineering, bringing familiar Spring design patterns to AI application development in Java. | [Java Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/azure-cosmos-db.html) |

## Related content

- [Azure Cosmos DB Samples Gallery](https://aka.ms/AzureCosmosDB/Gallery)
- [Vector Search with Azure Cosmos DB for NoSQL](vector-search-overview.md)
- [Tokens](tokens.md)
- [Vector Embeddings](vector-embeddings.md)
- [Retrieval Augmented Generated (RAG)](rag.md)
