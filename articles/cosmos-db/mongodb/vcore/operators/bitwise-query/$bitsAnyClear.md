---
  title: $bitsAnyClear bitwise query object expression in Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The bitsAnyClear command is used to match documents where any of the bit positions specified in a bitmask are clear.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 11/01/2024
---

# $bitsAnyClear as bitwise query operator

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

This command is used to match documents where any of the bit positions specified in a bitmask are clear (that is, 0). It's useful for querying documents with binary data or flags stored as integers. This operator enables efficient querying based on specific bit patterns.

## Syntax

```mongodb
{
  <field>: { $bitsAnyClear: <bitmask> }
}
```

- `<field>`: The field in the document to be queried.
- `<bitmask>`: A bitmask where each bit position represents a position to check if it's clear (0).

## Example

Consider a collection named `stores` with documents similar to the provided JSON structure. To find stores where the `totalStaff.fullTime` field has any of the first 3 bits clear, you can use the following query:

```mongodb
db.stores.find({
  "store.staff.totalStaff.fullTime": { $bitsAnyClear: 0b00000111 }
})
```

In this example, `0b00000111` is the bitmask representing the first 3 bits. The query would return documents where any of the first 3 bits of the `totalStaff.fullTime` field are clear.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
