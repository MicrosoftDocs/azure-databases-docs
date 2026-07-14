---
title: Create Extensions in Azure HorizonDB
description: This article describes how to create extensions in Azure HorizonDB.
#customer intent: As a user, I want to create extensions in my Azure HorizonDB cluster, so that I can extend the functionality of my PostgreSQL database.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 07/06/2026
ms.service: azure-horizondb
ms.subservice: extensions-modules
ms.topic: how-to
---

# Create extensions in Azure HorizonDB (Preview)

Before creating extensions in an Azure HorizonDB cluster, you must [allowlist](how-to-allow-extensions.md) them.

## Steps to create extensions

1. [Allow extensions in Azure HorizonDB (Preview)](how-to-allow-extensions.md) the extension.

1. If the extension requires it, also add it to `shared_load_libraries`.

1. To create untrusted extensions, you must be a member of the `azure_pg_admin` role. Any user with `CREATE` privilege can create any trusted extension listed in `azure.extensions`. You can retrieve this list by running `SHOW azure.extensions;`.

1. Run the [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) command to create or install a particular extension. This command loads the packaged objects into your database.

   ```sql
   CREATE EXTENSION <extension>;
   ```

1. Some extensions require other extensions to be created first, because they depend on objects distributed by those other extensions. It's the case, for example, of the `pg_diskann` extension, which has dependencies on the `vector` extension. To install such extensions, you can proceed in two ways:
   - [Allow extensions in Azure HorizonDB (Preview)](how-to-allow-extensions.md) and run `CREATE EXTENSION` first on the extension on which it depends. Then, allowlist and run `CREATE EXTENSION` on the dependent extension.

   ```sql
   CREATE EXTENSION <depending_extension>;
   CREATE EXTENSION <dependent_extension>;
   ```

   - [Allow extensions in Azure HorizonDB (Preview)](how-to-allow-extensions.md) and run `CREATE EXTENSION` on the dependent extension only, but add the `CASCADE` clause, so that it automatically creates all extensions on which it depends.

   ```sql
   CREATE EXTENSION <dependent_extension> CASCADE;
   ```

> [!NOTE]  
> Third-party extensions offered for Azure HorizonDB are open-source licensed code. Microsoft doesn't offer any third-party extensions or extension versions with premium or proprietary licensing models.

Your Azure HorizonDB instance supports a subset of all existing PostgreSQL extensions, as listed in [supported extensions by name](concepts-extensions-versions.md) or in [supported extensions by version of PostgreSQL](concepts-extensions-by-engine.md).

You can also see this information by running `SHOW azure.extensions;`.

You can't bring your own extensions into an Azure HorizonDB instance. Extensions not included in the lists referred to earlier aren't supported on your Azure HorizonDB instance.

## Related content

- [Extensions and modules in Azure HorizonDB (Preview)](concepts-extensions.md)
- [Considerations with the use of extensions and modules in Azure HorizonDB (Preview)](concepts-extensions-considerations.md)
- [List of extensions and modules by name in Azure HorizonDB (Preview)](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL in Azure HorizonDB (Preview)](concepts-extensions-by-engine.md)
