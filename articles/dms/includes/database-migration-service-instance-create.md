---
author: pehewitt
ms.author: pehewitt
ms.reviewer: randolphwest
ms.date: 10/28/2025
ms.service: sql-database
ms.topic: include
ms.collection:
  - sql-migration-content
ms.custom:
  - sfi-image-nochange
---

## Create an Azure Database Migration Service instance

1. In the Azure portal menu or on the **Home** page, select **Create a resource**. Search for and select **Azure Database Migration Service**.

   :::image type="content" source="../media/portal-marketplace.png" alt-text="Screenshot of Azure Marketplace.":::

1. On the **Azure Database Migration Service** screen, select **Create**.

   :::image type="content" source="../media/dms-create-1.png" alt-text="Screenshot of Create Azure Database Migration Service instance." lightbox="../media/dms-create-1.png":::

   Select the appropriate **Source server type** and **Target server type**, and choose the **Database Migration Service (Classic)** option.

   :::image type="content" source="../media/dms-classic-create-2.png" alt-text="Screenshot of Select Database Migration Service (Classic) scenario." lightbox="../media/dms-classic-create-2.png":::

1. On the **Create Migration Service** basics screen:

   - Select the subscription.
   - Create a new resource group or choose an existing one.
   - Specify a name for the instance of the Azure Database Migration Service.
   - Select the location in which you want to create the instance of Azure Database Migration Service.
   - Choose **Azure** as the service mode.
   - Select a pricing tier. For more information on costs and pricing tiers, see the [pricing page](https://aka.ms/dms-pricing).

   :::image type="content" source="../media/dms-settings-1.png" alt-text="Screenshot of Configure Azure Database Migration Service instance basics settings.":::

   - Select **Next: Networking**.

1. On the **Create Migration Service** networking screen:

   - Select an existing virtual network or create a new one. The virtual network provides Azure Database Migration Service with access to the source server and the target instance. For more information about how to create a virtual network in the Azure portal, see the article [Create a virtual network using the Azure portal](/azure/virtual-network/quick-create-portal).

   :::image type="content" source="../media/dms-settings-2.png" alt-text="Screenshot of Configure Azure Database Migration Service instance networking settings.":::

   - Select **Review + Create** to review the details and then select **Create** to create the service.

   - After a few moments, your instance of the Azure Database Migration service is created and ready to use:

   :::image type="content" source="../media/dms-service-created.png" alt-text="Screenshot of migration service created." lightbox="../media/dms-service-created.png":::
