---
title: AI and Agentic Use Cases and Sample Applications
description: Explore AI and agentic use cases across industries, with solution accelerators and sample applications for Azure HorizonDB.
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
# customer intent: As a user, I want to explore common use cases, design patterns and workflows for AI and agentic app development with Azure HorizonDB.
---

# AI and agentic use cases and sample applications (Preview)

Azure HorizonDB combines relational, vector, graph, and document storage in a single engine, making it a natural foundation for AI-powered applications. Whether you're building semantic search, RAG copilots, multi-agent systems, or intelligent analytics, Azure HorizonDB provides the capabilities you need: vector search with `pgvector` and DiskANN, graph reasoning with Apache AGE, in-database AI functions through the `azure_ai` extension, [AI agent and framework integrations](ai-frameworks.md), [MCP connectivity](foundry-agent-integration.md), and [durable AI pipelines](ai-pipelines.md).

This article is a starting point for exploring what you can build. Each use case highlights the problem, how an AI application or agent solves it, and which Azure HorizonDB features power the solution.

For a comprehensive hub of app development resources, tutorials, and community content for PostgreSQL on Azure, visit the [PostgreSQL Hub for Azure Developers](https://aka.ms/postgres-hub).

## Quick reference

| Industry | Use case | Key capabilities |
| --- | --- | --- |
| **Financial services** | [AI copilot for financial research](#ai-copilot-for-financial-research) | Hybrid search, semantic reranking, AI pipelines |
| | [Fraud detection & compliance](#fraud-detection-and-compliance) | Knowledge graph, AI functions in SQL, real-time scoring |
| **Retail & e-commerce** | [Personalized shopping (AgenticShop)](#personalized-shopping-agenticshop) | Vector search, semantic reranking, multi-agent |
| | [Returns & cancellations analysis](#returns-and-cancellations-analysis) | Sentiment analysis, semantic reranking, AI pipelines |
| **SaaS** | [Support ops commander](#support-ops-commander) | Vector search, semantic reranking, AI agents |
| | [Customer churn prediction](#customer-churn-prediction) | Vector search, AI pipelines, AI functions in SQL |
| **Travel & hospitality** | [Multi-agent trip planner](#multi-agent-trip-planner) | Multi-agent, PostGIS, knowledge graph |
| **Legal** | [Legal research with GraphRAG](#legal-research-with-graphrag) | GraphRAG, knowledge graph, hybrid search, semantic reranking |
| **HR & people** | [Skills & expertise mapper](#skills-and-expertise-mapper) | Knowledge graph, vector search |
| **Developer tools** | [Database development agent](#database-development-agent) | AI agents, AI functions in SQL |

## Use cases

### AI copilot for financial research

Financial analysts need fast, accurate answers grounded in earnings reports, SEC filings, and market data, not LLM hallucinations. A RAG copilot retrieves the most relevant passages from your financial document corpus using hybrid search, reranks them for precision, and generates grounded answers with citations.

> [!TIP]  
> The [Build your own AI copilot](https://aka.ms/pg-byoac-docs) solution accelerator provides an end-to-end guide for building this pattern with Azure HorizonDB and Azure AI Services.

**Build with Azure HorizonDB:**

1. Store financial documents (earnings reports, SEC filings, analyst notes) in Azure HorizonDB with chunked text and `pgvector` embeddings indexed with DiskANN for submillisecond similarity search across millions of passages.
1. Create a full-text search index with `pg_fts` over financial terms, tickers, and entity names for precise keyword matching.
1. Use the `azure_ai` extension to generate embeddings and chat completions directly from SQL - no external orchestration needed.
1. Combine vector search and BM25 full-text search with Reciprocal Rank Fusion for hybrid retrieval, then apply `azure_ai.rank()` to rerank the top candidates for precision.
1. Build a conversational interface that retrieves context, generates grounded answers, and cites the source passages with document IDs and page numbers.

### Fraud detection and compliance

Financial services companies process millions of transactions daily. Manual review doesn't scale, and batch processing lets fraudulent transactions slip through. An agent can evaluate each transaction in real time against rule-based checks and ML models, flag anomalies, enforce KYC, and AML compliance, and maintain the auditable trail that regulators require.

**Build with Azure HorizonDB:**

1. Write transactions to partitioned Azure HorizonDB tables with row-level security enabled.
1. Use Apache AGE to model transaction networks as a graph and detect ring fraud patterns through relationship traversal.
1. Use the `azure_ai` extension to call Azure Machine Learning models for real-time fraud scoring directly from SQL.
1. Build an agent with tools for rule evaluation, graph-based anomaly detection, and compliance checks.
1. Use PostgreSQL triggers to route flagged transactions to a `fraud_alerts` table with confidence scores.
1. Enable `pg_audit` for a complete compliance trail and connect escalation to your risk team's workflow.

### Personalized shopping (AgenticShop)

Traditional search fails when a customer says "a lightweight jacket for hiking in the rain." An agent can understand intent using vector similarity, filter by availability and purchase history, and present ranked recommendations that improve with every interaction.

> [!TIP]  
> Try the [AgenticShop](https://aka.ms/agentic-shop) solution accelerator: a multi-agent e-commerce demo powered by LlamaIndex with observability and memory persistence.

**Build with Azure HorizonDB:**

1. Store product catalogs with `pgvector` embeddings indexed using DiskANN for submillisecond similarity search across millions of products.
1. Use `azure_ai.rank()` to rank results by relevance to the customer's natural-language query.
1. Use the `azure_ai` extension to generate product embeddings and enrich catalog metadata with Azure OpenAI.
1. Build an agent with tools for vector search, keyword matching, and customer history lookup.
1. Log every interaction in a `customer_sessions` table so the agent personalizes over time.
1. Connect the agent to your storefront via API for real-time conversational shopping.

### Returns and cancellations analysis

When return rates climb, the data to explain why exists across order details, reviews, shipping logs, and pricing changes. But connecting those signals manually is slow. An agent can investigate patterns automatically, correlate them with upstream signals, and produce weekly insight reports with root causes and recommendations.

**Build with Azure HorizonDB:**

1. Store returns, cancellations, reviews, and order details in Azure HorizonDB with JSONB metadata.
1. Use the `azure_ai` extension to run sentiment analysis on reviews and extract themes using Azure OpenAI.
1. Use `azure_ai.rank()` to correlate review text with return reasons.
1. Build an agent with tools for cluster detection (by product, region, time window) and signal correlation.
1. Schedule the agent weekly via `pg_cron` to produce insight reports.
1. Route reports to product and operations teams for action.

### Support ops commander

Support teams struggle with inconsistent triage when tickets arrive from multiple channels and priority depends on context scattered across systems. An agent can classify each ticket using semantic similarity, correlate it with known incidents, draft a consistent response, and escalate emerging patterns before more customers are affected.

**Build with Azure HorizonDB:**

1. Store tickets in Azure HorizonDB with JSONB metadata and `pgvector` embeddings indexed with DiskANN for fast semantic search at scale.
1. Use `azure_ai.rank()` to rank similar tickets and surface the most relevant matches for correlation.
1. Use the `azure_ai` extension to generate embeddings and draft response summaries directly from SQL.
1. Build an agent with tools for ticket classification, incident correlation, and response drafting.
1. Use PostgreSQL triggers to alert when SLA thresholds are approaching.
1. Configure escalation rules so the agent flags clusters of similar tickets automatically.

### Customer churn prediction

SaaS companies often learn a customer is leaving only after they cancel. The warning signs were there earlier, in usage logs, support tickets, and billing patterns, but no one connected the dots in time. An agent can score every active account on a schedule, flag declining engagement, and recommend specific retention actions before it's too late.

**Build with Azure HorizonDB:**

1. Consolidate usage metrics, support tickets, and billing events in Azure HorizonDB.
1. Use the `azure_ai` extension to generate behavioral embeddings for each account using Azure OpenAI.
1. Use `pg_cron` to trigger scheduled scoring jobs with window functions and `pgvector` similarity (DiskANN indexed).
1. Build an agent with tools that score accounts, write predictions to a `churn_scores` table, and recommend retention actions.
1. Connect the output to your CRM so the customer success team can act immediately.

### Multi-agent trip planner

Planning a trip means juggling flights, hotels, restaurants, budgets, and personal preferences all at once. Multiple specialized agents collaborate through shared Azure HorizonDB tables, each owning one domain of the problem, to produce a complete personalized trip plan.

*Example prompt: "Plan a 5-day trip to Tokyo for two foodies on a $3,000 budget."*

| Agent | Role | Shared table |
| --- | --- | --- |
| **Research agent** | Finds flights, hotels, and attractions. Stores candidates with cost and fit scores. | `travel_options` |
| **Budget agent** | Tracks totals, flags overruns, suggests alternatives. | `trip_budget` |
| **Itinerary agent** | Builds a day-by-day plan accounting for timing and travel distances. | `itinerary` |
| **Personalization agent** | Steers recommendations using diet, mobility, and past trip history. | `user_preferences` |

**Build with Azure HorizonDB:**

1. Create shared state tables in Azure HorizonDB with JSONB for flexible option storage and PostGIS for location-aware planning.
1. Use the `azure_ai` extension to generate embeddings for travel options and match them against user preferences.
1. Enable DiskANN indexing on `pgvector` columns for fast preference matching across large option sets.
1. Model location connectivity and route relationships using Apache AGE for graph-based itinerary planning.
1. Build each agent with its own tool set (search APIs, budget calculators, scheduling logic, graph queries).
1. Point all agents at the same Azure HorizonDB instance so they coordinate through shared tables - one agent writes its findings, the next picks up exactly where the first left off.
1. Orchestrate the agents in sequence or parallel using a multi-agent framework.

### Legal research with GraphRAG

Legal research requires traversing complex relationships between cases, statutes, and precedents, not just keyword matching. GraphRAG combines vector search over case text with graph traversal over citation networks, so a research assistant can find relevant precedents, trace how rulings build on each other, and synthesize answers that cite the full chain of reasoning.

> [!TIP]  
> Try the [GraphRAG Legal Research Copilot](https://github.com/Azure-Samples/graphrag-legalcases-postgres): an end-to-end sample with U.S. Case Law (500K cases), vector search, semantic ranking, AGE graph, and RRF fusion.

**Build with Azure HorizonDB:**

1. Store case law documents with `pgvector` embeddings indexed using DiskANN for fast semantic search across hundreds of thousands of cases.
1. Model case citation networks using the Apache AGE extension (cases as nodes, citations as edges) so agents can traverse precedent chains and find indirect relationships.
1. Use the `azure_ai` extension to generate embeddings for case text and produce natural-language summaries of retrieved precedent chains.
1. Combine vector similarity search with graph traversal in a single query to find cases that are both semantically relevant and legally connected.
1. Apply hybrid search with RRF and semantic reranking for the highest-quality retrieval in the final results.

### Skills and expertise mapper

Organizations struggle to answer "Who has experience with payment systems and PostgreSQL?" when employee skills are scattered across résumés, project records, and HR systems. An agent maps skills, project history, and team relationships into a knowledge graph, then answers hiring and gap analysis questions in seconds.

**Build with Azure HorizonDB:**

1. Enable the Apache AGE extension and model employee-skill-project relationships as a property graph. Employees, skills, projects, and teams become nodes; proficiency levels and assignments become edges.
1. Use the `azure_ai` extension to generate skill embeddings from résumés and project descriptions using Azure OpenAI.
1. Index skill embeddings with DiskANN for fast similarity matching across large workforces to find people with *similar* skills, not just exact keyword matches.
1. Build an agent with tools for graph traversal queries (AGE) and semantic skill matching (`pgvector`) so it can answer questions like "Find engineers who have worked on payment systems and speak Japanese."
1. Ingest employee profiles, project assignments, and skill assessments into the graph on a recurring basis.
1. Expose the agent to hiring managers and leadership for talent search, team composition, and gap analysis.

### Database development agent

Development teams spend too much time on database plumbing: provisioning instances, designing schemas by hand, onboarding new members to unfamiliar databases, and chasing down slow queries after the fact. An agent can handle the full lifecycle from a single conversation. You describe your workload, and it provisions an Azure HorizonDB instance, designs your schema, ships migration scripts, onboards your team, tunes performance, and audits security continuously.

| Capability | Description |
| --- | --- |
| **Provision** | Creates an Azure HorizonDB instance with the right SKU, region, networking, and extensions. No portal selects required. |
| **Design and ship** | Converts a feature request into schema design, migration scripts, API endpoints, test data, and validation. |
| **Clone and stage** | Mirrors production into a safe staging environment with realistic synthetic data and performance checks. |
| **Onboard** | Reads an unfamiliar database and explains key tables, relationships, query patterns, and red flags. |
| **Optimize** | Identifies the biggest bottlenecks and recommends specific query, index, and configuration changes. |
| **Secure** | Audits for security risks, personal data (PII) exposure, and over-permissioned roles. Can lock down critical gaps automatically. |

**Build with Azure HorizonDB:**

1. Deploy Azure HorizonDB with MCP enabled for natural-language database interaction.
1. Create an agent with tools for Azure Resource Manager, PostgreSQL MCP, and system catalog access.
1. Define tool functions for schema introspection, DDL generation, `EXPLAIN ANALYZE`, and security audit queries.
1. Use the `azure_ai` extension to generate documentation and onboarding summaries directly from schema metadata.
1. Connect the agent to your Azure HorizonDB instance so it can provision, design, monitor, and secure in a loop.

## Solution accelerators and samples

Get started quickly with these end-to-end solution accelerators and sample applications:

| Solution | Description | Link |
| --- | --- | --- |
| **Build your own AI copilot (Financial Services)** | End-to-end guide for building RAG-based copilots with Azure HorizonDB and Azure AI Services. Covers ingestion, embeddings, retrieval, and generation. | [Documentation](https://aka.ms/pg-byoac-docs) |
| **Chat with your Data** | Conversational search experience combining Azure AI Search and Azure OpenAI with natural language and speech-to-text. Deployable in your Azure subscription. | [GitHub repo](https://aka.ms/pg-cwyd-repo) |
| **GraphRAG Legal Research Copilot** | Graph-augmented RAG with U.S. Case Law (500K cases). Includes vector search, semantic ranking, AGE graph, and RRF fusion. | [GitHub repo](https://github.com/Azure-Samples/graphrag-legalcases-postgres) |
| **GraphRAG + Docker + AI Agents** | Containerized GraphRAG deployment with AI agent integration for automated graph construction and retrieval. | [GitHub repo](https://github.com/Azure-Samples/postgreSQL-graphRAG-docker) |
| **AgenticShop** | Multi-agent e-commerce demo powered by LlamaIndex. Showcases personalized product discovery using unstructured data, with observability and memory persistence. | [Documentation](https://aka.ms/agentic-shop) |

> [!TIP]  
> Visit the [PostgreSQL Hub for Azure Developers](https://aka.ms/postgres-hub) for more tutorials, samples, community content, and everything app development with PostgreSQL on Azure.

## Related content

- [What are AI capabilities in Azure HorizonDB](overview.md)
- [Build AI agents with Azure HorizonDB](ai-agents.md)
- [Build a semantic search application](build-semantic-search-app.md)
