---

title: Integrations with Azure Cosmos DB for AI apps
description: Learn about integrations with AI/LLM orchestration packages
author: jcodella
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 9/16/2024
ms.author: jacodel

---

# Integrations

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]


Azure Cosmos DB seamlessly integrates with leading large language model (LLM) orchestration packages like [Semantic Kernel](https://github.com/microsoft/semantic-kernel) and [LangChain](https://www.langchain.com/), enabling developers to harness the power of advanced AI capabilities within their applications. These orchestration packages can streamline the management and use of LLMs, embedding models, and databases, making it even easier to develop Generative AI applications.

## Semantic Kernel
[Semantic Kernel](/semantic-kernel/overview/) is an open-source framework, developed by Microsoft, that allows developers to build advanced AI applications by integrating AI agents with conventional programming languages like C#, Python, and Java, enabling seamless orchestration of code and AI models.

**Azure Cosmos DB for NoSQL**
- [Python](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-nosql-connector?pivots=programming-language-python)
- [.NET](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-nosql-connector?pivots=programming-language-csharp)

**Azure Cosmos DB for MongoDB vCore**
- [Python](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-mongodb-connector?pivots=programming-language-python)
- [.NET](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-mongodb-connector?pivots=programming-language-csharp)

## LangChain
[LangChain](https://www.langchain.com/) is a framework designed to simplify the development of applications powered by large language models (LLMs), providing modular components and tools for building, deploying, and monitoring context-aware reasoning applications. LangChain is supported in Python, JavaScript, and Java (through a third party effort)

**Azure Cosmos DB for NoSQL**
- [Python](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db_no_sql/)
- [JavaScript](https://js.langchain.com/docs/integrations/vectorstores/azure_cosmosdb_nosql/)
- [Java](https://docs.langchain4j.dev/integrations/embedding-stores/azure-cosmos-nosql/)

**Azure Cosmos DB for MongoDB vCore**
- [Python](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db/)
- [JavaScript](https://js.langchain.com/docs/integrations/vectorstores/azure_cosmosdb_mongodb/)
- [Java](https://docs.langchain4j.dev/integrations/embedding-stores/azure-cosmos-mongo-vcore/)

## LlamaIndex
[LlamaIndex](https://www.llamaindex.ai/) is a framework for creating context-augmented generative AI applications, offering tools to ingest, parse, index, and query data, enabling the integration of private or domain-specific data with LLMs for complex workflows and agents.

**Azure Cosmos DB for NoSQL**
- [Python](https://docs.llamaindex.ai/en/stable/examples/vector_stores/AzureCosmosDBNoSqlDemo/)

**Azure Cosmos DB for MongoDB vCore**
- [Python](https://docs.llamaindex.ai/en/stable/examples/vector_stores/AzureCosmosDBMongoDBvCoreDemo/)

## CosmosAIGraph
[CosmosAIGraph](https://aka.ms/cosmosaigraph) uses Azure Cosmos DB to create AI-powered knowledge graphs, integrating advanced graph database capabilities with AI for robust data management and querying. It utilizes Cosmos DB’s scalability and performance to build sophisticated data models, uncovering hidden relationships and concepts in semi-structured data.

**Azure Cosmos DB for NoSQL**
- [Quickstart](https://github.com/AzureCosmosDB/CosmosAIGraph/tree/main/impl/docs#quick-start)

**Azure Cosmos DB for MongoDB vCore**
- [Quickstart](https://github.com/AzureCosmosDB/CosmosAIGraph/tree/main/impl/docs#quick-start)

## Next steps

Check out these resources here to get started with vector search and building AI apps:

- [Azure Cosmos DB Samples Gallery](https://aka.ms/AzureCosmosDB/Gallery)
- [Vector Search with Azure Cosmos DB for NoSQL](vector-search-overview.md)
- [Tokens](tokens.md)
- [Vector Embeddings](vector-embeddings.md)
- [Retrieval Augmented Generated (RAG)](rag.md)
- [30-day Free Trial without Azure subscription](https://azure.microsoft.com/try/cosmosdb/)
- [90-day Free Trial and up to $6,000 in throughput credits with Azure AI Advantage](../ai-advantage.md)

> [!div class="nextstepaction"]
> [Use the Azure Cosmos DB lifetime free tier](../free-tier.md)
