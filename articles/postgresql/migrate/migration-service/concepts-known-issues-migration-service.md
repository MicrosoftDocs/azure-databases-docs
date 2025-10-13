---
title: "Known Issues And Limitations For The Migration Service"
description: This article describes the limitations and known issues of the migration service in Azure Database for PostgreSQL.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 02/07/2025
ms.service: azure-database-postgresql
ms.topic: concept-article
---

# Known issues and limitations for the migration service

This article describes the known issues and limitations that are associated with the migration service in Azure Database for PostgreSQL.

## Common limitations

The following list describes common limitations that apply to migration scenarios:

- You can have only one active migration or validation to your flexible server.
- The migration service supports migration for users and roles only when the source is Azure Database for PostgreSQL - Single Server.
- The migration service shows the number of tables that are copied from the source to the target. You must manually check the data and PostgreSQL objects on the target server after migration.
- The migration service migrates only user databases. The service doesn't migrate system databases like **template_0** and **template_1**.
- You can't move extensions that aren't supported by Azure Database for PostgreSQL flexible server. Supported extensions are listed in [Extensions for Azure Database for PostgreSQL](/azure/postgresql/flexible-server/concepts-extensions).
- User-defined collations can't be migrated to Azure Database for PostgreSQL flexible server.
- You can't migrate to an earlier version. For instance, you can't migrate from Azure Database for PostgreSQL version 15 to Azure Database for PostgreSQL version 14.
- The migration service works only with an `SSLMODE` value of `preferred` or `required`.
- The migration service doesn't support superuser permissions and objects.
- Azure Database for PostgreSQL flexible server doesn't support the creation of custom tablespaces due to restrictions on superuser permissions. During migration, data from custom tablespaces in the source PostgreSQL instance is migrated to the default tablespaces of the target instance of Azure Database for PostgreSQL flexible server.
- The following PostgreSQL objects can't be migrated to a flexible server target:
  - Create casts
  - Creation of full-text search (FTS) parsers and FTS templates
  - Users that have superuser roles
  - Create TYPE
- The migration service doesn't support migration at the object level. That is, you can't migrate a table or a schema.

  > [!IMPORTANT]
  > Though the Burstable SKU is not a limitation, it is recommended to choose a higher SKU for your flexible server to perform faster migrations. Azure Database for PostgreSQL flexible server supports near-zero downtime compute and IOPS scaling, so the SKU can be updated with minimal downtime. You can always change the SKU to match the application needs post-migration.

## Limitations in migrating from Azure Database for PostgreSQL - Single Server

The following list describes limitations specific to migrating from Azure Database for PostgreSQL - Single Server:

- If the target flexible server uses the SCRAM-SHA-256 password encryption method, connection to a flexible server by using the users or roles on a single server fails. On a single server, passwords are encrypted by using the MD5 algorithm. To mitigate this limitation, for the `password_encryption` server parameter on your flexible server, select the option `MD5`.
- Online migration uses [pgcopydb follow](https://pgcopydb.readthedocs.io/en/latest/ref/pgcopydb_follow.html). Some [logical decoding restrictions](https://pgcopydb.readthedocs.io/en/latest/ref/pgcopydb_follow.html#pgcopydb-follow) apply.
- The migration service does not support copying Microsoft Entra ID–authenticated roles when using a [runtime server](./concepts-migration-service-runtime-server.md) for performing the migration from Single Server to Flexible server. We recommend that you manually create the Entra ID–authenticated roles on the target server before initiating the migration.

## Related content

- [Migration service](concepts-migration-service-postgresql.md)
- [Network setup](how-to-network-setup-migration-service.md)
- [Premigration validations](concepts-premigration-migration-service.md)
