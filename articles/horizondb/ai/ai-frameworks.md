---
title: Generative AI Frameworks and Azure HorizonDB
description: Integrate Azure HorizonDB with AI and large language model (LLM) orchestration frameworks like Microsoft Agent Framework, Semantic Kernel, LangChain, LlamaIndex and CrewAI to build AI applications.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: ai-frameworks
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
---

# Build AI Applications with Azure HorizonDB and LLM Orchestration Frameworks

Azure HorizonDB seamlessly integrates with leading large language model (LLM) orchestration frameworks so that developers can use advanced AI capabilities within their applications. These frameworks can streamline the management and use of LLMs, embedding models, and databases in developing generative AI applications.

## LLM framework integrations

The following table highlights some popular LLM orchestration frameworks that integrate with Azure HorizonDB.

| Integration tool | Description | Azure HorizonDB |
| --- | --- | --- |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) (incorporating [Semantic Kernel](https://github.com/microsoft/semantic-kernel)) | A unified, production-ready open-source SDK by Microsoft for building AI agents in .NET and Python. It merges the orchestration and plugin capabilities of Semantic Kernel with multi-agent workflow patterns. It uses the same PostgreSQL connectors as Semantic Kernel. | [Python connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-python)<br />[.NET connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-csharp)<br />[Java connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-java) |
| [LangChain](https://www.langchain.com/) | A framework that simplifies the creation of applications powered by LLMs. It offers tools for context-aware reasoning applications in Python, JavaScript, and Java. | [Python](develop-with-langchain.md)<br />[JavaScript](https://docs.langchain.com/oss/javascript/langchain/overview) |
| [LlamaIndex](https://www.llamaindex.ai/) | A framework for building context-augmented AI applications that can integrate private or domain-specific data with LLMs for complex workflows. | [Python](https://aka.ms/azpg-llamaindex) |
| [GraphRAG](https://microsoft.github.io/graphrag/) | A framework by Microsoft that uses Azure HorizonDB to create AI-powered knowledge graphs. It enables robust data models and reveals relationships in semistructured data. | [Quickstart](https://github.com/Azure-Samples/graphrag-legalcases-postgres/) |
| [CrewAI](https://www.crewai.com/) | An open-source framework for orchestrating autonomous AI agents with role-based collaboration, task delegation, and multi-agent workflows. It supports PostgreSQL integration through its PGSearchTool for semantic search. | [PGSearchTool](https://docs.crewai.com/en/tools/database-data/pgsearchtool) |

## Related content

- [Develop AI apps with LangChain and Azure HorizonDB](develop-with-langchain.md)
- [Build AI Agents with Azure HorizonDB](ai-agents.md)
- [Implement Agent Knowledge Retrieval with Azure HorizonDB and Foundry](foundry-agent-integration.md)
- [Graph-augmented RAG patterns with Azure Database for PostgreSQL](graphrag.md)
- [Overview of AI capabilities in Azure HorizonDB](overview.md)
- [Implement vector search in Azure HorizonDB using the pgvector extension](vector-search-pgvector.md)
- [Generate vector embeddings using the create_embeddings() AI function](generate-vector-embeddings.md)
