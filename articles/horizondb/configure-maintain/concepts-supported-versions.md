---
title: Supported Versions of PostgreSQL in Azure HorizonDB
description: Describes the supported major and minor versions of PostgreSQL in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: concept-article
---

# Supported versions of PostgreSQL in Azure HorizonDB

Azure HorizonDB currently supports the following major versions.

## PostgreSQL version 18

The current minor release is **[!INCLUDE [minor-versions-18](includes/minor-version-18.md)]**. Refer to the [!INCLUDE [minor-versions-docs-18](includes/minor-version-docs-18.md)] to learn more about new features and improvements in this latest release. New servers are created with this minor version.

### Limitations

- Certain PostgreSQL extensions aren't supported in the PG18 release. Refer to the [list of supported extensions](../extensions/concepts-extensions-by-engine.md?pivots=postgresql-18) for details.
- Can't configure server to use new Async I/O `io_method = io_uring`.

## PostgreSQL version 17

The current minor release is **[!INCLUDE [minor-versions-17](includes/minor-version-17.md)]**. Refer to the [!INCLUDE [minor-versions-docs-17](includes/minor-version-docs-17.md)] to learn more about new features and improvements in this latest release. New servers are created with this minor version.

<a id="managing-upgrades"></a>

## Manage upgrades

The PostgreSQL project regularly issues minor releases to fix reported bugs. Azure HorizonDB automatically patches servers with minor releases during the service's monthly deployments.

It's also possible to do in-place major version upgrades by using the [major version upgrade](concepts-major-version-upgrade.md) feature. This feature greatly simplifies the upgrade process of an instance from a major version (PostgreSQL 11, for example) to any higher supported version (like PostgreSQL 16).

## Supportability and retirement policy of the underlying operating system

Azure HorizonDB is a fully managed open-source database. The underlying operating system is an integral part of the service. Microsoft continually works to ensure ongoing security updates and maintenance for security compliance and vulnerability mitigation, whether a partner or an internal vendor provides them. Automatic upgrades during scheduled maintenance help keep your managed database secure, stable, and up to date.

<a id="managing-postgresql-engine-defects"></a>

## Manage PostgreSQL engine defects

Microsoft has a team of committers and contributors who work full time on the open-source Postgres project and are long-term members of the community. Our contributions include features, performance enhancements, bug fixes, and security patches, among other things. Our open-source team also incorporates feedback from our Azure fleet (and customers) when prioritizing work. But keep in mind that the Postgres project has its own independent contribution guidelines, review process, and release schedule.

When we identify a defect with PostgreSQL engine, we take immediate action to mitigate the problem. If it requires code change, we fix the defect to address the production issue, if possible. We work with the community to incorporate the fix as quickly as possible.

## Related content

- [Allow extensions in Azure HorizonDB](../extensions/how-to-allow-extensions.md)
