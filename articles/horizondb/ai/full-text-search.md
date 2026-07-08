---
title: Full-text search with pg_textsearch in Azure HorizonDB
description: Use the pg_textsearch extension to add BM25-ranked full-text search to Azure HorizonDB for keyword retrieval at scale, with language-aware tokenization and hybrid search patterns.
#customer intent: As a developer building search on Azure HorizonDB, I want to add BM25 full-text search with pg_textsearch so that keyword queries return high-quality results at scale.
author: abeomor
ms.author: abeomorogbe
ms.reviewer: maghan
ms.date: 07/07/2026
ms.service: azure-horizondb
ms.subservice: ai-search
ms.topic: how-to
ms.collection: ce-skilling-ai-copilot
ms.update-cycle: 180-days
---

# Full-text search with pg_textsearch in Azure HorizonDB (Preview)

The `pg_textsearch` extension adds BM25-ranked full-text search to Azure HorizonDB. BM25 is the same relevance algorithm used by Elasticsearch, Solr, and Azure AI Search. `pg_textsearch` brings BM25 into Postgres as a custom index access method, so you can run keyword search next to relational data without a separate search system.

`pg_textsearch` works on its own, and it composes with `pgvector` and DiskANN to power [hybrid search](hybrid-search.md).

> [!NOTE]  
> `pg_textsearch` is in **preview**.

## When to use pg_textsearch vs. built-in tsvector

PostgreSQL has built-in full-text search through `tsvector` and `tsquery`. `pg_textsearch` doesn't replace that path, but it is often a better fit when you need BM25 ranking and top-k search behavior.

| Need | Built-in `tsvector` + GIN | `pg_textsearch` |
| --- | --- | --- |
| Ranking algorithm | `ts_rank` - no term saturation, no length normalization, no native IDF | **BM25** - industry-standard ranker with all three |
| Query pattern | `WHERE @@ tsquery`, then sort | `ORDER BY ... <@> ... LIMIT n` for top-k retrieval |
| Language configuration | PostgreSQL text search configs | PostgreSQL text search configs via `text_config` |
| Phrase queries | Supported with `tsquery` phrase operators | Not natively supported (see limitations) |

If you already have a small search workload and you're satisfied with `ts_rank`, built-in FTS might be enough. For modern keyword retrieval with BM25 ranking and top-k performance patterns, use `pg_textsearch`.

## Why BM25

BM25 (Best Matching 25) solves three problems that `ts_rank` doesn't:

- **Term frequency saturation.** Repeated occurrences of a keyword have diminishing returns, so a keyword-stuffed document can't dominate results.
- **Document length normalization.** A short product title that mentions "wireless headphones" outranks a 10,000-word blog post that happens to mention the same phrase once.
- **Inverse document frequency (IDF).** Common words (`the,` `error`) get down-weighted; rare, discriminating terms ("PG-4012," "replication") get up-weighted.

That's why modern search engines use BM25 (or a close variant) as a baseline ranker. By using `pg_textsearch`, you get the same ranking model inside Postgres.

## Enable pg_textsearch

To enable `pg_textsearch` on Azure HorizonDB, first configure a parameter group, then create the extension in each database.

Use these setup articles:

- [Load shared libraries](../extensions/how-to-load-libraries.md)
- [Allow extensions](../extensions/how-to-allow-extensions.md)
- [Create extensions](../extensions/how-to-create-extensions.md)

1. Create a parameter group for your server.
1. Set `shared_preload_libraries` to include `pg_textsearch`.
1. Set `azure.extensions` to include `pg_textsearch`.
1. Apply the parameter group to the server.
1. Connect to each target database and run:

```sql
CREATE EXTENSION IF NOT EXISTS pg_textsearch;
```

To verify both parameter settings after restart:

```sql
SHOW shared_preload_libraries;
SHOW azure.extensions;
```

To remove the extension from the current database:

```sql
DROP EXTENSION IF EXISTS pg_textsearch;
```

## Create a full-text search index

The `pg_textsearch` module provides a custom index access method named `bm25`.

Create a table and a BM25 index:

```sql
CREATE TABLE products (
    id          INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT NOT NULL
);

INSERT INTO products_pgts (name, description, category, lang) VALUES
('QuietWave Pro', 'wireless noise cancelling headphones with long battery life', 'audio', 'en'),
('BassMini Buds', 'compact wireless earbuds with deep bass', 'audio', 'en'),
('StudioMax One', 'over ear headphones for studio monitoring and editing', 'audio', 'en'),
('CloudShell 16', 'lightweight laptop sleeve for travel and daily commute', 'accessories', 'en'),
('HomeSense Hub', 'smart home hub with voice control and automation', 'home', 'en'),
('NoiseBlock X', 'premium noise cancelling headset with adaptive ANC', 'audio', 'en'),
('Libro Uno', 'auriculares inalambricos con cancelacion de ruido', 'audio', 'es');

CREATE INDEX idx_products_bm25
    ON products
    USING bm25 (description)
    WITH (text_config = 'english');
```

Key differences from a GIN index on `tsvector`:

- You index plain `text` directly, not a persisted `tsvector` column.
- Ranking uses BM25 and is produced through the `<@>` operator.
- Top-k queries use `ORDER BY ... LIMIT n` and can benefit from index-level optimizations.

## Run searches

### Basic keyword search

Use `<@>` in `ORDER BY` to rank results by BM25 score.

```sql
SELECT id, name, description
FROM products
ORDER BY description <@> 'wireless noise cancelling headphones'
LIMIT 10;
```

`<@>` returns negative BM25 scores. Lower values are better matches.

### Use an explicit index with to_bm25query()

Use explicit index selection when you want predictable behavior across environments, especially if a table has multiple BM25 indexes or you run queries in stored procedures. `to_bm25query()` makes the target index explicit, which helps avoid ambiguity and improves operational consistency.

```sql
SELECT id, name, description
FROM products
ORDER BY description <@> to_bm25query(
    'wireless headphones',
    'idx_products_bm25')
LIMIT 10;
```

### Project the BM25 score

Return the score in the result set and sort by score:

```sql
SELECT id,
       name,
       description <@> to_bm25query(
           'wireless headphones',
           'idx_products_bm25') AS score
FROM products
ORDER BY score
LIMIT 10;
```

### Combine filtering with ranking

Apply structured filters in `WHERE`, and keep BM25 ranking in `ORDER BY`:

```sql
SELECT id, name, category, 
        description <@> to_bm25query(
           'noise cancelling',
           'idx_products_bm25') AS score
FROM products
WHERE category = 'audio'
ORDER BY score
LIMIT 10;
```

### Threshold filtering by score

Use a score predicate when you need a minimum relevance threshold:

```sql
SELECT id, name,
       description <@> to_bm25query(
           'wireless headphones',
           'idx_products_bm25') AS score
FROM products
WHERE (description <@> to_bm25query(
           'wireless headphones',
           'idx_products_bm25')) < -0.01
ORDER BY score
LIMIT 10;
```

## Multi-language support

`pg_textsearch` uses PostgreSQL text search configurations through the `text_config` index option.

```sql
-- English stemming
CREATE INDEX idx_products_en
    ON products
    USING bm25 (description)
    WITH (text_config = 'english');

-- Simple tokenization (no stemming)
CREATE INDEX idx_products_simple
    ON products
    USING bm25 (description)
    WITH (text_config = 'simple');
```

Compare English stemming vs simple tokenization for the same query.
```sql
SELECT id,
       name,
       description <@> to_bm25query(
           'wireless headphones',
           'idx_products_pgts_bm25') AS score_english,
       description <@> to_bm25query(
           'wireless headphones',
           'idx_products_pgts_bm25_simple') AS score_simple
FROM products_pgts
ORDER BY score_english
LIMIT 10;
```

To list available text search configurations:

```sql
SELECT cfgname FROM pg_ts_config;
```

## Combine pg_textsearch with vector search (hybrid search)

Use **Reciprocal Rank Fusion (RRF)** to combine BM25 and vector search. Run the two searches separately, then combine their ranks.

```sql
WITH bm25_results AS (
    SELECT id,
           ROW_NUMBER() OVER (
               ORDER BY description <@> to_bm25query(
                   'wireless noise cancelling',
                   'idx_products_bm25')) AS bm25_rank
    FROM products
    ORDER BY description <@> to_bm25query(
        'wireless noise cancelling',
        'idx_products_bm25')
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

- **Use `ORDER BY ... LIMIT`.** Top-k queries are the primary access pattern and are typically the fastest.
- **Bulk load first, then create index.** Like other index types, build time is often lower when you create the BM25 index after loading data.
- **Choose the right `text_config`.** Language-specific configurations improve stemming and tokenization quality.
- **Use force-merge after large loads.** After major batch inserts, `bm25_force_merge()` can improve query speed.

## Limitations (Preview)

- **No native phrase queries.** BM25 indexes store term statistics, not term positions. You can emulate phrase matching by reranking candidates with a post-filter.
- **No built-in fuzzy or typo operator.** Use PostgreSQL features such as `pg_trgm` when you need typo-tolerant matching.
- **PL/pgSQL requires explicit index names.** Inside stored procedures and DO blocks, use `to_bm25query(query, index_name)` instead of implicit `text <@> 'query'`.

## Related content

- [Retrieval foundations: vector, full-text, and hybrid search in Azure HorizonDB (Preview)](ai-search-overview.md)
- [Hybrid search in Azure HorizonDB (Preview)](hybrid-search.md)
- [Implement vector search in Azure HorizonDB using the pgvector extension (Preview)](vector-search-pgvector.md)
