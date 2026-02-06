---
title: "Migration Runtime Server in Azure Database for PostgreSQL"
description: "This article discusses concepts about migration runtime server with the migration service in Azure Database for PostgreSQL."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 07/21/2025
ms.service: azure-database-postgresql
ms.topic: concept-article
---

# Migration runtime server with the migration service in Azure Database for PostgreSQL

The migration runtime server is a crucial component in the migration service for Azure Database for PostgreSQL. It serves as an intermediary server, ensuring secure and efficient data transfer during the migration process. This server is particularly useful when migrating databases from environments that are only accessible via private networks.

By acting as a bridge between the source PostgreSQL instance and the target Azure Database for PostgreSQL flexible server instance, the migration runtime server facilitates seamless data migration. It ensures that the migration occurs within a secure and isolated network space, maintaining the integrity and confidentiality of the data being transferred.

This article provides an in-depth look at the migration runtime server, its supported scenarios, and how to use it effectively within the migration service in Azure Database for PostgreSQL.

:::image type="content" source="media/concepts-migration-service-runtime-server/private-endpoint-scenario.png" alt-text="Screenshot that shows migration runtime server." lightbox="media/concepts-migration-service-runtime-server/private-endpoint-scenario.png":::

## Supported migration scenarios with the migration runtime server

Migration runtime server is essential for transferring data from different source PostgreSQL instances to the Azure Database for PostgreSQL flexible server instance. Runtime server is applicable for sources such as on-premises databases, Azure virtual machines, or AWS instances, that are only accessible via private networks, and the target Azure Database for PostgreSQL flexible server instance with a private endpoint.

## How do you use the migration runtime server?

To use the migration runtime server within the migration service in Azure Database for PostgreSQL, you have two migration options:

- Use the Azure portal during setup.
- Specify the `migrationRuntimeResourceId` parameter in the JSON properties file during the migration create command in the Azure CLI.

Here's how to do it in both methods.

# [Azure portal](#tab/azure-portal)

### Use the Azure portal

1. Sign in to the Azure portal and access the migration service (from the target server) in the Azure Database for PostgreSQL instance.
1. Begin a new migration workflow within the service.
1. When you reach the **Runtime server** tab, select **Yes** in the **Use runtime server** radio button.
1. Select your Azure subscription and resource group. Select the location of the virtual network integrated Azure Database for PostgreSQL flexible server instance.
1. Select the appropriate Azure Database for PostgreSQL flexible server instance to serve as your migration runtime server instance.

   :::image type="content" source="media/concepts-migration-service-runtime-server/select-runtime-server.png" alt-text="Screenshot that shows selecting migration runtime server." lightbox="media/concepts-migration-service-runtime-server/select-runtime-server.png":::

# [Azure CLI](#tab/azure-cli)

### Use the Azure CLI

1. Open your command-line interface.
1. Ensure that you have the Azure CLI installed, and that you're signed in to your Azure account by using `az login`.
1. The version should be at least 2.62.0 or above to use the migration runtime server option.
1. The `az postgres flexible-server migration create` command requires a JSON file path as part of the `--properties` parameter, which contains configuration details for the migration. Provide the `migrationRuntimeResourceId` parameter in the JSON properties file.

---

## Migration runtime server essentials

- **Minimal configuration**: Despite being created from Azure Database for PostgreSQL flexible server, migration runtime server solely facilitates migration without the need for high availability, backups, version specificity, or advanced storage features.
- **Performance and sizing**: Migration runtime server must be appropriately scaled to manage the workload. We recommend that you select an SKU equivalent to or greater than that of the target server.
- **Networking**: Ensure that migration runtime server is appropriately integrated into the virtual network and that network security allows for secure communication with both the source and target servers. For more information, see [Network guide for migration service](how-to-network-setup-migration-service.md).
- **Post-migration cleanup**: After the migration is finished, migration runtime server should be decommissioned to avoid unnecessary costs. Before deletion, ensure that all data was successfully migrated and that the server is no longer needed.

## Related content

- [Migration service](concepts-migration-service-postgresql.md)
- [Network setup](how-to-network-setup-migration-service.md)
- [Premigration validations](concepts-premigration-migration-service.md)
