title: $mod (as Query Operator)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $mod query operator in Azure Cosmos DB for MongoDB vCore is used to filter documents based on a modulus operation.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/27/2024

# $mod (as Query Operator)

The `$mod` query operator is used in MongoDB to filter documents based on the remainder of a division operation. This operator allows for queries that involve mathematical conditions, such as finding values divisible by a number or having a specific remainder. It is supported in Azure Cosmos DB for MongoDB vCore.

## Syntax

```json
{ 
  <field>: { $mod: [ <divisor>, <remainder> ] } 
}
```

- **`<field>`**: The field on which to perform the modulus operation.
- **`<divisor>`**: The number by which to divide the field's value.
- **`<remainder>`**: The expected remainder after the division.

## Example(s)

### Example 1: Find documents where the `sales` value is divisible by 3

```json
db.collection.find({ "sales": { $mod: [3, 0] } })
```

This example retrieves all documents where the `sales` field value is divisible by 3 (i.e., the remainder is 0).

### Example 2: Find documents where the `totalSales` value has a remainder of 2 when divided by 5

```json
db.collection.find({ "totalSales": { $mod: [5, 2] } })
```

This query filters documents where the `totalSales` field has a remainder of 2 when divided by 5.

### Example 3: Query nested fields using $mod

```json
db.collection.find({ "sales.monthly.total": { $mod: [4, 1] } })
```

This example demonstrates querying a nested field (`sales.monthly.total`) with the `$mod` operator.

## Limitations

- The `$mod` operator is applied to numerical fields only. Using it on non-numerical fields will result in an error.
- Ensure that the divisor is not zero, as this will lead to an invalid operation.

## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](migration-options.md).
- Get started by [creating an account](../quickstart-portal.md).