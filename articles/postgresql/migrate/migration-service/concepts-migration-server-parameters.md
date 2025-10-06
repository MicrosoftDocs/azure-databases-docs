---
title: "Managing Migration with Server Parameters"
description: Learn about migration configurable parameters, by using the migration service in Azure Database for PostgreSQL.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 07/21/2025
ms.service: azure-database-postgresql
ms.topic: concept-article
---

# Managing migration with server parameters

To provide customers with greater control over migration settings, we have introduced configurable migration parameters within the server parameters section. These parameters allow users to tailor their migration experience based on their data requirements, reducing the need for backend interventions and support requests.

For example, customers can use the `azure.migration_skip_role_user` parameter to decide whether user roles should be migrated automatically or handled manually. Similarly, parameters such as `azure.migration_table_split_size allow` users to optimize data transfer efficiency. These options empower customers to manage their migration settings independently, improve flexibility, and reduce operational overhead.

:::image type="content" source="media/concepts-migration-server-parameters/configure-server-parameters.png" alt-text="Screenshot of migration server parameters within Azure Database for PostgreSQL flexible server." lightbox="media/concepts-migration-server-parameters/configure-server-parameters.png":::

## Migration server parameters

| Parameter name | Type | Description | Supported sources |
| --- | --- | --- | --- |
| `azure.migration_skip_role_user` | Boolean | When set to `on`, this parameter excludes user roles from the migration process. | Only Azure Database for PostgreSQL single server |
| `azure.migration_copy_with_binary` | Boolean | When set to `on`, this parameter enables the use of the binary format for copying data during migration. | All supported sources by the migration service |
| `azure.migration_table_split_size` | Integer (MB) | Defines the size (in MB) at which tables will be partitioned during migration. | All supported sources by the migration service |
| `azure.migration_skip_analyze` | Boolean | When set to `on`, this parameter skips the analyze phase during the migration. | only Azure Database for PostgreSQL - Single server |
| `azure.migration_skip_large_objects` | Boolean | When set to `on`, this parameter skips the migration of large objects such as BLOBs. | All supported sources by the migration service |
| `azure.migration_skip_extensions` | Boolean | When set to `on`, this parameter skips the migration of extensions. | All supported sources by the migration service |

> [!NOTE]
> - The migration configurable server parameters are only applicable to the new Azure Database for PostgreSQL flexible server.
> - Changes in the migration configurable server parameters do not require a restart.
> - The `azure.migration_skip_role_user` parameter is disabled for the target Azure Database for PostgreSQL flexible server version 16.

These parameters allow users to customize their migration process efficiently, ensuring a streamlined and optimized experience while minimizing dependencies on backend adjustments.


## Related content

- [Migration service](concepts-migration-service-postgresql.md)
- [Known issues and limitations](concepts-known-issues-migration-service.md)
- [Network setup](how-to-network-setup-migration-service.md)
