# MongoDB `count` Command

The `count` command in MongoDB is used to count the number of documents in a collection that match a specified query. This command is particularly useful for obtaining quick statistics about the data stored in your collections, such as the number of documents that meet certain criteria.

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

2. **Counting documents with specific criteria**

   To count the number of stores with a specific `_id` store ID:

   ```javascript
   db.stores.count({ "store._id": "e5767a9f-cd95-439c-9ec4-7ddc13d22926" })
   ```

3. **Counting documents with nested criteria**

   To count the number of stores that have a specific promotion event:

   ```javascript
   db.stores.count({ "promotionEvents.eventName": "Incredible Discount Days" })   
   ```

4. **Counting documents with multiple criteria**

   To count the number of stores located at a specific latitude and longitude:

   ```javascript
   db.stores.count({ "location.lat": -2.4111, "location.lon": 72.1041 })
   ```


## Limitations

Delete if no limitations/deviations from standard Mongo command, else update as necessary.

## Related content

Manually add content as necessary.