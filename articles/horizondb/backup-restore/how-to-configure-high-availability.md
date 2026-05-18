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

# Configure high availability in Azure HorizonDB

This article describes how to enable or disable high availability (HA) on your Azure HorizonDB instance by using the Azure portal. 

The high-availability feature deploys primary and standby compute replicas in separate availability zones. You can enable high availability during or after the creation of your Azure HorizonDB instance.

## Enable high availability for existing servers

You can enable high availability on an existing Azure HorizonDB cluster at any time. When you enable high availability, the service creates a standby compute replica that mirrors your primary server. 

### [Portal](#tab/portal-enable-existing-server)

1. In the [Azure portal](https://portal.azure.com/), select your Azure HorizonDB cluster.

2. On the left menu, in the **Settings** section, select **High availability**. You have two choices:

- **Zone Redundant- Replica in a different availability zone**- When you select this option, service creates the standby compute in a different availability zone than the primary. This option gives you the best protection against zone-level failures.
- **Disabled**- High availability isn't configured.

3.  select the **Zone Redundant- Replica in a different availability zone** option and click **save**

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-enabled.png" alt-text="Screenshot that shows the pane for configuring high availability." lightbox="media/how-to-configure-high-availability/high-availability-enabled.png":::

4. A dialog appears indicating that high availability is being enabled. Once the process completes, high availability is successfully configured on your HorizonDB cluster.

## Enable High Availability during server provisioning

You can configure high availability when you first create your Azure HorizonDB cluster. By enabling high availability during provisioning, you deploy a standby compute replica in a different availability zone, so you get immediate protection against zone or server failures.

### [Portal](#tab/portal-enable-new-server)

1. In the [Azure portal](https://portal.azure.com/), during provisioning of a new Azure HorizonDB cluster, go to the **High availability** section. 

You have two choices:

- **Zone Redundant- Replica in a different availability zone**- When you select this option, service creates the standby compute in a different availability zone than the primary. This option gives you the best protection against zone-level failures.
- **Disabled**- High availability isn't configured.

2.  select the **Zone Redundant- Replica in a different availability zone** option and click **save**

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-provisioning.png" alt-text="Screenshot that shows the selection of high  availability option  for primary server." lightbox="media/how-to-configure-high-availability/high-availability-provisioning.png":::

## Related content
- [Overview of business continuity in Azure HorizonDB](../backup-restore/concepts-business-continuity.md)
