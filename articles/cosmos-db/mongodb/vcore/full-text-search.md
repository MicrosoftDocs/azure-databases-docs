---
title: Integrated vector store
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Use the integrated vector store in Azure Cosmos DB for MongoDB vCore to enhance AI-based applications.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ MongoDB vCore
---

# Full-Text Search Capabilities in Azure Cosmos DB for MongoDB vCore

Azure Cosmos DB for MongoDB vCore provides **full-text search capabilities** by supporting MongoDB's `$text` query operator and text indexes. This allows developers to perform efficient search operations across one or more text fields within documents. This feature is suitable for use cases like blog search, product catalogs, and user-generated content.

## What is Text Search?

Text search refers to the ability to query and retrieve documents based on the content of their textual fields. Instead of relying on exact field-value matches, text search indexes the content of specified fields, allowing you to search for words, phrases, or patterns. Azure Cosmos DB for MongoDB vCore enables basic text search capabilities using the `$text` query operator.

This feature is especially useful for applications involving large amounts of text such as blogs, reviews, articles, or catalog metadata. It works by tokenizing the text (splitting it into individual words), applying stemming (reducing words to their root form), and indexing the results for fast lookups.

The underlying implementation in vCore uses PostgreSQL's TSVector approach to build the text index and supports many of the same query styles as MongoDB Atlas.

## Full-Text Search Feature Support

| Feature            | Support Level       | Description                                                                                     | Sample Query                                                                 |
|--------------------|---------------------|-------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| **Tokenization**   | Supported           | Breaks down text into individual tokens using TSVector                                          | _Internal processing step; no query needed_                                    |
| **Stemming**       | Supported           | Converts inflected words to their root form based on language analyzers                         | _Internal processing step; no query needed_                                    |
| **Language Support** | Partially Supported | Supports common languages like `en`, `es`, `fr`, etc., matching MongoDB capabilities            | `db.text_search.find({ "$text": { "$search": "leche", "$language": "es" } })` |
| **Term-Based Search** | Supported         | Exact term search in indexed fields                                                             | `db.movies.find({ "$text": { "$search": "surfer" } })`                        |
| **Phrase Search**  | Partially Supported | Exact phrase match using quotes. Some compatibility issues exist.                              | `db.text_search.find({ "$text": { "$search": "\"are cats\"" } })`           |
| **Prefix Query**   | Supported           | Find terms starting with a pattern using regex                                                  | `db.articles.find({ title: { $regex: /^data/i } })`                            |
| **Wildcard Search** | Supported          | Match flexible patterns using regex + `$text`                                                   | `db.articles.find({ $and: [ { $text: { $search: "hello" } }, { title: { $regex: /.*world.*/i } } ] })` |
| **Regex Search**   | Supported           | Use regular expressions for flexible text pattern matching                                      | `db.articles.find({ title: { $regex: /^hello.*world$/i } })`                   |
| **Boolean Operators** | Supported         | Use `+`, `-` to include/exclude terms                                                           | `db.text_search.find({ "$text": { "$search": "cafe +con" } })`                |
| **Multi-Match**    | Partially Supported | Multi-field query via combined index with weights                                              | `db.myColl.createIndex({ title: "text", genre: "text" }, { default_language: "english", weights: { title: 10, genre: 3 } })` |
| **Custom Analyzers** | Not Available      | Custom tokenization or filtering not supported                                                  | _Not applicable_                                                               |
| **Synonym Support** | Not Available      | No native support for synonyms                                                                 | _Not applicable_                                                               |
| **Fuzzy Search**   | Not Available       | No typo-tolerant or fuzzy match support                                                         | _Not applicable_                                                               |
| **Boost (per-term)** | Not Available     | No dynamic boosting at query time; only field-level weighting                                   | _Not applicable_                                                               |
| **Proximity Search** | Not Available     | Cannot search for terms within specific word distances                                          | _Not applicable_                                                               |
| **Faceted Search** | Not Available     | filter search results by different attributes or categories, making it easier to find relevant information | _Not applicable_                                                               |
| **Autocomplete & Boost** | Not Available     |                              TODO             | _Not applicable_                                                               |

---

## Aggregation and Compatibility Notes

- **Aggregation Compatibility**: `$text` is not recognized in all aggregation stages; use `cosmosSearch` or `knnBeta` in aggregation instead.
- **One Text Index per Collection**: MongoDB allows only one text index; multi-field support must be combined in that one index.
- **No Regex in $text**: `$text` does not support wildcards or partial word matching directly—use regex separately.
- **No Fuzzy Matching, Synonyms, or Proximity**: Advanced search features are not available in the vCore `$text` operator.

---

## Supported Languages

- Danish (`da`)
- Dutch (`nl`)
- English (`en`)
- Finnish (`fi`)
- French (`fr`)
- German (`de`)
- Hungarian (`hu`)
- Italian (`it`)
- Norwegian (`nb`)
- Portuguese (`pt`)
- Romanian (`ro`)
- Russian (`ru`)
- Spanish (`es`)
- Swedish (`sv`)
- Turkish (`tr`)

---

## Summary

Azure Cosmos DB for MongoDB vCore enables developers to use familiar MongoDB-style full-text search capabilities with support for tokenization, stemming, boolean logic, and basic multi-field indexes. However, it lacks advanced features like fuzzy matching, synonyms, or custom analyzers.

To build performant and accurate search experiences, developers should:
- Combine text search with regex where needed
- Carefully construct multi-field indexes with weights
- Understand the underlying language and stemming behavior

For more complex search scenarios (e.g., typo-tolerance, semantic search), consider combining vCore with external search solutions such as Azure Cognitive Search.

## Next step

> [!div class="nextstepaction"]
> [Create a lifetime free-tier vCore cluster for Azure Cosmos DB for MongoDB](free-tier.md)
