---
title: Semantic Operators in the Azure AI Extension
description: Overview of semantic operator capabilities in the azure_ai extension for Azure Database for PostgreSQL. These operators bring advanced Generative AI (GenAI) functionality directly into SQL workflows, bringing intelligent, model-driven processing natively into the database.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 01/20/2026
ms.service: azure-database-postgresql
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.custom:
  - build-2025
# customer intent: As a user, I want to understand the available Semantic Operators in the azure_ai extension for Azure Database for PostgreSQL flexible server instances, explore their use cases, and learn how to use them effectively.
---

# Semantic operators in the Azure AI extension (Preview)

The Azure AI extension introduces **Semantic Operators**, a feature that integrates advanced Generative AI (GenAI) capabilities directly into PostgreSQL SQL. By using these operators, which models like chat completion and other [Azure AI deployments](https://azure.microsoft.com/products/ai-model-catalog), developers can build GenAI-driven applications directly within their databases. This integration unlocks new capabilities for understanding text, reasoning, and generating structured outputs.

## Key features

The Semantic Operators provide users with four core SQL functions that use generative AI capabilities:

- `azure_ai.generate()`: Generates text or structured output using Large Language Models (LLMs).
- `azure_ai.is_true()`: Evaluates the likelihood that a given statement is true.
- `azure_ai.extract()`: Extracts structured features or entities from text.
- `azure_ai.rank()`: Reranks a list of documents based on relevance to a given query.

Each function operates through AI Foundry endpoints registered by using the `azure_ai.set_setting` function, ensuring seamless integration and user control.

## Understanding semantic operators

Semantic Operators in the Azure AI extension simplify complex AI-driven tasks directly within your PostgreSQL database. By using these operators, you can seamlessly integrate generative AI capabilities into your SQL workflows. You can perform advanced text generation, truth evaluation, entity extraction, and document ranking. Each operator is optimized for ease of use and flexibility, so you can build intelligent applications with minimal effort.

### `azure_ai.generate()`

Use this operator to generate text or structured output by using LLMs.

It supports the following input parameters:

| Argument | Type | Description |
| --- | --- | --- |
| `prompt` | `text` | User prompt to send to the LLM. |
| `json_schema` (optional) | `JsonB` `DEFAULT ''` | JSON schema of the structured output you want the LLM response to follow. Must follow the [OpenAI notation for structured output](https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses). |
| `model` (optional) | `text` `DEFAULT "gpt-4.1"` | Name of the model deployment in Azure AI Foundry. |
| `system_prompt` (optional) | `text` `DEFAULT "You are a helpful assistant."` | System prompt to send to the LLM. |

By default, the operator returns a `text` value containing the generated response. If you provide the `json_schema` argument, the operator returns the output as a structured `JsonB` object that conforms to the specified schema.

**Example usage:**

```sql
SELECT azure_ai.generate(
  'Rewrite the following comment to be more polite: ' comment_text
) AS polite_comment
FROM user_comments;

SELECT review, azure_ai.generate(
    prompt        => 'Rewrite the following comment to be more polite and return the number of products mentioned:' || review,
    json_schema   => '{
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
     model  => 'gpt-4.1-mini'
) as polite_comment_with_count
FROM
    Reviews;
```

### `azure_ai.is_true()`

This operator evaluates the likelihood that a given statement is true. It returns a `boolean` value or `NULL` if the result is inconclusive.

It supports the following input parameters:

| Argument | Type | Description |
| --- | --- | --- |
| `statement` | `text` | Statement to evaluate as true or false. |
| `model` (optional) | `text` `DEFAULT "gpt-4.1"` | Name of the model deployment in Azure AI Foundry. |

**Example usage:**

```sql
SELECT azure_ai.is_true(
  'The review talks about the product: '
  product_name
  ' Review: '
  review_text
) AS is_relevant_review
FROM product_reviews;
```

### `azure_ai.extract()`

Use this operator to extract structured features or entities from text based on user-defined labels.

It supports the following input parameters:

| Argument | Type | Description |
| --- | --- | --- |
| `document` | `text` | A document containing the entities and features. |
| `data` | `array[text]` | An array of labels or feature names, where each entry represents a distinct entity type to extract from the input text. |
| `model` (optional) | `text` `DEFAULT "gpt-4.1"` | Name of the model deployment in Azure AI Foundry. |

The operator returns a `JsonB` object containing the extracted entities mapped to their corresponding labels.

**Example usage**:

```sql
SELECT azure_ai.extract(
   'The headphones are not great. They have a good design, but the sound quality is poor and the battery life is short.',
   ARRAY[ 'product', 'sentiment']
);

-- Output: {"product": "headphones", "sentiment": "negative"}

SELECT azure_ai.extract(
    'The music quality is good, though the call quality could have been better. The design is sleek, but still slightly heavy for convenient travel.',
    ARRAY[
        'design: string - comma separated list of design features of the product',
        'sound: string - sound quality (e.g., music, call, noise cancellation) of the product',
        'sentiment: number - sentiment score of the review; 1 (lowest) to 5 (highest)'
    ]
);

-- Output: {"sound": "music quality is good, call quality could have been better", "design": "sleek, slightly heavy", "sentiment": 3}
```

### `azure_ai.rank()`

Use this operator to rerank documents based on their relevance to a given query. It supports cross-encoder and GPT models.

It supports the following input parameters:

| Argument | Type | Description |
| --- | --- | --- |
| `query` | `text` | The search string used to evaluate and rank the relevance of each document. |
| `document_contents` | `array[text]` | An array of documents to be reranked. |
| `document_ids` (optional) | `array` | An array of document identifiers corresponding to the input documents. |
| `model` (optional) | `text` `DEFAULT "cohere-rerank-v3.5"` | Name of the model deployment in Azure AI Foundry. Supports both cross-encoder and GPT-based models. |

The operator returns a `table` containing the document ID, its rank, and the associated relevance score.

**Example usage:**

```sql
SELECT azure_ai.rank(
    'Best headphones for travel',
    ARRAY[
        'The headphones are lightweight and foldable, making them easy to carry.',
        'Bad battery life, not so great for long trips.',
        'The sound quality is excellent, with good noise isolation.'
    ]
)

SELECT azure_ai.rank(
  query => 'Clear calling capability that blocks out background noise',
  document_contents => ARRAY[
                        'The product has a great battery life, good design, and decent sound quality.',
                        'These headphones are perfect for long calls and music.',
                        'Best headphones for music lovers. Call quality could have been better.',
                        'The product has a good design, but it is a bit heavy. Not recommended for travel.'
                      ],
  document_ids => ARRAY['Review1', 'Review2', 'Review3', 'Review4'],
  model => 'gpt-4.1'
) AS ranked_reviews;
```

## How to get started

To use Semantic Operators in your PostgreSQL database, follow these steps:

### Setup for `.generate()`, `.extract()`, and `.is_true()` operators

These operators support chat completion models and default to [`gpt-4.1`](/azure/ai-foundry/openai/concepts/models#gpt-41-series).

1. **[Enable the `azure_ai` extension](generative-ai-azure-overview.md#enable-the-azure_ai-extension)** on your Azure Database for PostgreSQL flexible server instance.
1. [Create an Azure OpenAI service resource](/azure/ai-services/openai/how-to/create-resource) and **deploy a chat completion model** (for example, [`gpt-4.1`](/azure/ai-foundry/openai/concepts/models#gpt-41-series)). Alternatively, you can deploy and manage models through the intuitive experiences provided by [Azure AI Foundry](/azure/ai-foundry/quickstarts/get-started-code#start-with-a-project-and-model).
1. Note the Azure OpenAI **endpoint URL** and **API key**.
1. **Configure access**:

   To enable the `azure_ai` extension to invoke this model by using subscription key authentication, run the following SQL commands:

   ```sql
   SELECT azure_ai.set_setting('azure_openai.endpoint', 'https://<endpoint>.openai.azure.com/');
   SELECT azure_ai.set_setting('azure_openai.subscription_key', '<API Key>');
   ```

   If you want to use managed identities instead, refer to [this article](generative-ai-enable-managed-identity-azure-ai.md) to perform the following steps:
   - Enable system-assigned managed identity for your Azure Database for PostgreSQL flexible server instance and restart the server.
   - Assign the "Cognitive Services OpenAI User" role to the managed identity to interact with the Azure OpenAI resource.
   - Set the `azure_openai.auth_type` to 'managed-identity'.
   - Set the `azure_openai.endpoint` with the endpoint URL.

1. You're now all set to invoke the `.generate()`, `.is_true()`, and `.extract()` operators.

   Example usage with `gpt-4.1` (default):

   ```sql
   SELECT name, azure_ai.generate(
     'Generate a description for the product: ' || name
   ) AS description
   FROM products;
   ```

   Example usage with other models:

   ```sql
   SELECT name, azure_ai.generate(
     'Generate a description for the product: ' || name , 'gpt-4.1-mini'
   ) AS description
   FROM products;
   ```

### Setup for `.rank()` operator

The `.rank()` operator supports both cross encoder and chat completion models. It defaults to the cross encoder [`Cohere-rerank-v3.5`](/azure/ai-foundry/concepts/models-inference-examples#cohere-rerank).

Using `Cohere-rerank-v3.5` cross-encoder:

1. **[Enable the `azure_ai` extension](generative-ai-azure-overview.md#enable-the-azure_ai-extension)** on your Azure Database for PostgreSQL instance.
1. Go to Azure AI Foundry and **[deploy the `Cohere-rerank-v3.5` model](https://ai.azure.com/explore/models?&selectedCollection=cohere)** by using the Serverless API purchase option.
1. Note the model's **endpoint key and the Reranker API route**. It should look something like this: `https://<deployment name>.<region>.models.ai.azure.com/<v1 or v2>/rerank`.
1. **Configure access**:

   To enable the `azure_ai` extension to invoke this model by using subscription key authentication, run the following SQL commands:

   ```sql
   SELECT azure_ai.set_setting('azure_ml.serverless_ranking_endpoint', '<Cohere reranker API>');
   SELECT azure_ai.set_setting('azure_ml.serverless_ranking_endpoint_key', '<API Key>');
   ```

   If you want to use managed identities instead, refer to [this article](generative-ai-enable-managed-identity-azure-ai.md) to perform the following steps:
   - Enable system-assigned managed identity for your Azure Database for PostgreSQL flexible server instance and restart the server.
   - Assign the "Azure Machine Learning Data Scientist" role to the managed identity to interact with the Cohere model.
   - Set the `azure_ml.auth_type` to 'managed-identity'.
   - Set the `azure_ml.serverless_ranking_endpoint` with the Cohere reranker API.

1. You're now all set to invoke the `.rank()` operator by using Cohere reranker model.

   ```sql
   SELECT azure_ai.rank(
     'Best headphones for travel',
     ARRAY[
         'The headphones are lightweight and foldable, making them easy to carry.',
         'Bad battery life, not so great for long trips.',
         'The sound quality is excellent, with good noise isolation.'
     ]
   ) AS ranked_reviews;
   ```

To use the `.rank()` operator with chat completion models like `gpt-4.1`, deploy the desired model on Azure OpenAI, configure the `azure_ai` extension with the model's endpoint details, and specify the model name when invoking the operator.

```sql
SELECT azure_ai.set_setting('azure_openai.endpoint', 'https://<endpoint>.openai.azure.com/');
SELECT azure_ai.set_setting('azure_openai.subscription_key', '<API Key>');

SELECT azure_ai.rank(
 'Best headphones for travel',
  ARRAY[
      'The headphones are lightweight and foldable, making them easy to carry.',
      'Bad battery life, not so great for long trips.',
      'The sound quality is excellent, with good noise isolation.'
  ],
  'gpt-4.1'
) AS ranked_reviews;
```

## Related content

- [Generative AI with Azure Database for PostgreSQL](generative-ai-overview.md)
- [Azure AI extension in Azure Database for PostgreSQL](generative-ai-azure-overview.md)
- [Vector stores in Azure Database for PostgreSQL](generative-ai-vector-databases.md)
- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-postgresql)
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
