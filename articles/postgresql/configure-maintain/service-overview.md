---
title: Service overview
description: Provides an overview of the Azure Database for PostgreSQL flexible server relational database service.
author: gbowerman
ms.author: guybo
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: overview
ms.custom:
  - mvc
---

# What is Azure Database for PostgreSQL ?

> [!IMPORTANT]
> Azure Database for PostgreSQL - Hyperscale (Citus) is now [Azure Cosmos DB for PostgreSQL](../../cosmos-db/postgresql/introduction.md). To learn more about this change, see [Where is Hyperscale (Citus)?](../hyperscale/moved.md).

Azure Database for PostgreSQL flexible server is a relational database service in the Microsoft cloud based on the [PostgreSQL open source relational database](https://www.postgresql.org/). Azure Database for PostgreSQL flexible server delivers:

- Built-in high availability.
- Data protection using automatic backups and point-in-time-restore for up to 35 days.
- Automated maintenance for underlying hardware, operating system and database engine to keep the service secure and up to date.
- Predictable performance, using inclusive pay-as-you-go pricing.
- Elastic scaling within seconds.
- Enterprise grade security and industry-leading compliance to protect sensitive data at-rest and in-motion.
- Monitoring and automation to simplify management and monitoring for large-scale deployments.
- Industry-leading support experience.

:::image type="content" source="./media/service-overview/overview-what-is-azure-postgres.png" alt-text="Azure Database for PostgreSQL flexible server.":::

These capabilities require almost no administration, and all are provided at no extra cost. They allow you to focus on rapid application development and accelerating your time to market rather than allocating precious time and resources to managing virtual machines and infrastructure. In addition, you can continue to develop your application with the open-source tools and platform of your choice to deliver with the speed and efficiency your business demands, all without having to learn new skills.

## Deployment modes

Azure Database for PostgreSQL flexible server powered by the PostgreSQL community edition has two deployment modes:

- Flexible server

### Azure Database for PostgreSQL 

Azure Database for PostgreSQL flexible server is a fully managed database service designed to provide more granular control and flexibility over database management functions and configuration settings. In general, the service provides more flexibility and customizations based on the user requirements. The flexible server architecture allows users to opt for high availability within single availability zone and across multiple availability zones. Azure Database for PostgreSQL flexible server provides better cost optimization controls with the ability to stop/start server and burstable compute tier, ideal for workloads that don’t need full-compute capacity continuously. Azure Database for PostgreSQL flexible server currently supports community version of PostgreSQL [!INCLUDE [major-versions-ascending](../includes/major-versions-ascending.md)] with plans to add newer versions as they become available. Azure Database for PostgreSQL flexible server is generally available today in a wide variety of [Azure regions](../configure-maintain/overview.md#azure-regions).

Azure Database for PostgreSQL flexible server instances are best suited for:

- Application developments requiring better control and customizations
- Cost optimization controls with ability to stop/start server
- Zone redundant high availability
- Managed maintenance windows

For a detailed overview of Azure Database for PostgreSQL flexible server deployment mode, see [Azure Database for PostgreSQL flexible server](../configure-maintain/overview.md).

## Related content
- [Azure Database for PostgreSQL flexible server overview](../configure-maintain/overview.md)