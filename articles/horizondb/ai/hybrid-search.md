---
title: Hybrid Search in Azure HorizonDB
description: Combine BM25 full-text search with pgvector and DiskANN vector search in Azure HorizonDB to get keyword precision plus semantic recall, fused with Reciprocal Rank Fusion.
author: abeomor
ms.author: abeomorogbe
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: ai-vector-search
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
ai-usage: ai-assisted
# customer intent: As a developer building retrieval on Azure HorizonDB, I want to combine keyword and vector search so that I get accurate results across exact-match and semantic queries.
---

# Hybrid search in Azure HorizonDB (Preview)

Hybrid search combines two retrieval strategies in a single query:

- **BM25 full-text search** with [Full-text search with pg_fts in Azure HorizonDB (Preview)](full-text-search.md) - strong on exact terms, product codes, error messages, named entities, and any query where the user typed words that should literally appear in the result.
- **Vector similarity search** with [Implement vector search in Azure HorizonDB using the pgvector extension (Preview)](vector-search-pgvector.md) and [Scalable vector indexing with DiskANN (Preview)](vector-indexing-diskann.md) - strong on synonyms, paraphrases, and semantic intent where the right document doesn't share the user's exact words.

Used alone, each method has blind spots. Used together, they cover for each other. Hybrid search is the default retrieval pattern for production AI applications on Azure HorizonDB - agentic apps, knowledge bases, recommendation engines, support search, and RAG over enterprise content.

This article shows you how to build hybrid search end to end inside HorizonDB, without copying data to a separate search service.

## Why hybrid wins

A query like `"connection timeout error PG-4012"` has two signals:

- The literal token `PG-4012` is a precise identifier - vector search likely can miss it because the embedding model has never seen it.
- The phrase `"connection timeout error"` is semantic - BM25 might match the words, but a different document phrased as `"the database stopped responding after the network dropped"` is a better answer that BM25 won't surface.

Pure vector search misses the first signal. Pure BM25 misses the second. Hybrid search returns a single ranked list that surfaces both. The boost is largest exactly where customers care most: enterprise-specific terminology, product names, error codes, multitenant filtered queries, and any corpus where a phrase can mean two different things.

## How hybrid search works on HorizonDB

A hybrid query has three logical steps, all of which run inside HorizonDB:

1. **Run BM25** with `pg_fts` to get the top-N keyword matches.
1. **Run vector search** with `pgvector` (using DiskANN as the index) to get the top-N semantic matches.
1. **Fuse the two ranked lists** into a single ordered result set.

Optionally, a fourth step:

1. **Re-rank the top-K** of the fused list with a cross-encoder model using [`azure_ai.rank()`](ai-functions.md#azure_airank) for a final accuracy bump on the documents that will actually be shown to the user.

Everything happens in a single SQL query. There's no copy-syncing to an external search index, no application-side join, and no separate vector database.

## Reciprocal Rank Fusion (RRF)

The standard way to combine BM25 and vector results is **Reciprocal Rank Fusion**. RRF ignores the raw score of each ranker (which are on incompatible scales) and uses only the **rank** each document achieves in each list.

The constant `k` (commonly 60) prevents the top-1 document from dominating. Documents that appear high in both rankers naturally float to the top. Documents that appear in only one ranker still contribute, just with a lower combined score.

RRF is the right default because:

- It needs no tuning - `k = 60` is a well-known good choice.
- It's robust to score-scale differences across rankers.
- It composes naturally with more than two rankers (for example, graph search and structured filters).

## Prerequisites

Enable the extensions you need on your database:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_diskann CASCADE;
CREATE EXTENSION IF NOT EXISTS pg_fts;
CREATE EXTENSION IF NOT EXISTS azure_ai;
```

For instructions on enabling extensions at the instance level, see [Allow extensions in Azure HorizonDB](../extensions/how-to-allow-extensions.md).

> [!TIP]  
> If you have [AI Model Management in Azure HorizonDB (Preview)](ai-model-management.md) enabled, the `azure_ai` extension is already installed and configured with a `default-embedding` model. You can skip the `CREATE EXTENSION azure_ai` step and omit the model alias in AI function calls.

## Set up the table and indexes

Use a single table for both retrieval methods. Storing embeddings, content, and metadata together is a key advantage of doing this in HorizonDB instead of a separate search service - you keep transactional consistency and avoid sync drift.

```sql
CREATE TABLE products (
    id          INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT NOT NULL,
    category    TEXT NOT NULL,
    embedding   public.vector(1536)
);

-- BM25 index over the searchable text columns
CREATE INDEX idx_products_fts
    ON products
    USING fts (name, description);

-- DiskANN vector index for semantic search
CREATE INDEX idx_products_vec
    ON products
    USING diskann (embedding vector_cosine_ops);
```

> [!TIP]  
> DiskANN is the recommended vector index for hybrid search workloads because it supports [advanced filtering](vector-indexing-diskann.md#filter-your-search-with-advanced-filtering) - you can combine `WHERE` clauses on metadata with vector similarity without losing recall.

## Generate embeddings in SQL

You can generate embeddings inside Postgres using the [AI functions in the azure_ai extension for Azure HorizonDB (Preview)](ai-functions.md). This eliminates the embedding pipeline entirely - no external service calls in your application code.

If you have [AI Model Management in Azure HorizonDB (Preview)](ai-model-management.md) enabled, you can omit the model parameter - the function automatically uses the `default-embedding` model (`text-embedding-3-small`). If you're using your own model (BYOM), pass your registered model alias as the first argument. See [AI functions in the azure_ai extension for Azure HorizonDB (Preview)](ai-functions.md) for details on registering models.

```sql
-- Backfill embeddings for existing rows
UPDATE products
SET embedding = azure_openai.create_embeddings(
    'default-embedding', -- model alias (omit if using AI Model Management)
    name || ' ' || description
)::vector
WHERE embedding IS NULL;
```

> [!NOTE]  
> **AI Model Management users:** You can simplify the call to `azure_openai.create_embeddings(input => name || ' ' || description)` - the `default-embedding` model is used automatically.

For an end-to-end embedding workflow including durable batch processing for large tables, see [Generate vector embeddings using the create_embeddings() AI function (Preview)](generate-vector-embeddings.md) and [Implement durable AI pipelines in Azure HorizonDB (Preview)](ai-pipelines.md).

## Run a hybrid search query

The complete hybrid search query: BM25 + vector search + RRF fusion in a single statement.

```sql
WITH
-- Embed the query once and reuse it
query AS (
    SELECT
        'wireless noise cancelling headphones' AS q_text,
        azure_openai.create_embeddings(
            'my-embedding',                          -- model alias (omit if using AI Model Management)
            'wireless noise cancelling headphones'
        )::vector AS q_vec
),
-- Top-N BM25 results, ranked by relevance
bm25 AS (
    SELECT id,
           ROW_NUMBER() OVER () AS bm25_rank
    FROM products, query
    WHERE pgfts.fts_query(query.q_text, 'idx_products_fts')
    LIMIT 50
),
-- Top-N vector results, ranked by cosine distance
vec AS (
    SELECT p.id,
           ROW_NUMBER() OVER (
               ORDER BY p.embedding <=> query.q_vec
           ) AS vec_rank
    FROM products p, query
    ORDER BY p.embedding <=> query.q_vec
    LIMIT 50
)
-- Reciprocal Rank Fusion
SELECT p.id, p.name, p.description,
       (1.0 / (60 + COALESCE(b.bm25_rank, 1000))) +
       (1.0 / (60 + COALESCE(v.vec_rank, 1000))) AS rrf_score
FROM products p
LEFT JOIN bm25 b ON b.id = p.id
LEFT JOIN vec  v ON v.id = p.id
WHERE b.id IS NOT NULL OR v.id IS NOT NULL
ORDER BY rrf_score DESC
LIMIT 10;
```

A few things to note:

- The query embedding is generated **once** in the `query` CTE and reused - saving you a round-trip per ranker.
- Each ranker pulls its own top-50; RRF then keeps the top-10 of the fusion. Tune the inner `LIMIT` (the candidate pool) and the outer `LIMIT` (the result count) independently.
- `LEFT JOIN` keeps documents that appear in only one ranker. The `COALESCE(..., 1000)` gives them a low contribution rather than dropping them.
- The constant `60` is the standard RRF `k`. You rarely need to change it.

## Combine hybrid search with metadata filters

Because everything is in HorizonDB, you can apply a structured `WHERE` filter at the same time as similarity ranking. With DiskANN advanced filtering, the predicate is pushed into the vector index - so adding `WHERE category = 'audio'` doesn't collapse recall.

```sql
WITH query AS (
    SELECT
        'noise cancelling for travel' AS q_text,
        azure_openai.create_embeddings(
            'default-embedding',                          -- model alias (omit if using AI Model Management)
            'noise cancelling for travel'
        )::vector AS q_vec
),
bm25 AS (
    SELECT id, ROW_NUMBER() OVER () AS bm25_rank
    FROM products, query
    WHERE category = 'audio'
      AND pgfts.fts_query(query.q_text, 'idx_products_fts')
    LIMIT 50
),
vec AS (
    SELECT p.id, ROW_NUMBER() OVER (ORDER BY p.embedding <=> query.q_vec) AS vec_rank
    FROM products p, query
    WHERE p.category = 'audio'
    ORDER BY p.embedding <=> query.q_vec
    LIMIT 50
)
SELECT p.id, p.name,
       (1.0 / (60 + COALESCE(b.bm25_rank, 1000))) +
       (1.0 / (60 + COALESCE(v.vec_rank, 1000))) AS rrf_score
FROM products p
LEFT JOIN bm25 b ON b.id = p.id
LEFT JOIN vec  v ON v.id = p.id
WHERE (b.id IS NOT NULL OR v.id IS NOT NULL)
ORDER BY rrf_score DESC
LIMIT 10;
```

For more on filtered vector search, see [Filter your search with advanced filtering](vector-indexing-diskann.md#filter-your-search-with-advanced-filtering).

## Add a semantic reranker for the final accuracy bump

RRF gives you a strong ranked list cheaply. For the documents that will actually be shown to a user or fed to an LLM, a **cross-encoder reranker** can push relevance higher still, at the cost of one model call per candidate.

The pattern:

1. Run hybrid search and take the top 50 from RRF.
1. Pass those 50 candidates plus the original query through a reranker model.
1. Return the reranker's top 10.

For the full reranking pattern using the `azure_ai.rank()` function, see [Semantic reranking with the rank() function (Preview)](semantic-rank-function.md).

## When *not* to use hybrid search

Hybrid search adds two index scans and a fusion step. It's not free. Reach for pure BM25 or pure vector search when:

- Your queries are unambiguously keyword (product code lookup, log search, code search). Pure BM25 is faster and as accurate.
- Your queries are unambiguously semantic over a small homogeneous corpus (FAQ retrieval over a few thousand answers). Pure vector search with DiskANN is enough.
- Your application latency budget is below the combined cost of two index scans and you can validate that one ranker alone meets your relevance bar.

For mixed real-world queries - which is most production retrieval - hybrid is the right default.

## Performance notes

- **Latency.** Each ranker runs an independent index scan. With DiskANN and `pg_fts` both retrieving 50 candidates, hybrid search typically lands in the low double-digit milliseconds on millions of rows. The reranker step adds tens to low hundreds of milliseconds depending on the candidate pool.
- **Candidate pool size.** Pulling 50 from each ranker and keeping 10 after RRF is a good default. Increasing the inner `LIMIT` improves recall at a small latency cost; raise it before tuning RRF's `k`.
- **Index updates.** Both `pg_fts` and DiskANN apply inserts and updates in place. There's no cron job or refresh step.
- **Embeddings.** Generate query embeddings once per request and reuse them across rankers, as shown in the SQL above.

## Related content

- [Retrieval foundations: vector, full-text, and hybrid search in Azure HorizonDB (Preview)](ai-search-overview.md)
- [Full-text search with pg_fts in Azure HorizonDB (Preview)](full-text-search.md)
- [Semantic reranking with the rank() function (Preview)](semantic-rank-function.md)
