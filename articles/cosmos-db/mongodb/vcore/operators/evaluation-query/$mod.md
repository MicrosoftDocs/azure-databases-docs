---
  title: $mod
  titleSuffix: Overview of the $mod operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $mod operator performs a modulo operation on the value of a field and selects documents with a specified result.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 07/25/2025
---

# $mod

The `$mod` operator performs a modulo operation on the value of a field and selects documents with a specified result. This operator is useful for finding documents where a numeric field value, when divided by a divisor, leaves a specific remainder. It commonly serves for pagination, sampling data, or finding patterns in numeric sequences.

## Syntax

```Javascript
{
  <field>: { $mod: [ <divisor>, <remainder> ] }
}
```

## Parameters

| Parameters | Description |
| --- | --- |
| **`<field>`** | The field to perform the modulo operation on. The field must contain numeric values. |
| **`<divisor>`** | The number to divide the field value by. Must be a positive number. |
| **`<remainder>`** | The expected remainder after the modulo operation. Must be a non-negative number less than the divisor. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "new-store-001",
  "name": "TechWorld Electronics - Downtown Branch",
  "sales": {
    "totalSales": 5000
  },
  "createdDate": { "$date": "2025-06-11T11:11:32.262Z" },
  "status": "new",
  "staff": {
    "totalStaff": {
      "fullTime": 0,
      "partTime": 0
    }
  },
  "version": 1,
  "storeOpeningDate": { "$date": "2025-06-11T11:11:32.262Z" }
}
```

### Example 1: Find stores with sales divisible by 1000

The example retrieves stores where total sales are divisible by 1000 (useful for identifying round sales figures).

```javascript
db.stores.find({
  "sales.totalSales": { $mod: [1000, 0] }
}).limit(2)
```

This query identifies stores with sales figures that are exact multiples of 1000, which might indicate promotional pricing or bulk sales patterns.

```json
  {
    "_id": "new-store-001",
    "name": "TechWorld Electronics - Downtown Branch",
    "sales": {
      "totalSales": 5000
    },
    "createdDate": "2025-06-11T11:11:32.262Z",
    "status": "new",
    "staff": {
      "totalStaff": {
        "fullTime": 0,
        "partTime": 0
      }
    },
    "version": 1
  },
  {
    "_id": "gaming-store-mall-001",
    "name": "Gaming Paradise - Mall Location",
    "location": {
      "lat": 35.6762,
      "lon": 139.6503
    },
    "createdDate": "2025-06-11T11:13:27.180Z",
    "status": "active",
    "staff": {
      "totalStaff": {
        "fullTime": 8,
        "partTime": 12
      },
      "manager": "Alex Johnson",
      "departments": [
        "gaming",
        "accessories",
        "repairs"
      ]
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
```

### Example 2: Pagination-style querying

Find stores where part-time employee count leaves remainder 0 when divided by 4 (useful for creating data subsets).

```javascript
db.stores.find({
  "staff.totalStaff.partTime": { $mod: [4, 0] }
})
```

This type of query is useful for creating consistent data partitions or implementing custom pagination logic based on field values.

```json
  {
    "_id": "new-store-001",
    "name": "TechWorld Electronics - Downtown Branch",
    "sales": {
      "totalSales": 5000
    },
    "createdDate": "2025-06-11T11:11:32.262Z",
    "status": "new",
    "staff": {
      "totalStaff": {
        "fullTime": 0,
        "partTime": 0
      }
    },
    "version": 1
  },
  {
    "_id": "gaming-store-mall-001",
    "name": "Gaming Paradise - Mall Location",
    "location": {
      "lat": 35.6762,
      "lon": 139.6503
    },
    "createdDate": "2025-06-11T11:13:27.180Z",
    "status": "active",
    "staff": {
      "totalStaff": {
        "fullTime": 8,
        "partTime": 12
      },
      "manager": "Alex Johnson",
      "departments": [
        "gaming",
        "accessories",
        "repairs"
      ]
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
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
