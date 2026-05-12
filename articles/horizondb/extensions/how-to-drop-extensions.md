---
title: Drop Extensions in Azure HorizonDB
description: This article describes how to drop extensions in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
# customer intent: As a user, I want to learn how to drop extensions in Azure HorizonDB.
---

# Drop extensions in Azure HorizonDB

Before dropping extensions in an Azure HorizonDB instance, you must [allowlist](how-to-allow-extensions.md) them.

## Steps to drop extensions

1. [Allow extensions in Azure HorizonDB](how-to-allow-extensions.md) the extension.

1. The user that drops the extensions must be a member of the `azure_pg_admin` role.

1. Run the [DROP EXTENSION](https://www.postgresql.org/docs/current/sql-dropextension.html) command to drop or uninstall a particular extension. This command drops the objects packaged in the extension from your database.

```sql
DROP EXTENSION <extension>;
```

1. Some extensions might distribute objects required by other extension. It's the case, for example, of the `vector` extension, in which the `pg_diskann` extension depends. To drop such extensions, you can proceed in two ways:
   - [Allow extensions in Azure HorizonDB](how-to-allow-extensions.md) and run `DROP EXTENSION` on all the extensions that depend on the one that you're trying to drop first. Then, allowlist and run `DROP EXTENSION` on the extension on which other extensions depended.

   ```sql
   DROP EXTENSION <dependent_extension>;
   DROP EXTENSION <depending_extension>;
   ```

   - [Allow extensions in Azure HorizonDB](how-to-allow-extensions.md) and run `DROP EXTENSION` on the extension that you want to drop, that other extensions depend on, but add the `CASCADE` clause, so that it automatically drops all extensions on which it depends.

   ```sql
   DROP EXTENSION <depending_extension> CASCADE;
   ```

## Related content

- [Extensions and modules in Azure HorizonDB](concepts-extensions.md)
- [Considerations with the use of extensions and modules in Azure HorizonDB](concepts-extensions-considerations.md)
- [List of extensions and modules by name in Azure HorizonDB](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL in Azure HorizonDB](concepts-extensions-by-engine.md)
