---
title: Scale operations - Azure portal
description: This article describes how to perform scale operations in Azure Database for PostgreSQL - Flexible Server through the Azure portal.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 06/09/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Scale operations in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides steps to perform scaling operations for compute and storage. You're able to change your compute tiers between burstable, general purpose, and memory optimized SKUs, including choosing the number of vCores that is suitable to run your application. You can also scale up your storage. Expected IOPS are shown based on the compute tier, vCores and the storage capacity. The cost estimate is also shown based on your selection.

> [!IMPORTANT]
> You can't scale down the storage.

## Prerequisites

To complete this how-to guide, you need:

-   You must have an Azure Database for PostgreSQL flexible server instance. The same procedure is also applicable for an Azure Database for PostgreSQL flexible server instance configured with zone redundancy.


## Scaling the compute tier and size

Follow these steps to choose the compute tier.
 
1.  In the [Azure portal](https://portal.azure.com/), choose the Azure Database for PostgreSQL flexible server instance that you want to restore the backup from.

2.  Select **Compute+storage**.

3.  A page with current settings is displayed.
 :::image type="content" source="./media/how-to-scale-compute-storage-portal/click-compute-storage.png" alt-text="Screenshot that shows compute+storage view.":::

4.  You can choose the compute class between burstable, general purpose, and memory optimized tiers.
   :::image type="content" source="./media/how-to-scale-compute-storage-portal/list-compute-tiers.png" alt-text="Screenshot that  list compute tiers.":::


5.  If you're good with the default vCores and memory sizes, you can skip the next step.

6.  If you want to change the number of vCores, you can select the drop-down of **Compute size** and select the desired number of vCores/Memory from the list.
    
    - Burstable compute tier:
    :::image type="content" source="./media/how-to-scale-compute-storage-portal/compute-burstable-dropdown.png" alt-text="Screenshot that shows burstable compute.":::

    - General purpose compute tier:
    :::image type="content" source="./media/how-to-scale-compute-storage-portal/compute-general-purpose-dropdown.png" alt-text="Screenshot that shows general-purpose compute.":::

    - Memory optimized compute tier:
    :::image type="content" source="./media/how-to-scale-compute-storage-portal/compute-memory-optimized-dropdown.png" alt-text="Screenshot that shows memory optimized compute.":::

7.  Select **Save**. 
8.  You see a confirmation message. Select **OK** if you want to proceed. 
9.  A notification about the scaling operation in progress.


## Manual storage scaling

Follow these steps to increase your storage size.

1.  In the [Azure portal](https://portal.azure.com/), choose the Azure Database for PostgreSQL flexible server instance for which you want to increase the storage size.

2.  Select **Compute+storage**.

3.  A page with current settings is displayed.
   
:::image type="content" source="./media/how-to-scale-compute-storage-portal/click-compute-storage.png" alt-text="Screenshot that shows compute+storage.":::

4.  Select **Storage size in GiB** drop down and choose your new desired size.

 :::image type="content" source="./media/how-to-scale-compute-storage-portal/storage-scaleup.png" alt-text="Screenshot that shows storage scale up.":::

5. If you're good with the storage size, select **Save**.
   
6. Most of the disk scaling operations are **online** and as soon as you select **Save** scaling process starts without any downtime but some scaling operations are **offline** and you see below server restart message. Select **continue** if you want to proceed.

     :::image type="content" source="./media/how-to-scale-compute-storage-portal/offline-scaling.png" alt-text="Screenshot that shows offline scaling.":::
   
7. You will receive a notification that scaling operation is in progress.


## Storage autogrow 

Use below steps to enable storage autogrow for your Azure Database for PostgreSQL flexible server instance and automatically scale your storage in most cases.

1.  In the [Azure portal](https://portal.azure.com/), choose the Azure Database for PostgreSQL flexible server instance for which you want to increase the storage size.

2.  Select **Compute+storage**.

3.  A page with current settings is displayed.
   
:::image type="content" source="./media/how-to-scale-compute-storage-portal/storage-autogrow.png" alt-text="Screenshot that shows storage autogrow checkbox.":::

4. Check **Storage Auto-growth** button

 :::image type="content" source="./media/how-to-scale-compute-storage-portal/storage-autogrow.png" alt-text="Screenshot that shows storage autogrow.":::

5.  Select **Save**. 

6.  You receive a notification that storage autogrow enablement is in progress.

> [!IMPORTANT]
> Storage autogrow initiates disk scaling operations online, but there are specific situations where online scaling is not possible. In such cases, like when approaching or surpassing the 4,096-GiB limit, storage autogrow does not activate, and you must manually increase the storage. A portal informational message is displayed when this happens.

## Performance tier

### Scaling up

Use the below steps to scale up the performance tier on your Azure Database for PostgreSQL flexible server instance.

1. In the [Azure portal](https://portal.azure.com/), choose the Azure Database for PostgreSQL flexible server instance that you want to scale up.

2. Select **Compute + storage**.

3. A page with current settings is displayed.
 
    :::image type="content" source="./media/how-to-scale-compute-storage-portal/iops-scale-up-1.png" alt-text="Screenshot that shows performance tier 1.":::

4. You see the new “Performance Tier” drop-down option. The option selected will be the pre-provisioned IOPS, which is also the minimum amount of IOPS available for the selected storage size.

    :::image type="content" source="./media/how-to-scale-compute-storage-portal/iops-scale-up-2.png" alt-text="Screenshot that shows performance tier drop-down 2.":::

5. Select your new performance tier and select save.

    :::image type="content" source="./media/how-to-scale-compute-storage-portal/iops-scale-up-3.png" alt-text="Screenshot that shows performance tier and save 3.":::

6. Your server deploys and once the deployment is completed, your server is updated and will show the new performance tier.

### Scaling down 

Use the below steps to scale down the performance tier on your Azure Database for PostgreSQL flexible server instance.

1. In the [Azure portal](https://portal.azure.com/), choose the Azure Database for PostgreSQL flexible server instance that you want to scale down.

2. Select **Compute + storage**.

3. A page with current settings is displayed.

    :::image type="content" source="./media/how-to-scale-compute-storage-portal/iops-scale-down-1.png" alt-text="Screenshot that shows performance tier 4.":::

4.	You see the new “Performance Tier” drop-down option. The option selected will be your last selected IOPS when you scaled up.

    :::image type="content" source="./media/how-to-scale-compute-storage-portal/iops-scale-down-2.png" alt-text="Screenshot that shows performance tier drop-down 5.":::

5.	Select your new performance tier and select save.

    :::image type="content" source="./media/how-to-scale-compute-storage-portal/iops-scale-down-3.png" alt-text="Screenshot that shows performance tier and save 6.":::

6.	Your server deploys and once the deployment is completed, your server is updated and will show the new performance tier.

> [!IMPORTANT]
> You can only scale down the Performance Tier of your server 12 hours after scaling up. This restriction is in place to ensure stability and performance after any changes to your server's configuration.

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Overview of business continuity with Azure Database for PostgreSQL - Flexible Server](concepts-business-continuity.md).
- [High availability in Azure Database for PostgreSQL - Flexible Server](/azure/reliability/reliability-postgresql-flexible-server).
- [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md).
- [Storage options in Azure Database for PostgreSQL - Flexible Server](concepts-storage.md).
- [Limits in Azure Database for PostgreSQL - Flexible Server](concepts-limits.md).
