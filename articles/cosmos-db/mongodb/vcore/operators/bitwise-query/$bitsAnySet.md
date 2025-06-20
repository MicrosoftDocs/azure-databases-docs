---
  title: $bitsAnySet bitwise query object expression in Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The bitsAnySet command is used to select documents where any of the bit positions specified are set to `1`.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 11/01/2024
---

# $bitsAnySet as bitwise query operator

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

This command is used to select documents where any of the bit positions specified are set to `1`. It's useful for querying documents with fields that store bitmask values. This operator can be handy when working with fields that represent multiple boolean flags in a single integer.

## Syntax

```javascript
{
  <field>: { $bitsAnySet: [ <bit positions> ] }
}
```

- **`<field>`**: The field to be queried.
- **`<bit positions>`**: An array of bit positions to check if any are set to `1`.

## Examples

### Example 1: Querying for Documents with Specific Bit Positions Set

Suppose we have a collection named `stores` and we want to find all stores where any of the bit positions 1 or 3 in the `storeId` field are set to `1`.

```javascript
db.stores.find({
  "store.storeId": { $bitsAnySet: [1, 3] }
})
```

### Example 2: Querying for Documents with Bit Positions in Nested Fields

Suppose we want to find all promotion events where any of the bit positions 0 or 2 in the `discountPercentage` for the "Laptops" category are set to `1`.

```javascript
db.stores.find({
  "store.promotionEvents.discounts": {
    $elemMatch: {
      "categoryName": "Laptops",
      "discountPercentage": { $bitsAnySet: [0, 2] }
    }
  }
})
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
