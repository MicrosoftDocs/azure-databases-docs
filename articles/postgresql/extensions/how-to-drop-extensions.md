---
title: Drop Extensions in Azure Database for PostgreSQL Flexible Server
description: This article describes how to drop extensions in Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to learn how to drop extensions in Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 07/10/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
---

# Drop extensions in Azure Database for PostgreSQL flexible server

Before dropping extensions in Azure Database for PostgreSQL flexible server, [allowlist](how-to-allow-extensions.md) them.

## Steps to drop extensions

1. [Allowlist](how-to-allow-extensions.md) the extension.

1. The user that drops the extensions must be a member of the `azure_pg_admin` role.

1. Run the [DROP EXTENSION](https://www.postgresql.org/docs/current/sql-dropextension.html) command to drop or uninstall a particular extension. This command removes the objects packaged in the extension from your database.

```sql
DROP EXTENSION <extension>;
```

1. Some extensions might distribute objects required by other extensions. For example, the `vector` extension requires the `pg_diskann` extension. To drop such extensions, you can proceed in two ways:
    - [Allowlist](how-to-allow-extensions.md) and run `DROP EXTENSION` on all the extensions that depend on the one that you're trying to drop first. Then, allowlist and run `DROP EXTENSION` on the extension on which other extensions depended.

    ```sql
    DROP EXTENSION <dependent_extension>;
    DROP EXTENSION <depending_extension>;
    ```

    - [Allowlist](how-to-allow-extensions.md) and run `DROP EXTENSION` on the extension that you want to drop, that other extensions depend on, but add the `CASCADE` clause, so that it automatically drops all extensions on which it depends.

    ```sql
    DROP EXTENSION <depending_extension> CASCADE;
    ```

## Related content

- [Extensions and modules](concepts-extensions.md)
- [Special considerations with extensions and modules](concepts-extensions-considerations.md)
- [List of extensions and modules by name](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL](concepts-extensions-by-engine.md)
