---
  title: $natural (query and projection operator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $natural operator forces the query to use the natural order of documents in a collection, providing control over document ordering and retrieval.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $natural (miscellaneous query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$natural` operator forces the query to use the natural order of documents in a collection. It can be used in sorting operations to retrieve documents in the order they were inserted or in reverse order. This operator is useful when you need predictable ordering without relying on indexed fields.

## Syntax

The syntax for the `$natural` operator in sort operations is as follows:

```javascript
{ $natural: <1 | -1> }
```

## Parameters

| | Description |
| --- | --- |
| **`1`** | Sort in forward natural order (insertion order). |
| **`-1`** | Sort in reverse natural order (reverse insertion order). |

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

### Example 1: Basic Natural Order Sorting

To retrieve stores in their natural insertion order:

```javascript
db.stores.find({}).sort({ $natural: 1 })
```

This query returns all stores in the order they were inserted into the collection.

### Example 2: Reverse Natural Order

To retrieve stores in reverse insertion order (most recently inserted first):

```javascript
db.stores.find({}).sort({ $natural: -1 })
```

This query returns all stores in reverse insertion order, with the most recently added documents appearing first.

### Example 3: Natural Order with Filtering

To find stores with total sales above a certain threshold and sort them in natural order:

```javascript
db.stores.find({
  "sales.totalSales": { $gt: 50000 }
}).sort({ $natural: 1 })
```

This query filters stores with total sales greater than 50,000 and returns them in natural insertion order.

### Example 4: Natural Order with Projection

To retrieve specific fields from stores in natural order:

```javascript
db.stores.find({}, {
  name: 1,
  "sales.totalSales": 1,
  "location.lat": 1,
  "location.lon": 1
}).sort({ $natural: 1 })
```

This query returns only the store name, total sales, and location coordinates in natural insertion order.

### Example 5: Natural Order with Limit

To get the first three stores that were inserted into the collection:

```javascript
db.stores.find({}).sort({ $natural: 1 }).limit(3)
```

This query returns the first three stores in their natural insertion order.

## Use Cases

The `$natural` operator is useful in the following scenarios:

- Audit trails: When you need to process documents in the order, they were created
- Chronological processing: For time-sensitive data where insertion order matters
- Batch processing: When processing documents in predictable order without indexes
- Debugging: To understand the natural storage order of documents in a collection


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
