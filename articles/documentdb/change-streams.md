---
  title: Change Stream on Azure DocumentDB
  description: Learn how to configure and use change streams to track the real-time changes made on targeted collection\database.
  author: avijitgupta
  ms.author: avijitgupta
  ms.topic: concept-article
  ms.date: 05/20/2025
---

# Change Stream on Azure DocumentDB

Change streams are a real-time stream of database changes that flows from your database to your application. This feature enables you to build reactive applications by subscribing to database changes, eliminating the need for continuous polling to detect changes.

> [!NOTE]
> Azure DocumentDB currently supports Change Stream in single-shard clusters. We are actively working on
> providing Change Stream support for multi-shard clusters in the near future.
>
> Azure DocumentDB imposes a 400 MB limit on change streams. Please submit a support request for increasing 
> this limit.

## Enable change streams

You can enable or disable this feature using the Azure CLI or an ARM template. Portal support will be added soon.

### Steps to enable change streams on cluster via CLI

1. Log in to Azure CLI

```bash
az login
```

2. Retrieve the current settings for the feature flags on your cluster. This ensures you retain any existing flags while adding the new feature.

```bash
az resource show --ids "/subscriptions/<sub id>/resourceGroups/<resource group name>/providers/Microsoft.DocumentDB/mongoClusters/<resource name of your Azure DocumentDB cluster>" --api-version 2024-10-01-preview
```

3. Send PATCH request to enable the feature.

```bash
az resource patch --ids "/subscriptions/<subscription_id>/resourceGroups/<resource_group_name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>" --api-version 2024-10-01-preview --properties "{\"previewFeatures\": [ \"ChangeStreams\"]}"
```

4. Verify result:
   - Ensure the response payload includes `"previewFeatures": ["ChangeStreams"]`.
   - If you encounter the error "change streams isn't supported on this cluster," please create a support request.

## Configuring change streams

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
        MongoClient mongoClient = MongoClients.create("mongodb://<username>:<pwd>@<clustername>.global.mongocluster.cosmos.azure.com/?tls=true");
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

---

> [!IMPORTANT]
> Change streams are resumable by specifying a resume token to `resumeAfter` when opening the cursor. Though, it's expected that there's enough history to locate the operation associated with the token. The document observed in change stream in `_id` field represents the resumable token.
>
> `cursor = db.exampleCollection.watch(resume_after=resume_token)`

## Monitoring database changes with Change Stream

Let's understand the change stream output through the example.

# [Insert](#tab/Insert)

In this change stream event, we see that a new record was `inserted` into the `exampleCollection` collection within the `cs` database, and the event details include the full content of the newly added document.

```json
{
  "_id": { "_data": "AeARBpQ/AAAA" }, // "resume_token"
  "operationType": "insert",
  "fullDocument": {
    "_id": { "$oid": "66e6f63e6f49ecaabf794958" },
    "employee_id": "17986",
    "name": "John",
    "position": "Software Engineer",
    "department": "IT",
    "rating": 4
  },
  "ns": { "db": "cs", "coll": "exampleCollection" },
  "documentKey": { "_id": { "$oid": "66e6f63e6f49ecaabf794958" } }
}
```

# [Update](#tab/Update)

In this update event, the `position` & `rating` for John are modified. The change stream reflects an `update` in the `exampleCollection` collection with post update state of the document.

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
    "db": "cs", "coll": "exampleCollection"
  },
  "documentKey": {
    "_id": { "$oid": "66e6f63e6f49ecaabf794958" }
  }
}

```

# [Delete](#tab/Delete)

The change stream event indicates that a document was `deleted` from the `exampleCollection` collection in the `cs` database. The event captures the unique identifier of the removed document.

```json
{
  "_id": { "_data": "ASgBAJs/AAAA" },
  "operationType": "delete",
  "ns": { "db": "cs", "coll": "exampleCollection" },
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

- Change stream events on multi-shard cluster are yet not supported.
- Change stream cursors need to be reinitialized after a fail-over event at current state.
- `Update` event yet doesn't support Update description.
- `pre-image` is an unsupported option.
- `$changestream` as a nested pipeline of another stage is yet not supported.

## Related content

- Integrate [Change streams with Kafka (using debezium connector)](https://github.com/Azure-Samples/Delivery-tracking-vCore-debezium).
