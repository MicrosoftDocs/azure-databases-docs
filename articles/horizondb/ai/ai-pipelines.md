---
title: Implement AI Pipelines in Azure HorizonDB
description: Define and run AI data pipelines directly in Azure HorizonDB with built-in support for chunking, embeddings, extraction, retrieval, and reranking, backed by reliable execution with state, retries, and crash recovery.
#customer intent: As a user, I want to understand how to implement durable AI pipelines for chunking, embedding, extraction, and retrieval.
author: abeomor
ms.author: abeomorogbe
ms.reviewer: maghan
ms.date: 07/07/2026
ms.service: azure-horizondb
ms.subservice: ai-search
ms.topic: concept-article
ms.collection: ce-skilling-ai-copilot
ms.update-cycle: 180-days
---

# Implement AI pipelines in Azure HorizonDB (Preview)

AI pipelines in Azure HorizonDB let you describe an AI workflow (chunking, embedding, extraction, generation, ranking, human approval) declaratively in SQL, and run it as a fault-tolerant pipeline that lives inside the database. The pipeline definition is just a row in a system catalog. The execution is durable: it survives crashes, retries failed steps, checkpoints incremental work, and resumes long-running jobs from the last completed step.

AI pipelines are part of the `azure_ai` extension. The `ai.*` functions and views used throughout this article are provided by `azure_ai` and built on top of [pg_durable](../development/durable-functions.md). Where `pg_durable` gives you a general durable-execution engine, the `ai.*` pipeline API gives you a higher-level, AI-shaped surface - sources, steps, sinks, and triggers - that compiles down to a durable graph automatically.

> [!NOTE]  
> AI pipelines are in **preview**.

## Why pipelines belong in the database

The most common pattern for getting data into a vector store today is a service in the application tier that reads source rows, calls an embedding API, and writes chunks back to Postgres. That pattern works, but it has predictable failure modes:

- The embedding service hits a transient API failure mid-batch, and there's no shared checkpoint between the application and the database that says which rows are done.
- A worker crashes after writing some chunks but before committing the parent row's "processed" flag, leaving the index in an inconsistent state.
- The embedding model changes, and now there's no clean way to re-embed exactly the rows that need it.

AI pipelines move that logic into HorizonDB itself. The source, the steps, the sink, and the run history are all SQL. The database is already where your data lives, where your transactions commit, and where backups and PITR already protect you - so it's the natural place for the embedding pipeline to live too.

## Pipeline anatomy

A pipeline has four parts:

- **Source** - where rows come from. Today, a `table_source(...)` over a HorizonDB table, optionally with an `incremental_column` (so the pipeline can skip rows it's already processed).
- **Steps** - the AI operations that transform each row, in order. Each step appends columns to the in-flight batch.
- **Sink** *(optional)* - where the resulting rows are written.
- **Trigger** - `'on_change'` (run automatically when source rows change) or `'manual'` (run only when you call `ai.run()`).

### Step types

Each step reads one or more input columns and writes its result to a fixed output column on the in-flight batch. During preview, these output column names are implicit, so your sink table must declare columns with exactly these names. For more information, see [Build the sink table](#build-the-sink-table).

| Step | Purpose | Reads | Writes to |
| --- | --- | --- | --- |
| `ai.chunk()` | Split a long text column into overlapping chunks. | The input text column. | `doc_id`, `chunk_index`, `chunk_text`, `metadata` |
| `ai.embed()` | Generate vector embeddings for a column. | `chunk_text` or another text column. | `embedding` |
| `ai.extract()` | Extract structured fields from text using an LLM. | A text column. | Merges its JSON result into `metadata`. |
| `ai.generate()` | Generate text from a prompt template using an LLM. | A text column. | `generated_text` |
| `ai.rank()` | Score documents against a required `query`. | A text column. | `rank_score` (double precision, roughly 0–1) |

## Prerequisites

Enable the required extensions:

```sql
CREATE EXTENSION IF NOT EXISTS pg_durable;
CREATE EXTENSION IF NOT EXISTS azure_ai;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_diskann;
```

> [!NOTE]  
> You must preload `pg_durable` through `shared_preload_libraries` before you can [create the extension](../development/durable-functions.md). If `CREATE EXTENSION pg_durable` fails with `pg_durable must be loaded via shared_preload_libraries`, add it to that parameter and restart the instance. The `ai.*` pipeline API works without `pg_durable`, so you only need it for the optional [durable-instance inspection](#run-monitor-and-retry).

You also need an embedding (and optionally a generation) model that `azure_ai` can call. You have two options:

### Option 1: AI Model Management

If [AI Model Management (limited preview)](ai-model-management.md) is enabled on your HorizonDB instance, models are provisioned and registered in the model registry automatically. There's no endpoint or key to manage. AI functions use the Managed Models by default.

```sql
-- No endpoint configuration needed; AI Model Management handles it.
-- Uses the default-embedding Managed Model when no model alias is specified.
SELECT azure_openai.create_embeddings(input => 'hello world');
```

### Option 2: Manually register a model in the model registry

If you don't use AI Model Management, deploy your own model through [Microsoft Foundry](/azure/ai-foundry/quickstarts/get-started-code#start-with-a-project-and-model) and register it in the model registry:

```sql
SELECT model_registry.model_add(
    'my-embedding',                          -- a unique alias for your model
    'https://YOUR_RESOURCE.openai.azure.com/', -- your Azure OpenAI endpoint
    'text-embedding-3-small',                -- deployment name
    'text-embedding-3-small',                -- model name
    NULL,                                    -- API version (NULL for latest)
    'subscription-key',                      -- auth type
    'YOUR_API_KEY'                           -- endpoint key
);
```

For complete details on model registration, see [Manual setup with model registry](ai-functions.md#option-2-manual-setup-with-model-registry).

The examples in this article use the model alias `default-embedding`. This alias isn't guaranteed to exist on every instance. Confirm which aliases are registered, and use one of those names (or register `default-embedding` yourself) before you run the pipeline examples:

```sql
-- List the model aliases registered on this instance.
SELECT * FROM model_registry.model_list();
```

Model registration doesn't validate the endpoint or key during preview. A wrong endpoint, deployment name, or key surfaces only when the pipeline runs, and can appear as empty output rather than as an error. After you register a model, confirm it responds with a one-shot call before you build a pipeline around it:

```sql
-- Confirm a registered model alias responds before building a pipeline.
SELECT azure_openai.create_embeddings('my-embedding', 'connectivity test');
```

The pipeline examples in this article work the same way under either option.

## Define a pipeline

The smallest useful AI pipeline takes a source table of documents, chunks the body, generates embeddings, and writes the result to a sink table.

### Build the sink table

`ai.create_pipeline()` doesn't create the sink table for you. Create it yourself *before* you call `ai.create_pipeline()`, and give it columns that match the output columns your steps write. If the sink is missing a column that a step writes to, the pipeline still reports success but that step's result is silently dropped. For more information, see [Verify pipeline output](#verify-pipeline-output).

The columns you need depend on which steps your pipeline chains together:

| Steps in your pipeline | Required sink columns |
| --- | --- |
| `chunk` → `embed` | `doc_id`, `chunk_index`, `chunk_text`, `embedding`, `metadata` |
| `chunk` → `extract` | `doc_id`, `chunk_index`, `chunk_text`, `metadata` (extracted fields merge into `metadata`) |
| `chunk` → `generate` | `doc_id`, `chunk_index`, `chunk_text`, `generated_text`, `metadata` |
| `chunk` → `rank` | `doc_id`, `chunk_index`, `chunk_text`, `rank_score`, `metadata` |

Keep these behaviors in mind when you design the sink during preview:

- **`ai.generate()` writes to `generated_text`.** Read its output from `generated_text`, not `output`, `result`, `response`, or `generated`.
- **`ai.extract()` merges into `metadata`.** Extracted fields don't get their own columns. Read them from the `metadata` JSONB, for example `metadata->'style'`. Two extract steps in the same pipeline share this single blob.
- **`ai.rank()` writes to `rank_score` and requires a `query`.** The score is a `double precision` value (roughly 0–1). The `query` argument is required and has no default. Pass the optional `top_n` argument to keep only the highest-scoring rows. `ai.rank()` doesn't emit a `rank` or `relevance` column matching the synchronous `azure_ai.rank()` table shape.
- **`ai.chunk()` materializes `chunk_text` and `metadata`.** `ai.extract()`, `ai.generate()`, and `ai.rank()` depend on the `metadata` and `chunk_text` columns that `ai.chunk()` creates, so a chunk step must run first. Running them without a preceding `chunk` step fails with `column "metadata" does not exist`, and `doc_id` stays NULL.
- **Chunking can multiply rows.** One source row can produce several chunk rows, and therefore several output rows. If you need exactly one output row per source row, set `chunk_size` larger than your source text so each row yields a single chunk.

> [!IMPORTANT]  
> The sink table isn't created automatically and has no schema validation during preview. Create it manually with the columns listed earlier before you call `ai.create_pipeline()`.

### Create the pipeline

```sql
-- Create the sink table first, with columns that match the pipeline steps.
CREATE TABLE rag_pipeline_output (
    doc_id      INT,
    chunk_index INT,
    chunk_text  TEXT,
    embedding   vector(1536),
    metadata    JSONB
);

CREATE INDEX diskann_sq_embedding_idx ON rag_pipeline_output USING diskann (embedding vector_cosine_ops) WITH (spherical_quantized = true);

CREATE TABLE documents_ai_pipeline (
    id          SERIAL PRIMARY KEY,
    title       TEXT NOT NULL,
    content     TEXT NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO documents_ai_pipeline (title, content) VALUES
('PostgreSQL Basics', 'PostgreSQL is an open-source relational database designed for reliability, extensibility, and SQL compliance.'),
('Vector Search', 'Vector search compares embeddings to find semantically similar content across large collections of text.'),
('Durable Workflows', 'Durable execution helps pipelines recover from crashes, retry transient failures, and resume from checkpoints.');

SELECT ai.create_pipeline(
    name   => 'rag_pipeline',
    source => ai.table_source(
        table_name => 'documents_ai_pipeline'
    ),
    steps  => ARRAY[
        ai.chunk(input => 'content',
                 chunk_size => 512, --Optional, default = 512
                 overlap    => 64   --Optional, default = 64
                 ),
        ai.embed(model => 'default-embedding',
                 input => 'chunk_text', -- This column comes from the chunk step output.
                 dimensions => 1536)
    ],
    trigger => 'on_change',
    sink   => ai.table_sink('rag_pipeline_output')
);
```

The `ai.create_pipeline()` function registers the definition. It doesn't run anything yet. To inspect the compiled execution plan, use `ai.explain()`:

```sql
SELECT ai.explain('rag_pipeline');
```

Behind the scenes, `ai.run()` translates the definition into a `pg_durable` graph and submits it via [Durable functions with pg_durable in Azure HorizonDB (Preview)](../development/durable-functions.md). Each AI step becomes a durable node, so a failure in `ai.embed()` doesn't rerun `ai.chunk()`.

> [!TIP]  
> After the sink table is populated, you can build a [Scalable vector indexing with DiskANN (Preview)](vector-index-diskann.md) on the `embedding` column and use it directly in [hybrid-search](hybrid-search.md) queries.

### Use named arguments and required parameters

Always call the step builders and `ai.create_pipeline()` with **named arguments**. 

The verified step and pipeline signatures during preview are:

- **Create a pipeline**

```sql
ai.create_pipeline(name text, source jsonb, steps jsonb[], sink jsonb,
                   trigger text DEFAULT 'manual', options jsonb DEFAULT NULL)
```

- **Generate text**

```sql
ai.generate(input text, system_prompt text DEFAULT 'You are a helpful assistant.',
           max_tokens integer DEFAULT 1024, model text DEFAULT NULL)
```

- **Extract structured fields**

```sql
ai.extract(input text, data text[] DEFAULT NULL, model text DEFAULT NULL)
```

- **Embed text**

```sql
ai.embed(input text, model text DEFAULT NULL, batch_size integer DEFAULT 100,
        dimensions integer DEFAULT NULL)
```

- **Rank documents**

```sql
ai.rank(input text, query text, top_n integer DEFAULT NULL,
        model text DEFAULT NULL)
```

- **Chunk text**

```sql
ai.chunk(input text, method text DEFAULT NULL, chunk_size integer DEFAULT 512,
        overlap integer DEFAULT 64)
```

- **Define a table source**

```sql
ai.table_source(table_name text, incremental_column text DEFAULT NULL,
               schema_name text DEFAULT 'public')
```

- **Define a table sink**

```sql
ai.table_sink(table_name text, schema_name text DEFAULT 'public',
             on_conflict text[] DEFAULT NULL, on_conflict_action text DEFAULT 'insert')
```

## Advanced pipeline steps

Beyond chunking and embedding, AI pipelines support extraction, generation, and ranking. These examples reuse the `documents_ai_pipeline` source table from the previous section, define a `search_results` source for ranking, and use the verified argument names from the signatures block. Each example starts with `ai.chunk()` because `ai.extract()`, `ai.generate()`, and `ai.rank()` depend on the `chunk_text` and `metadata` columns that chunking materializes.

### Extract structured fields with `ai.extract()`

`ai.extract()` takes a `data` array of field labels (not a free-text prompt and not an `output_schema`). It merges the extracted values into the `metadata` column, so read them as `metadata->'<field>'`:

```sql
CREATE TABLE extraction_pipeline_output (
    doc_id      INT,
    chunk_index INT,
    chunk_text  TEXT,
    metadata    JSONB   -- ai.extract merges its fields here
);

SELECT ai.create_pipeline(
    name   => 'extraction_pipeline',
    source => ai.table_source(table_name => 'documents_ai_pipeline'),
    steps  => ARRAY[
        ai.chunk(input => 'content'),
        ai.extract(
            input => 'chunk_text',
            data  => ARRAY['topics: string - the main topics discussed',
                           'entities: string - named people, products, or places']
            model => 'my-gpt'
        )
    ],
    sink   => ai.table_sink('extraction_pipeline_output')
);
```
Each field is a label, either a bare name like `product`, or the detailed form `name: type - description` (for example `sentiment: number - sentiment score from 1 to 5`). HorizonDB does the rest durably, in bulk, with the same retry-and-resume guarantees.

### Generate new content with `ai.generate()`

`ai.generate()` takes the instruction in `system_prompt` (not `prompt`) and writes its result to `generated_text`:

```sql
CREATE TABLE generation_pipeline_output (
    doc_id         INT,
    chunk_index    INT,
    chunk_text     TEXT,
    generated_text TEXT,   -- ai.generate writes here
    metadata       JSONB
);

SELECT ai.create_pipeline(
    name   => 'generation_pipeline',
    source => ai.table_source(table_name => 'documents_ai_pipeline'),
    steps  => ARRAY[
        ai.chunk(input => 'content'),
        ai.generate(
            input => 'chunk_text',
            system_prompt => 'Create a concise summary in 50 words or fewer.'
            model => 'my-gpt'
        )
    ],
    sink   => ai.table_sink('generation_pipeline_output')
);
```
Swap the `system_prompt` and the same shape becomes a classifier ("Label this ticket as billing, bug, or feature request"), a translator, or a headline generator. The instruction goes in `system_prompt`; the result lands in `generated_text`.

### Rank documents with `ai.rank()`

`ai.rank()` requires a `query` argument and writes a relevance score to `rank_score`. Start with a chunk step so `doc_id` and `chunk_text` are populated; without it, `doc_id` stays NULL:

```sql
CREATE TABLE search_results (
    id            SERIAL PRIMARY KEY,
    document_text TEXT NOT NULL
);

INSERT INTO search_results (document_text) VALUES
('PostgreSQL supports vector search through the vector extension.'),
('Durable functions checkpoint progress so workflows survive restarts.');

CREATE TABLE ranking_pipeline_output (
    doc_id      INT,
    chunk_index INT,
    chunk_text  TEXT,
    rank_score  DOUBLE PRECISION,   -- ai.rank writes the relevance score here
    metadata    JSONB
);

SELECT ai.create_pipeline(
    name   => 'ranking_pipeline',
    source => ai.table_source(table_name => 'search_results'),
    steps  => ARRAY[
        ai.chunk(input => 'document_text'),
        ai.rank(
            input => 'chunk_text',
            query => 'How does PostgreSQL handle vector search?'
            top_n => 10,
            model => 'my-reranker'
        )
    ],
    sink   => ai.table_sink('ranking_pipeline_output')
);
```

## Run, monitor, and retry

Trigger a run and wait for it:

```sql
SELECT ai.run('rag_pipeline');
```

Inspect the output table.

```sql
SELECT doc_id, chunk_index, left(chunk_text, 80) AS preview,embedding 
FROM rag_pipeline_output
ORDER BY doc_id, chunk_index;
```

You can query status, history, and the underlying durable instance from SQL:

```sql
SELECT * FROM ai.status('rag_pipeline');
SELECT * FROM ai.list_pipelines();
```

For full execution history, query the [durable function](../development/durable-functions.md) instance. This query requires `pg_durable` to be installed and preloaded through `shared_preload_libraries`. Without it, the `df.instances` relation doesn't exist and the query fails:

```sql
-- Optional: requires pg_durable. Check whether a run is pending, completed, or failed.
SELECT di.id AS instance_id, di.label, di.status AS df_status, di.created_at
FROM df.instances di
WHERE di.label = 'ai-pipeline:rag_pipeline'
ORDER BY di.created_at DESC
LIMIT 5;
```

The durable engine automatically retries failed steps. The `azure_ai` extension internally handles transient errors from the embedding endpoint. Persistent failures appear in `ai.status()` and in the `pg_durable` instance history.

To pause and resume change-triggered runs:

```sql
SELECT ai.pause('rag_pipeline');
SELECT ai.resume('rag_pipeline');
```

### Verify pipeline output

A pipeline can report success while producing all-NULL output. If your sink table is missing a column that a step writes to, or that column has the wrong name, the step's result is dropped without an error. `ai.status()` still reports `last_run_status = completed` with a nonzero `total_processed`.

After a run, confirm that the output columns are populated, not just that the row count is nonzero:

```sql
-- Confirm the step output columns aren't all NULL.
SELECT
    count(*)         AS rows,
    count(embedding) AS embeddings_written
FROM rag_pipeline_output;
```

If `embeddings_written` is zero while `rows` is nonzero, the sink is missing or misnaming the `embedding` column. For a pipeline that ends in `ai.generate()`, check `count(generated_text)` the same way. Compare your sink columns against [Build the sink table](#build-the-sink-table).

### Manage the pipeline lifecycle

A pipeline persists in the database until you drop it. The full lifecycle is `ai.create_pipeline()` → `ai.run()` (or an `on_change` trigger) → `ai.status()` → `ai.drop_pipeline()`. The `on_change` trigger persists across sessions: once set, the pipeline reruns whenever source rows change until you pause or drop it.

List the pipelines you defined, and remove one when you're done:

```sql
SELECT * FROM ai.list_pipelines();
SELECT ai.drop_pipeline('rag_pipeline');
```

## Re-embed when the model changes

Embedding models change. Dimensions change. Chunk sizes change. AI pipelines treat that change as a first-class operation: you change the pipeline definition (or the sink schema), then call `ai.backfill()` to reprocess every row from scratch:

```sql
-- After dropping and recreating the pipeline with a new model or dimensions:
TRUNCATE rag_pipeline_output;
SELECT ai.backfill('rag_pipeline');
```

The backfill runs as a single durable instance. If the database restarts mid-backfill, it resumes from the last checkpointed batch. You don't restart from row zero.

## Cost controls

Embedding and LLM call cost money. AI pipelines give you a few practical levers to keep that cost predictable:

- `incremental_column` ensures you only embed new or changed rows on subsequent runs.
- `ai.pause()` stops the change trigger from launching new runs while you're tuning.
- **`ai.backfill()` is explicit.** Re-embedding everything only happens when you ask for it.

## Choose between `ai.*` pipelines and `azure_ai.*` calls

HorizonDB exposes two related namespaces, and mixing them up is the most common source of confusion:

- **`azure_ai.*` and `azure_openai.*`** functions run *immediately and synchronously*. `azure_openai.create_embeddings(...)` returns a vector in the calling statement.
- **`ai.*`** functions are *pipeline step builders*. `ai.embed(...)` doesn't call a model. It returns a JSON descriptor that `ai.create_pipeline()` compiles into a durable graph, and the work runs later, durably, when the pipeline runs.

The two surfaces solve different problems:

| Concepts | One-shot `azure_ai` calls | AI pipelines |
| --- | --- | --- |
| Namespace | `azure_ai.*`, `azure_openai.*` | `ai.*` |
| Shape | Single SQL function call (`azure_openai.create_embeddings(...)`) | Declarative pipeline with source, steps, sink |
| Execution | Immediate and synchronous | Deferred and durable |
| Durability | None. Fails the calling statement | Durable: retries, resume after crash, checkpoints |
| Best for | Unplanned embedding of a few rows; using AI inside a query | Bulk ingestion, ongoing change-driven embedding, multi-step workflows |
| Backfill | Manual `UPDATE ... SET embedding = ...` | `ai.backfill()` |

Use one-shot calls for interactive queries and small jobs. Use a pipeline whenever the work is large enough, long enough, or important enough that you'd otherwise build a service tier for it.

### Map AI functions to AI pipeline steps

The pipeline step builders are the deferred analogues of the [AI functions](ai-functions.md), but their argument names, sets, and order differ during preview. Don't assume the arguments you learned for AI functions carry over to its pipeline step. Use this mapping, and always pass named arguments:

| Operation | AI function call | Pipeline step | Watch out for |
| --- | --- | --- | --- |
| Generate | `azure_ai.generate(prompt, model, json_schema, system_prompt)` | `ai.generate(input, system_prompt, max_tokens, model)` | The first argument is `prompt` synchronously but `input` in the pipeline. The pipeline step has no `json_schema` and adds `max_tokens`. |
| Extract | `azure_ai.extract(document, data, model)` | `ai.extract(input, data, model)` | The first argument is `document` synchronously but `input` in the pipeline. |
| Embed | `azure_openai.create_embeddings(model, input)` | `ai.embed(input, model, batch_size, dimensions)` | Different namespace and argument order. The pipeline step adds `batch_size` and `dimensions`. |
| Rank | `azure_ai.rank(query, documents, model)` | `ai.rank(input, query, top_n, model)` | The pipeline step ranks one input column per row and writes `rank_score`, rather than returning a ranked table. Use `top_n` to keep only the highest-scoring rows. |
| Chunk | No synchronous equivalent | `ai.chunk(input, method, chunk_size, overlap)` | Pipeline-only step. |

## Monitor pipelines in Visual Studio Code

The PostgreSQL extension for Visual Studio Code includes a **Pipelines & Workflows** view where you can inspect AI pipeline runs and monitor execution state without leaving your editor.

### Open the Pipelines pane 

1. In Visual Studio Code, open the PostgreSQL extension.
1. In **Object Explorer**, right-click your database.
1. Select **Pipelines & Workflows**.
1. Select the **AI Pipelines** tab.

:::image type="content" source="media/pipelines/ai-pipeline-usage.png" alt-text="Screenshot of the AI Pipelines tab in the PostgreSQL extension for Visual Studio Code showing pipeline definitions, runs, and the pipeline graph." lightbox="media/pipelines/ai-pipeline-usage.png" :::

### Understand the pipeline graph

When you select a pipeline run, the center pane displays the execution graph with color-coded step types:

- **Blue**: Source and sink steps (data entry and exit points).
- **Green**: Intermediate processing steps (chunk, embed, extract, generate, rank operations).
- **Pink**: External calls (model API calls and external services).

Use this color mapping to quickly validate that your pipeline is shaped correctly and executing as expected.

### Inspect run details

For each pipeline run, you can verify:

- **Status**: `completed`, `running`, or `failed`.
- **Run ID**: Unique identifier for traceability.
- **Start time and duration**: Performance insights.
- **Pipeline definition link**: Navigate from a run back to its definition to review recent changes.

If a run fails, open the graph view and inspect the step where execution stopped to identify the issue.

## Limitations during preview

- Sources are HorizonDB tables. To ingest from blob storage or external systems, land the content in a staging table first; the pipeline handles chunking, embedding, checkpointing, and sink writes from there.
- Pipelines run on the primary. Read replicas can query `ai.*` views but don't execute pipelines.
- Pipeline state isn't portable across major versions of `pg_durable` during **preview**. Drain or pause running pipelines before upgrading.

## Related content

- [Durable functions with pg_durable in Azure HorizonDB (Preview)](../development/durable-functions.md)
- [Generate vector embeddings using the create_embeddings() AI function (Preview)](generate-vector-embeddings.md)
- [AI functions in the azure_ai extension for Azure HorizonDB (Preview)](ai-functions.md)
