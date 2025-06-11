---
  title: $setOnInsert (field update operator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $setOnInsert operator sets field values only when an upsert operation results in an insert of a new document.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $setOnInsert (field update operator)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$setOnInsert` operator is used to set field values only when an upsert operation results in the insertion of a new document. If the document already exists and is being updated, the `$setOnInsert` operator has no effect. This operator is particularly useful for setting default values or initialization data that should only be applied when creating new documents.

## Syntax

The syntax for the `$setOnInsert` operator is as follows:

```javascript
{
  $setOnInsert: {
    <field1>: <value1>,
    <field2>: <value2>,
    ...
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The name of the field to set only on insert. Can be a top-level field or use dot notation for nested fields. |
| **`value`** | The value to assign to the field only when inserting a new document. Can be any valid BSON type. |

## Example

Let's understand the usage with sample json from `stores` dataset for upsert operations.

### Example 1: Basic $setOnInsert usage

Suppose you want to create or update a store record, but only set certain initialization fields when creating a new store.

```javascript
// First, let's try upserting a store that doesn't exist
db.stores.updateOne(
  { "_id": "new-store-001" },
  {
    $set: {
      "name": "TechWorld Electronics - Downtown",
      "sales.totalSales": 0
    },
    $setOnInsert: {
      "createdDate": new Date(),
      "status": "new",
      "staff.totalStaff.fullTime": 0,
      "staff.totalStaff.partTime": 0,
      "version": 1
    }
  },
  { upsert: true }
)
```
Output:
```json
{
  acknowledged: true,
  insertedId: 'new-store-001',
  matchedCount: 0,
  modifiedCount: Long("0"),
  upsertedCount: 1
}
```

Since the document with `_id: "new-store-001"` doesn't exist, this will create a new document:


```json
{
  "_id": "new-store-001",
  "name": "TechWorld Electronics - Downtown",
  "sales": {
    "totalSales": 0
  },
  "createdDate": ISODate("2025-06-05T10:30:00.000Z"),
  "status": "new",
  "staff": {
    "totalStaff": {
      "fullTime": 0,
      "partTime": 0
    }
  },
  "version": 1
}
```

### Example 2: $setOnInsert with existing document

Now, let's try to upsert the same document again with different values:

```javascript
db.stores.updateOne(
  { "_id": "new-store-001" },
  {
    $set: {
      "name": "TechWorld Electronics - Downtown Branch",
      "sales.totalSales": 5000
    },
    $setOnInsert: {
      "createdDate": new Date(),
      "status": "updated",
      "staff.totalStaff.fullTime": 10,
      "staff.totalStaff.partTime": 5,
      "version": 2
    }
  },
  { upsert: true }
)
```

Since the document already exists, only the `$set` operations will be applied, and `$setOnInsert` will be ignored:

```json
{
  "_id": "new-store-001",
  "name": "TechWorld Electronics - Downtown Branch",
  "sales": {
    "totalSales": 5000
  },
  "createdDate": ISODate("2025-06-05T10:30:00.000Z"),
  "status": "new",
  "staff": {
    "totalStaff": {
      "fullTime": 0,
      "partTime": 0
    }
  },
  "version": 1
}
```

### Example 3: Complex $setOnInsert with nested objects

You can use `$setOnInsert` to initialize complex nested structures:

```javascript
db.stores.updateOne(
  { "name": "Gaming Paradise - Mall Location" },
  {
    $set: {
      "location.lat": 35.6762,
      "location.lon": 139.6503
    },
    $setOnInsert: {
      "_id": "gaming-store-mall-001",
      "createdDate": new Date(),
      "status": "active",
      "staff": {
        "totalStaff": {
          "fullTime": 8,
          "partTime": 12
        },
        "manager": "Alex Johnson",
        "departments": ["gaming", "accessories", "repairs"]
      },
      "sales": {
        "totalSales": 0,
        "salesByCategory": []
      },
      "operatingHours": {
        "weekdays": "10:00-22:00",
        "weekends": "09:00-23:00"
      },
      "metadata": {
        "version": 1,
        "source": "store-management-system"
      }
    }
  },
  { upsert: true }
)
```

### Example 4: Using $setOnInsert with arrays

You can initialize arrays and complex data structures:

```javascript
db.stores.updateOne(
  { "address.city": "New Tech City" },
  {
    $set: {
      "name": "Future Electronics Hub",
      "sales.totalSales": 25000
    },
    $setOnInsert: {
      "_id": "future-electronics-001",
      "establishedDate": new Date(),
      "categories": ["electronics", "gadgets", "smart-home"],
      "promotionEvents": [],
      "ratings": {
        average: 0,
        count: 0,
        reviews: []
      },
      "inventory": {
        lastUpdated: new Date(),
        totalItems: 0,
        lowStockAlerts: []
      }
    }
  },
  { upsert: true }
)
```

> [!Important]

> The `$setOnInsert` operator only takes effect during upsert operations (`{ upsert: true }`).
> 
> If the document exists, `$setOnInsert` fields are completely ignored.
> 
> `$setOnInsert` is commonly used with `$set` to handle both update and insert scenarios in a single operation.
> 
> You can combine `$setOnInsert` with other update operators like `$inc`, `$push`, etc.
> 
> The `$setOnInsert` operator is ideal for setting creation timestamps, default values, and initialization data.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
