---
  title: $setField object expression usage in Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The setField command is used to add, update, or remove fields in embedded documents.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 1/01/2024
---

# $setField as object expression operator

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$setField` operator is used to add, update, or remove fields in embedded documents. This operator allows for precise manipulation of document fields. This makes it useful for tasks such as updating nested fields, restructuring documents, or even removing fields entirely.

## Syntax

The syntax for the `$setField` operator is as follows:

```json
{
  $setField: {
    field: <fieldName>,
    input: <expression>,
    value: <expression>
  }
}
```

- `field`: The name of the field to add, update, or remove.
- `input`: The document or field being processed.
- `value`: The new value to assign to the field. If `value` is `null`, the field is removed.

## Examples

### Example 1: Updating a nested field

Suppose you want to update the `discountPercentage` for the "Laptops" category in the "Summer Sale" promotion event.

```json
db.collection.updateOne(
  { "store.storeId": "12345" },
  [{
    $set: {
      "store.promotionEvents": {
        $map: {
          input: "$store.promotionEvents",
          as: "event",
          in: {
            $setField: {
              field: "discounts",
              input: "$$event",
              value: {
                $map: {
                  input: "$$event.discounts",
                  as: "discount",
                  in: {
                    $cond: {
                      if: { $eq: ["$$discount.categoryName", "Laptops"] },
                      then: { 
                        categoryName: "$$discount.categoryName", 
                        discountPercentage: 18 
                      },
                      else: "$$discount"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }]
)
```

### Example 2: Removing a field

Suppose you want to remove the `totalStaff` field from the `staff` object.

```json
db.collection.updateOne(
  { "store.storeId": "12345" },
  [{
    $set: {
      "store.staff": {
        $setField: {
          field: "totalStaff",
          input: "$store.staff",
          value: null
        }
      }
    }
  }]
)
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
