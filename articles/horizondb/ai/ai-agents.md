---
title: Build AI agents with Azure HorizonDB
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

# Build AI agents with Azure HorizonDB

AI agents are transforming how applications interact with data. Unlike traditional applications that follow fixed logic, agents combine large language models (LLMs) with external tools, memory, and planning to autonomously reason through complex tasks. Azure HorizonDB provides the unified data layer that agents need — persistent memory, knowledge retrieval, and scalable storage — all inside a single PostgreSQL database.

## What are AI agents?

AI agents go beyond simple chatbots or standalone LLMs. An agent is a system that uses an LLM as its reasoning core, augmented with the ability to:

- **Plan**: Break down complex goals into sequential or parallel subtasks.
- **Use tools**: Call APIs, execute code, query databases, and interact with external services.
- **Perceive**: Process and understand inputs from diverse data sources — text, images, structured data.
- **Remember**: Store and recall context from current and past interactions to make better decisions.

These capabilities make agents fundamentally different from traditional retrieval-augmented generation (RAG) systems.

### How agents differ from RAG

Traditional RAG follows a fixed pipeline: retrieve documents via vector search, pass them as context to an LLM, and generate a response. It works for simple question-answering but can't break down multi-step queries, choose between tools, remember prior interactions, or self-correct. Agentic systems add a reasoning loop — the agent decides *when* to retrieve, *what* to search for, *which* tool to use, and *whether* to try a different approach.

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

## Why databases are essential for AI agents

AI agents need more than an LLM — they need persistent infrastructure. Databases serve three essential roles:

- **Memory and context**: Persist conversation history, user preferences, and task state so agents maintain continuity across interactions.
- **Knowledge retrieval**: Give agents access to your business data like product catalogs, customer records, policies, so that responses are grounded in facts, not just the LLM's training data.
- **Scalable multi-modal storage**: Handle relational records, JSON documents, vector embeddings, graph relationships, and geospatial data in a single system, eliminating the complexity of managing separate stores.

## Why PostgreSQL and Azure HorizonDB

PostgreSQL delivers on each of these pillars with purpose-built capabilities:

### Memory

PostgreSQL's SQL and ACID guarantees ensure agents don't operate on stale or corrupted state, critical for reliable memory persistence. Agents need both short-term memory (session context, intermediate reasoning steps) and long-term memory (user preferences, interaction history, learned facts that persist across sessions). Major agent frameworks including [Microsoft Agent Framework](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-python), [LangGraph](https://langchain-ai.github.io/langgraph/concepts/persistence/), and [Mem0](https://docs.mem0.ai/open-source/quickstart#4-postgresql) support PostgreSQL as a memory backend, providing built-in connectors for persisting chat history, agent state, and semantic memory.

### Knowledge retrieval

PostgreSQL extensions like `pgvector`, Apache AGE, and full-text search bring AI-native retrieval directly into the database engine — vector search, graph traversal, and keyword matching all run alongside your operational data in a single system.

Azure HorizonDB builds on this foundation with the following retrieval and AI capabilities:

- **[Vector search](vector-search-pgvector.md)**: Find content by semantic meaning, with [embeddings generated](generate-vector-embeddings.md) directly in SQL.
- **[Full-text and hybrid search](hybrid-search.md)**: Combine [full-text search](full-text-search-pgfts.md) with vector search for both semantic and keyword matching.
- **[Semantic reranking](semantic-reranking.md)**: Reorder results by true relevance to the query after initial retrieval.
- **[Knowledge graphs](build-knowledge-graph.md)**: Traverse entity relationships for [graph-augmented RAG](graphrag.md) and multi-hop reasoning.
- **[AI functions in SQL](ai-functions.md)**: Run extraction, generation, reranking, and embeddings directly in database queries.
- **[AI pipelines](ai-pipelines.md)**: Automate chunking, embedding, indexing, search, and reranking as durable pipelines inside the database.

### Scalable multi-modal storage

Native support for JSONB, geospatial data (PostGIS), arrays, full-text search, vector embeddings, and binary data, all in a single database. No need to manage separate stores for each data type your agents consume.

Additionally, PostgreSQL's open-source ecosystem provides decades of community development, extensive tooling, and [broad framework support](#orchestration-frameworks).

Azure HorizonDB adds managed infrastructure, built-in AI functions, AI Model Management, and AI pipelines on top of PostgreSQL, and is purpose-built for AI agent workloads.

## Multi-agent architecture

### Single agent vs. multi-agent

A single agent handles all reasoning, tool use, and retrieval within one orchestration loop — suitable for focused tasks where latency, cost, and debugging simplicity are priorities. Multi-agent architectures distribute work across specialized agents that collaborate on complex problems — useful when the task requires diverse expertise, parallelism, or different security boundaries for different parts of the workflow.

### Orchestration patterns

Multi-agent systems use several common patterns:

| Pattern | Description |
| --- | --- |
| **Supervisor** | A central agent delegates tasks to specialized worker agents, collects results, and synthesizes the final output. |
| **Sequential pipeline** | Agents hand off work in a defined sequence. Each agent's output becomes the next agent's input. |
| **Collaborative** | Agents communicate peer-to-peer, negotiating and sharing intermediate results without a central coordinator. |

When you build multi-agent systems, Azure HorizonDB serves as the shared data layer. All agents read from and write to the same database, ensuring consistent state and enabling coordination through shared memory and knowledge.

## Agent standards and protocols

Open standards are emerging to standardize how agents interact with tools and with each other.

### Model Context Protocol (MCP)

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open standard developed by Anthropic and now governed by the Linux Foundation. MCP defines how AI agents connect to external tools and data sources, acting as the "agent-to-tool" layer.

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

These protocols are complementary — MCP connects agents to tools and data, A2A connects agents to each other. Together, they enable complex multi-agent workflows that span multiple data sources and agent platforms.

## Orchestration frameworks

Agent frameworks provide the scaffolding for building, deploying, and managing AI agents. The following frameworks integrate with Azure HorizonDB:

| Framework | Description | Azure HorizonDB integration |
| --- | --- | --- |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | A unified, production-ready SDK by Microsoft for building AI agents in .NET and Python. Incorporates Semantic Kernel for orchestration, planning, and multi-agent workflows. | [Python connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-python), [.NET connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-csharp), [Java connector](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector?pivots=programming-language-java) |
| [LangChain / LangGraph](https://www.langchain.com/) | LangChain simplifies LLM application development. LangGraph adds stateful, graph-based orchestration for complex multi-agent workflows with checkpointed execution. | [Python](develop-with-langchain.md), [JavaScript](https://docs.langchain.com/oss/javascript/langchain/overview) |
| [LlamaIndex](https://www.llamaindex.ai/) | A framework for building context-augmented AI applications. Excels at structured data retrieval and knowledge-graph-powered reasoning over enterprise data. | [Python](https://aka.ms/azpg-llamaindex) |
| [CrewAI](https://www.crewai.com/) | An open-source framework for orchestrating role-based, collaborative multi-agent workflows with task delegation and standard operating procedures. | [PGSearchTool](https://docs.crewai.com/en/tools/database-data/pgsearchtool) |
| [AutoGen](https://microsoft.github.io/autogen/) | A Microsoft framework for multi-agent conversation patterns. Supports flexible agent communication topologies and tool integration. | [PostgreSQL tools](https://microsoft.github.io/autogen/) |
| [Microsoft Foundry Agent Service](/azure/ai-services/agents/overview) | A managed service for building, deploying, and scaling AI agents with built-in tool support, tracing, and monitoring. | [Implementation guide](foundry-agent-integration.md) |

## Build AI agents with Azure HorizonDB

To start building AI agents with Azure HorizonDB:

1. **Set up your data layer**: Create an Azure HorizonDB instance and enable the `azure_ai` and `pgvector` extensions. Store your domain data and [generate vector embeddings](generate-vector-embeddings.md).
1. **Choose a retrieval strategy**: Based on your use case, implement [vector search](vector-search-pgvector.md), [hybrid search](hybrid-search.md), or [graph-augmented RAG](graphrag.md) to give your agent access to domain knowledge.
1. **Configure agent memory**: Use your framework's PostgreSQL connector to persist conversation history and agent state in Azure HorizonDB.
1. **Connect your agent**: Use an [orchestration framework](ai-frameworks.md) or the [Microsoft Foundry Agent Service](foundry-agent-integration.md) to build your agent, connecting it to Azure HorizonDB through native connectors or the [MCP server](foundry-agent-integration.md).
1. **Enrich with AI functions**: Use [AI functions in SQL](ai-functions.md) to add extraction, generation, reranking, and embeddings directly in your database queries.
1. **Iterate and scale**: Set up [durable AI pipelines](ai-pipelines.md) to automate data preparation, add [semantic reranking](semantic-reranking.md) to improve retrieval quality, optimize [vector indexing](vector-indexing-diskann.md) for complex domains, and scale to multi-agent architectures as your workload grows.

For industry-specific implementation patterns, see [AI and agentic use cases and sample applications](samples.md).

## Related content

- [Implement Agent Knowledge Retrieval with Foundry and MCP](foundry-agent-integration.md)
- [AI and agentic use cases and sample applications](samples.md)
- [Overview of AI capabilities in Azure HorizonDB](overview.md)
- [Retrieval foundations: vector, full-text, and hybrid search](ai-search-overview.md)
- [Implement vector search with pgvector](vector-search-pgvector.md)
- [Graph-augmented RAG patterns](graphrag.md)
- [Implement durable AI pipelines](ai-pipelines.md)

<!-- Implementation example (preserved for review — not referenced from the article)

## Implementation example

This article's example uses [Agent Service](/azure/ai-services/agents/overview) for agent planning, tool usage, and perception. It uses Azure HorizonDB as a tool for vector database and semantic search capabilities.

The following sections walk you through building an AI agent that helps legal teams research relevant cases to support their clients in Washington State. The agent:

1. Accepts natural language queries about legal situations.
1. Uses vector search in Azure HorizonDB to find relevant case precedents.
1. Analyzes and summarizes the findings in a helpful format for legal professionals.

### Prerequisites

1. [Enable and configure](generative-ai-azure-overview.md#enable-the-azure_ai-extension) the `azure_ai` and `pg_vector` extensions.
1. [Create a Microsoft Foundry project](/azure/ai-services/agents/quickstart?pivots=ai-foundry-portal).
1. [Deploy models](/azure/ai-services/agents/quickstart?pivots=ai-foundry-portal#deploy-a-model) `gpt-4o-mini` and `text-embedding-small`.
1. Install [Visual Studio Code](https://code.visualstudio.com/download).
1. Install the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension.
1. Install [Python 3.11.x](https://www.python.org/downloads/).
1. Install the [Azure CLI](/cli/azure/install-azure-cli-windows?tabs=powershell) (latest version).

   > [!NOTE]
   > You need the key and endpoint from the deployed models that you created for the agent.

<a id="getting-started"></a>

### Get started

All the code and sample datasets are available in [this GitHub repository](https://github.com/Azure-Samples/postgres-agents).

### Step 1: Set up vector search in Azure HorizonDB

First, prepare your database to store and search legal case data by using vector embeddings.

#### Set up the environment

If you're using macOS and Bash, run these commands:

```bash
python -m venv .pg-azure-ai
source .pg-azure-ai/bin/activate
pip install -r requirements.txt
```

If you're using Windows and PowerShell, run these commands:

```bash
python -m venv .pg-azure-ai
.pg-azure-ai \Scripts\Activate.ps1
pip install -r requirements.txt
```

If you're using Windows and `cmd.exe`, run these commands:

```bash
python -m venv .pg-azure-ai
.pg-azure-ai \Scripts\activate.bat
pip install -r requirements.txt
```

#### Configure environment variables

Create an `.env` file with your credentials:

```bash
AZURE_OPENAI_API_KEY=""
AZURE_OPENAI_ENDPOINT=""
EMBEDDING_MODEL_NAME=""
AZURE_PG_CONNECTION=""
```

#### Load documents and vectors

The Python file [load_data/main.py](https://github.com/Azure-Samples/postgres-agents/blob/main/azure-ai-agent-service/load_data/main.py) serves as the central entry point for loading data into Azure HorizonDB. The code processes the [data for sample cases](https://github.com/Azure-Samples/postgres-agents/blob/main/azure-ai-agent-service/load_data/cases.csv), including information about cases in Washington.

The `main.py` file:

1. Creates necessary extensions, sets up OpenAI API settings, and manages database tables by dropping existing ones and creating new ones for storing case data.
1. Reads data from a CSV file and inserts it into a temporary table, and then processes and transfers it into the main case table.
1. Adds a new column for embeddings in the case table and generates embeddings for case opinions by using OpenAI's API. It stores the embeddings in the new column. The embedding process takes about 3 to 5 minutes.

To start the data loading process, run the following command from the `load_data` directory:

```bash
python main.py
```

Here's the output of `main.py`:

```output
Extensions created successfully
OpenAI connection established successfully
The case table was created successfully
Temp cases table created successfully
Data loaded into temp_cases_data table successfully
Data loaded into cases table successfully.
Adding Embeddings will take a while, around 3-5 mins.
Embeddings added successfully All Data loaded successfully!
```

### Step 2: Create a Postgres tool for the agent

Next, configure AI agent tools to retrieve data from Postgres. Then use the Agent Service SDK to connect your AI agent to the Postgres database.

#### Define a function for your agent to call

Start with defining a function for your agent to call by describing its structure and any required parameters in a docstring. Include all your function definitions in a single file, [legal_agent_tools.py](https://github.com/Azure-Samples/postgres-agents/blob/main/azure-ai-agent-service/src/legal_agent_tools.py). You can then import the file into your main script.

```python
def vector_search_cases(vector_search_query: str, start_date: datetime ="1911-01-01", end_date: datetime ="2025-12-31", limit: int = 10) -> str:
    """
 Fetches the case information in Washington State for the specified query.

 :param query(str): The query to fetch cases specifically in Washington.
 :type query: str
 :param start_date: The start date for the search defaults to "1911-01-01"
 :type start_date: datetime, optional
 :param end_date: The end date for the search, defaults to "2025-12-31"
 :type end_date: datetime, optional
 :param limit: The maximum number of cases to fetch, defaults to 10
 :type limit: int, optional

 :return: Cases information as a JSON string.
 :rtype: str
 """

 db = create_engine(CONN_STR)

 query = """
 SELECT id, name, opinion,
 opinions_vector <=> azure_openai.create_embeddings(
 'text-embedding-3-small', %s)::vector as similarity
 FROM cases
 WHERE decision_date BETWEEN %s AND %s
 ORDER BY similarity
 LIMIT %s;
 """

    # Fetch case information from the database
 df = pd.read_sql(query, db, params=(vector_search_query,datetime.strptime(start_date, "%Y-%m-%d"), datetime.strptime(end_date, "%Y-%m-%d"),limit))

 cases_json = json.dumps(df.to_json(orient="records"))
    return cases_json
 ```

### Step 3: Create and configure the AI agent with Postgres

Now, set up the AI agent and integrate it with the Postgres tool. The Python file [src/simple_postgres_and_ai_agent.py](https://github.com/Azure-Samples/postgres-agents/blob/main/azure-ai-agent-service/src/simple_postgres_and_ai_agent.py) serves as the central entry point for creating and using your agent.

The `simple_postgres_and_ai_agent.py` file:

1. Initializes the agent in your Foundry project with a specific model.
1. Adds the Postgres tool for vector search on your database, during the agent initialization.
1. Sets up a communication thread. This thread is used to send messages to the agent for processing.
1. Processes the user's query by using the agent and tools. The agent can plan with tools to get the correct answer. In this use case, the agent calls the Postgres tool based on the function signature and docstring to do a vector search and retrieve the relevant data to answer the question.
1. Displays the agent's response to the user's query.

#### Find the project connection string in Foundry

In your Foundry project, you find your project connection string from the project's overview page. You use this string to connect the project to the Agent Service SDK. Add this string to the `.env` file.

#### Set up the connection

Add these variables to your `.env` file in the root directory:

```shell
PROJECT_CONNECTION_STRING=" "
MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
```

```python
### Create the agent with tool access
We created the agent in the Foundry project and added the Postgres tools needed to query the database. The code snippet below is an excerpt from the file [simple_postgres_and_ai_agent.py](https://github.com/Azure-Samples/postgres-agents/blob/main/azure-ai-agent-service/src/simple_postgres_and_ai_agent.py).

# Create a Foundry client
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)

# Initialize the agent toolset with user functions
functions = FunctionTool(user_functions)
toolset = ToolSet()
toolset.add(functions)

agent = project_client.agents.create_agent(
    model= os.environ["MODEL_DEPLOYMENT_NAME"],
    name="legal-cases-agent",
    instructions= "You are a helpful legal assistant who can retrieve information about legal cases.",
    toolset=toolset
)
```

#### Create a communication thread

This code snippet shows how to create an agent thread and message, which the agent processes in a run:

```python
# Create a thread for communication
thread = project_client.agents.create_thread()

# Create a message to thread
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Water leaking into the apartment from the floor above. What are the prominent legal precedents in Washington regarding this problem in the last 10 years?"
)
```

#### Process the request

The following code snippet creates a run for the agent to process the message and use the appropriate tools to provide the best result.

By using the tools, the agent can call Postgres and the vector search on the query "Water leaking into the apartment from the floor above" to retrieve the data that it needs to best answer the question.

```python
from pprint import pprint

# Create and process an agent run in the thread with tools
run = project_client.agents.create_and_process_run(
thread_id=thread.id,
agent_id=agent.id
)

# Fetch and log all messages
messages = project_client.agents.list_messages(thread_id=thread.id)
pprint(messages['data'][0]['content'][0]['text']['value'])
```

#### Run the agent

To run the agent, run the following command from the `src` directory:

```bash
python simple_postgres_and_ai_agent.py
```

The agent produces a similar result by using the Azure HorizonDB tool to access case data saved in the Postgres database.

Here's a snippet of output from the agent:

```
1.     Pham v. Corbett

Citation: Pham v. Corbett, No. 4237124
Summary: This case involved tenants who counterclaimed against their landlord for relocation assistance and breached the implied warranty of habitability due to severe maintenance issues, including water and sewage leaks. The trial court held that the landlord had breached the implied warranty and awarded damages to the tenants.

2.     Hoover v. Warner

Citation: Hoover v. Warner, No. 6779281
Summary: The Warners appealed a ruling finding them liable for negligence and nuisance after their road grading project caused water drainage issues affecting Hoover's property. The trial court found substantial evidence supporting the claim that the Warners' actions impeded the natural water flow and damaged Hoover's property.
```

### Step 4: Test and debug with the agent playground

After you run your agent by using the Agent Service SDK, the agent is stored in your project. You can experiment with the agent in the agent playground:

1. In Foundry, go to the **Agents** section.

1. Find your agent in the list and select it to open it.

1. Use the playground interface to test various legal queries.

   :::image type="content" source="media/generative-ai-agents/find-playground.png" alt-text="Screenshot that shows selections for finding the agent playground." lightbox="media/generative-ai-agents/find-playground.png":::

1. Test the query "Water leaking into the apartment from the floor above, What are the prominent legal precedents in Washington?" The agent picks the right tool to use and asks for the expected output for that query. Use [sample_vector_search_cases_output.json](https://github.com/Azure-Samples/postgres-agents/blob/main/azure-ai-agent-service/src/sample_outputs_for_playground/sample_vector_search_cases_output.json) as the sample output.

   :::image type="content" source="media/generative-ai-agents/playground-ai-foundry.png" alt-text="Screenshot that shows the results of a query in the agent playground." lightbox="media/generative-ai-agents/playground-ai-foundry.png":::

### Step 5: Debug with Foundry tracing

When you're developing the agent by using the Agent Service SDK, you can [debug the agent with tracing](/azure/ai-services/agents/concepts/tracing). Tracing allows you to debug the calls to tools like Postgres and see how the agent orchestrates each task.

1. In Foundry, go to **Tracing**.

1. To create a new Application Insights resource, select **Create new**. To connect an existing resource, select one in the **Application Insights resource name** box, and then select **Connect**.

   :::image type="content" source="media/generative-ai-agents/activate-tracing.png" alt-text="Screenshot that shows the area for selecting an Application Insights resource and activating tracing." lightbox="media/generative-ai-agents/activate-tracing.png":::

1. View detailed traces of your agent's operations.

   :::image type="content" source="media/generative-ai-agents/tracing-ai-foundry.png" alt-text="Screenshot that the result of tracing in Foundry." lightbox="media/generative-ai-agents/tracing-ai-foundry.png":::

Learn more about how to set up tracing with the AI agent and Postgres in the [advanced_postgres_and_ai_agent_with_tracing.py file on GitHub](https://github.com/Azure-Samples/postgres-agents/blob/main/azure-ai-agent-service/src/advanced_postgres_and_ai_agent_with_tracing.py).

-->
