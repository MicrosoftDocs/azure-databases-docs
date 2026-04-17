---
title: Migrate from VNet to a Private Endpoint Capable Network Configuration
description: Learn how to migrate Azure Database for PostgreSQL from a VNet deployment to a network configuration that supports private endpoint connectivity.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan, ignacioal
ms.date: 03/31/2026
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: how-to
---

# Migrate from VNet to a Private Endpoint Capable Network Configuration (Preview)

Azure Database for PostgreSQL deployed with [private access](concepts-networking-private.md) uses [virtual network injection](/azure/virtual-network/virtual-network-for-azure-services) to place the server in a delegated subnet within your virtual network. You can migrate these servers to a network configuration that supports private endpoints. Private endpoints provide secure connectivity through Azure Private Link, so you can access your server over a private IP address within your virtual network. This migration replaces VNet-injected networking with private endpoint support, giving you more flexibility in network design while maintaining private connectivity.

This article walks you through the steps to migrate your server, what to expect during the process, and how to restore connectivity after the migration is complete.

## Prerequisites

Before you begin, verify that your server and environment meet the following requirements.

- Access requirements:

  - Azure API, SDK, or CLI supports this migration operation. Ensure you have access to one of these tools.

## Details to know in advance

Review the following information about connectivity, downtime, and post-migration defaults before you start the migration.

- Public access settings:

  - After migration, public access is enabled by default. The migration process doesn't configure any firewall rules that permit inbound traffic unless you explicitly define them. If you don't want public access, you can disable it after migration.

  > [!NOTE]  
  > A future update changes the default to disable public access after migration.

- If you use Terraform to deploy PostgreSQL, you need to adjust your scripts after the migration to comply with the new setup. For more information, see the [Post-migration Setup](#post-migration-setup) section.

- The end-to-end migration process typically takes about 20 minutes. During this time, the server is in an **Updating** state.

- Connectivity impact:

  - For about 10 minutes, the server is inaccessible. The migration process terminates existing database connections and rejects new connection attempts during this period.

## Migration steps

### [Portal](#tab/portal-migrate)

This operation isn't currently available through the Azure portal. Use the **CLI** tab to initiate the migration.

After you start the migration, monitor the server status in the Azure portal. Refresh the page periodically until the status changes from **Updating** to **Ready**.

### [CLI](#tab/cli-migrate)

Run the following command to migrate your server to a PE-capable network configuration:

```azurecli-interactive
az postgres flexible-server migrate-network \
  --resource-group <resource_group> \
  --name <server>
```

After you run the command, the server's status changes to **Updating**. You can check the server state:

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query "state"
```

---

## Post-migration setup

After the migration completes, configure networking and update any infrastructure-as-code templates to match the new network configuration.

### Restore connectivity

When migration finishes, the server is inaccessible until you configure a private endpoint or establish appropriate firewall rules.

For more information, see [Add private endpoint connections to Azure Database for PostgreSQL](../network/how-to-networking-servers-deployed-public-access-add-private-endpoint.md?tabs=cli-add-private-endpoint-connection).

### Update Terraform scripts

After the VNet to PE-capable network migration, the server is no longer VNet-integrated. If you have Terraform configurations, update them accordingly:

- Remove `delegated_subnet_id` from the PostgreSQL server resource.
- Ensure `public_network_access_enabled` remains `true` (this value is the post-migration default).

## Related content

- [Add private endpoint connections to Azure Database for PostgreSQL](../network/how-to-networking-servers-deployed-public-access-add-private-endpoint.md?tabs=cli-add-private-endpoint-connection)
- [Azure Database for PostgreSQL networking overview](concepts-networking-private.md)
