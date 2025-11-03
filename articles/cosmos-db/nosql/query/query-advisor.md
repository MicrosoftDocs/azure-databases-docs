---
title: Query Advisor
titleSuffix: Azure Cosmos DB for NoSQL
description: Get advice how to optimize the performance and costs of each query after execution. 
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 11/03/2025
---

# Query Advisor for Azure Cosmos DB for NoSQL

Azure Cosmos DB for NoSQL now features Query Advisor, designed to help you write faster and more efficient queries. Whether you're optimizing for performance, cost, or scalability, Query Advisor provides actionable recommendations to help you get the most out of your data.

## Why Query Optimization Matters

Azure Cosmos DB's query language is flexible, allowing developers to query JSON data with familiar SQL-like syntax. But as applications grow in complexity, small differences in query structure can have a big impact on performance and Request Units (RUs).

For example, two queries that return the same result may differ dramatically in efficiency based on how predicates are written and how indexes are leveraged.

Query Advisor analyzes your queries and offers targeted recommendations to help you:

- **Reduce RU costs** by identifying inefficient expressions or unnecessary filters.
- **Improve query performance** through more optimal query structures.
- **Understand the "why"** behind each suggestion, with explanations written in clear, developer-friendly language.


## How It Works

When you execute a query, the Query Advisor runs over your query plan, evaluating patterns that may cause high RU consumption, excessive scans, or potentially unnecessary processing. It then returns a set of recommendations that indicates what is the part of the query that may be limiting performance, and suggests a potential change that could help. 


## Using Query Advisor

You can enable query advisor capabilities by setting the `PopulateQueryAdvice` property in `QueryRequestOptions` to `true`. When not specified, `PopulateQueryAdvice` defaults to `false`. To access the advice, use the string property `FeedResponse.QueryAdvice`.

> [!IMPORTANT]
> Query Advisor is currently only supported in the .NET SDK. 

> [!NOTE]
> The query advice is only returned on the first round trip and is unavailable on subsequent continuation calls.

### Usage Example

```csharp
string query = "SELECT VALUE r.id FROM root r WHERE CONTAINS(r.name, 'Abc')";

QueryRequestOptions requestOptions = new QueryRequestOptions() { PopulateQueryAdvice = true };

using FeedIterator<CosmosElement> itemQuery = testContainer.GetItemQueryIterator<CosmosElement>(
    query,
    requestOptions: requestOptions);

string queryAdvice = null;
while (itemQuery.HasMoreResults)
{
    if (queryAdvice != null)
    {
        break;
    }

    FeedResponse<Item> page = await itemQuery.ReadNextAsync();
    queryAdvice = page.QueryAdvice;
}

Console.WriteLine(queryAdvice);
```

### Example Output

In this example query, we observe that there is one single advice, called **QA1002**:

```
QA1002: Instead of CONTAINS, consider using STARTSWITH or computed properties, which may improve performance. For more information, please visit https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query/queryadvisor/QA1002
```

The query advice contains three important pieces of information:

- **The Query Advice ID**: `QA1002`
- **The advice description**: "Instead of..."
- **The link to the documentation**: A URL to detailed guidance

We encourage you to visit the provided link to learn more about the query advice where you can see further examples, detailed explanations, and suggestions to improve your query.

## Additional Examples

### Example: Optimizing System Functions

**Query:**

```sql
SELECT GetCurrentTicks() 
FROM root r 
WHERE GetCurrentTimestamp() > 10
```

**Query Advice:**

```bash
QA1009: Instead of using GetCurrentTimestamp, consider using GetCurrentTimestampStatic, which may improve performance. For more information, please visit https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query/queryadvisor/QA1009

QA1008: Instead of using GetCurrentTicks, consider using GetCurrentTicksStatic, which may improve performance. For more information, please visit https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query/queryadvisor/QA1008
```

In this example, there are 2 pieces of advice returned by the Query Advisor, **QA1008** and **QA1009**. Each piece of advice is separated into a new line in the `QueryAdvice` string.

## Next Steps

- Learn more about [query performance](query-metrics.md)
- Understand [request units](../request-units.md)
- Explore [indexing policies](../index-policy.md)