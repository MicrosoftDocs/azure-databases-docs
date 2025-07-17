---
  title: $type (element query)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $type operator selects documents if a field is of the specified type.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 06/17/2025
---

# $type (element query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$type` operator selects documents if a field is of the specified type. This is useful for data validation and ensuring consistency across documents in a collection. The `$type` operator accepts both BSON type numbers and string aliases.

## Syntax

The syntax for the `$type` operator is as follows:

```javascript
{
  <field>: { $type: <BSON type number> | <string alias> }
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The field to check the type of. |
| **`BSON type number`** | A number corresponding to the BSON type (e.g., 1 for double, 2 for string). |
| **`string alias`** | A string alias for the BSON type (e.g., "double", "string", "object", "array"). |

## Common BSON Types

| Type | Number | Alias | Description |
| --- | --- | --- | --- |
| Double | 1 | "double" | 64-bit floating point |
| String | 2 | "string" | UTF-8 string |
| Object | 3 | "object" | Embedded document |
| Array | 4 | "array" | Array |
| ObjectId | 7 | "objectId" | ObjectId |
| Boolean | 8 | "bool" | Boolean |
| Date | 9 | "date" | Date |
| Null | 10 | "null" | Null value |
| 32-bit integer | 16 | "int" | 32-bit integer |
| Timestamp | 17 | "timestamp" | Timestamp |
| 64-bit integer | 18 | "long" | 64-bit integer |

## Example

Let's understand the usage with sample JSON from the `stores` dataset.

```json
{
  "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
  "name": "Trey Research | Home Office Depot - Lake Freeda",
  "location": { "lat": -48.9752, "lon": -141.6816 },
  "staff": { "employeeCount": { "fullTime": 12, "partTime": 19 } },
  "sales": {
    "salesByCategory": [ { "categoryName": "Desk Lamps", "totalSales": 37978 } ],
    "revenue": 37978
  },
  "promotionEvents": [
    {
      "eventName": "Crazy Deal Days",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 9, "Day": 27 },
        "endDate": { "Year": 2023, "Month": 10, "Day": 4 }
      },
      "discounts": [
        { "categoryName": "Desks", "discountPercentage": 22 },
        { "categoryName": "Filing Cabinets", "discountPercentage": 23 }
      ]
    }
  ],
  "company": "Trey Research",
  "city": "Lake Freeda",
  "storeOpeningDate": "2024-09-26T22:55:25.779Z",
  "lastUpdated": "Timestamp({ t: 1729983325, i: 1 })"
}
```

### Example 1: Find stores with string-type names

The example finds all stores where the `name` field is of string type.

```javascript
db.stores.find(
 { "name": { $type: "string" }},
 { "_id": 1, "name": 1 }).limit(1)
```

The query returns all documents where the `name` field contains a string value.

```json
{
  "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
  "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort"
}
```

### Example 2: Data validation using multiple type checks

This example demonstrates validating that essential fields have the correct data types.

```javascript
db.stores.find({
  "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
  "name": { $type: "string" },
  "location": { $type: "object" },
  "staff.employeeCount.fullTime": { $type: ["int", "long"] },
  "promotionEvents": { $type: "array" }},
  { "_id": 1, "name": 1,"location":1, "staff": 1 }
)
```

The query returns stores where all specified fields have the expected data types, helping ensure data consistency.

```json
{
  "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
  "name": "Trey Research | Home Office Depot - Lake Freeda",
  "location": { "lat": -48.9752, "lon": -141.6816 },
  "staff": { "employeeCount": { "fullTime": 12 } }
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
