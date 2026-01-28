---
title: Custom Roles for MySQL to Azure Database for MySQL Migrations Using Database Migration Service
titleSuffix: Azure Database Migration Service
description: Learn to use the custom roles for MySQL to Azure Database for MySQL migrations.
author: saikondapalli11
ms.author: skondapalli
ms.reviewer: randolphwest
ms.date: 10/16/2025
ms.service: azure-database-migration-service
ms.topic: how-to
ms.collection:
  - sql-migration-content
---

# Custom roles for MySQL to Azure Database for MySQL migrations using Database Migration Service

This article explains how to set up a custom role for MySQL to Azure Database for MySQL migrations using DMS.

The role has no permission to create a new Database Migration Service and no permission to create a database migration project. Meaning the user assigned to the custom role will need to have an already created Database Migration Service and migration project under the assigned resource group. The user will then be able to create and run migration activities under the migration project.

```json
{
    "properties": {
        "roleName": "DmsCustomRoleDemoforMySQL",
        "description": "",
        "assignableScopes": [
            "/subscriptions/<DMSSubscription>/resourceGroups/<dmsServiceRG>"
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.DataMigration/locations/operationResults/read",
                    "Microsoft.DataMigration/locations/operationStatuses/read",
                    "Microsoft.DataMigration/services/read",
                    "Microsoft.DataMigration/services/stop/action",
                    "Microsoft.DataMigration/services/start/action",
                    "Microsoft.DataMigration/services/checkStatus/*",
                    "Microsoft.DataMigration/services/configureWorker/action",
                    "Microsoft.DataMigration/services/addWorker/action",
                    "Microsoft.DataMigration/services/removeWorker/action",
                    "Microsoft.DataMigration/services/updateAgentConfig/action",
                    "Microsoft.DataMigration/services/slots/read",
                    "Microsoft.DataMigration/services/projects/*",
                    "Microsoft.DataMigration/services/serviceTasks/read",
                    "Microsoft.DataMigration/services/serviceTasks/write",
                    "Microsoft.DataMigration/services/serviceTasks/delete",
                    "Microsoft.DataMigration/services/serviceTasks/cancel/action",
                    "Microsoft.DBforMySQL/flexibleServers/read",
                    "Microsoft.DBforMySQL/flexibleServers/databases/read",
                    "Microsoft.DBforMySQL/servers/read",
                    "Microsoft.DBforMySQL/servers/databases/read",
                    "Microsoft.Resources/subscriptions/resourceGroups/read",
                    "Microsoft.DataMigration/skus/read"
                ],
                "notActions": [],
                "dataActions": [],
                "notDataActions": []
            }
        ]
    }
}
```

You can use either the Azure portal, AZ PowerShell, Azure CLI or Azure REST API to create the roles.

For more information, see the articles [Create custom roles using the Azure portal](/azure/role-based-access-control/custom-roles-portal) and [Azure custom roles](/azure/role-based-access-control/custom-roles).

## Role assignment

To assign a role to users, open the Azure portal, perform the following steps:

1. Navigate to the resource, go to **Access Control**, and then scroll to find the custom roles you created.

1. Select the appropriate role, select the User, and then save the changes.

The user now appears listed on the **Role assignments** tab.

## Related content

- [What is Azure Database for MySQL - Flexible Server?](../mysql/flexible-server/overview.md)
- [What is Azure Database Migration Service?](dms-overview.md)
- [Known Issues With Migrations To Azure Database for MySQL](known-issues-azure-mysql-fs-online.md)
- [Troubleshoot common Azure Database Migration Service (classic) issues and errors](known-issues-troubleshooting-dms.md)
- [Troubleshoot DMS errors when connecting to source databases](known-issues-troubleshooting-dms-source-connectivity.md)
