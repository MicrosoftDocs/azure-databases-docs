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

## Register the resource provider

Register the Microsoft.DataMigration resource provider before you create your first instance of the Database Migration Service.

1. Sign in to the Azure portal. Search for and select **Subscriptions**.

   :::image type="content" source="../media/portal-select-subscription.png" alt-text="Screenshot showing portal subscriptions." lightbox="../media/portal-select-subscription.png":::

1. Select the subscription in which you want to create the instance of Azure Database Migration Service, and then select **Resource providers**.

   :::image type="content" source="../media/portal-select-resource-provider.png" alt-text="Screenshot showing resource providers." lightbox="../media/portal-select-resource-provider.png":::

1. Search for migration, and then select **Register** for **Microsoft.DataMigration**.

   :::image type="content" source="../media/portal-register-resource-provider.png" alt-text="Screenshot of the Register resource provider screen.":::
