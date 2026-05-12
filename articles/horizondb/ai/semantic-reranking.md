---
title: Semantic reranking with the rank() function
description: Understand why semantic reranking improves search relevance, and use the azure_ai.rank() function to add a cross-encoder reranking stage to vector, full-text, or hybrid search in Azure HorizonDB.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: ai-semantic-operators
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.custom:
  - build-2026
# customer intent: As a user, I want to understand why and how to perform semantic reranking for vector search in Azure HorizonDB.
---

# Semantic reranking with the rank() function

Vector search retrieves results that are semantically close to a query, but "close" in embedding space doesn't always mean "relevant" to the user's intent. Synonyms, intent shifts, long-tail phrasing, and domain-specific nuance can cause the most relevant document to rank third or tenth instead of first. Users judge results by how well they match their intent, not by raw distance scores.

**Semantic reranking** addresses this. After an initial retrieval stage (vector search, full-text search, or hybrid search) returns a broad set of candidates, a **cross-encoder reranker model** rescores each candidate against the original query. Unlike embedding models that encode the query and document separately, a cross-encoder processes the query and document together, capturing fine-grained interactions between them and producing more accurate relevance scores.

The `azure_ai.rank()` function in the `azure_ai` extension brings this capability directly into SQL, so you can add a reranking stage without leaving the database.

## Why reranking matters

### The gap between distance and relevance

Vector embeddings are optimized for fast, approximate similarity at scale. They encode meaning into fixed-size vectors independently, one for the query, one for each document. This **bi-encoder** approach is efficient (you can index billions of vectors with DiskANN), but it compresses away fine-grained interactions between query and document.

A cross-encoder, by contrast, processes the query and document as a **single input pair**. It attends to every word in both, capturing token-level interactions that bi-encoders miss. The result is more accurate relevance scores, but at higher computational cost, because every candidate requires a separate inference call.

### Why not use a cross-encoder for everything?

Cross-encoders are accurate but expensive. Scoring 1 million documents with a cross-encoder at query time is impractical as it would take seconds to minutes per query. That's why production retrieval uses a **two-stage pipeline**:

1. **Stage 1: Retrieve** a broad set of candidates cheaply (vector search, BM25, or hybrid search). This narrows millions of documents down to the top 50-100.
1. **Stage 2: Rerank** only those 50-100 candidates with a cross-encoder for precision on the results that matter most.

This pattern gives you the speed of embedding-based retrieval with the accuracy of cross-encoder scoring, at a fraction of the cost of running the cross-encoder over the entire corpus.

## When to use semantic reranking

| Use reranking when | Skip reranking when |
| --- | --- |
| Search quality directly affects user experience (product search, support search, knowledge base) | Simple exact-match lookups (product code, ID search) |
| Queries are natural language with nuance, synonyms, or intent variation | The corpus is small and homogeneous enough that vector search alone achieves high precision |
| You're building RAG or [AI pipelines](ai-pipelines.md) and need the best possible context for LLM generation | Latency budget can't accommodate the additional model call |
| Hybrid search returns a fused list and you want a final accuracy bump | Results are already filtered to a small set (fewer than 5) |

## Prerequisites

An Azure HorizonDB instance with either:

- **[AI Model Management](ai-model-management.md) enabled (recommended)**: It automatically provisions a `default-reranker` model (`Cohere-rerank-v4.0-fast`) ready to use.
- **The `azure_ai` extension installed with a reranker model registered** via the model registry. See [Manual setup with model registry](ai-functions.md#option-2-manual-setup-with-model-registry).

## The rank() function

The `azure_ai.rank()` function reranks a set of documents based on their relevance to a query using a cross-encoder model.

### Syntax

```sql
azure_ai.rank(
    query text,
    document_contents text[],
    document_ids text[] DEFAULT NULL,
    model text DEFAULT NULL
)
```

### Arguments

| Argument | Type | Description |
| --- | --- | --- |
| `query` | `text` | The search query to evaluate relevance against. |
| `document_contents` | `text[]` | Array of document texts to rerank. |
| `document_ids` (optional) | `text[]` | Array of identifiers corresponding to each document. |
| `model` (optional) | `text` | Model alias registered in the model registry. When omitted, uses the `default-reranker` Managed Model (`Cohere-rerank-v4.0-fast`). |

### Return type

Returns a table with columns: `document_id`, `rank`, and `relevance_score`.

> [!NOTE]  
> **BYOM users:** Pass your registered reranker model alias as the `model` argument. For example: `azure_ai.rank('query', documents, ids, 'my-reranker')`. See [AI functions](ai-functions.md) for details on registering models.

## Basic reranking example

Rerank a set of product descriptions against a search query:

```sql
SELECT * FROM azure_ai.rank(
    'wireless noise cancelling headphones',
    ARRAY[
        'Over-ear wireless headphones with active noise cancellation and 30-hour battery life.',
        'Wired earbuds with inline microphone, no noise cancellation.',
        'Bluetooth speaker with 360-degree sound and waterproof design.',
        'Compact noise cancelling earbuds with transparency mode and wireless charging case.'
    ]
);
```

> [!NOTE]  
> **BYOM users:** Add your model alias as the last argument: `azure_ai.rank('wireless noise cancelling headphones', ARRAY[...], NULL, 'my-reranker')`.

## Two-stage retrieval: vector search + reranking

The most common pattern is to retrieve candidates with vector search, then rerank the top results for precision:

```sql
WITH candidates AS (
    SELECT id, title, description
    FROM products
    ORDER BY embedding <=> azure_openai.create_embeddings(
        input => 'wireless noise cancelling headphones'
    )::vector
    LIMIT 20
),
reranked AS (
    SELECT *
    FROM azure_ai.rank(
        'wireless noise cancelling headphones',
        ARRAY(SELECT description FROM candidates),
        ARRAY(SELECT id::text FROM candidates)
    )
)
SELECT c.id, c.title, r.rank, r.relevance_score
FROM candidates c
JOIN reranked r ON r.document_id = c.id::text
ORDER BY r.rank ASC
LIMIT 10;
```

> [!NOTE]  
> **BYOM users:** Replace `azure_openai.create_embeddings(input => 'wireless noise cancelling headphones')` with `azure_openai.create_embeddings('my-embedding', 'wireless noise cancelling headphones')` and add `'my-reranker'` as the last argument to `azure_ai.rank()`.

## Hybrid search + reranking

For the best retrieval quality, combine BM25 full-text search and vector search with Reciprocal Rank Fusion, then rerank the fused results. If you want to run this pattern as a durable, fault-tolerant workflow with automatic retries and checkpointing, see [AI pipelines](ai-pipelines.md) - which supports `ai.rank()` as a built-in pipeline step.

```sql
WITH query AS (
    SELECT
        'wireless noise cancelling headphones' AS q_text,
        azure_openai.create_embeddings(
            input => 'wireless noise cancelling headphones'
        )::vector AS q_vec
),
bm25 AS (
    SELECT id, ROW_NUMBER() OVER () AS bm25_rank
    FROM products, query
    WHERE pgfts.fts_query(query.q_text, 'idx_products_fts')
    LIMIT 50
),
vec AS (
    SELECT p.id, ROW_NUMBER() OVER (ORDER BY p.embedding <=> query.q_vec) AS vec_rank
    FROM products p, query
    ORDER BY p.embedding <=> query.q_vec
    LIMIT 50
),
fused AS (
    SELECT p.id, p.description,
           (1.0 / (60 + COALESCE(b.bm25_rank, 1000))) +
           (1.0 / (60 + COALESCE(v.vec_rank, 1000))) AS rrf_score
    FROM products p
    LEFT JOIN bm25 b ON b.id = p.id
    LEFT JOIN vec v ON v.id = p.id
    WHERE b.id IS NOT NULL OR v.id IS NOT NULL
    ORDER BY rrf_score DESC
    LIMIT 20
),
reranked AS (
    SELECT *
    FROM azure_ai.rank(
        'wireless noise cancelling headphones',
        ARRAY(SELECT description FROM fused),
        ARRAY(SELECT id::text FROM fused)
    )
)
SELECT f.id, f.description, r.rank, r.relevance_score
FROM fused f
JOIN reranked r ON r.document_id = f.id::text
ORDER BY r.rank ASC
LIMIT 10;
```

> [!NOTE]  
> **BYOM users:** Pass your model aliases to `create_embeddings()` and `rank()` as shown in previous examples.

## Performance considerations

| Factor | Recommendation |
| --- | --- |
| **Candidate pool size** | Rerank 20-50 candidates. More candidates improve recall but increase latency and cost linearly. |
| **Latency** | Cross-encoder scoring adds tens to low hundreds of milliseconds depending on the pool size and document length. |
| **Document length** | Shorter documents rerank faster. If documents are long, consider reranking over summaries or the most relevant chunk rather than the full text. |
| **When to skip** | If your retrieval stage already returns fewer than five results, reranking adds cost with diminishing accuracy gains. |

## Related content

- [AI functions in the azure_ai extension](ai-functions.md)
- [AI Model Management](ai-model-management.md)
- [Retrieval foundations: vector, full-text, and hybrid search](ai-search-overview.md)
- [Hybrid search](hybrid-search.md)
- [Implement vector search with pgvector](vector-search-pgvector.md)
- [Generate vector embeddings](generate-vector-embeddings.md)
- [AI pipelines](ai-pipelines.md)
- [Build a semantic search application](build-semantic-search-app.md)
