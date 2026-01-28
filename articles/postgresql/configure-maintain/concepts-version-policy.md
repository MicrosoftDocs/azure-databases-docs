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
