---
title: Update Extensions in Azure HorizonDB
description: This article describes how to update extensions in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
# customer intent: As a user, I want to learn how to update extensions in Azure HorizonDB.
---

# Update extensions in Azure HorizonDB

Before dropping extensions in an Azure HorizonDB instance, you must [allowlist](how-to-allow-extensions.md) them.

## Steps to update extensions

To update an installed extension to the latest available version supported by Azure, use the following SQL command:

```sql
ALTER EXTENSION <extension> UPDATE;
```

This command simplifies the management of database extensions by allowing users to manually upgrade to the latest version approved by Azure, enhancing both compatibility and security.

## Limitations

While updating extensions is straightforward, there are certain limitations:

- **Selection of a specific version**: The command doesn't support updating to intermediate versions of an extension.
  - It constantly updates the [latest available version](concepts-extensions-versions.md).

- **Downgrading**: Doesn't support downgrading an extension to a previous version. If a downgrade is necessary, it might require support assistance and depends on the availability of the previous version.

## Related content

- [Extensions and modules in Azure HorizonDB](concepts-extensions.md)
- [Considerations with the use of extensions and modules in Azure HorizonDB](concepts-extensions-considerations.md)
- [List of extensions and modules by name in Azure HorizonDB](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL in Azure HorizonDB](concepts-extensions-by-engine.md)
