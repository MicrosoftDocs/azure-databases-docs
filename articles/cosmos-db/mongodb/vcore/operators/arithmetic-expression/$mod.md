---
title: $mod (as Query Operator)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $mod query operator in Azure Cosmos DB for MongoDB vCore is used to filter documents based on a modulus operation.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/27/2024
---

# $mod (as query operator)

The `$mod` query operator is used to filter documents based on the remainder of a division operation. This operator allows for queries that involve mathematical conditions, such as finding values divisible by a number or having a specific remainder. It's supported in Azure Cosmos DB for MongoDB (vCore).

## Syntax

```javascript
{ 
  <field>: { $mod: [ <divisor>, <remainder> ] } 
}
```

- **`<field>`**: The field on which to perform the modulus operation.
- **`<divisor>`**: The number by which to divide the field's value.
- **`<remainder>`**: The expected remainder after the division.

## Example

### Example 1: Find documents where the `sales` value is divisible by 3

```json
db.collection.find({ "sales": { "$mod": [3, 0] } })
```

This example retrieves all documents where the `sales` field value is divisible by 3 (that is, the remainder is 0). It will produce the following output:
```json
[
  { "_id": 1, "sales": 9, "product": "A" },
  { "_id": 2, "sales": 15, "product": "B" },
  { "_id": 3, "sales": 21, "product": "C" }
]
```

### Example 2: Find documents where the `totalSales` value has a remainder of 2 when divided by 5

```json
db.collection.find({ "totalSales": { "$mod": [5, 2] } })
```

This query filters documents where the `totalSales` field has a remainder of 2 when divided by 5. It will produce the following output:
```json
[
  { "_id": 4, "totalSales": 7, "product": "X" },
  { "_id": 5, "totalSales": 12, "product": "Y" },
  { "_id": 6, "totalSales": 17, "product": "Z" }
]
```

### Example 3: Query nested fields using $mod

```json
db.collection.find({ "sales.monthly.total": { "$mod": [4, 1] } })
```

This example demonstrates querying a nested field (`sales.monthly.total`) with the `$mod` operator. It will produce the following output:
```json
[
  { "_id": 7, "sales": { "monthly": { "total": 5 } }, "category": "Electronics" },
  { "_id": 8, "sales": { "monthly": { "total": 9 } }, "category": "Clothing" }
]
```

## Considerations

- If fewer than two values are specified in the array for the $mod operator, an error is thrown by the server indicating not enough arguments were passed. 
- If more than two values are specified in the array for the $mod operator, an error is thrown by the server indicating too many arguments were passed.

## Limitations

- The `$mod` operator is applied to numerical fields only. Using it on non-numerical fields result in an error.
- Ensure that the divisor isn't zero, as it leads to an invalid operation.

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]