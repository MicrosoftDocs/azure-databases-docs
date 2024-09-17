---
  title: Count command usage in Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: is used to count the number of documents in a collection that match a specified query.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 09/12/2024
---

# count

The `count` command is used to count the number of documents in a collection that match a specified query. This command is particularly useful for obtaining quick statistics about the data stored in your collections, such as the number of documents that meet certain criteria.

## Syntax

The syntax for the `count` command is as follows:

```
db.collection.count(query, options)
```

- `query`: A document specifying the selection criteria using query operators.
- `options`: Optional. A document specifying options, such as `limit` and `skip`.

## Examples

Here are some examples to demonstrate the usage of the `count` command:

1. **Counting all documents in a collection**

   To count all documents in the `store` collection:

   ```javascript
   db.stores.count({})
   ```


#### Sample output

```javascript
```

2. **Counting documents with specific criteria**

   To count the number of stores with a specific `_id` store ID:

   ```javascript
   db.stores.count({ "store._id": "e5767a9f-cd95-439c-9ec4-7ddc13d22926" })
   ```


#### Sample output

```javascript
```

3. **Counting documents with nested criteria**

   To count the number of stores that have a specific promotion event:

   ```javascript
   db.stores.count({ "promotionEvents.eventName": "Incredible Discount Days" })   
   ```

#### Sample output

```javascript
```

4. **Counting documents with multiple criteria**

   To count the number of stores located at a specific latitude and longitude:

   ```javascript
   db.stores.count({ "location.lat": -2.4111, "location.lon": 72.1041 })
   ```

#### Sample output

```javascript
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
