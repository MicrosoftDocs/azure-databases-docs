---
title: Build a Semantic Search Application with Azure HorizonDB
description: Learn how to build an end-to-end semantic search application with vector search, DiskANN indexing, and semantic reranking in Azure HorizonDB.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: ai-vector-search
ms.topic: tutorial
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
# customer intent: As a user, I want to learn how to build an end-to-end semantic search application with Azure HorizonDB and its generative AI capabilities.
---

# Tutorial: Build a semantic search application with Azure HorizonDB (Preview)

This hands-on tutorial shows you how to build a semantic search application by using Azure HorizonDB. You use vector search to find semantically similar results, DiskANN indexing for scalable performance, and semantic reranking to surface the most relevant matches.

Semantic search finds results based on meaning rather than exact keywords. For example, a recipe dataset might not contain labels like "gluten-free" or "vegan," but you can deduce these characteristics from the ingredients. Semantic search lets you issue natural language queries like "healthy vegan breakfast" and get relevant results, even when those exact words don't appear in the data.

In this tutorial, you:

> [!div class="checklist"]
> - Install required extensions and set up AI models.
> - Import sample recipe data.
> - Generate vector embeddings for your data using the `create_embeddings()` AI function.
> - Create a DiskANN index for scalable vector search.
> - Perform semantic search queries to find nearest neighbors.
> - Rerank search results using the `rank()` AI function to improve relevance.

## Prerequisites

1. An Azure HorizonDB instance. If you don't have one, [create an Azure HorizonDB instance](../configure-maintain/quickstart-create-cluster.md).
1. [AI Model Management in Azure HorizonDB (Preview)](ai-model-management.md) enabled on your instance. This automatically provisions the `azure_ai` extension and registers embedding and reranking models. If you prefer to use your own models instead, skip AI Model Management and install the `azure_ai` extension manually by running `CREATE EXTENSION azure_ai;` on your database. Then register your models as described in [Use your own models](#use-your-own-models-byom).

## Install extensions and set up AI models

### Enable the required extensions

Add `vector` and `pg_diskann` to your [extension allow list](../extensions/how-to-allow-extensions.md), and verify they're correctly added by running `SHOW azure.extensions;`.

Then install the extensions by connecting to your target database and running the following commands:

```sql
CREATE EXTENSION vector;
CREATE EXTENSION pg_diskann;
```

### Set up AI models

This tutorial uses [AI Model Management in Azure HorizonDB (Preview)](ai-model-management.md), which automatically provisions and configures the AI models you need. When you enable AI Model Management, it:

- Installs the `azure_ai` extension.
- Registers a `default-embedding` model (`text-embedding-3-small`) for generating vector embeddings.
- Registers a `default-reranker` model (`Cohere-rerank-v4.0-fast`) for semantic reranking.

With AI Model Management enabled, you can call AI functions without specifying a model. They automatically use the corresponding default model.

### Use your own models

If you prefer to use your own Microsoft Foundry model deployments instead of the Managed Models, register them in the model registry:

```sql
SELECT model_registry.model_add(
    'my-embedding',                              -- a unique alias for your model
    'https://my-endpoint.openai.azure.com/',     -- your Azure OpenAI endpoint URL
    'my-embedding-deployment',                   -- deployment name
    'text-embedding-3-small',                    -- model name
    NULL,                                        -- API version (NULL for latest)
    'subscription-key',                          -- auth type
    '<your-endpoint-key>'                        -- endpoint key
);
```

Then pass your model alias (for example, `'my-embedding'`) to AI function calls throughout this tutorial. For complete details on model registration and management, see [AI functions in the azure_ai extension](ai-functions.md#option-2-manual-setup-with-model-registry).

## Import sample data

### Download the data

Download the recipe dataset from [Kaggle](https://www.kaggle.com/datasets/thedevastator/better-recipes-for-a-better-life).

> [!TIP]  
> For datasets with large documents that exceed embedding model token limits, you should chunk the content into smaller segments before generating embeddings. This tutorial's recipe dataset has naturally small rows, so chunking isn't needed. For guidance on chunking strategies, see [Prepare data for AI app and agent development in Azure HorizonDB (Preview)](ai-data-preparation.md).

### Create the table

Connect to your server and create a `test` database. In that database, create a table to import the data:

```sql
CREATE TABLE public.recipes(
    rid integer NOT NULL,
    recipe_name text,
    prep_time text,
    cook_time text,
    total_time text,
    servings integer,
    yield text,
    ingredients text,
    directions text,
    rating real,
    url text,
    cuisine_path text,
    nutrition text,
    timing text,
    img_src text,
    PRIMARY KEY (rid)
);
```

### Load the data

Set the following environment variable on the client window to set encoding to UTF-8. This step is necessary because this particular dataset uses Windows-1252 encoding.

```cmd
Rem on Windows
Set PGCLIENTENCODING=utf-8;
```

```bash
# on Unix based operating systems
export PGCLIENTENCODING=utf-8
```

Import the data into the table. This dataset contains a header row.

```bash
psql -d <database> -h <host> -U <user> -c "\copy recipes FROM <local recipe data file> DELIMITER ',' CSV HEADER"
```

## Generate vector embeddings

Add a vector column to the table to store the embeddings:

```sql
ALTER TABLE recipes ADD COLUMN embedding vector(1536);
```

Generate embeddings for your data by using the `create_embeddings()` AI function. The following example concatenates several fields to produce a rich text representation of each recipe and generates an embedding for the result.

```sql
WITH ro AS (
    SELECT ro.rid
    FROM
      recipes ro
    WHERE
      ro.embedding IS NULL
      LIMIT 500
)
UPDATE
    recipes r
SET
    embedding = azure_openai.create_embeddings(
      input => r.recipe_name || ' ' || r.cuisine_path || ' ' || r.ingredients || ' ' || r.nutrition || ' ' || r.directions
    )
FROM
    ro
WHERE
    r.rid = ro.rid;
```

Repeat the command until there are no more rows to process.

> [!NOTE]  
> To use your own embedding model instead of the default Managed Model, pass your model alias as the first argument: `azure_openai.create_embeddings('my-embedding', input => ...)`. See [Use your own models](#use-your-own-models-byom).

> [!TIP]  
> Experiment with the `LIMIT` value. A high value might cause Azure OpenAI to throttle the request and cause the statement to fail partway through. If the statement fails, wait for at least one minute and run the command again.

## Create a DiskANN index

After you generate embeddings, create a DiskANN index on the vector column for fast, scalable approximate nearest neighbor search:

```sql
CREATE INDEX recipes_embedding_diskann ON recipes
    USING diskann (embedding vector_cosine_ops);
```

DiskANN is the recommended default vector index for production workloads on Azure HorizonDB. It supports in-place updates, scales to billions of vectors, and provides advanced filtering capabilities. For more information, see [Scalable vector indexing with DiskANN (Preview)](vector-indexing-diskann.md).

## Semantic search

Create a search function in your database for convenience:

```sql
CREATE FUNCTION
    recipe_search(search_query text, num_results int)
RETURNS TABLE(
    recipe_id int,
    recipe_name text,
    nutrition text,
    score real)
AS $$
DECLARE
    query_embedding vector(1536);
BEGIN
    query_embedding := azure_openai.create_embeddings(input => search_query);
    RETURN QUERY
    SELECT
      r.rid,
      r.recipe_name,
      r.nutrition,
      (r.embedding <=> query_embedding)::real AS score
    FROM
      recipes r
    ORDER BY score ASC LIMIT num_results; -- cosine distance
END $$
LANGUAGE plpgsql;
```

> [!NOTE]  
> To use your own embedding model, replace `azure_openai.create_embeddings(input => search_query)` with `azure_openai.create_embeddings('my-embedding', search_query)`. See [AI functions in the azure_ai extension for Azure HorizonDB (Preview)](ai-functions.md).

Invoke the function to search:

```sql
SELECT recipe_id, recipe_name, score FROM recipe_search('vegan recipes', 10);
```

Explore the results:

```
 recipe_id |                         recipe_name                          |   score
-----------+--------------------------------------------------------------+------------
      829 | Avocado Toast (Vegan)                                        | 0.15672222
      836 | Vegetarian Tortilla Soup                                     | 0.17583494
      922 | Vegan Overnight Oats with Chia Seeds and Fruit               | 0.17668104
      600 | Spinach and Banana Power Smoothie                            |  0.1773768
      519 | Smokey Butternut Squash Soup                                 | 0.18031077
      604 | Vegan Banana Muffins                                         | 0.18287598
      832 | Kale, Quinoa, and Avocado Salad with Lemon Dijon Vinaigrette | 0.18368931
      617 | Hearty Breakfast Muffins                                     | 0.18737361
      946 | Chia Coconut Pudding with Coconut Milk                       |  0.1884186
      468 | Spicy Oven-Roasted Plums                                     | 0.18994217
(10 rows)
```

## Semantic reranking

Vector search returns results that are semantically similar, but the top results might not be the most relevant for the specific query. Semantic reranking applies a second-stage scoring pass using a cross-encoder model to rescore the initial results and surface the best matches.

The following query retrieves the top 20 vector search results and then reranks them using the `rank()` AI function:

```sql
WITH vector_results AS (
    SELECT rid, recipe_name, ingredients,
      (embedding <=> azure_openai.create_embeddings(
          input => 'quick vegan dinner recipes'
      ))::real AS vector_score
    FROM recipes
    ORDER BY vector_score ASC
    LIMIT 20
),
reranked AS (
    SELECT id AS row_id, rank
    FROM azure_ai.rank(
      'quick vegan dinner recipes',
      ARRAY(SELECT recipe_name || ': ' || ingredients FROM vector_results),
      ARRAY(SELECT rid FROM vector_results)
    )
)
SELECT
    vr.rid,
    vr.recipe_name,
    vr.vector_score,
    rr.rank AS rerank_position
FROM vector_results vr
LEFT JOIN reranked rr ON rr.row_id = vr.rid
ORDER BY rr.rank ASC;
```

> [!NOTE]  
> To use your own reranker model instead of the default Managed Model, pass your model alias as the last argument to `azure_ai.rank()`. For example: `azure_ai.rank('query', documents, ids, 'my-reranker')`. See [AI functions in the azure_ai extension](ai-functions.md#azure_airank).

The reranked results prioritize recipes that are most relevant to the specific query intent - in this case, recipes that are both quick to prepare and vegan - rather than semantically similar to the query text.

For more information on the two-stage retrieval-and-rerank pattern, see [Semantic reranking with the rank() function (Preview)](semantic-rank-function.md) and [Implement durable AI pipelines in Azure HorizonDB (Preview)](ai-pipelines.md).

## Related content

- [Implement vector search in Azure HorizonDB using the pgvector extension (Preview)](vector-search-pgvector.md)
- [Generate vector embeddings using the create_embeddings() AI function (Preview)](generate-vector-embeddings.md)
- [Semantic reranking with the rank() function (Preview)](semantic-rank-function.md)
