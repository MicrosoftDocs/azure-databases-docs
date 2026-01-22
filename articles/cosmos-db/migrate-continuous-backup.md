---
title: Migrate From Periodic to Continuous Backup Mode
description: Migrate your Azure Cosmos DB account from periodic to continuous backup mode. Learn about the benefits, limitations, and steps for migration. Start your migration today.
author: kanshiG
ms.author: govindk
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 08/20/2025
ms.custom:
  - devx-track-azurecli
  - sfi-image-nochange
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Gremlin
  - ✅ Table
---

# Migrate an Azure Cosmos DB account from periodic to continuous backup mode

Azure Cosmos DB accounts with periodic mode backup policy can be migrated to continuous mode using the Azure portal, Azure CLI, Azure PowerShell, or Bicep templates. Migration from periodic to continuous mode is one-way and isn't reversible. After you migrate from periodic to continuous mode, you get the benefits of continuous mode.

Key reasons to migrate to continuous mode:

* Restore data yourself using Azure portal, CLI, or PowerShell.
* Restore to a specific second within the last 30-day or 7-day window.
* Make sure backups are consistent across shards or partition key ranges.
* Restore a container, database, or the full account after deletion or changes.
* Select events on the container, database, or account and choose when to start the restore.

> [!NOTE]
> Migration is one-way and can't be reversed. Once you migrate from periodic mode to continuous mode, you can't switch back.
>
> You can migrate an account to continuous backup mode only if these conditions are true. Also, check the [point in time restore limitations](continuous-backup-restore-introduction.md#current-limitations) before you migrate:
>
> * The account is API for NoSQL, Table, Gremlin, or MongoDB.
> * The account never had Azure Synapse Link disabled for a container.
>
> If the account uses [customer-managed keys](./how-to-setup-cmk.md), declare a managed identity (system-assigned or user-assigned) in the Key Vault access policy and set it as the default identity on the account.

> [!IMPORTANT]
> After you migrate your account to continuous backup mode, the cost can change compared to periodic backup mode. The choice between 30 days and seven days also affects backup cost. For details, see [continuous backup mode pricing](continuous-backup-restore-introduction.md#continuous-backup-pricing).

## Prerequisites

- An Azure Cosmos DB account
- The `Microsoft.DocumentDB/databaseAccounts/write` role-based access control permission for the account that is being migrated
- Latest version of Azure CLI or Azure PowerShell

## Migrate using portal

Use the following steps to migrate your account from periodic backup to continuous backup mode:

### [Azure CLI](#tab/azure-cli)

1. Sign in to the Azure CLI.

    ```azurecli-interactive
    az login
    ```

1.  Migrate the account to ``continuous30days`` or ``continuous7days`` tier.

    ```azurecli-interactive
    az cosmosdb update \
        --resource-group "<resource-group-name>" \
        --name "<account-name>" \
        --backup-policy-type "Continuous"
    ```
    
    ```azurecli-interactive
    az cosmosdb update \
        --resource-group "<resource-group-name>" \
        --name "<account-name>" \
        --backup-policy-type "Continuous" \
        --continuous-tier "Continuous7Days"
    ```

    > [!NOTE]
    > If you don't provide a tier value, the default is ``continuous30days``.

1.  After the migration completes successfully, the output shows the ``backupPolicy`` object, which includes ``type`` property with a value of ``Continuous``.

    ```json
    {
      ...
      "backupPolicy": {
        "continuousModeProperties": {
          "tier": "Continuous7Days"
        },
        "migrationState": null,
        "type": "Continuous"
      },
      ...
    }
    ```

### [Azure portal](#tab/azure-portal)

1.  Sign in to the [Azure portal](https://portal.azure.com).

1.  Navigate to your Azure Cosmos DB account and open the **Backup & Restore** pane. Select **Backup Policies** tab and select on **change**. Once you choose the target continuous mode, select on **Save**.

   :::image type="content" source="./media/migrate-continuous-backup/migrate-from-periodic-continuous.png" alt-text="Migrate to continuous mode using Azure portal" lightbox="./media/migrate-continuous-backup/migrate-from-periodic-continuous.png":::

1.  When the migration is in progress, the popup shows **Updating Backup policy settings**. If you select that notification, you might see **Updating** on the account level and **Migrating** for Backup policy on overview of the account. When migration completes, the backup policy switches to the chosen tier of **Continuous** mode. Migration time depends on the size of data in your account.

   :::image type="content" source="./media/migrate-continuous-backup/migrate-result-periodic-continuous.png" alt-text="Check the status of migration from Azure portal" lightbox="./media/migrate-continuous-backup/migrate-result-periodic-continuous.png":::

### [Azure PowerShell](#tab/azure-powershell)

1. Sign in to Azure PowerShell.

    ```azurepowershell-interactive
    Connect-AzAccount
    ```

1. Migrate your account from periodic to continuous backup mode with ``continuous30days`` tier or ``continuous7days`` days.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<resource-group-name>"
        Name = "<account-name>"
        BackupPolicyType = "Continuous"
    }
    Update-AzCosmosDBAccount @parameters
    ```
    
    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<resource-group-name>"
        Name = "<account-name>"
        BackupPolicyType = "Continuous"
        ContinuousTier = "Continuous7Days"
    }
    Update-AzCosmosDBAccount @parameters
    ```

    > [!NOTE]
    > If you don't provide a tier value, the default is ``continuous30days``.

---

### Check the migration status

Use the Azure CLI to check the status of an existing migration.

### [Azure CLI](#tab/azure-cli)

1. Run the following command to get the properties of the Azure Cosmos DB account.

    ```azurecli-interactive
    az cosmosdb show \
        --resource-group "<resource-group-name>" \
        --name "<account-name>" \
    ```

1. Check the `status` and `targetType` properties of the `backupPolicy` object. The status should be `InProgress` after the migration starts.

    ```json
    {
      ...
      "backupPolicy": {
        ...
        "migrationState": {
          "status": "InProgress",
          "targetType": "Continuous"
        },
        "type": "Periodic"
      },
      ...
    }
    ```

1. When the migration is complete, the backup type changes to `Continuous` and includes the chosen tier. If a tier wasn't provided, the tier would be set to `Continuous30Days`. Run the same `az cosmosdb show` command again to check the status.

    ```json
    {
      ...
      "backupPolicy": {
        "continuousModeProperties": {
          "tier": "Continuous7Days"
        },
        "migrationState": null,
        "type": "Continuous"
      },
      ...
    }
    ```

### [Azure portal](#tab/azure-portal)

Not available

### [Azure PowerShell](#tab/azure-powershell)

1. Run the following command to get the properties of the Azure Cosmos DB account.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<resource-group-name>"
        Name = "<account-name>"
    }
    Get-AzCosmosDBAccount @parameters
    ```

1. Check the `status` and `targetType` properties of the `backupPolicy` object. The status should be `InProgress` after the migration starts.

    ```json
    {
      ...
      "backupPolicy": {
        ...
        "migrationState": {
          "status": "InProgress",
          "targetType": "Continuous"
        },
        "type": "Periodic"
      },
      ...
    }
    ```

1. When the migration is complete, the backup type changes to `Continuous` and includes the chosen tier. If a tier wasn't provided, the tier would be set to `Continuous30Days`. Run the same `Get-AzCosmosDBAccount` command again to check the status.

    ```json
    {
      ...
      "backupPolicy": {
        "continuousModeProperties": {
          "tier": "Continuous7Days"
        },
        "migrationState": null,
        "type": "Continuous"
      },
      ...
    }
    ```

---

## Change Continuous Mode tiers

You can switch between ``Continuous30Days`` and ``Continous7Days`` in Azure PowerShell, Azure CLI, or the Azure portal.

### [Azure CLI](#tab/azure-cli)

The Following Azure CLI command illustrates switching an existing account to ``Continous7Days``:

```azurecli-interactive
az cosmosdb update \
    --resource-group "<resource-group-name>" \
    --name "<account-name>" \
    --backup-policy-type "Continuous" \
    --continuous-tier "Continuous7Days"
```

### [Azure portal](#tab/azure-portal)

In the portal for the given Azure Cosmos DB account, choose **Point in Time Restore** pane, select on change link next to Backup policy mode to show you the option of Continuous (30 days) or  Continuous (7 days). Choose the required target and select on **Save**.

:::image type="content" source="./media/migrate-continuous-backup/migrate-continuous-mode-tiers.png" lightbox="./media/migrate-continuous-backup/migrate-continuous-mode-tiers.png" alt-text="Screenshot of the dialog to select a tier of continuous backup mode.":::

### [Azure PowerShell](#tab/azure-powershell)

The following Azure PowerShell command illustrates switching an existing account to ``Continous7Days``:

```azurepowershell-interactive
$parameters = @{
    ResourceGroupName = "<resource-group-name>"
    Name = "<account-name>"
    BackupPolicyType = "Continuous"
    ContinuousTier = "Continuous7Days"
}
Update-AzCosmosDBAccount @parameters
```

---

You can also use an ARM template in a method similar to using the Azure CLI and Azure PowerShell.

> [!NOTE]
> When you switch from the 30-day to the 7-day tier, you immediately lose the ability to restore data older than seven days. When you switch from the 7-day to the 30-day tier, you can only restore data from the last seven days until new backups accumulate. You can check the earliest available restore time using Azure PowerShell or Azure CLI. Any price changes from switching tiers take effect immediately.

## Migrate to continuous backup using Bicep

To migrate to continuous backup mode using a Bicep template and Azure Resource Manager, find the backupPolicy section of your template and update the `type` property. 

1. Consider this example template that has a `Periodic` backup policy:

    ```bicep
    resource azureCosmosDBAccount 'Microsoft.DocumentDB/databaseAccounts@2025-04-15' = {
      name: '<account-name>'
      properties: {
        // Other required properties omitted for brevity
        backupPolicy: {
          type: 'Periodic'
          periodicModeProperties: {
            backupIntervalInMinutes: 240 // 4 hours
            backupRetentionIntervalInHours: 48 // 2 days
          }
        }
      }
    }
    ```

1. Update the example template to use `Continuous` backup mode at the **7-day** tier:

    ```bicep
    resource azureCosmosDBAccount 'Microsoft.DocumentDB/databaseAccounts@2025-04-15' = {
      name: '<account-name>'
      properties: {
        // Other required properties omitted for brevity
        backupPolicy: {
          type: 'Continuous'
          continuousModeProperties: {
            tier: 'Continuous7Days'
          }
        }
      }
    }
    ```

1. Deploy the template by using Azure PowerShell or CLI. The following example shows how to deploy the template with a CLI command:

    ```azurecli
    az deployment group create \
        --resource-group "<resource-group-name>" \
        --template-file "<template-file-path>"
    ```

## Related content

- [Frequently asked questions about continuous backup migration](faq.yml#migrating-to-continuous-backup-mode)
- [Introduction to continuous backup mode with point-in-time restore.](continuous-backup-restore-introduction.md)
- [Continuous backup mode resource model.](continuous-backup-restore-resource-model.md)
- [Restore an account from a backup](restore-account-continuous-backup.md)
