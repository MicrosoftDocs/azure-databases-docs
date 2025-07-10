---
title: Version Policy
description: Describes the policy around Postgres major and minor versions in Azure Database for PostgreSQL - Single Server and Azure Database for PostgreSQL flexible server.
author: andtapia
ms.author: andreatapia
ms.reviewer: varundhawan, maghan
ms.date: 07/01/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Azure Database for PostgreSQL version policy

This page describes the Azure Database for PostgreSQL flexible server versioning policy.

## Supported PostgreSQL versions

Azure Database for PostgreSQL flexible server supports the following database versions.

| Version | Supported | Policy information |
| --- | --- | --- |
| PostgreSQL 17 | Yes | N/A |
| PostgreSQL 16 | Yes | N/A |
| PostgreSQL 15 | Yes | N/A |
| PostgreSQL 14 | Yes | N/A |
| PostgreSQL 13 | Yes | N/A |
| PostgreSQL 12 | No (retired) | [Policy](#postgresql-12-support) |
| PostgreSQL 11 | Yes | N/A |
| PostgreSQL 10 | No (retired) | [Policy](#retired-postgresql-engine-versions-not-supported-in-azure-database-for-postgresql) |
| PostgreSQL 9.6 | No (retired) | [Policy](#retired-postgresql-engine-versions-not-supported-in-azure-database-for-postgresql) |
| PostgreSQL 9.5 | No (retired) | [Policy](#retired-postgresql-engine-versions-not-supported-in-azure-database-for-postgresql) |

## Major version

A major version is a change in the first number of the version. For example, PostgreSQL 10 to PostgreSQL 11 is a major version upgrade. Major versions introduce new features and capabilities, and might include changes that require application code updates.

### Support

Azure Database for PostgreSQL supports each major PostgreSQL version from the date Azure begins offering support until the version reaches end of life (end of support) as defined by the PostgreSQL community. For details, see [PostgreSQL community versioning policy](https://www.postgresql.org/support/versioning/).

### Retirement policy

The table below provides the retirement details for PostgreSQL major versions. The dates follow the [PostgreSQL community versioning policy](https://www.postgresql.org/support/versioning/).

| PostgreSQL Version | What's New | Azure Support Start Date | Azure Retirement Date |
| --- | --- | --- | --- |
| [PostgreSQL 17](https://www.postgresql.org/about/news/postgresql-17-released-2936/) | [Release notes](https://www.postgresql.org/docs/17/release-17.html) | 30-Sep-2024 | 8-Nov-2029 |
| [PostgreSQL 16](https://www.postgresql.org/about/news/postgresql-16-released-2715/) | [Release notes](https://www.postgresql.org/docs/16/release-16.html) | 15-Oct-2023 | 9-Nov-2028 |
| [PostgreSQL 15](https://www.postgresql.org/about/news/postgresql-15-released-2526/) | [Release notes](https://www.postgresql.org/docs/15/release-15.html) | 15-May-2023 | 11-Nov-2027 |
| [PostgreSQL 14](https://www.postgresql.org/about/news/postgresql-14-released-2318/) | [Release notes](https://www.postgresql.org/docs/14/release-14.html) | 29-Jun-2022 | 12-Nov-2026 |
| [PostgreSQL 13](https://www.postgresql.org/about/news/postgresql-13-released-2077/) | [Release notes](https://www.postgresql.org/docs/13/release-13.html) | 25-May-2021 | 13-Nov-2025 |
| [PostgreSQL 12 (retired)](https://www.postgresql.org/about/news/postgresql-12-released-1976/) | [Release notes](https://www.postgresql.org/docs/12/release-12.html) | 22-Sep-2020 | 14-Nov-2024 |
| [PostgreSQL 11](https://www.postgresql.org/about/news/postgresql-11-released-1894/) | [Release notes](https://www.postgresql.org/docs/11/release-11.html) | 24-Jul-2019 | 9-Nov-2025 |
| [PostgreSQL 10 (retired)](https://www.postgresql.org/about/news/postgresql-10-released-1786/) | [Release notes](https://wiki.postgresql.org/wiki/New_in_postgres_10) | 4-Jun-2018 | 10-Nov-2022 |
| [PostgreSQL 9.6 (retired)](https://www.postgresql.org/about/news/postgresql-96-released-1703/) | [Release notes](https://wiki.postgresql.org/wiki/NewIn96) | 18-Apr-2018 | 11-Nov-2021 |
| [PostgreSQL 9.5 (retired)](https://www.postgresql.org/about/news/postgresql-132-126-1111-1016-9621-and-9525-released-2165/) | [Release notes](https://www.postgresql.org/docs/9.5/release-9-5.html) | 18-Apr-2018 | 11-Feb-2021 |

## Minor version support

Azure Database for PostgreSQL flexible server automatically performs minor version upgrades to the Azure preferred PostgreSQL version as part of periodic maintenance.

## Extended Support

To help customers maintain secure and compliant workloads beyond community end-of-life (end of support), Azure is introducing Extended Support for Azure Database for PostgreSQL.

Extended Support offers continued access to critical security updates and technical assistance, giving you time to plan and implement your upgrade strategy with confidence.

Extended support provides:

- Up to three additional years of support after standard support ends
- Security patches and critical bug fixes
- Technical support via Azure Support channels (per your existing plan)

> [!NOTE]  
> Extended Support doesn't include new feature releases, performance enhancements, or support for minor version upgrades.

### Why use Extended Support?

Ideal for customers who...

- Need more time to upgrade complex workloads.
- Require compliance and security coverage during upgrade planning.
- Depend on uninterrupted technical support for critical environments.

Best Practices

- Treat Extended Support as a temporary bridge, not a long-term solution.
- Begin upgrade planning well before the end-of-life (end of support) date.
- Consider upgrading to newer versions such as PostgreSQL 15 or 16 for improved performance and support.

### Eligible PostgreSQL versions

| PostgreSQL Version | Azure Support Start Date | Community Retirement Date | Paid Extended Support Starts (includes grace period) | Extended Support Ends |
| --- | --- | --- | --- | --- |
| 11 | 24-Jul-19 | 9-Nov-25 | 1-Apr-26 | 31-Mar-29 |
| 12 | 22-Sep-20 | 14-Nov-24 | 1-Apr-26 | 31-Mar-29 |
| 13 | 25-May-21 | 13-Nov-25 | 1-Apr-26 | 31-Mar-29 |

### Enrollment and price

- Automatic Enrollment: PostgreSQL servers running unsupported versions are automatically enrolled in Extended Support on March 1, 2026.
- Opt-Out Option: You can opt out at any time by upgrading to a supported version.
- Grace Period: A one-month grace period applies. Billing begins on April 1, 2026.
- Pricing: Details are published on this [page](https://azure.microsoft.com/pricing/details/postgresql/flexible-server/?cdn=disable) before billing begins.

### Frequently asked questions (FAQs)

**Q: What happens if I continue running an unsupported PostgreSQL version on Azure after its community end of support?**

A: Your server is automatically enrolled in Extended Support one month after the community end of support date (or on March 1, 2026, for versions 11, 12, and 13).

**Q: Can I continue using my PostgreSQL instance without Extended Support?**

A: Yes, but after the grace period, you're automatically enrolled in paid Extended Support unless you upgrade to a supported version. During the grace period, you assume full operational risk, and Microsoft support can't guarantee issue resolution.

**Q: Can my applications break during a major version upgrade?**

A: Azure provides pre-upgrade validation checks (PVC) to identify common issues such as extension compatibility and parameter conflicts. We recommend testing upgrades in nonproduction environments. Azure is also investing in Blue/Green deployments to enable near-zero-downtime upgrades.

**Q: How do I know if my server is in Extended Support?**

A: The Azure portal and CLI clearly indicate if a server is enrolled in Extended Support.

**Q: Do I need to update Server Parameter Groups post major version upgrades?**

A: Yes. Major PostgreSQL versions often introduce or deprecate configuration parameters. Create a new parameter group for the target version and adjust memory and performance settings as needed.

**Q: Are PostgreSQL extensions automatically upgraded during a major version upgrade?**

A: No. While Azure upgrades the database engine, noncore extensions (for example, pgvector, timescaledb) require manual updates. Use ALTER EXTENSION ... UPDATE or recreate unsupported extensions after the upgrade.

**Q: How can I reduce downtime during a major upgrade?**

A: To minimize downtime:
- Apply pending maintenance before the upgrade.
- Take a manual backup just before the upgrade to speed up snapshot creation.
- Schedule upgrades during low-traffic periods.
- Monitor replication lag and connections if using Blue/Green deployment.

**Q: Where can I track which of my servers are nearing end of support?**

A: Azure provides visibility through the Portal.

**Q: What support options are available during the Extended Support phase?**

A: Servers in Extended Support can raise support cases for security-related issues only. Feature requests, performance tuning, and general bug fixes aren't supported for end of support versions. Improvements to existing features for end of support versions will not be backported. 

**Q:** **How will the period between November 13, 2025, and March 1, 2026, be handled for PostgreSQL version 13? Will support be continued during this time? How will it differ from the period before November 13, 2025**?

A: According to the [PostgreSQL community versioning policy](https://www.postgresql.org/support/versioning/), each major version is supported until retired by the community. Extended support from Azure will not be provided  between November 13, 2025 - March 1, 2026. Customers are charged for Extended Support starting April 1. Users are encouraged to upgrade to newer versions to ensure continued support and access to new features.

## PostgreSQL 12 support

PostgreSQL 12 reached its end of life on **November 14, 2024**, in line with the PostgreSQL community [versioning policy](https://www.postgresql.org/support/versioning/). According to this policy, each major version is supported until retired by the community. Unlike PostgreSQL 11, which has extended support until November 9, 2025, PostgreSQL 12 doesn't receive extended support from Azure until March 1, 2026. Users are encouraged to upgrade to newer versions to ensure continued support and access to new features.

## PostgreSQL 11 support

Azure is extending PostgreSQL 11 support for Azure Database for PostgreSQL flexible server. This extended support timeline is designed to provide more time for users to plan and [migrate from Azure Database for PostgreSQL single server to flexible server](../migrate/concepts-single-to-flexible.md) and to upgrade to higher PostgreSQL versions. The extended support timeline is designed to facilitate a smooth transition for users currently relying on PostgreSQL 11.

### Flexible server support

- You can create and operate PostgreSQL 11 servers on Azure Database for PostgreSQL flexible Server, until November 9, 2025, when Azure stops supporting PostgreSQL 11.
- From November 9, 2023, to November 9, 2025, while users can continue using and creating new instances of PostgreSQL 11 on the flexible server, they're [restrictions](#retired-postgresql-engine-versions-not-supported-in-azure-database-for-postgresql) of other retired PostgreSQL engines.

This extension of Postgres 11 support is part of Azure's commitment to providing a seamless migration path and ensuring continued functionality for users.

## Retired PostgreSQL engine versions not supported in Azure Database for PostgreSQL

You might continue to run the retired version in Azure Database for PostgreSQL flexible server. However, note the following restrictions after the retirement date for each PostgreSQL database version:

- Once a PostgreSQL version is retired by the community, Azure Database for PostgreSQL – Flexible Server no longer applies bug or security patches to the database engine. This might expose your server to security risks or other issues. However, Azure continues to maintain and patch the underlying host, operating system, containers, and related service components.

- If any support issue you might experience relates to the PostgreSQL engine itself, as the community no longer provides the patches, we might not be able to provide you with support. In such cases, you have to upgrade your database to one of the supported versions.

- You can't create new servers using a PostgreSQL version that has been retired. However, you're able to perform point-in-time recoveries and create read replicas for your existing servers.

- New service capabilities developed by Azure Database for PostgreSQL flexible server might only be available to supported database server versions.

- Uptime SLAs apply solely to Azure Database for PostgreSQL flexible server service-related issues and not to any downtime caused by database engine-related bugs.

- In rare cases where a critical vulnerability in a retired PostgreSQL version poses a threat to the service, Azure might stop affected servers to protect the platform. In such case, you're notified to upgrade the server before bringing the server online.

- New extensions introduced for Azure Database for PostgreSQL – Flexible Server aren't supported on PostgreSQL versions that have been retired by the community.

## PostgreSQL version syntax

Before PostgreSQL version 10, the [PostgreSQL versioning policy](https://www.postgresql.org/support/versioning/) considered a major version upgrade to be an increase in the first or second number. For example, 9.5 to 9.6 was considered as a major version upgrade. As of version 10, only a change in the first number is considered as a major version upgrade. For example, 10.0 to 10.1 is a minor release upgrade. Version 10 to 11 is a major version upgrade.

## Related content

- [Supported versions of PostgreSQL in Azure Database for PostgreSQL flexible server](concepts-supported-versions.md)
