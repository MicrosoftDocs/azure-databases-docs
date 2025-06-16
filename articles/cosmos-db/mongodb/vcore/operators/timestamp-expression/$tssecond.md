---
  title: $tsSecond (variable expression)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $tsSecond operator extracts the seconds portion from a timestamp value.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/09/2025
---

# $tsSecond (variable expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$tsSecond` operator returns the seconds value from a timestamp. Timestamps consist of two parts: a time value (in seconds since epoch) and an increment value. This operator extracts the seconds portion, which represents the time since the Unix epoch (January 1, 1970, 00:00:00 UTC).

## Syntax

The syntax for the `$tsSecond` operator is as follows:

```javascript
{
  $tsSecond: <expression>
}
```

## Parameters

| | Description |
| --- | --- |
| **`expression`** | An expression that evaluates to a timestamp. If the expression does not evaluate to a timestamp, `$tsSecond` returns an error. |

## Example

Let's understand the usage with sample JSON from the `stores` dataset.

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

### Example 1: Extract seconds from audit timestamp

The example extracts the seconds value from the last updated timestamp in the audit log.

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  {
    $project: {
      name: 1,
      lastUpdatedSeconds: {
        $tsSecond: "$lastUpdated"
      },
      lastUpdatedDate: {
        $toDate: {
          $multiply: [
            { $tsSecond: "$lastUpdated" },
            1000
          ]
        }
      }
    }
  }
])
```

This will produce an output showing the seconds value from the timestamp and its corresponding date:

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "lastUpdatedSeconds": Long("1640995200"),
  "lastUpdatedDate": ISODate("2022-01-01T00:00:00.000Z")
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]