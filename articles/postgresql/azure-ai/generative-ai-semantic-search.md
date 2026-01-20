---
title: Create a Semantic Search with Azure OpenAI
description: Learn how to build a semantic search application by using Azure Database for PostgreSQL and Azure OpenAI.
author: mulander
ms.author: adamwolk
ms.reviewer: maghan
ms.date: 01/20/2026
ms.service: azure-database-postgresql
ms.topic: tutorial
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
---

# Tutorial: Create a semantic search with Azure Database for PostgreSQL and Azure OpenAI

This hands-on tutorial shows you how to build a semantic search application by using Azure Database for PostgreSQL and Azure OpenAI.

Semantic search does searches based on semantics. Standard lexical search does searches based on keywords provided in a query. For example, your recipe dataset might not contain labels like gluten-free, vegan, dairy-free, fruit-free, or dessert, but you can deduce these characteristics from the ingredients. The idea is to issue such semantic queries and get relevant search results.

In this tutorial, you:

> [!div class="checklist"]
> - Identify the search scenarios and the data fields that are involved in a search.
> - For every data field involved in a search, create a corresponding vector field to store the embeddings of the value stored in the data field.
> - Generate embeddings for the data in the selected data fields and store the embeddings in their corresponding vector fields.
> - Generate the embedding for any input search query.
> - Search the vector data field and list the nearest neighbors.
> - Run the results through appropriate relevance, ranking, and personalization models to produce the final ranking. In the absence of such models, rank the results in decreasing dot-product order.
> - Monitor the model, results quality, and business metrics, such as select-through rate and dwell time. Incorporate feedback mechanisms to debug and improve the search stack, from data quality, data freshness, and personalization to user experience.

## Prerequisites

1. Create an OpenAI account and [request access to Azure OpenAI](https://aka.ms/oai/access).
1. Get access to Azure OpenAI in the desired subscription.
1. Get permissions to [create Azure OpenAI resources and to deploy models](/azure/ai-services/openai/how-to/role-based-access-control).
1. [Create and deploy an Azure OpenAI resource and a model](/azure/ai-services/openai/how-to/create-resource). Deploy the embeddings model [text-embedding-ada-002](/azure/ai-services/openai/concepts/models#embeddings-models). Copy the deployment name, because you need it to create embeddings.

## Enable the azure_ai and pgvector extensions

Before you can enable `azure_ai` and `pgvector` on your Azure Database for PostgreSQL flexible server instance, [add them to your allow list](../extensions/how-to-allow-extensions.md). Make sure that they're correctly added by running `SHOW azure.extensions;`.

Then you can install the extension by connecting to your target database and running the [CREATE EXTENSION](https://www.postgresql.org/docs/current/static/sql-createextension.html) command. Repeat the command separately for every database where you want the extension to be available.

```sql
CREATE EXTENSION azure_ai;
CREATE EXTENSION vector;
```

## Configure an OpenAI endpoint and key

In Azure AI services, under **Resource Management** > **Keys and Endpoints**, you can find the endpoint and the keys for your Azure AI resource. Use the endpoint and one of the keys to enable the `azure_ai` extension to invoke the model deployment:

```sql
select azure_ai.set_setting('azure_openai.endpoint','https://<endpoint>.openai.azure.com');
select azure_ai.set_setting('azure_openai.subscription_key', '<API Key>');
```

## Download the data

Download the data from [Kaggle](https://www.kaggle.com/datasets/thedevastator/better-recipes-for-a-better-life).

## Create the table

Connect to your server and create a `test` database. In that database, use the following command to create a table where you import data:

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

## Import the data

Set the following environment variable on the client window to set encoding to UTF-8. This step is necessary because this particular dataset uses Windows-1252 encoding.

```cmd
Rem on Windows
Set PGCLIENTENCODING=utf-8;
```

```bash
# on Unix based operating systems
export PGCLIENTENCODING=utf-8
```

Import the data into the table that you created. This dataset contains a header row.

```bash
psql -d <database> -h <host> -U <user> -c "\copy recipes FROM <local recipe data file> DELIMITER ',' CSV HEADER"
```

## Add a column to store the embeddings

Add an embedding column to the table:

```sql
ALTER TABLE recipes ADD COLUMN embedding vector(1536);
```

## Generate embeddings

Generate embeddings for your data by using the `azure_ai` extension. The following example vectorizes a few fields and concatenates them.

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

Repeat the command until there are no more rows to process.

> [!TIP]  
> Experiment with the `LIMIT` value. If you set a high value, Azure OpenAI might throttle the request and cause the statement to fail halfway through. If the statement fails, wait for at least one minute and run the command again.

## Search

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

Explore the results:

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

- [Integrate Azure Database for PostgreSQL with Azure Cognitive Services](generative-ai-azure-cognitive.md)
- [Integrate Azure Database for PostgreSQL with Azure Machine Learning services](generative-ai-azure-machine-learning.md)
- [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL](generative-ai-azure-openai.md)
- [Azure AI extension in Azure Database for PostgreSQL](generative-ai-azure-overview.md)
- [Generative AI with Azure Database for PostgreSQL](generative-ai-overview.md)
- [Create a recommendation system with Azure Database for PostgreSQL and Azure OpenAI](generative-ai-recommendation-system.md)
- [Enable and use pgvector in Azure Database for PostgreSQL](../extensions/how-to-use-pgvector.md)
