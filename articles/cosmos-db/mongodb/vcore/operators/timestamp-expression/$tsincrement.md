---
  title: The `$tsIncrement` operator returns the increment value from a timestamp.
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $tsIncrement operator extracts the increment portion from a timestamp value.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/09/2025
---

# $tsIncrement (variable expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$tsIncrement` operator returns the increment value from a timestamp. Timestamps in MongoDB consist of two parts: a time value (in seconds since epoch) and an increment value. This operator extracts the increment portion.

## Syntax

The syntax for the `$tsIncrement` operator is as follows:

```javascript
{
  $tsIncrement: <expression>
}
```

## Parameters

| | Description |
| --- | --- |
| **`expression`** | An expression that evaluates to a timestamp. If the expression does not evaluate to a timestamp, `$tsIncrement` returns an error. |

## Example

Let's understand the usage with sample JSON from the `stores` dataset. For demonstration purposes, we'll add timestamp fields to show how `$tsIncrement` works.

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
  },
  "lastUpdated": Timestamp({ t: 1640995200, i: 5 }),
  "storeOpeningDate": ISODate("2021-10-03T00:00:00.000Z"),
  "promotionEvents": [
    {
      "eventName": "Price Drop Palooza",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 21
        },
        "endDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 30
        }
      },
      "discounts": [
        {
          "categoryName": "Bath Accessories",
          "discountPercentage": 18
        },
        {
          "categoryName": "Pillow Top Mattresses",
          "discountPercentage": 17
        },
        {
          "categoryName": "Bathroom Scales",
          "discountPercentage": 9
        }
      ]
    }
  ]
}
```

### Example 1: Extract increment from audit timestamp

Extract the increment value from the last updated timestamp in the audit log.

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  {
    $project: {
      name: 1,
      lastUpdatedIncrement: {
        $tsIncrement: "$auditLog.lastUpdated"
      }
    }
  }
])
```

This will produce an output showing the increment value from the timestamp:

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "lastUpdatedIncrement": Long("5")
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
