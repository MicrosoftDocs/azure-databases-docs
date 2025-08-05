---
  title: $setField
  titleSuffix: Overview of the $setField expression in Azure Cosmos DB for MongoDB (vCore)
  description: The setField command is used to add, update, or remove fields in embedded documents.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 08/03/2025
---

# $setField

The `$setField` operator is used to add, update, or remove fields in embedded documents. The operator allows for precise manipulation of document fields, which makes it useful for tasks such as updating nested fields, restructuring documents, or even removing fields entirely.

## Syntax

```javascript
{
  $setField: {
    field: <fieldName>,
    input: <expression>,
    value: <expression>
  }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`<field>`** | The document (object) to be transformed into an array of key-value pairs. |
| **`<input>`** | The document or field being processed. |
| **`<value>`** | The new value to assign to the field. If `value` is `null`, the field is removed.|

## Examples

### Example 1: Updating a nested field

This query performs a conditional update on nested discount values inside promotion events for the document matching a specific `_id`.

```javascript
db.stores.updateOne(
  { "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4" },
  [
    {
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
    }
  ]
)
```

### Example 2: Removing a field

Suppose you want to remove the `totalStaff` field from the `staff` object.

```javascript
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
