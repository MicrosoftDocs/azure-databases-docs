---
  title: $sortArray
  titleSuffix: Overview of the $sortArray operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $sortArray operator helps in sorting the elements in an array.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 07/28/2025
---

# $sortArray

The `$sortArray` operator is used to sort the elements of an array. The operator can be useful when you need to sort arrays within your documents based on specific fields or criteria. It can be applied to arrays of embedded documents or simple arrays of values.

## Syntax

```javascript
{
  $sortArray: {
    input: <arrayExpression>,
    sortBy: <sortSpecification>
  }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`input`** | The array to be sorted. |
| **`sortBy`** | Specifies the sort order. It can be a single field or multiple fields with their corresponding sort order (1 for ascending, -1 for descending). |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "d3c9df51-41bd-4b4e-a26b-b038d9cf8b45",
  "location": {
    "lat": -67.7571,
    "lon": 97.2505
  },
  "sales": {
    "totalSales": 149849,
    "salesByCategory": [
      {
        "categoryName": "DJ Speakers",
        "totalSales": 36972
      },
      {
        "categoryName": "DJ Headphones",
        "totalSales": 12877
      },
      {
        "categoryName": "Music Accessories",
        "totalSales": 40000
      },
      {
        "categoryName": "DJ Accessories",
        "totalSales": 60000
      }
    ]
  },
  "tag": [
    "#ShopLocal",
    "#FashionStore",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}
```

### Example 1: Sorting an Array of Embedded Documents

The example query sorts the `sales.salesByCategory` array within each document in descending order based on `totalSales`.

```javascript
db.stores.aggregate([
  {$match: {"_id": "d3c9df51-41bd-4b4e-a26b-b038d9cf8b45"} }
, {
    $project: {
      sortedSalesByCategory: {
        $sortArray: {
          input: "$sales.salesByCategory",
          sortBy: { totalSales: -1 }
        }
      }
    }
  }
])
```

The query returns array elements sorted by `totalSales` for the sample json.

```json
{
  "_id": "d3c9df51-41bd-4b4e-a26b-b038d9cf8b45",
  "sortedSalesByCategory": [
    { "categoryName": "DJ Accessories", "totalSales": 60000 },
    { "categoryName": "Music Accessories", "totalSales": 40000 },
    { "categoryName": "DJ Speakers", "totalSales": 36972 },
    { "categoryName": "DJ Headphones", "totalSales": 12877 }
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)].
