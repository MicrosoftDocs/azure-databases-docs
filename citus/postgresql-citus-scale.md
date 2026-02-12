---
title: PostgreSQL at Any Scale with Citus
description: Learn how Citus scales from small clusters to large deployments, and discover when to use Citus for multitenant SaaS, real-time analytics, and microservices workloads.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
ai-usage: ai-assisted
monikerRange: "citus-13 || citus-14"
---

# Scale PostgreSQL with Citus

This article shows what scaling out looks like and highlights real customer cluster sizes to illustrate that Citus works for both small (2–3 node) and large multinode deployments.

You can start using Citus on a single node with a distributed data model from the beginning so your solution is "scale out ready." When your PostgreSQL workload needs to scale, you can easily add worker nodes to the Citus database cluster, and scale up the coordinator and worker nodes in your cluster.
Citus scales from small clusters (2-3 nodes) to large deployments handling petabytes of data and billions of rows per day. Real-world production clusters scale to more than 100 nodes, processing billions of events daily with subsecond query response times.

## When to use Citus

Use these scenario guides to decide if Citus aligns with your workload—multitenant SaaS, real-time analytics, or microservices—and to understand the considerations and limits before adopting.

### Multitenant SaaS database

Most B2B applications already include the concept of a tenant, customer, or account in their data model. In this model, the database serves many tenants, and each tenant's data stays separate from the data of other tenants.

Citus provides full SQL coverage for this workload and lets you scale out your relational database to more than 100,000 tenants. Citus also adds new features for multitenancy. For example, Citus supports tenant isolation to provide performance guarantees for large tenants. It also includes the concept of reference tables to reduce data duplication across tenants.

By using these capabilities, you can scale out your tenants' data across many machines and easily add more CPU, memory, and disk resources. Sharing the same database schema across multiple tenants makes efficient use of hardware resources and simplifies database management.

Some advantages of Citus for multitenant applications include:

- Fast queries for all tenants
- Sharding logic in the database, not the application
- Hold more data than possible in single-node PostgreSQL
- Scaling out without giving up SQL
- Maintaining performance under high concurrency
- Fast metrics analysis across customer base
- Easily scale to handle new customer signups
- Isolate resource usage of large and small customers

### Real-time analytics

Citus supports real-time queries over large datasets. These queries commonly occur in rapidly growing event systems or systems with time series data. Example use cases include:

- Analytic dashboards with subsecond response times
- Exploratory queries on unfolding events
- Large dataset archival and reporting
- Analyzing sessions with funnel, segmentation, and cohort queries

Citus benefits you by parallelizing query execution and scaling linearly with the number of worker databases in a cluster. Some advantages of Citus for real-time applications include:

- Maintaining subsecond responses as the dataset grows
- Analyzing new events and new data as it happens, in real-time
- Parallelizing SQL queries
- Scaling out without giving up SQL
- Maintaining performance under high concurrency
- Fast responses to dashboard queries
- Using one database, not a patchwork
- Rich PostgreSQL data types and extensions

### Microservices

Citus supports schema-based sharding, which you can use to distribute regular database schemas across many machines. This sharding method works well with typical microservices architecture, where each service fully owns its storage and can't share the same schema definition with other tenants.

Schema-based sharding is an easier model to adopt. Create a new schema and set the `search_path` in your service, and you're ready to go.

Advantages of using Citus for microservices:

- Distribute horizontally scalable state across services, solving one of the [main problems](https://stackoverflow.blog/2020/11/23/the-macro-problem-with-microservices/) of microservices.
- Ingest strategic business data from microservices into common distributed tables for analytics.
- Efficiently use hardware by balancing services on multiple machines.
- Isolate noisy services to their own nodes.
- Easy to understand sharding model.
- Quick adoption.

### Considerations and limitations

Citus extends PostgreSQL with distributed functionality, but it isn't a replacement that scales out all workloads. A performant Citus cluster involves thinking about the data model, tooling, and choice of SQL features.

If your workload aligns with the use cases described in this article and you run into an unsupported tool or query, there's usually a good workaround.

### When Citus isn't the right fit

Some workloads don't need a powerful distributed database, while others require a large flow of information between worker nodes. In the first case, Citus is unnecessary, and in the second case, it's not performant. Here are some examples:

- Workloads that never grow beyond a single PostgreSQL node.
- Offline analytics without the need for real-time ingest or real-time queries.
- Analytics apps that don't need to support a large number of concurrent users.
- Queries that return data-heavy ETL results rather than summaries.

## Related content

- [What is Citus?](what-is-citus.md)
- [Multitenant applications tutorial](tutorial-multi-tenant.md)
