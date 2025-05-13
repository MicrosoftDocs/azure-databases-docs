---
title: What Are Semantic Operators?
description: Overview Semantic Operator capabilities in the azure_ai extension for Azure Database for PostgreSQL.
author: jojohnso-msft
ms.author: jojohnso
ms.reviewer: maghan
ms.date: 05/19/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.custom:
  - build-2025
# customer intent: As a user, I want to understand what Semantic Operators are available in the azure_ai extension for Azure Database for PostgreSQL flexible server.
---

# Semantic operators in the Azure AI extension Preview

The Azure AI extension introduces Semantic Operators, a groundbreaking feature integrating advanced Generative AI (GenAI) functionality directly into PostgreSQL SQL. With Azure OpenAI chat completion APIs, these operators allow users to explore innovative ways of building GenAI applications directly within their databases.

## Key features

The Semantic Operators provide users with four core SQL functions that use generative AI capabilities:

- **azure_ai.generate()**: Generates text or structured output using (Large Language Models (LLMs).
- **azure_ai.is_true()**: Evaluates the likelihood that a given statement is true.
- **azure_ai.extract()**: Extracts structured features or entities from text.
- **azure_ai.rank()**: Reranks a list of documents based on relevance to a given query.

Each function operates via AI Foundry endpoints registered using the `azure_ai.set_setting` function, ensuring seamless integration and user control.

## Understanding semantic operators

Semantic Operators in the Azure AI extension are designed to simplify complex AI-driven tasks directly within your PostgreSQL database. These operators allow users to seamlessly integrate generative AI capabilities into their SQL workflows, enabling advanced text generation, truth evaluation, entity extraction, and document ranking. Each operator is optimized for ease of use and flexibility, allowing developers to build intelligent applications with minimal effort.

### azure_ai.generate()

This function uses LLMs to generate text or structured output and supports custom parameters such as prompts, JSON schema, model selection, temperature, time-out, and retry logic.

Example usage:

```sql
SELECT azure_ai.generate(
  'Rewrite the following comment to be more polite: '
 comment_text
) AS polite_comment
FROM user_comments;
```

### azure_ai.is_true()

This operator evaluates whether a given statement is likely true, returning a boolean value or NULL if inconclusive.

Example usage:

```sql
SELECT azure_ai.is_true(
  'The review talks about the product: '
 product_name
  ' Review: '
 review_text
) AS is_relevant_review
FROM product_reviews;
```

### azure_ai.extract()

Extract structured features or entities from text based on user-defined labels.

Example usage:

```sql
SELECT azure_ai.extract(
  'Alice Smith traveled to Paris.',
 ARRAY['person', 'location', 'action']
);
-- Output: {"person": "Alice Smith", "location": "Paris", "action": "travel"}
```

### azure_ai.rank()

Reranks documents based on query relevance, supporting cross-encoder and GPT models.

Example usage:

```sql
SELECT azure_ai.rank(
  'How to Care for Indoor Succulents',
 ARRAY[
    'A complete guide to watering succulents.',
    'Best outdoor plants for shade.',
    'Soil mixtures for cacti and succulents.'
 ]
) AS ranked_documents;
```

## Related content

- [Azure Database for PostgreSQL documentation](overview.md)
- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-postgresql)
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
- [MSSQL extension for Visual Studio Code?](/sql/tools/visual-studio-code-extensions/mssql/mssql-extension-visual-studio-code)
