---
title: Enable Deletion Protection in Azure HorizonDB
description: This article describes how to enable deletion protection in an Azure HorizonDB instance using Azure Resource Manager locks.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
# customer intent: As a user, I want to learn how to prevent accidental deletion of an Azure HorizonDB instance by enabling a CanNotDelete lock.
---

# Protect against accidental deletion with resource locks for Azure HorizonDB (Preview)

You can apply **management locks**-specifically **Delete** or **ReadOnly**-to Azure HorizonDB to safeguard them from accidental deletion or modifications. These locks operate at the control plane and override user permissions, offering an extra layer of resource protection.

## Lock Types

| Lock Type | Description |
| --- | --- |
| **Delete** | Users can read and modify settings, but can't delete the server resource. |
| **ReadOnly** | Users can only read; they can't update or delete the server. Similar to the *Reader* role. |

## Prerequisites

- An existing Azure HorizonDB instance within your subscription.

## Lock behavior and inheritance

- Locks can be applied at the **subscription**, **resource group**, or **server** level.
- Child resources inherit locks from their parents; the **most restrictive lock** takes precedence.
- Locks restrict Azure Resource Manager operations (Portal, CLI, API) but do **not** block data plane actions (like editing tables or schemas).

## Apply Locks Using Portal

### [Portal](#tab/lock-compute)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB.

1. In the resource menu, under **Settings**, select **Locks**.

1. Select the **Add** button, provide the name of your lock, and choose **Delete** as the type of lock.

   :::image type="content" source="media/how-to-enable-deletion-protection/delete-lock.png" alt-text="Screenshot showing the Add lock dialog to add a lock to protect your resource against accidental deletions." lightbox="media/how-to-enable-deletion-protection/delete-lock.png":::

1. Select **OK**. You should see a notification message indicating that the lock was created successfully.

   :::image type="content" source="media/how-to-enable-deletion-protection/success-lock.png" alt-text="Screenshot success lock page." lightbox="media/how-to-enable-deletion-protection/success-lock.png":::

## Permissions

Creating or deleting locks requires permissions for `Microsoft.Authorization/locks/*`, which are available in built-in roles like **Owner** and **User Access Administrator**.

## Best practices and considerations

- Ideal for **production workloads** that require deletion safeguards.
- For **high availability or backend servers**, consider implementing locks at deployment time.
- Ensure **network resources (virtual networks and subnets)** are unlocked before provisioning, then reapply locks post-deployment to avoid interference.
- While locks prevent server deletion, they do **not** restrict destructive SQL operations. Enforce SQL-level policies as needed.

---

## Related content

- [Overview of Resource Manager locks](/azure/azure-resource-manager/management/lock-resources)
- [Backups in Azure HorizonDB (Preview)](../backup-restore/concepts-backup-restore.md)
