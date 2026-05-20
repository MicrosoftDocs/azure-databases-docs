---
title: Configure High Availability in Azure HorizonDB
description: This article describes how to configure and operate high availability in Azure HorizonDB.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: high-availability
ms.topic: how-to
# customer intent: As a user, I want to learn how to configure and operate high availability in Azure HorizonDB.
---

# Configure high availability in Azure HorizonDB (Preview)

This article describes how to enable or disable high availability (HA) on your Azure HorizonDB instance by using the Azure portal.

The high-availability feature deploys physically separate primary and standby compute replicas in different availability zones. You can enable high availability during or after the creation of your Azure HorizonDB instance.


## Enable high availability for existing servers

You can enable high availability on an existing Azure HorizonDB instance at any time. When you enable high availability, the service creates a standby compute replica that mirrors your primary server.

### [Portal](#tab/portal-enable-existing-server)

1. In the [Azure portal](https://portal.azure.com/), select your Azure HorizonDB instance.

2. On the left menu, in the **Settings** section, select **High availability**.

You have two choices:

- **Disabled** - High availability isn't configured.
- **Zone redundant - Replica in a different availability zone** - a stand by  compute replica is provisioned in a different availability zone.

3. select the **Zone redundant - Replica in a different availability zone** option.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-enabled" alt-text="Screenshot that shows the pane for configuring high availability." lightbox="media/how-to-configure-high-availability/high-availability-enabled.png":::

4. When you're done configuring the settings, select **Save** to apply the changes.

5. A deployment starts. When it finishes, a notification shows that you successfully enabled high availability.


## Enable High Availability during server provisioning

You can configure high availability when you first create your Azure HorizonDB instance. By enabling high availability during provisioning, you deploy a standby replica alongside your primary server, so you get immediate protection against zone or server failures.

### [Portal](#tab/portal-enable-new-server)

1.  In the [Azure portal](https://portal.azure.com/), select Azure HorizonDB Service and Click Create.

      :::image type="content" source="media/how-to-configure-high-availability/high-availability-enabled" alt-text="Screenshot that shows the pane for configuring high availability." lightbox="media/how-to-configure-high-availability/high-availability-enabled.png":::


2. Provide your cluster name and go to  **High availability** section.

You have two High availability mode choices:

- **Disabled** - High availability isn't configured.
- **Zone redundant - Replica in a different availability zone** - a stand by  compute replica is provisioned in a different availability zone.

3. select the **Zone redundant - Replica in a different availability zone** option.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-provisioning" alt-text="Screenshot that shows the pane for configuring high availability during provisioning." lightbox="media/how-to-configure-high-availability/high-availability-provisioning.png":::

4. When you're done configuring the settings, select  **Review + create** to review the changes then click **create**

5. A deployment starts. Deployment begins. After completion, a notification confirms that the HorizonDB cluster has been successfully created with high availability enabled.


## Related content

- [Overview of business continuity in Azure HorizonDB](../backup-restore/concepts-business-continuity.md)
