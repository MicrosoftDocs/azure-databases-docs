---
title: Versioning policy
description: Describes the policy around Postgres major and minor versions in Azure Database for PostgreSQL - Single Server and Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 6/29/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Azure Database for PostgreSQL flexible server versioning policy

[!INCLUDE [applies-to-postgresql-flexible-server](../includes/applies-to-postgresql-flexible-server.md)]

[!INCLUDE [azure-database-for-postgresql-single-server-deprecation](../includes/azure-database-for-postgresql-single-server-deprecation.md)]

This page describes the Azure Database for PostgreSQL flexible server versioning policy, and is applicable to these deployment modes:

* Azure Database for PostgreSQL single server
* Azure Database for PostgreSQL flexible server

## Supported PostgreSQL versions

Azure Database for PostgreSQL flexible server supports the following database versions.

| Version | Azure Database for PostgreSQL single server | Azure Database for PostgreSQL flexible server |
| ----- | :------: | :----: |
| PostgreSQL 17 |   | X |
| PostgreSQL 16 |   | X |
| PostgreSQL 15 |   | X |
| PostgreSQL 14 |   | X |
| PostgreSQL 13 |   | X |
| PostgreSQL 12 (retired)* |   | See [policy](#postgresql-12-support) |
| PostgreSQL 11 | X | X |
| *PostgreSQL 10 (retired)* | See [policy](#retired-postgresql-engine-versions-not-supported-in-azure-database-for-postgresql-flexible-server) |  |
| *PostgreSQL 9.6 (retired)* | See [policy](#retired-postgresql-engine-versions-not-supported-in-azure-database-for-postgresql-flexible-server) |  |
| *PostgreSQL 9.5 (retired)* | See [policy](#retired-postgresql-engine-versions-not-supported-in-azure-database-for-postgresql-flexible-server) |  |

## Major version support

Azure Database for PostgreSQL - Flexible server supports each major PostgreSQL version from the date Azure begins offering support until the version reaches end of life (EOL) as defined by the PostgreSQL community. For details, see [PostgreSQL community versioning policy](https://www.postgresql.org/support/versioning/).

## Minor version support

Azure Database for PostgreSQL flexible server automatically performs minor version upgrades to the Azure preferred PostgreSQL version as part of periodic maintenance.

## Major version retirement policy

The table below provides the retirement details for PostgreSQL major versions. The dates follow the [PostgreSQL community versioning policy](https://www.postgresql.org/support/versioning/).

| Version                                                                                                                     | What's New                                                       | Azure support start date | Retirement date (Azure) |
| --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------ | ----------------------- |
| [PostgreSQL 17](https://www.postgresql.org/about/news/postgresql-17-released-2936/)                                         | [Features](https://www.postgresql.org/docs/17/release-17.html)   | 30-Sep-24                | 8-Nov-29                |
| [PostgreSQL 16](https://www.postgresql.org/about/news/postgresql-16-released-2715/)                                         | [Features](https://www.postgresql.org/docs/16/release-16.html)   | 15-Oct-23                | 9-Nov-28                |
| [PostgreSQL 15](https://www.postgresql.org/about/news/postgresql-15-released-2526/)                                         | [Features](https://www.postgresql.org/docs/15/release-15.html)   | 15-May-23                | 11-Nov-27               |
| [PostgreSQL 14](https://www.postgresql.org/about/news/postgresql-14-released-2318/)                                         | [Features](https://www.postgresql.org/docs/14/release-14.html)   | 29-Jun-22                | 12-Nov-26               |
| [PostgreSQL 13](https://www.postgresql.org/about/news/postgresql-13-released-2077/)                                         | [Features](https://www.postgresql.org/docs/13/release-13.html)   | 25-May-21                | 13-Nov-25               |
| [PostgreSQL 12 (retired)](https://www.postgresql.org/about/news/postgresql-12-released-1976/)                               | [Features](https://www.postgresql.org/docs/12/release-12.html)   | 22-Sep-20                | 14-Nov-24               |
| [PostgreSQL 11](https://www.postgresql.org/about/news/postgresql-11-released-1894/)                                         | [Features](https://www.postgresql.org/docs/11/release-11.html)   | 24-Jul-19                | 9-Nov-25                |
| [PostgreSQL 10 (retired)](https://www.postgresql.org/about/news/postgresql-10-released-1786/)                               | [Features](https://wiki.postgresql.org/wiki/New_in_postgres_10)  | 4-Jun-18                 | 10-Nov-22               |
| [PostgreSQL 9.5 (retired)](https://www.postgresql.org/about/news/postgresql-132-126-1111-1016-9621-and-9525-released-2165/) | [Features](https://www.postgresql.org/docs/9.5/release-9-5.html) | 18-Apr-18                | 11-Feb-21               |
| [PostgreSQL 9.6 (retired)](https://www.postgresql.org/about/news/postgresql-96-released-1703/)                              | [Features](https://wiki.postgresql.org/wiki/NewIn96)             | 18-Apr-18                | 11-Nov-21               |

## Extended Support

To help customers maintain secure and compliant workloads beyond community end-of-life (EOL), Azure is introducing Extended Support for Azure Database for PostgreSQL.

Extended Support offers continued access to critical security updates and technical assistance, giving you time to plan and implement your upgrade strategy with confidence.

__What is Extended Support?__

Extended Support provides:

- __Up to 3 additional years__ of support after standard support ends

- __Security patches and critical bug fixes__

- __Technical support via Azure Support channels__ (per your existing plan)

__Note__: Extended Support doesn't include new feature releases, performance enhancements, or support for minor version upgrades.

__Eligible PostgreSQL Versions__

| PostgreSQL Version | Azure Support Start Date | Community Retirement Date | Paid Extended Support Starts (includes grace period) | Extended Support Ends |
|--------------------|-------------------------|--------------------------|-----------------------------------------------------|----------------------|
| 11                 | 24-Jul-19               | 9-Nov-25                 | 1-Apr-26                                            | 31-Mar-29            |
| 12                 | 22-Sep-20               | 14-Nov-24                | 1-Apr-26                                            | 31-Mar-29            |
| 13                 | 25-May-21               | 13-Nov-25                | 1-Apr-26                                            | 31-Mar-29            |

 __Enrollment & Pricing__
 
- Automatic Enrollment: PostgreSQL servers running unsupported versions are automatically enrolled in Extended Support on March 1, 2026.
- Opt-Out Option: You can opt out at any time by upgrading to a supported version.
- Grace Period: A one-month grace period applies. Billing begins on April 1, 2026.
- Pricing: Details are published on this [page](https://azure.microsoft.com/pricing/details/postgresql/flexible-server/?cdn=disable) before billing begins.

__Why Use Extended Support?__

Extended Support is ideal for customers who: 
- Need more time to upgrade complex workloads.
- Require compliance and security coverage during upgrade planning.
- Depend on uninterrupted technical support for critical environments.

__Best Practices__
- Treat Extended Support as a temporary bridge, not a long-term solution.
- Begin upgrade planning well before the end-of-life (EOL) date.
- Consider upgrading to newer versions such as PostgreSQL 15 or 16 for improved performance and support.

__FAQ__

__Q: What happens if I continue running an unsupported PostgreSQL version on Azure after its community EOL?__

_A: Your server is automatically enrolled in Extended Support one month after the community EOL date (or on March 1, 2026, for versions 11, 12, and 13)._

__Q: Can I continue using my PostgreSQL instance without Extended Support?__

_A: Yes, but after the grace period, you're automatically enrolled in paid Extended Support unless you upgrade to a supported version. During the grace period, you assume full operational risk, and Microsoft support can't guarantee issue resolution._

__Q: Will my applications break during a major version upgrade?__

_A: Azure provides Pre-Upgrade Validation Checks (PVC) to identify common issues such as extension compatibility and parameter conflicts. We recommend testing upgrades in non-production environments. Azure is also investing in Blue/Green deployments to enable near-zero-downtime upgrades._

__Q: How will I know if my server is in Extended Support?__

_A: The Azure portal and CLI clearly indicate if a server is enrolled in Extended Support._ 

__Q: Do I need to update Server Parameter Groups post major version upgrades?__

_A: Yes. Major PostgreSQL versions often introduce or deprecate configuration parameters. Create a new parameter group for the target version and adjust memory and performance settings as needed._

__Q: Are PostgreSQL extensions automatically upgraded during a major version upgrade?__

_A: No. While Azure upgrades the database engine, noncore extensions (for example, pgvector, timescaledb) require manual updates. Use ALTER EXTENSION ... UPDATE or recreate unsupported extensions after the upgrade._

__Q: How can I reduce downtime during a major upgrade?__

_A: To minimize downtime:_
- Apply pending maintenance before the upgrade.
- Take a manual backup just before the upgrade to speed up snapshot creation.
- Schedule upgrades during low-traffic periods.
- Monitor replication lag and connections if using Blue/Green deployment.
- 
 __Q: Where can I track which of my servers are nearing EOL?__

_A:_ Azure provides visibility through the Portal.

__Q: What support options are available during the Extended Support phase?__

_A:_ Servers in Extended Support can raise support cases for security-related issues only. Feature requests, performance tuning, and general bug fixes aren't supported for EOL versions.

## PostgreSQL 11 support

Azure is extending PostgreSQL 11 support for Azure Database for PostgreSQL flexible server. This extended support timeline is designed to provide more time for users to plan and [migrate from Azure Database for PostgreSQL single server to flexible server](../migrate/concepts-single-to-flexible.md) and to upgrade to higher PostgreSQL versions. The extended support timeline is designed to facilitate a smooth transition for users currently relying on PostgreSQL 11.

## PostgreSQL 12 support

PostgreSQL 12 reached its end of life on **November 14, 2024**, in line with the PostgreSQL community [versioning policy](https://www.postgresql.org/support/versioning/). According to this policy, each major version is supported until retired by the community. Unlike PostgreSQL 11, which has extended support until November 9, 2025, PostgreSQL 12 doesn't receive extended support from Azure. Users are encouraged to upgrade to newer versions to ensure continued support and access to new features.

### Single Server Support:
- Until March 28, 2025, users can continue to create and utilize PostgreSQL 11 servers on the Azure Database for PostgreSQL Single Server, except for creation through the Azure portal. It's important to note that other [restrictions](#retired-postgresql-engine-versions-not-supported-in-azure-database-for-postgresql-flexible-server) associated with retired PostgreSQL engines still apply.
- Azure provides updates incorporating minor versions provided by the PostgreSQL community for PostgreSQL 11 servers until November 9, 2023.

### Flexible Server Support
- You can create and operate PostgreSQL 11 servers on Azure Database for PostgreSQL Flexible Server until November 9, 2025. 

- Updates with PostgreSQL community provided minor versions are available for PostgreSQL 11 servers until November 9, 2023.

- Beginning November 9, 2023, to November 9, 2025, while users can continue using and creating new instances of PostgreSQL 11 on the Flexible Server, they'll be subject to the [restrictions](#retired-postgresql-engine-versions-not-supported-in-azure-database-for-postgresql-flexible-server) of other retired PostgreSQL engines.

This extension of Postgres 11 support is part of Azure's commitment to providing a seamless migration path and ensuring continued functionality for users.

## Retired PostgreSQL engine versions not supported in Azure Database for PostgreSQL flexible server

You might continue to run the retired version in Azure Database for PostgreSQL flexible server. However, note the following restrictions after the retirement date for each PostgreSQL database version:
- Once a PostgreSQL version is retired by the community, Azure Database for PostgreSQL – Flexible Server no longer applies bug or security patches to the database engine. This may expose your server to security risks or other issues. However, Azure continues to maintain and patch the underlying host, operating system, containers, and related service components.

- If any support issue you might experience relates to the PostgreSQL engine itself, as the community no longer provides the patches, we might not be able to provide you with support. In such cases, you have to upgrade your database to one of the supported versions.
- You cannot create new servers using a PostgreSQL version that has been retired. However, you're able to perform point-in-time recoveries and create read replicas for your existing servers.

- New service capabilities developed by Azure Database for PostgreSQL flexible server might only be available to supported database server versions.
- Uptime SLAs apply solely to Azure Database for PostgreSQL flexible server service-related issues and not to any downtime caused by database engine-related bugs.  
- In rare cases where a critical vulnerability in a retired PostgreSQL version poses a threat to the service, Azure may stop affected servers to protect the platform. In such case, you're notified to upgrade the server before bringing the server online.

- New extensions introduced for Azure Database for PostgreSQL – Flexible Server are not supported on PostgreSQL versions that have been retired by the community.

## PostgreSQL version syntax

Before PostgreSQL version 10, the [PostgreSQL versioning policy](https://www.postgresql.org/support/versioning/) considered a _major version_ upgrade to be an increase in the first _or_ second number. For example, 9.5 to 9.6 was considered a _major_ version upgrade. As of version 10, only a change in the first number is considered a major version upgrade. For example, 10.0 to 10.1 is a _minor_ release upgrade. Version 10 to 11 is a _major_ version upgrade.

## Related content

- [Supported versions of PostgreSQL in Azure Database for PostgreSQL flexible server](concepts-supported-versions.md).
