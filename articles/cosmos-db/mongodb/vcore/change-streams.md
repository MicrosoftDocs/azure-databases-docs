---
  title: Change Stream on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: Learn how to use change streams on Azure Cosmos DB for MongoDB vCore to get the changes made to your data.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: how-to
  ms.date: 09/04/2024
---

# Change Stream on Azure Cosmos DB for MongoDB vCore (Preview)

Change streams in Azure Cosmos DB for MongoDB vCore a real-time stream of database changes that flows from your database to your application. This feature enables you to build reactive applications by subscribing to database changes, eliminating the need for continuous polling to detect changes.

> [!NOTE]
> Please register to enrol your interest using [Form](https://forms.office.com/r/G76XDQ6YSE).

## Customize Change Stream Data

The pipeline allows us to adjust the events produced by the change stream. Supported operators include the following.

- `$addFields`
- `$match`
- `$project`
- `$set`
- `$unset`

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

# [Python](#tab/python)

```python
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Connect to the MongoDB client
client = MongoClient('your_connection_string')
db = client['<database_name>']
collection = db['<collection_name>']

# Open a change stream
try:
    with collection.watch() as change_stream:
        for change in change_stream:
            print(change)
except PyMongoError as e:
    print(f"Error processing change stream: {e}")
finally:
    client.close()
```

# [Java](#tab/Java)

```java
import com.mongodb.MongoClientSettings;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.model.changestream.ChangeStreamDocument;
import org.bson.Document;
import org.bson.json.JsonWriterSettings;

public class ChangeStreamExample {
    public static void main(String[] args) {
        MongoClient mongoClient = MongoClients.create("mongodb://<username>:<password>@myCosmosDb.mongo.cosmos.azure.com:10255/?ssl=true");
        MongoDatabase database = mongoClient.getDatabase("<database_name>");
        MongoCollection<Document> collection = database.getCollection("<collection_name>");

        // Open a change stream
        MongoCursor<ChangeStreamDocument<Document>> cursor = collection.watch().iterator();

        // Listen for changes
        try {
            while (cursor.hasNext()) {
                ChangeStreamDocument<Document> change = cursor.next();
                System.out.println(change.getFullDocument().toJson(JsonWriterSettings.builder().indent(true).build()));
            }
        } catch (Exception e) {
            System.err.println("Error processing change stream: " + e);
        } finally {
            cursor.close();
            mongoClient.close();
        }
    }
}
```

> [!IMPORTANT]
> Change streams are resumable by specifying a resume token to `resumeAfter` when opening the cursor. Though it is expected that there is enough history to locate the operation associated with the token. The document observed in changestream in `_id` field represents the resumable token.
> `cursor = db.inventory.watch(resume_after=resume_token)`

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
