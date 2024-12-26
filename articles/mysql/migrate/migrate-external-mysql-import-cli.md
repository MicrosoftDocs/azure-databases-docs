---
title: "Migrate MySQL On-Premises or Virtual Machine (VM) Workload to Azure Database for MySQL - Flexible Server Using Azure Database for MySQL Import CLI"
description: This tutorial describes how to use the Azure Database for MySQL Import CLI to migrate MySQL on-premises or VM workload to Azure Database for MySQL - Flexible Server.
author: adig
ms.author: adig
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom:
  - mvc
  - devx-track-azurecli
  - mode-api
ms.devlang: azurecli
---

# Migrate MySQL on-premises or Virtual Machine (VM) workload to Azure Database for MySQL with Azure Database for MySQL Import CLI

Azure Database for MySQL Import for external migrations enables you to migrate your MySQL on-premises or Virtual Machine (VM) workload seamlessly to Azure Database for MySQL - Flexible Server. It uses a user-provided physical backup file and restores the source server's physical data files to the target server, offering a simple and fast migration path. Post-import operation, you can take advantage of the benefits of a flexible server, which include better price and performance, granular control over database configuration, and custom maintenance windows.

Based on user-inputs, it takes up the responsibility of provisioning your target flexible server and then restoring the user-provided physical backup of the source server stored in the Azure Blob storage account to the target Flexible Server instance.

This tutorial shows how to use the Azure Database for MySQL Import CLI command to migrate your Migrate MySQL on-premises or Virtual Machine (VM) workload to Azure Database for MySQL - Flexible Server.

## Launch Azure Cloud Shell

The [Azure Cloud Shell](/azure/cloud-shell/overview) is a free interactive shell that you can use to run the steps in this article. It has common Azure tools preinstalled and configured to use with your account.

To open the Cloud Shell, select **Try it** from the upper right corner of a code block. You can also open Cloud Shell in a separate browser tab by going to [https://shell.azure.com/bash](https://portal.azure.com/#cloudshell). Select **Copy** to copy the blocks of code, paste it into the Cloud Shell, and select **Enter** to run it.

If you prefer to install and use the CLI locally, this tutorial requires Azure CLI version 2.54.0 or later. To find the version, run `az --version`. If you need to install or upgrade, see [Install Azure CLI](/cli/azure/install-azure-cli).

## Setup

You must sign in to your account using the [az sign-in](/cli/azure/reference-index#az-login) command. Note the **id** property, which refers to your Azure account's **Subscription ID**.

```azurecli-interactive
az login
```

Select the specific subscription under your account where you want to deploy the target Flexible Server using the [az account set](/cli/azure/account#az-account-set) command. Note the **id** value from the **az login** output to use as the value for the **subscription** argument in the command. To get all your subscriptions, use [az account list](/cli/azure/account#az-account-list).

```azurecli-interactive
az account set --subscription <subscription id>
```

## Prerequisites

- Source server should have the following parameters:
  - Lower_case_table_names = 1
  - Innodb_file_per_table = ON
  - System tablespace name should be ibdata1.
  - System tablespace size should be greater than or equal to 12 MB. (MySQL Default)
  - Innodb_page_size = 16348 (MySQL Default)
  - Only INNODB engine is supported.
- Take a physical backup of your MySQL workload using Percona XtraBackup.
The following are the steps for using Percona XtraBackup to take a full backup:
  - Install Percona XtraBackup on the on-premises or VM workload. For MySQL engine version v5.7, install Percona XtraBackup version 2.4, see [Installing Percona XtraBackup 2.4]( https://docs.percona.com/percona-xtrabackup/2.4/installation.html). For MySQL engine version v8.0, install Percona XtraBackup version 8.0, see [Installing Percona XtraBackup 8.0]( https://docs.percona.com/percona-xtrabackup/8.0/installation.html).
  - For instructions for taking a Full backup with Percona XtraBackup 2.4, see [Full backup]( https://docs.percona.com/percona-xtrabackup/2.4/backup_scenarios/full_backup.html). For instructions for taking a Full backup with Percona XtraBackup 8.0, see [Full backup] (<https://docs.percona.com/percona-xtrabackup/8.0/create-full-backup.html>). While taking full backup, run the below commands in order:
    - ** xtrabackup --backup --host={host} --user={user} --password={password} --target-dir={backup__dir_path}**
    - ** xtrabackup --prepare --{backup_dir_path}** (Provide the same backup path here as in the previous command)
  - **Considerations while taking the Percona XtraBackup:**
    - Make sure you run both the backup and prepare step.
    - Make sure there are no errors in the backup and prepare step.
    - Keep the backup and prepare step logs for Azure Support, which is required in case of failures.

    > [!IMPORTANT]
    > Attempting to access corrupted tables imported from a source server can cause a flexible server to crash. As a result, before taking a backup using the Percona XtraBackup utility, it is strongly recommended to perform a "mysqlcheck / Optimize Table" operation on the source server.

- [Create an Azure Blob container](/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container) and get the Shared Access Signature (SAS) Token ([Azure portal](/azure/ai-services/translator/document-translation/how-to-guides/create-sas-tokens?tabs=Containers#create-sas-tokens-in-the-azure-portal) or [Azure CLI](/azure/storage/blobs/storage-blob-user-delegation-sas-create-cli)) for the container. Ensure that you grant Add, Create, and Write in the **Permissions** dropdown list. Copy and paste the Blob SAS token and URL values in a secure location. They're only displayed once and can't be retrieved once the window is closed.
- Upload the full backup file at {backup_dir_path} to your Azure Blob storage. Follow [these steps to upload a file](/azure/storage/common/storage-use-azcopy-blobs-upload#upload-a-file).
- To perform an online migration, capture and store the bin-log position of the backup file taken using Percona XtraBackup by running the **cat xtrabackup_info** command and copying the bin_log pos output.
- The Azure storage account should be publicly accessible using SAS token. Azure storage account with virtual network configuration are not supported.

## Limitations

- Source server configuration isn't migrated. You must configure the target Flexible server appropriately.
- Migration for encrypted backups isn't supported.
- Users and privileges aren't migrated as part of Azure Database for MySQL Import. You must take a manual dump of users and privileges before initiating Azure Database for MySQL Import to migrate logins post import operation by restoring them on the target Flexible Server.
  - user1@localhost can't be migrated as we don't support localhost user creation in Flexible Server.
- High Availability (HA) enabled Flexible Servers are returned as HA-disabled servers to increase the speed of migration operation post the import migration. Enable HA for your target Flexible Server post migration.

## Recommendations for an optimal migration experience

- Consider keeping the Azure Blob storage account and the target Flexible Server to be deployed in the same region for better import performance.
- Recommended SKU configuration for target Azure Database for MySQL Flexible Server –
  - Setting a Burstable SKU for the target isn't recommended to optimize migration time when running the Azure Database for MySQL Import operation. We recommend scaling to General Purpose/ Business Critical for the course of the import operation, post, which you can scale down to Burstable SKU.

## Trigger an Azure Database for MySQL Import operation to migrate from Azure Database for MySQL -Flexible Server

Trigger an Azure Database for MySQL Import operation with the `az mysql flexible-server import create` command. The following command creates a target Flexible Server and performs instance-level import from the backup file to target destination using your Azure CLI's local context:

```azurecli
az mysql flexible-server import create --data-source-type
                                --data-source
                                --data-source-sas-token
                                --resource-group
                                --name
                                --sku-name
                                --tier
                                --version
                                --location
                                [--data-source-backup-dir]
                                [--storage-size]
                                [--mode]
                                [--admin-password]
                                [--admin-user]
                                [--auto-scale-iops {Disabled, Enabled}]
                                [--backup-identity]
                                [--backup-key]
                                [--backup-retention]
                                [--database-name]
                                [--geo-redundant-backup {Disabled, Enabled}]
                                [--high-availability {Disabled, SameZone, ZoneRedundant}]
                                [--identity]
                                [--iops]
                                [--key]
                                [--private-dns-zone]
                                [--public-access]
                                [--resource-group]
                                [--standby-zone]
                                [--storage-auto-grow {Disabled, Enabled}]
                                [--subnet]
                                [--subnet-prefixes]
                                [--tags]
                                [--vnet]
                                [--zone]

The following example takes in the data source information for your source MySQL server's backup file and target Flexible Server information, creates a target Flexible Server named `test-flexible-server` in the `westus` location and performs an import from backup file to target.

azurecli-interactive
az mysql flexible-server import create --data-source-type "azure_blob" --data-source "https://onprembackup.blob.core.windows.net/onprembackup" --data-source-backup-dir "mysql_backup_percona" –-data-source-token "{sas-token}" --resource-group "test-rg"  --name "test-flexible-server" –-sku-name Standard_D2ds_v4  --tier GeneralPurpose –-version 5.7 -–location "westus"
```

Here are the details for the arguments above:

**Setting** | **Sample value** | **Description**
---|---|---
data-source-type | azure_blob | The type of data source that serves as the source destination for triggering Azure Database for MySQL Import. Accepted values: [azure_blob]. Description of accepted values- azure_blob: Azure Blob storage.
data-source | {resourceID} | The resource ID of the Azure Blob container.
data-source-backup-dir | mysql_percona_backup | The directory of the Azure Blob storage container in which the backup file was uploaded. This value is required only when the backup file isn't stored in the root folder of Azure Blob container.
data-source-sas-token | {sas-token} | The Shared Access Signature (SAS) token generated for granting access to import from the Azure Blob storage container.
resource-group | test-rg | The name of the Azure resource group of the target Azure Database for MySQL Flexible Server.
mode | Offline | The mode of Azure Database for MySQL import. Accepted values: [Offline]; Default value: Offline.
location | westus | The Azure location for the source Azure Database for MySQL Flexible Server.
name | test-flexible-server | Enter a unique name for your target Azure Database for MySQL Flexible Server. The server name can contain only lowercase letters, numbers, and the hyphen (-) character. It must contain from 3 to 63 characters. Note: This server is deployed in the same subscription, resource group, and region as the source.
admin-user | adminuser | The username for the administrator sign-in for your target Azure Database for MySQL Flexible Server. It can't be **azure_superuser**, **admin**, **administrator**, **root**, **guest**, or **public**.
admin-password | *password- | The administrator user's password for your target Azure Database for MySQL Flexible Server. It must contain between 8 and 128 characters. Your password must contain characters from three categories: English uppercase letters, English lowercase letters, numbers, and nonalphanumeric characters.
sku-name|GP_Gen5_2|Enter the name of the pricing tier and compute configuration for your target Azure Database for MySQL Flexible Server. Follows the convention {pricing tier}*{compute generation}*{vCores} in shorthand. For more information, see the [pricing tiers](../flexible-server/concepts-service-tiers-storage.md#service-tiers-size-and-server-types).
tier | Burstable | Compute tier of the target Azure Database for MySQL Flexible Server. Accepted values: Burstable, GeneralPurpose, MemoryOptimized; Default value: Burstable.
public-access | 0.0.0.0 | Determines the public access for the target Azure Database for MySQL Flexible Server. Enter single or range of IP addresses to be included in the allowed list of IPs. IP address ranges must be dash-separated and not contain any spaces. Specifying 0.0.0.0 allows public access from any resources deployed within Azure to access your server. Setting it to "None" sets the server in public access mode but doesn't create a firewall rule.
Virtual network | myVnet | Name or ID of a new or existing virtual network. If you want to use a virtual network from different resource group or subscription, provide a resource ID. The name must be between 2 to 64 characters. The name must begin with a letter or number, end with a letter, number or underscore, and can contain only letters, numbers, underscores, periods, or hyphens.
subnet | mySubnet | Name or resource ID of a new or existing subnet. If you want to use a subnet from different resource group or subscription, provide resource ID instead of name. The subnet is delegated to flexibleServers. After delegation, this subnet can't be used for any other type of Azure resources.
private-dns-zone | myserver.private.contoso.com | The name or ID of new or existing private dns zone. You can use the private dns zone from same resource group, different resource group, or different subscription. If you want to use a zone from different resource group or subscription, provide resource ID. CLI creates a new private dns zone within the same resource group as virtual network if not provided by users.
key | key identifier of testKey | The resource ID of the primary keyvault key for data encryption.
identity | testIdentity | The name or resource ID of the user assigned identity for data encryption.
storage-size | 32 | The storage capacity of the target Azure Database for MySQL Flexible Server. The minimum is 20 GiB, and max is 16 TiB.
tags | key=value | Provide the name of the Azure resource group.
version | 5.7 | Server major version of the target Azure Database for MySQL Flexible Server.
high-availability | ZoneRedundant | Enable (ZoneRedundant or SameZone) or disable the high availability feature for the target Azure Database for MySQL Flexible Server. Accepted values: Disabled, SameZone, ZoneRedundant; Default value: Disabled.
zone | 1 | Availability zone into which to provision the resource.
standby-zone | 3 | The availability zone information of the standby server when high Availability is enabled.
storage-auto-grow | Enabled | Enable or disable auto grow of storage for the target Azure Database for MySQL Flexible Server. The default value is Enabled. Accepted values: Disabled, Enabled; Default value: Enabled.
iops | 500 | Number of IOPS to be allocated for the target Azure Database for MySQL Flexible Server. You get a certain amount of free IOPS based on compute and storage provisioned. The default value for IOPS is free IOPS. To learn more about IOPS based on compute and storage, refer to IOPS in Azure Database for MySQL Flexible Server.

## Migrate to Flexible Server with minimal downtime

To perform an online migration after completing the initial seeding from backup file using Azure Database for MySQL import, you can configure data-in replication between the source and target by following steps [here](../flexible-server/how-to-data-in-replication.md?tabs=bash%2Ccommand-line). You can use the bin-log position captured while taking the backup file using Percona XtraBackup to set up Bin-log position based replication.

## How long does Azure Database for MySQL Import take to migrate my MySQL instance?

Benchmarked performance based on storage size.

  | Backup file Storage Size | Import time |
  | --- | :---: |
  | 1 GiB | 0 min 23 secs |
  | 10 GiB | 4 min 24 secs |
  | 100 GiB | 10 min 29 secs |
  | 500 GiB | 13 min 15 secs |
  | 1 TB | 22 min 56 secs |
  | 10 TB | 2 hrs 5 min 30 secs |

As the storage size increases, the time required for data copying also increases, almost in a linear relationship. However, it's important to note that network fluctuations can significantly affect copy speed. Therefore, the data provided here should be taken as a reference only.

## Next step

> [!div class="nextstepaction"]
> [Manage Azure Database for MySQL - Flexible Server using the Azure portal](../flexible-server/how-to-manage-server-portal.md)
