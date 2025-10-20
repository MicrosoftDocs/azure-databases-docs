---
title: Full text search FAQ
titleSuffix: Azure Cosmos DB
description: Commonly asked questions for full text indexing and search in Azure Cosmos DB
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 10/20/2025
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
---


# Full text search frequently asked questions

Full Text Search (sometimes called lexical search) in Azure Cosmos DB for NoSQL enables efficient querying of textual data using a specialized index and scoring system. It also features a text-relevancy method to order search results by the BM25 (Best Matching 25) algorithm. This ranks the returned documents based on relevancy, considering term frequency, inverse document frequency, and document length, and helps to enable applications to search for and retrieve the most relevant text documents from your Azure Cosmos DB data without relying on external search services like Lucene or Elasticsearch.

## What are the processing steps?
Full text search in Azure Cosmos DB applies several text processing techniques to improve search relevance and efficiency. It uses stemming to reduce words to their root forms, [stopword removal](./stopwords.md) to eliminate common words like "the" and "and" that don’t add value to search results, and tokenization to break text into searchable units. These steps help ensure that queries return the most meaningful and relevant documents

## Does the full text index support  wildcard paths?
No, wildcard characters such as * and [] aren't currently supported in full text container policies or indexes. Instead, the full text path should be defined explicitly.


## My full text queries have high latency and/or RU charge. 
Several factors can contribute to high latency or RU consumption:
- Query selectivity
- Number of indexed terms (words)
- Number of documents in the container
- Number of physical partitions of your Cosmos DB container

It's good practice to ensure your full text container and indexing policies are set correctly for your query paths. For example if using `FullTextScore(c.text, ...)`, you should have full text container and indexing policies set on the `c.text` path. [Learn more about full text policies here](./full-text-search.md#full-text-policy).


## Why is my ORDER BY RANK with FullTextScore have high latency or RU charge?

Using ORDER BY RANK FullTextScore(...) can be costly if the query includes long phrases. We recommend splitting phrases into individual keywords to improve performance. For example, instead of:
```SQL
ORDER BY RANK FullTextScore(c.text, "mountian bicycle thats have high performance shocks")
```

Use:
```SQL
ORDER BY RANK FullTextScore(c.text, "mountian", "bicycle", "thats" "have", "high", "performance", "shocks")
```)
```

## Can I see the score returned by FullTextscore?
As of today, you can't project the FullTextScore in the `SELECT` clause of a query.


## Why are my search results different than I expect?
If you're comparing Full Text Search results in Azure Cosmos DB to results from a search engine that indexes your Cosmos DB data, the results can be slightly different. This is usually because of one of the following reasons:
- Stopword filtering: Cosmos DB automatically removes common words like "the" and "and," which your search engine might include.
- Stemming differences: Cosmos DB reduces words to their root forms using language-specific rules, which may differ from your search engine’s approach.
- Scoring algorithm: Cosmos DB uses standard BM25 scoring, which may be tuned differently than your engine’s ranking logic.
- Tokenization rules: The way Cosmos DB breaks text into searchable units may differ from your engine’s tokenizer.
- Language support: Cosmos DB’s multi-language support is in preview and may behave differently than engines with mature analyzers for nonenglish languages.
- Fuzzy search behavior: Cosmos DB’s fuzzy search is limited to a maximum of 2 edits and 10 suggestions and its implementation is still in preview, so the results from a fuzzy search may differ compared to other search engines.


## Best practices
- Always define both a full text policy and full text index for optimal performance.
- Use FullTextContainsAll or FullTextContainsAny 
- Use FullTextScore only in ORDER BY RANK clauses.



## Known limitations

- Wildcard paths (*, []) for arrays aren't supported in full text policies or indexes.
- Using `FullTextScore` on phrases (strings with multiple words with spaces) can be slower than searching on each word separately.
- Multi-language support is in preview and may have inconsistent performance. Stopword removal is currently only available for English (en-US).
- Fuzzy search is also in preview and limited to a maximum edit distance of 2 and 10 suggestions.
-  Queries using FullTextScore within a JOIN aren't currently supported
- Issue: Providing the incorrect syntax for FullTextScore may result in a 500 error instead of the expected 400 error. 
 - Issue: When executing queries using ORDER BY RANK and `FullTextScore`, the results may differ slightly on macOS or Linux clients from Windows clients. 
