---
  title: $top
  titleSuffix: Overview of the $top operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $top operator returns the first document from the result set sorted by one or more fields
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 02/12/2025
---

# $top

The `$top` operator sorts documents on one more fields specified by the query and returns the first document matching the filtering criteria. It combines sorting and selection in a single operation, making it efficient for finding the highest or lowest values without requiring a separate sort stage.

## Syntax

```javascript
{
    $top: {
      output: [listOfFields],
      sortBy: {
          < fieldName >: < sortOrder >
      }
  }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`listOfFields`** | The list of fields to be returned for the last document in the result set|
| **`fieldName`** | The field to use for sorting the result set|
| **`sortOrder`** | 1 or -1. 1 implies sorting in ascending order of the value of the field while -1 implies sorting in descending order of the values of the field|

## Example

Consider this sample document from the stores collection.

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

### Example 1: Get the top selling category per store

To find the highest-selling category within the Boulder Innovations company, run a query to retrieve stores within the company, sort the documents in descending order of total sales within each category and return the top document in the sorted result set.

```javascript
db.stores.aggregate([{
    "$match": {
        "company": {
            "$in": ["Boulder Innovations"]
        }
    }
}, {
    "$group": {
        "_id": "$company",
        "topSales": {
            "$top": {
                "output": ["$company", "$sales"],
                "sortBy": {
                    "sales.totalSales": -1
                }
            }
        }
    }
}])
```

This query returns the following result:

```json
{
    "_id": "Boulder Innovations",
    "topSales": [
        "Boulder Innovations",
        {
            "salesByCategory": [
                {
                    "categoryName": "iPads",
                    "totalSales": 46592
                },
                {
                    "categoryName": "External Hard Drives",
                    "totalSales": 11364
                },
                {
                    "categoryName": "Student Laptops",
                    "totalSales": 30481
                },
                {
                    "categoryName": "Android Tablets",
                    "totalSales": 48149
                },
                {
                    "categoryName": "Desktops",
                    "totalSales": 42726
                },
                {
                    "categoryName": "Inkjet Cartridges",
                    "totalSales": 36581
                },
                {
                    "categoryName": "2-in-1 Laptops",
                    "totalSales": 26355
                },
                {
                    "categoryName": "Phone Mounts",
                    "totalSales": 19886
                },
                {
                    "categoryName": "Android Phones",
                    "totalSales": 4532
                },
                {
                    "categoryName": "Power Banks",
                    "totalSales": 48347
                },
                {
                    "categoryName": "All-in-One Printers",
                    "totalSales": 44346
                },
                {
                    "categoryName": "Photo Printers",
                    "totalSales": 44747
                }
            ],
            "revenue": 404106
        }
    ]
}
```

### Example 2: Get the highest discount by promotion category

To fetch the highest discount per sales category, first run a query to group all documents by store, then sort the documents in descending order of discount percentages within each promotion event and return the top document from the sorted result set per store.

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $unwind: "$promotionEvents.discounts"
    },
    {
        $group: {
            _id: "$_id",
            storeName: {
                $first: "$name"
            },
            highestDiscount: {
                $top: {
                    sortBy: {
                        "promotionEvents.discounts.discountPercentage": -1
                    },
                    output: {
                        categoryName: "$promotionEvents.discounts.categoryName",
                        discountPercentage: "$promotionEvents.discounts.discountPercentage",
                        eventName: "$promotionEvents.eventName"
                    }
                }
            }
        }
    }
])
```

The first two results returned by this query are:

```json
[
    {
        "_id": "64ec6589-068a-44a6-be5b-9d37bb0a90f1",
        "storeName": "First Up Consultants | Computer Gallery - West Cathrine",
        "highestDiscount": {
            "categoryName": "Gaming Accessories",
            "discountPercentage": 24,
            "eventName": "Crazy Markdown Madness"
        }
    },
    {
        "_id": "a58d0356-493b-44e6-afab-260aa3296930",
        "storeName": "Fabrikam, Inc. | Outdoor Furniture Nook - West Lexie",
        "highestDiscount": {
            "categoryName": "Fire Pits",
            "discountPercentage": 22,
            "eventName": "Savings Showdown"
        }
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
