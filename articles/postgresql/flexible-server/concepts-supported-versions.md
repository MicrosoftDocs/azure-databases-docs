---
title: Supported versions of PostgreSQL
description: Describes the supported major and minor versions of PostgreSQL in Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 09/25/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
ms.custom:
  - ignite-2023
---

# Supported versions of PostgreSQL in Azure Database for PostgreSQL flexible server

Azure Database for PostgreSQL flexible server currently supports the following major versions.

## PostgreSQL version 18 (Preview)

PostgreSQL 18 is now available in **Preview** on Azure Database for PostgreSQL flexible server. The preview is initially limited to the **East Asia** region, with additional regions coming in the following weeks. For a list of new features and improvements, refer to the [PostgreSQL 18 release notes](https://www.postgresql.org/docs/18/release-18.html).

### Limitations with PostgreSQL 18 Preview

- Microsoft Entra ID authentication is not supported in this preview release.  
- Extension availability is limited. Certain PostgreSQL extensions are not supported in the PG18 preview. Refer to the [list of supported extensions](./concepts-extensions.md) for details.  
- Query store and index tuning aren’t supported in this preview release.
- Regional availability is currently restricted to East Asia, with support in other regions planned over the next few weeks.  

These limitations are specific to the preview and will be addressed with the General Availability release of PostgreSQL 18.

## PostgreSQL version 17

The current minor release is **[!INCLUDE [minor-versions-17](includes/minor-version-17.md)]**. Refer to the [!INCLUDE [minor-versions-docs-17](includes/minor-version-docs-17.md)] to learn more about new features and improvements in this latest release. New servers are created with this minor version. 

## PostgreSQL version 16

The current minor release is **[!INCLUDE [minor-versions-16](includes/minor-version-16.md)]**. Refer to the [!INCLUDE [minor-versions-docs-16](includes/minor-version-docs-16.md)] to learn more about improvements and fixes in this release. New servers are created with this minor version. 

## PostgreSQL version 15

The current minor release is **[!INCLUDE [minor-versions-15](includes/minor-version-15.md)]**. Refer to the [!INCLUDE [minor-versions-docs-15](includes/minor-version-docs-15.md)] to learn more about improvements and fixes in this release. New servers are created with this minor version. 

## PostgreSQL version 14

The current minor release is **[!INCLUDE [minor-versions-14](includes/minor-version-14.md)]**. Refer to the [!INCLUDE [minor-versions-docs-14](includes/minor-version-docs-14.md)] to learn more about improvements and fixes in this release. New servers are created with this minor version.

## PostgreSQL version 13

The current minor release is **[!INCLUDE [minor-versions-13](includes/minor-version-13.md)]**. Refer to the [!INCLUDE [minor-versions-docs-13](includes/minor-version-docs-13.md)] to learn more about improvements and fixes in this release. New servers are created with this minor version. 

## PostgreSQL version 12 (retired)

The current minor release is **[!INCLUDE [minor-versions-12](includes/minor-version-12.md)]**. Refer to the [!INCLUDE [minor-versions-docs-12](includes/minor-version-docs-12.md)] to learn more about improvements and fixes in this release. Refer to the [versioning policy](./concepts-version-policy.md#postgresql-12-support) regarding the end-of-life.

## PostgreSQL version 11 (extended support)

The current minor release is **[!INCLUDE [minor-versions-11](includes/minor-version-11.md)]**. Refer to the [!INCLUDE [minor-versions-docs-11](includes/minor-version-docs-11.md)] to learn more about improvements and fixes in this release. Refer to the [versioning policy](./concepts-version-policy.md#postgresql-11-support) regarding the extended support.

## PostgreSQL version 10 and older

We don't support PostgreSQL version 10 and older for Azure Database for PostgreSQL flexible server.

## Managing upgrades

The PostgreSQL project regularly issues minor releases to fix reported bugs. Azure Database for PostgreSQL flexible server automatically patches servers with minor releases during the service's monthly deployments.

It's also possible to do in-place major version upgrades by using the [major version upgrade](concepts-major-version-upgrade.md) feature. This feature greatly simplifies the upgrade process of an instance from a major version (PostgreSQL 11, for example) to any higher supported version (like PostgreSQL 16).

## Supportability and retirement policy of the underlying operating system

Azure Database for PostgreSQL flexible server is a fully managed open-source database. The underlying operating system is an integral part of the service. Microsoft continually works to ensure ongoing security updates and maintenance for security compliance and vulnerability mitigation, whether a partner or an internal vendor provides them. Automatic upgrades during scheduled maintenance help keep your managed database secure, stable, and up to date.

## Managing PostgreSQL engine defects

Microsoft has a team of committers and contributors who work full time on the open-source Postgres project and are long-term members of the community. Our contributions include features, performance enhancements, bug fixes, and security patches, among other things. Our open-source team also incorporates feedback from our Azure fleet (and customers) when prioritizing work. But keep in mind that the Postgres project has its own independent contribution guidelines, review process, and release schedule.

When we identify a defect with PostgreSQL engine, we take immediate action to mitigate the problem. If it requires code change, we fix the defect to address the production issue, if possible. We work with the community to incorporate the fix as quickly as possible.

## Related content

- [Allow extensions](../extensions/how-to-allow-extensions.md).
