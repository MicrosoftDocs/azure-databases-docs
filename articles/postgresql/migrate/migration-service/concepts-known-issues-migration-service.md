---
title: "Known issues and limitations"
description: This article describes the limitations and known issues of the migration service in Azure Database for PostgreSQL.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 06/19/2024
ms.service: azure-database-postgresql
ms.topic: conceptual
---

# Known issues and limitations for the migration service in Azure Database for PostgreSQL

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article describes the known issues and limitations that are associated with the migration service in Azure Database for PostgreSQL.

## Common limitations

The following list describes common limitations that apply to migration scenarios:

- You can have only one active migration or validation to your flexible server.
- The migration service supports migration for users and roles only when the source is Azure Database for PostgreSQL - Single Server.
- The migration service shows the number of tables that are copied from source to target. You must manually check the data and PostgreSQL objects on the target server after migration.
- The migration service migrates only user databases. The service doesn't migrate system databases like template_0 and template_1.
- The migration service doesn't support moving POSTGIS_TOPOLOGY, POSTGIS_TIGER_GEOCODER, POSTGRES_FDW, and PG_PARTMAN extensions from source to target.

  > [!NOTE]
  > The feature to migrate databases that have the *TIMESCALEDB* extension is in preview. The option is turned off by default. To migrate your time series databases, you can open a support ticket.

- You can't move extensions that aren't supported by Azure Database for PostgreSQL - Flexible Server. Supported extensions are listed in [Extensions for Azure Database for PostgreSQL](/azure/postgresql/flexible-server/concepts-extensions).
- User-defined collations can't be migrated to Azure Database for PostgreSQL - Flexible Server.
- You can't migrate to an earlier version. For instance, you can't migrate from Azure Database for PostgreSQL version 15 to Azure Database for PostgreSQL version 14.
- The migration service works only with preferred or required SSLMODE values.
- The migration service doesn't support superuser privileges and objects.
- Azure Database for PostgreSQL - Flexible Server doesn't support the creation of custom tablespaces due to restrictions on superuser permissions. During migration, data from custom tablespaces in the source PostgreSQL instance is migrated to the default tablespaces of the target Azure Database for PostgreSQL - Flexible Server instance.
- Currently, online migration from Amazon Aurora PostgreSQL 13 to Azure Database for PostgreSQL - Flexible Server is not supported. An attempt to migrate will fail.
- The following PostgreSQL objects can't be migrated to the PostgreSQL flexible server target:

  - Create casts
  - Creation of FTS parsers and FTS templates
  - Users that have superuser roles
  - Create TYPE

- The migration service doesn't support migration at the object level. That is, you can't migrate a table or a schema.
- Currently, migrating to the Burstable SKU is supported only in the West Europe region. In all other Azure regions, you can migrate databases first to a General Purpose SKU or to a Memory Optimized SKU, and then scale down if needed.
- The migration runtime server is designed to operate with default DNS servers or private DNS zones, for example, with `privatelink.postgres.database.azure.com`. Custom DNS names and custom DNS servers aren't supported by the migration service when you use the migration runtime server feature. When you configure private endpoints for both the source database and the target database, it's imperative to use the default private DNS zone that's provided by Azure for the private link service. Using a custom DNS configuration isn't yet supported and might lead to connectivity issues during the migration process.

## Limitations migrating from Azure Database for PostgreSQL - Single Server

- Microsoft Entra ID users who are on your source server aren't migrated to the target server. To mitigate this limitation, see [Manage Microsoft Entra roles](../../flexible-server/how-to-manage-azure-ad-users.md). The solution is to manually create all Microsoft Entra users on your target server before you initiate a migration. If Microsoft Entra users aren't created on the target server, migration fails.
- If the target flexible server uses the SCRAM-SHA-256 password encryption method, connection to a flexible server by using the users or roles on a single server fails because the passwords are encrypted by using the md5 algorithm. To mitigate this limitation, choose the option `MD5` for the `password_encryption` server parameter on your flexible server.
- Online migration makes use of [pgcopydb follow](https://pgcopydb.readthedocs.io/en/latest/ref/pgcopydb_follow.html), and some of the [logical decoding restrictions](https://pgcopydb.readthedocs.io/en/latest/ref/pgcopydb_follow.html#pgcopydb-follow) apply.

## Related content

- [Migration service](concepts-migration-service-postgresql.md)
- [Network setup](how-to-network-setup-migration-service.md)
- [Premigration validations](concepts-premigration-migration-service.md)
