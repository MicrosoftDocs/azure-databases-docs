---
  title: $rename (field update operator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $rename operator allows renaming fields in documents during update operations.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $rename (field update operator)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$rename` operator is used to rename fields in documents during update operations. It removes the field with the old name and creates a new field with the specified name, preserving the original value. This operator is useful for restructuring document schemas or correcting field naming conventions.

## Syntax

The syntax for the `$rename` operator is as follows:

```javascript
{
  $rename: {
    <field1>: <newName1>,
    <field2>: <newName2>,
    ...
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The current name of the field to be renamed. |
| **`newName`** | The new name for the field. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "location": {
    "lat": 60.7954,
    "lon": -142.0012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 18,
      "partTime": 17
    }
  },
  "sales": {
    "totalSales": 37701,
    "salesByCategory": [
      {
        "categoryName": "Mattress Toppers",
        "totalSales": 37701
      }
    ]
  }
}
```

### Example 1: Renaming top-level fields

Suppose you want to rename the `name` field to `storeName` and `location` to `storeLocation`.

```javascript
db.stores.updateOne(
  { "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f" },
  {
    $rename: {
      "name": "storeName",
      "location": "storeLocation"
    }
  }
)
```

### Example 2: Renaming nested fields

You can also rename nested fields by using dot notation.

```javascript
db.stores.updateOne(
  { "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f" },
  {
    $rename: {
      "location.lat": "location.latitude",
      "location.lon": "location.longitude",
      "staff.totalStaff.fullTime": "staff.totalStaff.fullTimeEmployees"
    }
  }
)
```


### Example 3: Bulk rename operations

You can rename fields across multiple documents using `updateMany()`.

```javascript
db.stores.updateMany(
  {},
  {
    $rename: {
      "sales.totalSales": "sales.revenue",
      "staff.totalStaff": "staff.employeeCount"
    }
  }
)
```

> [!Important]
>
> If the field specified in `$rename` does not exist, the operation will have no effect on that field.
> 
> If the new field name already exists, the `$rename` operation will overwrite the existing field.
> 
> The `$rename` operator cannot be used to rename array elements or fields within array elements.
> 
> Field names cannot be empty strings or contain null characters.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
