---
title: Overview of AI capabilities in Azure HorizonDB
description: Learn about the AI capabilities in Azure HorizonDB, including AI functions, pipelines, vector search, semantic reranking, knowledge graphs, and agent integrations.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: ai-generative
ms.topic: overview
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
# customer intent: As a user, I want to understand the full set of AI capabilities in Azure HorizonDB so I can choose the right features for building AI applications and agents.
---

# What are AI capabilities in Azure HorizonDB

Generative AI is transforming how applications interact with data. As organizations move beyond basic chatbots toward retrieval-augmented generation (RAG), autonomous agents, and intelligent search, one thing is clear: **data is the foundation of intelligence**. Raw data becomes knowledge when it's structured, embedded, and made searchable, and knowledge becomes intelligence when AI models can reason over it, retrieve what's relevant, and take action.

Azure HorizonDB brings this full stack into PostgreSQL. Instead of stitching together separate services for embeddings, vector search, reranking, and orchestration, you get a single database that handles your operational data and your AI workloads together, with SQL as the interface.

## Key concepts

If you're new to generative AI, this section introduces the core concepts that underpin AI applications and agents. Each concept builds on the previous one.

### Large language models (LLMs)

A large language model (LLM) is an AI model trained on massive amounts of text data to understand and generate human-like language. LLMs use deep learning architectures (primarily transformers) with billions or trillions of parameters that capture complex patterns in language. Models like GPT-4o, GPT-5, and open-source alternatives (Llama, Mistral) can perform a wide range of tasks: text generation, summarization, translation, code generation, question answering, and more.

LLMs are powerful but have a key limitation: they only know what was in their training data. They can't access your private business data, and their knowledge has a cutoff date. This limitation is what makes the next concept, RAG, essential.

To learn more, see [Large language models](/azure/foundry/concepts/large-language-models).

### Retrieval-augmented generation (RAG)

Retrieval-augmented generation (RAG) is a pattern that addresses the limitation of LLMs by grounding their responses in your actual data. Instead of relying solely on what the model learned during training, a RAG system retrieves relevant documents from a data source and passes them as context to the LLM before it generates a response.

A typical RAG flow has three steps:

1. **Retrieve**: Search your data (using vector search, keyword search, or hybrid techniques) to find content relevant to the user's query.
1. **Augment**: Include the retrieved content in the prompt sent to the LLM, providing factual context the model wouldn't otherwise have.
1. **Generate**: The LLM produces a response grounded in the retrieved information, reducing hallucination and improving accuracy.

RAG is the foundation of most production AI applications, from customer-facing Q&A systems to internal knowledge assistants. The quality of a RAG system depends heavily on how well your data is prepared, embedded, indexed, and searched.

To learn more, see [Retrieval-augmented generation (RAG)](/azure/foundry/concepts/retrieval-augmented-generation).

### AI agents

AI agents go beyond RAG by adding a reasoning loop. Where a RAG application follows a fixed retrieve-then-generate pipeline, an agent uses an LLM to *plan*, *decide* which tools to call, *retrieve* information, *evaluate* results, and *self-correct*, autonomously completing multi-step tasks without human intervention. Agents combine a model, instructions, tools, and persistent memory to operate across sessions and workflows. Because agents need durable storage, access to knowledge, and scalable infrastructure, the choice of database is critical to their design.

To learn more, see [What are AI agents?](ai-agents.md#what-are-ai-agents).

### Embeddings, vectors, and vector search

A **vector** is a mathematical object: an ordered array of numbers that represents a point in multidimensional space. In AI, vectors are used to encode the meaning of content (text, images, records) so that machines can compare, search, and reason over it numerically.

An **embedding** is a specific type of vector produced by a machine learning model, where semantically similar content maps to nearby points in vector space. For example, the phrases "lightweight laptop for travel" and "ultraportable notebook under 1 kg" produce embeddings that are geometrically close together, even though they share no words. **Embedding models** such as `text-embedding-3-small` or `text-embedding-ada-002` are the AI models that perform this conversion, taking raw text (or other content) as input and outputting a dense vector of floating-point numbers.

The proximity between vectors is measured using **vector similarity** functions like cosine similarity, inner product, or Euclidean distance. **Vector search** uses this property to find content by meaning rather than keywords. At query time, the user's question is converted into a vector using the same embedding model, and the database finds the stored vectors closest to the query vector, returning the most semantically relevant results. Vector search is the core retrieval mechanism behind RAG. When combined with keyword search and other techniques like semantic reranking, it forms a comprehensive retrieval strategy. For a detailed look at all available retrieval techniques, see [Retrieval foundations: vector, full-text, and hybrid search in Azure HorizonDB](ai-search-overview.md).

To see an interactive visualization of how vector similarity works, see [Vectors comparison](https://pamelafox.github.io/vectors-comparison/).

## The role of databases in AI

Every AI pattern, be it RAG, agents, or fine-tuning, starts with data. But the relationship between AI and databases goes deeper than simple storage. As AI applications move from prototypes to production, the database becomes the critical infrastructure layer that determines scalability, reliability, and data freshness.

- **Data is the source of knowledge.** LLMs are only as good as the context they receive. Your business data (product catalogs, support tickets, policy documents, customer records, etc.) needs to be chunked, embedded, indexed, and kept in sync. The database orchestrates this entire data-to-knowledge pipeline.
- **Persistent memory for stateful applications.** Chatbots and agents need to remember conversation history, user preferences, and task progress across sessions. Without durable, transactional storage, every interaction starts from zero.
- **Unified multi-modal storage.** AI workloads involve relational records, JSON documents, vector embeddings, graph relationships, and geospatial data. Managing these across separate specialized systems introduces synchronization complexity, consistency risks, and operational overhead. A database that handles all of these natively eliminate that fragmentation.
- **Production-grade reliability.** Prototype AI apps can use in-memory stores or flat files. Production systems need ACID transactions, point-in-time recovery, high availability, and security. Mature database systems provide these capabilities out of the box.

PostgreSQL is uniquely suited for AI workloads because it handles relational data, JSON, vectors, graphs, and full-text search in a single transactional system backed by decades of ecosystem maturity, extensibility, and broad framework support. Azure HorizonDB builds on PostgreSQL with managed infrastructure, built-in AI functions, model management, and durable pipelines purpose-built for AI workloads. For a deeper dive, see [Why PostgreSQL and Azure HorizonDB for AI agents](ai-agents.md#why-postgresql-and-azure-horizondb-for-ai-agents).

## AI capabilities in Azure HorizonDB

:::image type="content" source="media/overview/ai-capabilities-overview.png" alt-text="Diagram showing AI capabilities in Azure HorizonDB organized as a top-down flow: Build AI agents and apps, AI functions in SQL, Data preparation and pipelines, Search and retrieval with subsections for improving performance and enhancing relevance, all on the Azure HorizonDB PostgreSQL foundation." lightbox="media/overview/ai-capabilities-overview.png" :::

### AI functions in SQL

Call AI models directly from SQL queries with no application code required.

- **[AI functions in the azure_ai extension](ai-functions.md)**: Generate text, extract entities, evaluate statements, create embeddings, and rerank results using functions like `azure_ai.generate()`, `azure_ai.extract()`, `azure_ai.rank()`, and `azure_openai.create_embeddings()`.
- **[AI Model Management in Azure HorizonDB](ai-model-management.md)**: One-select provisioning of embedding, chat, and reranking models. Models are automatically registered, configured, and kept up to date. You don't need to manage endpoints or keys.

### Data preparation and pipelines

Prepare your data for AI retrieval with automated, fault-tolerant workflows.

- **[Prepare data for AI app and agent development in Azure HorizonDB](ai-data-preparation.md)**: Strategies for chunking, formatting, and structuring your data for effective embedding and retrieval.
- **[Implement durable AI pipelines in Azure HorizonDB](ai-pipelines.md)**: Declare multi-step AI workflows (chunk → embed → index → search → rerank) as durable pipelines that run inside the database with automatic retries, checkpointing, and crash recovery.
- **[Generate vector embeddings using the create_embeddings() AI function](generate-vector-embeddings.md)**: Create embeddings directly in SQL using `azure_openai.create_embeddings()`, with support for batch processing and multiple models.

### Search and retrieval

Find the right information using multiple retrieval strategies, individually or combined.

- **[Implement vector search in Azure HorizonDB using the pgvector extension](vector-search-pgvector.md)**: Semantic similarity search using vector embeddings.
- **[Full-text search with pg_fts in Azure HorizonDB](full-text-search-pgfts.md)**: BM25 keyword matching for exact terms and identifiers.
- **[Hybrid search in Azure HorizonDB](hybrid-search.md)**: Combine vector and full-text search with Reciprocal Rank Fusion for best overall coverage.

#### Improve search performance

As your dataset grows, indexing strategies become critical for maintaining fast query response times.

- **[Scalable vector indexing with DiskANN](vector-indexing-diskann.md)**: Microsoft Research's graph-based algorithm, recommended for large, growing datasets with high dimensions and filtered queries.
- **[Optimize performance when using pgvector in Azure HorizonDB](optimize-pgvector-performance.md)**: Tuning HNSW and IVFFlat indexes for your workload.
- **[Choose the right vector index for your workload in Azure HorizonDB](vector-index-selection-guide.md)**: Choose the right index type based on dataset size, query patterns, and recall requirements.

#### Enhance search relevance

Retrieval is only the first step. Enhance accuracy and depth with second-stage scoring and structured knowledge.

- **[Semantic reranking with the rank() function](semantic-reranking.md)**: Cross-encoder rescoring that reorders initial search results by true relevance to the query.
- **[Graph-augmented RAG patterns with Azure HorizonDB](graphrag.md)**: Entity relationship traversal with Apache AGE for multi-hop reasoning across connected data. See also [Tutorial: Build a knowledge graph from unstructured text using AI Functions and Apache AGE](build-knowledge-graph.md).

### Build AI agents and apps

Connect Azure HorizonDB to agent frameworks, orchestration services, and tools.

- **[Build AI agents with Azure HorizonDB](ai-agents.md)**: Conceptual guide covering agent memory, knowledge retrieval, multi-agent architecture, standards (MCP, A2A), and orchestration frameworks.
- **[Implement Agent Knowledge Retrieval with Azure HorizonDB, Foundry and MCP](foundry-agent-integration.md)**: Implementation guide for connecting Foundry agents to your database through the MCP server.
- **[Build AI apps and agents with orchestration frameworks](ai-frameworks.md)**: Native connectors for Microsoft Agent Framework, LangGraph/LangChain, LlamaIndex, CrewAI, Auto-Gen, and more.
- **[Develop AI apps with LangChain and Azure HorizonDB](develop-with-langchain.md)**: Step-by-step guide for using LangChain with Azure HorizonDB.

### Samples and tutorials

- **[AI and agentic use cases and sample applications](samples.md)**: Industry-specific patterns and end-to-end implementations.
- **[Tutorial: Build a semantic search application with Azure HorizonDB](build-semantic-search-app.md)**: Tutorial for building a complete semantic search app with Azure HorizonDB.

## Get started

Azure HorizonDB gives you a single platform to go from raw data to production AI: embedding generation, vector and hybrid search, semantic reranking, knowledge graphs, durable pipelines, and agent integration, all within PostgreSQL and all accessible through SQL. Whether you're building your first RAG application or deploying multi-agent systems at scale, the capabilities described in this article work together as a complete, integrated stack. Explore the linked articles to dive deeper into each capability.

To go further, visit the [PostgreSQL Hub for Azure Developers](https://aka.ms/postgres-hub): a one-stop shop for curated code samples, solution accelerators, tutorials, structured learning pathways, and a growing developer community where you can connect with Microsoft and ecosystem experts.

## Related content

- [AI functions in the azure_ai extension](ai-functions.md)
- [Generate vector embeddings using the create_embeddings() AI function](generate-vector-embeddings.md)
- [Implement vector search in Azure HorizonDB using the pgvector extension](vector-search-pgvector.md)
- [Retrieval foundations: vector, full-text, and hybrid search in Azure HorizonDB](ai-search-overview.md)
- [Implement durable AI pipelines in Azure HorizonDB](ai-pipelines.md)
- [Build AI agents with Azure HorizonDB](ai-agents.md)
- [AI and agentic use cases and sample applications](samples.md)
