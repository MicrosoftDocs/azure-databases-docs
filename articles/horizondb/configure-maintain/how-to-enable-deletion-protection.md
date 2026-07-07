---
title: Enable Deletion Protection in Azure HorizonDB
description: This article describes how to enable deletion protection in an Azure HorizonDB instance using Azure Resource Manager locks.
#customer intent: As a user, I want to protect my Azure HorizonDB cluster from accidental deletion so that I can prevent data loss and service disruptions.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 07/06/2026
ms.service: azure-horizondb
ms.subservice: configuration
ms.topic: how-to
---

# Protect against accidental deletion by using resource locks in Azure HorizonDB (Preview)

To protect Azure HorizonDB from accidental deletion or modification, apply **management locks** - specifically **Delete** or **ReadOnly** locks. These locks work at the control plane and override user permissions, so they add an extra layer of protection for your resources.

## Lock types

| Lock type | Description |
| --- | --- |
| **Delete** | Users can read and change settings, but they can't delete the server resource. |
| **ReadOnly** | Users can only read; they can't update or delete the server. Similar to the *Reader* role. |

## Prerequisites

- An existing Azure HorizonDB instance in your subscription.

## Lock behavior and inheritance

- You can apply locks at the **subscription**, **resource group**, or **server** level.
- Child resources inherit locks from their parents. The **most restrictive lock** always takes priority.
- Locks restrict Azure Resource Manager operations (Portal, CLI, API) but they don't block data plane actions, like editing tables or schemas.

## Apply locks by using the portal

### [Portal](#tab/lock-compute)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB.

1. In the resource menu, under the **Settings** section, select **Locks**.

1. Select the **Add** button, enter the name of your lock, and choose **Delete** as the type of lock.

   :::image type="content" source="media/how-to-enable-deletion-protection/delete-lock.png" alt-text="Screenshot showing the Add lock dialog to add a lock to protect your resource against accidental deletions." lightbox="media/how-to-enable-deletion-protection/delete-lock.png":::

1. Select **OK**. You see a notification message indicating that the lock was created successfully.

   :::image type="content" source="media/how-to-enable-deletion-protection/success-lock.png" alt-text="Screenshot success lock page." lightbox="media/how-to-enable-deletion-protection/success-lock.png":::

## Permissions

To create or delete locks, you need permissions for `Microsoft.Authorization/locks/*`. You can get these permissions from built-in roles like **Owner** and **User Access Administrator**.

## Best practices and considerations

- Use locks for **production workloads** that require deletion safeguards.
- For **high availability or backend servers**, consider implementing locks at deployment time.
- Ensure **network resources (virtual networks and subnets)** are unlocked before provisioning, then reapply locks post-deployment to avoid interference.
- While locks prevent server deletion, they don't restrict destructive SQL operations. Enforce SQL-level policies as needed.

---

## Related content

- [Overview of Resource Manager locks](/azure/azure-resource-manager/management/lock-resources)
- [Backups in Azure HorizonDB (Preview)](../backup-restore/concepts-backup-restore.md)
