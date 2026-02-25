---
title: Identify a Distribution Strategy
description: This article describes how to identify a distribution strategy for your tables and keys when migrating a multitenant application to Citus.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
monikerRange: "citus-13 || citus-14"
---

# Identify a distribution strategy

The first step in a multitenant application to Citus is identifying suitable distribution keys and planning your table distribution accordingly.

## Pick a distribution key

In multitenant applications, the distribution key is typically an internal identifier for tenants. We typically refer to it as the *tenant ID*. The use-cases might vary, so we advise being thorough on this step.

For guidance, read these articles:

- [Determining application type](../app-type.md)
- [Choosing a distribution column](../data-modeling.md)

We're happy to help review your environment to be sure that the ideal distribution key is chosen. To do so, we typically examine schema layouts, larger tables, long-running and/or problematic queries, standard use cases, and more.

## Identify types of tables

Once you identify a distribution key, review the schema to identify how each table should be handled and whether any modifications to table layouts are required. We typically advise tracking this work with a spreadsheet.

Tables generally fall into one of the following categories:

- **Ready for distribution**. These tables already contain the distribution key, and are ready for distribution.
- **Needs backfill**. These tables are logically distributed by the chosen key, but don't contain a column directly referencing it. In the next section, we modify these tables to add the column.
- **Reference table**. These tables are typically small and don't contain the distribution key. They're commonly joined by distributed tables, and/or are shared across tenants. A copy of each of these tables is maintained on all nodes. Common examples include country/region code lookups, product categories, and the like.
- **Local table**. These tables are typically not joined to other tables, and don't contain the distribution key. They're maintained exclusively on the coordinator node. Common examples include admin user lookups and other utility tables.

Consider an example multitenant application similar to Etsy or Shopify where each tenant is a store. The following diagram shows a portion of a simplified schema for the exmaple app. The underlined items are primary keys and the italicized items are foreign keys.

:::image type="content" source="./media/migration-schema/mt-before.png" alt-text="Diagram of a portion of the schema for the example multitenant application, showing relationships between table keys.":::

In this example, stores are a natural tenant. The tenant ID in this case is the store_id. After distributing tables in the cluster, we want rows relating to the same store to reside together on the same nodes.

## Prepare source tables for migration

Once the scope of needed database changes is identified, the next major step is to modify the data structure for the application's existing database. First, tables requiring backfill are modified to add a column for the distribution key.

### Add distribution keys

In our storefront example, the stores and products tables have a store_id and are ready for distribution. Being normalized, the line_items table lacks a store ID. If we want to distribute by store_id, the table needs this column.

```sql
-- denormalize line_items by including store_id

ALTER TABLE line_items ADD COLUMN store_id uuid;
```

Be sure to check that the distribution column has the same type in all tables, for example, don't mix `int` and `bigint`. The column types must match to ensure proper data colocation.

### Backfill newly created columns

Once the schema is updated, backfill missing values for the tenant_id column in tables where the column was added. In our example, line_items requires values for store_id.

We backfill the table by obtaining the missing values from a join query with orders:

```sql
UPDATE line_items
   SET store_id = orders.store_id
  FROM line_items
 INNER JOIN orders
 WHERE line_items.order_id = orders.order_id;
```

Doing the whole table at once might cause too much load on the database and disrupt other queries. You can do the backfill more slowly instead. One way to do that is to make a function that backfills small batches at a time, then call the function repeatedly with [pg_cron](https://github.com/citusdata/pg_cron).

```sql
-- the function to backfill up to ten
-- thousand rows from line_items

CREATE FUNCTION backfill_batch()
RETURNS void LANGUAGE sql AS $$
  WITH batch AS (
    SELECT line_items_id, order_id
      FROM line_items
     WHERE store_id IS NULL
     LIMIT 10000
       FOR UPDATE
      SKIP LOCKED
  )
  UPDATE line_items AS li
     SET store_id = orders.store_id
    FROM batch, orders
   WHERE batch.line_item_id = li.line_item_id
     AND batch.order_id = orders.order_id;
$$;

-- run the function every quarter hour
SELECT cron.schedule('*/15 * * * *', 'SELECT backfill_batch()');

-- ^^ note the return value of cron.schedule
```

Once the backfill is caught up, the cron job can be disabled:

```sql
-- assuming 42 is the job id returned
-- from cron.schedule

SELECT cron.unschedule(42);
```

## Related content

- [Multitenant query migration](migration-query.md)
- [Migration overview](migrating.md)
