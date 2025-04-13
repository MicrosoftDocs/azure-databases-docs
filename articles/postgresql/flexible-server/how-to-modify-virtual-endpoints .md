---
title: Modify virtual endpoints
description: This article describes how to modify virtual endpoints for an Azure Database for PostgreSQL flexible server.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 04/13/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Modify vierual endpoints

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to create virtual endpoints for an Azure Database for PostgreSQL flexible server.

## Steps to modify virtual endpoints

### [Portal](#tab/portal-modify-virtual-endpoints)

Using the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server for which you want to modify its associated virtual endpoints.

2. In the resource menu, under the **Settings** section, select **Replication**.

    :::image type="content" source="./media/how-to-read-replicas/replication.png" alt-text="Screenshot showing the Replication page." lightbox="./media/how-to-read-replicas/replication.png":::

3.  In the **Virtual endpoints** section, select **Create virtual endpoints**.

    :::image type="content" source="./media/how-to-read-replicas/create-virtual-endpoints.png" alt-text="Screenshot showing the location of the Create virtual endpoints button in the Replication page." lightbox="./media/how-to-read-replicas/create-virtual-endpoints.png":::

4. The two fully qualified domain name aliases (CNAME) records that get created when you create virtual endpoints, have the following pattern: `<virtual-endpoints-base-name>.writer.postgres.database.azure.com` and `<virtual-endpoints-base-name>.reader.postgres.database.azure.com`. In the **Create virtual endpoints** dialog, in the **Virtual endpoints base name**, enter a meaningful name which isn't taken already by some other server.

    :::image type="content" source="./media/how-to-read-replicas/virtual-endpoints-base-name.png" alt-text="Screenshot showing where to enter the virtual endpoints base name." lightbox="./media/how-to-read-replicas/virtual-endpoints-base-name.png":::

5. Select **Create**.

    :::image type="content" source="./media/how-to-read-replicas/create-virtual-endpoints-create.png" alt-text="Screenshot showing the Create button to create the virtual endpoints." lightbox="./media/how-to-read-replicas/create-virtual-endpoints-create.png":::


6. A notification informs you that the virtual endpoints are being created.

    :::image type="content" source="./media/how-to-read-replicas/notification-creating-virtual-endpoints.png" alt-text="Screenshot showing a notification informing that the virtual endpoints are being created." lightbox="./media/how-to-read-replicas/notification-creating-virtual-endpoints.png":::

7. When the process completes, a notification informs you that the virtual endpoints were successfully created.

    :::image type="content" source="./media/how-to-read-replicas/notification-created-virtual-endpoints.png" alt-text="Screenshot showing a notification informing that the virtual endpoints were created successfully." lightbox="./media/how-to-read-replicas/notification-created-virtual-endpoints.png":::

### [Portal](#tab/cli-modify-virtual-endpoints)

You can create a read replica for your Azure PostgreSQL flexible server via the [`az postgres flexible-server virtual-endpoint create`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-virtual-endpoint-create) command. 

```azurecli-interactive
az postgres flexible-server virtual-endpoint create \
  --resource-group <resource_group> \
  --server-name <server_name> \
  --name <name> \
  --endpoint-type ReadWrite
  --members <replica-name>
```

## Related content

- [Read replicas](concepts-read-replicas.md).
