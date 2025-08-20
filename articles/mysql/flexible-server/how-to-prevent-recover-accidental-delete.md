---
title: Prevent and Recover from an Accidental Deletion
description: This article describes how to prevent and recover from an accidental deletion of an  Azure Database for MySQL flexible server.
author: ramnov  
ms.author: ramkumarch  
ms.reviewer: maghan
ms.date: 08/20/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
---

# Prevent and recover from an accidental deletion of an Azure Database for MySQL flexible server

Accidentally deleting critical Azure resources, such as Azure Database for MySQL flexible servers, can disrupt operations and compromise business continuity. This article outlines how to prevent accidental deletions by using Azure Resource Locks and Azure Policy, and how to recover deleted servers by using Azure CLI.

Azure provides built-in mechanisms to safeguard resources from unintended deletion. These mechanisms include:

- **Azure Resource Locks**: Prevent deletion of resources or resource groups.
- **Azure Policy**: Enforce organizational standards and protect critical infrastructure.
- **Azure CLI Recovery Commands**: Restore deleted servers when possible.

## Prevent an accidental deletion

You can apply resource locks at both the resource and resource group levels. These locks override user permissions to prevent deletion.

### Lock a MySQL Flexible Server

```bash
az lock create \
 --name "PreventDeleteLock" \
  --resource-group <RESOURCE_GROUP_NAME> \
 --resource-name <MYSQL_SERVER_NAME> \
  --resource-type "Microsoft.DBforMySQL/flexibleServers" \
 --lock-type CanNotDelete
```

### Verify locks

```bash
az lock list \
 --resource-group <RESOURCE_GROUP_NAME> \
  --resource-name <MYSQL_SERVER_NAME> \
 --resource-type "Microsoft.DBforMySQL/flexibleServers" \
  -o table
```

### Remove locks

```bash
az lock delete \
 --name "PreventDeleteLock" \
  --resource-group <RESOURCE_GROUP_NAME> \
 --resource-name <MYSQL_SERVER_NAME> \
  --resource-type "Microsoft.DBforMySQL/flexibleServers"
```

### Lock the entire resource group

```bash
az lock create \
 --name "PreventDeleteGroupLock" \
  --resource-group <RESOURCE_GROUP_NAME> \
 --lock-type CanNotDelete
```

## Recover a deleted server

If you accidentally delete a server, you can recover it by using Azure CLI and point-in-time restore (PITR), if backups are available.

### Restore with Azure CLI

```bash
az mysql flexible-server restore \
 --resource-group <RESOURCE_GROUP_NAME> \
  --name <NEW_SERVER_NAME> \
 --source-server <DELETED_SERVER_NAME> \
  --restore-time <TIMESTAMP>
```

> [!NOTE]
> Make sure you replace `<TIMESTAMP>` with the time just before deletion.

## Best practices

- Apply `CanNotDelete` locks to critical resources and resource groups.
- Use Azure Policy to enforce lock usage across subscriptions.
- Regularly test restore procedures to ensure recovery readiness.
- Monitor lock configurations and audit changes by using Azure Activity Logs.

## Related articles

- [Azure Database for MySQL overview](overview.md)
