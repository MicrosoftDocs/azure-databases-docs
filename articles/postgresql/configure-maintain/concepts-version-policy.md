---
title: Version Policy
description: Describes the policy around Postgres major and minor versions for Azure Database for PostgreSQL flexible server instances.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 01/20/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: concept-article
---

# Azure Database for PostgreSQL version policy

This article describes the Azure Database for PostgreSQL versioning policy.

## Major version

A major version is a change in the first number of the version. For example, PostgreSQL 16 to PostgreSQL 17 is a major version upgrade. Major versions introduce new features and capabilities. They might include changes that require application code updates. Azure Database for PostgreSQL supports each major PostgreSQL version from the date Azure begins offering support until the version reaches end of life (end of support) as defined by the PostgreSQL community. For details, see [PostgreSQL community versioning policy](https://www.postgresql.org/support/versioning/).

### Support policy

The following table provides the retirement details for PostgreSQL major versions. The dates follow the [PostgreSQL community versioning policy](https://www.postgresql.org/support/versioning/).

| PostgreSQL Version | What's New | Azure Standard Support Start Date | Azure Standard Support End Date |
| --- | --- | --- | --- |
| [PostgreSQL 18](https://www.postgresql.org/about/press/) | [Release notes](https://www.postgresql.org/docs/18/release-18.html) | 25-Sep-2025 (Preview) | 14-Nov-2030 |
| [PostgreSQL 17](https://www.postgresql.org/about/news/postgresql-17-released-2936/) | [Release notes](https://www.postgresql.org/docs/17/release-17.html) | 30-Sep-2024 | 8-Nov-2029 |
| [PostgreSQL 16](https://www.postgresql.org/about/news/postgresql-16-released-2715/) | [Release notes](https://www.postgresql.org/docs/16/release-16.html) | 15-Oct-2023 | 9-Nov-2028 |
| [PostgreSQL 15](https://www.postgresql.org/about/news/postgresql-15-released-2526/) | [Release notes](https://www.postgresql.org/docs/15/release-15.html) | 15-May-2023 | 11-Nov-2027 |
| [PostgreSQL 14](https://www.postgresql.org/about/news/postgresql-14-released-2318/) | [Release notes](https://www.postgresql.org/docs/14/release-14.html) | 29-Jun-2022 | 12-Nov-2026 |
| [PostgreSQL 13](https://www.postgresql.org/about/news/postgresql-13-released-2077/) | [Release notes](https://www.postgresql.org/docs/13/release-13.html) | 25-May-2021 | 31-Mar-2026 |
| [PostgreSQL 12](https://www.postgresql.org/about/news/postgresql-12-released-1976/) | [Release notes](https://www.postgresql.org/docs/12/release-12.html) | 22-Sep-2020 | 31-Mar-2026 |
| [PostgreSQL 11](https://www.postgresql.org/about/news/postgresql-11-released-1894/) | [Release notes](https://www.postgresql.org/docs/11/release-11.html) | 24-Jul-2019 | 31-Mar-2026 |

PostgreSQL 18 is currently available in **Preview** on Azure Database for PostgreSQL with initial availability in the East Asia region.

## Minor version support

An Azure Database for PostgreSQL flexible server instance automatically upgrades minor versions to the Azure preferred PostgreSQL version during periodic maintenance.

## Extended Support

To help you maintain secure and compliant workloads beyond community end-of-life (end of support), Azure is introducing Extended Support for Azure Database for PostgreSQL.

Extended Support gives you continued access to critical security updates and technical assistance. With Extended Support, you have time to plan and implement your upgrade strategy with confidence.

Extended support provides:

- Up to three extra years of support after standard support ends
- Security patches and critical bug fixes
- Technical support through Azure Support channels (per your existing plan)

> [!NOTE]  
> Extended Support doesn't include new feature releases, performance enhancements, or support for minor version upgrades.

### Why use Extended Support?

Extended Support is ideal for customers who...

- Need more time to upgrade complex workloads.
- Require compliance and security coverage during upgrade planning.
- Depend on uninterrupted technical support for critical environments.

### Best practices

- Treat Extended Support as a temporary bridge, not a long-term solution.
- Start upgrade planning well before the end-of-life (end of support) date.
- Consider upgrading to newer versions such as PostgreSQL 15 or 16 for improved performance and support.

### Eligible PostgreSQL versions

| PostgreSQL Version | Azure Standard Support Start Date | Community Retirement Date | Azure Standard Support End Date | Paid Extended Support Start Date | Paid Extended Support End Date |
| --- | --- | --- | --- | --- | --- |
| 11 | July 24, 2019 | November 9, 2023 | March 31, 2026 | April 1, 2026 | November 8, 2026 |
| 12 | September 22, 2020 | November 14, 2024 | March 31, 2026 | April 1, 2026 | November 13, 2027 |
| 13 | May 25, 2021 | November 13, 2025 | March 31, 2026 | April 1, 2026 | November 12, 2028 |
| 14 | June 29, 2022 | November 12, 2026 | December 11, 2026 | December 12, 2026 | November 11, 2029 |

### Enrollment and price

- Automatic Enrollment: PostgreSQL servers running unsupported versions are automatically enrolled in Extended Support on March 1, 2026.
- Opt-Out Option: You can opt out at any time by upgrading to a supported version.
- Grace Period: A one-month grace period applies. Billing begins on April 1, 2026.
- Pricing: Details are published on this [page](https://azure.microsoft.com/pricing/details/postgresql/flexible-server/?cdn=disable) before billing begins.

### Frequently asked questions (FAQs)

**Q: What if I want to keep running without extended support? Can I opt out?**

A: No.

**Q: What happens if I continue running an unsupported PostgreSQL version on Azure after its community end of support?**

A: Your server is automatically enrolled in Extended Support one month after the community end of support date (or on March 1, 2026, for versions 11, 12, and 13).

**Q: Can I continue using my PostgreSQL instance without Extended Support?**

A: Yes, but after the grace period, you're automatically enrolled in paid Extended Support unless you upgrade to a supported version. During the grace period, you assume full operational risk, and Microsoft support can't guarantee issue resolution.

**Q: Can my applications break during a major version upgrade?**

A. PostgreSQL major version upgrades can introduce changes that might affect your application—such as deprecated configuration parameters, incompatible extensions, or SQL behavior differences. We recommend validating upgrades in a nonproduction environment before applying them in production. For more details, review the key considerations and limitations in [Major Version Upgrades](./concepts-major-version-upgrade.md) docs.

[!INCLUDE [supported-upgrades](includes/supported-upgrades.md)]

**Q: How do I know if my server is in Extended Support?**

A: The Azure portal and CLI clearly indicate if a server is enrolled in Extended Support.

**Q: Do I need to update Server Parameters post major version upgrades?**

A: No manual change is required. The upgrade workflow will automatically update the parameters for the new PostgreSQL Version.

**Q: Are PostgreSQL extensions automatically upgraded during a major version upgrade?**

A: No. While Azure upgrades the database engine, noncore extensions (for example, pgvector, timescaledb) require manual updates. Use `ALTER EXTENSION ... UPDATE` or recreate unsupported extensions after the upgrade.

**Q: How can I reduce downtime during a major upgrade?**

A: To minimize downtime:
- Plan upgrades during low-traffic hours.
- Identify and fix any upgrade blockers (for example, extensions, roles, replication slots) ahead of the upgrade.
- Pause background jobs and long-running sessions.
- Temporarily scale up compute to speed up pg_upgrade.
- Clean up bloat with VACUUM or REINDEX if needed.
- Run ANALYZE after upgrade to restore performance.

**Q: Where can I track which of my servers are nearing end of support?**

A: Azure provides visibility through the portal.

**Q: What support options are available during the Extended Support phase?**

A: Servers in Extended Support can raise support cases for security-related issues only. Feature requests, performance tuning, and general bug fixes aren't supported for end of support versions. Improvements to existing features for end of support versions won't be backported.

**Q: How will the period between November 13, 2025, and March 1, 2026, be handled for PostgreSQL version 13? Will support be continued during this time? How will it differ from the period before November 13, 2025?**

A: According to the [PostgreSQL community versioning policy](https://www.postgresql.org/support/versioning/), each major version is supported until retired by the community. Free Extended support from Azure will be provided through March 31, 2026. Customers are charged for Extended Support starting April 1. To ensure continued support and access to new features, upgrade to newer versions.

## Retired PostgreSQL engine versions not supported in Azure Database for PostgreSQL

You can continue to use the retired version in Azure Database for PostgreSQL flexible server instances. However, after the retirement date for each PostgreSQL database version, the following restrictions apply:

- When the community retires a PostgreSQL version, Azure Database for PostgreSQL stops applying bug or security patches to the database engine. This change might expose your server to security risks or other issues. However, Azure continues to maintain and patch the underlying host, operating system, containers, and related service components.

- If you experience a support issue that relates to the PostgreSQL engine itself, we might not be able to provide support because the community no longer provides the patches. In such cases, you need to upgrade your database to one of the supported versions.

- You can't create new servers by using a PostgreSQL version that is retired. However, you can perform point-in-time recoveries and create read replicas for your existing servers.

- New service capabilities developed by Azure Database for PostgreSQL server might only be available to supported database server versions.

- Uptime SLAs apply solely to Azure Database for PostgreSQL flexible server instance service-related issues and don't apply to any downtime caused by database engine-related bugs.

- In rare cases where a critical vulnerability in a retired PostgreSQL version poses a threat to the service, Azure might stop affected servers to protect the platform. In such cases, you're notified to upgrade the server before bringing the server online.

- New extensions introduced for Azure Database for PostgreSQL flexible server instances aren't supported on PostgreSQL versions that the community retired.

## PostgreSQL version syntax

Before PostgreSQL version 10, the [PostgreSQL versioning policy](https://www.postgresql.org/support/versioning/) considered a major version upgrade to be an increase in the first or second number. For example, 9.5 to 9.6 was considered as a major version upgrade. As of version 10, only a change in the first number is considered as a major version upgrade. For example, 10.0 to 10.1 is a minor release upgrade. Version 10 to 11 is a major version upgrade.

## Related content

- [Supported versions of PostgreSQL in Azure Database for PostgreSQL](concepts-supported-versions.md)
