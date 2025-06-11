---
  title: $unset (field update operator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $unset operator removes specified fields from documents during update operations.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $unset (field update operator)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$unset` operator is used to remove specified fields from documents during update operations. This operator completely removes the field from the document, regardless of its current value. It is useful for cleaning up document schemas, removing deprecated fields, or eliminating unnecessary data from documents.

## Syntax

The syntax for the `$unset` operator is as follows:

```javascript
{
  $unset: {
    <field1>: "",
    <field2>: "",
    ...
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The name of the field to remove. Can be a top-level field or use dot notation for nested fields. |
| **`value`** | The value is typically an empty string ("") but can be any value. The actual value is ignored; only the field name matters. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6",
  "name": "VanArsdel, Ltd. | Picture Frame Store - Port Clevelandton",
  "location": {
    "lat": 16.8331,
    "lon": -141.9922
  },
  "staff": {
    "totalStaff": {
      "fullTime": 6,
      "partTime": 8
    }
  },
  "sales": {
    "totalSales": 17676,
    "salesByCategory": [
      {
        "categoryName": "Photo Albums",
        "totalSales": 17676
      }
    ]
  },
  "temporaryField": "This should be removed",
  "outdatedInfo": {
    "oldSystem": true,
    "legacyData": "deprecated"
  }
}
```

### Example 1: Removing top-level fields

Suppose you want to remove temporary or outdated fields from a store document.

```javascript
db.stores.updateOne(
  { "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6" },
  {
    $unset: {
      "temporaryField": "",
      "outdatedInfo": ""
    }
  }
)
```

After above operation, the document would be updated as follows:

```json
{
  "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6",
  "name": "VanArsdel, Ltd. | Picture Frame Store - Port Clevelandton",
  "location": {
    "lat": 16.8331,
    "lon": -141.9922
  },
  "staff": {
    "totalStaff": {
      "fullTime": 6,
      "partTime": 8
    }
  },
  "sales": {
    "totalSales": 17676,
    "salesByCategory": [
      {
        "categoryName": "Photo Albums",
        "totalSales": 17676
      }
    ]
  }
}
```

### Example 2: Removing nested fields

You can remove specific nested fields using dot notation.

```javascript
db.stores.updateOne(
  { "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6" },
  {
    $unset: {
      "location": "",
      "staff.totalStaff.partTime": ""
    }
  }
)
```

After above operation, the document would be updated as follows:

```json
{
  "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6",
  "name": "VanArsdel, Ltd. | Picture Frame Store - Port Clevelandton",
  "location": {
    "lat": 16.8331
  },
  "staff": {
    "totalStaff": {
      "fullTime": 6
    }
  },
  "sales": {
    "totalSales": 17676,
    "salesByCategory": [
      {
        "categoryName": "Photo Albums",
        "totalSales": 17676
      }
    ]
  }
}
```

### Example 3: Removing array elements

When using `$unset` with array elements, it sets the element to `null` rather than removing it completely.

```javascript
// Assuming we have a store with multiple sales categories
db.stores.updateOne(
  { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" },
  {
    $unset: {
      "sales.salesByCategory.1": ""
    }
  }
)
```

This will set the second element (index 1) of the salesByCategory array to `null`:

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "sales": {
    "totalSales": 151864,
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2120
      },
      null,
      {
        "categoryName": "Game Controllers",
        "totalSales": 43522
      }
    ]
  }
}
```

### Example 4: Bulk unset operations

You can remove fields from multiple documents using `updateMany()`.

```javascript
// Remove deprecated fields from all stores
db.stores.updateMany(
  {},
  {
    $unset: {
      "legacyField": "",
      "deprecatedStatus": "",
      "oldVersion": ""
    }
  }
)
```

### Example 5: Conditional Field Removal

You can combine `$unset` with query conditions to selectively remove fields.

```javascript
// Remove specific fields from stores with low sales
db.stores.updateMany(
  { "sales.totalSales": { $lt: 50000 } },
  {
    $unset: {
      "premiumFeatures": "",
      "vipCustomerList": "",
      "exclusiveOffers": ""
    }
  }
)
```

### Example 6: Using $unset with other operators

You can combine `$unset` with other update operators in a single operation.

```javascript
db.stores.updateOne(
  { "_id": "26afb024-53c7-4e94-988c-5eede72277d5" },
  {
    $set: {
      "status": "updated",
      "lastModified": new Date()
    },
    $unset: {
      "temporaryData": "",
      "processingFlag": ""
    }
  }
)
```

## Important Notes

- If the field specified in `$unset` does not exist, the operation will have no effect on that field.
- The value specified in `$unset` is ignored; any value can be used, but convention is to use an empty string ("").
- When used with array elements, `$unset` sets the array element to `null` rather than removing it entirely.
- To completely remove array elements, use operators like `$pull` or `$pop` instead.
- The `$unset` operator cannot be used to remove the `_id` field.
- Multiple fields can be unset in a single operation.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]