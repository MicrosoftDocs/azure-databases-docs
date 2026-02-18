---
title: How Distributed Outer Joins on PostgreSQL with Citus Work
description: Learn how to use distributed outer joins on PostgreSQL with Citus so you can efficiently query related data.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
monikerRange: "citus-13 || citus-14"
---

# How distributed outer joins on PostgreSQL with Citus work

(Copy of [original publication](https://www.citusdata.com/blog/2016/10/10/outer-joins-in-citus/))

SQL is a powerful language for analyzing and reporting against data. A core part of SQL is the idea of joins and how you combine various tables together. "Outer joins" are useful when you need to retain rows, even if they have no match on the other side.

The most common type of join, inner join, against tables A and B would bring only the tuples that have a match for both A and B. However, outer joins provide the ability to bring together all of table A even if they don't have a corresponding match in table B. For example, you keep customers in one table and purchases in another table. When you want to see all purchases of customers, you might want to see all customers in the result even if they didn't do any purchases yet. Then, you need an outer join. This article shows what outer joins are, and how they're supported in a distributed fashion on Citus.

For example, you have two tables, customer and purchase:

```sql
customer table:
 customer_id |      name
-------------+-----------------
           1 | Corra Ignacio
           3 | Warren Brooklyn
           2 | Jalda Francis

purchase table:
 purchase_id | customer_id | category |           comment
-------------+-------------+----------+------------------------------
        1000 |           1 | books    | Nice to Have!
        1001 |           1 | chairs   | Comfortable
        1002 |           2 | books    | Good Read, cheap price
        1003 |          -1 | hardware | Not very cheap
        1004 |          -1 | laptops  | Good laptop but expensive...
```

The following queries and results help clarify the inner and outer join behaviors:

```sql
SELECT customer.name, purchase.comment
FROM customer JOIN purchase ON customer.customer_id = purchase.customer_id
ORDER BY purchase.comment;

     name      |        comment
---------------+------------------------
 Corra Ignacio | Comfortable
 Jalda Francis | Good Read, cheap price
 Corra Ignacio | Nice to Have!
```

:::image type="content" source="./media/outer-joins/articles-join-inner.png" alt-text="Diagram showing the intersection of two circles representing an inner join that returns only matching records.":::

```sql
SELECT customer.name, purchase.comment
FROM customer INNER JOIN purchase ON customer.customer_id = purchase.customer_id
ORDER BY purchase.comment;

     name      |        comment
---------------+------------------------
 Corra Ignacio | Comfortable
 Jalda Francis | Good Read, cheap price
 Corra Ignacio | Nice to Have!
```

:::image type="content" source="./media/outer-joins/articles-join-left.png" alt-text="Diagram illustrating a left join showing all records from the left table and matching records from the right table.":::

```sql
SELECT customer.name, purchase.comment
FROM customer LEFT JOIN purchase ON customer.customer_id = purchase.customer_id
ORDER BY purchase.comment;

      name       |        comment
-----------------+------------------------
 Corra Ignacio   | Comfortable
 Jalda Francis   | Good Read, cheap price
 Corra Ignacio   | Nice to Have!
 Warren Brooklyn |
```

:::image type="content" source="./media/outer-joins/articles-join-right.png" alt-text="Diagram illustrating a right join showing all records from the right table and matching records from the left table.":::

```sql
SELECT customer.name, purchase.comment
FROM customer RIGHT JOIN purchase ON customer.customer_id = purchase.customer_id
ORDER BY purchase.comment;

     name      |           comment
---------------+------------------------------
 Corra Ignacio | Comfortable
 Jalda Francis | Good Read, cheap price
               | Good laptop but expensive...
 Corra Ignacio | Nice to Have!
               | Not very cheap
```

:::image type="content" source="./media/outer-joins/articles-join-full.png" alt-text="Diagram illustrating a full outer join showing all records from both tables including unmatched rows.":::

```sql
SELECT customer.name, purchase.comment
FROM customer FULL JOIN purchase ON customer.customer_id = purchase.customer_id
ORDER BY purchase.comment;

      name       |           comment
-----------------+------------------------------
 Corra Ignacio   | Comfortable
 Jalda Francis   | Good Read, cheap price
                 | Good laptop but expensive...
 Corra Ignacio   | Nice to Have!
                 | Not very cheap
 Warren Brooklyn |
```

## Distributed Outer Joins with Citus

The Citus extension allows PostgreSQL to distribute large tables into smaller fragments called "shards". Performing outer joins on these distributed tables becomes a bit more challenging, since the union of outer joins between individual shards doesn't always give the correct result. Currently, Citus support distributed outer joins under some criteria:

- Outer joins should be between distributed (sharded) tables only. You can't outer join a sharded table with a regular PostgreSQL table.
- Join criteria should be on [partition columns](https://docs.citusdata.com/en/v5.2/dist_tables/concepts.html) of the distributed tables.
- The query should join the distributed tables on the equality of partition columns (table1.a = table2.a)
- Shards of the distributed table should match one to one, that is, each shard of table A should overlap with one and only one shard from table B.

For example, assume you have three hash distributed tables X, Y and Z and let X and Y have four shards while Z has eight shards.

```sql
CREATE TABLE user (user_id int, name text);
SELECT create_distributed_table('user', 'user_id');

CREATE TABLE purchase (user_id int, amount int);
SELECT create_distributed_table('purchase', 'user_id');

CREATE TABLE comment (user_id int, comment text, rating int);
SELECT create_distributed_table('comment', 'user_id');
```

The following query works since distributed tables user and purchase have the same number of shards and the join criteria is equality of partition columns:

```sql
SELECT * FROM user OUTER JOIN purchase ON user.user_id = purchase.user_id;
```

The following queries aren't supported out of the box:

```sql
-- user and comment tables doesn't have the same number of shards:
SELECT * FROM user OUTER JOIN comment ON user.user_id = comment.user_id;

-- join condition is not on the partition columns:
SELECT * FROM user OUTER JOIN purchase ON user.user_id = purchase.amount;

-- join condition is not equality:
SELECT * FROM user OUTER JOIN purchase ON user.user_id < purchase.user_id;
```

## How Citus processes OUTER JOINs

When one-to-one matching between shards exists, performing an outer join on large tables is equivalent to combining outer join results of corresponding shards.

:::image type="content" source="./media/outer-joins/articles-join-example.png" alt-text="Diagram showing how Citus distributes outer joins across shards with one-to-one matching between table fragments.":::

For example, consider how Citus handles an outer join query:

```sql
SELECT table1.a, table1.b AS b1, table2.b AS b2, table3.b AS b3, table4.b AS b4
FROM table1
FULL JOIN table2 ON table1.a = table2.a
FULL JOIN table3 ON table1.a = table3.a
FULL JOIN table4 ON table1.a = table4.a;
```

First, the query goes through the standard PostgreSQL planner and Citus uses this plan to generate a distributed plan where various checks about Citus' support of the query are performed. Then individual queries that go to workers for distributed table fragments are generated.

```sql
SELECT table1.a, table1.b AS b1, table2.b AS b2, table3.b AS b3, table4.b AS b4
FROM (((table1_102359 table1
FULL JOIN table2_102363 table2 ON ((table1.a = table2.a)))
FULL JOIN table3_102367 table3 ON ((table1.a = table3.a)))
FULL JOIN table4_102371 table4 ON ((table1.a = table4.a))) WHERE true
```

```sql
SELECT table1.a, table1.b AS b1, table2.b AS b2, table3.b AS b3, table4.b AS b4
FROM (((table1_102360 table1
FULL JOIN table2_102364 table2 ON ((table1.a = table2.a)))
FULL JOIN table3_102368 table3 ON ((table1.a = table3.a)))
FULL JOIN table4_102372 table4 ON ((table1.a = table4.a))) WHERE true
```

```sql
SELECT table1.a, table1.b AS b1, table2.b AS b2, table3.b AS b3, table4.b AS b4
FROM (((table1_102361 table1
FULL JOIN table2_102365 table2 ON ((table1.a = table2.a)))
FULL JOIN table3_102369 table3 ON ((table1.a = table3.a)))
FULL JOIN table4_102373 table4 ON ((table1.a = table4.a))) WHERE true
```

```sql
SELECT table1.a, table1.b AS b1, table2.b AS b2, table3.b AS b3, table4.b AS b4
FROM (((table1_102362 table1
FULL JOIN table2_102366 table2 ON ((table1.a = table2.a)))
FULL JOIN table3_102370 table3 ON ((table1.a = table3.a)))
FULL JOIN table4_102374 table4 ON ((table1.a = table4.a))) WHERE true
```

The resulting queries might seem complex at first, but you can see that they're essentially the same as the original query, but the table names are a bit different. Citus stores the data in standard PostgreSQL tables called shards with the name as \_. With 1-1 matching of shards, the distributed outer join is equivalent to the union of all outer joins of individual matching shards. If you're sharding on some shared ID, as is common in certain [use cases](https://www.citusdata.com/blog/2016/08/10/sharding-for-a-multi-tenant-app-with-postgres/), then Citus joins on the appropriate node without any inter-worker communication.

## Related content

- [Guides overview](guides.md)
- [SQL support](reference-sql.md)
