---
title: Create Virtual Endpoints in Azure Database for PostgreSQL Flexible Server
description: This article describes how to create virtual endpoints for an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to create virtual endpoints for my Azure Database for PostgreSQL flexible server, so that I can route read and write traffic to the appropriate servers.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan, randolphwest
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: replication
ms.topic: how-to
---

# Create virtual endpoints in Azure Database for PostgreSQL flexible server

This article provides step-by-step instructions to create virtual endpoints for an Azure Database for PostgreSQL flexible server.

## Steps to create virtual endpoints

### [Portal](#tab/portal-create-virtual-endpoints)

Use the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server for which you want to create virtual endpoints.

1. In the resource menu, under the **Settings** section, select **Replication**.

   :::image type="content" source="media/how-to-read-replicas/replication.png" alt-text="Screenshot showing the Replication page." lightbox="media/how-to-read-replicas/replication.png":::

1.  In the **Virtual endpoints** section, select **Create virtual endpoints**.

    :::image type="content" source="media/how-to-create-virtual-endpoints/create-virtual-endpoints.png" alt-text="Screenshot showing the location of the Create virtual endpoints button in the Replication page." lightbox="media/how-to-create-virtual-endpoints/create-virtual-endpoints.png":::

1. The two fully qualified domain name aliases (CNAME) records that get created when you create virtual endpoints follow this pattern: `<virtual-endpoints-base-name>.writer.postgres.database.azure.com` and `<virtual-endpoints-base-name>.reader.postgres.database.azure.com`. In the **Create virtual endpoints** dialog, in the **Virtual endpoints base name**, enter a meaningful name that isn't already taken by another server.

   :::image type="content" source="media/how-to-create-virtual-endpoints/virtual-endpoints-base-name.png" alt-text="Screenshot showing where to enter the virtual endpoints base name." lightbox="media/how-to-create-virtual-endpoints/virtual-endpoints-base-name.png":::

1. The **Target of writer virtual endpoint** always points to the primary server, because it's the only server that supports user-initiated write operations. If the server where you're creating the virtual endpoints doesn't have any read replica, the **Target of reader virtual endpoint** also points to the primary server. However, if the server where you're creating the virtual endpoints has some read replicas, **Target of reader virtual endpoint** points to one of the read replicas by default. You can change it to point to the primary server or to any other read replica, as long as there's more than one.

   :::image type="content" source="media/how-to-create-virtual-endpoints/target-of-reader-virtual-endpoint.png" alt-text="Screenshot showing how the Target of reader virtual endpoint refers to a read replica when there's one configured." lightbox="media/how-to-create-virtual-endpoints/target-of-reader-virtual-endpoint.png":::

1. Select **Create**.

   :::image type="content" source="media/how-to-create-virtual-endpoints/create-virtual-endpoints-create.png" alt-text="Screenshot showing the Create button to create the virtual endpoints." lightbox="media/how-to-create-virtual-endpoints/create-virtual-endpoints-create.png":::

1. A notification informs you that the virtual endpoints are being created.

1. When the process finishes, a notification informs you that the virtual endpoints were successfully created.

    :::image type="content" source="./media/how-to-read-replicas/notification-created-virtual-endpoints.png" alt-text="Screenshot showing a notification informing that the virtual endpoints were created successfully." lightbox="./media/how-to-read-replicas/notification-created-virtual-endpoints.png":::

### [CLI](#tab/cli-create-virtual-endpoints)

Use the [`az postgres flexible-server virtual-endpoint create`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-virtual-endpoint-create) command to create virtual endpoints for your server. 

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

- [Read replicas in Azure Database for PostgreSQL](concepts-read-replicas.md)
- [Update virtual endpoints](how-to-update-virtual-endpoints.md)
- [Show virtual endpoints](how-to-show-virtual-endpoints.md)
- [Delete virtual endpoints](how-to-delete-virtual-endpoints.md)
- [Switch over read replica to primary](how-to-switch-over-replica-to-primary.md)
