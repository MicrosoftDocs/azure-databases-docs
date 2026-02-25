---
title: Scalable Real-Time Product Search Using PostgreSQL with Citus
description: Learn how to build scalable real-time product search by using PostgreSQL with Citus so you can handle large catalogs.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
monikerRange: "citus-13 || citus-14"
---

# Scalable real-time product search by using PostgreSQL with Citus

(Copy of [original publication](https://www.citusdata.com/blog/2016/04/28/scalable-product-search/))

> [!NOTE]  
> This article mentions the Citus Cloud service. You can no longer onboard to Citus Cloud on Amazon Web Service (AWS). If you're new to Citus, Citus is still available to you. Citus is now open source and in the cloud on Microsoft Azure, as a fully integrated deployment option in Azure Database for PostgreSQL.
>
> For more information, see [Managed service](citus-cloud.md).

Product search is a common, yet sometimes challenging use-case for online retailers and marketplaces. It typically involves a combination of full-text search and filtering by attributes, which differ for every product category. More complex use-cases might have many sellers that offer the same product, but with a different price and different properties.

PostgreSQL has the functionality required to build a product search application, but performs poorly when indexing and querying large catalogs. With Citus, PostgreSQL can distribute tables and parallelize queries across servers, which lets you scale out memory and compute power to handle large catalogs. The search functionality isn't as comprehensive as in dedicated search solutions. However, a huge benefit of keeping the data in PostgreSQL is that it can be updated in real-time and tables can be joined. This article goes through the steps of setting up an experimental products database with a parallel search function by using PostgreSQL and Citus, with the goal of showcasing several powerful features.

Set up a [Multi-Node Citus](multi-node.md) by using 4 m3.2xlarge instances as workers. An easier way to get started is to use [Citus Cloud](https://www.citusdata.com/), which gives you a managed Citus cluster with full autofailover. The main table in [database schema](https://gist.github.com/marcocitus/fb49a20404f5fa8d4ff16c25ce04599c) is the "product" table. The product table contains the name and description of a product, its price, and attributes in [JSON format](http://www.postgresql.org/docs/current/static/datatype-json.html) such that different types of products can use different attributes:

```sql
CREATE TABLE product (
  product_id int primary key,
  name text not null,
  description text not null,
  price decimal(12,2),
  attributes jsonb
);
```

To distribute the table by using Citus, call the functions for `ddl` the table into 16 shards (one per physical core). The shards are distributed and replicated across the four workers.

```sql
SELECT create_distributed_table('product', 'product_id');
```

Create a GIN index to allow fast filtering of attributes by the JSONB containment operator. For example, a search query for English books might have the following expression: `attributes @> '{"category":"books", "language":"english"}'`, which can use the GIN index.

```sql
CREATE INDEX attributes_idx ON product USING GIN (attributes jsonb_path_ops);
```

To filter products by their name and description, use the [full text search functions](http://www.postgresql.org/docs/current/static/textsearch.html) in PostgreSQL to find a match with a user-specified query. A text search operation is performed on a text search vector (tsvector) by using a text search query (tsquery). It can be useful to define an intermediate function that generates the tsvector for a product. The `product_text_search` function combines the name and description of a product into a tsvector. In that tsvector, the name is assigned the highest weight (from 'A' to 'D'), such that matches with the name shows up higher when sorting by relevance.

```sql
CREATE FUNCTION product_text_search(name text, description text)
RETURNS tsvector LANGUAGE sql IMMUTABLE AS $function$
  SELECT setweight(to_tsvector(name),'A') ||
         setweight(to_tsvector(description),'B');
$function$;
```

After setting up the function, define a GIN index on it, which speeds up text searches on the product table.

```sql
CREATE INDEX text_idx ON product USING GIN (product_text_search(name, description));
```

No large product dataset is available, so instead generate 10 million mock products (7GB) by appending random words to generate names, descriptions, and attributes, by using a [simple generator function](https://gist.github.com/marcocitus/dd315960d5923ad3f4d26b105618ed58). After adding words to the words table, you can run:

``` psql
\COPY (SELECT * FROM generate_products(10000000)) TO '/data/base/products.tsv'
```

The new COPY feature in Citus can be used to load the data into the product table. COPY for hash-partitioned tables is currently available in the [latest version of Citus](https://github.com/citusdata/citus) and in [Citus Cloud](https://www.citusdata.com/). A benefit of the use of COPY on distributed tables is that workers can process multiple rows in parallel. Because each shard is indexed separately, the indexes are also kept small, which improves ingestion rate for GIN indexes.

``` psql
\COPY product FROM '/data/base/products.tsv'
```

The data load takes just under 7 minutes; roughly 25,000 rows/sec on average. Loading the data into a regular PostgreSQL table occurred in 45 minutes (3,700 rows/sec) by creating the index after copying in the data.

To search for products, assume you're searching for "copper oven." You can convert the phrase into a tsquery by using the `plainto_tsquery` function and match it to the name and description by using the `@@` operator. As another filter, require that the "food" attribute of the product is either "waste" or "air." To order the query by relevance, use the `ts_rank` function, which takes the tsvector and tsquery as input.

```sql
SELECT p.product_id, p.name, p.price
FROM product p
WHERE product_text_search(name, description) @@ plainto_tsquery('copper oven')
  AND (attributes @> '{"food":"waste"}' OR attributes @> '{"food":"air"}')
ORDER BY ts_rank(product_text_search(name, description),
                 plainto_tsquery('copper oven')) DESC
LIMIT 10;
```

```output
 product_id |         name         | price
------------+----------------------+-------
    2016884 | oven copper hot      | 32.33
    8264220 | rifle copper oven    | 92.11
    4021935 | argument chin rub    | 79.33
    5347636 | oven approval circle | 50.78
(4 rows)
Time: 68.832 ms (~78ms on non-distributed table)
```

The query uses both GIN indexes to do a fast look-up of a few rows. A broader search can take longer because of the need to sort all the results by their rank. For example, the following query has 294,000 results that it needs to sort to get the first 10:

```sql
SELECT p.product_id, p.name, p.price
FROM product p
WHERE product_text_search(name, description) @@ plainto_tsquery('oven')
  AND price < 50
ORDER BY ts_rank(product_text_search(name, description),
                 plainto_tsquery('oven')) DESC
LIMIT 10;
```

```output
 product_id |         name         | price
------------+----------------------+-------
    6295883 | end oven oven        | 7.80
    3304889 | oven punishment oven | 28.27
    2291463 | town oven oven       | 7.47
...
(10 rows)
Time: 2262.502 ms (37 seconds on non-distributed table)
```

This query gets the top 10 results from each of the 16 shards, which is where most time is spent, and the final 160 rows are sorted. When you use more machines and more shards, the number of rows that you need to be sorted in each shard is lowered. However, the amount of sorting work done is still small. This means that you can get lower query times by using a bigger cluster with more shards.

In addition to products, imagine the retailer also has a marketplace where other sellers can offer products at different prices. Those offers should also show up in searches if their price is under the maximum. A product can have many such offers. You can create another distributed table, which you can distribute by `product_id` and assign the same number of shards, such that you can perform joins on the colocated product/offer tables on `product_id`.

```sql
CREATE TABLE offer (
  product_id int not null,
  offer_id int not null,
  seller_id int,
  price decimal(12,2),
  new bool,
  primary key(product_id, offer_id)
);
SELECT create_distributed_table('offer', 'product_id');
```

You can load 5 million random offers generated by using the `generate_offers` function and COPY. The following query searches for popcorn oven products priced under \$70, including products with offers under \$70. Offers are included in the results as an array of JSON objects.

```sql
SELECT p.product_id, p.name, p.price, to_json(array_agg(to_json(o)))
FROM   product p LEFT JOIN offer o USING (product_id)
WHERE  product_text_search(p.name, p.description) @@ plainto_tsquery('popcorn oven')
  AND (p.price < 70 OR o.price < 70)
GROUP BY p.product_id, p.name, p.description, p.price
ORDER BY ts_rank(product_text_search(p.name, p.description),
                 plainto_tsquery('popcorn oven')) DESC
LIMIT 10;
```

```output
    .
     product_id |          name          | price |                                        to_json
    ------------+------------------------+-------+---------------------------------------------------------------------------------------
        9354998 | oven popcorn bridge    | 41.18 | [null]
        1172380 | gate oven popcorn      | 24.12 | [{"product_id":1172380,"offer_id":4853987,"seller_id":2088,"price":55.00,"new":true}]
         985098 | popcorn oven scent     | 73.32 | [{"product_id":985098,"offer_id":5890813,"seller_id":5727,"price":67.00,"new":true}]
    ...
    (10 rows)

    Time: 337.441 ms (4 seconds on non-distributed tables)
```

Given the wide array of features available in PostgreSQL, you can make further enhancements. For example, you can convert the entire row to JSON, or add a filter to only return reasonably close matches. You can make sure only lowest priced offers are included in the results. You can also start doing real-time inserts and updates in the product and offer tables.

## Related content

- [Guides overview](guides.md)
- [Sharding PostgreSQL with semi-structured data](semi-structured-data.md)
