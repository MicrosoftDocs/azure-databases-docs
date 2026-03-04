---
title: Quickstart - AI Agent with Vector Search in TypeScript
description: Learn how to build an AI agent using TypeScript with vector search in Azure DocumentDB. Create intelligent hotel recommendation agents that use semantic search with LangChain.
ms.date: 03/04/2026
ms.topic: quickstart-sdk
ms.custom: devx-track-ai-agent, devx-track-azd, devx-track-typescript
ai-usage: ai-assisted
# CustomerIntent: As a developer, I want to learn how to build AI agents with vector search in TypeScript applications with Azure DocumentDB.
---

# Quickstart: AI Agent with vector search in Azure DocumentDB using TypeScript

Build an intelligent AI agent by using TypeScript and Azure DocumentDB. This quickstart demonstrates a two-agent architecture that performs semantic hotel search and generates personalized recommendations.

> [!IMPORTANT]
> This sample uses LangChain, a popular framework for building AI applications. LangChain provides abstractions for agents, tools, and prompts that simplify agent development.


## Prerequisites

You can use the Azure Developer CLI to create the required Azure resources by running the `azd` commands in the sample repository. For more information, see [Deploy Infrastructure with Azure Developer CLI](https://github.com/Azure-Samples/documentdb-samples/).

### Azure resources

- **[Azure OpenAI in Microsoft Foundry Models resource (classic)](/azure/foundry-classic/openai/how-to/create-resource)** with the following model deployments in Microsoft Azure AI Foundry:
  - `gpt-4o` deployment (Synthesizer Agent) - Recommended: **50,000 tokens per minute (TPM)** capacity
  - `gpt-4o-mini` deployment (Planner Agent) - Recommended: **30,000 tokens per minute (TPM)** capacity
  - `text-embedding-3-small` deployment (Embeddings) - Recommended: **10,000 tokens per minute (TPM)** capacity
  - **Token quotas**: Configure sufficient TPM for each deployment to avoid rate limiting
    - See [Manage Azure OpenAI quotas](/azure/ai-services/openai/how-to/quota) for quota management
    - If you encounter 429 errors, increase your TPM quota or reduce request frequency

- **[Azure DocumentDB (with MongoDB compatibility) cluster](quickstart-portal.md)** with vector search support:
  - **Cluster tier requirements** based on your preferred vector index algorithm:
    - **IVF (Inverted File Index)**: M10 or higher (default algorithm)
    - **HNSW (Hierarchical Navigable Small World)**: M30 or higher (graph-based)
    - **DiskANN**: M40 or higher (optimized for large-scale)
  - **Firewall configuration**: REQUIRED. Without proper firewall configuration, connection attempts fail
    - Add your client IP address to the cluster's firewall rules. For more information, see [Grant access from your IP address](how-to-configure-firewall.md#grant-access-from-your-ip-address).
  - For passwordless authentication, Role Based Access Control (RBAC) enabled

### Development tools

- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) for resource provisioning
- [Node.js LTS](https://nodejs.org/)
- [TypeScript](https://www.typescriptlang.org/) 5.0 or later
- [Azure CLI](/cli/azure/install-azure-cli) for authentication
- [Visual Studio Code](https://code.visualstudio.com/) with the [DocumentDB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb) for database management (optional)

## Agentic RAG application Architecture

The sample uses a two-agent architecture where each agent has a specific role.

:::image type="content" source="media/quickstart-agent-typescript/agent-architecture-typescript.svg" alt-text="Architecture diagram showing the two-agent workflow with planner agent, vector search tool, and synthesizer agent." border="false":::

This sample uses LangChain's agent framework with the OpenAI SDK. It leverages LangChain's function calling abstractions for tool integration and follows a linear workflow between the agents and the search tool. The execution is stateless with no conversation history, making it suitable for single-turn query and response scenarios.

## Get the Node.js sample code

1. Clone or download the repository [Azure DocumentDB Samples](https://github.com/Azure-Samples/documentdb-samples/) to your local machine to follow the quickstart.

1. Navigate to the project directory:

    ```bash
    cd ai/vector-search-agent-typescript
    ```

## Deploy Azure resources with Azure Developer CLI

Use the Azure Developer CLI (`azd`) to provision the required Azure OpenAI and DocumentDB resources.

1. Sign in to Azure:

    ```bash
    azd auth login
    ```

1. Provision and deploy the infrastructure:

    ```bash
    azd up
    ```

1. When prompted, select your subscription and a location (for example, `swedencentral` or `eastus2`).

1. After deployment completes, `azd` outputs the environment variables you need. Copy them into your `.env` file (see [Configure environment variables](#configure-environment-variables)).

> [!TIP]
> Run `azd env get-values` at any time to view the current environment values.

## Configure environment variables

If you created your Azure resources manually or want to use your own existing resources, you need to configure environment variables for the application to connect to Azure OpenAI and Azure DocumentDB. If you used `azd up`, you can skip this step, as the necessary environment variables are automatically set in the `azd` environment and can be accessed with `azd env get-values`.

Create a `.env` file in your project root to configure environment variables. You can create a copy of the `.env.sample` file from the repository.

Edit the `.env` file and replace these placeholder values:

This quickstart uses a two-agent architecture (planner + synthesizer) with three model deployments (two chat models + embeddings). The environment variables are configured for each model deployment. 

- `AZURE_OPENAI_PLANNER_DEPLOYMENT`: Your gpt-4o-mini deployment name
- `AZURE_OPENAI_SYNTH_DEPLOYMENT`: Your gpt-4o deployment name
- `AZURE_OPENAI_EMBEDDING_MODEL`: Your text-embedding-3-small deployment name

You can choose between two authentication methods: passwordless authentication using Azure Identity (recommended) or traditional connection string and API key.

### Option 1: Passwordless authentication

Use passwordless authentication with both Azure OpenAI and Azure DocumentDB. Set `USE_PASSWORDLESS=true`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_DOCUMENTDB_CLUSTER`.

```.env
# Enable passwordless authentication
USE_PASSWORDLESS=true

# Azure OpenAI Configuration (passwordless)
AZURE_OPENAI_ENDPOINT=your-openai-endpoint
AZURE_OPENAI_PLANNER_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_PLANNER_API_VERSION=2024-08-01-preview
AZURE_OPENAI_SYNTH_DEPLOYMENT=gpt-4o
AZURE_OPENAI_SYNTH_API_VERSION=2024-08-01-preview
AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-3-small
AZURE_OPENAI_EMBEDDING_API_VERSION=2023-05-15

# Azure DocumentDB (passwordless)
AZURE_DOCUMENTDB_CLUSTER=your-mongo-cluster-name
AZURE_DOCUMENTDB_DATABASENAME=Hotels
AZURE_DOCUMENTDB_COLLECTION=hotel_data

# Data Configuration
DATA_FILE_WITHOUT_VECTORS=../data/Hotels.json

# Vector Index Configuration
VECTOR_INDEX_ALGORITHM=vector-ivf
EMBEDDING_DIMENSIONS=1536
```

**Prerequisites for passwordless authentication:**
- Ensure you're signed in to Azure: `az login`
- Grant your identity the following roles:
  - `Cognitive Services OpenAI User` on the Azure OpenAI resource
  - `DocumentDB Account Contributor` and `Cosmos DB Account Reader Role` on the Azure DocumentDB resource

  For more information about assigning roles, see [Assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal).

#### How passwordless authentication works

When `USE_PASSWORDLESS=true`, the application uses `DefaultAzureCredential` from the Azure Identity SDK to obtain an OAuth token. For Azure DocumentDB connections, it uses an OIDC token callback that passes the access token directly to the MongoDB driver. This means no passwords or connection strings are stored in configuration files.

The authentication flow:

1. `DefaultAzureCredential` checks for available credentials (Azure CLI, managed identity, environment variables) in order.
2. For Azure OpenAI, the token is passed to the LangChain `AzureChatOpenAI` and `AzureOpenAIEmbeddings` clients automatically.
3. For Azure DocumentDB, a token callback function fetches an access token and provides it to the MongoDB client via the `MONGODB-OIDC` auth mechanism.

:::code language="typescript" source="~/documentdb-samples/ai/vector-search-agent-typescript/src/utils/clients.ts" range="1-40":::

### Option 2: Connection string and API key authentication

Use key-based authentication by setting `USE_PASSWORDLESS=false` (or omitting it) and providing `AZURE_OPENAI_API_KEY` and `AZURE_DOCUMENTDB_CONNECTION_STRING` values in your `.env` file.

```.env
# Disable passwordless authentication
USE_PASSWORDLESS=false

# Azure OpenAI Configuration (API key)
AZURE_OPENAI_ENDPOINT=your-openai-endpoint
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_PLANNER_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_PLANNER_API_VERSION=2024-08-01-preview
AZURE_OPENAI_SYNTH_DEPLOYMENT=gpt-4o
AZURE_OPENAI_SYNTH_API_VERSION=2024-08-01-preview
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
AZURE_OPENAI_EMBEDDING_API_VERSION=2023-05-15

# Azure DocumentDB (connection string)
AZURE_DOCUMENTDB_CLUSTER=your-mongo-cluster-name
AZURE_DOCUMENTDB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongocluster.cosmos.azure.com/
AZURE_DOCUMENTDB_DATABASENAME=Hotels
AZURE_DOCUMENTDB_COLLECTION=hotel_data

# Data Configuration
DATA_FILE_WITHOUT_VECTORS=../data/Hotels.json

# Vector Index Configuration
VECTOR_INDEX_ALGORITHM=vector-ivf
EMBEDDING_DIMENSIONS=1536
```

## Project structure

The project follows a standard Node.js/TypeScript project layout. Your directory structure should look like the following structure:

```
vector-search-agent-typescript/
├── src/
│   ├── agent.ts              # Main agent application
│   ├── upload-documents.ts   # Data upload utility
│   ├── cleanup.ts            # Database cleanup utility
│   ├── vector-store.ts       # Vector store and tool implementation
│   ├── utils/
│   │   ├── clients.ts        # Azure OpenAI and DocumentDB client setup
│   │   ├── prompts.ts        # System prompts and tool definitions
│   │   ├── types.ts          # TypeScript type definitions
│   │   └── mongo.ts          # MongoDB utility functions
│   └── scripts/              # Additional utility scripts
├── .env                      # Environment variable configuration
├── package.json              # npm dependencies and scripts
└── tsconfig.json             # TypeScript configuration
```

## Explore the Node.js code for agentic RAG application

This section walks through the core components of the AI agent workflow. It highlights how the agents process requests, how tools connect the AI to the database, and how prompts guide the AI's behavior.

### Node.js Agentic RAG application

The `src/agent.ts` file orchestrates an AI-powered hotel recommendation system.

The application uses two Azure services:

- Azure OpenAI that uses AI models that understand queries and generate recommendations
- Azure DocumentDB that stores hotel data and performs vector similarity searches

#### Node.js Agent and tool components

The three components work together to process the hotel search request:

- **Planner agent** - Interprets the request and decides how to search
- **Vector search tool** - Finds hotels similar to what the planner agent describes
- **Synthesizer agent** - Writes a helpful recommendation based on search results

#### Agentic RAG Application workflow

The application processes a hotel search request in two steps:

- **Planning:** The workflow calls the planner agent, which analyzes the user's query (like "hotels near running trails") and searches the database for matching hotels.
- **Synthesizing:** The workflow calls the synthesizer agent, which reviews the search results and writes a personalized recommendation explaining which hotels best match the request.

:::code language="typescript" source="~/documentdb-samples/ai/vector-search-agent-typescript/src/agent.ts" range="72-96":::

### Node.js Agents for planning and synthesizing

The `src/agent.ts` source file implements the planner and synthesizer agents that work together to process hotel search requests.

#### Planner agent

The planner agent is the *decision maker* that determines how to search for hotels.

The planner agent receives the user's natural language query and sends it to an AI model using LangChain's agent framework along with available tools it can use. The AI decides to call the vector search tool and provides search parameters. LangChain handles the tool execution automatically and returns the matching hotels. Instead of hardcoding search logic, the AI interprets what the user wants and chooses how to search, making the system flexible for different types of queries.

:::code language="typescript" source="~/documentdb-samples/ai/vector-search-agent-typescript/src/agent.ts" range="12-45":::

#### Synthesizer agent

The synthesizer agent is the *writer* that creates helpful recommendations.

The synthesizer agent receives the original user query along with the hotel search results. It sends everything to an AI model with instructions for writing recommendations. It returns a natural language response that compares hotels and explains the best options. This approach matters because raw search results aren't user-friendly. The synthesizer transforms database records into a conversational recommendation that explains why certain hotels match the user's needs.

:::code language="typescript" source="~/documentdb-samples/ai/vector-search-agent-typescript/src/agent.ts" range="48-69":::

### Agent tools for vector store search

The `src/vector-store.ts` source file defines the vector search tool that the planner agent uses.

The tools file defines a search tool that the AI agent can use to find hotels. This tool is how the agent connects to the database. The AI doesn't search the database directly. It asks to use the search tool, and the tool executes the actual search.

#### Node.js Function as tool definition 

LangChain's `tool` function creates a tool from a regular TypeScript function. The tool definition includes the name, description, and schema (using Zod for validation). This definition lets the AI know the tool exists and how to use it correctly.

:::code language="typescript" source="~/documentdb-samples/ai/vector-search-agent-typescript/src/vector-store.ts" range="144-176":::

#### Node.js Tool execution with Azure DocumentDB vector search

When the AI calls the tool, the function body runs. It generates an embedding by converting the text query into a numeric vector using Azure OpenAI's embedding model. Then it searches the database by sending the vector to Azure DocumentDB, which finds hotels with similar vectors meaning similar descriptions. Finally, it formats results by converting the database records into readable text that the synthesizer agent can understand.

The implementation leverages LangChain's `AzureDocumentDBVectorStore` for seamless integration with Azure DocumentDB.

#### Why use this pattern?

Separating the tool from the agent provides flexibility. The AI decides when to search and what to search for, while the tool handles how to search. You can add more tools without changing the agent logic.

### Agent prompts for guiding AI behavior

The `src/utils/prompts.ts` source file contains system prompts and tool definitions for the agents.

The prompts file defines the instructions and context given to the AI models for both the planner and synthesizer agents. These prompts guide the AI's behavior and ensure it understands its role in the workflow.

The quality of AI responses depends heavily on clear instructions. These prompts set boundaries, define the output format, and focus the AI on the user's goal of making a decision. You can customize these prompts to change how the agents behave without modifying any code.

:::code language="typescript" source="~/documentdb-samples/ai/vector-search-agent-typescript/src/utils/prompts.ts" range="30-75":::

## Prepare and upload data to Azure DocumentDB with Node.js 

The sample uses hotel data from a JSON file. The repository includes two versions:

- `Hotels.json` - Hotel data without vector embeddings (used by this sample)
- `Hotels_Vector.json` - Hotel data with pre-computed embeddings (used by other samples)

### How the upload works

The `upload-documents.ts` script performs three steps:

1. **Load data** — Reads hotel records from the `Hotels.json` file.
2. **Generate embeddings** — For each hotel, the script sends the `Description` field to the Azure OpenAI `text-embedding-3-small` model to generate a 1536-dimensional vector embedding. This converts the text description into a numeric representation that captures its semantic meaning.
3. **Insert and index** — The script inserts documents (with their embeddings) into the Azure DocumentDB collection and creates a vector index using the configured algorithm (IVF, HNSW, or DiskANN).

:::code language="typescript" source="~/documentdb-samples/ai/vector-search-agent-typescript/src/upload-documents.ts":::

### Vector index creation

The vector index is what enables fast similarity search. When the index is created, Azure DocumentDB organizes the embedding vectors so that queries like "find hotels similar to this description" can be answered efficiently without scanning every document.

The index type you choose affects performance:

| Algorithm | Cluster tier | Best for |
|---|---|---|
| **IVF** | M10+ | Small to medium datasets, lower cost |
| **HNSW** | M30+ | High recall, fast queries |
| **DiskANN** | M40+ | Large-scale datasets, billion+ vectors |

:::code language="typescript" source="~/documentdb-samples/ai/vector-search-agent-typescript/src/vector-store.ts" range="1-50":::

## Run the agentic RAG application with Node.js

1. Install dependencies:

    ```bash
    npm install
    ```

1. Before running the agent, upload hotel data with embeddings. The `upload-documents.ts` command loads hotels from the JSON file, generates embeddings for each hotel using `text-embedding-3-small`, inserts documents into Azure DocumentDB, and creates a vector index.

    ```bash
    npm run upload
    ```

1. Run the hotel recommendation agent by using the `agent.ts` command. The agent calls the planner agent, the vector search, and the synthesizer agent. The output includes similarity scores, and the synthesizer agent's comparative analysis with recommendations.

    ```bash
    npm start
    ```

    ```output
    DEBUG mode is OFF
    DEBUG_CALLBACKS length: 0
    Connected to existing vector store: Hotels.hotel_data

    --- PLANNER ---
    Found 5 documents from vector store
    Hotel: Nordick's Valley Motel, Score: 0.49866509437561035
    Hotel: White Mountain Lodge & Suites, Score: 0.48731985688209534
    Hotel: Trails End Motel, Score: 0.47985398769378662
    Hotel: Country Comfort Inn, Score: 0.47431993484497070
    Hotel: Lakefront Captain Inn, Score: 0.45787304639816284

    --- SYNTHESIZER ---
    Context size is 3233 characters
    Output: 812 characters of final recommendation

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

    :::image type="content" source="media/quickstart-agent-typescript/documentdb-view-data.png" alt-text="Visual Studio Code DocumentDB extension showing the vector search index and hotel documents.":::

## Clean up resources

If you used `azd up` to provision resources, you can remove all Azure resources with:

```bash
azd down
```

If you manually created the resources, and want to remove all the resources, delete the resource group to avoid extra costs. 

If you want to reuse the resources, use the cleanup command to delete the test database when you're done. Run the following command:

```bash
npm run cleanup
```

## Related content

- [Vector search overview in Azure DocumentDB](/azure/documentdb/vector-search)
- [Quickstart: AI Agent with vector search using Go](/azure/documentdb/quickstart-agent-go)
- [Azure DocumentDB documentation](/azure/documentdb/)
- [LangChain.js Azure DocumentDB integration](https://js.langchain.com/docs/integrations/vectorstores/azure_cosmosdb_mongodb/)
- [Azure OpenAI in Foundry Models Service documentation](/azure/ai-services/openai/)
