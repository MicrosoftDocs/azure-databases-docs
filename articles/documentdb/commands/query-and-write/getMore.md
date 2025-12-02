---
  title: GetMore command usage in Azure DocumentDB
  description: The getMore command is used to retrieve extra batches of documents from an existing cursor.
  author: avijitgupta
  ms.author: avijitgupta
  ms.topic: language-reference
  ms.date: 09/12/2024
---

# getMore

The `getMore` command is used to retrieve extra batches of documents from an existing cursor. This command is useful when dealing with large datasets that can't be fetched in a single query due to size limitations. The command allows clients to paginate through the results in manageable chunks with commands that return a cursor. For example, [find](./find.md) and [aggregate](../aggregation/aggregate.md), to return subsequent batches of documents currently pointed to by the cursor.

## Syntax

The syntax for the `getMore` command is as follows:

```
{
   getMore: <cursor-id>,
   collection: <collection-name>,
   batchSize: <number-of-documents>
}
```

- `getMore`: The unique identifier for the cursor from which to retrieve more documents.
- `collection`: The name of the collection associated with the cursor.
- `batchSize`: (Optional) The number of documents to return in the batch. If not specified, the server uses the default batch size.

## Examples

### Example 1: Retrieve more documents from a cursor

Assume you have a cursor with the ID `1234567890` from the `stores` collection. The following command retrieves the next batch of documents:

```javascript
{
   getMore: 1234567890,
   collection: "stores",
   batchSize: 5
}
```

### Example 2: Retrieve more documents without specifying batch size

If you don't specify the `batchSize`, the server uses the default batch size:

```json
{
   getMore: 1234567890,
   collection: "stores"
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
