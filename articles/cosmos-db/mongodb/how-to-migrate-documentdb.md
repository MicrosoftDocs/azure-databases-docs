---
title: Migrate to Azure DocumentDB
titleSuffix: Azure Cosmos DB for MongoDB
description: Learn how to migrate from Azure Cosmos DB for MongoDB to Azure DocumentDB using built-in migration tools. Step-by-step guide with prerequisites and job monitoring.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.topic: how-to
ms.date: 10/17/2025
appliesto:
  - MongoDB
---

# Migrate from Azure Cosmos DB for MongoDB to Azure DocumentDB

In this guide, you take an existing collection and migrate it from Azure Cosmos DB for MongoDB to Azure DocumentDB using the tooling built-in to the service and Azure portal.

## Prerequisites

- An Azure subscription

    - If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

- A target Azure DocumentDB cluster

    - If you don't already have a cluster, [create a new Azure DocumentDB cluster](../../documentdb/quickstart-portal.md).
    
    - Ensure that you have the **native authentication credentials** required to connect to your cluster. 

- An Azure Key Vault account

    - Ensure that the Key Vault account is enabled for role-based access control. For more information, see [role-based access control in Azure Key Vault](/azure/key-vault/general/rbac-guide).

## Set up Azure Key Vault

First, you need to configure your source Azure Cosmos DB for MongoDB account to store the target Azure DocumentDB cluster's native authentication credentials in your existing key vault.

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Navigate to your source Azure Cosmos DB for MongoDB account.

1. In your source account, navigate to **Settings > Identity**.

1. Turn on the **system-assigned** managed identity for your source account by setting the **Status** option to **On**. Note down the value of the **Object (principal) ID** to use later in this guide.
    
    :::image source="media/how-to-migrate-documentdb/configure-identity.png" alt-text="Screenshot of the Azure portal Identity settings page showing system-assigned managed identity configuration options.":::

    > [!TIP]
    > If you're using a user-assigned managed identity instead, ensure that at least one user-assigned managed identity is assigned to the source account.

1. Navigate to your existing key vault.

1. If the Key Vault uses the **Role-Based Access Control (RBAC)** permission model, select the **Access Control (IAM)** option in the resource menu and assign the **Key Vault Secret User** role to the principal ID (object ID) of the managed identity used for your source account. Otherwise, use the **Access policies** option in the resource menu to create an access policy with **Get** and **List Secret** permissions, then assign it to the principal ID (object ID).

1. Run the command to update your source account to use the preferred identity mechanism as the default identity.
    
    ```azurecli      
    az cosmosdb update \
        --resource-group "<resource-group-name>" \
        --name "<source-account-name>" \
        --default-identity "SystemAssignedIdentity"
    ```

    > [!TIP]
    > If you're using a user-assigned managed identity instead, run this command:
    >
    > ```azurecli-interactive
    > az cosmosdb update \
    >     --resource-group "<resource-group-name>" \
    >     --name "<source-account-name>" \
    >     --default-identity "UserAssignedIdentity=<fully-qualified-resource-id-of-user-assigned-managed-identity>"
    > ```

1. Back in your key vault, navigate to **Objects > Secrets**.
 
1. Then, select **Generate/Import** to create a new secret. Use these values for your secret:

    | | Description |
    | --- | --- |
    | **Name** | Secret names are used to identify the secret and can only contain alphanumeric characters and dashes. This value is eventually used in the migration job's **Secret Name** field. |
    | **Secret value** | Paste the native authentication credentials for your Azure Cosmos DB for MongoDB target cluster here. |

1. In your newly created secret, gather the value of **Vault URI**. This value is eventually used in the migration job's **Vault URI** field.

## Create migration job

First, create a migration job with the configuration required to start migrating data to the target cluster.

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Navigate to your Azure Cosmos DB for MongoDB account again.

1. On the account page, select **Migrate to DocumentDB** from the resource menu.

    :::image source="media/how-to-migrate-documentdb/home.png" alt-text="Screenshot of home page in the migration to DocumentDB workflow.":::

1. Select **Start a new migration job**.

## Select migration mode

The **Select Migration Mode** section is used to provide the migration mode that's most appropriate for your migration needs.

1. Select the appropriate mode from these options:

    | | Description |
    | --- | --- |
    | **Offline** | Offline migration captures a snapshot of the collection at the beginning, offering a simpler and predictable approach. It works well when using a static copy of the collection is acceptable, and real-time updates aren't essential. Use this option for nonproduction migrations. |
    | **Online** | Online migration copies collection data, ensuring updates are also replicated during the process. This method is advantageous with minimal downtime, allowing continuous operations for business continuity. Use this option when ongoing operations are crucial, and reducing downtime is a priority. |

    :::image source="media/how-to-migrate-documentdb/mode-selection.png" alt-text="Screenshot of the mode selection options for a migration job.":::

    > [!NOTE]
    > Continuous Backup is a prerequisite for online migrations. For more information, see [continuous backup](../continuous-backup-restore-introduction.md).

1. Select **Next**.

## Configure target migration credentials

The **Select Target Account** section is used to provide the connection details to the target Azure DocumentDB cluster. As a security best practice, we recommend that you store your native authentication credentials in Azure Key Vault.

> [!NOTE]
> Connection strings that use Microsoft Entra ID authentication are currently not supported.

1. Set the **Vault URI** and **Secret Name** fields to the values you recorded earlier in this guide.

    :::image source="media/how-to-migrate-documentdb/target-key-vault.png" alt-text="Screenshot of target selection section.":::

1. Select **Next**.

## Update target firewall

The **Update Target Firewall** section is used to make sure that the target Azure DocumentDB cluster's firewall doesn't block the migration job requests.

1. Observe the **IP Address** in this step.

    :::image source="media/how-to-migrate-documentdb/target-firewall.png" alt-text="Screenshot of the target firewall check section and the source account's IP address.":::

1. Navigate to your target Azure DocumentDB cluster using another browser window or tab.

1. Select **Networking** in the **Settings** section of the resource menu.

1. Add a rule to allow access to the migration job's IP address. For more information, see [manage cluster-level firewall rules](../../documentdb/how-to-configure-firewall.md#grant-access-from-azure-services).

1. Navigate back to the browser window or tab with the migration job configuration steps.

1. Select **Next**.

> [!NOTE]
> If network security is enabled on your Azure Key Vault, ensure the same [IP is added to the Azure Key Vault Firewall](/azure/key-vault/general/network-security#key-vault-firewall-enabled-ipv4-addresses-and-ranges---static-ips) as well.


## Configure and start job

Use the **Select Collections** and **Confirm & Submit** sections to finalize your job's configuration.

1. Select the collections you plan to migrate in the **Select Collections** section.

    :::image source="media/how-to-migrate-documentdb/select-collections.png" alt-text="Screenshot of the section to select collections to migrate.":::

1. Select **Next**.

1. Review the job configuration and provide a unique job name.

    > [!IMPORTANT]
    > 1. The migration job doesn't transfer the indexes to the target collections. Before proceeding, use this sample [migration script](https://aka.ms/mongoruschemamigrationscript) to create the indexes on the target collections. Once the indexes are ready, select the checkbox.
    > 2. The migration job doesn't support changing the shard key. If you need a different shard key, migrate the data as an unsharded collection. Once the migration is complete, shard the collection on target using the desired shard key.

1. Select **Submit** to create and start the job.

## Monitor migration jobs

Once a job is submitted, you can monitor the status of the newly created job along with other pending or completed jobs.

1. Navigate to your source Azure Cosmos DB for MongoDB account.

1. On the account page, select **Migrate to DocumentDB** from the resource menu.

1. Select **Monitor existing migration job(s)**.

    :::image source="media/how-to-migrate-documentdb/monitor-jobs.png" alt-text="Screenshot of the page where existing migration jobs can be monitored or modified.":::

1. All migration jobs created for the current source account are listed.

1. Optionally, to change the status of a job, select the context menu (**..**) corresponding to the specific job. Options include:

    | Option | Description |
    | --- | --- |
    | **Pause** | Temporarily pause a currently running job |
    | **Resume** | Resume a paused job |
    | **Cancel** | Permanently cancel a currently running job |
    | **Cutover** | Finalize the migration when the source and target are synced |

    > [!NOTE]
    > The **cutover** option is only applicable to online migrations. Once cutover is completed, the sync between the source account and target cluster is terminated. After performing a cutover, you should update the credentials in your client application to target the new Azure DocumentDB cluster.
