---
title: Show Virtual Endpoints in Azure HorizonDB
description: This article describes how to show virtual endpoints in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: replication
ms.topic: how-to
---

# Show virtual endpoints in Azure HorizonDB

This article provides step-by-step instructions to show virtual endpoints associated to an Azure HorizonDB.

## Steps to show virtual endpoints

### [Portal](#tab/portal-show-virtual-endpoints)

Using the [Azure portal](https://portal.azure.com/):

1. Select the Azure HorizonDB for which you want to show its associated virtual endpoints.

1. In the resource menu, under the **Settings** section, select **Replication**. In the **Virtual endpoints** section you can see the reader and writer endpoints displayed, along with the endpoints of the servers to which each of them is pointing to.

   :::image type="content" source="media/how-to-read-replicas/replication-with-virtual-endpoints.png" alt-text="Screenshot showing the Replication page with virtual endpoints created." lightbox="media/how-to-read-replicas/replication-with-virtual-endpoints.png":::

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

- [Read replicas in Azure HorizonDB](concepts-read-replicas.md)
- [Update virtual endpoints in Azure HorizonDB](how-to-update-virtual-endpoints.md)
- [Delete virtual endpoints in Azure HorizonDB](how-to-delete-virtual-endpoints.md)
- [Switch over read replica to primary in Azure HorizonDB](how-to-switch-over-replica-to-primary.md)
