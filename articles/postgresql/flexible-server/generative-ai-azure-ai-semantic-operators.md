---
title: What are Semantic Operators? 
description: Overview Semantic Operator capabilities in the azure_ai extension for Azure Database for PostgreSQL.
author: jojohnso-msft
ms.author: jojohnso
ms.reviewer: maghan
ms.date: 05/19/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
ms.custom:
  - build-2025
# customer intent: As a user, I want to understand what Semantic Operators are available in the azure_ai extension for Azure Database for PostgreSQL flexible server.
---

# Overview of Semantic Operators in the Azure AI Extension

## Introducing Advanced Generative AI Capabilities in Postgres SQL

### Introduction

The Azure AI extension introduces Semantic Operators, a groundbreaking feature that integrates advanced Generative AI (GenAI) functionality directly into Postgres SQL. Powered by Azure OpenAI chat completion APIs, these operators allow users to explore innovative ways of building GenAI applications directly within their databases. 

### Key Features

The Semantic Operators provide users with four core SQL functions that leverage generative AI capabilities:

- **azure_ai.generate()**: Generates text or structured output using LLMs.
- **azure_ai.is_true()**: Evaluates the likelihood that a given statement is true.
- **azure_ai.extract()**: Extracts structured features or entities from text.
- **azure_ai.rank()**: Re-ranks a list of documents based on relevance to a given query.

Each function operates via AI Foundry endpoints registered using the `azure_ai.set_setting` function, ensuring seamless integration and user control. 

### Operator Details

#### azure_ai.generate()

This function uses LLMs to generate text or structured output and supports custom parameters such as prompts, JSON schema, model selection, temperature, timeout, and retry logic.

Example usage:
```sql
SELECT azure_ai.generate(
  'Rewrite the following comment to be more polite: ' 
  comment_text
) AS polite_comment
FROM user_comments;
```

#### azure_ai.is_true()

This operator evaluates whether a given statement is likely true, returning a boolean value or NULL if inconclusive.

Example usage:
```sql
SELECT azure_ai.is_true(
  'The review talks about product: ' 
  product_name 
  ' Review: ' 
  review_text
) AS is_relevant_review
FROM product_reviews;
```

#### azure_ai.extract()

Extracts structured features or entities from text based on user-defined labels.

Example usage:
```sql
SELECT azure_ai.extract(
  'Alice Smith traveled to Paris.',
  ARRAY['person', 'location', 'action']
);
-- Output: {"person": "Alice Smith", "location": "Paris", "action": "travel"}
```

#### azure_ai.rank()

Re-ranks documents based on relevance to a query, supporting both cross-encoder and GPT models.

Example usage:
```sql
SELECT azure_ai.rank(
  'how to care for indoor succulents',
  ARRAY[
    'A complete guide to watering succulents.',
    'Best outdoor plants for shade.',
    'Soil mixtures for cacti and succulents.'
  ]
) AS ranked_documents;
```
