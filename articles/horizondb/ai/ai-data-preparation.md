---
title: Data Preparation for AI App and Agent Development in Azure HorizonDB
description: Learn the key data preparation steps—cleaning, chunking, embedding, enrichment, and indexing—required before building AI apps and agents with Azure HorizonDB.
author: shreyaaithal
ms.author: shaithal
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
# customer intent: As a user, I want to understand the data preparation steps required before building AI apps and agents, including search, RAG, and knowledge graph scenarios.
---

# Prepare data for AI app and agent development in Azure HorizonDB (Preview)

Before you can build AI-powered search, RAG applications, or intelligent agents, your source data needs to go through a preparation pipeline that transforms raw content into a queryable format. This article introduces the key steps: cleaning, chunking, embedding, enrichment, and indexing, and explains how Azure HorizonDB supports each one.

## Why data preparation matters

The quality of your AI application depends directly on the quality of your prepared data. A well-chunked, cleanly embedded dataset returns precise, relevant results. Poorly prepared data such as oversized chunks, noisy text, or mismatched embeddings lead to irrelevant matches and unreliable AI-generated answers.

Data preparation bridges the gap between raw source content and a queryable data store. The core process follows five steps:

1. **Clean and normalize**: remove noise from raw text.
1. **Chunk**: split large documents into smaller segments.
1. **Generate embeddings**: convert chunks into vector representations.
1. **Enrich with metadata**: attach filterable attributes to each chunk.
1. **Store and index**: save vectors, build vector, and full-text indexes for fast search.

## Step 1: Clean and normalize your data

Raw data is rarely ready for embedding. Before you chunk or embed anything, clean the source text to remove noise that would degrade vector quality.

Common cleaning tasks include:

- Stripping HTML or Markdown formatting tags.
- Removing boilerplate content like repeated headers, footers, or legal disclaimers.
- Fixing encoding issues and normalizing whitespace.
- Deduplicating repeated content across documents.

Cleaning doesn't need to be complex. Even basic normalization significantly improves embedding quality. Embedding models are sensitive to noise: a document that's 30% repeated boilerplate produces a vector that partially represents that boilerplate, not the actual content.

## Step 2: Chunk large documents

Embedding models have token limits (for example, 8,191 tokens for `text-embedding-3-small`), and a single embedding for an entire long document is too coarse-grained to match specific queries. Chunking splits documents into smaller, self-contained segments so the retrieval system can pinpoint the exact passage relevant to a query.

### Key decisions

**Chunk size** is one of the most used tuning parameters in a search pipeline:

- **Too large**: embeddings become diluted and retrieval precision drops.
- **Too small**: chunks lose context and the LLM receives fragmented information.

Adding **overlap** between consecutive chunks (repeating a portion of text at each boundary) helps preserve context across splits. A sentence straddling two chunks appear in both, preventing meaning from being lost at the boundary.

A common starting point is 512-2,000 characters. Tune based on your content type and retrieval quality.

<a id="chunking-in-azure-horizondb"></a>

### Chunk in Azure HorizonDB

Azure HorizonDB supports chunking directly in SQL through the `ai.chunk()` step in [AI pipelines](ai-pipelines.md). You specify a target chunk size and an overlap:

```sql
ai.chunk(input_column => 'content', chunk_size => 512, overlap => 64)
```

## Step 3: Generate embeddings

Embeddings convert each text chunk into a dense numerical vector, an array of floating-point numbers (for example, 1,536 dimensions) that captures the semantic meaning of the text. Chunks with similar meanings produce vectors that are geometrically close together in high-dimensional space, even if they use different words.

Traditional keyword search matches exact terms and fails when a user searches for "time off policy" but the document says "PTO guidelines." Vector embeddings capture meaning rather than spelling, enabling similarity search across synonyms, paraphrases, and even different languages.

It's important that you use the same embedding model for both your stored data and your search queries. If you embed documents with `text-embedding-3-small` but embed queries with a different model, the vectors exist in different mathematical spaces and similarity comparisons are meaningless.

<a id="embedding-in-azure-horizondb"></a>

### Embed in Azure HorizonDB

Azure HorizonDB provides two ways to generate embeddings:

- **In a query**: Call the [`azure_openai.create_embeddings()`](ai-functions.md#azure_openaicreate_embeddings) function directly in SQL to embed one or more texts on demand. This approach works well for ad hoc embedding of a few rows or for embedding user queries at search time. To learn more, see [Generate vector embeddings using the create_embeddings() AI function](generate-vector-embeddings.md).
- **In a pipeline**: Use the `ai.embed()` step in an [AI pipeline](ai-pipelines.md) to embed text at scale with built-in retries, checkpointing, and crash recovery.

## Step 4: Enrich with metadata

Attaching metadata to each chunk transforms a vector store into a queryable, filterable knowledge base. Metadata enables filtered search, narrowing results by date, document type, category, or access level before or during similarity ranking.

Common metadata fields include:

- **Provenance**: source document title, URL, page number, chunk index.
- **Temporal**: creation date, last modified date.
- **Categorical**: document type, department, language, topic tags.
- **AI-derived**: key phrases, named entities, sentiment, summary.

Without metadata, a semantic search returns the most similar chunks but can't restrict results to, for example, "only HR policy documents from 2024." Metadata also enables citation tracking, so you know which source document a chunk came from when presenting results to users or an LLM.

In Azure HorizonDB, you can store metadata as columns in your chunk table or in a `JSONB` field alongside the vector, and use standard SQL `WHERE` clauses to filter during search.

## Step 5: Store and index

After cleaning, chunking, embedding, and enriching your data, store the results in a table. Then, build the indexes needed for your search strategy.

### Vector index

Add a `vector` column for embeddings and create a vector index for fast similarity search:

```sql
CREATE TABLE document_chunks (
    id              SERIAL PRIMARY KEY,
    doc_id          INT NOT NULL,
    chunk_index     INT NOT NULL,
    chunk_text      TEXT,
    embedding       vector(1536),
    metadata        JSONB,
    UNIQUE (doc_id, chunk_index)
);

CREATE INDEX ON document_chunks USING diskann (embedding);
```

HorizonDB supports three vector index types: IVFFlat, HNSW, and DiskANN. Each type is optimized for different scale and performance characteristics. For guidance on choosing the right index, see [Choose the right vector index for your workload in Azure HorizonDB](vector-index-selection-guide.md).

### Full-text index

For hybrid search (combining keyword and vector results), also create a full-text search index on the chunk text by using the `pg_fts` extension:

```sql
CREATE INDEX ON document_chunks USING fts (chunk_text);
```

The `pg_fts` extension enables BM25-ranked keyword matching alongside vector similarity, which consistently improves retrieval quality over either approach alone. To learn more, see [Full-text search with pg_fts in Azure HorizonDB](full-text-search-pgfts.md).

## Beyond search: additional preparation tasks

The five core steps prepare your data for vector and hybrid search, which form the foundation of most AI applications. Depending on your scenario, you might also need:

- **Structured data extraction**: Use the `ai.extract()` pipeline step or the [AI functions in the azure_ai extension](ai-functions.md) function to pull structured fields (entities, dates, categories) from unstructured text. Extracted data can feed agent tools, power filtering, or populate relational tables alongside your vectors.

- **Knowledge graph construction**: Extract entities and relationships from text and store them as a graph by using Apache AGE, enabling relationship-based queries that complement vector search. For a walkthrough, see [Tutorial: Build a knowledge graph from unstructured text using AI Functions and Apache AGE](build-knowledge-graph.md).

## Automate with AI pipelines

Rather than running each step manually, you can define a complete data preparation workflow as a durable [AI pipeline](ai-pipelines.md). A single pipeline declaration handles chunking, embedding, and writing to a sink table - with built-in retries, crash recovery, and incremental processing that only re-embeds new or changed rows. For the full guide, see [Implement durable AI pipelines in Azure HorizonDB](ai-pipelines.md).

## Related content

- [Implement durable AI pipelines in Azure HorizonDB](ai-pipelines.md)
- [Retrieval foundations: vector, full-text, and hybrid search in Azure HorizonDB](ai-search-overview.md)
- [Generate vector embeddings using the create_embeddings() AI function](generate-vector-embeddings.md)
