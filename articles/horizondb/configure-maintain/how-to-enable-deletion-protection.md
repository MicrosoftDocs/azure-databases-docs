---
title: Enable Deletion Protection in Azure HorizonDB
description: This article describes how to enable deletion protection in an Azure HorizonDB instance using Azure Resource Manager locks.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
# customer intent: As a user, I want to learn how to prevent accidental deletion of an Azure HorizonDB instance by enabling a CanNotDelete lock.
---

# Protect with Resource Locks in Azure HorizonDB

You can apply **management locks**-specifically **CanNotDelete** or **ReadOnly**-to Azure HorizonDB to safeguard them from accidental deletion or modifications. These locks operate at the control plane and override user permissions, offering an additional layer of resource protection.

## Lock Types

| Lock Type | Description |
| --- | --- |
| **CanNotDelete** | Users can read and modify settings, but can't delete the server resource. |
| **ReadOnly** | Users can only read; they can't update or delete the server. Similar to the *Reader* role. |

## Prerequisites

- An existing Azure HorizonDB instance within your subscription.

## Lock Behavior & Inheritance

- Locks can be applied at the **subscription**, **resource group**, or **server** level.
- Child resources inherit locks from their parents; the **most restrictive lock** takes precedence.
- Locks restrict ARM operations (Portal, CLI, API) but do **not** block SQL data plane actions (like editing tables or schemas).

## Apply Locks Using Azure CLI or ARM

### Azure CLI

<a id="to-apply-a-cannotdelete-lock-on-an-existing-server"></a>

##### Apply a CanNotDelete lock on an existing server

```azurecli-interactive
az lock create \
  --name PreventDelete \
  --lock-type CanNotDelete \
  --resource-group MyResourceGroup \
  --resource-type Microsoft.DBforPostgreSQL/flexibleServers \
  --resource-name MyFlexibleServer
```

<a id="to-remove-the-lock"></a>

##### Remove the lock

```azurecli-interactive
az lock delete \
  --name PreventDelete \
  --resource-group MyResourceGroup \
  --resource-type Microsoft.DBforPostgreSQL/flexibleServers \
  --resource-name MyFlexibleServer
```

### ARM Template

When applying a lock to an Azure PostgreSQL DB resource, use the [Microsoft.Authorization/locks](/azure/templates/microsoft.authorization/2017-04-01/locks) Azure Resource Manager (ARM) resource.

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

Creating or deleting locks requires permissions for `Microsoft.Authorization/locks/*`, which are available in built-in roles like **Owner** and **User Access Administrator**.

## Best Practices & Considerations

- Ideal for **production workloads** that require deletion safeguards.
- For **high availability or backend servers**, consider implementing locks at deployment time.
- Ensure **network resources (VNETs/subnets)** are unlocked before provisioning, then reapply locks post-deployment to avoid interference.
- While locks prevent server deletion, they do **not** restrict destructive SQL operations. Enforce SQL-level policies as needed.

## Conclusion

Using ARM management locks helps protect your PostgreSQL flexible server instance from accidental deletions without impeding daily operations. Consider adding this to your automation scripts and deployment policies for safer production workflows.

---

## Related content

- [Overview of Azure Resource Manager Locks](/azure/azure-resource-manager/management/lock-resources)
