---
title: GenAI Frameworks and Azure Database for PostgreSQL
description: Integrate Azure Databases for PostgreSQL with AI and large language model (LLM) orchestration packages like Semantic Kernel and LangChain.
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

# Azure Database for PostgreSQL integrations for AI applications

Azure Database for PostgreSQL seamlessly integrates with leading large language model (LLM) orchestration packages like [Semantic Kernel](https://github.com/microsoft/semantic-kernel) and [LangChain](https://www.langchain.com/), enabling developers to harness the power of advanced AI capabilities within their applications. These orchestration packages can streamline the management and use of LLMs, embedding models, and databases, making it even easier to develop Generative AI applications.

| Integration Tool | Description | Azure Database for PostgreSQL | 
| --- | --- | --- |
| **[Semantic Kernel](https://github.com/microsoft/semantic-kernel)** | An open-source framework by Microsoft that combines AI agents with languages like C#, Python, and Java, enabling seamless orchestration of code and AI models. | [Python Connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-python) <br> [.NET Connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-csharp) <br> [Java Connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-java)
| **[LangChain](https://www.langchain.com/)** | A framework that simplifies the creation of applications powered by large language models (LLMs), offering tools for context-aware reasoning applications in Python, JavaScript, and Java. | [Python](https://python.langchain.com/docs/integrations/vectorstores/pgvector/) <br> [JavaScript](https://js.langchain.com/docs/integrations/vectorstores/pgvector/) | 
| **[LlamaIndex](https://www.llamaindex.ai/)** | A framework for building context-augmented AI applications that can integrate private or domain-specific data with LLMs for complex workflows. | [Python](https://docs.llamaindex.ai/en/stable/examples/vector_stores/postgres/) | 
| **[Microsoft GraphRAG](https://microsoft.github.io/graphrag/)** | Uses Azure Database for PostgreSQL to create AI-powered knowledge graphs, enabling robust data models and revealing relationships in semi-structured data. | [Quickstart](https://github.com/Azure-Samples/graphrag-legalcases-postgres/) | 

## Related content

- [Learn more about Azure OpenAI Service integration](generative-ai-azure-openai.md)
- [Learn more about Azure Machine Learning integration](generative-ai-azure-machine-learning.md)
- [Generate vector embeddings in Azure Database for PostgreSQL flexible server with locally deployed LLM (Preview)](generative-ai-azure-local-ai.md).
- [Integrate Azure Database for PostgreSQL with Azure Machine Learning Services](generative-ai-azure-machine-learning.md).
- [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL flexible server](generative-ai-azure-openai.md).
- [Azure AI extension in Azure Database for PostgreSQL flexible server](generative-ai-azure-overview.md).
- [Generative AI with Azure Database for PostgreSQL flexible server](generative-ai-overview.md).
- [Recommendation System with Azure Database for PostgreSQL flexible server and Azure OpenAI](generative-ai-recommendation-system.md).
- [Semantic Search with Azure Database for PostgreSQL flexible server and Azure OpenAI](generative-ai-semantic-search.md).
- [Enable and use pgvector in Azure Database for PostgreSQL flexible server](how-to-use-pgvector.md).
