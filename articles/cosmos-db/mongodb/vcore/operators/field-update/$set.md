---
  title: $set
  titleSuffix: Overview of the $set operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $set operator sets the value of a field in a document during update operations.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 02/12/2025
---

# $set

The `$set` operator is used to set the value of a field in a document during update operations. If the field does not exist, `$set` will create the field with the specified value. If the field already exists, `$set` will replace the existing value with the new value. This is one of the most commonly used update operators in MongoDB.

## Syntax

The syntax for the `$set` operator is as follows:

```javascript
{
  $set: {
    <field1>: <value1>,
    <field2>: <value2>,
    ...
  }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The name of the field to set. Can be a top-level field or use dot notation for nested fields. |
| **`value`** | The value to assign to the field. Can be any valid BSON type. |

## Example

Consider this sample document from the stores collection.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "location": {
    "lat": 70.1272,
    "lon": 69.7296
  },
  "staff": {
    "totalStaff": {
      "fullTime": 19,
      "partTime": 20
    }
  },
  "sales": {
    "totalSales": 151864,
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2120
      },
      {
        "categoryName": "Home Theater Projectors",
        "totalSales": 45004
      }
    ]
  }
}
```

### Example 1: Setting top-level fields

Suppose you want to update the store's total sales and add a new field for the store's status.

```javascript
db.stores.updateOne(
  { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" },
  {
    $set: {
      "sales.totalSales": 160000,
      "status": "active",
      "lastUpdated": new Date()
    }
  }
)
```

After above operation, the document would be updated as follows:

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "location": {
    "lat": 70.1272,
    "lon": 69.7296
  },
  "staff": {
    "totalStaff": {
      "fullTime": 19,
      "partTime": 20
    }
  },
  "sales": {
    "totalSales": 160000,
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2120
      },
      {
        "categoryName": "Home Theater Projectors",
        "totalSales": 45004
      }
    ]
  },
  "status": "active",
  "lastUpdated": ISODate("2025-06-05T10:30:00.000Z")
}
```

### Example 2: Setting nested fields

You can set values for nested fields using dot notation.

```javascript
db.stores.updateOne(
  { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" },
  {
    $set: {
      "location.address": "123 Entertainment Blvd",
      "location.city": "East Linwoodbury",
      "staff.totalStaff.contractors": 5,
      "staff.manager": "John Smith"
    }
  }
)
```

After above operation, the document would be updated as follows:

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "location": {
    "lat": 70.1272,
    "lon": 69.7296,
    "address": "123 Entertainment Blvd",
    "city": "East Linwoodbury"
  },
  "staff": {
    "totalStaff": {
      "fullTime": 19,
      "partTime": 20,
      "contractors": 5
    },
    "manager": "John Smith"
  },
  "sales": {
    "totalSales": 151864,
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2120
      },
      {
        "categoryName": "Home Theater Projectors",
        "totalSales": 45004
      }
    ]
  }
}
```

### Example 3: Setting array elements

You can set specific array elements using positional notation.

```javascript
db.stores.updateOne(
  { 
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "sales.salesByCategory.categoryName": "Sound Bars"
  },
  {
    $set: {
      "sales.salesByCategory.$.totalSales": 2500,
      "sales.salesByCategory.$.lastUpdated": new Date()
    }
  }
)
```

### Example 4: Bulk set operations

You can update multiple documents using `updateMany()`.

```javascript
db.stores.updateMany(
  { "sales.totalSales": { $gt: 100000 } },
  {
    $set: {
      "category": "high-volume",
      "priority": 1,
      "reviewDate": new Date()
    }
  }
)
```

> [!Important]
>
> If the field specified in `$set` does not exist, it will be created.
> 
> If the field already exists, its value will be replaced with the new value.
> 
> The `$set` operator can be used with any valid BSON data types including objects, arrays, and primitive types.
> 
> When using dot notation with arrays, you can use positional operators (`$`, `$[]`, `$[<identifier>]`) to target specific array elements.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
