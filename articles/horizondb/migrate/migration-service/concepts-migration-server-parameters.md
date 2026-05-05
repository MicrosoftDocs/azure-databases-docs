---
title: Managing Migration with Server Parameters in Azure HorizonDB
description: Learn about migration configurable parameters, by using the migration service in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.topic: concept-article
---

# Managing migration with server parameters in Azure HorizonDB

To provide customers with greater control over migration settings, we have introduced configurable migration parameters within the server parameters section. These parameters allow users to tailor their migration experience based on their data requirements, reducing the need for backend interventions and support requests.

For example, customers can use the `azure.migration_skip_role_user` parameter to decide whether user roles should be migrated automatically or handled manually. Similarly, parameters such as `azure.migration_table_split_size allow` users to optimize data transfer efficiency. These options empower customers to manage their migration settings independently, improve flexibility, and reduce operational overhead.

:::image type="content" source="media/concepts-migration-server-parameters/configure-server-parameters.png" alt-text="Screenshot of migration server parameters within Azure HorizonDB." lightbox="media/concepts-migration-server-parameters/configure-server-parameters.png":::

## Migration server parameters

| Parameter name | Type | Description | Supported sources |
| --- | --- | --- | --- |
| `azure.migration_copy_with_binary` | Boolean | When set to `on`, this parameter enables the use of the binary format for copying data during migration. | All supported sources by the migration service |
| `azure.migration_table_split_size` | Integer (MB) | Defines the size (in MB) at which tables will be partitioned during migration. | All supported sources by the migration service |
| `azure.migration_skip_large_objects` | Boolean | When set to `on`, this parameter skips the migration of large objects such as BLOBs. | All supported sources by the migration service |
| `azure.migration_skip_extensions` | Boolean | When set to `on`, this parameter skips the migration of extensions. | All supported sources by the migration service |

> [!NOTE]  
> - The migration configurable server parameters are only applicable to the new Azure HorizonDB.
> - Changes in the migration configurable server parameters don't require a restart.
> - The `azure.migration_skip_role_user` parameter is disabled for the target Azure HorizonDB version 16.

These parameters allow users to customize their migration process efficiently, ensuring a streamlined and optimized experience while minimizing dependencies on backend adjustments.

## Related content

- [What is the migration service in Azure HorizonDB?](overview-migration-service-postgresql.md)
- [Known issues and limitations for the migration service in Azure HorizonDB](concepts-known-issues-migration-service.md)
- [Network scenarios for the migration service in Azure HorizonDB](how-to-network-setup-migration-service.md)
