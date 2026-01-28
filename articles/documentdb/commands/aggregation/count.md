---
  title: Count command usage in Azure DocumentDB
  description: Count command is used to count the number of documents in a collection that match a specified query.
  author: avijitgupta
  ms.author: avijitgupta
  ms.topic: language-reference
  ms.date: 09/12/2024
---

# count

The `count` command is used to count the number of documents in a collection that match a specified query. This command is useful for obtaining quick statistics about the data stored in your collections, such as the number of documents that meet certain criteria.

## Syntax

The syntax for the `count` command is as follows:

```
db.collection.count(query, options)
```

- `query`: A document specifying the selection criteria using query operators.
- `options`: Optional. A document specifying options, such as `limit` and `skip`.

## Examples

Here are some examples to demonstrate the usage of the `count` command:

### Example 1. Counting all documents in a collection

   To count all documents in the `stores` collection:

   ```javascript
   db.stores.count({})
   ```

#### Sample output

```javascript
[mongos] StoreData> db.stores.countDocuments({})
60570
```

### Example 2. Counting documents with specific criteria

   To count the number of stores with a specific `_id` store ID:

   ```javascript
   db.stores.count({ "_id": "e5767a9f-cd95-439c-9ec4-7ddc13d22926" })
   ```

#### Sample output

```javascript
[mongos] StoreData> db.stores.count({ "_id": "e5767a9f-cd95-439c-9ec4-7ddc13d22926" })
1
```

### Example 3. Counting documents with nested criteria

   To count the number of stores that have a specific promotion event:

   ```javascript
   db.stores.count({ "promotionEvents.eventName": "Incredible Discount Days" })   
   ```

#### Sample output

```javascript
[mongos] StoreData> db.stores.count({ "promotionEvents.eventName": "Incredible Discount Days" })
2156
```

### Example 4. Counting documents with multiple criteria

   To count the number of stores located at a specific latitude and longitude:

   ```javascript
   db.stores.count({ "location.lat": -2.4111, "location.lon": 72.1041 })
   ```

#### Sample output

```javascript
[mongos] StoreData> db.stores.count({ "location.lat": -2.4111, "location.lon": 72.1041 })
1
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
