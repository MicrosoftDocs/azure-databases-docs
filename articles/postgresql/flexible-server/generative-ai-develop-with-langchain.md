---
title: Use LangChain with Azure Database for PostgreSQL
description: Integrate Azure Database for PostgreSQL with AI and LangChain, so that you can use advanced AI capabilities in your applications.
author: abeomor
ms.author: abeomorogbe
ms.date: 03/31/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.collection: ce-skilling-ai-copilot
ms.custom:
  - build-2025
ms.topic: how-to
---

# Use LangChain with Azure Database for PostgreSQL

Azure Database for PostgreSQL seamlessly integrates with leading large language model (LLM) orchestration packages such as [LangChain](https://www.langchain.com/). This integration enables developers use advanced AI capabilities in their applications. LangChain can streamline the management and use of LLMs, embedding models, and databases so that generative AI applications are easier to develop.

This article shows you how to use the integrated [vector database](how-to-use-pgvector.md) in Azure Database for PostgreSQL to store and manage documents in collections with LangChain. It also shows you how to create indices and perform vector search queries by using nearest-neighbor algorithms such as cosine distance, L2 distance (Euclidean distance), and inner product to locate documents close to the query vectors.

## Vector support

You can use Azure Database for PostgreSQL to efficiently store and query millions of vector embeddings in PostgreSQL. It can help you scale your AI use cases from proof of concept to production. The service:

- Provides a familiar SQL interface for querying vector embeddings and relational data.
- Boosts `pgvector` with a faster and more precise similarity search across more than 100 million vectors by using the [DiskANN indexing algorithm](https://aka.ms/pg-diskann-docs).
- Simplifies operations by integrating relational metadata, vector embeddings, and time-series data into a single database.
- Uses the power of the robust PostgreSQL ecosystem and the Azure cloud platform for enterprise-grade features, including replication and high availability.

## Authentication

Azure Database for PostgreSQL supports password-based and [Microsoft Entra](concepts-azure-ad-authentication.md) (formerly Azure Active Directory) authentication.

Microsoft Entra authentication allows you to use Microsoft Entra ID to authenticate to your PostgreSQL server. Microsoft Entra ID eliminates the need to manage separate usernames and passwords for your database users. It allows you to use the same security mechanisms that you use for other Azure services.

In this article, you can use either authentication method.

## Setup

Azure Database for PostgreSQL uses the open-source [LangChain Postgres support](https://python.langchain.com/docs/integrations/vectorstores/pgvector/) to connect to Azure Database for PostgreSQL. First, download the partner package:

```python
%pip install -qU langchain_postgres
%pip install -qU langchain-openai
%pip install -qU azure-identity
```

### Enable pgvector on Azure Database for PostgreSQL

For information about enabling pgvector, see [Enable and use pgvector in Azure Database for PostgreSQL](how-to-use-pgvector.md).

### Set up credentials

You need your Azure Database for PostgreSQL [connection details](quickstart-create-server-portal.md#get-the-connection-information) and add them as environment variables in the following commands.

Set the `USE_ENTRA_AUTH` flag to `True` if you want to use Microsoft Entra authentication. If you're using Microsoft Entra authentication, you need to supply the only host and database names. If you're using password authentication, you also need to set the username and password.

```python
import getpass
import os

USE_ENTRA_AUTH = True

# Supply the connection details for the database
os.environ["DBHOST"] = "<server-name>"
os.environ["DBNAME"] = "<database-name>"
os.environ["SSLMODE"] = "require"

if not USE_ENTRA_AUTH:
    # If you're using a username and password, supply them here
    os.environ["DBUSER"] = "<username>"
    os.environ["DBPASSWORD"] = getpass.getpass("Database Password:")
```

### Set up Azure OpenAI embeddings

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

### Use Microsoft Entra authentication

The following sections contain functions that set up LangChain to use Microsoft Entra authentication. The function `get_token_and_username` retrieves tokens for the Azure Database for PostgreSQL service by using `DefaultAzureCredential` from the `azure.identity` library. It ensures that the SQLAlchemy engine has a valid token with which to create new connections. It also parses the token, which is a Java Web Token (JWT), to extract the username that's used to connect to the database.

The `create_postgres_engine` function creates a SQLAlchemy engine that dynamically sets the username and password based on the token fetched from the token manager. This engine can be passed into the `connection` parameter of the `PGVector` LangChain vector store.

#### Sign in to Azure

To sign in to Azure, ensure that you have the [Azure CLI](/cli/azure/install-azure-cli) installed. Run the following command in your terminal:

``` bash
az login
```

After you sign in, the following code fetches the token:

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
    """Fetches a token and returns the username and token."""
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

    # Create a SQLAlchemy engine
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

### Use password authentication

If you're not using Microsoft Entra authentication, `get_connection_uri` provides a connection URI that pulls the username and password from environment variables:

``` python
import urllib.parse


def get_connection_uri():
    # Read URI parameters from the environment
    dbhost = os.environ["DBHOST"]
    dbname = os.environ["DBNAME"]
    dbuser = urllib.parse.quote(os.environ["DBUSER"])
    password = os.environ["DBPASSWORD"]
    sslmode = os.environ["SSLMODE"]

    # Construct the connection URI
    # Use Psycopg 3!
    db_uri = (
        f"postgresql+psycopg://{dbuser}:{password}@{dbhost}/{dbname}?sslmode={sslmode}"
    )
    return db_uri
```

### Create the vector store

``` python
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector

collection_name = "my_docs"

# The connection is either a SQLAlchemy engine or a connection URI
connection = create_postgres_engine() if USE_ENTRA_AUTH else get_connection_uri()

vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)
```

## Management of the vector store

### Add items to the vector store

Adding documents by ID overwrites any existing documents that match that ID.

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

### Update items in the vector store

``` python
docs = [
    Document(
        page_content="Updated - cooking class for beginners is offered at the community center",
        metadata={"id": 10, "location": "community center", "topic": "classes"},
    )
]
vector_store.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])
```

### Delete items from the vector store

``` python
vector_store.delete(ids=["3"])
```

## Queries to the vector store

After you create your vector store and add the relevant documents, you can query the vector store in your chain or agent.

### Filtering support

The vector store supports a set of filters that can be applied against the metadata fields of the documents:

| Operator | Meaning/Category                |
| -------- | ------------------------------- |
| `$eq`      | Equality (==)                   |
| `$ne`      | Inequality (!=)                 |
| `$lt`      | Less than (<)                   |
| `$lte`     | Less than or equal (<=)         |
| `$gt`      | Greater than (>)                |
| `$gte`     | Greater than or equal (>=)      |
| `$in`      | Special cased (in)              |
| `$nin`     | Special cased (not in)          |
| `$between` | Special cased (between)         |
| `$like`    | Text (like)                     |
| `$ilike`   | Text (case-insensitive like)    |
| `$and`     | Logical (and)                   |
| `$or`      | Logical (or)                    |

### Direct query

You can perform a simple similarity search as follows:

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

If you provide a dictionary with multiple fields but no operators, the top level is interpreted as a logical `AND` filter:

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

If you want to execute a similarity search and receive the corresponding scores, you can run:

``` python
results = vector_store.similarity_search_with_score(query="cats", k=1)
for doc, score in results:
    print(f"* [SIM={score:3f}] {doc.page_content} [{doc.metadata}]")
```

```shell
* [SIM=0.528338] there are cats in the pond [{'id': 1, 'topic': 'animals', 'location': 'pond'}]
```

For a full list of the searches that you can execute on a `PGVector` vector store, refer to the [API reference](https://python.langchain.com/api_reference/postgres/vectorstores/langchain_postgres.vectorstores.PGVector.html).

### Transformation into a retriever

You can also transform the vector store into a retriever for easier usage in your chains:

``` python
retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 1})
retriever.invoke("kitty")
```

```shell
[Document(id='1', metadata={'id': 1, 'topic': 'animals', 'location': 'pond'}, page_content='there are cats in the pond')]
```

## Current limitations

- `langchain_postgres` works only with Psycopg 3 (`psycopg3`). Update your connection strings from `postgresql+psycopg2://...` to `postgresql+psycopg://langchain:langchain@...`.
- The schema of the embedding store and collection changed to make `add_documents` work correctly with user specified IDs.
- You have to pass an explicit connection object now.

Currently, no mechanism supports easy data migration on schema changes. Any schema changes in the vector store require you to re-create the tables and add the documents again.

## Related content

- [LangChain PGVector reference](https://python.langchain.com/docs/integrations/vectorstores/pgvector/)
- [Generative AI Frameworks and Azure Database for PostgreSQL](generative-ai-frameworks.md)
- [AI agents in Azure Database for PostgreSQL](generative-ai-agents.md)
- [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL](generative-ai-azure-openai.md)
- [Generative AI with Azure Database for PostgreSQL](generative-ai-overview.md)
- [Enable and use pgvector in Azure Database for PostgreSQL](how-to-use-pgvector.md)
