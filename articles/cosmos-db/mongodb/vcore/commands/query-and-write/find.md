---
  title: Find command usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The find command is used to query documents within a collection.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 09/12/2024
---

# find

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `find` command is used to query documents within a collection. It allows you to retrieve documents that match specific criteria. This command is fundamental for data retrieval operations and can be customized with various filters, projections, and options to fine-tune the results.

## Syntax

The basic syntax for the `find` command is:

```javascript
db.collection.find(query, projection)
```

## Parameters

| | Description |
| --- | --- |
| **`query`** | A document that specifies the criteria for the documents to be retrieved. |
| **`projection`** | (Optional) A document that specifies the fields to return in the matching documents. |

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
