---
  title: $meta (projection) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $meta operator returns a calculated metadata column with returned dataset.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/12/2024
---

# $meta (projection)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$meta` projection operator is used to include metadata in the results of a query. It's useful for including metadata such as text search scores or other computed values in the output documents.

## Syntax

The syntax for using the `$meta` projection operator is as follows:

```javascript
db.collection.find( {$text: { $search: <string> } },
    { field: { $meta: <metaDataKeyword> } 
    }
)
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The name of the field in the output documents where the metadata gets included. |
| **`metaDataKeyword`** | The type of metadata to include common keywords like `textScore` for text search scores. |

## Example

Here's the example to illustrate the usage of the `$meta` projection operator.

### Example 1: Including text search scores

We have a collection named `stores` and we want to include the text search score in the results of a text search query.

```javascript
db.stores.createIndex({ "name": "text"});

db.stores.find(
    { $text: { $search: "Equipment Furniture Finds" } },
    { _id: 1, name: 1, score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } }).limit(2)

```

This query returns documents from the `stores` collection that match the text search criteria and include a `score` field containing the text search score.

```json
{
    "_id": "7a9aa41e-95bd-43c1-96cd-bcff0c3c33fb",
    "name": "Fabrikam, Inc",
    "score": 2
},
{
    "_id": "ee51cc4c-6770-4bb7-bb61-cd0cc44cb387",
    "name": "Proseware, Inc",
    "score": 2
}
```

## Limitation

- If no index is used, the { $meta: "indexKey" } doesn't return anything.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
