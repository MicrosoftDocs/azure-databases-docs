---
title: Designing Your SaaS Database for Scale with PostgreSQL
description: Learn how to design your SaaS database for scale with PostgreSQL so you can efficiently support thousands of tenants.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
monikerRange: "citus-13 || citus-14"
---

# Design your SaaS database for scale with PostgreSQL

(Copy of [original publication](https://www.citusdata.com/blog/2016/10/03/designing-your-saas-database-for-high-scalability/))

When building a SaaS application, you might have the notion of tenancy built in your data model. Typically, information relates to tenants, customers, and accounts, and your database tables capture this natural relation.

With smaller amounts of data (tens of GB), it's easy to throw more hardware at the problem and scale up your database. As these tables grow however, you need to think about ways to scale your multitenant database across dozens or hundreds of machines.

This article discusses architectural patterns for multitenant databases and when to use which. At a high level, developers have three options:

- Create one database per tenant
- Create one schema per tenant
- Have all tenants share the same table or tables

The option you pick has implications on scalability, how you handle data that varies across tenants, isolation, and ease-of-maintenance.

In practice, each of the three design options can address questions around scale, data that varies across tenants, and isolation. The decision depends on the primary dimension you're building/optimizing for. The tldr:

- If you're building for scale: Have all tenants share the same table or tables
- If you're building for isolation: Create one database per tenant

This article focuses on the scaling dimension and describing considerations around isolation.

If you plan to have 5 or 50 tenants in your B2B application, and your database is running into scalability issues, then you can create and maintain a separate database for each tenant. However, if you plan to have thousands of tenants, then sharding your tables on a `tenant_id`/`account_id` column helps you scale in a better way.

:::image type="content" source="./media/designing-saas/articles-saas-figure-1.png" alt-text="Diagram showing multitenant database architecture with all tenants sharing the same tables.":::

Common benefits of having all tenants share the same database are:

Resource pooling (reduced cost): If you create a separate database for each tenant, then you need to allocate resources to that database. Further, databases usually make assumptions about resources available to them–for example, PostgreSQL has `shared_buffers`, makes good use of the operating system cache, comes with connection count settings, runs processes in the background, and writes logs and data to disk. If you're running 50 of these databases on a few physical machines, then resource pooling becomes tricky even with today's virtualization tech.

Distributed databases can manage all tenants. You could shard your tables on `tenant_id` and easily support thousands or tens of thousands of tenants.

[Google's F1 paper](http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41344.pdf) is a good example that demonstrates a multitenant database that scales this way. The paper talks about technical challenges associated with scaling out the Google AdWords platform; and at its core describes a multitenant database. The F1 paper also highlights how best to model data to support many tenants/customers in a distributed database.

:::image type="content" source="./media/designing-saas/articles-saas-figure-2.png" alt-text="Screenshot comparing a relational database model versus a hierarchical database model for multitenant applications.":::

The data model on the left-hand side follows the relational database model and uses foreign key constraints to ensure data integrity in the database. This strict relational model introduces certain drawbacks in a distributed environment however.

In particular, most transactions and joins you perform on your database, and constraints you'd like to enforce across your tables, have a customer/tenant dimension to them. If you shard your tables on their primary key column (in the relational model), then most distributed transactions, joins, and constraints become expensive. Network and machine failures further add to this cost.

The diagram on the right-hand side proposes the hierarchical database model. This model is the one used by F1 and resolves the previously mentioned issues. In its simplest form, you add a `customer_id`/`tenant_id` column to your tables and shard them on `customer_id`. This ensures that data from the same customer gets [colocated together](https://citusdata.com/blog/2016/08/10/sharding-for-a-multi-tenant-app-with-postgres/). Colocation dramatically reduces the cost associated with distributed transactions, joins, and [foreign key constraints](https://github.com/citusdata/citus/issues/698).

Ease of maintenance: Another challenge associated with supporting 100-100K tenants is schema changes (Alter Table) and index creations (Create Index). As your application grows, you iterate on your database model and make improvements.

If you follow an architecture where each tenant lives in a separate database, you need to implement an infrastructure that ensures each schema change succeeds across all tenants or eventually gets rolled back. Consider what happens when you changed the schema for 5,000 of 10K tenants and observed a failure? How do you handle that?

When you shard your tables for multi-tenancy, then you're having your database do the work for you. The database either ensures that an Alter Table goes through across all shards, or it rolls it back.

What about data that varies across tenants? Another challenge with scaling to thousands of tenants relates to handling data that varies across tenants. Your multitenant application naturally includes a standard database setup with default tables, fields, queries, and relationships that are appropriate to your solution. Different tenants/organizations might have their own unique needs that a rigid, inextensible default data model won't be able to address. For example, one organization might need to track their stores in the US through their zip codes. Another customer in Europe might not care about US zip codes, but might be interested to keep tax ratios for each store.

This used to be an area where having a tenant per database offered the most flexibility, at the cost of extra maintenance work from the developer. You could create separate tables or columns per tenant in each database, and manage those differences across time.

If then you wanted to scale your infrastructure to thousands of tenants, you'd create a huge table with many string columns (Value0, Value1, ... Value500).

:::image type="content" source="./media/designing-saas/articles-saas-figure-3.png" alt-text="Screenshot of database schema showing custom columns labeled as V1, V2, and V3 for storing tenant-specific data.":::

In this database model, your tables have a preset collection of custom columns, labeled in this image as V1, V2, and V3. Dates and Numbers are stored as strings in a format such that they can be converted to their native types. When you're storing data associated with a particular tenant, you can then use these custom columns and tailor them to each tenant's needs.

Fortunately, designing your database to account for "flexible" columns became easier with the introduction of semi-structured data types. PostgreSQL has a rich set of semi-structured data types that include [hstore, json, and jsonb](https://citusdata.com/blog/2016/07/14/choosing-nosql-hstore-json-jsonb/). You can now represent the previous database schema by declaring a jsonb column and scale to thousands of tenants.

:::image type="content" source="./media/designing-saas/articles-saas-figure-4.png" alt-text="Screenshot of simplified database schema that uses JSONB column for flexible tenant-specific data storage.":::

If you shard your database tables, consider how to handle isolation or integrate with Object-Relational Mapping (ORM) libraries. Also consider what happens if you have a table where you can't easily add a `tenant_id` column.

For more information, see [Use cases](use-cases.md).

## Related content

- [Guides overview](guides.md)
- [Sharding a multitenant app with PostgreSQL](sharding-mt-app.md)
- [What is Citus?](what-is-citus.md)
