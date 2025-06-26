---
title: Use full-text search
description: Overview of full text search for querying data using "best matching 25" scoring in Azure Cosmos DB for NoSQL.
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 03/10/2025
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
ms.custom:
  - build-2025
---

# Full-text search in Azure Cosmos DB for NoSQL

[!INCLUDE [Ongoing Deployment](../nosql/includes/deployment-ongoing.md)]

Azure Cosmos DB for NoSQL now offers a powerful Full Text Search feature as generally available. This is designed to enhance the native search capabilities of your apps without needing an external search service for basic full-text search. 

## What is full text search?

Azure Cosmos DB for NoSQL now offers full-text indexing and search, designed to enhance your search adn retrieval workloads. This feature includes advanced text processing techniques such as stemming, stop word removal, and tokenization, enabling efficient and effective text searches through a specialized text index. Full text search also includes *full text scoring* with a function that evaluates the relevance of documents to a given search query. BM25, or Best Matching 25, considers factors like term frequency, inverse document frequency, and document length to score and rank documents. This helps ensure that the most relevant documents appear at the top of the search results, improving the accuracy and usefulness of text searches.

Full Text Search is ideal for a variety of scenarios, including:

- **E-commerce**: Quickly find products based on descriptions, reviews, and other text attributes.
- **Content management**: Efficiently search through articles, blogs, and documents.
- **Customer support**: Retrieve relevant support tickets, FAQs, and knowledge base articles.
- **User content**: Analyze and search through user-generated content such as posts and comments.
- **RAG for chatbots**: Enhance chatbot responses by retrieving relevant information from large text corpora, improving the accuracy and relevance of answers.
- **Multi-Agent AI apps**: Enable multiple AI agents to collaboratively search and analyze vast amounts of text data, providing comprehensive and nuanced insights.

## How to use full text search

1. Configure a container with a full text policy and full text index.
2. Insert your data with text properties.
3. Run queries against the data using full text search system functions.

### Configure container policies and indexes for hybrid search

To use full text search capabilities, you should first define two policies:
- A container-level full text policy that defines what paths contain text for the new full text query system functions.
- A full text index added to the indexing policy that enables efficient search.

While it's possible to run full text search queries without these policies, they won't utilize the full-text index and can consume higher RUs and have longer execution times. It's strongly recommended to define full text container and index policies. 

### Full text policy

For every text property you'd like to configure for full text search, you must declare both the `path` of the property with text and the `language` of the text. A simple full text policy can be:

 ```json
{
    "defaultLanguage": "en-US",
    "fullTextPaths": [
        {
            "path": "/text",
            "language": "en-US"
        }
    ]
}
```

Defining multiple text paths is easily done by adding another element to the `fullTextPolicy` array:

 ```json
{
    "defaultLanguage": "en-US",
    "fullTextPaths": [
        {
            "path": "/text1",
            "language": "en-US"
        },
        {
            "path": "/text2",
            "language": "en-US"
        }
    ]
}
```


> [!IMPORTANT]
> Wild card characters (*, []) are not currently supported in the full text policy or full text index.

#### Multi-language support (preview)
Multi-language support allows you to index and search text in languages beyond English. It applies language-specific tokenization, stemming, and stopword removal for more accurate search results. 

> [!NOTE]
> Multi-language support is in early preview. Performance and quality of search may be different than full-text search in English. For example, stopword removal is only available for English (en-us) at this time. The functionality is subject to change through the evolution of the preview. To try it, you must enroll in the *Preview Capabilities for Full Text Search* feature via the "Features" section of your Azure Cosmos DB resource in the Azure portal. 

Currently supported languages are:
- en-US (English)
- de-DE (German)
- es-ES (Spanish)
- fr-FR (French)


### Full text index

Any full text search operations should make use of a [*full text index*](../index-policy.md#full-text-indexes). A full text index can easily be defined in any Azure Cosmos DB for NoSQL index policy per the example below.

```json
{
    "indexingMode": "consistent",
    "automatic": true,
    "includedPaths": [
        {
            "path": "/*"
        }
    ],
    "excludedPaths": [
        {
            "path": "/\"_etag\"/?"
        },
    ],
    "fullTextIndexes": [
        {
            "path": "/text"
        }
    ]
}
```

Just as with the full text policies, full text indexes can be defined on multiple paths.

```json
{
    "indexingMode": "consistent",
    "automatic": true,
    "includedPaths": [
        {
            "path": "/*"
        }
    ],
    "excludedPaths": [
        {
            "path": "/\"_etag\"/?"
        },
    ],
    "fullTextIndexes": [
        {
            "path": "/text"
        },
        {
            "path": "/text2"
        }
    ]
}
```

### Full text search queries

Full text search and scoring operations are performed using the following system functions in the Azure Cosmos DB for NoSQL query language:

- [`FullTextContains`](../nosql/query/fulltextcontains.md): Returns `true` if a given string is contained in the specified property of a document. This is useful in a `WHERE` clause when you want to ensure specific key words are included in the documents returned by your query.
- [`FullTextContainsAll`](../nosql/query/fulltextcontainsall.md): Returns `true` if *all* of the given strings are contained in the specified property of a document. This is useful in a `WHERE` clause when you want to ensure that multiple key words are included in the documents returned by your query.
- [`FullTextContainsAny`](../nosql/query/fulltextcontainsany.md): Returns `true` if *any* of the given strings are contained in the specified property of a document. This is useful in a `WHERE` clause when you want to ensure that at least one of the key words is included in the documents returned by your query.
- [`FullTextScore`](../nosql/query/fulltextscore.md): Returns a score. This can only be used in an `ORDER BY RANK` clause, where the returned documents are ordered by the rank of the full text score, with most relevant (highest scoring) documents at the top, and least relevant (lowest scoring) documents at the bottom.

Here are a few examples of each function in use.

#### FullTextContains

In this example, we want to obtain the first 10 results where the phrase "red bicycle" is contained in the property `c.text`.

```sql
SELECT TOP 10 *
FROM c
WHERE FullTextContains(c.text, "red bicycle")
```

#### FullTextContainsAll

In this example, we want to obtain first 10 results where the keywords "red" and "bicycle" are contained in the property `c.text`, but not necessarily together.

```sql
SELECT TOP 10 *
FROM c
WHERE FullTextContainsAll(c.text, "red", "bicycle")
```

#### FullTextContainsAny

In this example, we want to obtain the first 10 results where the keywords "red" and either "bicycle" or "skateboard"  are contained in the property `c.text`.

```sql
SELECT TOP 10 *
FROM c
WHERE FullTextContains(c.text, "red") AND FullTextContainsAny(c.text, "bicycle", "skateboard")
```

#### FullTextScore

In this example, we want to obtain the first 10 results where "mountain" and "bicycle" are included, and sorted by order of relevance. That is, documents that have these terms more often should appear higher in the list. 

```sql
SELECT TOP 10 *
FROM c
ORDER BY RANK FullTextScore(c.text, "bicycle", "mountain")
```

> [!IMPORTANT]
> FullTextScore can only be used in the `ORDER BY RANK` clause and not projected in the `SELECT` statement or in a `WHERE` clause.

#### Fuzzy Search (preview)
Fuzzy search can improve resilience to typos and text variations. You can specify an allowable "distance" (number of edits) between the search term and document text, allowing near matches to be considered a hit. The maximum distance that can be specified is 2 (two edits).

> [!NOTE]
> Fuzzy search is in early preview. Performance, quality, and functionality are subject to change through the evolution of the preview. To try it, you must enroll in the *Preview Capabilities for Full Text Search* feature via the "Features" section of your Azure Cosmos DB resource in the Azure portal. 

```sql
SELECT TOP 10 *
FROM c
WHERE FullTextContains(c.text, {"term": "red", "distance":1}, {"term": "bicycle", "distance":2})
```

## Related content

- [``FullTextContains`` system function](../nosql/query/fulltextcontains.md)
- [``FullTextContainsAll`` system function](../nosql/query/fulltextcontainsall.md)
- [``FullTextContainsAny`` system function](../nosql/query/fulltextcontainsany.md)
- [``FullTextScore`` system function](../nosql/query/fulltextscore.md)
- [``RRF`` system function](../nosql/query/rrf.md)
- [``ORDER BY RANK`` clause](../nosql/query/order-by-rank.md)
