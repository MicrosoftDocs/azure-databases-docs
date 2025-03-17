---
title: Semantic Search With Azure OpenAI
description: Semantic Search with Azure Database for PostgreSQL flexible server and Azure OpenAI.
author: mulander
ms.author: adamwolk
ms.reviewer: maghan
ms.date: 11/19/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: tutorial
ms.collection:
  - ce-skilling-ai-copilot
ms.custom:
  - ignite-2023
---

# Semantic Search with Azure Database for PostgreSQL Azure OpenAI

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This hands-on tutorial shows you how to build a semantic search application using Azure Database for PostgreSQL flexible server and Azure OpenAI Service. Semantic search does searches based on semantics; standard lexical search does searches based on keywords provided in a query. For example, your recipe dataset might not contain labels like gluten-free, vegan, dairy-free, fruit-free, or dessert but these characteristics can be deduced from the ingredients. The idea is to issue such semantic queries and get relevant search results.

Building semantic search capability on your data using GenAI and Flexible Server involves the following steps:
> [!div class="checklist"]
> * Identify the search scenarios. Identify the data fields that will be involved in search.
> * For every data field involved in search, create a corresponding vector field to store the embeddings of the value stored in the data field.
> * Generate embeddings for the data in the selected data fields and store the embeddings in their corresponding vector fields.
> * Generate the embedding for any given input search query.
> * Search for the vector data field and list the nearest neighbors.
> * Run the results through appropriate relevance, ranking and personalization models to produce the final ranking. In the absence of such models, rank the results in decreasing dot-product order.
> * Monitor the model, results quality, and business metrics such as CTR (select-through rate) and dwell time. Incorporate feedback mechanisms to debug and improve the search stack from data quality, data freshness and personalization to user experience.

## Prerequisites

1. Create an OpenAI account and [request access to Azure OpenAI Service](https://aka.ms/oai/access).
1. Grant access to Azure OpenAI in the desired subscription.
1. Grant permissions to [create Azure OpenAI resources and to deploy models](/azure/ai-services/openai/how-to/role-based-access-control).

[Create and deploy an Azure OpenAI Service resource and a model](/azure/ai-services/openai/how-to/create-resource), deploy the embeddings model [text-embedding-ada-002](/azure/ai-services/openai/concepts/models#embeddings-models). Copy the deployment name as it is needed to create embeddings.

## Enable the azure_ai and pgvector extensions

Before you can enable `azure_ai` and `pgvector` on your Azure Database for PostgreSQL flexible server instance, you need to add them to your allowlist as described in [how to use PostgreSQL extensions](../extensions/how-to-allow-extensions.md) and check if correctly added by running `SHOW azure.extensions;`.

Then you can install the extension, by connecting to your target database and running the [CREATE EXTENSION](https://www.postgresql.org/docs/current/static/sql-createextension.html) command. You need to repeat the command separately for every database you want the extension to be available in.

```sql
CREATE EXTENSION azure_ai;
CREATE EXTENSION vector;
```

## Configure OpenAI endpoint and key

In the Azure AI services under **Resource Management** > **Keys and Endpoints** you can find the endpoint and the keys for your Azure AI resource. Use the endpoint and one of the keys to enable `azure_ai` extension to invoke the model deployment.

```sql
select azure_ai.set_setting('azure_openai.endpoint','https://<endpoint>.openai.azure.com');
select azure_ai.set_setting('azure_openai.subscription_key', '<API Key>');
```

## Download & Import the Data

1. Download the data from [Kaggle](https://www.kaggle.com/datasets/thedevastator/better-recipes-for-a-better-life).
1. Connect to your server and create a `test` database, and in it create a table in which you'll import the data.
1. Import the data.
1. Add an embedding column to the table.
1. Generate the embeddings.
1. Search.

### Create the table

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

### Import the data

Set the following environment variable on the client window, to set encoding to utf-8. This step is necessary because this particular dataset uses the WIN1252 encoding.

```cmd
Rem on Windows
Set PGCLIENTENCODING=utf-8;
```

```bash
# on Unix based operating systems
export PGCLIENTENCODING=utf-8
```

Import the data into the table created; note that this dataset contains a header row:

```bash
psql -d <database> -h <host> -U <user> -c "\copy recipes FROM <local recipe data file> DELIMITER ',' CSV HEADER"
```

### Add a column to store the embeddings

```sql
ALTER TABLE recipes ADD COLUMN embedding vector(1536);
```

### Generate embeddings

Generate embeddings for your data using the azure_ai extension. In the following, we vectorize a few different fields, concatenated:

```sql
WITH ro AS (
    SELECT ro.rid
    FROM
        recipes ro
    WHERE
        ro.embedding is null
        LIMIT 500
)
UPDATE
    recipes r
SET
    embedding = azure_openai.create_embeddings('text-embedding-ada-002', r.recipe_name||' '||r.cuisine_path||' '||r.ingredients||' '||r.nutrition||' '||r.directions)
FROM
    ro
WHERE
    r.rid = ro.rid;
```

Repeat the command, until there are no more rows to process.

> [!TIP]  
> Play around with the `LIMIT`. With a high value, the statement might fail halfway through due to throttling imposed by Azure OpenAI. If it fails, wait for at least one minute and execute the command again.

### Search

Create a search function in your database for convenience:

```sql
create function
    recipe_search(searchQuery text, numResults int)
returns table(
            recipeId int,
            recipe_name text,
            nutrition text,
            score real)
as $$
declare
    query_embedding vector(1536);
begin
    query_embedding := (azure_openai.create_embeddings('text-embedding-ada-002', searchQuery));
    return query
    select
        r.rid,
        r.recipe_name,
        r.nutrition,
        (r.embedding <=> query_embedding)::real as score
    from
        recipes r
    order by score asc limit numResults; -- cosine distance
end $$
language plpgsql;
```

Now just invoke the function to search:

```sql
select recipeid, recipe_name, score from recipe_search('vegan recipes', 10);
```

And explore the results:

```bash
 recipeid |                         recipe_name                          |   score
----------+--------------------------------------------------------------+------------
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

## Related content

- [Integrate Azure Database for PostgreSQL flexible server with Azure Cognitive Services](generative-ai-azure-cognitive.md).
- [Generate vector embeddings in Azure Database for PostgreSQL flexible server with locally deployed LLM (Preview)](generative-ai-azure-local-ai.md).
- [Integrate Azure Database for PostgreSQL with Azure Machine Learning Services](generative-ai-azure-machine-learning.md).
- [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL flexible server](generative-ai-azure-openai.md).
- [Azure AI extension in Azure Database for PostgreSQL flexible server](generative-ai-azure-overview.md).
- [Generative AI with Azure Database for PostgreSQL flexible server](generative-ai-overview.md).
- [Recommendation System with Azure Database for PostgreSQL flexible server and Azure OpenAI](generative-ai-recommendation-system.md).
- [Enable and use pgvector in Azure Database for PostgreSQL flexible server](how-to-use-pgvector.md).
