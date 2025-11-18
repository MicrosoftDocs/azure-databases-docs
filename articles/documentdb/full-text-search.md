---
title: Full-Text Search
description: Explore built-in full text search capabilities in Azure DocumentDB
author: khelanmodi
ms.author: khelanmodi
ms.topic: concept-article
ms.date: 09/12/2025
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
---

# Full-text search capabilities in Azure DocumentDB

Full-text search functionality in Azure DocumentDB provides powerful document searching capabilities beyond traditional query methods. This advanced search technique enables users to discover relevant content based on natural language processing, word variations, and contextual relevance—not just exact matches.

The integrated text search engine removes the need for external search services. This helps simplify your database architecture. It uses specialized text indexes to handle search operations efficiently. The system processes, tokenizes, and analyzes document content. As a result, your applications can quickly find documents that include specific keywords, phrases, or related terms.

> [!NOTE]
> The full-text search in Azure DocumentDB uses a PostgreSQL-style TSVector index under the hood, with support for MongoDB’s `$text` operator.

## Feature support

| Feature            | Support level       | Description      | Sample query    |
|--------------------|---------------------|------------------|-----------------|
| **Tokenization**   | Supported           | Breaks down text into individual tokens using TSVector   | _Not applicable_    |
| **Stemming**       | Supported           | Converts inflected words to their root form based on language analyzers   | _Not applicable_  |
| **Language support** | Partially supported | Supports common languages like Danish (`da`), Dutch (`nl`), English (`en`), Finnish (`fi`), French (`fr`), German (`de`), Hungarian (`hu`), Italian (`it`), Norwegian (`nb`), Portuguese (`pt`), Romanian (`ro`), Russian (`ru`), Spanish (`es`), Swedish (`sv`), Turkish (`tr`)           | `db.text_search.find({ "$text": { "$search": "leche", "$language": "es" } })` |
| **Term-based search** | Supported         | Exact term search in indexed fields  | `db.movies.find({ "$text": { "$search": "surfer" } })`  |
| **Phrase search**  | Partially supported | Exact phrase match using quotes. Some compatibility issues exist.  | `db.text_search.find({ "$text": { "$search": "\"are cats\"" } })`  |
| **Prefix query**   | Supported           | Find terms starting with a pattern using regex   | `db.articles.find({ title: { $regex: /^data/i } })`  |
| **Wildcard search** | Supported          | Match flexible patterns using regex + `$text`  | `db.articles.find({ $and: [ { $text: { $search: "hello" } }, { title: { $regex: /.*world.*/i } } ] })` |
| **Regex search**   | Supported           | Use regular expressions for flexible text pattern matching  | `db.articles.find({ title: { $regex: /^hello.*world$/i } })`  |
| **Boolean operators** | Supported        | Use `+`, `-` to include/exclude terms  | `db.text_search.find({ "$text": { "$search": "cafe +con" } })`  |
| **Multi-match**    | Partially supported | Multi-field query via combined index with weights   | `db.myColl.createIndex({ title: "text", genre: "text" }, { default_language: "english", weights: { title: 10, genre: 3 } })` |
| **Faceted search** | Not available       | Filter search results by categories or tags (e.g., brand, color, price). Not supported natively in text search. | _Not applicable_ |
| **Autocomplete & boost** | Not available | Autocomplete (type-ahead suggestions) and query-time boosting of specific terms aren't supported. Boosting can only be done at index level via field weights. | _Not applicable_ |
| **Custom analyzers** | Not available     | Custom tokenization or filtering not supported  | _Not applicable_   |
| **Synonym support** | Not available      | No native support for synonyms    | _Not applicable_     |
| **Fuzzy search**   | Not available       | No typo-tolerant or fuzzy match support    | _Not applicable_  |
| **Proximity search** | Not available     | Can't search for terms within specific word distances  | _Not applicable_   |

## Next step

> [!div class="nextstepaction"]
> [Azure DocumentDB Free Tier](free-tier.md)
