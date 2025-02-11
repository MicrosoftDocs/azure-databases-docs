---
title: Drop Extensions
description: This article describes how to drop extensions in an Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/07/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
# customer intent: As a user, I want to learn how to drop extensions in an Azure Database for PostgreSQL flexible server.
---

# Drop extensions

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Before dropping extensions in Azure Database for PostgreSQL flexible server, you must [allowlist](how-to-allow-extensions.md) them.

## Steps to drop extensions

1. [Allowlist](how-to-allow-extensions.md) the extension.

1. The user that drops the extensions must be a member of the `azure_pg_admin` role.

1. Run the [DROP EXTENSION](https://www.postgresql.org/docs/current/sql-dropextension.html) command to drop or uninstall a particular extension. This command drops the objects packaged in the extension from your database.

```sql
DROP EXTENSION <extension>;
```

1. Some extensions might distribute objects required by other extension. It's the case, for example, of the `vector` extension, in which the `pg_diskann` extension depends. To drop such extensions, you can proceed in two ways:
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

- [Allow extensions](how-to-allow-extensions.md)
- [Load libraries](how-to-load-libraries.md)
- [Create extensions](how-to-create-extensions.md)
- [Update extensions](how-to-update-extensions.md)
- [View installed extensions](how-to-view-installed-extensions.md)
