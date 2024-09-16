---
  title: getMore command usage in Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The getMore is used to retrieve additional batches of documents from an existing cursor.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 09/12/2024
---

# getMore

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `getMore` command is used to retrieve additional batches of documents from an existing cursor. This is particularly useful when dealing with large datasets that cannot be fetched in a single query due to size limitations. The command allows clients to paginate through the results in manageable chunks.

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
- `batchSize`: (Optional) The number of documents to return in the batch. If not specified, the server will use the default batch size.

## Examples

### Example 1: Retrieve additional documents from a cursor

Assume you have a cursor with the ID `1234567890` from the `stores` collection. The following command retrieves the next batch of documents:

```json
{
   getMore: 1234567890,
   collection: "stores",
   batchSize: 5
}
```

### Example 2: Retrieve additional documents without specifying batch size

If you do not specify the `batchSize`, the server will use the default batch size:

```json
{
   getMore: 1234567890,
   collection: "stores"
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
