---
title: Build AI Agents with Azure HorizonDB
description: Learn what AI agents are, why databases and PostgreSQL are essential for agent memory and knowledge, and how to build intelligent agents with Azure HorizonDB.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: ai-agents
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
# customer intent: As a user, I want to understand what AI agents are, why databases are essential for agents, and how Azure HorizonDB supports agent memory, knowledge retrieval, and tool integration for building scalable AI agents.
---

# Build AI agents with Azure HorizonDB (Preview)

AI agents are transforming how applications interact with data. Unlike traditional applications that follow fixed logic, agents combine large language models (LLMs) with external tools, memory, and planning to autonomously reason through complex tasks. Azure HorizonDB provides the unified data layer that agents need: persistent memory, knowledge retrieval, and scalable storage, all inside a single PostgreSQL database.

## What are AI agents?

AI agents go beyond simple chatbots or standalone LLMs. An agent is a system that uses an LLM as its reasoning core, augmented with the ability to:

- **Plan**: Break down complex goals into sequential or parallel subtasks.
- **Use tools**: Call APIs, execute code, query databases, and interact with external services.
- **Perceive**: Process and understand inputs from diverse data sources - text, images, structured data.
- **Remember**: Store and recall context from current and past interactions to make better decisions.

These capabilities make agents fundamentally different from traditional retrieval-augmented generation (RAG) systems.

### How agents differ from RAG

Traditional RAG follows a fixed pipeline: retrieve documents via vector search, pass them as context to an LLM, and generate a response. It works for simple question-answering but can't break down multi-step queries, choose between tools, remember prior interactions, or self-correct. Agentic systems add a reasoning loop: the agent decides *when* to retrieve, *what* to search for, *which* tool to use, and *whether* to try a different approach.

### Key capabilities of AI agents

Effective AI agents exhibit six core capabilities:

| Capability | Description |
| --- | --- |
| **Perception, understanding, and memory** | Process multimodal inputs (text, images, structured data), understand context, and maintain state across interactions. |
| **Dynamic task decomposition and planning** | Break complex goals into subtasks, sequence them appropriately, and adapt plans when conditions change. |
| **Contextual retrieval and grounded generation** | Retrieve relevant knowledge from databases, documents, and knowledge graphs to produce accurate, grounded responses. |
| **Tool use and orchestration** | Select and invoke the right tools (databases, APIs, code execution, search engines) based on the task at hand. |
| **Evaluation, feedback, and self-correction** | Assess the quality of outputs, detect errors or hallucinations, and iterate to improve results without human intervention. |
| **Trust, safety, and reliability** | Operate within guardrails, handle sensitive data appropriately, and produce auditable, explainable outputs. |

## Why PostgreSQL and Azure HorizonDB for AI agents

AI agents need more than an LLM, they need persistent infrastructure. PostgreSQL delivers on each of the three pillars that agents require:

### Memory

Agents need continuity across interactions, which means conversation history, user preferences, and task state must persist reliably.

PostgreSQL's SQL and ACID guarantees ensure agents don't operate on stale or corrupted state. Agents use both short-term memory (session context, intermediate reasoning steps) and long-term memory (user preferences, interaction history, learned facts that persist across sessions). Major agent frameworks including [Microsoft Agent Framework](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-python), [LangGraph](https://langchain-ai.github.io/langgraph/concepts/persistence/), and [Mem0](https://docs.mem0.ai/open-source/quickstart#4-postgresql) support PostgreSQL as a memory backend, providing built-in connectors for persisting chat history, agent state, and semantic memory.

### Knowledge retrieval

Agents need access to your business data, such as product catalogs, customer records, and policies, so their responses are grounded in facts, not just the LLM's training data.

PostgreSQL extensions like `pgvector`, Apache AGE, and full-text search bring AI-native retrieval directly into the database engine. This approach means vector search, graph traversal, and keyword matching can all run alongside your operational data in a single system.

Azure HorizonDB builds on this foundation with [vector, full-text, hybrid search, semantic reranking, knowledge graphs, AI functions, and durable AI pipelines](ai-search-overview.md), giving agents multiple retrieval strategies to connect to your business data.

### Scalable multimodal storage

Agents work with diverse data types. PostgreSQL handles JSONB, geospatial data (PostGIS), arrays, full-text search, vector embeddings, and binary data natively, all in a single database. There's no need to manage separate stores for each data type your agents consume.

Additionally, PostgreSQL's open-source ecosystem provides decades of community development, extensive tooling, and [broad framework support](ai-frameworks.md).

HorizonDB adds managed infrastructure, built-in AI functions, AI Model Management, and AI pipelines on top of PostgreSQL. It's purpose-built for AI agent workloads.

## Multi-agent architecture

### Single agent vs. multi-agent

A single agent handles all reasoning, tool use, and retrieval within one orchestration loop, suitable for focused tasks where latency, cost, and debugging simplicity are priorities. Multi-agent architectures distribute work across specialized agents that collaborate on complex problems, useful when the task requires diverse expertise, parallelism, or different security boundaries for different parts of the workflow.

### Orchestration patterns

Multi-agent systems use several common patterns:

| Pattern | Description |
| --- | --- |
| **Supervisor** | A central agent delegates tasks to specialized worker agents, collects results, and synthesizes the final output. |
| **Sequential pipeline** | Agents hand off work in a defined sequence. Each agent's output becomes the next agent's input. |
| **Collaborative** | Agents communicate peer-to-peer, negotiating, and sharing intermediate results without a central coordinator. |

When you build multi-agent systems, Azure HorizonDB can serve as the shared data layer. All agents read from and write to the same database, ensuring consistent state and enabling coordination through shared memory and knowledge.

## Agent standards and protocols

Open standards are emerging to standardize how agents interact with tools and with each other.

### Model Context Protocol (MCP)

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro) is an open standard developed by Anthropic and now governed by the Linux Foundation. MCP defines how AI agents connect to external tools and data sources, acting as the "agent-to-tool" layer.

Key aspects of MCP:

- **Universal tool interface**: Agents discover and invoke tools through a standardized schema, regardless of the underlying implementation.
- **Client-server architecture**: The agent (client) connects to an MCP server, which provides access to tools and data sources.
- **Security**: Built-in support for OAuth 2.1 authentication and managed identity.

Azure HorizonDB provides an [MCP server](foundry-agent-integration.md) that enables Foundry agents to interact with your database through natural language, supporting SQL queries, vector search, schema discovery, and data analysis.

### Agent-to-Agent Protocol (A2A)

[Agent-to-Agent Protocol (A2A)](https://developers.google.com/a2a) is an open standard developed by Google for inter-agent communication. While MCP handles agent-to-tool connectivity, A2A enables agent-to-agent collaboration:

- **Peer-to-peer delegation**: Agents can discover, negotiate with, and delegate tasks to other agents.
- **Agent Cards**: Agents publish their capabilities through standardized metadata, enabling discovery.
- **Cross-vendor interoperability**: Agents built on different platforms can collaborate on shared workflows.

These protocols are complementary: MCP connects agents to tools and data, A2A connects agents to each other. Together, they enable complex multi-agent workflows that span multiple data sources and agent platforms.

## Build AI agents with Azure HorizonDB

To start building AI agents with Azure HorizonDB:

1. **Set up your data layer**: Create an Azure HorizonDB instance and enable the `azure_ai` and `pgvector` extensions. Store your domain data and [generate vector embeddings](generate-vector-embeddings.md).
1. **Choose a retrieval strategy**: Based on your use case, implement [vector search](vector-search-pgvector.md), [hybrid search](hybrid-search.md), or [graph-augmented RAG](graphrag.md) to give your agent access to domain knowledge.
1. **Configure agent memory**: Use your framework's PostgreSQL connector to persist conversation history and agent state in Azure HorizonDB.
1. **Connect your agent**: Use an [orchestration framework](ai-frameworks.md) or the [Foundry MCP integration](foundry-agent-integration.md) to build your agent, connecting it to Azure HorizonDB through native connectors or the [MCP server](foundry-agent-integration.md).
1. **Enrich with AI functions**: Use [AI functions in the azure_ai extension](ai-functions.md) to add extraction, generation, reranking, and embeddings directly in your database queries.
1. **Iterate and scale**: Set up [durable AI pipelines](ai-pipelines.md) to automate data preparation, add [semantic reranking](semantic-reranking.md) to improve retrieval quality, optimize [vector indexing](vector-indexing-diskann.md) for complex domains, and scale to multi-agent architectures as your workload grows.

For industry-specific implementation patterns, see [AI and agentic use cases and sample applications](samples.md).

## Related content

- [Implement Agent Knowledge Retrieval with Azure HorizonDB, Foundry, and MCP](foundry-agent-integration.md)
- [AI and agentic use cases and sample applications](samples.md)
- [What are AI capabilities in Azure HorizonDB](overview.md)
