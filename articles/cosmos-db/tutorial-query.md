---
title: |
  Tutorial: Query Data
description: Learn how to query data in Azure Cosmos DB for NoSQL with the built-in query syntax using the Data Explorer.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.custom: tutorial-develop, mvc
ms.topic: tutorial
ms.date: 07/21/2025
appliesto:
  - ✅ NoSQL
---

# Tutorial: Query data in Azure Cosmos DB for NoSQL

[Azure Cosmos DB for NoSQL](introduction.md) supports querying documents using the built-in query syntax. This article provides a sample document and two sample queries and results.

This article covers the following tasks:

> [!div class="checklist"]
>
> - Query NoSQL data with the built-in query syntax
>

## Prerequisites

- An Azure Cosmos DB account, database, and container. If you don't have these resources, see [Create an Azure Cosmos DB account, database, container, and items from the Azure portal](quickstart-portal.md).

You can run the queries using the [Azure Cosmos DB Explorer](data-explorer.md) in the Azure portal. You can also run queries by using the [REST API](/rest/api/cosmos-db/) or [various SDKs](sdk-dotnet-v3.md).

For more information about queries, see [Queries in Azure Cosmos DB for NoSQL](/cosmos-db/query/overview).

## Sample document

The queries in this article use the following sample document.

```json
{
  "id": "WakefieldFamily",
  "parents": [
    { "familyName": "Wakefield", "givenName": "Robin" },
    { "familyName": "Miller", "givenName": "Ben" }
  ],
  "children": [
    {
      "familyName": "Merriam", 
      "givenName": "Jesse", 
      "gender": "female", "grade": 1,
      "pets": [
          { "givenName": "Goofy" },
          { "givenName": "Shadow" }
      ]
    },
    { 
      "familyName": "Miller", 
        "givenName": "Lisa", 
        "gender": "female", 
        "grade": 8 
    }
  ],
  "address": { "state": "NY", "county": "Manhattan", "city": "NY" },
  "creationDate": 1431620462,
  "isRegistered": false
}
```

## Select all fields and apply a filter

Given the sample family document, the following query returns the documents where the ID field matches `WakefieldFamily`. Since it's a `SELECT *` statement, the output of the query is the complete JSON document:

Query:

```sql
SELECT * 
FROM Families f 
WHERE f.id = "WakefieldFamily"
```

Results:

```json
{
  "id": "WakefieldFamily",
  "parents": [
    { "familyName": "Wakefield", "givenName": "Robin" },
    { "familyName": "Miller", "givenName": "Ben" }
  ],
  "children": [
    {
      "familyName": "Merriam", 
      "givenName": "Jesse", 
      "gender": "female", "grade": 1,
      "pets": [
          { "givenName": "Goofy" },
          { "givenName": "Shadow" }
      ]
    },
    { 
      "familyName": "Miller", 
        "givenName": "Lisa", 
        "gender": "female", 
        "grade": 8 
    }
  ],
  "address": { "state": "NY", "county": "Manhattan", "city": "NY" },
  "creationDate": 1431620462,
  "isRegistered": false
}
```

## Select a cross-product of a child collection field

The next query returns all the given names of children in the family whose ID matches `WakefieldFamily`.

Query:

```sql
SELECT c.givenName 
FROM Families f 
JOIN c IN f.children 
WHERE f.id = 'WakefieldFamily'
```

Results:

```json
[
  {
    "givenName": "Jesse"
  },
  {
    "givenName": "Lisa"
  }
]
```

## Next step

> [!div class="nextstepaction"]
> [Distribute your data globally](tutorial-global-distribution.md)
