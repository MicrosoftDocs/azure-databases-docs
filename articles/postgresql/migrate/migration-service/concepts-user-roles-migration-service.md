---
title: "Permissions in Migration Scenarios"
description: Learn about key concerns about permissions when you migrate users, roles, and ownerships by using the migration service in Azure Database for PostgreSQL. Learn about steps to take in specific migration scenarios.
author: shriramm
ms.author: shriramm
ms.reviewer: maghan
ms.date: 01/24/2025
ms.service: azure-database-postgresql
ms.topic: concept-article
---

# Permissions in migration scenarios for the migration service

The migration service in Azure Database for PostgreSQL provides the following built-in capabilities for Azure Database for PostgreSQL - Single Server as the source and data migration:

- Migrates user roles from your source server to the target server.
- Migrates ownership of all database objects from your source server to the target server.
- Migrates permissions of database objects like GRANT and REVOKE from your source server to the target server.

> [!IMPORTANT]  
> You can migrate users, roles, ownerships, and permissions only when the source is an Azure Database for PostgreSQL flexible server - Single Server. Currently, this feature is not available for PostgreSQL version 16 servers.

> [!IMPORTANT]  
> The migration service does not support copying Microsoft Entra ID–authenticated roles when using a [runtime server](./concepts-migration-service-runtime-server.md) for performing the migration from Single Server to Flexible server. We recommend that you manually create the Entra ID–authenticated roles on the target server before initiating the migration.

## Permissions on a single server compared to a flexible server

This section describes the differences in permissions granted to the azure_pg_admin role in Azure Database for PostgreSQL - Single Server and Azure Database for PostgreSQL flexible server environments.

### pg_catalog schema permissions

Unlike a user-created schema that organizes database objects into logical groups, pg_catalog is a system schema. It holds crucial system-level information, such as details about tables, columns, and other internal bookkeeping data. The pg_catalog schema is where PostgreSQL stores important metadata. Permissions vary between single server and flexible server environments:

- In a single server environment, a user who belongs to the azure_pg_admin role is granted specific permissions for all pg_catalog tables and views.
- In a flexible server environment, permissions for certain tables and views are restricted so that only superusers can query them.

Granting unrestricted access to system tables and views in the pg_catalog schema can lead to unauthorized modifications, accidental deletions, or even security breaches. Restricted access reduces the risk of unintended changes or data exposure.

We removed all permissions for non-superusers on the following pg_catalog *tables*:

- pg_authid

- pg_largeobject

- pg_statistic

- pg_subscription

- pg_user_mapping

We removed all permissions for non-superusers on the following pg_catalog *views*:

- pg_config

- pg_file_settings

- pg_hba_file_rules

- pg_replication_origin_status

- pg_shadow

### pg_pltemplate deprecation

Another important consideration is the deprecation of the pg_pltemplate system table. Starting in *version 13*, PostgreSQL community deprecates the pg_pltemplate system table in the pg_catalog schema. If you migrate to Azure Database for PostgreSQL flexible server version 13 or later and you granted permissions to users on the pg_pltemplate table on your single server, you must revoke these permissions before you initiate a migration.

#### Effects

The following list describes important effects of pg_pltemplate deprecation:

- If your application is designed to directly query the relevant tables and views, it encounters issues when you migrate to a flexible server. We strongly recommend that you refactor your application to avoid direct queries to these system tables.
- If you granted or revoked permissions to any users or roles for the relevant pg_catalog tables and views, an error occurs during the migration process. You can identify this error by the following pattern:

  ```sql
  pg_restore error: could not execute query <GRANT/REVOKE> <PERMISSIONS> on <relevant TABLE/VIEW> to <user>.
  ```

#### Workaround

To resolve a pg_catalog error, remove the permissions that you granted to users and roles related to the relevant pg_catalog tables and views.

##### Step 1: Identify permissions

Execute the following query on your single server by logging in as the admin user.

In the code:

- Permissions are called *privileges*.
- A *relation_name* value is a table name or view name.

```sql
SELECT
  array_to_string(array_agg(acl.privilege_type), ', ') AS privileges,
  t.relname AS relation_name,
  r.rolname AS grantee
FROM
  pg_catalog.pg_class AS t
  CROSS JOIN LATERAL aclexplode(t.relacl) AS acl
  JOIN pg_roles r ON r.oid = acl.grantee
WHERE
  acl.grantee <> 'azure_superuser'::regrole
  AND t.relname IN (
    'pg_authid', 'pg_largeobject', 'pg_subscription', 'pg_user_mapping', 'pg_statistic',
    'pg_config', 'pg_file_settings', 'pg_hba_file_rules', 'pg_replication_origin_status', 'pg_shadow', 'pg_pltemplate'
  )
GROUP BY
  r.rolname, t.relname;
```

##### Step 2: Review the output

The output of the query shows the list of permissions that are granted to roles on the relevant tables and views.

For example:

| Permissions | Table or view (relation name) | Grantee |
| :--- | :--- | :--- |
| SELECT | pg_authid | adminuser1 |
| SELECT, UPDATE | pg_shadow | adminuser2 |

##### Step 3: Revoke the permissions

To revoke the permissions, run `REVOKE` statements for each permission on the table or view from the grantee.

For example:

```sql
REVOKE SELECT ON pg_authid FROM adminuser1;
REVOKE SELECT ON pg_shadow FROM adminuser2;
REVOKE UPDATE ON pg_shadow FROM adminuser2;
```

##### Step 4: Final verification

Run the query from step 1 again to ensure that the resulting output set is empty.

> [!NOTE]  
> To avoid any permissions-related issues during the migration, make sure that you complete the preceding steps for all the databases that are included in the migration.

After you finish these steps, you can initiate a migration from a single server to a flexible server by using the migration service.

## Related content

- [Migration service](concepts-migration-service-postgresql.md)
- [Known issues and limitations](concepts-known-issues-migration-service.md)
- [Network setup](how-to-network-setup-migration-service.md)
