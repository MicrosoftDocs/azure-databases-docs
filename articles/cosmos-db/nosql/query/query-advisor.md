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
ms.date: 11/04/2025
---

# Query Advisor for Azure Cosmos DB for NoSQL

> [!IMPORTANT]
> Query Advisor is currently only supported in the .NET SDK. 

> [!NOTE]
> The query advice is only returned on the first round trip and is unavailable on subsequent continuation calls.

### Usage example

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

### Example output

In this example query, we observe that there's one single advice, called **QA1002**:

```
QA1002: Instead of CONTAINS, consider using STARTSWITH or computed properties, which may improve performance. [...]
```

The query advice contains three important pieces of information:

- **The Query Advice ID**: `QA1002`
- **The advice description**: "Instead of..."
- **The link to the documentation**: A URL to detailed guidance

We encourage you to visit the provided link to learn more about the query advice where you can see further examples, detailed explanations, and suggestions to improve your query.

## Additional examples

### Optimizing system functions

**Query:**

```sql
SELECT GetCurrentTicks() 
FROM root r 
WHERE GetCurrentTimestamp() > 10
```

**Query Advice:**

```bash
QA1009: Instead of using GetCurrentTimestamp, consider using GetCurrentTimestampStatic, which may improve performance. [...]

QA1008: Instead of using GetCurrentTicks, consider using GetCurrentTicksStatic, which may improve performance. [...]
```

In this example, there are 2 pieces of advice returned by the Query Advisor, **QA1008** and **QA1009**. Each piece of advice is separated into a new line in the `QueryAdvice` string.

## Relatec content

- [Query metrics](../query-metrics.md)
- [Index metrics](../index-metrics.md)
