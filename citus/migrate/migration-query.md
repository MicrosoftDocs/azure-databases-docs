---
title: Prepare an Application for Citus
description: This article describes how to prepare an application to work with Citus.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
monikerRange: "citus-13 || citus-14"
---

# Prepare an application for Citus

When you [migrate an existing application to Citus](migration.md), the first steps are to optimize the existing database schema. This article describes the next step, which is to update your application code and queries to deal with those schema changes.

## Set up development Citus cluster

When modifying an application to work with Citus, you need a database to test against. Follow the instructions to set up a `development` of your choice.

Next, dump a copy of the schema from your application's original database and restore the schema in the new development database.

```bash
# get schema from source db

pg_dump \
   --format=plain \
   --no-owner \
   --schema-only \
   --file=schema.sql \
   --schema=target_schema \
   postgres://user:pass@host:5432/db

# load schema into test db

psql postgres://user:pass@testhost:5432/db -f schema.sql
```

The schema should include a distribution key (a *tenant ID*) in all of the tables you wish to distribute. Before pg_dumping the schema, be sure you complete the step [prepare source tables for migration](migration-schema.md#prepare-source-tables-for-migration).

### Include distribution column in keys

Citus can't enforce uniqueness constraints unless a unique index or primary key contains the distribution column. Thus, we must modify primary and foreign keys in our example to include `store_id`.

Some of the libraries listed in the next section are able to help migrate the database schema to include the distribution column in keys. However, here's an example of the underlying SQL commands to turn the simple keys composite in the development database:

```sql
BEGIN;

-- drop simple primary keys (cascades to foreign keys)

ALTER TABLE products   DROP CONSTRAINT products_pkey CASCADE;
ALTER TABLE orders     DROP CONSTRAINT orders_pkey CASCADE;
ALTER TABLE line_items DROP CONSTRAINT line_items_pkey CASCADE;

-- recreate primary keys to include would-be distribution column

ALTER TABLE products   ADD PRIMARY KEY (store_id, product_id);
ALTER TABLE orders     ADD PRIMARY KEY (store_id, order_id);
ALTER TABLE line_items ADD PRIMARY KEY (store_id, line_item_id);

-- recreate foreign keys to include would-be distribution column

ALTER TABLE line_items ADD CONSTRAINT line_items_store_fkey
  FOREIGN KEY (store_id) REFERENCES stores (store_id);
ALTER TABLE line_items ADD CONSTRAINT line_items_product_fkey
  FOREIGN KEY (store_id, product_id) REFERENCES products (store_id, product_id);
ALTER TABLE line_items ADD CONSTRAINT line_items_order_fkey
  FOREIGN KEY (store_id, order_id) REFERENCES orders (store_id, order_id);

COMMIT;
```

Now that the step is complete, our schema from the previous section looks like the following diagram:

:::image type="content" source="./media/migration-query/mt-after.png" alt-text="Diagram of a portion of the schema for the example multitenant application, showing relationships between table keys.":::

(Underlined items are primary keys, italicized items are foreign keys.)

Be sure to modify data flows to add keys to incoming data.

## Add distribution key to queries

Once the distribution key is present on all appropriate tables, the application needs to include it in queries. The following steps should be done using a copy of the application running in a development environment, and testing against a Citus back-end. After the application is working with Citus, we'll see how to migrate production data from the source database into a real Citus cluster.

- Application code and any other ingestion processes that write to the tables should be updated to include the new columns.
- Running the application test suite against the modified schema on Citus is a good way to determine which areas of the code need to be modified.
- It's a good idea to enable database logging. The logs can help uncover stray cross-shard queries in a multitenant app that should be converted to per-tenant queries.

Cross-shard queries are supported, but in a multitenant application most queries should be targeted to a single node. For simple select, update, and delete queries this restriction means that the *where* clause should filter by tenant ID. Citus can then run these queries efficiently on a single node.

There are helper libraries for many popular application frameworks that make it easy to include a tenant ID in queries:

| Framework | Resource |
| --- | --- |
| Ruby on Rails | [Ruby on Rails migration guide](migration-ruby-rails.md) |
| Django | [Django Multitenant](https://django-multitenant.readthedocs.io/en/latest/migration_mt_django.html) |
| ASP.NET | [ASP.NET migration guide](migration-asp.md) |
| Java Hibernate | [Using Hibernate and Spring to build multitenant Java apps](https://www.citusdata.com/blog/2018/02/13/using-hibernate-and-spring-to-build-multitenant-java-apps/) |

It's possible to use the libraries for database writes first (including data ingestion), and later for read queries. For instance, the [activerecord-multi-tenant](https://github.com/citusdata/activerecord-multi-tenant) Gemfile has a [write-only mode](https://github.com/citusdata/activerecord-multi-tenant#rolling-out-activerecord-multi-tenant-for-your-application-write-only-mode) that only modifies the write queries.

### Other (SQL principles)

If you're using a different object-relational mapping (ORM) than in the previous section, or doing multitenant queries more directly in SQL, follow these general principles.

Using our earlier example of an e-commerce application, suppose we want to get the details for an order. Distributed queries that filter on the tenant ID run most efficiently in multitenant apps, so the following change makes the query faster (while both queries return the same results):

```sql
-- before
SELECT *
  FROM orders
 WHERE order_id = 123;

-- after
SELECT *
  FROM orders
 WHERE order_id = 123
   AND store_id = 42; -- <== added
```

The tenant_id column isn't only beneficial--but critical--for insert statements. Inserts must include a value for the tenant_id column or else Citus is unable to route the data to the correct shard and it raises an error.

Finally, when joining tables make sure to filter by tenant_id too. For instance, here's how to inspect how many "Awesome Wool Pants" a given store sold:

```sql
-- One way is to include store_id in the join and also
-- filter by it in one of the queries

SELECT sum(l.quantity)
  FROM line_items l
 INNER JOIN products p
    ON l.product_id = p.product_id
   AND l.store_id = p.store_id
 WHERE p.name='Awesome Wool Pants'
   AND l.store_id='8c69aa0d-3f13-4440-86ca-443566c1fc75'

-- Equivalently you omit store_id from the join condition
-- but filter both tables by it. This may be useful if
-- building the query in an ORM

SELECT sum(l.quantity)
  FROM line_items l
 INNER JOIN products p ON l.product_id = p.product_id
 WHERE p.name='Awesome Wool Pants'
   AND l.store_id='8c69aa0d-3f13-4440-86ca-443566c1fc75'
   AND p.store_id='8c69aa0d-3f13-4440-86ca-443566c1fc75'
```

## Enable secure connections

Clients should connect to Citus with TLS/SSL to protect information and prevent man-in-the-middle attacks.

## Check for cross-node traffic

With large and complex application code-bases, certain queries generated by the application can often be overlooked, and don't have a tenant_id filter on them. Citus' parallel executor still executes these queries successfully, and so, during testing, these queries remain hidden since the application still works fine. However, if a query doesn't contain the tenant_id filter, Citus' executor hits every shard in parallel, but only one returns any data. This configuration consumes resources needlessly, and might exhibit itself as a problem only when one moves to a higher-throughput production environment.

To prevent encountering such issues only after launching in production, one can set a config value to log queries that hit more than one shard. In a properly configured and migrated multitenant application, each query should only hit one shard at a time.

During testing, you can log these queries by making this configuration:

```sql
-- adjust for your own database's name of course

ALTER DATABASE citus SET citus.multi_task_query_log_level = 'error';
```

With this setting, Citus errors out if it encounters queries that are going to hit more than one shard. Erroring out during testing allows the application developer to find and migrate such queries.

During a production launch, one can configure the same setting to log, instead of error out:

```sql
ALTER DATABASE citus SET citus.multi_task_query_log_level = 'log';
```

The configuration parameter section has more info on supported values for this setting.

## Related content

- [Migrate the schema](migration-schema.md)
- [Migrate an existing application to Citus](migration.md)
- [What is Citus?](../what-is-citus.md)
