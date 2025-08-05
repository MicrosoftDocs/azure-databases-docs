---
  title: $getField
  titleSuffix: Overview of the $getField operation in Azure Cosmos DB for MongoDB (vCore)
  description: The $getField operator allows retrieving the value of a specified field from a document.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $getField

The `$getField` operator is used to retrieve the value of a specified field from a document. It's useful when working with dynamic field names or when you need to access fields programmatically within aggregation pipelines.

## Syntax

The syntax for the `$getField` operator is as follows:

```javascript
{
  $getField: {
    field: <string>,
    input: <document>
  }
}
```

Or the shorthand syntax:

```javascript
{
  $getField: <string>
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | A string representing the name of the field to retrieve. |
| **`input`** | The document from which the field is retrieved. If not specified, defaults to the current document (`$$ROOT`). |

## Examples

Consider this sample document from the stores collection.

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
        }
      ]
    }
  ]
}
```

### Example 1: Basic field retrieval

Retrieve the total sales value using `$getField`:

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  {
    $project: {
      name: 1,
      totalSalesValue: {
        $getField: {
          field: "totalSales",
          input: "$sales"
        }
      }
    }
  }
])
```

This command produces the following output:

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "totalSalesValue": 37701
}
```

### Example 2: Shorthand syntax

Use the shorthand syntax to retrieve the store name:

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  {
    $project: {
      storeName: { $getField: "name" },
      storeLocation: { $getField: "location" }
    }
  }
])
```

This command produces the following output:

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "storeName": "First Up Consultants | Bed and Bath Center - South Amir",
  "storeLocation": {
    "lat": 60.7954,
    "lon": -142.0012
  }
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
