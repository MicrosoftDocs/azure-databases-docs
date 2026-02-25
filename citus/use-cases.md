---
title: Use Cases
description: This article describes Use Cases.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: how-to
monikerRange: "citus-13 || citus-14"
---

# Use cases

After [Getting Started](getting-started.md), it's time to go deeper into the most common use-cases for Citus.

- [Choosing a distribution column](data-modeling.md) is a hands-on guide for building the backend of an example ad analytics app. The article reviews data modeling for distributed systems, including how to adapt an existing single-machine database schema. It also outlines common challenges for scaling and how to solve them.
- [Building a scalable PostgreSQL metrics backend using the Citus extension](metrics-dashboard.md) outlines the other prominent Citus use case: super fast, highly parallel aggregate queries. The article shows how to model the backend for a web dashboard for event data. It also discusses managing constantly increasing data, even when the data is unstructured.

Once you learn these use-cases in depth, you can learn more about [Migrating an existing app](migrate/migration.md) to port your existing application.

## Related content

- [Multitenant applications tutorial](tutorial-multi-tenant.md)
- [Analytics and dashboards tutorial](tutorial-analytics.md)
- [What is Citus?](what-is-citus.md)
