---
title: Sharding a Multitenant App with PostgreSQL
description: Learn how to shard a multitenant app with PostgreSQL and Citus so you can scale your SaaS application efficiently.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
monikerRange: "citus-13 || citus-14"
---

# Shard a multitenant app with PostgreSQL

(Copy of [original publication](https://www.citusdata.com/blog/2016/08/10/sharding-for-a-multi-tenant-app-with-postgres/))

If you're building an application, and your customer is another business, then a multitenant approach is the norm. A multitenant approach works whether you're building marketing analytics, a portal for e-commerce sites, or an application to cater to schools. The same code runs for all customers, but each customer sees their own private data set, except in some cases of holistic internal reporting.

Early in your application's life, customer data has a simple structure that evolves organically. Typically all information relates to a central customer/user/tenant table. With a smaller amount of data (10s of GB), it's easy to scale the application by throwing more hardware at it. However, consider when you scale out because you found success and data that no longer fits in memory in a single box. Or, consider that you need more concurrencies.

If you model your multitenant data in the right way, sharding can become simpler and give you the power you need from a database including joins, indexing, and more. While Citus lets you scale out your processing power and memory, how you model your data determines the ease and flexibility you get from the system. If you're building a multitenant SaaS application, following example highlights how you can plan early for scaling.

## Tenancy

At the core of most nonconsumer focused applications, tenancy is already built in. As previously mentioned, you might have a users table. Consider the following SaaS schema:

```sql
CREATE TABLE stores (
  id UUID,
  owner_email VARCHAR(255),
  owner_password VARCHAR(255),
  name VARCHAR(255),
  url VARCHAR(255),
  last_login_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ
)

CREATE TABLE products (
  id UUID,
  name VARCHAR(255),
  description TEXT,
  price INTEGER,
  quantity INTEGER,
  store_id UUID,
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ
)

CREATE TABLE purchases (
  id UUID,
  product_id UUID,
  customer_id UUID,
  store_id UUID,
  price INTEGER,
  purchased_at TIMESTAMPTZ,
)
```

The previous schema highlights a simplified, multitenant e-commerce site. For example, if someone has a preferred site, there are many queries you would run:

List the products for a particular store:

```sql
SELECT id,
       name,
       price
FROM products
WHERE store_id = 'foo';
```

If you want to compute how many purchases exist weekly for a given store:

```sql
SELECT date_trunc('week', purchased_at),
       sum(price * quantity)
FROM purchases,
     stores
WHERE stores.id = products.stores_id
  AND store_id = 'foo'
```

From here, you can plan how to give each store its own presence and analytics. The easiest level to scale out is the tenant level or on store ID. With the previous data model, the largest tables over time are likely to be products and purchases. You could shard on both. Though if you choose products or purchases, the difficulty lies in the fact that you might want to do queries that focus on some high level item such as store. If you choose store ID, then all data for a particular store would exist on the same node. This choice allows you to push down all computations directly to a single node.

## Multi-tenancy and colocation, a perfect pair

Colocating data within the same physical instance avoids sending data over the network during joins, which can result in faster operations. With Citus, you can move your data around, so you can join and query it in a flexible manner. For this class of multitenant SaaS apps, it's simple if you can ensure data ends up on the shard. To ensure data ends up on the shard, you need to push down your store ID to all of your tables.

Include `store_id` on all tables, so you can easily shard out all your data so that it's on the same shard. In the previous data model,`store_id` is on all of the tables, but if it weren't there, you could add it. Doing so would put you in a good position to distribute all your data to store it on the same nodes. You can now try sharding your tenants, in this case stores:

```sql
SELECT create_distributed_table('stores', 'id');
SELECT create_distributed_table('products', 'store_id');
SELECT create_distributed_table('purchases', 'store_id');
```

The previous example shards by `store_id`, which allows all queries to be routed to a single PostgreSQL instance. The same queries as before should work for you as long as you have `store_id` on your query. An example layout of your data might look something like:

:::image type="content" source="./media/sharding-mt-app/sharding-store-tenant.png" alt-text="Diagram showing data distribution across shards with stores, products, and purchases colocated by store ID on the same nodes.":::

The alternative to colocation is to choose a lower level shard key, such as orders or products. This choice makes joins and querying more difficult because you have to send more data over the network and make sure things work in a distributed way. A lower level key can be useful for consumer focused datasets if your analytics are always against the entire data set, as is often the case in metrics-focused use cases.

## In conclusion

Different distribution models have different benefits and trade-offs. In some cases, modeling on a lower level entity ID, such as products or purchases, can be the right choice. You gain more parallelism for analytics and trade off simplicity in querying a single store. To make a model to scale, you can choose a multitenant data model or adopt semi-structured data. For more information, see [Sharding PostgreSQL with semi-structured data and its performance implications](semi-structured-data.md).

## Related content

- [Guides overview](guides.md)
- [Designing your SaaS database for scale](designing-saas.md)
- [Tutorial: Design a multitenant database](tutorial-multi-tenant.md)
