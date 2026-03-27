---
title: Migrate from VNet to a Private Endpoint Capable Network Configuration
description: Learn how to migrate Azure Database for PostgreSQL from a VNet deployment to a network configuration that supports private endpoint connectivity.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 03/27/2026
ms.topic: how-to
ms.service: azure-database-postgresql
ms.subservice: networking
---

# Migrate from VNet to a Private Endpoint Capable Network Configuration (Preview)

Azure Database for PostgreSQL flexible servers instances deployed with Virtual Network (VNet) integration can be migrated to a network configuration that supports private endpoints. Private endpoints provide secure connectivity through Azure Private Link, allowing your server to be accessed over a private IP address within your virtual network. This migration replaces VNet-injected networking with private endpoint support, giving you more flexibility in network design while maintaining private connectivity.

This article walks you through the steps to migrate your server, what to expect during the process, and how to restore connectivity after the migration is complete.

## Prerequisites

Before you begin, verify that your server and environment meet the following requirements.

- Server Configuration:

  - The migration currently supports servers that are non-High Availability (HA) and non-replica. If HA is enabled, you must disable it before migration. Support for HA-enabled server migration is planned for future updates.

    > [!TIP]
    > You can re-enable HA after the process is complete.

- Access Requirements:

  - Azure API, SDK, or CLI supports this migration operation. Ensure you have access to one of these tools.

## Details to know in advance

Review the following information about connectivity, downtime, and post-migration defaults before you start the migration.

- Public access settings:

  - After migration, public access is enabled by default. The migration doesn't configure any firewall rules that permit inbound traffic unless you explicitly define them. If you don't want public access, you can disable it after migration.

  > [!NOTE]
  > A future update changes the default to disable public access after migration.

- You need to adjust Terraform scripts after the migration to comply with the new setup. For more information, see the *Post-migration Setup* section.

- The end-to-end migration process typically takes about 20 minutes. During this time, the server is in an "updating" state.

- Connectivity impact:

  - For about 10 minutes, the server is inaccessible. The migration process terminates existing database connections and rejects new connection attempts during this period.

## Migration steps

Use the Azure CLI to start the migration and then monitor the server status until the operation completes.

### Initiate the migration

Use the Azure CLI to migrate your server to a PE-capable network configuration. Replace `your-resource-group` and `your-server-name` with your actual resource group and server names.

```azurecli
az postgres flexible-server migrate-network --resource-group your-resource-group --name your-server-name
```

### Monitor server status

After you run the CLI command, the server's status changes to **updating**. Monitor the status:

- **From portal**: Refresh the page in the Azure portal periodically until the update finishes.

  :::image type="content" source="media/how-to-migrate-vnet-private-endpoint-capable-server/image2.png" alt-text="Screenshot of the Azure portal showing the server in updating state.":::

- **From terminal**: You see the Azure CLI progress spinner for a long-running operation. This spinner means the command starts successfully and the service processes the network migration asynchronously on the backend. In a second terminal, you can check the server state:

    ```azurecli
    az postgres flexible-server show \
        --resource-group your-resource-group \
        --name your-server-name \
        --query "state"
    ```

## Post-migration setup

After the migration completes, configure networking and update any infrastructure-as-code templates to match the new network configuration.

### Restore connectivity

When migration finishes, the server is inaccessible until you configure a private endpoint or establish appropriate firewall rules.

For more information, see [Add private endpoint connections to Azure Database for PostgreSQL](../network/how-to-networking-servers-deployed-public-access-add-private-endpoint.md?tabs=cli-add-private-endpoint-connection).

### Update Terraform scripts

After the VNet to PE-capable network migration, the server is no longer VNet-integrated. Update Terraform configurations accordingly:

- Remove `delegated_subnet_id` from the PostgreSQL server resource.
- Ensure `public_network_access_enabled` remains `true` (this value is the post-migration default).

## Related content

- [Add private endpoint connections to Azure Database for PostgreSQL](../network/how-to-networking-servers-deployed-public-access-add-private-endpoint.md?tabs=cli-add-private-endpoint-connection)
- [Azure Database for PostgreSQL networking overview](concepts-networking-private.md)