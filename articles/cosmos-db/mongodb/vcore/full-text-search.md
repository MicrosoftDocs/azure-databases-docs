---
title: Full-Text Search
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Explore built-in full text search capabilities in Azure Cosmos DB for MongoDB vCore
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: concept-article
ms.date: 04/03/2025
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ MongoDB vCore
---

# Full-Text Search Capabilities in Azure Cosmos DB for MongoDB (vCore)

Full-text search functionality in vCore-based Azure Cosmos DB for MongoDB provides powerful document searching capabilities beyond traditional query methods. This advanced search technique enables users to discover relevant content based on natural language processing, word variations, and contextual relevance—not just exact matches.

The integrated text search engine removes the need for external search services. This helps simplify your database architecture. It uses specialized text indexes to handle search operations efficiently. The system processes, tokenizes, and analyzes document content. As a result, your applications can quickly find documents that include specific keywords, phrases, or related terms.

> [!NOTE]
> The full-text search in vCore-based Azure Cosmos DB for MongoDB uses a PostgreSQL-style TSVector index under the hood, with support for MongoDB’s `$text` operator.

## Feature Support
| Feature            | Support Level       | Description                                                                                     | Sample Query                                                                 |
|--------------------|---------------------|-------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| **Tokenization**   | Supported           | Breaks down text into individual tokens using TSVector                                          | _Not applicable_                                    |
| **Stemming**       | Supported           | Converts inflected words to their root form based on language analyzers                         | _Not applicable_                                    |
| **Language Support** | Partially Supported | Supports common languages like Danish (`da`), Dutch (`nl`), English (`en`), Finnish (`fi`), French (`fr`), German (`de`), Hungarian (`hu`), Italian (`it`), Norwegian (`nb`), Portuguese (`pt`), Romanian (`ro`), Russian (`ru`), Spanish (`es`), Swedish (`sv`), Turkish (`tr`) etc.            | `db.text_search.find({ "$text": { "$search": "leche", "$language": "es" } })` |
| **Term-Based Search** | Supported         | Exact term search in indexed fields                                                             | `db.movies.find({ "$text": { "$search": "surfer" } })`                        |
| **Phrase Search**  | Partially Supported | Exact phrase match using quotes. Some compatibility issues exist.                              | `db.text_search.find({ "$text": { "$search": "\"are cats\"" } })`           |
| **Prefix Query**   | Supported           | Find terms starting with a pattern using regex                                                  | `db.articles.find({ title: { $regex: /^data/i } })`                            |
| **Wildcard Search** | Supported          | Match flexible patterns using regex + `$text`                                                   | `db.articles.find({ $and: [ { $text: { $search: "hello" } }, { title: { $regex: /.*world.*/i } } ] })` |
| **Regex Search**   | Supported           | Use regular expressions for flexible text pattern matching                                      | `db.articles.find({ title: { $regex: /^hello.*world$/i } })`                   |
| **Boolean Operators** | Supported         | Use `+`, `-` to include/exclude terms                                                           | `db.text_search.find({ "$text": { "$search": "cafe +con" } })`                |
| **Multi-Match**    | Partially Supported | Multi-field query via combined index with weights                                              | `db.myColl.createIndex({ title: "text", genre: "text" }, { default_language: "english", weights: { title: 10, genre: 3 } })` |
| **Faceted Search** | Not Available       | Filter search results by categories or tags (e.g., brand, color, price). Not supported natively in vCore text search. | _Not applicable_ |
| **Autocomplete & Boost** | Not Available | Autocomplete (type-ahead suggestions) and query-time boosting of specific terms are not supported. Boosting can only be done at index level via field weights. | _Not applicable_ |
| **Custom Analyzers** | Not Available      | Custom tokenization or filtering not supported                                                  | _Not applicable_                                                               |
| **Synonym Support** | Not Available      | No native support for synonyms                                                                 | _Not applicable_                                                               |
| **Fuzzy Search**   | Not Available       | No typo-tolerant or fuzzy match support                                                         | _Not applicable_                                                               |
| **Proximity Search** | Not Available     | Cannot search for terms within specific word distances                                          | _Not applicable_                                                               |

## Next step

> [!div class="nextstepaction"]
> [Create a lifetime free-tier vCore cluster for Azure Cosmos DB for MongoDB](free-tier.md)
