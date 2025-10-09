---
title: Manage Indexing
titleSuffix: Azure Cosmos DB for MongoDB
description: Learn how to manage indexing in Azure Cosmos DB for MongoDB to optimize query performance. Explore types, benefits, and best practices for faster queries.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.topic: how-to
ms.devlang: javascript
ms.date: 08/20/2025
ms.custom:
  - cosmos-db-video
  - sfi-image-nochange
appliesto:
  - ✅ MongoDB
---

# Manage indexing in Azure Cosmos DB for MongoDB

Azure Cosmos DB for MongoDB lets you use indexing to speed up query performance. This article shows you how to manage and optimize indexes for faster data retrieval and better efficiency.

> [!VIDEO https://www.youtube.com/embed/qHFVwvfqZMA?si=rq2EOJSH8qY_09br]

## Indexing for MongoDB server version 3.6 and higher

Azure Cosmos DB for MongoDB server version 3.6+ automatically indexes the `_id` field and the shard key (only in sharded collections). The API enforces the uniqueness of the `_id` field per shard key.

The API for MongoDB works differently from Azure Cosmos DB for NoSQL, which indexes all fields by default.

### Editing indexing policy

Edit your indexing policy in Data Explorer in the Azure portal. Add single field and wildcard indexes from the indexing policy editor in Data Explorer:

:::image type="content" source="media/indexing/indexing-policy-editor.png" alt-text="Screenshot of indexing policy editor in Azure Cosmos DB for MongoDB.":::

> [!NOTE]
> You can't create compound indexes using the indexing policy editor in the Data Explorer.

## Index types

### Single field

Create an index on any single field. The sort order of the single field index doesn't matter. Use the following command to create an index on the field `name`:

`db.coll.createIndex({name:1})`

Create the same single field index on `name` in the Azure portal:

:::image type="content" source="media/indexing/add-index.png" alt-text="Screenshot of adding a name index in the indexing policy editor.":::

A query uses multiple single field indexes where available. Create up to 500 single field indexes per collection.

### Compound indexes (MongoDB server version 3.6+)

In the API for MongoDB, use compound indexes with queries that sort multiple fields at once. For queries with multiple filters that don't need to sort, create multiple single field indexes instead of a compound index to save on indexing costs.

A compound index or single field indexes for each field in the compound index result in the same performance for filtering in queries.

Compound indexes on nested fields aren't supported by default because of limitations with arrays. If a nested field doesn't have an array, the index works as intended. If a nested field has an array anywhere on the path, that value is ignored in the index.

For example, a compound index containing `people.dylan.age` works in this case because there's no array on the path:

```json
{
  "people": {
    "dylan": {
      "name": "Dylan",
      "age": "25"
    },
    "reed": {
      "name": "Reed",
      "age": "30"
    }
  }
}
```

The same compound index doesn't work in this case because there's an array in the path:

```json
{
  "people": [
    {
      "name": "Dylan",
      "age": "25"
    },
    {
      "name": "Reed",
      "age": "30"
    }
  ]
}
```

Enable this feature for your database account by [enabling the 'EnableUniqueCompoundNestedDocs' capability](how-to-configure-capabilities.md).


> [!NOTE]
> You can't create compound indexes on arrays.

The following command creates a compound index on the fields `name` and `age`:

```mongodb
db.coll.createIndex({name:1,age:1})
```

You can use compound indexes to sort efficiently on multiple fields at once, as shown in the following example:

```mongodb
db.coll.find().sort({name:1,age:1})
```

You can also use the preceding compound index to efficiently sort on a query with the opposite sort order on all fields. Here's an example:

```mongodb
db.coll.find().sort({name:-1,age:-1})
```

However, the sequence of the paths in the compound index must exactly match the query. Here's an example of a query that would require an extra compound index:

```mongodb
db.coll.find().sort({age:1,name:1})
```

### Multikey indexes

Azure Cosmos DB creates multikey indexes to index content in arrays. If you index a field with an array value, Azure Cosmos DB automatically indexes each element in the array.

### Geospatial indexes

Many geospatial operators benefit from geospatial indexes. Azure Cosmos DB for MongoDB supports `2dsphere` indexes. The API doesn't support `2d` indexes yet.

Here's an example of creating a geospatial index on the `location` field:

```mongodb
db.coll.createIndex({ location : "2dsphere" })
```

### Text indexes

Azure Cosmos DB for MongoDB doesn't support text indexes. For text search queries on strings, use [Azure AI Search](/azure/search/search-howto-index-cosmosdb) integration with Azure Cosmos DB. 

## Wildcard indexes

Use wildcard indexes to support queries against unknown fields. Imagine a collection that has data about families.

Here's part of an example document in that collection:

```json
"children": [
  {
    "firstName": "Henriette Thaulow",
    "grade": "5"
  }
]
```

Here's another example with a different set of properties in `children`:

```json
"children": [
  {
    "familyName": "Merriam",
    "givenName": "Jesse",
    "pets": [
      { "givenName": "Goofy" },
      { "givenName": "Shadow" }
    ]
  },
  {
    "familyName": "Merriam",
    "givenName": "John",
  }
]
```

Documents in this collection can have many different properties. To index all data in the `children` array, create separate indexes for each property or create one wildcard index for the entire `children` array.

### Create a wildcard index

Use the following command to create a wildcard index on any properties within `children`:

```mongodb
db.coll.createIndex({"children.$**" : 1})
```

- *Unlike in MongoDB, wildcard indexes can support multiple fields in query predicates*. There's no difference in query performance if you use a single wildcard index instead of creating a separate index for each property.

Create the following index types using wildcard syntax:

- Single field
- Geospatial

### Indexing all properties

Create a wildcard index on all fields with the following command:

```mongodb
db.coll.createIndex( { "$**" : 1 } )
```

Create wildcard indexes using Data Explorer in the Azure portal:

![Add wildcard index in indexing policy editor](./media/indexing/add-wildcard-index.png)

> [!NOTE]
> If you're just starting development, start with a wildcard index on all fields. This approach simplifies development and makes it easier to optimize queries.

Documents with many fields can have a high Request Unit (RU) charge for writes and updates. If you have a write-heavy workload, use individually indexed paths instead of wildcards.

### Limitations

Wildcard indexes don't support any of the following index types or properties:

- Compound
- TTL
- Unique

- *Unlike in MongoDB*, in Azure Cosmos DB for MongoDB you can't use wildcard indexes for:

- Creating a wildcard index that includes multiple specific fields

  ```json
  db.coll.createIndex(
    { "$**" : 1 },
    { "wildcardProjection " :
      {
        "children.givenName" : 1,
        "children.grade" : 1
      }
    }
  )
  ```

- Creating a wildcard index that excludes multiple specific fields

  ```json
  db.coll.createIndex(
    { "$**" : 1 },
    { "wildcardProjection" :
      {
        "children.givenName" : 0,
        "children.grade" : 0
      }
    }
  )
  ```

As an alternative, create multiple wildcard indexes.

## Index properties

The following operations are common for accounts that use wire protocol version 4.0 and earlier versions. Learn more about [supported indexes and indexed properties](feature-support-40.md#indexes-and-index-properties).

### Unique indexes

[Unique indexes](../unique-keys.md) help make sure that two or more documents don't have the same value for indexed fields.

Run the following command to create a unique index on the `student_id` field:

```mongodb
db.coll.createIndex( { "student_id" : 1 }, {unique:true} )

{
  "_t" : "CreateIndexesResponse",
  "ok" : 1,
  "createdCollectionAutomatically" : false,
  "numIndexesBefore" : 1,
  "numIndexesAfter" : 4
}
```

For sharded collections, provide the shard (partition) key to create a unique index. All unique indexes on a sharded collection are compound indexes, and one of the fields is the shard key. The shard key should be the first field in the index definition.

Run the following commands to create a sharded collection named `coll` (with `university` as the shard key) and a unique index on the `student_id` and `university` fields:

```mongodb
db.runCommand({shardCollection: db.coll._fullName, key: { university: "hashed"}});
{
  "_t" : "ShardCollectionResponse",
  "ok" : 1,
  "collectionsharded" : "test.coll"
}
```

```mongodb
db.coll.createIndex( { "university" : 1, "student_id" : 1 }, {unique:true});
{
  "_t" : "CreateIndexesResponse",
  "ok" : 1,
  "createdCollectionAutomatically" : false,
  "numIndexesBefore" : 3,
  "numIndexesAfter" : 4
}
```

If you omit the `"university":1` clause in the preceding example, you see the following error message:

`cannot create unique index over {student_id : 1.0} with shard key pattern { university : 1.0 }`

#### Limitations

Create unique indexes while the collection is empty.

Azure Cosmos DB for MongoDB accounts with [continuous backup](../continuous-backup-restore-introduction.md#current-limitations) don't support creating a unique index for an existing collection. For such an account, unique indexes must be created along with their collection creation, which must and can only be done using the create collection [extension commands](./custom-commands.md#create-collection).
```mongodb
db.runCommand({customAction:"CreateCollection", collection:"coll", shardKey:"student_id", indexes:[
{key: { "student_id" : 1}, name:"student_id_1", unique: true}
]});
```

Unique indexes on nested fields aren't supported by default because of limitations with arrays. If your nested field doesn't have an array, the index works as intended. If your nested field has an array anywhere on the path, that value is ignored in the unique index, and uniqueness isn't preserved for that value.

For example, a unique index on `people.tom.age` works in this case because there's no array on the path:

```json
{
  "people": {
    "tom": {
      "age": "25"
    },
    "mark": {
      "age": "30"
    }
  }
}
```

But doesn't work in this case because there's an array in the path:

```json
{
  "people": {
    "tom": [
      {
        "age": "25"
      }
    ],
    "mark": [
      {
        "age": "30"
      }
    ]
  }
}
```

This feature can be enabled for your database account by [enabling the 'EnableUniqueCompoundNestedDocs' capability](how-to-configure-capabilities.md).


### TTL indexes

To let documents expire in a collection, create a [time-to-live (TTL) index](../time-to-live.md). A TTL index is an index on the `_ts` field with an `expireAfterSeconds` value.

Example:

```mongodb
db.coll.createIndex({"_ts":1}, {expireAfterSeconds: 10})
```

The preceding command deletes any documents in the `db.coll` collection that were modified more than 10 seconds ago.

> [!NOTE]
> The **_ts** field is specific to Azure Cosmos DB and isn't accessible from MongoDB clients. It's a reserved (system) property that contains the time stamp of the document's last modification.

## Track index progress

Version 3.6+ of Azure Cosmos DB for MongoDB supports the `currentOp()` command to track index progress on a database instance. This command returns a document with information about in-progress operations on a database instance. Use the `currentOp` command to track all in-progress operations in native MongoDB. In Azure Cosmos DB for MongoDB, this command only tracks the index operation.

Here are some examples of how to use the `currentOp` command to track index progress:

- Get index progress for a collection:

  ```mongodb
  db.currentOp({"command.createIndexes": <collectionName>, "command.$db": <databaseName>})
  ```

- Get index progress for all collections in a database:

  ```mongodb
  db.currentOp({"command.$db": <databaseName>})
  ```

- Get index progress for all databases and collections in an Azure Cosmos DB account:

  ```mongodb
  db.currentOp({"command.createIndexes": { $exists : true } })
  ```

### Examples of index progress output

Index progress details show the percentage of progress for the current index operation. Here are examples of the output document format for different stages of index progress:

- An index operation on a "foo" collection and "bar" database that's 60 percent complete has the following output document. The `Inprog[0].progress.total` field shows 100 as the target completion percentage.

  ```json
  {
    "inprog": [
      {
        ...
        "command": {
          "createIndexes": foo
          "indexes": [],
          "$db": bar
        },
        "msg": "Index Build (background) Index Build (background): 60 %",
        "progress": {
          "done": 60,
          "total": 100
        },
        ...
      }
    ],
    "ok": 1
  }
  ```

- If an index operation just started on a "foo" collection and "bar" database, the output document can show 0 percent progress until it reaches a measurable level.

  ```json
  {
    "inprog": [
      {
        ...
        "command": {
          "createIndexes": foo
          "indexes": [],
          "$db": bar
        },
        "msg": "Index Build (background) Index Build (background): 0 %",
        "progress": {
          "done": 0,
          "total": 100
        },
        ...
      }
    ],
    "ok": 1
  }
  ```

- When the index operation finishes, the output document shows empty `inprog` operations.

  ```json
  {
    "inprog" : [],
    "ok" : 1
  }
  ```

## Background index updates

Index updates always run in the background, no matter what value you set for the **Background** index property. Because index updates use Request Units (RUs) at a lower priority than other database actions, index changes don't cause downtime for writes, updates, or deletes.

Adding a new index doesn't affect read availability. Queries use new indexes only after the index transformation finishes. During the transformation, the query engine keeps using existing indexes, so you see similar read performance as before you start the indexing change. Adding new indexes doesn't risk incomplete or inconsistent query results.

If you remove indexes and immediately run queries that filter on those dropped indexes, results can be inconsistent and incomplete until the index transformation finishes. The query engine doesn't provide consistent or complete results for queries that filter on newly removed indexes. Most developers don't drop indexes and then immediately query them, so this situation is unlikely.

> [!NOTE]
> You can [track index progress](#track-index-progress).

## `reIndex` command

The `reIndex` command recreates all indexes on a collection. In rare cases, running the `reIndex` command can fix query performance or other index issues in your collection. If you're experiencing indexing issues, try recreating the indexes with the `reIndex` command. 

Run the `reIndex` command using the following syntax:

```mongodb
db.runCommand({ reIndex: <collection> })
```

Use the following syntax to check if running the `reIndex` command improves query performance in your collection:

```mongodb
db.runCommand({"customAction":"GetCollection",collection:<collection>, showIndexes:true})
```

Sample output:

```json
{
  "database": "myDB",
  "collection": "myCollection",
  "provisionedThroughput": 400,
  "indexes": [
    {
      "v": 1,
      "key": {
        "_id": 1
      },
      "name": "_id_",
      "ns": "myDB.myCollection",
      "requiresReIndex": true
    },
    {
      "v": 1,
      "key": {
        "b.$**": 1
      },
      "name": "b.$**_1",
      "ns": "myDB.myCollection",
      "requiresReIndex": true
    }
  ],
  "ok": 1
}
```

If `reIndex` improves query performance, **requiresReIndex** is true. If `reIndex` doesn't improve query performance, this property is omitted.

## Migrate collections with indexes

You can only create unique indexes when the collection has no documents. Popular MongoDB migration tools try to create unique indexes after importing the data. To work around this issue, manually create the corresponding collections and unique indexes instead of letting the migration tool try. You achieve this behavior for ```mongorestore``` by using the `--noIndexRestore` flag in the command line.

## Indexing for MongoDB version 3.2

Indexing features and defaults differ for Azure Cosmos DB accounts that use version 3.2 of the MongoDB wire protocol. Check your account's version at [feature-support-36.md#protocol-support](feature-support-36.md#protocol-support), and upgrade to version 3.6 at [upgrade-version.md](upgrade-version.md).

If you're using version 3.2, this section highlights key differences from versions 3.6 and later.

### Dropping default indexes (version 3.2)

Unlike versions 3.6 and later, Azure Cosmos DB for MongoDB version 3.2 indexes every property by default. Use the following command to drop these default indexes for a collection (`coll`):

```mongodb
db.coll.dropIndexes()
```

```json
{ "_t" : "DropIndexesResponse", "ok" : 1, "nIndexesWas" : 3 }
```

After you drop the default indexes, add more indexes as you do in version 3.6 and later.

### Compound indexes (version 3.2)

Compound indexes reference multiple fields in a document. To create a compound index, upgrade to version 3.6 or 4.0 at [upgrade-version.md](upgrade-version.md).

### Wildcard indexes (version 3.2)

To create a wildcard index, upgrade to version 4.0 or 3.6 at [upgrade-version.md](upgrade-version.md).

## Next steps

- [Indexing in Azure Cosmos DB](../index-policy.md)
- [Expire data in Azure Cosmos DB automatically with time to live](../time-to-live.md)
