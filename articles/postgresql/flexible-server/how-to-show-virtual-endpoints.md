---
title: Show virtual endpoints
description: This article describes how to show virtual endpoints for an Azure Database for PostgreSQL flexible server.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 04/13/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Show virtual endpoints

This article provides step-by-step instructions to show virtual endpoints associated to an Azure Database for PostgreSQL flexible server.

## Steps to show virtual endpoints

### [Portal](#tab/portal-show-virtual-endpoints)

Using the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server for which you want to show its associated virtual endpoints.

2. In the resource menu, under the **Settings** section, select **Replication**. In the **Virtual endpoints** section you can see the reader and writer endpoints displayed, along with the endpoints of the servers to which each of them is pointing to.

    :::image type="content" source="./media/how-to-read-replicas/replication-with-virtual-endpoints.png" alt-text="Screenshot showing the Replication page with virtual endpoints created." lightbox="./media/how-to-read-replicas/replication-with-virtual-endpoints.png":::

### [CLI](#tab/cli-show-virtual-endpoints)

You can show the existing virtual endpoints of your Azure PostgreSQL flexible server via the [`az postgres flexible-server virtual-endpoint show`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-virtual-endpoint-show) command or via the [`az postgres flexible-server virtual-endpoint list`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-virtual-endpoint-list) command.

Because only one pair of virtual endpoints is allowed per replication set, both commands yield the same results.

```azurecli-interactive
az postgres flexible-server virtual-endpoint show \
  --resource-group <resource_group> \
  --server-name <server> \
  --name <virtual_endpoints_base_name>
```

```azurecli-interactive
az postgres flexible-server virtual-endpoint list \
  --resource-group <resource_group> \
  --server-name <server> \
```
---

## Related content

- [Read replicas](concepts-read-replicas.md).
- [Update virtual endpoints](how-to-update-virtual-endpoints.md).
- [Delete virtual endpoints](how-to-delete-virtual-endpoints.md).
- [Switch over read replica to primary](how-to-switch-over-replica-to-primary.md).
