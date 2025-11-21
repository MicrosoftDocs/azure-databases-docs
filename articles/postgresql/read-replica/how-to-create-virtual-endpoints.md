---
title: Create virtual endpoints
description: This article describes how to create virtual endpoints for an Azure Database for PostgreSQL flexible server instance.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 04/13/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Create virtual endpoints

This article provides step-by-step instructions to create virtual endpoints for an Azure Database for PostgreSQL flexible server instance.

## Steps to create virtual endpoints

### [Portal](#tab/portal-create-virtual-endpoints)

Using the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server instance for which you want to create virtual endpoints.

2. In the resource menu, under the **Settings** section, select **Replication**.

    :::image type="content" source="./media/how-to-read-replicas/replication.png" alt-text="Screenshot showing the Replication page." lightbox="./media/how-to-read-replicas/replication.png":::

3.  In the **Virtual endpoints** section, select **Create virtual endpoints**.

    :::image type="content" source="./media/how-to-read-replicas/create-virtual-endpoints.png" alt-text="Screenshot showing the location of the Create virtual endpoints button in the Replication page." lightbox="./media/how-to-read-replicas/create-virtual-endpoints.png":::

4. The two fully qualified domain name aliases (CNAME) records that get created when you create virtual endpoints, have the following pattern: `<virtual-endpoints-base-name>.writer.postgres.database.azure.com` and `<virtual-endpoints-base-name>.reader.postgres.database.azure.com`. In the **Create virtual endpoints** dialog, in the **Virtual endpoints base name**, enter a meaningful name which isn't taken already by some other server.

    :::image type="content" source="./media/how-to-read-replicas/virtual-endpoints-base-name.png" alt-text="Screenshot showing where to enter the virtual endpoints base name." lightbox="./media/how-to-read-replicas/virtual-endpoints-base-name.png":::

5. **Target of writer virtual endpoint** must always point to the primary server, because that's the only server that is configured to support user initiated write operations. If the server on which you're creating the virtual endpoints don't have any read replica, then **Target of reader virtual endpoint** also points to the primary server. However, if the server on which you're creating the virtual endpoints has some read replica, by default **Target of reader virtual endpoint** is pointed to one of the read replicas, and can be changed to point to the primary server or to any other read replica, provided there's more than one.

    :::image type="content" source="./media/how-to-read-replicas/target-of-reader-virtual-endpoint.png" alt-text="Screenshot showing how the Target of reader virtual endpoint refers to a read replica when there's one configured." lightbox="./media/how-to-read-replicas/target-of-reader-virtual-endpoint.png":::

6. Select **Create**.

    :::image type="content" source="./media/how-to-read-replicas/create-virtual-endpoints-create.png" alt-text="Screenshot showing the Create button to create the virtual endpoints." lightbox="./media/how-to-read-replicas/create-virtual-endpoints-create.png":::


7. A notification informs you that the virtual endpoints are being created.

    :::image type="content" source="./media/how-to-read-replicas/notification-creating-virtual-endpoints.png" alt-text="Screenshot showing a notification informing that the virtual endpoints are being created." lightbox="./media/how-to-read-replicas/notification-creating-virtual-endpoints.png":::

8. When the process completes, a notification informs you that the virtual endpoints were successfully created.

    :::image type="content" source="./media/how-to-read-replicas/notification-created-virtual-endpoints.png" alt-text="Screenshot showing a notification informing that the virtual endpoints were created successfully." lightbox="./media/how-to-read-replicas/notification-created-virtual-endpoints.png":::

### [CLI](#tab/cli-create-virtual-endpoints)

You can create virtual endpoints for your Azure PostgreSQL flexible server instance via the [`az postgres flexible-server virtual-endpoint create`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-virtual-endpoint-create) command. 

```azurecli-interactive
az postgres flexible-server virtual-endpoint create \
  --resource-group <resource_group> \
  --server-name <server> \
  --name <virtual_endpoints_base_name> \
  --endpoint-type ReadWrite
  --members <replica>
```
---

## Related content

- [Read replicas](concepts-read-replicas.md).
- [Update virtual endpoints](how-to-update-virtual-endpoints.md).
- [Show virtual endpoints](how-to-show-virtual-endpoints.md).
- [Delete virtual endpoints](how-to-delete-virtual-endpoints.md).
- [Switch over read replica to primary](how-to-switch-over-replica-to-primary.md).
