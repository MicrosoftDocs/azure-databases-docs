---
title: AI Frameworks for Building Apps and Agents with Azure HorizonDB
description: Integrate Azure HorizonDB with AI and LLM orchestration frameworks like Microsoft Agent Framework, Semantic Kernel, LangChain, LlamaIndex, and CrewAI to build AI applications and agents.
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

# Build AI apps and agents with orchestration frameworks (Preview)

Azure HorizonDB integrates with leading LLM orchestration frameworks for building both AI applications and autonomous agents. These frameworks provide the scaffolding for managing LLMs, embedding models, agent memory, multi-agent workflows, and database connectivity.

## Framework integrations

The following frameworks and services integrate with Azure HorizonDB:

| Framework | Description | Azure HorizonDB integration |
| --- | --- | --- |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) (incorporating [Semantic Kernel](https://github.com/microsoft/semantic-kernel)) | A unified, production-ready open-source SDK by Microsoft for building AI agents in .NET and Python. It merges the orchestration and plugin capabilities of Semantic Kernel with multi-agent workflow patterns. | [Python connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-python)<br />[.NET connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-csharp)<br />[Java connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-java) |
| [LangChain / LangGraph](https://www.langchain.com/) | LangChain simplifies LLM application development with tools for context-aware reasoning in Python and JavaScript. [LangGraph](https://langchain-ai.github.io/langgraph/) adds stateful, graph-based orchestration for complex multi-agent workflows with checkpointed execution. | [Develop AI apps (in Python) with LangChain and Azure HorizonDB](develop-with-langchain.md)<br />[JavaScript](https://docs.langchain.com/oss/javascript/langchain/overview) |
| [LlamaIndex](https://www.llamaindex.ai/) | A framework for building context-augmented AI applications that integrates private or domain-specific data with LLMs for complex workflows. Excels at structured data retrieval and knowledge-graph-powered reasoning. | [Python](https://aka.ms/azpg-llamaindex) |
| [GraphRAG](https://microsoft.github.io/graphrag/) | A framework by Microsoft that uses Azure HorizonDB to create AI-powered knowledge graphs. It enables robust data models and reveals relationships in semistructured data. | [Quickstart](https://github.com/Azure-Samples/graphrag-legalcases-postgres/) |
| [CrewAI](https://crewai.com) | An open-source framework for orchestrating role-based, collaborative multi-agent workflows with task delegation and standard operating procedures. | [PGSearchTool](https://docs.crewai.com/en/tools/database-data/pgsearchtool) |
| [AutoGen](https://microsoft.github.io/autogen/) | A Microsoft framework for multi-agent conversation patterns. Supports flexible agent communication topologies and tool integration. | [PostgreSQL tools](https://microsoft.github.io/autogen/) |
| [Microsoft Foundry Agent Service](/azure/ai-services/agents/overview) | A managed service for building, deploying, and scaling AI agents with built-in tool support, tracing, and monitoring. | [Implement Agent Knowledge Retrieval with Azure HorizonDB, Foundry, and MCP](foundry-agent-integration.md) |

## Related content

- [Develop AI apps with LangChain and Azure HorizonDB](develop-with-langchain.md)
- [Build AI agents with Azure HorizonDB](ai-agents.md)
- [Implement Agent Knowledge Retrieval with Azure HorizonDB, Foundry, and MCP](foundry-agent-integration.md)
