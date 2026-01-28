---
title: Quickstart - AI Agent with Vector Search in Go
description: Learn how to build an AI agent using Go with vector search in Azure DocumentDB. Create intelligent hotel recommendation agents that use semantic search with a custom agentic architecture.
ms.date: 01/23/2026
ms.topic: quickstart-sdk
ms.custom: devx-track-go
ai-usage: ai-assisted
# CustomerIntent: As a developer, I want to learn how to build AI agents with vector search in Go applications with Azure DocumentDB.
---

# Quickstart: AI Agent with vector search in Azure DocumentDB using Go

Build an intelligent AI agent by using Go and Azure DocumentDB. This quickstart demonstrates a two-agent architecture that performs semantic hotel search and generates personalized recommendations.

> [!IMPORTANT]
> This sample is a reference implementation demonstrating agentic patterns in Go. It uses a custom-built agent architecture rather than an agent framework, which is the recommended approach for production agentic applications.

## Prerequisites

### Azure resources

- **Azure OpenAI resource** with the following model deployments in Microsoft Azure AI Foundry:
  - `gpt-4o` deployment (Synthesizer Agent) - Recommended: **50,000 tokens per minute (TPM)** capacity
  - `gpt-4o-mini` deployment (Planner Agent) - Recommended: **30,000 tokens per minute (TPM)** capacity
  - `text-embedding-3-small` deployment (Embeddings) - Recommended: **10,000 tokens per minute (TPM)** capacity
  - **Token quotas**: Configure sufficient TPM for each deployment to avoid rate limiting
    - See [Manage Azure OpenAI quotas](/azure/ai-services/openai/how-to/quota) for quota management
    - If you encounter 429 errors, increase your TPM quota or reduce request frequency

- **Azure Cosmos DB for MongoDB vCore cluster** with vector search support:
  - **Cluster tier requirements** based on vector index algorithm:
    - **IVF (Inverted File Index)**: M10 or higher (default algorithm)
    - **HNSW (Hierarchical Navigable Small World)**: M30 or higher (graph-based)
    - **DiskANN**: M40 or higher (optimized for large-scale)
  - **Firewall configuration**: REQUIRED Without proper firewall configuration, connection attempts fail
    - Add your client IP address to the cluster's firewall rules. For more information, see [Grant access from your IP address](/azure/cosmos-db/how-to-configure-firewall#grant-access-from-your-ip-address).
  - For passwordless authentication, Role Based Access Control (RBAC) enabled

### Development tools

- [Go](https://golang.org/dl/) 1.22 or later
- [Azure CLI](/cli/azure/install-azure-cli) for authentication

## Architecture

The sample uses a two-agent architecture where each agent has a specific role.

:::image type="content" source="media/quickstart-agent-go/agent-architecture-go.svg" alt-text="Architecture diagram showing the two-agent workflow with planner agent, vector search tool, and synthesizer agent." border="false" lightbox="media/quickstart-agent-go/agent-architecture-go.svg":::

This sample uses a custom implementation with the OpenAI SDK directly, without relying on an agent framework. It leverages OpenAI function calling for tool integration and follows a linear workflow between the agents and the search tool. The execution is stateless with no conversation history, making it suitable for single-turn query and response scenarios.

## Get the sample code

1. Clone or download the repository [Azure DocumentDB Vector Search - Go Agent Sample](https://github.com/Azure-Samples/cosmos-db-vector-samples/tree/main/mongo-vcore-agent-go) to your local machine to follow the quickstart.

1. Navigate to the project directory:

    ```bash
    cd mongo-vcore-agent-go
    ```

## Configure environment variables

Create a `.env` file in your project root to configure environment variables. You can create a copy of the `.env.sample` file from the repository.

Edit the `.env` file and replace these placeholder values:

This quickstart uses a two-agent architecture (planner + synthesizer) with three model deployments (two chat models + embeddings). The environment variables are configured for each model deployment. 

- `AZURE_OPENAI_PLANNER_DEPLOYMENT`: Your gpt-4o-mini deployment name
- `AZURE_OPENAI_SYNTH_DEPLOYMENT`: Your gpt-4o deployment name
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`: Your text-embedding-3-small deployment name

You can choose between two authentication methods: passwordless authentication using Azure Identity (recommended) or traditional connection string and API key.

### Option 1: Passwordless authentication

Use Azure Identity for passwordless authentication with both Azure OpenAI and Azure DocumentDB. Set `USE_PASSWORDLESS=true` or omit `AZURE_OPENAI_API_KEY` and `AZURE_DOCUMENTDB_CONNECTION_STRING`, and provide `AZURE_OPENAI_API_INSTANCE_NAME` and `MONGO_CLUSTER_NAME` instead.

```.env
# Enable passwordless authentication
USE_PASSWORDLESS=true

# Azure OpenAI Configuration (passwordless)
AZURE_OPENAI_API_INSTANCE_NAME=your-openai-instance-name

# Azure DocumentDB (passwordless)
MONGO_CLUSTER_NAME=your-mongo-cluster-name
MONGO_DB_NAME=vectorSearchDB
MONGO_DB_COLLECTION=vectorSearchCollection
MONGO_DB_INDEX_NAME=vectorSearchIndex
```

**Prerequisites for passwordless authentication:**
- Ensure you're signed in to Azure: `az login`
- Grant your identity the following roles:
  - `Cognitive Services OpenAI User` on the Azure OpenAI resource
  - `DocumentDB Account Contributor` and `Cosmos DB Account Reader Role` on the Azure DocumentDB resource

  For more information about assigning roles, see [Assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal).

### Option 2: Connection string and API key authentication

Use key-based authentication by setting `USE_PASSWORDLESS=false` (or omitting it) and providing `AZURE_OPENAI_API_KEY` and `AZURE_DOCUMENTDB_CONNECTION_STRING` values in your `.env` file.

```.env
# Disable passwordless authentication
USE_PASSWORDLESS=false

# Azure OpenAI Configuration (API key)
AZURE_OPENAI_API_INSTANCE_NAME=your-openai-instance-name
AZURE_OPENAI_API_KEY=your-azure-openai-api-key

# Azure DocumentDB (connection string)
AZURE_DOCUMENTDB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongocluster.cosmos.azure.com/
MONGO_DB_NAME=vectorSearchDB
MONGO_DB_COLLECTION=vectorSearchCollection
MONGO_DB_INDEX_NAME=vectorSearchIndex
```

## Copy the sample hotel data

Copy the `HotelsData_toCosmosDB.JSON` file from the root data directory of the repository into the data directory for the sample.

```bash
mkdir -p ./data    # Create data directory if it doesn't exist
cp ../data/HotelsData_toCosmosDB.JSON ./data/    # Copy the sample data file
```

## Project structure

The project follows the standard Go project layout. Your directory structure should look like the following structure:

```
mongo-vcore-agent-go/
├── cmd/
│   ├── agent/          # Main agent application
│   │   └── main.go
│   ├── upload/         # Data upload utility
│   │   └── main.go
│   └── cleanup/        # Database cleanup utility
│       └── main.go
├── data/               # Sample data files
│   └── HotelsData_toCosmosDB.JSON
├── internal/
│   ├── agents/         # Agent and tool implementations
│   │   ├── agents.go   # Planner and synthesizer agents
│   │   └── tools.go    # Vector search tool
│   ├── clients/        # Azure OpenAI client
│   │   └── openai.go
│   ├── models/         # Hotel data models
│   │   └── hotel.go
│   ├── prompts/        # System prompts and tool definitions
│   │   └── prompts.go
│   └── vectorstore/    # Azure DocumentDB vector store operations
│       └── store.go
├── .env                # Environment variable configuration
├── go.mod              # Go module file
└── go.sum              # Go module checksum file
```

## Explore the code

This section walks through the core components of the AI agent workflow. It highlights how the agents process requests, how tools connect the AI to the database, and how prompts guide the AI's behavior.

### Agent application

The `cmd/agent/main.go` file orchestrates an AI-powered hotel recommendation system.

The application uses two Azure services:

- Azure OpenAI that uses AI models that understand queries and generate recommendations
- Azure DocumentDB that stores hotel data and performs vector similarity searches

#### Agent and tool components

The three components work together to process the hotel search request:

- **Planner agent** - Interprets the request and decides how to search
- **Vector search tool** - Finds hotels similar to what the planner agent describes
- **Synthesizer agent** - Writes a helpful recommendation based on search results

#### Application workflow

The application processes a hotel search request in two steps:

- **Planning:** The workflow calls the planner agent, which analyzes the user's query (like "hotels near running trails") and searches the database for matching hotels.
- **Synthesizing:** The workflow calls the synthesizer agent, which reviews the search results and writes a personalized recommendation explaining which hotels best match the request.

:::code language="go" source="~/cosmos-db-vector-samples/mongo-vcore-agent-go/cmd/agent/main.go" range="71-85":::

### Agents

The `internal/agents/agents.go` source file implements the planner and synthesizer agents that work together to process hotel search requests.

#### Planner agent

The planner agent is the *decision maker* that determines how to search for hotels.

The planner agent receives the user's natural language query and sends it to an AI model along with available tools it can use. The AI decides to call the vector search tool and provides search parameters. The agent then extracts the tool name and arguments from the AI's response, executes the search tool, and returns the matching hotels. Instead of hardcoding search logic, the AI interprets what the user wants and chooses how to search, making the system flexible for different types of queries.

:::code language="go" source="~/cosmos-db-vector-samples/mongo-vcore-agent-go/internal/agents/agents.go" range="12-79":::

#### Synthesizer agent

The synthesizer agent is the *writer* that creates helpful recommendations.

The synthesizer agent receives the original user query along with the hotel search results. It sends everything to an AI model with instructions for writing recommendations. It returns a natural language response that compares hotels and explains the best options. This approach matters because raw search results aren't user-friendly. The synthesizer transforms database records into a conversational recommendation that explains why certain hotels match the user's needs.

:::code language="go" source="~/cosmos-db-vector-samples/mongo-vcore-agent-go/internal/agents/agents.go" range="87-109":::

### Agent tools

The `internal/agents/tools.go` source file defines the vector search tool that the planner agent uses.

The tools file defines a search tool that the AI agent can use to find hotels. This tool is how the agent connects to the database. The AI doesn't search the database directly. It asks to use the search tool, and the tool executes the actual search.

#### Tool definition

The `GetToolDefinition` method describes the tool to the AI model in a format it understands. It specifies the tool's name, a description of what the tool does, and the parameters defining what inputs the tool needs. This definition lets the AI know the tool exists and how to use it correctly.

:::code language="go" source="~/cosmos-db-vector-samples/mongo-vcore-agent-go/internal/agents/tools.go" range="54-81":::

#### Tool execution

When the AI calls the tool, the `Execute` method runs. It generates an embedding by converting the text query into a numeric vector using Azure OpenAI's embedding model. Then it searches the database by sending the vector to Azure DocumentDB, which finds hotels with similar vectors meaning similar descriptions. Finally, it formats results by converting the database records into readable text that the synthesizer agent can understand.

:::code language="go" source="~/cosmos-db-vector-samples/mongo-vcore-agent-go/internal/agents/tools.go" range="30-52":::

#### Why use this pattern?

Separating the tool from the agent provides flexibility. The AI decides when to search and what to search for, while the tool handles how to search. You can add more tools without changing the agent logic.

### Prompts

The `internal/prompts/prompts.go` source file contains system prompts and tool definitions for the agents.

The prompts file defines the instructions and context given to the AI models for both the planner and synthesizer agents. These prompts guide the AI's behavior and ensure it understands its role in the workflow.

The quality of AI responses depends heavily on clear instructions. These prompts set boundaries, define the output format, and focus the AI on the user's goal of making a decision. You can customize these prompts to change how the agents behave without modifying any code.

:::code language="go" source="~/cosmos-db-vector-samples/mongo-vcore-agent-go/internal/prompts/prompts.go" range="20-51":::

## Run the sample

1. Before running the agent, upload hotel data with embeddings. The `cmd/upload/main.go` command loads hotels from the JSON file, generates embeddings for each hotel using `text-embedding-3-small`, inserts documents into Azure DocumentDB, and creates a vector index.

    ```bash
    go run cmd/upload/main.go
    ```

1. Run the hotel recommendation agent by using the `cmd/agent/main.go` command. The agent calls the planner agent, the vector search, and the synthesizer agent. The output includes similarity scores, and the synthesizer agent's comparative analysis with recommendations.

    ```bash
    go run cmd/agent/main.go
    ```

    ```output
    Query: quintessential lodging near running trails, eateries, retail
    Nearest Neighbors: 5

    --- PLANNER ---
    Tool: search_hotels_collection
    Query: quintessential lodging near running trails, eateries, and retail shops with good amenities and access to outdoor activities
    K: 5
    Hotel #1: Nordick's Valley Motel, Score: 0.498665
    Hotel #2: White Mountain Lodge & Suites, Score: 0.487320
    Hotel #3: Trails End Motel, Score: 0.479854
    Hotel #4: Country Comfort Inn, Score: 0.474320
    Hotel #5: Lakefront Captain Inn, Score: 0.457873

    --- SYNTHESIZER ---
    Context size: 3233 characters

    --- FINAL ANSWER ---
    1. COMPARISON SUMMARY:  
    • Nordick's Valley Motel has the highest rating (4.5) and offers free parking, air conditioning, and continental breakfast. It is located in Washington D.C., near historic attractions and trails.
    • White Mountain Lodge & Suites is a resort with unique amenities like a pool, restaurant, and meditation gardens, but has the lowest rating (2.4). It is located in Denver, surrounded by forest trails.
    • Trails End Motel is budget-friendly with a moderate rating (3.2), free parking, free wifi, and a restaurant. It is close to downtown Scottsdale and eateries.

    Key tradeoffs:
    - Nordick's Valley Motel excels in rating and proximity to historic attractions but lacks a pool or free wifi.
    - White Mountain Lodge & Suites offers resort-style amenities and forest trails but has the lowest rating.
    - Trails End Motel balances affordability and essential amenities but has fewer unique features compared to the others.

    2. BEST OVERALL:
    Nordick's Valley Motel is the best choice for its high rating, proximity to trails and attractions, and free parking.

    3. ALTERNATIVE PICKS:
    • Choose White Mountain Lodge & Suites if you prioritize resort amenities and forest trails over rating.
    • Choose Trails End Motel if affordability and proximity to downtown Scottsdale are your main concerns.
    ```

## View and manage data in Visual Studio Code

1. Select the [DocumentDB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb) in Visual Studio Code to connect to your Azure DocumentDB account.

1. View the data and indexes in the Hotels database.

    :::image type="content" source="media/quickstart-agent-go/documentdb-view-data.png" alt-text="Visual Studio Code DocumentDB extension showing the vector search index and hotel documents.":::

## Clean up resources

Use the cleanup command to delete the test database when you're done. Run the following command:

```bash
go run cmd/cleanup/main.go
```
Delete the resource group, DocumentDB account, and Azure OpenAI resource when you don't need them to avoid extra costs.
