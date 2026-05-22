---
title: Full-Text Search with pg_fts in Azure HorizonDB
description: Use the pg_fts extension to add BM25-ranked full-text search to Azure HorizonDB for keyword-based retrieval at scale, with fuzzy matching, phrase proximity, and CJK language support.
author: abeomor
ms.author: abeomorogbe
ms.reviewer: maghan
ms.date: 06/02/2026
ai-usage: ai-assisted
ms.service: azure-database-postgresql
ms.subservice: ai-vector-search
ms.topic: how-to
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
# customer intent: As a developer building search on Azure HorizonDB, I want to add BM25 full-text search with pg_fts so that keyword queries return high-quality results at scale.
---

# Full-text search with pg_fts in Azure HorizonDB (Preview)

The `pg_fts` extension adds production-quality, BM25-ranked full-text search to Azure HorizonDB. BM25 is the same relevance algorithm used by Elasticsearch, Solr, and Azure AI Search - `pg_fts` brings it inside Postgres as a custom index, so you can do keyword search natively next to your relational data without standing up a separate search service or copy-syncing data into one.

`pg_fts` is the recommended full-text search option on HorizonDB. It works on its own, and it composes with `pgvector` and DiskANN to power [hybrid search](hybrid-search.md).

> [!NOTE]  
> `pg_fts` is in **public preview**.

## When to use pg_fts vs. built-in tsvector

PostgreSQL has had built-in full-text search through `tsvector` and `tsquery` for years. `pg_fts` doesn't replace that - it solves the cases where built-in FTS falls short:

| Need | Built-in `tsvector` + GIN | `pg_fts` |
| --- | --- | --- |
| Ranking algorithm | `ts_rank` - no term saturation, no length normalization, no native IDF | **BM25** - industry-standard ranker with all three |
| Latency at 100K+ rows on multi-keyword queries | Often hundreds of ms to seconds | Single-digit to low double-digit ms |
| Scale to billions of documents | Degrades - GIN posting lists grow large | Designed for scale via a custom index |
| Fuzzy / typo tolerance | Manual `pg_trgm` plumbing | First-class fuzzy queries |
| Phrase proximity (words within N positions) | Limited | First-class |
| CJK languages | Requires custom dictionaries | Built-in analyzers for Chinese, Japanese, Korean, Thai |

If you have a small, low-traffic search workload and you're already happy with `ts_rank`, the built-in path is fine. For anything closer to a real search experience - product catalog, support content, log search, agent retrieval - use `pg_fts`.

## Why BM25

BM25 (Best Matching 25) solves three problems that `ts_rank` doesn't:

- **Term frequency saturation.** Repeated occurrences of a keyword have diminishing returns, so a keyword-stuffed document can't dominate results.
- **Document length normalization.** A short product title that mentions "wireless headphones" outranks a 10,000-word blog post that happens to mention the same phrase once.
- **Inverse document frequency (IDF).** Common words ("the", "error") get down-weighted; rare, discriminating terms ("PG-4012", "replication") get up-weighted.

That's why every modern search engine uses BM25 (or a close variant) as its baseline. With `pg_fts`, you get the same quality without leaving Postgres.

## Enable pg_fts

To use the `pg_fts` extension, [allow the extension](../extensions/how-to-allow-extensions.md#allow-extensions-in-azure-horizondb) at the instance level, then [create the extension](../extensions/how-to-create-extensions.md) on each database where you want to use it.

```sql
CREATE EXTENSION IF NOT EXISTS pg_fts;
```

For convenient access to the functions and operators, add the `pgfts` schema to your `search_path` for the session:

```sql
SET search_path = public, pgfts;
```

To verify the install:

```sql
SELECT pgfts.hello_pg_fts();
```

To remove the extension from the current database:

```sql
DROP EXTENSION IF EXISTS pg_fts;
```

## Create a full-text search index

`pg_fts` exposes a custom index access method called `fts`. Create an index on one or more text columns:

```sql
CREATE TABLE products (
    id          INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE INDEX idx_products_fts
    ON products
    USING fts (name, description);
```

Key differences from a GIN index on `tsvector`:

- The data column stays as plain `text` - no `tsvector` column to maintain.
- The index updates automatically on `INSERT`, `UPDATE`, and `DELETE`. No `REFRESH` step.
- The index isn't visible in `pg_stat_user_indexes` the same way GIN is, because results are produced through a custom scan.

## Run searches

### Basic keyword search

`pgfts.fts_query()` is a boolean filter that names the index to search. Results come back in BM25 rank order automatically.

```sql
SELECT id, name, description
FROM products
WHERE pgfts.fts_query('wireless noise cancelling headphones', 'idx_products_fts')
LIMIT 10;
```

### Project the BM25 score

Use `pgfts.fts_score()` to surface the relevance score alongside the row. This requires `pg_fts` in `shared_preload_libraries`.

```sql
SELECT id, name, description,
       pgfts.fts_score(description) AS score
FROM products
WHERE pgfts.fts_query('wireless headphones', 'idx_products_fts')
ORDER BY score DESC
LIMIT 10;
```

### Boolean queries (AND / OR / NOT)

```sql
SELECT id, name
FROM products
WHERE pgfts.fts_query('wireless AND headphones NOT earbuds', 'idx_products_fts')
LIMIT 10;
```

### Fuzzy search for typo tolerance

Use the JSON DSL to match terms within an edit distance of 0, 1, or 2. This is how you handle real-world misspellings without bolting on `pg_trgm`.

```sql
SELECT id, name
FROM products
WHERE pgfts.fts_query(
        '{"fuzzy": {"description": {"value": "headhpones", "fuzziness": 1}}}'::jsonb,
        'idx_products_fts')
LIMIT 10;
```

### Phrase proximity

Find words that appear within N positions of each other.

```sql
-- Exact adjacent phrase
SELECT id, name
FROM products
WHERE pgfts.fts_query('"noise cancelling"~0', 'idx_products_fts');

-- Words within 5 positions of each other
SELECT id, name
FROM products
WHERE pgfts.fts_query('"wireless headphones"~5', 'idx_products_fts');
```

### The `@@?` operator

For simple, single-keyword filters on a text column, you can use the `@@?` operator directly. It does **not** support boolean syntax - use `pgfts.fts_query()` for `AND` / `OR` / `NOT`.

```sql
SELECT id, name
FROM products
WHERE description OPERATOR(pgfts.@@?) 'wireless headphones';
```

## Multi-language support

`pg_fts` ships with analyzers for major non-Latin-script languages.

| Analyzer | Language | Description |
| --- | --- | --- |
| `default` | Multiple | Simple tokenizer with lowercase filter, suitable for English and most Latin-script languages |
| `chinese` | Chinese | Jieba segmentation |
| `japanese` | Japanese | Lindera with IPADIC dictionary |
| `korean` | Korean | Lindera with mecab-ko-dic dictionary |
| `thai` | Thai | ICU4X word segmentation |

You can inspect tokenization for any analyzer with the debug helper:

```sql
SELECT *
FROM pgfts.debug_analyze_text('japanese', '{}', '東京の天気');
```

To list available analyzers:

```sql
SELECT * FROM pgfts.list_fts_analyzers();
```

## Combine pg_fts with vector search (hybrid search)

`pg_fts` is built to compose with vector search. The standard pattern is **Reciprocal Rank Fusion (RRF)**: run BM25 and vector search separately, then combine the ranks.

```sql
WITH bm25_results AS (
    SELECT id, ROW_NUMBER() OVER () AS bm25_rank
    FROM products
    WHERE pgfts.fts_query('wireless noise cancelling', 'idx_products_fts')
    LIMIT 20
),
vector_results AS (
    SELECT id,
           ROW_NUMBER() OVER (
               ORDER BY embedding <=> azure_openai.create_embeddings(
        'text-embedding-3-small',
        '<query>')::vector
           ) AS vec_rank
    FROM products
    ORDER BY embedding <=> azure_openai.create_embeddings(
        'text-embedding-3-small',
        '<query>')::vector
    LIMIT 20
)
SELECT COALESCE(b.id, v.id) AS id,
       (1.0 / (60 + COALESCE(b.bm25_rank, 999))) +
       (1.0 / (60 + COALESCE(v.vec_rank, 999))) AS rrf_score
FROM bm25_results b
FULL OUTER JOIN vector_results v ON b.id = v.id
ORDER BY rrf_score DESC
LIMIT 10;
```

For an end-to-end walkthrough - including embedding generation in SQL and adding a semantic reranker - see [Hybrid search in Azure HorizonDB (Preview)](hybrid-search.md).

## Performance notes

- **LIMIT pushdown.** The `pg_fts` custom scan pushes `LIMIT` into the index and only retrieves as many candidates as you ask for. This is what makes multi-keyword queries fast on large tables.
- **Index size.** The `fts` index is denser than a GIN index over `tsvector` because it stores positions, frequencies, and language-specific analyzer state. Plan disk accordingly.
- **Updates.** Inserts and updates are applied to the index continuously. There's no separate refresh step.
- **`ORDER BY score`.** When you order by `pgfts.fts_score()`, the planner still uses the FTS custom scan - it doesn't rerank the whole table.

## Limitations during preview

- `pgfts.fts_score()` requires `pg_fts` in `shared_preload_libraries`. Without it, only `pgfts.fts_query()` (which already returns rows in rank order) works.
- The `@@?` operator doesn't support boolean (`AND` / `OR` / `NOT`) syntax. Use `pgfts.fts_query()` for those queries.
- CJK analyzers can be inspected with `pgfts.debug_analyze_text()` but can't yet be selected at index creation time via a `WITH (analyzer = '...')` option.
- The index isn't represented in `pg_stat_user_indexes` the same way GIN is, because results come through a custom scan.

## Related content

- [Retrieval foundations: vector, full-text, and hybrid search in Azure HorizonDB (Preview)](ai-search-overview.md)
- [Hybrid search in Azure HorizonDB (Preview)](hybrid-search.md)
- [Implement vector search in Azure HorizonDB using the pgvector extension (Preview)](vector-search-pgvector.md)
