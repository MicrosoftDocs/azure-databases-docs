---
  title: $currentDate (field update operator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $currentDate operator sets the value of a field to the current date, either as a Date or a timestamp.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 02/12/2025
---

# $currentDate (field update operator)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$currentDate` operator sets the value of a field to the current date, either as a Date or a timestamp. This operator is useful for tracking when documents were last modified or for setting creation timestamps.

## Syntax

The syntax for the `$currentDate` operator is as follows:

```javascript
{
  $currentDate: {
    <field1>: <typeSpecification1>,
    <field2>: <typeSpecification2>,
    ...
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The name of the field to set to the current date. |
| **`typeSpecification`** | Optional. Specifies the type of the date value. Can be `true` (for Date type) or `{ $type: "timestamp" }` for timestamp type. Default is `true` (Date). |

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

### Example 1: Setting current date

Add a `lastUpdated` field with the current date to a store document.

```javascript
db.stores.updateOne(
  { "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f" },
  {
    $currentDate: {
      "lastUpdated": true
    }
  }
)
```

This will add a `lastUpdated` field with the current date as a Date object.

### Example 2: Setting current timestamp

Add both a date field and a timestamp field to track modifications.

```javascript
db.stores.updateOne(
  { "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f" },
  {
    $currentDate: {
      "lastModified": true,
      "lastModifiedTimestamp": { $type: "timestamp" }
    }
  }
)
```

Output:

```json
{
  acknowledged: true,
  insertedId: null,
  matchedCount: Long("1"),
  modifiedCount: Long("1"),
  upsertedCount: 0
}
```


### Example 3: Updating nested fields

Set current date for nested fields in the document structure.

```javascript
db.stores.updateOne(
  { "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f" },
  {
    $currentDate: {
      "sales.lastSalesUpdate": true,
      "staff.lastStaffUpdate": { $type: "timestamp" }
    }
  }
)
```

After these operations, the document would include the new timestamp fields:

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "lastUpdated": ISODate("2025-02-12T10:30:45.123Z"),
  "lastModified": ISODate("2025-02-12T10:30:45.123Z"),
  "lastModifiedTimestamp": Timestamp(1739450445, 1),
  "sales": {
    "totalSales": 37701,
    "lastSalesUpdate": ISODate("2025-02-12T10:30:45.123Z"),
    "salesByCategory": [
      {
        "categoryName": "Mattress Toppers",
        "totalSales": 37701
      }
    ]
  },
  "staff": {
    "totalStaff": {
      "fullTime": 18,
      "partTime": 17
    },
    "lastStaffUpdate": Timestamp(1739450445, 1)
  }
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
