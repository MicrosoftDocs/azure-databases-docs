---
  title: $regex (evaluation query)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $regex operator provides regular expression capabilities for pattern matching in queries, allowing flexible string matching and searching.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/16/2025
---

# $regex (evaluation query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$regex` operator provides regular expression capabilities for pattern matching in queries. It allows you to search for documents where a field matches a specified regular expression pattern. This operator is useful for flexible string searching, pattern validation, and complex text filtering operations.

## Syntax

The syntax for the `$regex` operator is as follows:

```javascript
{
  <field>: { $regex: <pattern>, $options: <options> }
}
```

Or the shorter form:

```javascript
{
  <field>: { $regex: /<pattern>/<options> }
}
```

## Parameters

| | Description |
| --- | --- |
| **`<field>`** | The field to search in. Must contain string values. |
| **`<pattern>`** | The regular expression pattern to match against. |
| **`<options>`** | Optional. Regular expression options such as case-insensitive matching. Common options include 'i' (case insensitive), 'm' (multiline), 's' (dot all), and 'x' (extended). |

## Example

### Example 1: Find stores by name pattern

The example finds all the stores containing "Consultants" in their name (case-insensitive).

```javascript
db.stores.find(
    { "name": { $regex: "Consultants", $options: "i" } },
    { "_id": 1, "name": 1, "storeOpeningDate": 1 }
).limit(3)
```

The query returns matches with store names containing "Consultants" regardless of case, helping identify stores belonging to consulting companies.

```json
  {
    "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
    "name": "First Up Consultants | Bed and Bath Pantry - Port Antone",
    "storeOpeningDate": "2024-09-19T17:31:59.665Z"
  },
  {
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
    "storeOpeningDate": "2024-09-10T13:43:51.209Z"
  },
  {
    "_id": "62438f5f-0c56-4a21-8c6c-6bfa479494ad",
    "name": "First Up Consultants | Plumbing Supply Shoppe - New Ubaldofort",
    "storeOpeningDate": "2024-09-19T08:27:44.268Z"
  }
```

### Example 2: Advanced pattern matching for category names

The example finds stores selling products with category name that starts with a vowel.

```javascript
db.stores.find(
  {
    "sales.salesByCategory.categoryName": { $regex: "^[AEIOUaeiou]", $options: "" }
  },
  { "_id": 1, "name": 1, "sales.salesByCategory.categoryName": 1}
).limit(2)
```

The query uses the caret (^) anchor and character class to match category names beginning with vowels.

```json
  {
    "_id": "e6410bb3-843d-4fa6-8c70-7472925f6d0a",
    "name": "Relecloud | Toy Collection - North Jaylan",
    "sales": { 
      "salesByCategory": [ 
        { "categoryName": "Educational Toys" } 
      ] 
    }
  },
  {
    "_id": "4e064f0a-7e30-4701-9a80-eff3caf46ce8",
    "name": "Fourth Coffee | Outdoor Furniture Deals - Lucianohaven",
    "sales": {
      "salesByCategory": [
        { "categoryName": "Outdoor Swings" },
        { "categoryName": "Hammocks" }
      ]
    }
  }
```

### Example 3: Find stores with specific naming conventions

The example finds stores with names containing a pipe character (|) separator.

```javascript
db.stores.find(
{ "name": { $regex: "\\|" }},
{ "_id": 1, "name": 1, "sales.salesByCategory.categoryName": 1}).limit(2)
```

The query searches for stores with names containing the pipe character, which appears to be a naming convention in the dataset.

```json
  {
    "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
    "name": "Trey Research | Home Office Depot - Lake Freeda",
    "sales": { 
      "salesByCategory": [ 
        { "categoryName": "Desk Lamps" } 
      ] 
    }
  },
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "sales": { 
      "salesByCategory": [ 
        { "categoryName": "Stockings" } 
      ] 
    }
  }
```

### Example 4: Complex pattern for discount categories

The example finds stores with categories containing both "Bath" and ending with "s".

```javascript
db.stores.aggregate([
  { $match: { "promotionEvents.discounts.categoryName": { $regex: "Bath.*s$", $options: "i" } } },
  { $project: { "_id": 1, "name": 1, "promotionEvents.discounts.categoryName":1 }},
  { $match: {"promotionEvents.discounts.categoryName": { $ne: [] }} },
  { $limit: 2 }])
```

The query combines multiple regex features: literal text matching, the dot-star quantifier (.*), and the end-of-string anchor ($).

```json
{
    "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
    "name": "First Up Consultants | Bed and Bath Pantry - Port Antone",
    "promotionEvents": [
      {
        "discounts": [
          { "categoryName": "Bath Sheets", "discountPercentage": 16 },
          { "categoryName": "Bath Accessories", "discountPercentage": 11 }
        ]
      },
      {
        "discounts": [ 
          { "categoryName": "Bath Mats", "discountPercentage": 22 } 
        ]
      },
      {
        "discounts": [
          { "categoryName": "Bath Towels", "discountPercentage": 21 },
          { "categoryName": "Bathrobes", "discountPercentage": 19 },
          { "categoryName": "Bath Accessories", "discountPercentage": 5 }
        ]
      },
      {
        "discounts": [
          { "categoryName": "Bath Sheets", "discountPercentage": 25 },
          { "categoryName": "Bath Towels", "discountPercentage": 15 }
        ]
      }
    ]
  },
  {
    "_id": "27ef6004-70fa-4217-8395-0eabc4cc9841",
    "name": "Fabrikam, Inc. | Bed and Bath Store - O'Connerborough",
    "promotionEvents": [
      {
        "discounts": [
          { "categoryName": "Bath Accessories", "discountPercentage": 24 }
        ]
      },
      {
        "discounts": [
          { "categoryName": "Bathrobes", "discountPercentage": 18 },
          { "categoryName": "Bath Towels", "discountPercentage": 14 },
          { "categoryName": "Bath Accessories", "discountPercentage": 20 }
        ]
      }
    ]
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
