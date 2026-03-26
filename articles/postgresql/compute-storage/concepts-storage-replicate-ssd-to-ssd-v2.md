---
title: Migrate SSD Server to SSDv2 Using Replicas
description: This article describes how to migrate a Premium SSD server to Premium SSDv2 using replicas in Azure Database for PostgreSQL flexible server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 08/10/2025
ms.service: azure-database-postgresql
ms.subservice: compute-storage
ms.topic:  concept-article
#customer intent: As a user, I want to learn how to migrate from Premium SSD server to Premium SSDv2 in Azure Database for PostgreSQL flexible server.
---

# Migrate or replicate from Premium SSD to Premium SSDv2

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to migrate from Premium SSD to Premium SSDv2  using replication in Azure Database for PostgreSQL flexible server.

## Steps to migrate or replicate from Premium SSD to Premium SSDv2


Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Settings** go to **Replication** and click the **Create replica** button. 

    :::image type="content" source="./media/concepts-storage-replicate-ssd-to-ssd-v2/create-replica.png" alt-text="Screenshot showing the Replication page." lightbox="./media/concepts-storage-replicate-ssd-to-ssd-v2/create-replica.png":::

   
3.  Provide Server name and Select **Configure server**.


:::image type="content" source="media/concepts-storage-replicate-ssd-ssd-v2/configure-server-page.png"  alt-text="Screenshot showing the Compute + storage page." lightbox="./media/concepts-storage-replicate-ssd-to-ssd-v2/configure-server-page.png":::":::":::


4. Choose **Premium SSD v2** for the **Storage type** Field.

   :::image type="content" source="media/concepts-storage-replicate-ssd-ssd-v2/premium-ssdv2.png" alt-text="Screenshot showing the Premium SSDv2 storage type button selected." lightbox="./media/concepts-storage-replicate-ssd-to-ssd-v2/premium-ssdv2.png":::":::

5.  Once all the replica server is configured to your needs, select **Review + create**.

    
      :::image type="content" source="./media/concepts-storage-replicate-ssd-ssd-v2/add-replica-validation.png" alt-text="Screenshot showing the Add Replica page." lightbox="./media/concepts-storage-replicate-ssd-to-ssd-v2/add-replica-validation.png":::


7. A new deployment is launched to create your new Azure Database for PostgreSQL flexible server with Premium SSD v2 storage type with the latest data using replication.

   
8. When the deployment completes, you can select **Go to resource**, to get you to the **Compute +Storage** page of your new Azure Database for PostgreSQL flexible server, and start validate your **Storage type**.

    :::image type="content" source="./media/concepts-storage-replicate-ssd-ssd-v2/validate-ssdv2.png" alt-text="Screenshot that shows new server created using premium ssd v2." lightbox="./media/concepts-storage-replicate-ssd-to-ssd-v2/validate-ssdv2.png":::

9. Select **Replication** and click  **Switch over or promote to standalone**, select **Promote to standalone server and remove from replication.This won't impact primary server** for **Action**. And select **Planned-sync data before promoting**  and you have to mark the **I understand that this read replica will become an independent standalone server and this action can't be undone.** checkbox to acknowledge. Finally, select **Promote to standalone**.

    :::image type="content" source="./media/concepts-storage-replicate-ssd-ssd-v2/promote-primary.png" alt-text="Screenshot that shows promoting new server ssd v2 server as standalone." lightbox="./media/concepts-storage-replicate-ssd-to-ssd-v2/promote-primary.png":::


10. Once the promotion is complete, you can repoint your virtual endpoints from the Premium SSD–based server to the new Premium SSD v2 server and safely decommission the original server

 :::image type="content" source="./media/concepts-storage-replicate-ssd-ssd-v2/recreate-virtual-endpoint.png" alt-text="Screenshot that shows new server  using virtual endpoint." lightbox="./media/concepts-storage-replicate-ssd-to-ssd-v2/recreate-virtual-endpoint.png":::

---

## Related content

- [Migrate SSD to SSDv2 using restore](concepts-storage-replicate-ssd-to-ssd-v2.md).
- [Restore to paired region (geo-restore)](../backup-restore/how-to-restore-paired-region.md).
- [Restore a dropped server](../backup-restore/how-to-restore-dropped-server.md).
