---
title: Vector search on Azure Database for PostgreSQL
description: Enable semantic similarity search for Retrieval Augmented Generation (RAG) on Azure Database for PostgreSQL with pgvector database extension.
author: AvijitkGupta
ms.author: avijitgupta
ms.reviewer: kabharati, maghan
ms.date: 04/27/2024
ms.update-cycle: 180-days
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
ms.collection: ce-skilling-ai-copilot
ms.custom:
  - build-2023
  - ignite-2023
ai-usage: ai-assisted
---

# Enable and use pgvector in Azure Database for PostgreSQL 

[!INCLUDE [Introduction to `pgvector`](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-introduction.md)]

## Enable extension

Before you can enable `pgvector` on your Azure Database for PostgreSQL flexible server instance, you need to add it to your allowlist as described in [how to use PostgreSQL extensions](../extensions/how-to-allow-extensions.md#allow-extensions), and check if correctly added by running `SHOW azure.extensions;`.

> [!IMPORTANT]
> Notice that although all PostgreSQL community tends to refer to this extension as pgvector, the name of the binary and the extension itself is simply `vector`. Take that into consideration, because that is the name you must use to allowlist it or to create it on any database via the CREATE EXTENSION command.

Then you can install the extension, by connecting to your target database and running the [CREATE EXTENSION](https://www.postgresql.org/docs/current/static/sql-createextension.html) command. You need to repeat the command separately for every database you want the extension to be available in.

```sql
CREATE EXTENSION vector;
```

> [!Note]
> To remove the extension from the currently connected database use `DROP EXTENSION vector;`.

[!INCLUDE [`pgvector`](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-basics.md)]

## Preprocess documents before embedding

For complex source documents such as PDFs, scanned files, board packets, or forms, use [Azure Document Intelligence](/azure/ai-services/document-intelligence/overview) to extract and normalize text before chunking and embedding. Azure Document Intelligence parses layout, tables, and key fields to produce structured content that improves the quality of embeddings and downstream retrieval.

A typical workflow:

1. Call Azure Document Intelligence to parse and normalize document content.
1. Persist the cleaned text and relevant metadata in a PostgreSQL table.
1. Generate embeddings with `azure_openai.create_embeddings()` and store them in a `vector` column for retrieval.

This approach improves accuracy for summarization and minutes-generation scenarios.

## Hybrid SQL–vector search

You can combine pgvector similarity with standard SQL filters to perform hybrid retrieval—restricting results by structured metadata while ranking by semantic distance. This pattern is common in RAG applications. Select the distance operator that matches the embedding model you use:

- `<->` or `l2_distance` for Euclidean (L2) distance—smaller values indicate greater similarity.
- `<=>` or `cosine_distance` for cosine distance—smaller values indicate greater similarity.
- `<#>` for negative inner product—used with normalized vectors.

The following example combines a metadata filter with cosine distance ordering. Replace the query vector with a call to `azure_openai.create_embeddings()` as shown in [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL](../azure-ai/generative-ai-azure-openai.md):

```sql
SELECT doc_id, title, summary
FROM documents
WHERE document_type = 'board_packet'
  AND meeting_date BETWEEN '2024-01-01' AND '2024-12-31'
ORDER BY embedding <=> azure_openai.create_embeddings('{your-deployment-name}', 'quarterly earnings summary')::vector
LIMIT 10;
```

## Indexing for vector search

Create an index on the embedding column to make vector similarity queries more efficient at scale. The following example creates an IVFFLAT index on a `vector` column:

```sql
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

Before running similarity queries, set the number of probes to balance recall and performance:

```sql
SET ivfflat.probes = 10;
```

For guidance on tuning IVFFLAT index parameters and HNSW indexes for your workload, see [Optimize performance when using pgvector in Azure Database for PostgreSQL flexible server](how-to-optimize-performance-pgvector.md).

## Related content

- [Optimize performance when using pgvector in Azure Database for PostgreSQL flexible server](how-to-optimize-performance-pgvector.md).
- [Integrate Azure Database for PostgreSQL flexible server with Azure Cognitive Services](../azure-ai/generative-ai-azure-cognitive.md).
- [Generate vector embeddings in Azure Database for PostgreSQL flexible server with locally deployed LLM (Preview)](../azure-ai/generative-ai-overview.md).
- [Integrate Azure Database for PostgreSQL with Azure Machine Learning Services](../azure-ai/generative-ai-azure-machine-learning.md).
- [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL flexible server](../azure-ai/generative-ai-azure-openai.md).
- [Azure AI extension in Azure Database for PostgreSQL flexible server](../azure-ai/generative-ai-azure-overview.md).
- [Generative AI with Azure Database for PostgreSQL flexible server](../azure-ai/generative-ai-overview.md).
- [Recommendation System with Azure Database for PostgreSQL flexible server and Azure OpenAI](../azure-ai/generative-ai-recommendation-system.md).
- [Semantic Search with Azure Database for PostgreSQL flexible server and Azure OpenAI](../azure-ai/generative-ai-semantic-search.md).
- [Enable and use pgvector in Azure Database for PostgreSQL flexible server](how-to-use-pgvector.md).
