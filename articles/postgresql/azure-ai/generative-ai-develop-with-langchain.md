---
title: Use LangChain with Azure Database for PostgreSQL
description: Integrate Azure Database for PostgreSQL with AI and LangChain, so that you can use advanced AI capabilities in your applications.
author: abeomor
ms.author: abeomorogbe
ms.reviewer: maghan
ms.date: 01/20/2026
ms.service: azure-database-postgresql
ms.subservice: ai-frameworks
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2025
---

# Use LangChain with Azure Database for PostgreSQL

Azure Database for PostgreSQL seamlessly integrates with leading large language model (LLM) orchestration packages such as [LangChain](https://www.langchain.com/). This integration enables developers to use advanced AI capabilities in their applications. LangChain can streamline the management and use of LLMs, embedding models, and databases so that generative AI applications are easier to develop.

This article shows you how to use the integrated [vector database](../extensions/../extensions/how-to-use-pgvector.md) in Azure Database for PostgreSQL to store and manage documents in collections with LangChain. It also shows you how to create indices and perform vector search queries by using nearest-neighbor algorithms such as cosine distance, L2 distance (Euclidean distance), and inner product to locate documents close to the query vectors.

## Vector support

You can use Azure Database for PostgreSQL to efficiently store and query millions of vector embeddings in PostgreSQL. The service can help you scale your AI use cases from proof of concept to production. It offers these benefits:

- Provides a familiar SQL interface for querying vector embeddings and relational data.
- Boosts `pgvector` with a faster and more precise similarity search across more than 100 million vectors by using the [DiskANN indexing algorithm](https://aka.ms/pg-diskann-docs).
- Simplifies operations by integrating relational metadata, vector embeddings, and time-series data into a single database.
- Uses the power of the robust PostgreSQL ecosystem and the Azure cloud platform for enterprise-grade features, including replication and high availability.

## Authentication

Azure Database for PostgreSQL supports password-based and [Microsoft Entra](../security/security-entra-concepts.md) (formerly Azure Active Directory) authentication.

Microsoft Entra authentication allows you to use Microsoft Entra ID to authenticate to your PostgreSQL server. Microsoft Entra ID eliminates the need to manage separate usernames and passwords for your database users. It allows you to use the same security mechanisms that you use for other Azure services.

In this article, you can use either authentication method.

## Setup

Azure Database for PostgreSQL uses the open-source [LangChain Postgres support](https://python.langchain.com/docs/integrations/vectorstores/pgvector/) to connect to Azure Database for PostgreSQL. First, download the partner package:

```python
%pip install -qU langchain-azure-postgresql
%pip install -qU langchain-openai
%pip install -qU azure-identity
```

### Enable pgvector on Azure Database for PostgreSQL

See [Enable and use pgvector in Azure Database for PostgreSQL](../extensions/../extensions/how-to-use-pgvector.md).

### Set up credentials

You need to get your Azure Database for PostgreSQL [connection details](../configure-maintain/quickstart-create-server.md) and add them as environment variables.

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

The following sections demonstrate how to set up LangChain to use Microsoft Entra authentication. The class `AzurePGConnectionPool` in the LangChain Azure Postgres package retrieves tokens for the Azure Database for PostgreSQL service by using `DefaultAzureCredential` from the `azure.identity` library.

The connection can be passed into the `connection` parameter of the `AzurePGVectorStore` LangChain vector store.

#### Sign in to Azure

To sign in to Azure, ensure that you have the [Azure CLI](/cli/azure/install-azure-cli) installed. Run the following command in your terminal:

``` bash
az login
```

After you sign in, the following code fetches the token:

``` python
from langchain_azure_postgresql.common import (
    BasicAuth,
    AzurePGConnectionPool,
    ConnectionInfo,
)
from langchain_azure_postgresql.langchain import AzurePGVectorStore
entra_connection_pool = AzurePGConnectionPool(
        azure_conn_info=ConnectionInfo(
            host=os.environ["DBHOST"],
            dbname=os.environ["DBNAME"]
        )
    )
```

### Use password authentication

If you're not using Microsoft Entra authentication, the `BasicAuth` class allows the use of username and password:

``` python
basic_auth_connection_pool = AzurePGConnectionPool(
    azure_conn_info=ConnectionInfo(
        host=os.environ["DBHOST"],
        dbname=os.environ["DBNAME"],
        credentials=BasicAuth(
            username=os.environ["DBUSER"],
            password=os.environ["DBPASSWORD"],
        )
    )
)
```

### Create the vector store

``` python
from langchain_core.documents import Document
from langchain_azure_postgresql.langchain import AzurePGVectorStore

collection_name = "my_docs"

# The connection is either using Entra ID or Basic Auth
connection = entra_connection_pool if USE_ENTRA_AUTH else basic_auth_connection_pool

vector_store = AzurePGVectorStore(
    embeddings=embeddings,
    table_name=table_name,
    connection=connection,
)
```

## Management of the vector store

### Add items to the vector store

Adding documents by ID overwrites any existing documents that match that ID.

``` python
docs = [
    Document(
        page_content="there are cats in the pond",
        metadata={"doc_id": 1, "location": "pond", "topic": "animals"},
    ),
    Document(
        page_content="ducks are also found in the pond",
        metadata={"doc_id": 2, "location": "pond", "topic": "animals"},
    ),
    Document(
        page_content="fresh apples are available at the market",
        metadata={"doc_id": 3, "location": "market", "topic": "food"},
    ),
    Document(
        page_content="the market also sells fresh oranges",
        metadata={"doc_id": 4, "location": "market", "topic": "food"},
    ),
    Document(
        page_content="the new art exhibit is fascinating",
        metadata={"doc_id": 5, "location": "museum", "topic": "art"},
    ),
    Document(
        page_content="a sculpture exhibit is also at the museum",
        metadata={"doc_id": 6, "location": "museum", "topic": "art"},
    ),
    Document(
        page_content="a new coffee shop opened on Main Street",
        metadata={"doc_id": 7, "location": "Main Street", "topic": "food"},
    ),
    Document(
        page_content="the book club meets at the library",
        metadata={"doc_id": 8, "location": "library", "topic": "reading"},
    ),
    Document(
        page_content="the library hosts a weekly story time for kids",
        metadata={"doc_id": 9, "location": "library", "topic": "reading"},
    ),
    Document(
        page_content="a cooking class for beginners is offered at the community center",
        metadata={"doc_id": 10, "location": "community center", "topic": "classes"},
    ),
]

uuids = vector_store.add_documents(docs)
uuids
```

### Update items in the vector store

``` python
updated_docs = [
    Document(
        page_content="Updated - cooking class for beginners is offered at the community center",
        metadata={"doc_id": 10, "location": "community center", "topic": "classes"},
        id=uuids[-1],
    )
]
vector_store.add_documents(docs, ids=[uuids[-1]], on_conflict_update=True)
```

### See items from the vector store

``` python
vector_store.get_by_ids([str(uuids[-1])])
```

### Delete items from the vector store

``` python
vector_store.delete(ids=[uuids[-1]])
```

## Queries to the vector store

After you create your vector store and add the relevant documents, you can query the vector store in your chain or agent.

### Filtering support

The vector store supports a set of filters that can be applied against the metadata fields of the documents via the `FilterCondition`, `OrFilter`, and `AndFilter` in the [LangChain Azure PostgreSQL](https://pypi.org/project/langchain-azure-postgresql/) package:

| Operator | Meaning/Category |
| --- | --- |
| `=` | Equality (==) |
| `!=` | Inequality (!=) |
| `<` | Less than (<) |
| `<=` | Less than or equal (<=) |
| `>` | Greater than (>) |
| `>=` | Greater than or equal (>=) |
| `in` | Special cased (in) |
| `not in` | Special cased (not in) |
| `is null` | Special cased (is null) |
| `is not null` | Special cased (is not null) |
| `between` | Special cased (between) |
| `not between` | Special cased (not between) |
| `like` | Text (like) |
| `ilike` | Text (case-insensitive like) |
| `AND` | Logical (and) |
| `OR` | Logical (or) |

### Direct query

You can perform a simple similarity search as follows:

``` python
from langchain_azure_postgresql import FilterCondition, AndFilter

results = vector_store.similarity_search(
    "kitty",
    k=10,
    filter=FilterCondition(
        column="(metadata->>'doc_id')::int",
        operator="in",
        value=[1, 5, 2, 9],
    ),
)

for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")
```

```shell
    * there are cats in the pond [{'doc_id': 1, 'topic': 'animals', 'location': 'pond'}]
    * ducks are also found in the pond [{'doc_id': 2, 'topic': 'animals', 'location': 'pond'}]
    * the new art exhibit is fascinating [{'doc_id': 5, 'topic': 'art', 'location': 'museum'}]
    * the library hosts a weekly story time for kids [{'doc_id': 9, 'topic': 'reading', 'location': 'library'}]
```

If you provide a dictionary with multiple fields but no operators, the top level is interpreted as a logical `AND` filter:

``` python
results = vector_store.similarity_search(
    "ducks",
    k=10,
    filter=AndFilter(
        AND=[
            FilterCondition(
                column="(metadata->>'doc_id')::int",
                operator="in",
                value=[1, 5, 2, 9],
            ),
            FilterCondition(
                column="metadata->>'location'",
                operator="in",
                value=["pond", "market"],
            ),
        ]
    ),
)

for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")
```

```shell
    * ducks are also found in the pond [{'topic': 'animals', 'doc_id': 2, 'location': 'pond'}]
    * there are cats in the pond [{'topic': 'animals', 'doc_id': 1, 'location': 'pond'}]
```

If you want to execute a similarity search and receive the corresponding scores, you can run:

``` python
results = vector_store.similarity_search_with_score(query="cats", k=1)
for doc, score in results:
    print(f"* [SIM={score:3f}] {doc.page_content} [{doc.metadata}]")
```

```shell
* [SIM=0.528338] there are cats in the pond [{'doc_id': 1, 'topic': 'animals', 'location': 'pond'}]
```

If you want to use max marginal relevance search on your vector store:

``` python
results = vector_store.max_marginal_relevance_search(
    "query about cats",
    k=10,
    lambda_mult=0.5,
    filter=FilterCondition(
        column="(metadata->>'doc_id')::int",
        operator="in",
        value=[1, 2, 5, 9],
    ),
)

for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")
```

```shell
    * there are cats in the pond [{'doc_id': 1, 'topic': 'animals', 'location': 'pond'}]
    * ducks are also found in the pond [{'doc_id': 2, 'topic': 'animals', 'location': 'pond'}]
    * the new art exhibit is fascinating [{'doc_id': 5, 'topic': 'art', 'location': 'museum'}]
    * the library hosts a weekly story time for kids [{'doc_id': 9, 'topic': 'reading', 'location': 'library'}]
```

For a full list of the searches that you can execute on a `PGVector` vector store, refer to the [API reference](https://python.langchain.com/api_reference/postgres/vectorstores/langchain_postgres.vectorstores.PGVector.html).

### Transformation into a retriever

You can also transform the vector store into a retriever for easier usage in your chains:

``` python
retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 1})
retriever.invoke("kitty")
```

```shell
[Document(id='9fe8bc1c-9a8e-4f83-b546-9b64527aa79d', metadata={'doc_id': 1, 'topic': 'animals', 'location': 'pond'}, page_content='there are cats in the pond')]
```

## Related content

- [LangChain AzurePGVectorStore reference](https://pypi.org/project/langchain-azure-postgresql/)
- [Azure Database for PostgreSQL integrations for AI applications](generative-ai-frameworks.md)
- [AI agents in Azure Database for PostgreSQL](generative-ai-agents.md)
- [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL](generative-ai-azure-openai.md)
- [Generative AI with Azure Database for PostgreSQL](generative-ai-overview.md)
- [Enable and use pgvector in Azure Database for PostgreSQL](../extensions/../extensions/how-to-use-pgvector.md)
