---
title: Manage read replicas - Azure portal, REST API
description: Learn how to manage read replicas for Azure Database for PostgreSQL flexible server from the Azure portal, CLI, and REST API.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - ignite-2023
  - devx-track-azurecli
---

# Create and manage read replicas in Azure Database for PostgreSQL flexible server from the Azure portal, CLI, or REST API

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

In this article, you learn how to create and manage read replicas in Azure Database for PostgreSQL Flexible Server from the Azure portal, CLI, and REST API. To learn more about read replicas, see the [overview](concepts-read-replicas.md).

## Prerequisites

[Create an Azure Database for PostgreSQL flexible server](quickstart-create-server.md) to be the primary server.

> [!NOTE]  
> When deploying read replicas for persistent heavy write-intensive primary workloads, the replication lag could continue to grow and might never catch up with the primary. This might also increase storage usage at the primary as the WAL files are only deleted once received at the replica.

## Review primary settings

Before setting up a read replica for Azure Database for PostgreSQL Flexible Server, ensure the primary server is configured to meet the necessary prerequisites. Specific settings on the primary server can affect the ability to create replicas.

**Storage auto-grow**: Storage autogrow settings on the primary server and its read replicas must adhere to specific guidelines to ensure consistency and prevent replication disruptions. Refer to the [Storage autogrow](concepts-read-replicas.md#storage-autogrow) for detailed rules and settings.

**Premium SSD v2**: The current release doesn't support the creation of read replicas for primary servers using Premium SSD v2 storage. If your workload requires read replicas, choose a different storage option for the primary server.


#### [Portal](#tab/portal)

1.  In the [Azure portal](https://portal.azure.com/), choose the Azure Database for PostgreSQL flexible server instance you want for the replica.

2.  On the **Overview** dialog, note the PostgreSQL version (ex `15.4`). Also, note the region your primary is deployed to (ex., `East US`).

    :::image type="content" source="./media/how-to-read-replicas-portal/primary-settings.png" alt-text="Screenshot of review primary settings." lightbox="./media/how-to-read-replicas-portal/primary-settings.png":::

3.  On the server sidebar, under **Settings**, select **Compute + storage**.

4.  Review and note the following settings:

      - Compute Tier, Processor, Size (ex `Standard_D4ads_v5`).
    
      - Storage
        - Storage size (ex `128GB`)
        - Autogrow
    
      - High Availability
        - Enabled / Disabled
        - Availability zone settings
    
      - Backup settings
        - Retention period
        - Redundancy Options

5.  Under **Settings**, select **Networking.**

6. Review the network settings.

      :::image type="content" source="./media/how-to-read-replicas-portal/primary-compute.png" alt-text="Screenshot of server settings." lightbox="./media/how-to-read-replicas-portal/primary-compute.png":::

#### [CLI](#tab/cli)

> [!NOTE]  
> The commands provided in this guide are applicable for Azure CLI version 2.56.0 or higher. Ensure that you have the required version or a later one installed to execute these commands successfully. You can check your current Azure CLI version by running `az --version` in your command line interface. To update Azure CLI to the latest version, follow the instructions provided in the [Azure CLI documentation](/cli/azure/update-azure-cli).


To view the configuration and current status of an Azure PostgreSQL Flexible Server, use the `az postgres flexible-server show` command. This command provides detailed information about the specified server.

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource-group> \
  --name <server-name>
```

Replace `<resource-group>` and `<server-name>` with your specific resource group and the name of the server you wish to view.

Review and note the following settings:

  - Compute Tier, Processor, Size (ex `Standard_D8ads_v5`).
  - Storage
    - Type
    - Storage size (ex `128`)
    - autogrow
  - High Availability
    - Enabled / Disabled
    - Availability zone settings
  - Backup settings
    - Retention period
    - Redundancy Options

**Sample response**

```json
{
  "administratorLogin": "myadmin",
  "administratorLoginPassword": null,
  "authConfig": {
    "activeDirectoryAuth": "Disabled",
    "passwordAuth": "Enabled",
    "tenantId": null
  },
  "availabilityZone": "2",
  "backup": {
    "backupRetentionDays": 7,
    "earliestRestoreDate": "2024-01-06T11:43:44.485537+00:00",
    "geoRedundantBackup": "Disabled"
  },
  "createMode": null,
  "dataEncryption": {
    "geoBackupEncryptionKeyStatus": null,
    "geoBackupKeyUri": null,
    "geoBackupUserAssignedIdentityId": null,
    "primaryEncryptionKeyStatus": null,
    "primaryKeyUri": null,
    "primaryUserAssignedIdentityId": null,
    "type": "SystemManaged"
  },
  "fullyQualifiedDomainName": "{serverName}.postgres.database.azure.com",
  "highAvailability": {
    "mode": "Disabled",
    "standbyAvailabilityZone": null,
    "state": "NotEnabled"
  },
  "id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBforPostgreSQL/flexibleServers/{serverName}",
  "identity": null,
  "location": "East US",
  "maintenanceWindow": {
    "customWindow": "Disabled",
    "dayOfWeek": 0,
    "startHour": 0,
    "startMinute": 0
  },
  "minorVersion": "0",
  "name": "{serverName}",
  "network": {
    "delegatedSubnetResourceId": null,
    "privateDnsZoneArmResourceId": null,
    "publicNetworkAccess": "Enabled"
  },
  "pointInTimeUtc": null,
  "privateEndpointConnections": null,
  "replica": {
    "capacity": 5,
    "promoteMode": null,
    "promoteOption": null,
    "replicationState": null,
    "role": "Primary"
  },
  "replicaCapacity": 5,
  "replicationRole": "Primary",
  "resourceGroup": "{resourceGroupName}",
  "sku": {
    "name": "Standard_D8ads_v5",
    "tier": "GeneralPurpose"
  },
  "sourceServerResourceId": null,
  "state": "Ready",
  "storage": {
    "autoGrow": "Disabled",
    "iops": 500,
    "storageSizeGb": 128,
    "throughput": null,
    "tier": "P10",
    "type": ""
  },
  "systemData": {
    "createdAt": "2023-11-08T11:27:48.972812+00:00",
    "createdBy": null,
    "createdByType": null,
    "lastModifiedAt": null,
    "lastModifiedBy": null,
    "lastModifiedByType": null
  },
  "tags": {},
  "type": "Microsoft.DBforPostgreSQL/flexibleServers",
  "version": "16"
}

```

#### [REST API](#tab/restapi)

To obtain information about the configuration of a server in Azure Database for PostgreSQL Flexible Server, especially to view settings for recently introduced features like storage autogrow or private link, you should use the latest API version `2023-06-01-preview`. The `GET` request would be formatted as follows:

```http
https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBforPostgreSQL/flexibleServers/{serverName}?api-version=2023-06-01-preview
```

Replace `{subscriptionId}`, `{resourceGroupName}`, and `{serverName}` with your Azure subscription ID, the resource group name, and the name of the primary server you want to review, respectively. This request gives you access to the configuration details of your primary server, ensuring it's properly set up for creating a read replica.

Review and note the following settings:

  - Compute Tier, Processor, Size (ex `Standard_D8ads_v5`).
  - Storage
    - Type
    - Storage size (ex `128`)
    - autogrow
  - Network
  - High Availability
    - Enabled / Disabled
    - Availability zone settings
  - Backup settings
    - Retention period
    - Redundancy Options


**Sample response**

```json
{
    "sku": {
        "name": "Standard_D8ads_v5",
        "tier": "GeneralPurpose"
    },
    "systemData": {
        "createdAt": "2023-11-22T16:11:42.2461489Z"
    },
    "properties": {
        "replica": {
            "role": "Primary",
            "capacity": 5
        },
        "storage": {
            "type": "",
            "iops": 500,
            "tier": "P10",
            "storageSizeGB": 128,
            "autoGrow": "Disabled"
        },
        "network": {
            "publicNetworkAccess": "Enabled"
        },
        "dataEncryption": {
            "type": "SystemManaged"
        },
        "authConfig": {
            "activeDirectoryAuth": "Disabled",
            "passwordAuth": "Enabled"
        },
        "fullyQualifiedDomainName": "{serverName}.postgres.database.azure.com",
        "version": "15",
        "minorVersion": "4",
        "administratorLogin": "myadmin",
        "state": "Ready",
        "availabilityZone": "1",
        "backup": {
            "backupRetentionDays": 7,
            "geoRedundantBackup": "Disabled",
            "earliestRestoreDate": "2023-11-23T12:55:33.3443218+00:00"
        },
        "highAvailability": {
            "mode": "Disabled",
            "state": "NotEnabled"
        },
        "maintenanceWindow": {
            "customWindow": "Disabled",
            "dayOfWeek": 0,
            "startHour": 0,
            "startMinute": 0
        },
        "replicationRole": "Primary",
        "replicaCapacity": 5
    },
    "location": "East US",
    "tags": {},
    "id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBforPostgreSQL/flexibleServers/{serverName}",
    "name": "{serverName}",
    "type": "Microsoft.DBforPostgreSQL/flexibleServers"
}
```

---

## Create a read replica

To create a read replica, follow these steps:

#### [Portal](#tab/portal)

1.  Select an existing Azure Database for PostgreSQL flexible server instance to use as the primary server.

2.  On the server sidebar, under **Settings**, select **Replication**.

3.  Select **Create replica**.

    :::image type="content" source="./media/how-to-read-replicas-portal/add-replica.png" alt-text="Screenshot of create a replica action." lightbox="./media/how-to-read-replicas-portal/add-replica.png":::

4.  Enter the Basics form with the following information.

    :::image type="content" source="./media/how-to-read-replicas-portal/basics.png" alt-text="Screenshot showing entering the basics information." lightbox="./media/how-to-read-replicas-portal/basics.png":::

5.  Select **Review + create** to confirm the creation of the replica or **Next: Networking** if you want to add, delete, or modify any firewall rules.

    :::image type="content" source="./media/how-to-read-replicas-portal/networking.png" alt-text="Screenshot of modify firewall rules action." lightbox="./media/how-to-read-replicas-portal/networking.png":::

6.  Leave the remaining defaults and then select the **Review + create** button at the bottom of the page or proceed to the next forms to add tags or change data encryption method.

7.  Review the information in the final confirmation window. When you're ready, select **Create**. A new deployment is created.

    :::image type="content" source="./media/how-to-read-replicas-portal/replica-review.png" alt-text="Screenshot of reviewing the information in the final confirmation window.":::

8.  During the deployment, you see the primary in `Updating` state.
    
    :::image type="content" source="./media/how-to-read-replicas-portal/primary-updating.png" alt-text="Screenshot of primary entering into updating status." lightbox="./media/how-to-read-replicas-portal/primary-updating.png":::
    After the read replica is created, it can be viewed from the **Replication** window.

    :::image type="content" source="./media/how-to-read-replicas-portal/list-replica.png" alt-text="Screenshot of viewing the new replica in the replication window." lightbox="./media/how-to-read-replicas-portal/list-replica.png":::

#### [CLI](#tab/cli)

You can create a read replica for your Azure PostgreSQL Flexible Server by using the [`az postgres flexible-server replica create`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-replica-create) command. 

```azurecli-interactive
az postgres flexible-server replica create \
  --replica-name <replica-name> \
  --resource-group <resource-group> \
  --source-server <source-server-name> \
  --location <location>
```

Replace `<replica-name>`, `<resource-group>`, `<source-server-name>`, and `<location>` with your specific values.

After the read replica is created, the properties of all servers, which are replicas of a primary replica can be obtained by using the [`az postgres flexible-server replica create`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-replica-list) command. 

```azurecli-interactive
az postgres flexible-server replica list \
  --name <source-server-name> \
  --resource-group <resource-group>
```

Replace `<source-server-name>`, and `<resource-group>` with your specific values.



#### [REST API](#tab/restapi)

Initiate an `HTTP PUT` request by using the [servers create API](/rest/api/postgresql/flexibleserver/servers/create):

```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{replicaserverName}?api-version=2022-12-01
```

Here, you need to replace `{subscriptionId}`, `{resourceGroupName}`, and `{replicaserverName}` with your specific Azure subscription ID, the name of your resource group, and the desired name for your read replica, respectively.

```json
{
  "location": "eastus",
  "properties": {
    "createMode": "Replica",
    "SourceServerResourceId": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{sourceserverName}"
  }
}
```

After the read replica is created, the properties of all servers, which are replicas of a primary replica can be obtained by initiating an `HTTP GET` request by using [replicas list by server API](/rest/api/postgresql/flexibleserver/replicas/list-by-server): 

```http
GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{sourceserverName}/replicas?api-version=2022-12-01
```

Here, you need to replace `{subscriptionId}`, `{resourceGroupName}`, and `{sourceserverName}` with your specific Azure subscription ID, the name of your resource group, and the name you assigned to your primary replica, respectively.

```json
[
  {
    "administratorLogin": null,
    "administratorLoginPassword": null,
    "authConfig": null,
    "availabilityZone": null,
    "backup": {
      "backupRetentionDays": null,
      "earliestRestoreDate": "2023-11-23T12:55:33.3443218+00:00",
      "geoRedundantBackup": "Disabled"
    },
    "createMode": null,
    "dataEncryption": {
      "geoBackupEncryptionKeyStatus": null,
      "geoBackupKeyUri": null,
      "geoBackupUserAssignedIdentityId": null,
      "primaryEncryptionKeyStatus": null,
      "primaryKeyUri": null,
      "primaryUserAssignedIdentityId": null,
      "type": "SystemManaged"
    },
    "fullyQualifiedDomainName": null,
    "highAvailability": null,
    "id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBforPostgreSQL/flexibleServers/{replicaserverName}",
    "identity": null,
    "location": "eastus",
    "maintenanceWindow": {
      "customWindow": "Disabled",
      "dayOfWeek": 0,
      "startHour": 0,
      "startMinute": 0
    },
    "minorVersion": null,
    "name": "{replicaserverName}",
    "network": {
      "delegatedSubnetResourceId": null,
      "privateDnsZoneArmResourceId": null,
      "publicNetworkAccess": "Disabled"
    },
    "pointInTimeUtc": null,
    "privateEndpointConnections": null,
    "replica": {
      "capacity": null,
      "promoteMode": null,
      "promoteOption": null,
      "replicationState": "Active",
      "role": "AsyncReplica"
    },
    "replicaCapacity": null,
    "replicationRole": "AsyncReplica",
    "resourceGroup": "{resourceGroupName}",
    "sku": {
      "name": "",
      "tier": null
    },
    "sourceServerResourceId": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBforPostgreSQL/flexibleServers/{serverName}",
    "state": "Ready",
    "storage": {
      "autoGrow": "Disabled",
      "iops": null,
      "storageSizeGb": 0,
      "throughput": null,
      "tier": null,
      "type": null
    },
    "systemData": {
      "createdAt": "2023-11-22T17:11:42.2461489Z",
      "createdBy": null,
      "createdByType": null,
      "lastModifiedAt": null,
      "lastModifiedBy": null,
      "lastModifiedByType": null
    },
    "tags": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers",
    "version": null
  }
]
```
---

- Set the replica server name.

   > [!TIP]  
   > It is a Cloud Adoption Framework (CAF) best practice to [use a resource naming convention](/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming) that will allow you to easily determine what instance you are connecting to or managing and where it resides.

- Select a location different from your primary but note that you can select the same region.

   > [!TIP]  
   > To learn more about which regions you can create a replica in, visit the [read replica concepts article](concepts-read-replicas.md).

- Set the compute and storage to what you recorded from your primary. If the displayed compute doesn't match, select **Configure server** and select the appropriate one.

   > [!NOTE]  
   > If you select a compute size smaller than the primary, the deployment will fail. Also be aware that the compute size might not be available in a different region.

    :::image type="content" source="./media/how-to-read-replicas-portal/replica-compute.png" alt-text="Screenshot of chose the compute size.":::



> [!IMPORTANT]  
> Review the [considerations section of the Read Replica overview](concepts-read-replicas.md#considerations).
>  
> To avoid issues during promotion of replicas constantly change the following server parameters on the replicas first, before applying them on the primary: `max_connections`, `max_prepared_transactions`, `max_locks_per_transaction`, `max_wal_senders`, `max_worker_processes`.

## Create virtual endpoints

> [!NOTE]
> All operations involving virtual endpoints - like adding, editing, or removing - are executed in the context of the primary server. 


#### [Portal](#tab/portal)
1. In the Azure portal, select the primary server.

2. On the server sidebar, under **Settings**, select **Replication**.

3. Select **Create endpoint**.

4. In the dialog, type a meaningful name for your endpoint. Notice the DNS endpoint that is being generated.

    :::image type="content" source="./media/how-to-read-replicas-portal/add-virtual-endpoint.png" alt-text="Screenshot of creating a new virtual endpoint with custom name.":::

5. Select **Create**.

    > [!NOTE]  
    > If you do not create a virtual endpoint you will receive an error on the promote replica attempt.

    :::image type="content" source="./media/how-to-read-replicas-portal/replica-promote-attempt.png" alt-text="Screenshot of promotion error when missing virtual endpoint.":::

#### [CLI](#tab/cli)
You can create a virtual endpoint by using the [`az postgres flexible-server virtual-endpoint create`](/cli/azure/postgres/flexible-server/virtual-endpoint#az-postgres-flexible-server-virtual-endpoint-create) command. 

```azurecli-interactive
    az postgres flexible-server virtual-endpoint create \
      --resource-group <resource-group> \
      --server-name <primary-name> \
      --name <virtual-endpoint-name> \
      --endpoint-type ReadWrite \
      --members <replica-name>
```

Replace `<resource-group>`, `<primary-name>`, `<virtual-endpoint-name>`, and `<replica-name>` with your specific values.


#### [REST API](#tab/restapi)

To create a virtual endpoint using Azure's REST API, you would use an `HTTP PUT` request. The request would look like this:

```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{sourceserverName}/virtualendpoints/{virtualendpointName}?api-version=2023-06-01-preview
```

The accompanying JSON body for this request is as follows:

```json
{ 
  "Properties": { 
    "EndpointType": "ReadWrite", 
    "Members": ["{replicaserverName}"] 
  }
} 
```

Here, `{replicaserverName}` should be replaced with the name of the replica server you're including as a reader endpoint target in this virtual endpoint.

---


## List virtual endpoints

To list virtual endpoints, use the following steps:

#### [Portal](#tab/portal)

1. In the Azure portal, select the **primary** server.

2. On the server sidebar, under **Settings**, select **Replication**.

3. At the top of the page, you see both the reader and writer endpoints displayed, along with the names of the servers they're pointing to.

    :::image type="content" source="./media/how-to-read-replicas-portal/virtual-endpoints-show.png" alt-text="Screenshot of virtual endpoints list." lightbox="./media/how-to-read-replicas-portal/virtual-endpoints-show.png":::

#### [CLI](#tab/cli)

You can view the details of the virtual endpoint using either the [`list`](/cli/azure/postgres/flexible-server/virtual-endpoint#az-postgres-flexible-server-virtual-endpoint-list) or [`show`](/cli/azure/postgres/flexible-server/virtual-endpoint#az-postgres-flexible-server-virtual-endpoint-show) command. Given that only one virtual endpoint is allowed per primary-replica pair, both commands yield the same result.

Here's an example of how to use the `list` command:

```azurecli-interactive
az postgres flexible-server virtual-endpoint list \
      --resource-group <resource-group> \
      --server-name <server-name>
```

Replace `<server-name>` with the name of your primary server and `<resource-group>` with the name of your resource group.

Here's how you can use the `show` command:

```azurecli-interactive
az postgres flexible-server virtual-endpoint show \
      --name <virtual-endpoint-name>
      --resource-group <resource-group> \
      --server-name <server-name>
```
In this command, replace `<virtual-endpoint-name>`,`<server-name>`, and `<resource-group>` with the respective names. `<server-name>` is the name of your primary server.

#### [REST API](#tab/restapi)

```http request
GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{sourceserverName}/virtualendpoints?api-version=2023-06-01-preview
```

Here, `{sourceserverName}` should be the name of the primary server from which you're managing the virtual endpoints.

---


### Modify application to point to the virtual endpoint

Modify any applications that are using your Azure Database for PostgreSQL flexible server instance to use the new virtual endpoints (ex: `corp-pg-001.writer.postgres.database.azure.com` and `corp-pg-001.reader.postgres.database.azure.com`).

## Promote replicas

With all the necessary components in place, you're ready to perform a promote replica to primary operation.

#### [Portal](#tab/portal)
To promote replica from the Azure portal, follow these steps:

1.  In the [Azure portal](https://portal.azure.com/), select your primary Azure Database for PostgreSQL flexible server instance.

2.  On the server menu, under **Settings**, select **Replication**.

3.  Under **Servers**, select the **Promote** icon for the replica.

    :::image type="content" source="./media/how-to-read-replicas-portal/replica-promote.png" alt-text="Screenshot of selecting to promote for a replica.":::

4.  In the dialog, ensure the action is **Promote to primary server**.

5.  For **Data sync**, ensure **Planned - sync data before promoting** is selected.

    :::image type="content" source="./media/how-to-read-replicas-portal/replica-promote.png" alt-text="Screenshot of how to select promote for a replica.":::

6.  Select **Promote** to begin the process. Once it completes, the roles reverse: the replica becomes the primary, and the primary assumes the role of the replica.

#### [CLI](#tab/cli)

When promoting a replica to a primary server in Azure PostgreSQL Flexible Server, use the `az postgres flexible-server replica promote` command. This process is essential for elevating a replica server to function as the primary server and demotion of current primary to replica role. Specify `--promote-mode switchover` and `--promote-option planned` in the command.

```azurecli-interactive
az postgres flexible-server replica promote \
  --resource-group <resource-group> \
  --name <replica-server-name> \
  --promote-mode switchover \
  --promote-option planned
```

Replace `<resource-group>` and `<replica-server-name>` with your specific resource group and replica server name. This command ensures a smooth transition of the replica to a primary role in a planned manner.

#### [REST API](#tab/restapi)

When promoting a replica to a primary server, use an `HTTP PATCH` request with a specific `JSON` body to set the promotion options. This process is crucial when you need to elevate a replica server to act as the primary server.

The `HTTP` request is structured as follows:

```http
PATCH https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{replicaserverName}?api-version=2023-06-01-preview
```

```json
{
  "Properties": {
    "Replica": {
      "PromoteMode": "switchover",
      "PromoteOption": "planned"
    }
  }
}
```

In this `JSON`, the promotion is set to occur in `switchover` mode with a `planned` promotion option. While there are two options for promotion - `planned` or `forced` - chose `planned` for this exercise.

---

   > [!NOTE]  
   > The replica you are promoting must have the reader virtual endpoint assigned, or you will receive an error on promotion.
   

### Test applications

To perform some operations, restart your applications and then attempt those operations. Your applications should function seamlessly without modifying the virtual endpoint connection string or DNS entries. Leave your applications running this time.

### Failback to the original server and region

Repeat the same operations to promote the original server to the primary.

#### [Portal](#tab/portal)

1.  In the [Azure portal](https://portal.azure.com/), select the replica.

2.  On the server sidebar, under **Settings**, select **Replication**

3.  Under **Servers**, select the **Promote** icon for the replica.

4.  In the dialog, ensure the action is **Promote to primary server**.

5.  For **Data sync**, ensure **Planned - sync data before promoting** is selected.

6.  Select **Promote**, the process begins. Once it completes, the roles reverse: the replica becomes the primary, and the primary assumes the role of the replica.

#### [CLI](#tab/cli)

This time, change the `<replica-server-name>` in the `az postgres flexible-server replica promote` command to refer to your old primary server, which is currently acting as a replica, and execute the request again.

```azurecli-interactive
az postgres flexible-server replica promote \
  --resource-group <resource-group> \
  --name <replica-server-name> \
  --promote-mode switchover \
  --promote-option planned
```

Replace `<resource-group>` and `<replica-server-name>` with your specific resource group and current replica server name.

#### [REST API](#tab/restapi)

This time, change the `{replicaserverName}` in the API request to refer to your old primary server, which is currently acting as a replica, and execute the request again.

```http
PATCH https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{replicaserverName}?api-version=2023-06-01-preview
```

```json
{
  "Properties": {
    "Replica": {
      "PromoteMode": "switchover",
      "PromoteOption": "planned"
    }
  }
}
```

In this `JSON`, the promotion is set to occur in `switchover` mode with a `planned` promotion option. While there are two options for promotion - `planned` or `forced` - chose `planned` for this exercise.

---

### Test applications

Again, switch to one of the consuming applications. Wait for the primary and replica status to change to `Updating` and then attempt to perform some operations. During the replica promote, your application might encounter temporary connectivity issues to the endpoint:

:::image type="content" source="./media/how-to-read-replicas-portal/failover-connectivity-psql.png" alt-text="Screenshot of potential promote connectivity errors." lightbox="./media/how-to-read-replicas-portal/failover-connectivity-psql.png":::


## Add secondary read replica

Create a secondary read replica in a separate region to modify the reader virtual endpoint and to allow for creating an independent server from the first replica.

#### [Portal](#tab/portal)

1.  In the [Azure portal](https://portal.azure.com/), choose the primary Azure Database for PostgreSQL flexible server instance.

2.  On the server sidebar, under **Settings**, select **Replication**.

3.  Select **Create replica**.

4.  Enter the Basics form with information in a third region (ex `westus` and `corp-pg-westus-001`)

5.  Select **Review + create** to confirm the creation of the replica or **Next: Networking** if you want to add, delete, or modify any firewall rules.

6.  Verify the firewall settings. Notice how the primary settings are copied automatically.

7.  Leave the remaining defaults and then select the **Review + create** button at the bottom of the page or proceed to the following forms to configure security or add tags.

8.  Review the information in the final confirmation window. When you're ready, select **Create**. A new deployment is created.

9.  During the deployment, you see the primary in `Updating` state.
    
    :::image type="content" source="./media/how-to-read-replicas-portal/primary-updating.png" alt-text="Screenshot of primary entering into updating status." lightbox="./media/how-to-read-replicas-portal/primary-updating.png":::

#### [CLI](#tab/cli)

You can create a secondary read replica by using the [`az postgres flexible-server replica create`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-replica-create) command. 

```azurecli-interactive
az postgres flexible-server replica create \
  --replica-name <replica-name> \
  --resource-group <resource-group> \
  --source-server <source-server-name> \
  --location <location>
```

Choose a distinct name for `<replica-name>` to differentiate it from the primary server and any other replicas.
Replace `<resource-group>`, `<source-server-name>`, and `<location>` with your specific values.

#### [REST API](#tab/restapi)

You can create a secondary read replica by using the [servers create API](/rest/api/postgresql/flexibleserver/servers/create):

```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{replicaserverName}?api-version=2022-12-01
```

Choose a distinct name for `{replicaserverName}` to differentiate it from the primary server and any other replicas.

```json
{
  "location": "westus3",
  "properties": {
    "createMode": "Replica",
    "SourceServerResourceId": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{sourceserverName}"
  }
}
```

The location is set to `westus3`, but you can adjust the setting based on your geographical and operational needs.

---

## Modify virtual endpoint

#### [Portal](#tab/portal)

1.  In the [Azure portal](https://portal.azure.com/), choose the primary Azure Database for PostgreSQL flexible server instance.

2.  On the server sidebar, under **Settings**, select **Replication**.

3.  Select the ellipses and then select **Edit**.
   
    :::image type="content" source="./media/how-to-read-replicas-portal/edit-virtual-endpoint.png" alt-text="Screenshot of editing the virtual endpoint." lightbox="./media/how-to-read-replicas-portal/edit-virtual-endpoint.png":::

4.  In the dialog, select the new secondary replica.

    :::image type="content" source="./media/how-to-read-replicas-portal/select-secondary-endpoint.png" alt-text="Screenshot of selecting the secondary replica.":::

5.  Select **Save**. The reader endpoint is now pointed at the secondary replica, and the promote operation is now tied to this replica.

#### [CLI](#tab/cli)

You can now modify your reader endpoint to point to the newly created secondary replica by using a `az postgres flexible-server virtual-endpoint update` command. Remember to replace `<replica-name>` with the name of the newly created read replica.

```azurecli-interactive
az postgres flexible-server virtual-endpoint update \
  --resource-group <resource-group> \
  --server-name <server-name> \
  --name <virtual-endpoint-name> \
  --endpoint-type ReadWrite \
  --members <replica-name>
```

Replace `<resource-group>`, `<server-name>`, `<virtual-endpoint-name>`, and `<replica-name>` with your specific values.

#### [REST API](#tab/restapi)

You can now modify your reader endpoint to point to the newly created secondary replica by using a `PATCH` request. Remember to replace `{replicaserverName}` with the name of the newly created read replica.

```http
PATCH https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{sourceserverName}/virtualendpoints/{virtualendpointName}?api-version=2023-06-01-preview
```

```json
{ 
  "Properties": { 
    "EndpointType": "ReadWrite", 
    "Members": ["{replicaserverName}"] 
  }
} 
```

---

## Promote replica to independent server

Rather than switchover to a replica, it's also possible to break the replication of a replica such that it becomes its standalone server.

#### [Portal](#tab/portal)

1.  In the [Azure portal](https://portal.azure.com/), choose the Azure Database for PostgreSQL flexible server primary server.

2.  On the server sidebar, on the server menu, under **Settings**, select **Replication**.

3.  Under **Servers**, select the **Promote** icon for the replica you want to promote to an independent server.

    :::image type="content" source="./media/how-to-read-replicas-portal/replica-promote-servers.png" alt-text="Screenshot of how to select to promote for a replica 2." lightbox="./media/how-to-read-replicas-portal/replica-promote-servers.png":::
    
4.  In the dialog, ensure the action is **Promote to independent server and remove from replication. This won't impact the primary server**.

5.  For **Data sync**, ensure **Planned - sync data before promoting** is selected.

    :::image type="content" source="./media/how-to-read-replicas-portal/replica-promote-independent.png" alt-text="Screenshot of promoting the replica to independent server.":::

6.  Select **Promote**, the process begins. Once completed, the server is no longer a replica of the primary.


#### [CLI](#tab/cli)

When you promote a replica in Azure PostgreSQL Flexible Server, the default behavior is to promote it to an independent server. The promotion is achieved using the [`az postgres flexible-server replica promote`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-replica-promote) command without specifying the `--promote-mode` option, as `standalone` mode is assumed by default.

```azurecli-interactive
az postgres flexible-server replica promote \
  --resource-group <resource-group> \
  --name <replica-server-name>
```

In this command, replace `<resource-group>` and `<replica-server-name>` with your specific resource group name and the name of the first replica server that you created, that isn't part of virtual endpoint anymore.



#### [REST API](#tab/restapi)

You can promote a replica to a standalone server using a `PATCH` request. Send a `PATCH` request to the specified Azure Management REST API URL with the first `JSON` body, where `PromoteMode` is set to `standalone` and `PromoteOption` to `planned`. The second `JSON` body format, setting `ReplicationRole` to `None`, is deprecated but still mentioned here for backward compatibility.

```http
PATCH https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{replicaserverName}?api-version=2023-06-01-preview
```


```json
{
  "Properties": {
    "Replica": {
      "PromoteMode": "standalone",
      "PromoteOption": "planned"
    }
  }
}
```

```json
{
  "Properties": {
    "ReplicationRole": "None"
  }
}
```

---

   > [!NOTE]  
   > Once a replica is promoted to an independent server, it cannot be added back to the replication set.
   

## Delete virtual endpoint

#### [Portal](#tab/portal)

1. In the Azure portal, select the **primary** server.

2. On the server sidebar, under **Settings**, select **Replication**.

3. At the top of the page, locate the `Virtual endpoints` section. Navigate to the three dots (menu options) next to the endpoint name, expand it, and choose `Delete`.

4. A delete confirmation dialog appears. It warns you: "This action deletes the virtual endpoint `virtualendpointName`. Any clients connected using these domains may lose access." Acknowledge the implications and confirm by clicking on **Delete**.


#### [CLI](#tab/cli)

To remove a virtual endpoint from an Azure PostgreSQL Flexible Server, you can use the [`az postgres flexible-server virtual-endpoint delete`](/cli/azure/postgres/flexible-server/virtual-endpoint#az-postgres-flexible-server-virtual-endpoint-delete) command. This action permanently deletes the specified virtual endpoint.

```azurecli-interactive
az postgres flexible-server virtual-endpoint delete \
  --resource-group <resource-group> \
  --server-name <server-name> \
  --name <virtual-endpoint-name>
```

In this command, replace `<resource-group>`, `<server-name>`, and `<virtual-endpoint-name>` with your specific resource group, server name, and the name of the virtual endpoint you wish to delete.


#### [REST API](#tab/restapi)

To delete a virtual endpoint using Azure's REST API, you would issue an `HTTP DELETE` request. The request URL would be structured as follows:

```http
DELETE https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{serverName}/virtualendpoints/{virtualendpointName}?api-version=2023-06-01-preview
```

---

## Delete a replica

#### [Portal](#tab/portal)

You can delete a read replica similar to how you delete a standalone Azure Database for PostgreSQL flexible server instance.

1.  In the Azure portal, open the **Overview** page for the read replica. Select **Delete**.

    :::image type="content" source="./media/how-to-read-replicas-portal/delete-replica.png" alt-text="Screenshot of the replica Overview page, select to delete the replica.":::

You can also delete the read replica from the **Replication** window by following these steps:

2.  In the Azure portal, select your primary Azure Database for PostgreSQL flexible server instance.

3.  On the server menu, under **Settings**, select **Replication**.

4.  Select the read replica to delete and then select the ellipses. Select **Delete**.

    :::image type="content" source="./media/how-to-read-replicas-portal/delete-replica02.png" alt-text="Screenshot of select the replica to delete." lightbox="./media/how-to-read-replicas-portal/delete-replica02.png":::

5.  Acknowledge **Delete** operation.

#### [CLI](#tab/cli)
To delete a primary or replica server, use the [`az postgres flexible-server delete`](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-delete) command. If server has read replicas, then you should delete the read replicas first before deleting the primary server.

```azurecli-interactive
az postgres flexible-server delete \
  --resource-group <resource-group> \
  --name <server-name>
```

Replace `<resource-group>` and `<server-name>` with the name of your resource group name and the replica server name you wish to delete.

#### [REST API](#tab/restapi)
To delete a primary or replica server, use the [servers delete API](/rest/api/postgresql/flexibleserver/servers/delete). If server has read replicas, then read replicas should be deleted first before deleting the primary server.

```http
DELETE https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{replicaserverName}?api-version=2022-12-01
```

---

## Delete a primary server

You can only delete the primary server once you delete all read replicas. To delete replicas, follow the instructions in the [Delete a replica](#delete-a-replica) section and then proceed with the steps provided.

#### [Portal](#tab/portal)

To delete a server from the Azure portal, follow these steps:

1.  In the Azure portal, select your primary Azure Database for PostgreSQL flexible server instance.

2.  Open the **Overview** page for the server and select **Delete**.

    :::image type="content" source="./media/how-to-read-replicas-portal/delete-primary.png" alt-text="Screenshot of the server Overview page, select to delete the primary server." lightbox="./media/how-to-read-replicas-portal/delete-primary.png":::

3.  Enter the name of the primary server to delete. Select **Delete** to confirm the deletion of the primary server.

    :::image type="content" source="./media/how-to-read-replicas-portal/delete-primary-confirm.png" alt-text="Screenshot of confirming to delete the primary server.":::

#### [CLI](#tab/cli)
To delete a primary or replica server, use the [`az postgres flexible-server delete`](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-delete) command. If server has read replicas, then read replicas should be deleted first before deleting the primary server.

```azurecli-interactive
az postgres flexible-server delete \
  --resource-group <resource-group> \
  --name <server-name>
```

Replace `<resource-group>` and `<server-name>` with the name of your resource group name and the primary server name you wish to delete.

#### [REST API](#tab/restapi)
To delete a primary or replica server, use the [servers delete API](/rest/api/postgresql/flexibleserver/servers/delete). If server has read replicas, then read replicas should be deleted first before deleting the primary server.

```http
DELETE https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DBForPostgreSql/flexibleServers/{sourceserverName}?api-version=2022-12-01
```

---


## Monitor a replica

Two metrics are available to monitor read replicas.

### Max Physical Replication Lag

> Available only on the primary.

The **Max Physical Replication Lag** metric shows the byte lag between the primary server and the most lagging replica.

1.  In the Azure portal, select the primary server.

2.  Select **Metrics**. In the **Metrics** window, select **Max Physical Replication Lag**.

    :::image type="content" source="./media/how-to-read-replicas-portal/metrics_max_physical_replication_lag.png" alt-text="Screenshot of the Metrics page showing Max Physical Replication Lag metric." lightbox="./media/how-to-read-replicas-portal/metrics_max_physical_replication_lag.png":::

3.  For your **Aggregation**, select **Max**.

### Read Replica Lag metric

The **Read Replica Lag** metric shows the time since the last replayed transaction on a replica. If no transactions occur on your primary, the metric reflects this time lag. For instance, if no transactions occur on your primary server, and the last transaction was replayed 5 seconds ago, then the Read Replica Lag shows a 5-second delay.

1.  In the Azure portal, select read replica.

2.  Select **Metrics**. In the **Metrics** window, select **Read Replica Lag**.

    :::image type="content" source="./media/how-to-read-replicas-portal/metrics_read_replica_lag.png" alt-text="Screenshot of the Metrics page showing Read Replica Lag metric." lightbox="./media/how-to-read-replicas-portal/metrics_read_replica_lag.png":::

3.  For your **Aggregation**, select **Max**.

## Related content

- [Read replicas in Azure Database for PostgreSQL flexible server](concepts-read-replicas.md).
- [Geo-replication in Azure Database for PostgreSQL flexible server](concepts-read-replicas-geo.md).
- [Promote read replicas in Azure Database for PostgreSQL flexible server](concepts-read-replicas-promote.md).
- [Virtual endpoints for read replicas in Azure Database for PostgreSQL flexible server](concepts-read-replicas-virtual-endpoints.md).
- [Create and manage read replicas in Azure Database for PostgreSQL flexible server](how-to-read-replicas-portal.md).
- [Replication across Azure regions and virtual networks with private networking](concepts-networking-private.md#replication-across-azure-regions-and-virtual-networks-with-private-networking).
- [Terraform Azure provider documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs).
