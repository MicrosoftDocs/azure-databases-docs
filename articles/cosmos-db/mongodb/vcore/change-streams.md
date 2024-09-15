---
  title: Change Streams on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: Learn how to configure and use change streams to track the real-time changes made on targeted collection\database.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: conceptual
  ms.date: 09/17/2024
---

# Change Streams on Azure Cosmos DB for MongoDB vCore (Preview)

Change streams is a real-time stream of database changes that flows from your database to your application. This feature enables you to build reactive applications by subscribing to database changes, eliminating the need for continuous polling to detect changes.

> [!NOTE]
> Please register to enrol your interest using [Form](https://forms.office.com/r/G76XDQ6YSE).

## Configuring Change Streams

This example code initiates a change stream on the `exampleCollection` collection, continuously monitoring for any changes. When a change is detected, it retrieves the change event and prints it in JSON format.

# [JavaScript](#tab/javascript)

```javascript
// Open a change stream
const changeStream = db.exampleCollection.watch();

// Listen for changes
while (changeStream.hasNext()) 
    {
        const change = changeStream.next();
        printjson(change);
    }
```

# [Java](#tab/Java)

```java
package com.example;
 
import com.mongodb.MongoClientSettings;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.model.changestream.ChangeStreamDocument;
 
import org.bson.BsonDocument;
import org.bson.Document;
import org.bson.json.JsonWriterSettings;
import org.json.JSONObject;
 
public class ChangeStreamExample {
    public static void main(String[] args) {
        MongoClient mongoClient = MongoClients.create("mongodb://<username>:<pwd>@<clustername>.pgmongo-dev.cosmos.windows-int.net:10260/?tls=true");
        MongoDatabase database = mongoClient.getDatabase("test");
        MongoCollection<Document> collection = database.getCollection("test");
 
        // Open a change stream
        MongoCursor<ChangeStreamDocument<Document>> cursor = collection.watch().iterator();
 
        // Listen for changes
        try {
            while (cursor.hasNext()) {
                ChangeStreamDocument<Document> change = cursor.next();
 
                // Create a JSONObject from the fields of the ChangeStreamDocument
                JSONObject json = new JSONObject();
 
                // Add fields to the JSON object
                json.put("operationType", change.getOperationType().getValue());
                json.put("namespace", change.getNamespace().getFullName());
 
                if (change.getDocumentKey() != null) {
                    json.put("documentKey", change.getDocumentKey().toJson().toString());
                }
 
                if (change.getResumeToken() != null) {
                    json.put("resumeToken", change.getResumeToken().toJson());
                }
 
                if (change.getFullDocument() != null) {
                    json.put("fullDocument", change.getFullDocument().toJson());
                }
 
                if (change.getWallTime() != null) {
                    json.put("wallTime", change.getWallTime().toString());
                }
 
                // Pretty-print the JSON object with 4-space indent
                System.out.println(json.toString(4)); 
            }
        } 
        catch (Exception e) {
            System.err.println("Error processing change stream: " + e);
        } 
        finally {
            cursor.close();
            mongoClient.close();
        }
    }
}
```

# [Python](#tab/python)

```python
from pgmongo import MongoClient
from pgmongo.errors import PyMongoError
import json
from bson import json_util

def main():
    uri = "mongodb://<username>:<pwd>@<clustername>.pgmongo-dev.cosmos.windows-int.net:10260/?tls=true"
    client = MongoClient(uri)
    database = client['test']
    collection = database['test']

    # Open a change stream
    try:
        with collection.watch() as stream:
            for change in stream:
                # Create a JSON object from the fields of the ChangeStreamDocument
                json_data = {}

                # Add fields to the JSON object
                json_data['operationType'] = change['operationType']
                json_data['namespace'] = change['ns']['db'] + '.' + change['ns']['coll']

                if 'documentKey' in change:
                    json_data['documentKey'] = json_util.dumps(change['documentKey'])

                if '_id' in change:
                    json_data['resumeToken'] = json_util.dumps(change['_id'])

                if 'fullDocument' in change:
                    json_data['fullDocument'] = json_util.dumps(change['fullDocument'])

                if 'clusterTime' in change:
                    json_data['wallTime'] = str(change['clusterTime'].as_datetime())

                # Pretty-print the JSON object with 4-space indent
                print(json.dumps(json_data, indent=4, default=json_util.default))

    except PyMongoError as e:
        print(f"Error processing change stream: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
```

---

> [!IMPORTANT]
> Change streams are resumable by specifying a resume token to `resumeAfter` when opening the cursor. Though it is expected that there is enough history to locate the operation associated with the token. The document observed in changestream in `_id` field represents the resumable token.
>
> `cursor = db.inventory.watch(resume_after=resume_token)`

## Monitoring database changes with Change Streams

Let's understand the change stream output through the example.

# [Insert](#tab/Insert)

In this change stream event, we see that a new record was `inserted` into the `employee` collection within the `cs` database, and the event details include the full content of the newly added document.

```json
{
  "_id": { "_data": "AeARBpQ/AAAA" }, // resume_token
  "operationType": "insert",
  "fullDocument": {
    "_id": { "$oid": "66e6f63e6f49ecaabf794958" },
    "employee_id": "17986",
    "name": "John",
    "position": "Software Engineer",
    "department": "IT",
    "rating": 4
  },
  "ns": { "db": "cs", "coll": "employee" },
  "documentKey": { "_id": { "$oid": "66e6f63e6f49ecaabf794958" } }
}
```

# [Update](#tab/Update)

In this update event, the `position` & `rating` for John are modified. The change stream reflects an `update` in the `employee` collection with post update state of the document.

```json
{
  "_id": { "_data": "AWACAKM/AAAA" },
  "operationType": "update",
  "fullDocument": {
    "_id": { "$oid": "66e6f63e6f49ecaabf794958" },
    "employee_id": "17986",
    "name": "John",
    "position": "SSE",
    "department": "IT",
    "rating": 5
  },
  "ns": {
    "db": "cs", "coll": "employee"
  },
  "documentKey": {
    "_id": { "$oid": "66e6f63e6f49ecaabf794958" }
  }
}

```

# [Delete](#tab/Delete)

The change stream event indicates that a document was `deleted` from the `employee` collection in the `cs` database. The event captures the unique identifier of the removed document.

```json
{
  "_id": { "_data": "ASgBAJs/AAAA" },
  "operationType": "delete",
  "ns": { "db": "cs", "coll": "employee" },
  "documentKey": { "_id": { "$oid": "66e6f63e6f49ecaabf794958" } }
}
```

---

## Personalize data in Change Stream

Customize your change stream output by specifying an array of one or more pipeline stages during configuration. Supported operators include the following.

- `$addFields`
- `$match`
- `$project`
- `$set`
- `$unset`

## Limitations

- `Replace` event is yet not supported.
- `pre-image` is an unsupported option.
- Change stream cursors need to be reinitialized after a fail-over event.
- Historical changestream events from past timeline are unsupported.
- `Update` event doesn't support Update description.
- Change stream events on multi-shard cluster is unsupported.
- Changestream on a sharded collection is unsupported.
- `showexpandedevents` isn't supported yet. This includes `createIndex`, `dropIndex`, `createCollection`, `rename` etc.
- `$changestream` as a nested pipeline of another stage is yet not supported.
