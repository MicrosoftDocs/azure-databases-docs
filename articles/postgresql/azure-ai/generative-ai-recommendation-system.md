---
title: Create a Recommendation System with Azure OpenAI
description: Learn how to build a recommendation system by using Azure Database for PostgreSQL and Azure OpenAI.
author: mulander
ms.author: adamwolk
ms.reviewer: maghan
ms.date: 01/20/2026
ms.service: azure-database-postgresql
ms.subservice: ai-generative
ms.topic: tutorial
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
---

# Tutorial: Create a recommendation system with Azure Database for PostgreSQL and Azure OpenAI

This hands-on tutorial shows you how to build a recommender application by using Azure Database for PostgreSQL and Azure OpenAI. Recommendations have applications in different domains. Service providers tend to provide recommendations for products and services that they offer based on prior history and contextual information collected from the customer and environment.

There are various ways to model recommendation systems. This tutorial explores the simplest form: a recommendation based on a product that corresponds to (for example) a prior purchase. This tutorial uses the recipe dataset that the [tutorial for semantic search](generative-ai-semantic-search.md) uses. The recommendation is for recipes based on a recipe that a customer liked or searched for in the past.

## Prerequisites

1. Create an OpenAI account and [request access to Azure OpenAI](https://aka.ms/oai/access).
1. Grant access to Azure OpenAI in the desired subscription.
1. Grant permissions to [create Azure OpenAI resources and to deploy models](/azure/ai-services/openai/how-to/role-based-access-control).
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

```shell
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

Generate embeddings for your data by using the `azure_ai` extension. The following example vectorizes a few fields and is concatenated.

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
> Experiment with the `LIMIT` value. With a high value, Azure OpenAI might throttle the statement and cause it to fail halfway through. If the statement fails, wait for at least one minute and run the command again.

## Search

Create a search function in your database for convenience:

```sql
create function
    recommend_recipe(sampleRecipeId int, numResults int)
returns table(
            out_recipeName text,
            out_nutrition text,
            out_similarityScore real)
as $$
declare
    queryEmbedding vector(1536);
    sampleRecipeText text;
begin
    sampleRecipeText := (select
                            recipe_name||' '||cuisine_path||' '||ingredients||' '||nutrition||' '||directions
                        from
                            recipes where rid = sampleRecipeId);

    queryEmbedding := (azure_openai.create_embeddings('text-embedding-ada-002',sampleRecipeText));

    return query
    select
        distinct r.recipe_name,
        r.nutrition,
        (r.embedding <=> queryEmbedding)::real as score
    from
        recipes r
    order by score asc limit numResults; -- cosine distance
end $$
language plpgsql;
```

Now just invoke the function to search for the recommendation:

```sql
select out_recipename, out_similarityscore from recommend_recipe(1, 20); -- search for 20 recipe recommendations that closest to recipeId 1
```

And explore the results:

```output
            out_recipename             | out_similarityscore
---------------------------------------+---------------------
 Apple Pie by Grandma Ople             |                   0
 Easy Apple Pie                        |          0.05137232
 Grandma's Iron Skillet Apple Pie      |         0.054287136
 Old Fashioned Apple Pie               |         0.058492836
 Apple Hand Pies                       |          0.06449003
 Apple Crumb Pie                       |          0.07290977
 Old-Fashioned Apple Dumplings         |         0.078374185
 Fried Apple Pies                      |          0.07918481
 Apple Pie Filling                     |         0.084320426
 Apple Turnovers                       |          0.08576391
 Dutch Apple Pie with Oatmeal Streusel |          0.08779895
 Apple Crisp - Perfect and Easy        |          0.09170883
 Delicious Cinnamon Baked Apples       |          0.09384012
 Easy Apple Crisp with Pie Filling     |          0.09477234
 Jump Rope Pie                         |          0.09503954
 Easy Apple Strudel                    |         0.095167875
 Apricot Pie                           |          0.09634114
 Easy Apple Crisp with Oat Topping     |          0.09708358
 Baked Apples                          |          0.09826993
 Pear Pie                              |         0.099974394
(20 rows)
```

## Related content

- [Integrate Azure Database for PostgreSQL with Azure Cognitive Services](generative-ai-azure-cognitive.md)
- [Integrate Azure Database for PostgreSQL with Azure Machine Learning services](generative-ai-azure-machine-learning.md)
- [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL](generative-ai-azure-openai.md)
- [Azure AI extension in Azure Database for PostgreSQL](generative-ai-azure-overview.md)
- [Generative AI with Azure Database for PostgreSQL](generative-ai-overview.md)
- [Create a semantic search with Azure Database for PostgreSQL and Azure OpenAI](generative-ai-recommendation-system.md)
- [Enable and use pgvector in Azure Database for PostgreSQL](../extensions/../extensions/how-to-use-pgvector.md)
