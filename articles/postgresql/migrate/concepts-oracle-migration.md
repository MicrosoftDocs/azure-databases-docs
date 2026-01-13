---
title: "Migrating Oracle to Azure Database for PostgreSQL"
description: "This article discusses concepts regarding Oracle to Azure Database for PostgreSQL migrations."
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: maghan
ms.contributor: datasqlninja
ms.date: 01/24/2025
ms.service: azure-database-postgresql
ms.topic: concept-article
ms.collection:
  - migration
  - onprem-to-azure
---

# Migrating Oracle To Azure Database for PostgreSQL

Migrating from Oracle database to Azure Database for PostgreSQL flexible server can provide multiple key benefits to organizations who are modernizing their operations and infrastructure including: cost efficiency, simplified licensing models and vendor independence, flexible resource scalability, open-source extensibility, and advanced security integration features.

The success and increasing popularity of open source technologies over the past several years have resulted in Postgres database gaining the status as the preferred platform for Oracle migrations. This same popularity and extended ecosystem have led to new challenges as well. Organizations interested in migrating must navigate through a crowded solution space occupied by numerous open-source and private third-party providers offering similar, yet critically unique differences in their approach and feature sets.

These concepts and strategic best practices provide a comprehensive overview of the key phases required to migrate successfully for all migration paths and introduces our recommended solution provider ecosystem offering tools, technologies, and services to ensure each stage of your migration moves forward.

## Why Migrate?

Sustainable organizations are increasingly assessing their infrastructural environments against the ever-changing collection of business drivers to plan their strategic priorities and operations. Decision makers are seeking efficiencies wherever possible to focus their investments in areas that drive innovation and growth. Under these circumstances, it's easy to understand why so many teams are finding success in leveraging cloud platforms to host their critical workloads. Whether contending with overwhelming security threats, software and hardware refresh cycles, budget and resource constraints, or end-of-life support agreements, the Azure cloud delivers on-demand infrastructure, prioritizes security, and encourages innovation for every facet of your delivery roadmap.

:::image type="content" source="media/concepts-oracle-migration/why-migrate.png" alt-text="Screenshot of top drivers for migrating Oracle to the cloud." lightbox="media/concepts-oracle-migration/why-migrate.png":::

## Why Choose Azure Database for PostgreSQL?

As businesses evolve, database platforms need to keep pace in adopting modern features and capabilities. Modernizing onto Azure Database for PostgreSQL (Azure Postgres) enables organizations to focus on innovation rather than database management, hardware operations, disaster recovery mitigation, and licensing fees. Azure Postgres raises your ability to take advantage of the cloud native infrastructure and encapsulates the key principles of well-architected pillars: cost optimization, operational excellence, performance efficiency, reliability, and security. Azure Postgres additionally embodies extensibility by offering powerful and innovative transactional applications capable of unlocking a variety of critical workloads, such as: time-series based data, geo-spatial capabilities, and cutting-edge generative AI language models and delivering increased performance, decreased cost, all while maintaining complete observability and control over your environment.

Azure Postgres is built upon the official open-source Postgres community builds, ensuring your workloads are compatible with every Postgres release without risk of proprietary dependencies or lock-ins. Our team embraces the open-source community, and we proudly employ the most Postgres contributors who are actively enhancing and maintaining the community Postgres platform.

:::image type="content" source="media/concepts-oracle-migration/azure-postgres-benefits.png" alt-text="Screenshot of examples how Azure builds upon the core benefits of PostgreSQL." lightbox="media/concepts-oracle-migration/azure-postgres-benefits.png":::

## Getting Started

A critical step toward the successful completion of your initiative includes recognition that Oracle migrations are complex operations which require the successful execution of multiple sequential key phases and must be addressed in a specific and structured order. Carefully orchestrating and following these established methodologies and battle-tested processes are essential to achieving success. Our experience and expertise in supporting countless successful migrations can ensure that your migration is able to use and apply our learned lessons within your specific migration scenario. Additionally, there are key solution providers within the Microsoft Partner network offering powerful tools to assist with your migration efforts.

This reference is intended to help identify key migration stages and recommend the ideal set of services and solutions for each stage of your Oracle migration:

:::image type="content" source="media/concepts-oracle-migration/migration-stages.png" alt-text="Migration Stages: Discovery, Assessment, Schema Migration, Code Migration, Data Migration, Application Migration, Performance Tuning, and Cloud Optimization." lightbox="media/concepts-oracle-migration/migration-stages.png":::

## Related content

- [Oracle to Azure PostgreSQL Migration Stages](./concepts-oracle-migration-stages.md)
- [Oracle to Azure PostgreSQL Migration Playbook](https://download.microsoft.com/download/8/f/c/8fc4fe39-7cb1-484a-aaa0-418704b90c0e/Oracle%20to%20Azure%20Postgres%20Migration%20Playbook.pdf)
- [Oracle to Azure PostgreSQL Migration Workarounds](https://github.com/Microsoft/DataMigrationTeam/blob/master/Whitepapers/Oracle%20to%20Azure%20Database%20for%20PostgreSQL%20Migration%20Workarounds.pdf)
- [Azure Database for PostgreSQL Migration Partners](./partners-migration-postgresql.md)
