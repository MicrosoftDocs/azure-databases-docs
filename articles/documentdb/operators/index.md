---
title: Operators
description: Review the details for various supported operators you can use with Azure DocumentDB.
author: avijitgupta
ms.author: avijitgupta
ms.topic: language-reference
ms.date: 06/04/2025
ai-usage: ai-assisted
---

# Azure DocumentDB operators

This article contains details for various supported operators you can use with Azure DocumentDB.

## Aggregation

| | Description |
| --- | --- |
| **[`$facet`](aggregation/$facet.md)** | The `$facet` stage aggregation pipelines allow for multiple parallel aggregations to be executed within a single pipeline stage. |
| **[`$geonear`](aggregation/$geonear.md)** | The `$geoNear` aggregation stage calculates distances between a specified point and the location field in each document, sorts the documents by distance, and can optionally limit results by distance. |
| **[`$lookup`](aggregation/$lookup.md)** | The `$lookup` stage in the Aggregation Framework is used to perform left outer joins with other collections. |
| **[`$match`](aggregation/$match.md)** | The `$match` stage in the aggregation pipeline is used to filter documents that match a specified condition. |

## Array expression

| | Description |
| --- | --- |
| **[`$arrayToObject`](array-expression/$arraytoobject.md)** | The `$arrayToObject` operator is used to convert an array into a single document. |
| **[`$concatArrays`](array-expression/$concatarrays.md)** | The `$concatArrays` operator is used to combine multiple arrays into a single array. |
| **[`$filter`](array-expression/$filter.md)** | The `$filter` operator is used to filter elements from an array based on a specified condition. |
| **[`$indexOfArray`](array-expression/$indexOfArray.md)** | The `$indexOfArray` operator is used to search for an element in an array and return the index of the first occurrence of the element. |
| **[`$map`](array-expression/$map.md)** | The `$map` operator in MongoDB is used to apply an expression to each element in an array and return an array with the applied results. |
| **[`$reduce`](array-expression/$reduce.md)** | The `$reduce` operator is used to apply an expression to each element in an array and accumulate the results into a single value. |
| **[`$reverseArray`](array-expression/$reversearray.md)** | The `$reverseArray` operator is used to reverse the order of elements in an array. |
| **[`$slice`](array-expression/$slice.md)** | The `$slice` operator is used to return a subset of an array. |
| **[`$sortArray`](array-expression/$sortarray.md)** | The `$sortArray` operator is used to sort the elements of an array. |
| **[`$zip`](array-expression/$zip.md)** | The `$zip` operator is used to merge two or more arrays element-wise into a single array of arrays. |

## Array query

| | Description |
| --- | --- |
| **[`$all`](array-query/$all.md)** | The `$all` operator is used to select documents where the value of a field is an array that contains all the specified elements. |
| **[`$elemMatch`](array-query/$elemmatch.md)** | The `$elemMatch` operator is used to match documents that contain an array field with at least one element that matches all the specified query criteria. |
| **[`$size`](array-query/$size.md)** | The `$size` operator is used to query documents where an array field has a specified number of elements. |

## Array update

| | Description |
| --- | --- |
| **[`$each`](array-update/$each.md)** | The `$each` operator is used within an `$addToSet` or `$push` operation to add multiple elements to an array field in a single update operation. |
| **[`$positional`](array-update/$positional.md)** | The `$position` is used to specify the position in the array where a new element should be inserted. |
| **[`$pullAll`](array-update/$pullall.md)** | The `$pullAll` operator removes all instances of the specified values from an existing array. |
| **[`$push`](array-update/$push.md)** | The `$push` operator appends a specified value to an array. |
| **[`$slice`](array-expression/$slice.md)** | The `$slice` operator limits the number of array elements that are returned or modified. |

## Bitwise query

| | Description |
| --- | --- |
| **[`$bitsAllClear`](bitwise-query/$bitsallclear.md)** | The `$bitsAllClear` operator is used to match documents where all the bit positions specified in a bitmask are clear (that is, 0). |
| **[`$bitsAllSet`](bitwise-query/$bitsallset.md)** | The `$bitsAllSet` operator is used to match documents where all the bit positions specified in a bitmask are set (that is, 1). |
| **[`$bitsAnyClear`](bitwise-query/$bitsanyclear.md)** | The `$bitsAnyClear` operator is used to match documents where any bit positions specified in a bitmask are clear (that is, 0). |
| **[`$bitsAnySet`](bitwise-query/$bitsanyset.md)** | The `$bitsAnySet` operator is used to match documents where any bit positions specified in a bitmask are set (that is, 1). |

## Comparison query

| | Description |
| --- | --- |
| **[`$eq`](comparison-query/$eq.md)** | The `$eq` operator matches documents where the value of a field equals the specified value. |

## Date expression

| | Description |
| --- | --- |
| **[`$dateadd`](date-expression/$dateadd.md)** | The `$dateAdd` operator adds a specified number of time units to a date value. |
| **[`$datediff`](date-expression/$datediff.md)** | The `$dateDiff` operator returns the difference between two dates. |
| **[`$datefromparts`](date-expression/$datefromparts.md)** | The `$dateFromParts` operator constructs a date from the specified parts. |
| **[`$datefromstring`](date-expression/$datefromstring.md)** | The `$dateFromString` operator converts a date/time string to a date object. |

## Evaluation query

| | Description |
| --- | --- |
| **[`$expr`](evaluation-query/$expr.md)** | The `$expr` operator allows the use of aggregation expressions within the query language. |

## Geospatial

| | Description |
| --- | --- |
| **[`$geoIntersect`](geospatial/$geointersects.md)** | The `$geoIntersects` operator selects documents whose geospatial data intersects with a specified GeoJSON object. |

## Logical query

| | Description |
| --- | --- |
| **[`$and`](logical-query/$and.md)** | The `$and` operator joins query clauses with a logical AND and returns all documents that match the conditions of both clauses. |
| **[`$nor`](logical-query/$nor.md)** | The `$nor` operator performs a logical NOR operation on an array of one or more query expressions and selects the documents that fail all the query expressions in the array. |
| **[`$not`](logical-query/$not.md)** | The `$not` operator inverts the effect of a query expression and returns documents that don't match the query expression. |
| **[`$or`](logical-query/$or.md)** | The `$or` operator performs a logical OR operation on an array of two or more expressions and selects the documents that satisfy at least one of the expressions. |

## Object expression

| | Description |
| --- | --- |
| **[`$mergeObjects`](object-expression/$mergeobjects.md)** | The `$mergeObjects` operator combines multiple documents into a single document. |
| **[`$objectToArray`](object-expression/$objectToArray.md)** | The `$objectToArray` operator converts a document (object) into an array of key-value pairs. |
| **[`$setField`](object-expression/$setField.md)** | The `$setField` operator sets or updates the value of a field in a document. |

## Projection

| | Description |
| --- | --- |
| **[`$meta`](projection/$meta.md)** | The `$meta` projection operator returns metadata about the query, such as the text score. |

## Related content

- [MongoDB commands](../commands/index.md)
- [MongoDB compatibility](../compatibility-query-language.md)
