---
title: Create extensions
description: This article describes how to create extensions in an Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/17/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
# customer intent: As a user, I want to learn how to create extensions in an Azure Database for PostgreSQL flexible server.
---

# Create extensions

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Before creating extensions in Azure Database for PostgreSQL flexible server, you must [allowlist](how-to-allow-extensions.md) them.

## Steps to create extensions

1. [Allowlist](how-to-allow-extensions.md) the extension.

1. If the extension requires it, also add it to `shared_load_libraries`.

1. The user that creates the extensions must be a member of the `azure_pg_admin` role.

1. Run the [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) command to create or install a particular extension. This command loads the packaged objects into your database.

    ```sql
    CREATE EXTENSION <extension>;
    ```

1. Some extensions require other extensions to be created first, because they depend on objects distributed by those other extensions. It's the case, for example, of the `pg_diskann` extension, which has dependencies on the `vector` extension. To install such extensions, you can proceed in two ways:
    - [Allowlist](how-to-allow-extensions.md) and run `CREATE EXTENSION` first on the extension on which it depends. Then, allowlist and run `CREATE EXTENSION` on the dependent extension.

    ```sql
    CREATE EXTENSION <depending_extension>;
    CREATE EXTENSION <dependent_extension>;
    ```

    - [Allowlist](how-to-allow-extensions.md) and run `CREATE EXTENSION` on the dependent extension only, but add the `CASCADE` clause, so that it automatically creates all extensions on which it depends.

    ```sql
    CREATE EXTENSION <dependent_extension> CASCADE;
    ```

> [!NOTE]  
> Third-party extensions offered in Azure Database for PostgreSQL flexible server are open-source licensed code. We don't offer any third-party extensions or extension versions with premium or proprietary licensing models.

Your Azure Database for PostgreSQL flexible server supports a subset of all existing PostgreSQL extensions, as listed in [supported extensions by name](concepts-extensions-versions.md) or in [supported extensions by version of PostgreSQL](concepts-extensions-by-engine.md). 

This information is also available by running `SHOW azure.extensions;`. 

You can't bring your own extensions into Azure Database for PostgreSQL flexible server. Extensions not included in the lists referred before aren't supported on your Azure Database for PostgreSQL flexible server.

## Related content

- [Extensions and modules](concepts-extensions.md)
- [Special considerations with extensions and modules](concepts-extensions-considerations.md)
- [List of extensions and modules by name](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL](concepts-extensions-by-engine.md)
