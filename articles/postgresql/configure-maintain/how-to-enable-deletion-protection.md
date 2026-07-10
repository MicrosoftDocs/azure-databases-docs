---
title: Enable deletion protection
description: This article describes how to enable deletion protection in an Azure Database for PostgreSQL flexible server using Azure Resource Manager locks.
#customer intent: As a user, I want to learn how to prevent accidental deletion of an Azure Database for PostgreSQL flexible server by enabling a CanNotDelete lock.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
ai-usage: ai-assisted
---

# Protect Azure Database for PostgreSQL flexible server with resource locks

To protect Azure Database for PostgreSQL flexible servers from accidental deletion or modification, apply **management locks** such as **CanNotDelete** or **ReadOnly**. These locks work at the control plane and override user permissions, so they add an extra layer of protection for your resources.

## Lock types
| Lock type      | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| **CanNotDelete** | Users can read and change settings, but they can't delete the server resource. |
| **ReadOnly**      | Users can only read; they can't update or delete the server. Similar to the *Reader* role. |

## Prerequisites
- An existing Azure Database for PostgreSQL flexible server in your subscription.

## Lock behavior and inheritance
- You can apply locks at the **subscription**, **resource group**, or **server** level.  
- Child resources inherit locks from their parents. The **most restrictive lock** always takes priority.  
- Locks restrict Azure Resource Manager operations (Portal, CLI, API) but don't block SQL data plane actions (like editing tables or schemas).  

## Apply locks using Azure CLI or ARM

### Azure CLI

##### To apply a **CanNotDelete** lock on an existing server:

```azurecli-interactive
az lock create \
  --name PreventDelete \
  --lock-type CanNotDelete \
  --resource-group MyResourceGroup \
  --resource-type Microsoft.DBforPostgreSQL/flexibleServers \
  --resource-name MyFlexibleServer
```

##### To remove the lock:

```azurecli-interactive
az lock delete \
  --name PreventDelete \
  --resource-group MyResourceGroup \
  --resource-type Microsoft.DBforPostgreSQL/flexibleServers \
  --resource-name MyFlexibleServer
```

### ARM template

When you apply a lock to an Azure PostgreSQL DB resource, use the [Microsoft.Authorization/locks](/azure/templates/microsoft.authorization/2017-04-01/locks) Azure Resource Manager (ARM) resource.

```json
{
  "type": "Microsoft.Authorization/locks",
  "apiVersion": "2016-09-01",
  "name": "serverLock",
  "scope": "[resourceId('Microsoft.DBforPostgreSQL/flexibleServers', parameters('serverName'))]",
  "properties": {
    "level": "CanNotDelete",
    "notes": "Prevent accidental deletion of PostgreSQL server."
  }
}
```

## Permissions

To create or delete locks, you need permissions for `Microsoft.Authorization/locks/*`. You can get these permissions from built-in roles like **Owner** and **User Access Administrator**.

## Best practices and considerations

* Use locks for **production workloads** that require deletion safeguards.
* For **high availability or backend servers**, consider implementing locks at deployment time.
* Ensure **network resources (VNETs/subnets)** are unlocked before provisioning, then reapply locks post-deployment to avoid interference.
* While locks prevent server deletion, they don't restrict destructive SQL operations. Enforce SQL-level policies as needed.

## Conclusion
Using ARM management locks helps protect your PostgreSQL flexible server from accidental deletions without impeding daily operations. Consider adding this step to your automation scripts and deployment policies for safer production workflows.

---

## Related content

- [Overview of Azure Resource Manager Locks](/azure/azure-resource-manager/management/lock-resources)
