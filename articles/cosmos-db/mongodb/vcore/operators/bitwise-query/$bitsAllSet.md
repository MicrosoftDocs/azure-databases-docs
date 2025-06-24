---
  title: $bitsAllSet bitwise query object expression in Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The bitsAllSet command is used to match documents where all the specified bit positions are set.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 11/02/2024
---

# $bitsAllSet as bitwise query operator

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$bitsAllSet` operator is used to match documents where all the specified bit positions are set (that is, are 1). This operator is useful for performing bitwise operations on fields that store integer values. It can be used in scenarios where you need to filter documents based on specific bits being set within an integer field.

## Syntax

```json
{
  <field>: { $bitsAllSet: <bitmask> }
}
```

- `<field>`: The field in the document on which the bitwise operation is to be performed.
- `<bitmask>`: A bitmask indicating which bits must be set in the field's value.

## Example

Consider a collection named `stores` that contains documents with various fields. To find documents where the `storeId` field has specific bits set, you can use the `$bitsAllSet` operator.

### Example 1: Find stores with specific bits set in `storeId`

```javascript
db.stores.find({
  "store.storeId": { $bitsAllSet: 0b00000011 }
})
```

This query would return documents where the `storeId` field has both the first and second bits set.

### Example 2: Find stores with specific bits set in `totalStaff.fullTime`

```javascript
db.stores.find({
  "store.staff.totalStaff.fullTime": { $bitsAllSet: 0b00001111 }
})
```

This query would return documents where the `fullTime` field in `totalStaff` has the first 4 bits set.


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
