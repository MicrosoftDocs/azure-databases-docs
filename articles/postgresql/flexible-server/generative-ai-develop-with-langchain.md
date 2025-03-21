---
title: GenAI Frameworks and Azure Database for PostgreSQL
description: Integrate Azure Databases for PostgreSQL with AI and large language model (LLM) orchestration packages like Semantic Kernel and LangChain.
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

Azure Database for PostgreSQL seamlessly integrates with leading large language model (LLM) orchestration packages such as [LangChain](https://www.langchain.com/), enabling developers to harness the power of advanced AI capabilities within their applications. LangChanin can streamline the management and use of LLMs, embedding models, and databases, making it even easier to develop Generative AI applications.

This notebook shows you how to leverage Azure Database for PostgreSQL integrated [vector database](./how-to-use-pgvector.md) to store documents in collections, create indicies and perform vector search queries using approximate nearest neighbor algorithms such as Cosine Distance, L2 (Euclidean distance), and IP (inner product) to locate documents close to the query vectors.


## Vector Support

Azure Database for PostgreSQL - Flexible Server enables you to efficiently store and query millions of vector embeddings in PostgreSQL. As well as scale your AI use cases from POC to production:

-   Provides a familiar SQL interface for querying vector embeddings and relational data.
-   Boosts `pgvector` with a faster and more precise similarity search across 100M+ vectors using DiskANN indexing algorithm.
-   Simplifies operations by integrating relational metadata, vector embeddings, and time-series data into a single database.
-   Leverages the power of the robust PostgreSQL ecosystem and Azure Cloud for enterprise-grade features inculding replication, and high availability.

## Authentication

Azure Database for PostgreSQL - Flexible Server supports password-based as well as [Microsoft Entra](./concepts-azure-ad-authentication.md) (formerly Azure Active Directory) authentication. Entra authentication allows you to use Entra identity to authenticate to your PostgreSQL server. This eliminates the need to manage separate usernames and passwords for your database users, and allows you to leverage the same security mechanisms that you use for other Azure services.

This notebook is set up to use either authentication method. You can configure whether or not to use Entra authentication later in the notebook.

## Setup

Azure Database for PostgreSQL uses the open-source [LangChain's Postgres support](https://python.langchain.com/docs/integrations/vectorstores/pgvector/) to connect to Azure Database for PostgreSQL. First download the partner package:

```python
%pip install -qU langchain_postgres
%pip install -qU langchain-openai
%pip install -qU azure-identity
```

### Enable pgvector on Azure Database for PostgreSQL - Flexible Server

See [enablement instructions](./how-to-use-pgvector) for Azure Database for PostgreSQL.

### Credentials

You will need you Azure Database for PostgreSQL [connection details](./quickstart-create-server-portal#get-the-connection-information) and add them as environment variables to run this notebook.

Set the `USE_ENTRA_AUTH` flag to `True` if you want to use Microsoft Entra authentication. If using Entra authentication, you will only need to supply the host and database name. If using password authentication, you'll also need to set the username and password.

``` python
import getpass
import os

USE_ENTRA_AUTH = True

# Supply the connection details for the database
os.environ["DBHOST"] = "<server-name>"
os.environ["DBNAME"] = "<database-name>"
os.environ["SSLMODE"] = "require"

if not USE_ENTRA_AUTH:
    # If using a username and password, supply them here
    os.environ["DBUSER"] = "<username>"
    os.environ["DBPASSWORD"] = getpass.getpass("Database Password:")
```

### Setup Azure OpenAI Embeddings
``` python
os.environ["AZURE_OPENAI_ENDPOINT"] = "<azure-openai-endpoint>"
os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass("Azure OpenAI API Key:")
```

``` python
AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]

from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment="text-embedding-3-small",
)
```

## Initialization

### Entra Authentication

The cell below contains functions that set up LangChain to use Entra authentication. It provides a function `get_token_and_username` that retrieves tokens for the Azure DB for PostgreSQL service using `DefaultAzureCredential` from the `azure.identity` library. his is used to ensure the sqlalchemy Engine has a valid token with which to create new connections. It will also parse the token, which is a Java Web Token (JWT), to extract the username that is used to connect to the database.

The create_postgres_engine function creates a sqlalchemy `Engine` that dynamically sets the username and password based on the token fetched from the TokenManager. This `Engine` can be passed into the `connection` parameter of the `PGVector` LangChain VectorStore.

#### Logging into Azure

To log into Azure, ensure you have the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) installed. You will need to run the following command in your terminal:

``` bash
az login
```

Once you have logged in, the below code will be able to fetch the token.

``` python
import base64
import json
from functools import lru_cache

from azure.identity import DefaultAzureCredential
from sqlalchemy import create_engine, event
from sqlalchemy.engine.url import URL


@lru_cache(maxsize=1)
def get_credential():
    """Memoized function to create the Azure credential, which caches tokens."""
    return DefaultAzureCredential()


def decode_jwt(token):
    """Decode the JWT payload to extract claims."""
    payload = token.split(".")[1]
    padding = "=" * (4 - len(payload) % 4)
    decoded_payload = base64.urlsafe_b64decode(payload + padding)
    return json.loads(decoded_payload)


def get_token_and_username():
    """Fetches a token returns the username and token."""
    # Fetch a new token and extract the username
    token = get_credential().get_token(
        "https://ossrdbms-aad.database.windows.net/.default"
    )
    claims = decode_jwt(token.token)
    username = claims.get("upn")
    if not username:
        raise ValueError("Could not extract username from token. Have you logged in?")

    return username, token.token


def create_postgres_engine():
    db_url = URL.create(
        drivername="postgresql+psycopg",
        username="",  # This will be replaced dynamically
        password="",  # This will be replaced dynamically
        host=os.environ["DBHOST"],
        port=os.environ.get("DBPORT", 5432),
        database=os.environ["DBNAME"],
    )

    # Create a sqlalchemy engine
    engine = create_engine(db_url, echo=True)

    # Listen for the connection event to inject dynamic credentials
    @event.listens_for(engine, "do_connect")
    def provide_dynamic_credentials(dialect, conn_rec, cargs, cparams):
        # Fetch the dynamic username and token
        username, token = get_token_and_username()

        # Override the connection parameters
        cparams["user"] = username
        cparams["password"] = token

    return engine
```
 
### Password Authentication

If not using Entra authentication, the `get_connection_uri` provides a connection URI that pulls the username and password from environment
variables.

``` python
import urllib.parse


def get_connection_uri():
    # Read URI parameters from the environment
    dbhost = os.environ["DBHOST"]
    dbname = os.environ["DBNAME"]
    dbuser = urllib.parse.quote(os.environ["DBUSER"])
    password = os.environ["DBPASSWORD"]
    sslmode = os.environ["SSLMODE"]

    # Construct connection URI
    # Use psycopg 3!
    db_uri = (
        f"postgresql+psycopg://{dbuser}:{password}@{dbhost}/{dbname}?sslmode={sslmode}"
    )
    return db_uri
```

### Creating the vector store
``` python
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector

collection_name = "my_docs"

# The connection is either a sqlalchemy engine or a connection URI
connection = create_postgres_engine() if USE_ENTRA_AUTH else get_connection_uri()

vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)
```

## Manage vector store

### Add items to vector store

Note that adding documents by ID will over-write any existing documents that match that ID.

``` python
docs = [
    Document(
        page_content="there are cats in the pond",
        metadata={"id": 1, "location": "pond", "topic": "animals"},
    ),
    Document(
        page_content="ducks are also found in the pond",
        metadata={"id": 2, "location": "pond", "topic": "animals"},
    ),
    Document(
        page_content="fresh apples are available at the market",
        metadata={"id": 3, "location": "market", "topic": "food"},
    ),
    Document(
        page_content="the market also sells fresh oranges",
        metadata={"id": 4, "location": "market", "topic": "food"},
    ),
    Document(
        page_content="the new art exhibit is fascinating",
        metadata={"id": 5, "location": "museum", "topic": "art"},
    ),
    Document(
        page_content="a sculpture exhibit is also at the museum",
        metadata={"id": 6, "location": "museum", "topic": "art"},
    ),
    Document(
        page_content="a new coffee shop opened on Main Street",
        metadata={"id": 7, "location": "Main Street", "topic": "food"},
    ),
    Document(
        page_content="the book club meets at the library",
        metadata={"id": 8, "location": "library", "topic": "reading"},
    ),
    Document(
        page_content="the library hosts a weekly story time for kids",
        metadata={"id": 9, "location": "library", "topic": "reading"},
    ),
    Document(
        page_content="a cooking class for beginners is offered at the community center",
        metadata={"id": 10, "location": "community center", "topic": "classes"},
    ),
]

vector_store.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])
```

### Update items in vector store
``` python
docs = [
    Document(
        page_content="Updated - cooking class for beginners is offered at the community center",
        metadata={"id": 10, "location": "community center", "topic": "classes"},
    )
]
vector_store.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])
```

### Delete items from vector store
``` python
vector_store.delete(ids=["3"])
```

## Query vector store

Once your vector store has been created and the relevant documents have been added you will most likely wish to query it during the running of your chain or agent.

### Filtering Support

The vectorstore supports a set of filters that can be applied against the metadata fields of the documents.

  Operator    Meaning/Category
  ----------- ------------------------------
  $eq        Equality (==)
  $ne        Inequality (!=)
  $lt        Less than (\<)
  $lte       Less than or equal (\<=)
  $gt        Greater than (\>)
  $gte       Greater than or equal (\>=)
  $in        Special Cased (in)
  $nin       Special Cased (not in)
  $between   Special Cased (between)
  $like      Text (like)
  $ilike     Text (case-insensitive like)
  $and       Logical (and)
  $or        Logical (or)

### Query directly

Performing a simple similarity search can be done as follows:

``` python
results = vector_store.similarity_search(
    "kitty", k=10, filter={"id": {"$in": [1, 5, 2, 9]}}
)
for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")
```

```shell
    * there are cats in the pond [{'id': 1, 'topic': 'animals', 'location': 'pond'}]
    * ducks are also found in the pond [{'id': 2, 'topic': 'animals', 'location': 'pond'}]
    * the new art exhibit is fascinating [{'id': 5, 'topic': 'art', 'location': 'museum'}]
    * the library hosts a weekly story time for kids [{'id': 9, 'topic': 'reading', 'location': 'library'}]
```

If you provide a dict with multiple fields, but no operators, the top level will be interpreted as a logical **AND** filter

``` python
vector_store.similarity_search(
    "ducks",
    k=10,
    filter={"id": {"$in": [1, 5, 2, 9]}, "location": {"$in": ["pond", "market"]}},
)
```

```shell
    [Document(id='2', metadata={'id': 2, 'topic': 'animals', 'location': 'pond'}, page_content='ducks are also found in the pond'),
     Document(id='1', metadata={'id': 1, 'topic': 'animals', 'location': 'pond'}, page_content='there are cats in the pond')]
```

``` python
vector_store.similarity_search(
    "ducks",
    k=10,
    filter={
        "$and": [
            {"id": {"$in": [1, 5, 2, 9]}},
            {"location": {"$in": ["pond", "market"]}},
        ]
    },
)
```

```shell
    [Document(id='2', metadata={'id': 2, 'topic': 'animals', 'location': 'pond'}, page_content='ducks are also found in the pond'),
     Document(id='1', metadata={'id': 1, 'topic': 'animals', 'location': 'pond'}, page_content='there are cats in the pond')]
```

If you want to execute a similarity search and receive the corresponding scores you can run:

``` python
results = vector_store.similarity_search_with_score(query="cats", k=1)
for doc, score in results:
    print(f"* [SIM={score:3f}] {doc.page_content} [{doc.metadata}]")
```

```shell
    * [SIM=0.528338] there are cats in the pond [{'id': 1, 'topic': 'animals', 'location': 'pond'}]
```

For a full list of the different searches you can execute on a `PGVector` vector store, please refer to the [API reference](https://python.langchain.com/api_reference/postgres/vectorstores/langchain_postgres.vectorstores.PGVector.html).

### Query by turning into retriever

You can also transform the vector store into a retriever for easier usage in your chains.

``` python
retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 1})
retriever.invoke("kitty")
```

```shell
    [Document(id='1', metadata={'id': 1, 'topic': 'animals', 'location': 'pond'}, page_content='there are cats in the pond')]
```

## Current Limitations

-   langchain_postgres works only with psycopg3. Please update your connnecion strings from `postgresql+psycopg2://...` to `postgresql+psycopg://langchain:langchain@...` 
-   The schema of the embedding store and collection have been changed to make add_documents work correctly with user specified ids.
-   One has to pass an explicit connection object now.

Currently, there is **no mechanism** that supports easy data migration on schema changes. So any schema changes in the vectorstore will require the user to recreate the tables and re-add the documents. If this is a concern, please use a different vectorstore. If not, this implementation should be fine for your use case.


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
