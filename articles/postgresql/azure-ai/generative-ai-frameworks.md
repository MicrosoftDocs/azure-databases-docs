---
title: Generative AI Frameworks and Azure Database for PostgreSQL
description: Integrate Azure Database for PostgreSQL with AI and large language model (LLM) orchestration packages like Semantic Kernel and LangChain.
author: abeomor
ms.author: abeomorogbe
ms.date: 03/17/2025
ms.update-cycle: 180-days
ms.service: azure-database-postgresql
ms.collection: ce-skilling-ai-copilot
ms.custom:
  - build-2025
ms.topic: concept-article
---

# Azure Database for PostgreSQL integrations for AI applications

Azure Database for PostgreSQL seamlessly integrates with leading large language model (LLM) orchestration packages so that developers can use advanced AI capabilities within their applications. These orchestration packages can streamline the management and use of LLMs, embedding models, and databases in developing generative AI applications.

## List of LLM orchestration packages

| Integration tool | Description | Azure Database for PostgreSQL |
| --- | --- | --- |
| [Semantic Kernel](https://github.com/microsoft/semantic-kernel) | An open-source framework by Microsoft that combines AI agents with languages like C#, Python, and Java. It enables seamless orchestration of code and AI models. | [Python connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-python) <br> [.NET connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-csharp) <br> [Java connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-java) |
| [LangChain](https://www.langchain.com/) | A framework that simplifies the creation of applications powered by LLMs. It offers tools for context-aware reasoning applications in Python, JavaScript, and Java. | [Python](generative-ai-develop-with-langchain.md) <br> [JavaScript](https://js.langchain.com/docs/integrations/vectorstores/pgvector/) |
| [LlamaIndex](https://www.llamaindex.ai/) | A framework for building context-augmented AI applications that can integrate private or domain-specific data with LLMs for complex workflows. | [Python](https://aka.ms/azpg-llamaindex) |
| [GraphRAG](https://microsoft.github.io/graphrag/) | A framework by Microsoft that uses Azure Database for PostgreSQL to create AI-powered knowledge graphs. It enables robust data models and reveals relationships in semistructured data. | [Quickstart](https://github.com/Azure-Samples/graphrag-legalcases-postgres/) |

## Related content

- [Use LangChain with Azure Database for PostgreSQL](generative-ai-develop-with-langchain.md)
- [AI agents in Azure Database for PostgreSQL](generative-ai-agents.md)
- [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL](generative-ai-azure-openai.md)
- [Generative AI with Azure Database for PostgreSQL](generative-ai-overview.md)
- [Enable and use pgvector in Azure Database for PostgreSQL](../extensions/../extensions/how-to-use-pgvector.md)
