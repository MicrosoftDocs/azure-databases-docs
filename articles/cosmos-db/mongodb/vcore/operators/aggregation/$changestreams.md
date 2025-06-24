---
  title: $changeStream (aggregation)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $changeStream stage opens a change stream cursor to track data changes in real-time.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/23/2025
---

# $changeStream (aggregation)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$changeStream` aggregation stage opens a change stream cursor that tracks data changes in real-time. This stage enables applications to react to insert, update, delete, and other operations as they occur in the collection.

## Syntax

The syntax for the `$changeStream` stage is as follows:

```javascript
{
  $changeStream: {
    allChangesForCluster: <boolean>,
    fullDocument: <string>,
    fullDocumentBeforeChange: <string>,
    resumeAfter: <ResumeToken>,
    startAfter: <ResumeToken>,
    startAtOperationTime: <Timestamp>,
    showExpandedEvents: <boolean>
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`allChangesForCluster`** | Optional. Boolean. If true, returns changes for the entire cluster. Default is false. |
| **`fullDocument`** | Optional. String. Determines what to return for update operations. Options: 'default', 'updateLookup', 'whenAvailable', 'required'. |
| **`fullDocumentBeforeChange`** | Optional. String. Returns the preimage of the document. Options: "off", "whenAvailable", "required". |
| **`resumeAfter`** | Optional. Resume token to resume change stream after a specific event. |
| **`startAfter`** | Optional. Resume token to start change stream after a specific event. |
| **`startAtOperationTime`** | Optional. timestamp for starting change stream from a specific time. |
| **`showExpandedEvents`** | Optional. Boolean. Include another change stream events. Default is false. |

## Example

Let's understand the usage with the `stores` dataset for monitoring real-time changes.

### Example 1: Monitor all changes in stores collection

The example shows how to set up a change stream to monitor all changes in the stores collection.

```javascript
db.stores.aggregate([
  {
    $changeStream: {
      fullDocument: "updateLookup"
    }
  }
])
```

When a store document is updated, the change stream returns the change event with the full document.

```json
{
  "_id": { "_data": "AeARBpQ/AAAA" },
  "operationType": "update",
  "fullDocument": {
    "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
    "name": "Trey Research | Home Office Depot - Lake Freeda",
    "sales": {
      "revenue": 42500
    },
    "company": "Trey Research",
    "lastUpdated": ISODate("2024-06-16T10:30:00.000Z")
  },
  "ns": {
    "db": "StoreData",
    "coll": "stores"
  },
  "documentKey": {
    "_id": "905d1939-e03a-413e-a9c4-221f74055aac"
  }
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
