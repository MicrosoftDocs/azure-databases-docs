---
title: AI Agents in Azure Database for PostgreSQL
description: Learn how to integrate Azure Database for PostgreSQL to create intelligent AI agents capable of advanced data retrieval and analysis.
author: abeomor
ms.author: abeomorogbe
ms.date: 03/17/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.collection: ce-skilling-ai-copilot
ms.custom:
  - build-2025
ms.topic: conceptual
---

Artificial Intelligence (AI) agents are transforming how applications interact with data by combining large language models (LLMs) with external tools and databases. Agents enable automation of complex workflows, enhances information retrieval accuracy, and facilitates natural language interfaces to databases. In this guide, we will explore how to create intelligent AI agents capable of searching and analyzing your data in Azure Database for PostgreSQL. We'll walk through setup, implementation, and testing, using a legal research assistant as our example.

## What are AI agents?
AI agents go beyond simple chatbots by combining large language models (LLMs) with external tools and databases. Unlike standalone LLMs or standard RAG systems, AI agents can:

* **Plan**: Break down complex tasks into smaller, sequential steps.
* **Use Tools**: Leverage APIs, code execution, search systems to gather information or perform actions.
* **Perceive**: Understand and process inputs from various data sources.
* **Remember**: Store and recall previous interactions for better decision-making.

By connecting AI agents to databases like Azure Database for PostgreSQL, agents can deliver more accurate, context-aware responses based on your data. AI agents extend beyond basic human conversation to carry out tasks based on natural language. These tasks traditionally required coded logic; however, agents can plan the tasks needed to execute based on user-provided context.

## Implementation of AI agents
### Frameworks
Various frameworks and tools can facilitate the development and deployment of AI agents.

* [Azure AI Agent Service](https://learn.microsoft.com/en-us/azure/ai-services/agents/overview)
* [LangChain/LangGraph] (https://python.langchain.com/v0.1/docs/modules/agents/)
* [LlamaIndex] (https://docs.llamaindex.ai/en/stable/use_cases/agents/)
* [Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/overview/)
* [AutoGen](https://microsoft.github.io/autogen/)
* [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview)

All these frameworks support using Azure Database for PostgreSQL as a tool. This uses the Azure AI Agents Service for agent planning, tool usage, and perception, while using Azure Database for PostgreSQL as a tool for vector database and semantic search capabilities.

## Implementation sample
In this tutorial, we'll build an AI agent that helps legal teams research relevant cases to support their clients in Washington state. Our agent will:

1. Accept natural language queries about legal situations.
1. Use vector search in Azure Database for PostgreSQL to find relevant case precedents.
1. Analyze and summarize the findings in a format useful for legal professionals.

### Prerequisites

1. [Enable and configure](generative-ai-azure-overview.md#enable-the-azure_ai-extension) the `azure_ai` & `pg_vector` extension.
1. [Create a Azure AI Foundry Project](https://learn.microsoft.com/en-us/azure/ai-services/agents/quickstart?pivots=ai-foundry-portal).
1. [Deploy models](https://learn.microsoft.com/en-us/azure/ai-services/agents/quickstart?pivots=ai-foundry-portal#deploy-a-model), the `gpt-4o-mini` & `text-embedding-small`
1. Install [Visual Studio Code](https://code.visualstudio.com/download).
1. Install the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension.
1. Install [Python 3.11.x](https://www.python.org/downloads/).
1. Install [Azure CLI.](https://learn.microsoft.com/cli/azure/install-azure-cli-windows?tabs=powershell)(latest version)

> [!NOTE]  
> You will need the key, and endpoint from the deployed models you created for the agent.

### Getting started
All the code and sample datasets are available in [this GitHub repository](https://github.com/Azure-Samples/postgres-agents).

### Step 1: Set Up Vector Search in Azure Database for PostgreSQL
First, we'll prepare our database to store and search legal case data using vector embeddings:

**Environment Setup:**

If using macOS / bash:

```bash
python -m venv .pg-azure-ai 
source .pg-azure-ai/bin/activate 
pip install -r requirements.txt
```

Windows / PowerShell

```bash
python -m venv .pg-azure-ai 
.pg-azure-ai \Scripts\Activate.ps1 
pip install -r requirements.txt
```

Windows / cmd.exe:

```bash
python -m venv .pg-azure-ai 
.pg-azure-ai \Scripts\activate.bat 
pip install -r requirements.txt
```

**Configure Environment Variables:**

Create a `.env` file with your credentials:

```bash
AZURE_OPENAI_API_KEY="" 
AZURE_OPENAI_ENDPOINT="" 
EMBEDDING_MODEL_NAME="" 
AZURE_PG_CONNECTION=""
```
 
**Load documents and vectors**

The Python file [load_data/main.py](https://github.com/Azure-Samples/postgres-agents/blob/main/load_data/main.py) serves as the central entry point for loading data into Azure Database for PostgreSQL. This code processes sample [cases data](https://github.com/Azure-Samples/postgres-agents/blob/main/load_data/cases.csv), including information about cases in Washington.


High level details of [main.py](https://github.com/Azure-Samples/postgres-agents/blob/main/load_data/main.py):
1. **Database setup and Table Creation**: Creates necessary extensions, sets up OpenAI API settings, and manages database tables by dropping existing ones and creating new ones for storing case data.
1. **Data Ingestion**: Reads data from a CSV file and inserts it into a temporary table, then processes and transfers this data into the main cases table.
1. **Embedding Generation**: Adds a new column for embeddings in the cases table and generates embeddings for case opinions using OpenAI's API, storing them in the new column. The embedding process will take ~3-5 minutes

To start the data loading process, run the following command from the *load_data* directory:

```bash
python main.py
```

Here's the output of *main.py*:

```
Extensions created successfully 
OpenAI connection established successfully 
Cases table created successfully 
Temp cases table created successfully 
Data loaded into temp_cases_data table successfully 
Data loaded into cases table successfully 
Adding Embeddings, this will take a while around 3-5 mins... 
Embeddings added successfully All Data loaded successfully!
```

### Step 2: Create Postgres tool for the Agent
In this step we will be configuring AI agent tools to retrieve data from Postgres and then using the **Azure AI Agent Service SDK** to connect your AI agent to the Postgres database.

**Define a function for your agent to call**

Start by defining a function for your agent to call by describing its structure and any required parameters in a docstring. Include all your function definitions in a single file, [legal_agent_tools.py](https://github.com/Azure-Samples/postgres-agents/blob/main/src/legal_agent_tools.py) which you can then import into your main script.

```python
def vector_search_cases(vector_search_query: str, start_date: datetime ="1911-01-01", end_date: datetime ="2025-12-31", limit: int = 10) -> str:
    """
    Fetches the cases information in Washington State for the specified query.

    :param query(str): The query to fetch cases for specifically in Washington.
    :type query: str
    :param start_date: The start date for the search, defaults to "1911-01-01"
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
    
    # Fetch cases information from the database
    df = pd.read_sql(query, db, params=(vector_search_query,datetime.strptime(start_date, "%Y-%m-%d"), datetime.strptime(end_date, "%Y-%m-%d"),limit))

    cases_json = json.dumps(df.to_json(orient="records"))
    return cases_json
 ```

### Step 3: Create and Configure the AI Agent with Postgres
 

Now we'll set up the AI agent and integrate it with our PostgreSQL tool. The Python file [src/simple_postgres_and_ai_agent.py](https://github.com/Azure-Samples/postgres-agents/blob/main/src/simple_postgres_and_ai_agent.py) serves as the central entry point for creating and using your agent.

High level details of [simple_postgres_and_ai_agent.py](https://github.com/Azure-Samples/postgres-agents/blob/main/src/simple_postgres_and_ai_agent.py):

1. **Create an Agent**: Initializes the agent in your Azure AI Project with a specific model.
1. **Add Postgres tool**: During the agent initialization, the Postgres tool to do vector search on your Postgres DB is added.
1. **Create a Thread**: Sets up a communication thread. This will be used to send messages to the agent to process
1. **Run the Agent and Call Postgres tool**: Processes the user's query using the agent and tools. The agent can plan with tools to use to get the correct answer. In this use case the agent will call the Postgres tool based on the function signature and docstring to do vector search and retrieve the relevant data to answer the question.
1. **Display the Agent’s Response**: Outputs the agent's response to the user's query.
 

**Find the Project Connection String in Azure AI Foundry**:

In your Azure AI Foundry project you will find you Project Connection String from the Overview page of the project we will use this string to connect the project to the AI agent SDK. We will be adding this string to the .env file.

![Project Setup Page](./media/generative-ai/ai-foundry-project-setup.png) 

**Connection Setup:**
Add these variables to your *.env* file in the root directory:

```shell
PROJECT_CONNECTION_STRING=" " 
MODEL_DEPLOYMENT_NAME="gpt-4o-mini" 
AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
```

```python
### Create the Agent with Tool Access
We will create the agent in the AI Foundry project and add the Postgres tools needed to query to Database. The code snippet below is an excerpt from the file [simple_postgres_and_ai_agent.py](https://github.com/Azure-Samples/postgres-agents/blob/main/src/simple_postgres_and_ai_agent.py).

# Create an Azure AI Client
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)

# Initialize agent toolset with user functions
functions = FunctionTool(user_functions)
toolset = ToolSet()
toolset.add(functions)

agent = project_client.agents.create_agent(
    model= os.environ["MODEL_DEPLOYMENT_NAME"], 
    name="legal-cases-agent",
    instructions= "You are a helpful legal assistant that can retrieve information about legal cases.", 
    toolset=toolset
)
```

**Create Communication Thread:**

This code snippet, shows how to create a thread and message for the agent. The thread and message will be what the agent processes in a run.

```python
# Create thread for communication
thread = project_client.agents.create_thread()

# Create message to thread
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Water leaking into the apartment from the floor above, What are the prominent legal precedents in Washington on this problem in the last 10 years?"
)
```

**Process the Request:**

This code snippet creates a run for the agent to process the message and use the appropriate tools to provide the best result.

Using the tool, the agent will be able to call your Postgres and the vector search on the query *“Water leaking into the apartment from the floor above”*, to retrieve the data it will need to answer the question best.

```python
from pprint import pprint

# Create and process agent run in thread with tools
run = project_client.agents.create_and_process_run(
thread_id=thread.id, 
agent_id=agent.id
)

# Fetch and log all messages
messages = project_client.agents.list_messages(thread_id=thread.id)
pprint(messages['data'][0]['content'][0]['text']['value'])
```

**Run the Agent:**

To run the agent, run the following command from the src directory:

```bash
python simple_postgres_and_ai_agent.py
```

The agent will produce a similar result as below using the Azure Database for PostgreSQL tool to access case data saved in the Postgres Database.

Snippet of output from agent:

```
1.     Pham v. Corbett

Citation: Pham v. Corbett, No. 4237124
Summary: This case involved tenants who counterclaimed against their landlord for relocation assistance and breach of the implied warranty of habitability due to severe maintenance issues, including water and sewage leaks. The trial court held that the landlord had breached the implied warranty and awarded damages to the tenants.

2.     Hoover v. Warner

Citation: Hoover v. Warner, No. 6779281
Summary: The Warners appealed a ruling finding them liable for negligence and nuisance after their road grading project caused water drainage issues affecting Hoover's property. The trial court found substantial evidence supporting the claim that the Warners' actions impeded the natural flow of water and damaged Hoover's property.
```

### Step 4: Testing and Debugging with Azure AI Foundry Playground
After running your agent with Azure AI Agent SDK, the agent will be stored in your project, and you can experiment with the agent in the Agent playground.

**Using the Agent Playground:**

1. Navigate to the Agents section in Azure AI Foundry
1. Find your agent in the list and click to open
1. Use the playground interface to test various legal queries
 
![Find AI Playground](./media/generative-ai/find-playground.png) 

1. Test the query *“Water leaking into the apartment from the floor above, What are the prominent legal precedents in Washington?”*. The agent will pick the right tool to use and ask for the expected output for that query. Use [sample_vector_search_cases_output.json](https://github.com/Azure-Samples/postgres-agents/blob/main/src/sample_outputs_for_playground/sample_vector_search_cases_output.json) as the sample output.
 
![Using AI Playground](./media/generative-ai/using-playground-ai-foundry.png) 

### Step 5: Debugging with Azure AI Foundry Tracing
When developing the agent by using the Azure AI Foundry SDK, you can also [debug the agent with Tracing.](https://learn.microsoft.com/en-us/azure/ai-services/agents/concepts/tracing?view=azure-python-preview) You will be able to debug the calls to tools like Postgres as well as seeing how to agent orchestrated each task.

**Debugging with Tracing:**

1. Click Tracing in the Azure AI Foundry menu
1. Create a new Application Insights resource or connect an existing one
 
![Activating Tracing](./media/generative-ai/activate-tracing.png) 

1. View detailed traces of your agent's operations

![Using Tracing in AI Foundry](./media/generative-ai/tracing-ai-foundry.png) 

Learn more about how to set up tracing with the AI agent and Postgres in the [advanced_postgres_and_ai_agent_with_tracing.py file on Github](https://github.com/Azure-Samples/postgres-agents/blob/main/src/advanced_postgres_and_ai_agent_with_tracing.py).


## Related content

- [Learn more about Azure OpenAI Service integration](generative-ai-azure-openai.md)
- [Learn more about Azure Machine Learning integration](generative-ai-azure-machine-learning.md)
- [Generate vector embeddings in Azure Database for PostgreSQL flexible server with locally deployed LLM (Preview)](generative-ai-azure-local-ai.md).
- [Integrate Azure Database for PostgreSQL with Azure Machine Learning Services](generative-ai-azure-machine-learning.md).
- [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL flexible server](generative-ai-azure-openai.md).
- [Azure AI extension in Azure Database for PostgreSQL flexible server](generative-ai-azure-overview.md).
- [Generative AI with Azure Database for PostgreSQL flexible server](generative-ai-overview.md).
- [Recommendation System with Azure Database for PostgreSQL flexible server and Azure OpenAI](generative-ai-recommendation-system.md).
- [Semantic Search with Azure Database for PostgreSQL flexible server and Azure OpenAI](generative-ai-semantic-search.md).
- [Enable and use pgvector in Azure Database for PostgreSQL flexible server](how-to-use-pgvector.md).
