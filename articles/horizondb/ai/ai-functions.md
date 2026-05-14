---
title: AI functions in the azure_ai extension for Azure HorizonDB
description: Overview of AI functions in the azure_ai extension for Azure HorizonDB. These functions bring advanced Generative AI (GenAI) functionality directly into SQL workflows, bringing intelligent, model-driven processing natively into the database.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: ai-semantic-operators
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
# customer intent: As a user, I want to understand the available AI functions in the azure_ai extension for Azure HorizonDB, explore their use cases, and learn how to use them effectively.
---

# AI functions in the azure_ai extension for Azure HorizonDB (Preview)

The `azure_ai` extension introduces **AI functions**, a feature that integrates advanced Generative AI (GenAI) capabilities directly into PostgreSQL SQL. By using these functions with models like chat-completion, embeddings, reranking, and other [Microsoft Foundry model deployments](https://azure.microsoft.com/products/ai-model-catalog), you can build GenAI-driven applications directly within your database. This integration unlocks new capabilities for generating vector embeddings, reranking vector search results, understanding text, reasoning, and generating structured outputs.

## Key features

The AI functions provide five core SQL functions that use generative AI capabilities:

- `azure_ai.generate()`: Generates text or structured output using Large Language Models (LLMs).
- `azure_ai.is_true()`: Evaluates the likelihood that a given statement is true.
- `azure_ai.extract()`: Extracts structured features or entities from text.
- `azure_ai.rank()`: Reranks a list of documents based on relevance to a given query.
- `azure_openai.create_embeddings()`: Creates vector embeddings for a given input text.

Each function operates through model endpoints registered in the model registry or through Managed Models provisioned by [AI Model Management](ai-model-management.md), ensuring seamless integration and user control.

## Enable the azure_ai extension and register models

Before you can use AI functions, you need to enable the `azure_ai` extension and register the AI models you want to use.

### Option 1: Use AI Model Management

[AI Model Management in Azure HorizonDB](ai-model-management.md) provides a turn-key experience that, when enabled on your Azure HorizonDB instance, automatically:

1. Installs and configures the `azure_ai` extension.
1. Provisions and registers three Managed Models:

   - `gpt-5.4` for chat completion (alias: `default-chat`).
   - `text-embedding-3-small` for embeddings (alias: `default-embedding`).
   - `Cohere-rerank-v4.0-fast` for reranking (alias: `default-reranker`).
1. Establishes secure connections to the model endpoints.

After you enable AI Model Management, you can immediately start using AI functions without additional configuration.

### Option 2: Manual setup with model registry

If you prefer to use your own Microsoft Foundry models (Bring Your Own Model), follow these steps:

1. Install the `azure_ai` extension on your database by running the following command:

   ```sql
   CREATE EXTENSION IF NOT EXISTS azure_ai;
   ```

   > [!TIP]  
   > If the extension is already installed, verify you're on the latest version and upgrade if needed:
   >
   > ```sql
   > SELECT * FROM pg_available_extensions WHERE name = 'azure_ai';
   > ALTER EXTENSION azure_ai UPDATE;
   > ```

1. Deploy a model through [Microsoft Foundry](/azure/ai-foundry/quickstarts/get-started-code#start-with-a-project-and-model). Select the model you want to use (for example, `gpt-5.4` or `text-embedding-3-small`) and complete the deployment.

1. In the Microsoft Foundry dashboard, navigate to your project and note the **API key** and the **Azure OpenAI endpoint URL**, which looks like `https://<your-resource-name>.openai.azure.com/`.

1. Navigate to your model deployment and note the following:
   - **Deployment name**: The name you assigned during deployment (for example, `gpt-5-deployment`).
   - **Model name**: The underlying model name (for example, `gpt-5.4`).

1. Register the model in the model registry.

   **Syntax:**

   ```sql
   SELECT model_registry.model_add(
       '<model-alias>',              -- a unique, custom identifier for your model
       '<endpoint-URL>',             -- the Azure OpenAI endpoint URL (ending in .openai.azure.com/)
       '<deployment-name>',          -- the deployment name of your model
       '<model-name>',               -- the model name (for example, gpt-5.4, text-embedding-3-small)
       '<API-version>',              -- the API version (NULL for latest)
       '<auth-type>',                -- subscription-key or managed-identity
       '<endpoint-key>'              -- endpoint key (NULL if using managed-identity)
   );
   ```

   **Example:**

   ```sql
   SELECT model_registry.model_add(
       'my-gpt',
       'https://my-endpoint.openai.azure.com/',
       'gpt-5-deployment',
       'gpt-5',
       '2025-01-01-preview',
       'subscription-key',
       '<your-endpoint-key>'
   );
   ```

1. You're now ready to invoke AI functions by using your registered model alias.

> [!TIP]  
> You can also register models with Azure API Management (APIM) endpoints to route requests through APIM for load balancing, monitoring, or policy enforcement.

### View registered models

To view all models registered in the model registry, run:

```sql
SELECT * FROM model_registry.model_list_all();
```

## Use AI functions

AI functions in the `azure_ai` extension simplify complex AI-driven tasks directly within your PostgreSQL database. You can seamlessly integrate generative AI capabilities into your SQL workflows to perform advanced text generation, truth evaluation, entity extraction, document ranking, and vector embedding creation. Each function is optimized for ease of use and flexibility, so you can build intelligent applications with minimal effort.

> [!TIP]  
> The `model` (model alias) parameter is optional in all AI functions. When you omit it, the function automatically uses the corresponding default Managed Model (`default-chat`, `default-embedding`, or `default-reranker`) provisioned by [AI Model Management in Azure HorizonDB](ai-model-management.md).

### `azure_openai.create_embeddings()`

Use this function to create vector embeddings for a given input text. Vector embeddings are numerical representations of text that capture semantic meaning, enabling similarity search, clustering, and other vector-based operations.

It supports the following input parameters:

| Argument | Type | Description |
| --- | --- | --- |
| `model` (optional) | `text` | Model alias registered in the model registry. When omitted, uses the `default-embedding` Managed Model. |
| `input` | `text` | Input text to generate embeddings for. |

The function returns a vector representation of the input text.

**Example usage:**

```sql
SELECT azure_openai.create_embeddings(
    'my-embedding',                         -- model alias
    'Alternatives to Lego'
) AS embedding_vector;
```

**Generate and store embeddings for a table column:**

```sql
ALTER TABLE products
ADD COLUMN description_vector vector(1536);

UPDATE products SET description_vector = azure_openai.create_embeddings(
    'my-embedding',                         -- model alias
    product_description                     -- input text
)::vector
WHERE description_vector IS NULL;
```

**Perform vector search with `create_embeddings()`:**

```sql
SELECT product_name, product_description
FROM products
ORDER BY description_vector <=> azure_openai.create_embeddings(
    'my-embedding',                         -- model alias
    'Alternatives to LEGO'                  -- search query
)::vector ASC
LIMIT 10;
```

### `azure_ai.generate()`

Use this function to generate text or structured output by using LLMs.

It supports the following input parameters:

| Argument | Type | Description |
| --- | --- | --- |
| `prompt` | `text` | User prompt to send to the LLM. |
| `model` (optional) | `text` | Model alias registered in the model registry. When omitted, uses the `default-chat` Managed Model. |
| `json_schema` (optional) | `JsonB` `DEFAULT ''` | JSON schema of the structured output you want the LLM response to follow. Must follow the [OpenAI notation for structured output](https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses). |
| `system_prompt` (optional) | `text` `DEFAULT 'You are a helpful assistant.'` | System prompt to send to the LLM. |

By default, the function returns a `text` value containing the generated response. If you provide the `json_schema` argument, the function returns the output as a structured `JsonB` object that conforms to the specified schema.

**Example usage:**

```sql
SELECT azure_ai.generate(
    'Rewrite the following comment to be more polite: ' || comment_text,
    'my-gpt'                             -- model alias
) AS polite_comment
FROM user_comments;
```

**Generate structured output with JSON schema:**

```sql
SELECT review, azure_ai.generate(
    prompt      => 'Rewrite the following comment to be more polite and return the number of products mentioned:' || review,
    json_schema => '{
                      "name": "generate_response",
                      "description": "Generate a response to the user",
                      "strict": true,
                      "schema": {
                        "type": "object",
                        "properties": {
                          "comment": { "type": "string" },
                          "num_products": { "type": "integer" }
                        },
                        "required": ["comment", "num_products"],
                        "additionalProperties": false
                      }
                    }',
    model       => 'my-gpt'             -- model alias
) AS polite_comment_with_count
FROM Reviews;
```

### `azure_ai.extract()`

Use this function to extract structured features or entities from text based on user-defined labels.

It supports the following input parameters:

| Argument | Type | Description |
| --- | --- | --- |
| `document` | `text` | A document containing the entities and features. |
| `data` | `array[text]` | An array of labels or feature names, where each entry represents a distinct entity type to extract from the input text. |
| `model` (optional) | `text` | Model alias registered in the model registry. When omitted, uses the `default-chat` Managed Model. |

The function returns a `JsonB` object containing the extracted entities mapped to their corresponding labels.

**Example usage:**

```sql
SELECT azure_ai.extract(
    'The headphones are not great. They have a good design, but the sound quality is poor and the battery life is short.',
    ARRAY['product', 'sentiment'],
    'my-gpt'                             -- model alias
);

-- Output: {"product": "headphones", "sentiment": "negative"}
```

**Extract with detailed labels:**

```sql
SELECT azure_ai.extract(
    'The music quality is good, though the call quality could have been better. The design is sleek, but still slightly heavy for convenient travel.',
    ARRAY[
        'design: string - comma separated list of design features of the product',
        'sound: string - sound quality (e.g., music, call, noise cancellation) of the product',
        'sentiment: number - sentiment score of the review; 1 (lowest) to 5 (highest)'
    ],
    'my-gpt'                            -- model alias
);

-- Output: {"sound": "music quality is good, call quality could have been better", "design": "sleek, slightly heavy", "sentiment": 3}
```

### `azure_ai.is_true()`

This function evaluates the likelihood that a given statement is true. It returns a `boolean` value or `NULL` if the result is inconclusive.

It supports the following input parameters:

| Argument | Type | Description |
| --- | --- | --- |
| `statement` | `text` | Statement to evaluate as true or false. |
| `model` (optional) | `text` | Model alias registered in the model registry. When omitted, uses the `default-chat` Managed Model. |

**Example usage:**

```sql
SELECT azure_ai.is_true(
    'The review talks about the product: ' || product_name || ' Review: ' || review_text,
    'my-gpt'                             -- model alias
) AS is_relevant_review
FROM product_reviews;
```

### `azure_ai.rank()`

Use this function to rerank documents based on their relevance to a given query. It supports cross-encoder and GPT models.

It supports the following input parameters:

| Argument | Type | Description |
| --- | --- | --- |
| `query` | `text` | The search string used to evaluate and rank the relevance of each document. |
| `document_contents` | `array[text]` | An array of documents to be reranked. |
| `document_ids` (optional) | `array` | An array of document identifiers corresponding to the input documents. |
| `model` (optional) | `text` | Model alias registered in the model registry. When omitted, uses the `default-reranker` Managed Model. |

The function returns a `table` containing the document ID, its rank, and the associated relevance score.

**Example usage:**

```sql
SELECT azure_ai.rank(    -- Alternatively, use SELECT * FROM azure_ai.rank(...) for a more readable rank result
    'Best headphones for travel',
    ARRAY[
        'The headphones are lightweight and foldable, making them easy to carry.',
        'Bad battery life, not so great for long trips.',
        'The sound quality is excellent, with good noise isolation.'
    ],
    'my-reranker'                       -- model alias
);
```

**Combine vector search with semantic reranking:**

```sql
WITH potential_toys AS (
    SELECT id AS product_id, title AS product_name, text_content AS product_description
    FROM products
    ORDER BY embedding <=> azure_openai.create_embeddings(
        input => 'Alternatives to LEGO'
    )::vector ASC
    LIMIT 10
),
reranked_results AS (
    SELECT
        id AS row_id, rank
    FROM azure_ai.rank(
        'Alternatives to LEGO',
        ARRAY(SELECT 'Product Description: ' || product_description FROM potential_toys),
        ARRAY(SELECT product_id FROM potential_toys),
        'my-reranker'                   -- model alias
    )
)
SELECT
    pt.product_id,
    pt.product_name
FROM potential_toys pt
LEFT JOIN reranked_results rr ON (rr.row_id = pt.product_id)
ORDER BY rr.rank ASC;
```

## Manage models in the model registry

The model registry provides a centralized interface for managing all AI model endpoints. You can register, update, and remove models by using SQL functions.

### Register a model

```sql
SELECT model_registry.model_add(
    '<model-alias>',                -- a unique, custom identifier for your model
    '<model-endpoint-URL>',         -- the Azure OpenAI endpoint URL (ending in .openai.azure.com/)
    '<model-deployment-name>',      -- the deployment name of your model
    '<model-name>',                 -- the model name (for example, gpt-5.4, text-embedding-3-small)
    '<API-version>',                -- the API version (NULL for latest)
    '<auth-type>',                  -- subscription-key or managed-identity
    '<model-endpoint-key>'          -- endpoint key (NULL if using managed-identity)
);
```

### Remove a model

```sql
SELECT model_registry.model_remove('<your-model-alias>');
```

### Update a model alias

```sql
SELECT model_registry.model_alias_update('<your-model-alias>', '<new-model-alias>');
```

### Update model metadata

Update individual or multiple metadata fields for a registered model:

```sql
SELECT model_registry.model_update(
    '<your-model-alias>',
    '{
        "endpoint": "<your-new-endpoint-URL>",
        "auth_type": "subscription-key",
        "model_name": "<your-new-model-name>",
        "deployment_name": "<your-new-deployment-name>",
        "api_version": "<your-new-api-version>"
    }'
);
```

### Update an API key

```sql
SELECT model_registry.model_key_update(
    '<your-model-alias>',
    '<your-new-endpoint-key>'
);
```

## User access management

When a model is registered, either by a user or through Managed Models (when AI Model Management is enabled), it's usable by all database users by default. You can explicitly manage and restrict access to models in the registry by using the `model_user_add`, `model_user_set`, and `model_user_remove` functions. This capability is useful for Bring Your Own Model (BYOM) entries, which might have associated costs or data privacy considerations.

### Roles

In addition to the built-in `azure_pg_admin` role, the `model_registry_manager` role has permissions to use, add, remove, and update models in the model registry, and manage user access to those models. A regular user can also register a model, and unless a specific user set is defined, the model remains accessible to all other users. Models can be updated either by the user who created them or by users with the appropriate privileges (`azure_pg_admin` or `model_registry_manager`).

**Assign the `model_registry_manager` role to a user:**

```sql
CREATE USER registry_manager;
GRANT model_registry_manager TO registry_manager;
```

### Grant access to specific users

Use `model_user_add` to grant a specific user access to a model:

```sql
SELECT model_registry.model_user_add('<your-model-alias>', 'target_user');
```

After you add at least one user, only the specified users can invoke AI functions with that model. Other users receive an error.

### Set a complete user access list

Use `model_user_set` to replace the entire access list for a model with a new set of users:

```sql
SELECT model_registry.model_user_set('<your-model-alias>', ARRAY['user1', 'user2']);
```

> [!IMPORTANT]  
> The `model_user_set` function removes any previously defined user access and replaces it with the new user set. Users not included in the new list lose access to the model.

### Verify user access

To verify a user's access, set the role and attempt to invoke an AI function:

```sql
SET ROLE target_user;
SELECT azure_ai.generate(
    'Rewrite the following comment to be more polite: This product is the worst.',
    'my-gpt'                         -- model alias
);
```

### Remove user access

Use `model_user_remove` to revoke a specific user's access to a model:

```sql
SELECT model_registry.model_user_remove('<your-model-alias>', 'target_user');
```

## Supported models

The following table lists the models supported by each AI function.

| Function | Supported models |
| --- | --- |
| `azure_ai.generate()` | All GPT and o-series models, except `gpt-5.4-pro`. |
| `azure_ai.extract()` | All GPT and o-series models, except `gpt-5.4-pro`. |
| `azure_ai.is_true()` | All GPT and o-series models, except `gpt-5.4-pro`. |
| `azure_openai.create_embeddings()` | `text-embedding-3-small`, `text-embedding-3-large`, `text-embedding-ada-002`. |
| `azure_ai.rank()` | All GPT models listed previously, `Cohere-rerank-v4.0-pro`, `Cohere-rerank-v4.0-fast`. |

## Related content

- [AI Model Management in Azure HorizonDB](ai-model-management.md)
- [Generate vector embeddings using the create_embeddings() AI function](generate-vector-embeddings.md)
- [Semantic reranking with the rank() function](semantic-reranking.md)
- [Extract knowledge graphs in Azure HorizonDB](build-knowledge-graph.md)
