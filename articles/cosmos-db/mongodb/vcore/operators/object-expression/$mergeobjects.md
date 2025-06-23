---
  title: $mergeObjects
  titleSuffix: Overview of the $mergeObjects expression in Azure Cosmos DB for MongoDB vCore
  description: The $mergeObjects operator merges multiple documents into a single document
  author: abinav2307
  ms.author: abramees
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 11/01/2024
---

# $mergeObjects as object expression operator

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$mergeObjects` operator combines multiple documents into a single document. The mergeObjects operation is used in aggregation pipelines to merge fields from different documents or add one or more fields to an existing document. The operator overwrites fields in the target document with fields from the source document when conflicts occur.

## Syntax

```mongodb
{ "$mergeObjects": [ <document1>, <document2>, ... ] }
```

## Parameters
| Parameter | Description |
| --- | --- |
| **`document1, document2`** | The documents to be merged. The documents can be specified as field paths, subdocuments, or constants. |

## Examples

Consider this sample document from the stores collection in the StoreData database.

```json
{
    "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4",
    "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
    "location": {
        "lat": -89.2384,
        "lon": -46.4012
    },
    "staff": {
        "totalStaff": {
            "fullTime": 8,
            "partTime": 20
        }
    },
    "sales": {
        "totalSales": 75670,
        "salesByCategory": [
            {
                "categoryName": "Wine Accessories",
                "totalSales": 34440
            },
            {
                "categoryName": "Bitters",
                "totalSales": 39496
            },
            {
                "categoryName": "Rum",
                "totalSales": 1734
            }
        ]
    },
    "promotionEvents": [
        {
            "eventName": "Unbeatable Bargain Bash",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 6,
                    "Day": 23
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 7,
                    "Day": 2
                }
            },
            "discounts": [
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 7
                },
                {
                    "categoryName": "Bitters",
                    "discountPercentage": 15
                },
                {
                    "categoryName": "Brandy",
                    "discountPercentage": 8
                },
                {
                    "categoryName": "Sports Drinks",
                    "discountPercentage": 22
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 19
                }
            ]
        },
        {
            "eventName": "Steal of a Deal Days",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 21
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 29
                }
            },
            "discounts": [
                {
                    "categoryName": "Organic Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "White Wine",
                    "discountPercentage": 20
                },
                {
                    "categoryName": "Sparkling Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 17
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 23
                }
            ]
        }
    ]
}
```

### Example 1 - Merging documents as an accumulator to group documents by the sales subdocument

```mongodb
db.stores.aggregate([{"$match": {"company": "Fourth Coffee"}}, {"$group": {"_id": "$city", "mergedSales": {"$mergeObjects": "$sales"}}}])
```

The top two documents returned by this query are:

```json
[{
    "_id": "Jalonborough",
    "mergedSales": {
        "totalSales": 45747,
        "salesByCategory": [
            {
                "categoryName": "Bucket Bags",
                "totalSales": 45747
            }
        ]
    }
},
{
    "_id": "Port Vladimir",
    "mergedSales": {
        "totalSales": 32000,
        "salesByCategory": [
            {
                "categoryName": "DJ Speakers",
                "totalSales": 24989
            },
            {
                "categoryName": "DJ Cables",
                "totalSales": 7011
            }
        ]
    }
}]
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
