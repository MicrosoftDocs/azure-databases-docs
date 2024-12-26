---
title: Troubleshooting Best Practices
description: This article describes some recommendations for troubleshooting Azure Database for MySQL - Flexible Server.
author: code-sidd
ms.author: sisawant
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Best practices for troubleshooting Azure Database for MySQL - Flexible Server

Use the following sections to keep your Azure Database for MySQL flexible server databases running smoothly and use this information as guiding principles for ensuring that the schemas are designed optimally and provide the best performance for your applications.

## Check the number of indexes

In a busy database environment, you might observe high I/O usage, which can be an indicator of poor data access patterns. Unused indexes can have a negative impact on performance as they consume disk space and cache, and slow down write operations (INSERT / DELETE / UPDATE). Unused indexes unnecessarily consume more storage space and increase the backup size.

Before you remove any index, be sure to gather enough information to verify that it's no longer in use. This verification can help you avoid inadvertently removing an index that is critical for a query that runs only quarterly or annually. Also, be sure to consider whether an index is used to enforce uniqueness or ordering.

> [!NOTE]  
> Remember to review indexes periodically and perform any necessary updates based on any modifications to the table data.

`SELECT object_schema,
  object_name,
  index_name
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE index_name IS NOT NULL
AND count_star = 0
ORDER BY object_schema, object_name;`

(or)

`use information_schema;
select
tables.table_name,
statistics.index_name,
statistics.cardinality,
tables.table_rows
from tables
join statistics
on (statistics.table_name = tables.table_name
and statistics.table_schema = '<YOUR DATABASE NAME HERE>'
and ((tables.table_rows / statistics.cardinality) > 1000));`

## List the busiest indexes on the server

The output from the following query provides information about the most used indexes across all tables and schemas on the database server. This information is helpful in identifying the ratio of writes to reads against each index and the latency numbers for reads as well as individual write operations, which can indicate that further tuning is required against the underlying table and dependent queries.

```sql
SELECT
object_schema AS table_schema,
object_name AS table_name,
index_name, count_star AS all_accesses,
count_read,
count_write,
Concat(Truncate(count_read / count_star * 100, 0), ':',
Truncate(count_write / count_star * 100, 0)) AS read_write_ratio,
 count_fetch AS rows_selected ,
 count_insert AS rows_inserted,
 count_update AS rows_updated,
 count_delete AS rows_deleted,
 Concat(Round(sum_timer_wait / 1000000000000, 2), ' s') AS total_latency ,
 Concat(Round(sum_timer_fetch / 1000000000000, 2), ' s') AS select_latency,
 Concat(Round(sum_timer_insert / 1000000000000, 2), ' s') AS insert_latency,
Concat(Round(sum_timer_update / 1000000000000, 2), ' s') AS update_latency,
 Concat(Round(sum_timer_delete / 1000000000000, 2), ' s') AS  delete_latency
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE index_name IS NOT NULL AND count_star > 0
ORDER BY sum_timer_wait DESC
```

## Review the primary key design

Azure Database for MySQL flexible server uses the InnoDB storage engine for all nontemporary tables. With InnoDB, data is stored within a clustered index using a B-Tree structure. The table is physically organized based on primary key values, which means that rows are stored in the primary key order.

Each secondary key entry in an InnoDB table contains a pointer to the primary key value in which the data is stored. In other words, a secondary index entry contains a copy of the primary key value to which the entry is pointing. Therefore, primary key choices have a direct effect on the amount of storage overhead in your tables.

If a key is derived from actual data (e.g., username, email, SSN, etc.), it's called a *natural key*. If a key is artificial and not derived from data (e.g., an autoincremented integer), it's referred to as a *synthetic key* or *surrogate key*.

It's generally recommended to avoid using natural primary keys. These keys are often very wide and contain long values from one or multiple columns. This in turn can introduce severe storage overhead with the primary key value being copied into each secondary key entry. Moreover, natural keys don't usually follow a predetermined order, which dramatically reduces performance and provokes page fragmentation when rows are inserted or updated. To avoid these issues, use monotonically increasing surrogate keys instead of natural keys. An autoincrement (big)integer column is a good example of a monotonically increasing surrogate key. If you require a certain combination of columns, be unique, declare those columns as a unique secondary key.

During the initial stages of building an application, you might not think ahead to imagine a time when your table begins to approach having two billion rows. As a result, you might opt to use a signed 4-byte integer for the data type of an ID (primary key) column. Be sure to check all table primary keys and switch to use 8-byte integer (BIGINT) columns to accommodate the potential for a high volume or growth.

> [!NOTE]  
> For more information about data types and their maximum values, in the MySQL Reference Manual, see [Data Types](https://dev.mysql.com/doc/refman/5.7/en/data-types.html).

## Use covering indexes

The previous section explains how indexes in MySQL are organized as B-Trees and in a clustered index, the leaf nodes contain the data pages of the underlying table. Secondary indexes have the same B-tree structure as clustered indexes, and you can define them on a table or view with a clustered index or a heap. Each index row in the secondary index contains the nonclustered key value and a row locator. This locator points to the data row in the clustered index or heap having the key value. As a result, any lookup involving a secondary index must navigate starting from the root node through the branch nodes to the correct leaf node to take the primary key value. The System then executes a random IO read on the primary key index (once again navigating from the root node through the branch nodes to the correct leaf node) to get the data row.

To avoid this extra random IO read on the primary key index to get the data row, use a covering index, which includes all fields required by the query. Generally, using this approach is beneficial for I/O bound workloads and cached workloads. So as a best practice, use covering indexes because they fit in memory and are smaller and more efficient to read than scanning all the rows.

Consider, for example, a table that you're using to try to find all employees who joined the company after January 1, 2000.

```sql
mysql> show create table employee\G
****************** 1. row ******************
       Table: employee
Create Table: CREATE TABLE `employee` (
  `empid` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(10) DEFAULT NULL,
  `lname` varchar(10) DEFAULT NULL,
  `joindate` datetime DEFAULT NULL,
  `department` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`empid`)
  ) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1
1 row in set (0.00 sec)`

`mysql> select empid, fname, lname from employee where joindate > '2000-01-01';
```

If you run an EXPLAIN plan on this query, you'd observe that currently no indexes are being used, and a where clause alone is being used to filter the employee records.

```sql
mysql> EXPLAIN select empid, fname, lname from employee where joindate > '2000-01-01'\G
****************** 1. row ******************
           id: 1
  select_type: SIMPLE
        table: employee
   partitions: NULL
         type: ALL
possible_keys: NULL
          key: NULL
      key_len: NULL
          ref: NULL
         rows: 3
     filtered: 33.33
        Extra: Using where
1 row in set, 1 warning (0.01 sec)
```

However, if you added an index that covers the column in the where clause, along with the projected columns you would see that the index is being used to locate the columns much more quickly and efficiently.

`mysql> CREATE INDEX cvg_idx_ex ON employee (joindate, empid, fname, lname);`

Now, if you run EXPLAIN plan on the same query, the "Using Index" value appears in the "Extra" field, which means that InnoDB executes the query using the index we created earlier, which confirms this as a covering index.

```sql
mysql> EXPLAIN select empid, fname, lname from employee where joindate > '2000-01-01'\G
****************** 1. row ******************
           id: 1
  select_type: SIMPLE
        table: employee
   partitions: NULL
         type: range
possible_keys: cvg_idx_ex
          key: cvg_idx_ex
      key_len: 6
          ref: NULL
         rows: 1
     filtered: 100.00
        Extra: Using where; Using index
1 row in set, 1 warning (0.01 sec)
```

> [!NOTE]  
> It's important to choose the correct order of the columns in the covering index to serve query correctly. The general rule is to choose the columns for filtering first (WHERE clause), then sorting/grouping (ORDER BY and GROUP BY) and finally the data projection (SELECT).

From the prior example, we've seen that having a covering index for a query provides more efficient record retrieval paths and optimizes performance in a highly concurrent database environment.

## Next step

> [!div class="nextstepaction"]
> [Stack Overflow](https://stackoverflow.com/questions/tagged/azure-database-mysql)
