---
title:  Indexes on Azure DocumentDB
description: Basic know-how for efficient usage of indexes on Azure DocumentDB.
author: avijitgupta
ms.author: avijitgupta
ms.topic: concept-article
ms.date: 09/23/2024
---

# Manage indexing in Azure DocumentDB

Indexes are structures that improve data retrieval speed by providing quick access to fields in a collection. They work by creating an ordered set of pointers to data, often based on key fields. Azure DocumentDB utilizes indexes in multiple contexts, including query push down, unique constraints and sharding.

> [!IMPORTANT]
> The "_id" field is the **only** field indexed by default & maximum size of the field can be `2 KB`. It is recommended to add additional indexes based on query filters & predicates to optimize performance.

## Index types

For simplicity, let us consider an example of a blog application with the following setup:

- **Database name**: `cosmicworks`
- **Collection name**: `products`

This example application stores articles as documents with the following structure. All the example quoted further utilizes the structure of this collection.

```json
{
  "_id": ObjectId("617a34e7a867530bff1b2346"),
  "title": "Azure DocumentDB - A Game Changer",
  "content": "Azure DocumentDB is a globally distributed, multi-model database service.",
  "author": {lastName: "Doe", firstName: "John"},
  "category": "Technology",
  "launchDate": ISODate("2024-06-24T10:08:20.000Z"),
  "published": true
}
```

## Single field indexes

Single field indexes store information from a single field in a collection. The sort order of the single field index doesn't matter. `_id` field remains indexed by default.

Azure DocumentDB supports creating index at following

- Top-level document fields.
- Embedded document.
- Fields within embedded document.

The following command creates a single field index on the field `author` and the following command creates it on an embedded field `firstName`.

```javascript
use cosmicworks

db.products.createIndex({"author": 1})

// indexing embedded property
db.products.createIndex({"author.firstName": -1})
```

One query can use multiple single field indexes where available.

> [!NOTE]
> Azure DocumentDB allows creating maximum of 64 indexes on a collection. Depending on the tier, we can plan extension up to 300 indexes upon request.

## Compound indexes

Compound indexes improve database performance by allowing efficient **querying and sorting** based on multiple fields within documents. This optimization reduces the need to scan entire collections, speeding up data retrieval and organization.

The following command creates a compound index on the fields `author` and `launchDate` in opposite sort order.

```javascript
use cosmicworks

db.products.createIndex({"author":1, "launchDate":-1})
```

`Order` of fields affect the selectivity or utilization of index. The `find` query wouldn't utilize the index created.

```javascript
use cosmicworks

db.products.find({"launchDate": {$gt: ISODate("2024-06-01T00:00:00.000Z")}})
```

### Limitations

- Maximum of 32 fields\paths within a compound index.

## Partial indexes

Indexes that have an associated query filter that describes when to generate a term in the index.

```javascript
use cosmicworks

db.products.createIndex (
   { "author": 1, "launchDate": 1 },
   { partialFilterExpression: { "launchDate": { $gt: ISODate("2024-06-24T10:08:20.000Z") } } }
)
```

### Limitations

- Partial indexes don't support `ORDER BY` or `UNIQUE` unless the filter qualifies.

## Text indexes

Text indexes are special data structures that optimize text-based queries, making them faster and more efficient.

Use the `createIndex` method with the `text` option for creating a text index on the `title` field.

```javascript
use cosmicworks;

db.products.createIndex({ title: "text" })
```

> [!NOTE]
> While you can define only one text index per collection, Azure DocumentDB allows you to create text indexes on combination of multiple fields to enable you to perform text searches across different fields in your documents.

### Configure text index options

Text indexes in Azure DocumentDB come with several options to customize their behavior. For example, you can specify the language for text analysis, set weights to prioritize certain fields, and configure case-insensitive searches. Here's an example of creating a text index with options:

- Create an index to support search on both the `title` and `content` fields with English language support. Also, assign higher weights to the `title` field to prioritize it in search results.

    ```javascript
    use cosmicworks

    db.products.createIndex(
        { title: "text", content: "text" },
        { default_language: "english", weights: { title: 10, content: 5 }, caseSensitive: false }
    )
    ```

> [!NOTE]
> When a client performs a text search query with the term "DocumentDB", the score for each document in the collection will be calculated based on the presence and frequency of the term in both the "title" and "content" fields, with higher importance given to the "title" field due to its higher weight.

### Perform a text search using a text index

Once the text index is created, you can perform text searches using the "text" operator in your queries. The text operator takes a search string and matches it against the text index to find relevant documents.

- Perform a text search for the phrase `DocumentDB`.

    ```javascript
    use cosmicworks

    db.products.find(
      { $text: { $search: "DocumentDB" } }
    )
    ```

- Optionally, use the `$meta` projection operator along with the `textScore` field in a query to see the weight

    ```javascript
    use cosmicworks

    db.products.find(
    { $text: { $search: "DocumentDB" } },
    { score: { $meta: "textScore" } }
    )
    ```

### Limitations

- Only one text index can be defined on a collection.
- Sort operations can't use the ordering of the text index in MongoDB.
- Hint() isn't supported in combination with a query using $text expression.
- Text indexes can be relatively large, consuming significant storage space compared to other index types.

## WildCard indexes

Index on single field, indexes all paths beneath the `field` , excluding other fields that are on the same level. For example, for the following sample document

```json
{
 "children":
    {
     "familyName": "Merriam",
     "pets": { "details": {“name”: "Goofy", ”age”: 3} }
   } 
}
```

Creating an index on { "pets.$**": 1 }, creates index on details & subdocument properties but doesn't create an index on "familyName".

### Limitations

- Wildcard indexes can't support unique indexes.
- Wildcard indexes don't support push downs of `ORDER BY` unless the filter includes only paths present in the wildcard (since they don't index undefined elements)
- A compound wildcard index can only have `one` wildcard term and `one` or more index terms.
`{ "pets.$**": 1, “familyName”: 1 }`

## Geospatial indexes

Geospatial indexes support queries on data stored as GeoJSON objects or legacy coordinate pairs. You can use geospatial indexes to improve performance for queries on geospatial data or to run certain geospatial queries.

Azure DocumentDB provides two types of geospatial indexes:

- 2dsphere Indexes, which support queries that interpret geometry on a sphere.
- 2d Indexes, which support queries that interpret geometry on a flat surface.

### 2d indexes

2d indexes are supported only with legacy coordinate pair style of storing geospatial data.

Use the `createIndex` method with the `2d` option for creating a geospatial index on the `location` field.

```javascript
db.places.createIndex({ "location": "2d"});
```

### Limitations

- Only `one` location field can be part of the `2d` index and only `one` other non-geospatial field can be part of the `compound 2d` index
`db.places.createIndex({ "location": "2d", "non-geospatial-field": 1 / -1 })`

### 2dsphere indexes

`2dsphere` indexes support geospatial queries on an earth-like sphere. It can support both GeoJSON objects or legacy coordinate pairs. `2dSphere` indexes work with the GeoJSON style of storing data, if legacy points are encountered then it would convert to GeoJSON point.

Use the `createIndex` method with the `2dsphere` option for creating a geospatial index on the `location` field.

```javascript
db.places.createIndex({ "location": "2dsphere"});
```

`2dsphere` indexes allow creating indexes on multiple geospatial and multiple non-geospatial data fields.
`db.places.createIndex({ "location": "2d", "non-geospatial-field": 1 / -1, ... "more non-geospatial-field": 1 / -1 })`

### Limitations

- A compound index using a regular index and geospatial index isn't supported. Creating either of the geospatial indexes would lead into errors.

    ```javascript
    // Compound Regular & 2dsphere indexes are not supported yet
    db.collection.createIndex({a: 1, b: "2dsphere"})

    // Compound 2d indexes are not supported yet
    db.collection.createIndex({a: "2d", b: 1})
    ```

- Polygons with holes don't work. Inserting a Polygon with hole isn't restricted though `$geoWithin` query fails for scenarios:
  1. If the query itself has polygon with holes

      ```javascript
      coll.find(
        {
            "b": {
                "$geoWithin": {
                    "$geometry": {
                        "coordinates": [
                            [
                                [ 0, 0], [0, 10], [10, 10],[10,0],[0, 0]
                            ],
                            [
                                [5, 5], [8, 5], [ 8, 8], [ 5, 8], [ 5, 5]
                            ]
                        ],
                        "type": "Polygon"
                    }
                }
            }
        })

      // MongoServerError: $geoWithin currently doesn't support polygons with holes
      ```

  2. If there's any unfiltered document that has polygon with holes.
  
      ```javascript
      [mongos] test> coll.find()
        [
          {
            _id: ObjectId("667bf7560b4f1a5a5d71effa"),
            b: {
              type: 'Polygon',
              coordinates: [
                [ [ 0, 0 ], [ 0, 10 ], [ 10, 10 ], [ 10, 0 ], [ 0, 0 ] ],
                [ [ 5, 5 ], [ 8, 5 ], [ 8, 8 ], [ 5, 8 ], [ 5, 5 ] ]
              ]
            }
          }
        ]
      // MongoServerError: $geoWithin currently doesn't support polygons with holes
      ```

  3. `key` field is mandatory while using `geoNear`.

      ```javascript
       [mongos] test> coll.aggregate([{ $geoNear: { $near: { "type": "Point", coordinates: [0, 0] } } }])

       // MongoServerError: $geoNear requires a 'key' option as a String
      ```

## Next steps

- Learn about indexing [Best practices](how-to-create-indexes.md) for most efficient outcomes.
- Learn about [background indexing](background-indexing.md)
- Learn here to work with [Text indexing](how-to-create-text-index.md).
- Learn here about [Wildcard indexing](how-to-create-wildcard-indexes.md).
