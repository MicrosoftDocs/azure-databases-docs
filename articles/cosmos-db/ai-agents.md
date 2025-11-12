---
title: AI Agents and Solutions
titleSuffix: Azure Cosmos DB
description: Learn about key concepts for agents and step through the implementation of an AI agent memory system.
author: wmwxwa
ms.author: wangwilliam
ms.service: azure-cosmos-db
ms.custom:
  - ignite-2024
  - sfi-ropc-blocked
ms.topic: concept-article
ms.date: 10/20/2025
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
---

# AI agents in Azure Cosmos DB

AI agents are designed to perform specific tasks, answer questions, and automate processes for users. These agents vary widely in complexity. They range from simple chatbots, to copilots, to advanced AI assistants in the form of digital or robotic systems that can run complex workflows autonomously.

This article provides conceptual overviews and detailed implementation samples for AI agents.

## What are AI agents?

Unlike standalone large language models (LLMs) or rule-based software/hardware systems, AI agents have these common features:

- **Planning**: AI agents can plan and sequence actions to achieve specific goals. The integration of LLMs has revolutionized their planning capabilities.
- **Tool usage**: Advanced AI agents can use various tools, such as code execution, search, and computation capabilities, to perform tasks effectively. AI agents often use tools through function calling.
- **Perception**: AI agents can perceive and process information from their environment, to make them more interactive and context aware. This information includes visual, auditory, and other sensory data.
- **Memory**: AI agents have the ability to remember past interactions (tool usage and perception) and behaviors (tool usage and planning). They store these experiences and even perform self-reflection to inform future actions. This memory component allows for continuity and improvement in agent performance over time.

> [!NOTE]
> The usage of the term *memory* in the context of AI agents is different from the concept of computer memory (like volatile, nonvolatile, and persistent memory).

### Copilots

Copilots are a type of AI agent. They work alongside users rather than operating independently. Unlike fully automated agents, copilots provide suggestions and recommendations to assist users in completing tasks.

For instance, when a user is writing an email, a copilot might suggest phrases, sentences, or paragraphs. The user might also ask the copilot to find relevant information in other emails or files to support the suggestion (see [retrieval-augmented generation](vector-database.md#retrieval-augmented-generation)). The user can accept, reject, or edit the suggested passages.

### Autonomous agents

Autonomous agents can operate more independently. When you set up autonomous agents to assist with email composition, you could enable them to perform the following tasks:

- Consult existing emails, chats, files, and other internal and public information that's related to the subject matter.
- Perform qualitative or quantitative analysis on the collected information, and draw conclusions that are relevant to the email.
- Write the complete email based on the conclusions, and incorporate supporting evidence.
- Attach relevant files to the email.
- Review the email to ensure that all the incorporated information is factually accurate and that the assertions are valid.
- Select the appropriate recipients for **To**, **Cc**, and **Bcc** fields, and look up their email addresses.
- Schedule an appropriate time to send the email.
- Perform follow-ups if responses are expected but not received.

You can configure the agents to perform each of the preceding tasks with or without human approval.

### Multi-agent systems

A popular strategy for achieving performant autonomous agents is the use of multi-agent systems. In multi-agent systems, multiple autonomous agents, whether in digital or robotic form, interact or work together to achieve individual or collective goals. Agents in the system can operate independently and possess their own knowledge or information. Each agent might also have the capability to perceive its environment, make decisions, and execute actions based on its objectives.

Multi-agent systems have these key characteristics:

- **Autonomous**: Each agent functions independently. It makes its own decisions without direct human intervention or control by other agents.
- **Interactive**: Agents communicate and collaborate with each other to share information, negotiate, and coordinate their actions. This interaction can occur through various protocols and communication channels.
- **Goal-oriented**: Agents in a multi-agent system are designed to achieve specific goals, which can be aligned with individual objectives or a shared objective among the agents.
- **Distributed**: Multi-agent systems operate in a distributed manner, with no single point of control. This distribution enhances the system's robustness, scalability, and resource efficiency.

A multi-agent system provides the following advantages over a copilot or a single instance of LLM inference:

- **Dynamic reasoning**: Compared to chain-of-thought or tree-of-thought prompting, multi-agent systems allow for dynamic navigation through various reasoning paths.
- **Sophisticated abilities**: Multi-agent systems can handle complex or large-scale problems by conducting thorough decision-making processes and distributing tasks among multiple agents.
- **Enhanced memory**: Multi-agent systems with memory can overcome the context windows of LLMs to enable better understanding and information retention.

## Implementation of AI agents

### Reasoning and planning

Complex reasoning and planning are the hallmark of advanced autonomous agents. Popular frameworks for autonomous agents incorporate one or more of the following methodologies (with links to arXiv archive pages) for reasoning and planning:

- [Self-ask](https://arxiv.org/abs/2210.03350)

  Improve on chain of thought by having the model explicitly ask itself (and answer) follow-up questions before answering the initial question.

- [Reason and act (ReAct)](https://arxiv.org/abs/2210.03629)

  Use LLMs to generate both reasoning traces and task-specific actions in an interleaved manner. Reasoning traces help the model induce, track, and update action plans, along with handling exceptions. Actions allow the model to connect with external sources, such as knowledge bases or environments, to gather additional information.

- [Plan and solve](https://arxiv.org/abs/2305.04091)

  Devise a plan to divide the entire task into smaller subtasks, and then carry out the subtasks according to the plan. This approach mitigates the calculation errors, missing-step errors, and semantic misunderstanding errors that are often present in zero-shot chain-of-thought prompting.

- [Reflect/self-critique](https://arxiv.org/abs/2303.11366)

  Use *reflexion* agents that verbally reflect on task feedback signals. These agents maintain their own reflective text in an episodic memory buffer to induce better decision-making in subsequent trials.

### Frameworks

Various frameworks and tools can facilitate the development and deployment of AI agents.

For tool usage and perception that don't require sophisticated planning and memory, some popular LLM orchestrator frameworks are LangChain, LlamaIndex, Prompt Flow, and Semantic Kernel.

For advanced and autonomous planning and execution workflows, [AutoGen](https://microsoft.github.io/autogen/) propelled the multi-agent wave that began in late 2022. OpenAI's [Responses API](https://platform.openai.com/docs/api-reference/responses) allows its users to create agents natively within the GPT ecosystem. [LangChain Agents](https://python.langchain.com/docs/how_to/#agents) and [LlamaIndex Agents](https://docs.llamaindex.ai/en/stable/use_cases/agents/) also emerged around the same time.

### AI agent memory system

The prevalent practice for experimenting with AI-enhanced applications from 2022 through 2025 has been using standalone database management systems for various data workflows or types. For example, you can use an in-memory database for caching, a relational database for operational data (including tracing/activity logs and LLM conversation history), and a [pure vector database](vector-database.md#integrated-vector-database-vs-pure-vector-database) for embedding management.

However, this practice of using a complex web of standalone databases can hurt an AI agent's performance. Integrating all these disparate databases into a cohesive, interoperable, and resilient memory system for AI agents is its own challenge.

Also, many of the frequently used database services aren't optimal for the speed and scalability that AI agent systems need. These databases' individual weaknesses are exacerbated in multi-agent systems.

#### In-memory databases

In-memory databases are excellent for speed but might struggle with the large-scale data persistence that AI agents need.

#### Relational databases

Relational databases aren't ideal for the varied modalities and fluid schemas of data that agents handle. Relational databases require manual efforts and even downtime to manage provisioning, partitioning, and sharding.

#### Pure vector databases

Pure vector databases tend to be less effective for transactional operations, real-time updates, and distributed workloads. The popular pure vector databases nowadays typically offer:

- No guarantee on reads and writes.
- Limited ingestion throughput.
- Low availability (below 99.9%, or an annualized outage of 9 hours or more).
- One consistency level (eventual).
- A resource-intensive in-memory vector index.
- Limited options for multitenancy.
- Limited security.

## Characteristics of a robust AI agent memory system

Just as efficient database management systems are critical to the performance of software applications, it's critical to provide LLM-powered agents with relevant and useful information to guide their inference. Robust memory systems enable organizing and storing various kinds of information that the agents can retrieve at inference time.

Currently, LLM-powered applications often use [retrieval-augmented generation](vector-database.md#retrieval-augmented-generation) that uses basic semantic search or vector search to retrieve passages or documents. [Vector search](vector-database.md#vector-search) can be useful for finding general information. But vector search might not capture the specific context, structure, or relationships that are relevant for a particular task or domain.

For example, if the task is to write code, vector search might not be able to retrieve the syntax tree, file system layout, code summaries, or API signatures that are important for generating coherent and correct code. Similarly, if the task is to work with tabular data, vector search might not be able to retrieve the schema, the foreign keys, the stored procedures, or the reports that are useful for querying or analyzing the data.

Weaving together a web of standalone in-memory, relational, and vector databases (as described [earlier](#ai-agent-memory-system)) isn't an optimal solution for the varied data types. This approach might work for prototypical agent systems. However, it adds complexity and performance bottlenecks that can hamper the performance of advanced autonomous agents.

A robust memory system should have the following characteristics.

### Multimodal

AI agent memory systems should provide collections that store metadata, relationships, entities, summaries, or other types of information that can be useful for various tasks and domains. These collections can be based on the structure and format of the data, such as documents, tables, or code. Or they can be based on the content and meaning of the data, such as concepts, associations, or procedural steps.

Memory systems aren't just critical to AI agents. They're also important for the humans who develop, maintain, and use these agents.

For example, humans might need to supervise agents' planning and execution workflows in near real time. While supervising, humans might interject with guidance or make in-line edits of agents' dialogues or monologues. Humans might also need to audit the reasoning and actions of agents to verify the validity of the final output.

Human/agent interactions are likely in natural or programming languages, whereas agents "think," "learn," and "remember" through embeddings. This difference poses another requirement on memory systems' consistency across data modalities.

### Operational

Memory systems should provide memory banks that store information that's relevant for the interaction with the user and the environment. Such information might include chat history, user preferences, sensory data, decisions made, facts learned, or other operational data that's updated with high frequency and at high volumes.

These memory banks can help the agents remember short-term and long-term information, avoid repeating or contradicting themselves, and maintain task coherence. These requirements must hold true even if the agents perform a multitude of unrelated tasks in succession. In advanced cases, agents might also test numerous branch plans that diverge or converge at different points.

### Shareable but also separable

At the macro level, memory systems should enable multiple AI agents to collaborate on a problem or process different aspects of the problem by providing shared memory that's accessible to all the agents. Shared memory can facilitate the exchange of information and the coordination of actions among the agents.

At the same time, the memory system must allow agents to preserve their own persona and characteristics, such as their unique collections of prompts and memories.

## Building a robust AI agent memory system

The preceding characteristics require AI agent memory systems to be highly scalable and swift. Painstakingly weaving together disparate in-memory, relational, and vector databases (as described [earlier](#ai-agent-memory-system)) might work for early-stage AI-enabled applications. However, this approach adds complexity and performance bottlenecks that can hamper the performance of advanced autonomous agents.

In place of all the standalone databases, Azure Cosmos DB can serve as a unified solution for AI agent memory systems. Its robustness successfully [enabled OpenAI's ChatGPT service](https://www.youtube.com/watch?v=6IIUtEFKJec&t) to scale dynamically with high reliability and low maintenance. Powered by an atom-record-sequence engine, it's the world's first globally distributed [NoSQL](distributed-nosql.md), [relational](distributed-relational.md), and [vector database](vector-database.md) service that offers a serverless mode. AI agents built on top of Azure Cosmos DB offer speed, scale, and simplicity.

### Speed

Azure Cosmos DB provides single-digit millisecond latency. This capability makes it suitable for processes that require rapid data access and management. These processes include caching (both traditional and semantic caching), transactions, and operational workloads.

Low latency is crucial for AI agents that need to perform complex reasoning, make real-time decisions, and provide immediate responses. In addition, the service's [use of the DiskANN algorithm](nosql/vector-search.md#enable-the-vector-indexing-and-search-feature) provides accurate and fast vector search with minimal memory consumption.

### Scale

Azure Cosmos DB is engineered for global distribution and horizontal scalability, with support for multi-region input-output and multitenancy.

The service helps ensure that memory systems can expand seamlessly and keep up with rapidly growing agents and associated data. The [availability guarantee in its service-level agreement (SLA)](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services) translates to less than 5 minutes of downtime per year. Pure vector database services, by contrast, come with 9 hours or more of downtime. This availability provides a solid foundation for mission-critical workloads. At the same time, the various service models in Azure Cosmos DB, like [Reserved Capacity](reserved-capacity.md) or Serverless, can help reduce financial costs.

### Simplicity

Azure Cosmos DB can simplify data management and architecture by integrating multiple database functionalities into a single, cohesive platform.

Its integrated vector database capabilities can store, index, and query embeddings alongside the corresponding data in natural or programming languages. This capability enables greater data consistency, scale, and performance.

Its flexibility supports the varied modalities and fluid schemas of the metadata, relationships, entities, summaries, chat history, user preferences, sensory data, decisions, facts learned, or other operational data involved in agent workflows. The database automatically indexes all data without requiring schema or index management, which helps AI agents perform complex queries quickly and efficiently.

Azure Cosmos DB is fully managed, which eliminates the overhead of database administration tasks like scaling, patching, and backups. Without this overhead, developers can focus on building and optimizing AI agents without worrying about the underlying data infrastructure.

### Advanced features

Azure Cosmos DB incorporates advanced features such as change feed, which allows tracking and responding to changes in data in real time. This capability is useful for AI agents that need to react to new information promptly.

Additionally, the built-in support for multi-master writes enables high availability and resilience to help ensure continuous operation of AI agents, even after regional failures.

The five available [consistency levels](consistency-levels.md) (from strong to eventual) can also cater to various distributed workloads, depending on the scenario requirements.

> [!TIP]
> Use Azure Cosmos DB for NoSQL to build your AI agent memory system. The API for NoSQL offers 99.999% availability guarantee and provides [three vector search algorithms](nosql/vector-search.md):
>
> - IVF
> - HNSW
> - DiskANN
>
> For information about the availability guarantees for this API, see the [service SLAs](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services).
>

## Related content

- [Azure Cosmos DB lifetime free tier](free-tier.md)
