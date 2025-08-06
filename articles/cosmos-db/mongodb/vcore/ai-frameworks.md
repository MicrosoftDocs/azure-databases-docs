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

# Azure Cosmos DB integrations for AI applications

Azure Cosmos DB seamlessly integrates with leading large language model (LLM) orchestration packages like [Semantic Kernel](https://github.com/microsoft/semantic-kernel) and [LangChain](https://www.langchain.com/), enabling developers to harness the power of advanced AI capabilities within their applications. These orchestration packages can streamline the management and use of LLMs, embedding models, and databases, making it even easier to develop Generative AI applications.

| Integration Tool | Description | Azure Cosmos DB for MongoDB (vCore) |
| --- | --- | --- | --- |
| **[Semantic Kernel](https://github.com/microsoft/semantic-kernel)** | An open-source framework by Microsoft that combines AI agents with languages like C#, Python, and Java, enabling seamless orchestration of code and AI models. | [Python Connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-nosql-connector?pivots=programming-language-python) <br> [.NET Connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-nosql-connector?pivots=programming-language-csharp) | [Python Connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-mongodb-connector?pivots=programming-language-python) <br> [.NET Connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-mongodb-connector?pivots=programming-language-csharp) |
| **[LangChain](https://www.langchain.com/)** | A framework that simplifies the creation of applications powered by large language models (LLMs), offering tools for context-aware reasoning applications in Python, JavaScript, and Java. | [Python](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db_no_sql/) <br> [JavaScript](https://js.langchain.com/docs/integrations/vectorstores/azure_cosmosdb_nosql/) <br> [Java](https://docs.langchain4j.dev/integrations/embedding-stores/azure-cosmos-nosql/) | [Python](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db/) <br> [JavaScript](https://js.langchain.com/docs/integrations/vectorstores/azure_cosmosdb_mongodb/) <br> [Java](https://docs.langchain4j.dev/integrations/embedding-stores/azure-cosmos-mongo-vcore/) |
| **[LlamaIndex](https://www.llamaindex.ai/)** | A framework for building context-augmented AI applications that can integrate private or domain-specific data with LLMs for complex workflows. | [Python](https://docs.llamaindex.ai/en/stable/examples/vector_stores/AzureCosmosDBNoSqlDemo/) | [Python](https://docs.llamaindex.ai/en/stable/examples/vector_stores/AzureCosmosDBMongoDBvCoreDemo/) |
| **[CosmosAIGraph](https://aka.ms/cosmosaigraph)** | Uses Azure Cosmos DB to create AI-powered knowledge graphs, enabling robust data models and revealing relationships in semi-structured data. | [Quickstart](https://github.com/AzureCosmosDB/CosmosAIGraph/tree/main/impl) | [Quickstart](https://github.com/AzureCosmosDB/CosmosAIGraph/tree/main/impl) |

## Related content

- [Azure Cosmos DB Samples Gallery](https://aka.ms/AzureCosmosDB/Gallery)
- [Vector Search with Azure Cosmos DB for MongoDB](../mongodb/vcore/vector-search.md)
- [Tokens](tokens.md)
- [Vector Embeddings](vector-embeddings.md)
- [Retrieval Augmented Generated (RAG)](rag.md)
- [30-day Free Trial without Azure subscription](https://azure.microsoft.com/try/cosmosdb/)
- [90-day Free Trial and up to $6,000 in throughput credits with Azure AI Advantage](../ai-advantage.md)

## Next step

> [!div class="nextstepaction"]
> [Use lifetime free tier of Integrated Vector Database in Azure Cosmos DB for MongoDB](free-tier.md)
