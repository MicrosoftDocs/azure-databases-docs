---
title: Update Extensions in Azure Database for PostgreSQL Flexible Server
description: This article describes how to update extensions in Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to learn how to update extensions in Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 07/10/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
---

# Update extensions in Azure Database for PostgreSQL flexible server


Before dropping extensions in an Azure Database for PostgreSQL flexible server, [allowlist](how-to-allow-extensions.md) them.

## Steps to update extensions

To update an installed extension to the latest available version supported by Azure, use the following SQL command:

```sql
ALTER EXTENSION <extension> UPDATE;
```

This command simplifies the management of database extensions by allowing you to manually upgrade to the latest version approved by Azure, enhancing both compatibility and security.

## Limitations

While updating extensions is straightforward, certain limitations exist:

- **Selection of a specific version**: The command doesn't support updating to intermediate versions of an extension.
    - It constantly updates the [latest available version](concepts-extensions-versions.md).

- **Downgrading**: The command doesn't support downgrading an extension to a previous version. If a downgrade is necessary, it might require support assistance and depends on the availability of the previous version.
## Related content

- [Extensions and modules](concepts-extensions.md)
- [Special considerations with extensions and modules](concepts-extensions-considerations.md)
- [List of extensions and modules by name](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL](concepts-extensions-by-engine.md)
