---
title: "Quickstart: Create a Flexible Server Instance"
description: Quickstart guide to creating and managing an Azure Database for PostgreSQL flexible server instance.
author: gbowerman
ms.author: guybo
ms.reviewer: maghan
ms.date: 12/11/2024
ms.service: azure-database-postgresql
ms.topic: quickstart
ms.custom:
  - mvc
  - mode-ui
---

# Quickstart: Create an Azure Database for PostgreSQL

Azure Database for PostgreSQL is a managed service that allows you to run, manage, and scale highly available PostgreSQL databases in the cloud.

This article shows you how to create an Azure Database for PostgreSQL using different mechanisms.

## Create an Azure Database for PostgreSQL 

If you don't have an Azure subscription, create a [free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

An Azure Database for PostgreSQL flexible server instance is created with a configured set of [compute and storage resources](concepts-compute.md). The server is created within an [Azure resource group](/azure/azure-resource-manager/management/overview).

Select any of the following tabs, depending on the method you want to use to deploy your instance:

## [Portal](#tab/portal-create-flexible)

Using the [Azure portal](https://portal.azure.com/):

1. Sign in with your credentials, if you're asked to do so.

2. Select **Create a resource** in the upper-left corner of the portal.

    :::image type="content" source="./media/quickstart-create-server/create-a-resource.png" alt-text="Screenshot that shows how to create a resource in Azure portal." lightbox="./media/quickstart-create-server/create-a-resource.png":::

3. Under **Categories**, select **Databases**.

    :::image type="content" source="./media/quickstart-create-server/create-an-instance-databases.png" alt-text="Screenshot that shows how to select Databases under resource categories." lightbox="./media/quickstart-create-server/create-an-instance-databases.png":::

4. From the filtered list of resource types, find the one called **Azure Database for PostgreSQL Flexible Server**.

    :::image type="content" source="./media/quickstart-create-server/create-an-instance-flexible-server.png" alt-text="Screenshot that shows the Azure Database for PostgreSQL resource type." lightbox="./media/quickstart-create-server/create-an-instance-flexible-server.png":::

5. Select **Create**.

    :::image type="content" source="./media/quickstart-create-server/create-an-instance-flexible-server-create.png" alt-text="Screenshot that shows the Create link in the Azure Database for PostgreSQL resource type." lightbox="./media/quickstart-create-server/create-an-instance-flexible-server-create.png":::

6. The **New Azure Database for PostgreSQL flexible server** wizard launches.

    :::image type="content" source="./media/quickstart-create-server/new-server-wizard.png" alt-text="Screenshot that shows the New Azure Database for PostgreSQL wizard." lightbox="./media/quickstart-create-server/new-server-wizard.png":::

7. Provide all information required, starting from the **Basics** tab.

    :::image type="content" source="./media/quickstart-create-server/fill-basics.png" alt-text="Screenshot that shows the Basics tab of the New Azure Database for PostgreSQL wizard to create a new instance." lightbox="./media/quickstart-create-server/fill-basics.png":::

8. Use the following table to understand the meaning of the different fields available in the **Basics** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Project details** | | | | |
    | | **Subscription** | Select the name of the [subscription](/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings#subscriptions) in which you want to create the resource. | A subscription is an agreement with Microsoft to use one or more Microsoft cloud platforms or services, for which charges accrue based on either a per-user license fee or on cloud-based resource consumption. If you have multiple subscriptions, choose the subscription in which you'd like to be billed for the resource. | An existing Azure Database for PostgreSQL flexible server instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | | **Resource group** | The [resource group](/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) in the selected subscription, in which you want to create the resource. It can be an existing resource group, or you can select **Create new**, and provide a name in that subscription which is unique among the existing resource group names. | A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution, or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can easily deploy, update, and delete them as a group | An existing Azure Database for PostgreSQL flexible server instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | **Server details** | | | | |
    | | **Server name** | The name that you want to assign to the server. | A unique name that identifies your Azure Database for PostgreSQL flexible server instance. The domain name `postgres.database.azure.com` is appended to the server name you provide, to conform the fully qualified host name by which you can use a Domain Naming System server to resolve the IP address of your instance. | Although the server name can't be changed after server creation, you can use the [point in time recovery](../backup-restore/concepts-backup-restore.md#point-in-time-recovery) feature, to restore the server under a different name. An alternative approach to continue using the existing server, but being able to refer to it using a different server name, would use the [virtual endpoints](../read-replica/concepts-read-replicas-virtual-endpoints.md) to create a writer endpoint with the new desired name. With this approach, you could refer to the instance by its original name, or that assigned to the write virtual endpoint. |
    | | **Region** | The name of one of the [regions in which the service is supported](../overview.md#azure-regions), and is more adequate for you to deploy your instance. | Compliance, data residency, pricing, proximity to your users, or availability of other services in the same region, are some of the requirements you should use when choosing the region. | The service doesn't offer a feature to automatically and transparently relocate an instance to a different region.  |
    | | **PostgreSQL version** | The version selected by default. | You can select among the list of major versions of PostgreSQL currently supported by the service. Currently those versions are: **[!INCLUDE [major-versions-ascending](../includes/major-versions-ascending.md)]** |
    | | **Workload type** | Default SKU selection. | You can choose from `Development` (Burstable SKU), `Production` (General Purpose, by default, or Memory Optimized SKUs). You can further customize the SKU and storage by selecting **Configure server**. | The service provides a built-in feature which can upgrade the current major version of your instance to any other higher version supported by the feature. For more information, see [major version upgrades](concepts-major-version-upgrade.md). |
    | | **Availability zone** | Your preferred [availability zone](/azure/reliability/availability-zones-overview). | You can choose in which availability zone you want your server to be deployed. Being able to choose the availability zone in which your instance is deployed, is useful to colocate it with your application. If you choose *No preference*, a default availability zone is automatically assigned to your instance during its creation. | Although the availability zone in which an instance is deployed can't be changed after its creation, you can use the [point in time recovery](../backup-restore/concepts-backup-restore.md#point-in-time-recovery) feature to restore the server under a different name on a different availability zone. |
    | **High availability** | | | | |
    | | **High availability** | Enable it for **Same zone** or **Zone redundant**. | If you select either of these two options, a standby server with the same configuration as your primary is automatically provisioned. The standby server is provisioned in the same availability zone or in a different availability zone within the same region, depending on the option selected. Notice that high availability can be enabled or disabled after the server is created. | High availability can be enabled or disabled after server creation. However, if it's enabled, it can't be changed directly from **Same zone** to **Zone redundant** or vice versa. In order to implement such change, you first need to disable high availability, and then re-enable it choosing the newly desired mode. |
    | **Authentication** | | | | |
    | | **Authentication method** | Although the recommended authentication method is **Microsoft Entra authentication**, for the sake of simplicity, in this quickstart let's select **PostgreSQL authentication only**. | By selecting **PostgreSQL authentication only**, you're required to provide a PostgreSQL native user name and a password. If you choose **Microsoft Entra authentication**, you need to provide the object identifier of the Microsoft Entra user or group which you want to assign as the administrator of the instance. If you choose, **PostgreSQL and Microsoft Entra authentication**, you need to satisfy both previous requirements. | Can be changed to any of the three supported values after server creation. |
    | | **Administrator login** | The name of the PostgreSQL native user that you want to assign as the administrator of your instance. For this example, let's set it to `adminuser`. | The admin username must contain between 1 and 63 characters, must only consist of numbers and letters, can’t start with **pg_** and can't be **azure_superuser**, **azure_pg_admin**, **admin**, **administrator**, **root**, **guest**, or **public**. | The name of this user can't be changed after the instance is created. Also, it can't be replaced with some other PostgreSQL native user that you could create in the instance. |
    | | **Password** | The password that you want to assign to the PostgreSQL native user which is designated as an administrator. | Specify a password for the server admin account. Make sure that your password is complex enough. | Can be changed as many times as needed after the server is created. |
    | | **Confirm password** | The password that you want to assign to the PostgreSQL native user which is designated as an administrator. | Must match the value assign to **Password**. | Can be changed as many times as needed after the server is created. |

9. To configure the compute and storage further, under **Server details**, in the **Compute + storage** section, select **Configure server**. The **Compute + storage** page opens, where you can configure several settings specific to the type of compute and storage you want to use. Once you configure your compute and storage according to your needs, select **Save** to return to the **Basics** page and continue configuring your instance.

    :::image type="content" source="./media/quickstart-create-server/fill-compute-and-storage.png" alt-text="Screenshot that shows the Compute + storage page where you can configure compute and storage of your server." lightbox="./media/quickstart-create-server/fill-compute-and-storage.png":::

10. Use the following table to understand the meaning of the different fields available in the **Compute + storage** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Cluster** | | | | |
    | | **Cluster options** | Select **Server**. | Possible values are **Server** (for workloads that can fit on one node) and **Elastic cluster** (for capacity larger than a single node, elastic cluster provides schema and row-based sharding on a database distributed across a cluster). | Can't be changed on existing servers. |
    | | **Node count** | Set it to **2**. | This option is only available when **Cluster options** is set to **Elastic cluster**. Allowed range of values span from 1 to 20. | Can be changed on existing servers. |
    | **Compute** | | | | |
    | | **Compute tier** | Select **General Purpose**. | Possible values are **Burstable** (typically used for development environments in which workloads don't need the full capacity of the CPU continuously) and **General Purpose** (typically used for production environments with most common workloads), and **Memory Optimized** (typically used for production environments running workloads that require a high memory to CPU ratio). For more information, see [Compute options in Azure Database for PostgreSQL](concepts-compute.md). | Can be changed after the server is created. However, if you're using some functionality which is only supported on certain tiers, and change the current tier to one in which the feature isn't supported, the feature stops being available or gets disabled. |
    | | **Compute processor** | Leave the default setting. | Notice that this option might not be visible for some regions. If the region selected in the **Basics** tab supports processors from more than one manufacturer, then the option is visible. In the regions supporting processors from different manufacturers, possible values are **AMD** and **Intel**. For more information, see [Compute options in Azure Database for PostgreSQL](concepts-compute.md). | Can be changed for existing instances, as long as the region in which the instance is deployed offers processors from more than one manufacturer. |
    | | **Compute size** | Leave the default setting. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL](concepts-compute.md). | Can be changed after instance is created. |
    | **Storage** | | | | |
    | | **Storage type** | Select **Premium SSD**. | Notice that the list of allowed values might vary depending on which other features you selected. For more information, see [Storage options in Azure Database for PostgreSQL](../extensions/concepts-storage.md). | Can't be changed after the instance is created. |
    | | **Storage size** | Leave the default setting. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL](concepts-compute.md). | Can be changed after the instance is created. It can only be increased. Manual or automatic shrinking of storage isn't supported. Acceptable values depend on the type of storage assigned to the instance. |
    | | **Performance tier** | Leave the default setting. | Performance of Premium solid-state drives (SSD) is set when you create the disk, in the form of their performance tier. When setting the provisioned size of the disk, a performance tier is automatically selected. This performance tier determines the IOPS and throughput of your managed disk. For Premium SSD disks, this tier can be changed at deployment or afterwards, without changing the size of the disk, and without downtime. Changing the tier allows you to prepare for and meet higher demand without using your disk's bursting capability. It can be more cost-effective to change your performance tier rather than rely on bursting, depending on how long the extra performance is necessary. This is ideal for events that temporarily require a consistently higher level of performance, like holiday shopping, performance testing, or running a training environment. To handle these events, you can switch a disk to a higher performance tier without downtime, for as long as you need the extra performance. You can then return to the original tier without downtime when the extra performance is no longer necessary. | Can be changed after the instance is created. |
    | | **Storage autogrow** | Select this option to enable the autogrow feature. | Notice that this option might not be supported for some storage types, and it might not be honored for certain storage sizes. For more information, see [Configure storage autogrow](../scale/how-to-auto-grow-storage.md). | Can be changed after the instance is created, as long as the storage type supports this feature. |
    | **High availability** | | | | |
    | | **High availability** | Leave the value that is selected by default. | Supported values are **Disabled** (99.9% SLA), **Same zone** (99.95% SLA), and **Zone redundant** (99.99% SLA). Notice that supported high availability options might vary depending on the region in which you're trying to deploy your instance. For more information, see [High availability in Azure Database for PostgreSQL](/azure/reliability/reliability-postgresql-flexible-server). | High availability can be enabled or disabled after server creation. However, if it's enabled, it can't be changed directly from **Same zone** to **Zone redundant** or viceversa. In order to implement such change, you first need to disable high availability, and then re-enable it choosing the newly desired mode. |
    | **Backups** | | | | |
    | | **Backup retention period (in days)** | Leave the value that is selected by default. | The default backup retention period is 7 days, but you can extend the period to a maximum of 35 days. Notice that supported high availability options might vary depending on the region in which you're trying to deploy your instance. For more information, see [High availability in Azure Database for PostgreSQL](/azure/reliability/reliability-postgresql-flexible-server). | Can be changed after instance is created. |
    | | **Backup redundancy** | Automatically selected for you, based on whether or not the selected region supports multiple availability zones, and the configuration of the geographical redundancy of backups. | Possible values are **Locally redundant** (provides at least 99.999999999% durability of backup objects over a year), **Zone redundant** (provides at least 99.9999999999% durability of backup objects over a year), and **Geo-Redundant** (provides at least 99.99999999999999% durability of backup objects over a year). When **Geo-redundancy** is enabled for the backup, then the backup redundancy option is set to **Geo-Redundant**. Otherwise, if the region doesn't support multiple availability zones, then backup redundancy is set to **Locally redundant**. And if the region supports multiple availability zones, then backup redundancy is set to **Zone redundant**. For more information, see [Backup redundancy options ](../backup-restore/concepts-backup-restore.md#backup-redundancy-options). | Can't be changed after instance is created. |
    | | **Geo-redundancy** | Leave this option disabled. | Geo-redundancy in backups is only supported on instances deployed in any of the [Azure paired regions](/azure/reliability/cross-region-replication-azure). For more information, see [Geo-redundant backup and restore](../backup-restore/concepts-backup-restore.md#geo-redundant-backup-and-restore)| Can't be changed after instance is created. |

11. After providing all required information in the **Basics** tab, select **Next: Networking** to move forward to the **Network** tab, from where you can configure the networking settings of your Azure Database for PostgreSQL flexible server instance:

    :::image type="content" source="./media/quickstart-create-server/next-networking.png" alt-text="Screenshot that shows the highlights the Next: Networking button in the Basics tab of the New Azure Database for PostgreSQL wizard to create a new instance." lightbox="./media/quickstart-create-server/next-networking.png":::

    :::image type="content" source="./media/quickstart-create-server/fill-networking.png" alt-text="Screenshot that shows the Networking tab of the New Azure Database for PostgreSQL wizard to create a new instance." lightbox="./media/quickstart-create-server/fill-networking.png":::

12. Use the following table to understand the meaning of the different fields available in the **Networking** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Network connectivity** | | | | |
    | | **Connectivity method** | Select **Public access (allowed IP addresses) and Private endpoint**, for the sake of simplicity. | Possible values are **Public access (allowed IP addresses) and Private endpoint** and **Private access (VNET Integration)**. For more information, see [Networking overview for Azure Database for PostgreSQL with public access](../network/../network/concepts-networking-public.md) and [Network with private access for Azure Database for PostgreSQL](../network/concepts-networking-private.md). | Can't be changed after instance is created. |
    | **Public access** | | | | |
    | | **Allow public access to this resource through the internet using a public IP address** | Enable the checkbox. | By enabling this checkbox, you can configure firewall rules to control the IP address ranges from where clients can connect to your instance through the public endpoint. For more information, see [Networking overview for Azure Database for PostgreSQL with public access](../network/../network/concepts-networking-public.md) | Can be changed after instance is created. |
    | **Firewall rules** | | | | |
    | | **Allow public access from any Azure service within Azure to this server** | Leave the default setting. | By enabling this checkbox, you configure a special firewall rule to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers. For more information, see [Networking overview for Azure Database for PostgreSQL with public access ](../network/../network/concepts-networking-public.md) | Can be changed after instance is created. |
    | | **+ Add current client IP address ( ###.###.###.### )** | Select the link with that text. | That configures a firewall rule to allow connections from  the IP address indicated in parenthesis. That IP address corresponds to the public IP address that's used by the computer from which you're accessing Azure portal. For more information, see [Networking overview for Azure Database for PostgreSQL with public access](../network/../network/concepts-networking-public.md) | Can be changed after instance is created. |

13. After providing all required information in the **Networking** tab, select **Next: Security** to move forward to the **Security** tab, from where you can configure the data security settings of your Azure Database for PostgreSQL flexible server instance:

    :::image type="content" source="./media/quickstart-create-server/next-security.png" alt-text="Screenshot that shows the highlights the Next: Security button in the Networking tab of the New Azure Database for PostgreSQL wizard to create a new instance." lightbox="./media/quickstart-create-server/next-security.png":::

    :::image type="content" source="./media/quickstart-create-server/fill-security.png" alt-text="Screenshot that shows the Security tab of the New Azure Database for PostgreSQL wizard to create a new instance." lightbox="./media/quickstart-create-server/fill-security.png":::

14. Use the following table to understand the meaning of the different fields available in the **Security** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Data encryption** | | | | |
    | | **Data encryption key** | Leave the default setting. | Possible values are **Service-managed key** and **Customer-managed key**. For more information, see [Data encryption at rest in Azure Database for PostgreSQL](../security/security-data-encryption.md). | Can't be changed after instance is created. |

15. After providing all required information in the **Security** tab, select **Next: Tags** to move forward to the **Tags** tab, from where you can attach some [tags](/azure/azure-resource-manager/management/tag-resources) to your Azure Database for PostgreSQL flexible server instance:

    :::image type="content" source="./media/quickstart-create-server/next-tags.png" alt-text="Screenshot that shows the highlights the Next: Tags button in the Security tab of the New Azure Database for PostgreSQL wizard to create a new instance." lightbox="./media/quickstart-create-server/next-tags.png":::

    :::image type="content" source="./media/quickstart-create-server/fill-tags.png" alt-text="Screenshot that shows the Tags tab of the New Azure Database for PostgreSQL wizard to create a new instance." lightbox="./media/quickstart-create-server/fill-tags.png":::

16. Use the following table to understand the meaning of the different fields available in the **Tags** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | | | | | |
    | | **Name** | Set it to `Environment`. | For more information about, see [tags](/azure/azure-resource-manager/management/tag-resources). | Can be changed after instance is created. |
    | | **Value** | Set it to `PostgreSQL Quickstart`. | For more information about, see [tags](/azure/azure-resource-manager/management/tag-resources). | Can be changed after instance is created. |

17. After providing all required information in the **Tags** tab, select **Next: Review + create** to move forward to the **Review + create** tab, from where you can review all settings configured for your new Azure Database for PostgreSQL flexible server instance, before you trigger its creation:

    :::image type="content" source="./media/quickstart-create-server/next-review-and-create.png" alt-text="Screenshot that shows the highlights the Next: Review + create button in the Tags tab of the New Azure Database for PostgreSQL wizard to create a new instance." lightbox="./media/quickstart-create-server/next-review-and-create.png":::

    :::image type="content" source="./media/quickstart-create-server/fill-review-and-create.png" alt-text="Screenshot that shows the Review + create tab of the New Azure Database for PostgreSQL wizard to create a new instance." lightbox="./media/quickstart-create-server/fill-review-and-create.png":::

18. After reviewing that the values of all settings match your requirements, select **Create** to initiate the deployment of your new Azure Database for PostgreSQL flexible server instance:

    :::image type="content" source="./media/quickstart-create-server/next-create.png" alt-text="Screenshot that shows the highlights the Create button in the Review + create tab of the New Azure Database for PostgreSQL wizard to create a new instance." lightbox="./media/quickstart-create-server/next-create.png":::

19. A new deployment is launched to create your Azure Database for PostgreSQL flexible server instance:

    :::image type="content" source="./media/quickstart-create-server/deployment-in-progress.png" alt-text="Screenshot that shows the deployment in progress to create your Azure Database for PostgreSQL flexible server instance." lightbox="./media/quickstart-create-server/deployment-in-progress.png":::

20. When the deployment completes, you can select **Go to resource**, to get you to the **Overview** page of your new Azure Database for PostgreSQL flexible server instance, and start using it:

    :::image type="content" source="./media/quickstart-create-server/deployment-completed.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure Database for PostgreSQL flexible server instance." lightbox="./media/quickstart-create-server/deployment-completed.png":::

    :::image type="content" source="./media/quickstart-create-server/overview.png" alt-text="Screenshot that shows the Overview page of your new Azure Database for PostgreSQL flexible server instance." lightbox="./media/quickstart-create-server/overview.png":::

## [CLI](#tab/cli-create-flexible)

The [Azure Cloud Shell](/azure/cloud-shell/overview) is a free interactive shell that you can use to run the steps in this article. It has common Azure tools preinstalled and configured to use with your account.

To open the Cloud Shell, just select **Open Cloud Shell** from the upper right corner of a code block. You can also open Cloud Shell in a separate browser tab, by going to [https://shell.azure.com/bash](https://shell.azure.com/bash). Select **Copy** to copy the blocks of code, paste them into the Cloud Shell, and select **Enter** to run them.

If you prefer to install and use Azure CLI locally, this quickstart requires version 2.67.0 or later. Run `az --version` to find the version currently installed. If you need to install or upgrade Azure CLI, see [Install Azure CLI](/cli/azure/install-azure-cli).

1. You need to log in to your account using the [az login](/cli/azure/reference-index#az-login) command. Note the `id` property in the output, which refers to the **Subscription ID** for your Azure account.

    ```azurecli-interactive
    az login
    ```

2. Create an Azure Database for PostgreSQL flexible server instance, using the [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create) command.

    ```azurecli-interactive
    az postgres flexible-server create \
      --subscription <subscription> \
      --resource-group <resource-group> \
      --name <name> \
      --location <region> \
      --version <version> \
      --zone <zone> \
      --password-auth <password-auth> \
      --admin-user <admin-user> \
      --admin-password <admin-password> \
      --tier <tier> \
      --sku-name <sku-name> \
      --storage-type <storage-type> \
      --storage-size <storage-size> \
      --performance-tier <performance-tier> \
      --storage-auto-grow <storage-auto-grow> \
      --high-availability <high-availability> \
      --standby-zone <standby-zone> \
      --backup-retention <backup-retention> \
      --geo-redundant-backup <geo-redundant-backup> \
      --public-access <public-access> \
      --tags <tags>
    ```

3. Use the following table to understand the meaning of each different parameter, and as guidance to provide values for each of them:

    | Parameter | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- |
    | **subscription** | Enter the name or identifier of the [subscription](/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings#subscriptions) in which you want to create the resource. | A subscription is an agreement with Microsoft to use one or more Microsoft cloud platforms or services, for which charges accrue based on either a per-user license fee or on cloud-based resource consumption. If you have multiple subscriptions, choose the subscription in which you'd like to be billed for the resource. | An existing Azure Database for PostgreSQL flexible server instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | **resource-group** | The [resource group](/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) in the selected subscription, in which you want to create the resource. It can be an existing resource group or, if it doesn't exist, it's created. | A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution, or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can easily deploy, update, and delete them as a group | An existing Azure Database for PostgreSQL flexible server instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | **name** | The name that you want to assign to the server. | A unique name that identifies your Azure Database for PostgreSQL flexible server instance. The domain name `postgres.database.azure.com` is appended to the server name you provide, to conform the fully qualified host name by which you can use a Domain Naming System server to resolve the IP address of your instance. | Although the server name can't be changed after server creation, you can use the [point in time recovery](../backup-restore/concepts-backup-restore.md#point-in-time-recovery) feature, to restore the server under a different name. An alternative approach to continue using the existing server but being able to refer to it using a different server name, would use the [virtual endpoints](../read-replica/concepts-read-replicas-virtual-endpoints.md) to create a writer endpoint with the new desired name. With this approach, you could refer to the instance by its original name, or that assigned to the write virtual endpoint. |
    | **region** | The name of one of the [regions in which the service is supported](../overview.md#azure-regions), and is more adequate for you to deploy your instance. | Compliance, data residency, pricing, proximity to your users, or availability of other services in the same region, are some of the requirements you should use when choosing the region. | The service doesn't offer a feature to automatically and transparently relocate an instance to a different region.  |
    | **version** | The version selected by default. | You can select among the list of major versions of PostgreSQL currently supported by the service. Currently those versions are: **[!INCLUDE [major-versions-ascending](../includes/major-versions-ascending.md)]** |
     **zone** | Set it to `1`. This number represents your preferred logical [availability zone](/azure/reliability/availability-zones-overview). | You can choose in which availability zone you want your server to be deployed. Being able to choose the availability zone in which your instance is deployed, is useful to colocate it with your application. If you don't specify this parameter, a default availability zone is automatically assigned to your instance during its creation. | Although the availability zone in which an instance is deployed can't be changed after its creation, you can use the [point in time recovery](../backup-restore/concepts-backup-restore.md#point-in-time-recovery) feature to restore the server under a different name on a different availability zone. |
    | **password-auth** | Set it to `enabled`. | Although the recommended authentication method is **Microsoft Entra authentication**, which you can configure using the `--active-directory-auth` parameter, for the sake of simplicity, in this quickstart let's select use PostgreSQL authentication. By selecting setting this parameter to `enabled`, you're required to also provide values for the `--admin-user` and `--admin-password` parameters. If you set `--active-directory-auth` to `enabled`, you can use the [az postgres flexible-server ad-admin](/cli/azure/postgres/flexible-server/ad-admin) commands to create or remove Microsoft Entra users or groups as PostgreSQL administrators. | Can be enabled or disabled after server creation. |
    | **admin-user** | The name of the PostgreSQL native user that you want to assign as the administrator of your instance. For this example, let's set it to `adminuser`. | The admin username must contain between 1 and 63 characters, must only consist of numbers and letters, can’t start with **pg_** and can't be **azure_superuser**, **azure_pg_admin**, **admin**, **administrator**, **root**, **guest**, or **public**. | The name of this user can't be changed after the instance is created. Also, it can't be replaced with some other PostgreSQL native user that you could create in the instance. |
    | **admin-password** | The password that you want to assign to the PostgreSQL native user which is designated as an administrator. | Specify a password for the server admin account. Make sure that your password is complex enough. | Can be changed as many times as needed after the server is created. |
    | **tier** | Set it to `generalpurpose`. | Possible values are `burstable` (typically used for development environments in which workloads don't need the full capacity of the CPU continuously), `generalpurpose` (typically used for production environments with most common workloads), and `memoryoptimized` (typically used for production environments running workloads that require a high memory to CPU ratio). For more information, see [Compute options in Azure Database for PostgreSQL](concepts-compute.md). | Can be changed after the server is created. However, if you're using some functionality which is only supported on certain tiers, and change the current tier to one in which the feature isn't supported, the feature stops being available or gets disabled. |
    | **sku-name** | Set it to `standard_d4ds_v5`. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL](concepts-compute.md). | Can be changed after instance is created. |
    | **storage-type** | Set it to `premium_lrs`. | Notice that the list of allowed values might vary depending on which other features you selected. For more information, see [Storage options in Azure Database for PostgreSQL](../extensions/concepts-storage.md). | Can't be changed after the instance is created. |
    | **storage-size** | Set it to `128`. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL](concepts-compute.md). | Can be changed after the instance is created. It can only be increased. Manual or automatic shrinking of storage isn't supported. Acceptable values depend on the type of storage assigned to the instance. |
    | **performance-tier** | Set it to `p10`. | Performance of Premium solid-state drives (SSD) is set when you create the disk, in the form of their performance tier. When setting the provisioned size of the disk, a performance tier is automatically selected. This performance tier determines the IOPS and throughput of your managed disk. For Premium SSD disks, this tier can be changed at deployment or afterwards, without changing the size of the disk, and without downtime. Changing the tier allows you to prepare for and meet higher demand without using your disk's bursting capability. It can be more cost-effective to change your performance tier rather than rely on bursting, depending on how long the extra performance is necessary. This is ideal for events that temporarily require a consistently higher level of performance, like holiday shopping, performance testing, or running a training environment. To handle these events, you can switch a disk to a higher performance tier without downtime, for as long as you need the extra performance. You can then return to the original tier without downtime when the extra performance is no longer necessary. | Can be changed after the instance is created. |
    | **storage-auto-grow** | Set it to `enabled`. | Notice that this option might not be supported for some storage types, and it might not be honored for certain storage sizes. For more information, see [Configure storage autogrow](../scale/how-to-auto-grow-storage.md). | Can be changed after the instance is created, as long as the storage type supports this feature. |
    | **high-availability** | Set it to `zoneredundant`. | Supported values are **disabled** (99.9% SLA), **samezone** (99.95% SLA), and **zoneredundant** (99.99% SLA). Notice that supported high availability options might vary depending on the region in which you're trying to deploy your instance. For more information, see [High availability in Azure Database for PostgreSQL](/azure/reliability/reliability-postgresql-flexible-server). | High availability can be enabled or disabled after server creation. However, if it's enabled, it can't be changed directly from **samezone** to **zoneredundant** or viceversa. In order to implement such change, you first need to disable high availability, and then re-enable it choosing the newly desired mode. |
    | **standby-zone** | Set it to `2`. This number represents your preferred logical [availability zone](/azure/reliability/availability-zones-overview) for the hot standby replica. | You can choose in which availability zone you want your server to be deployed. Being able to choose the availability zone in which your instance is deployed, is useful to colocate it with your application. If you choose *No preference*, a default availability zone is automatically assigned to your instance during its creation. | Although the availability zone in which an instance is deployed can't be changed after its creation, you can use the [point in time recovery](../backup-restore/concepts-backup-restore.md#point-in-time-recovery) feature to restore the server under a different name on a different availability zone. |
    | **backup-retention** | Set it to `7`. | The default backup retention period is 7 days, but you can extend the period to a maximum of 35 days. Notice that supported high availability options might vary depending on the region in which you're trying to deploy your instance. For more information, see [High availability in Azure Database for PostgreSQL](/azure/reliability/reliability-postgresql-flexible-server). | Can be changed after instance is created. |
    | **geo-redundant-backup** | Set it to `disabled`. | Geo-redundancy in backups is only supported on instances deployed in any of the [Azure paired regions](/azure/reliability/cross-region-replication-azure). For more information, see [Geo-redundant backup and restore](../backup-restore/concepts-backup-restore.md#geo-redundant-backup-and-restore)| Can't be changed after instance is created. |
    | **public-access** | Set it to `$(curl ipinfo.io/ip)` to create a firewall rule that allowlists the public IP address of the computer from which you're running the Azure CLI commands. That allows you to connect to your new instance from that computer. | Possible values are `all`, `none`, `<startIpAddress>`, or `<startIpAddress>-<endIpAddress>` . For more information, see [Networking overview for Azure Database for PostgreSQL with public access](../network/../network/concepts-networking-public.md) and [Network with private access for Azure Database for PostgreSQL](../network/concepts-networking-private.md). | Can't be changed after instance is created. |
    | **tags** | Set it to `"Environment=PostgreSQL Quickstart"`. | For more information about, see [tags](/azure/azure-resource-manager/management/tag-resources). | Can be changed after instance is created. |

4. If the deployment completes successfully, you should receive an output from the CLI command like the following:

    ```json
    {
    "connectionString": "postgresql://<admin-user>:<admin-password>@<name>.postgres.database.azure.com/None?sslmode=require",
    "databaseName": null,
    "firewallName": "FirewallIPAddress_<timestamp>",
    "host": "<name>.postgres.database.azure.com",
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<name>",
    "location": "<region>",
    "password": "<admin-password>",
    "resourceGroup": "<reource-group>",
    "skuname": "<sku-name>",
    "username": "<admin-user>",
    "version": "<version>"
    }
    ```

## [ARM template](#tab/arm-create-flexible)

[!INCLUDE [About Azure Resource Manager](~/reusable-content/ce-skilling/azure/includes/resource-manager-quickstart-introduction.md)]

Azure Resource Manager is the deployment and management service for Azure. It provides a management layer that enables you to create, update, and delete resources in your Azure account. You use management features, like access control, locks, and tags, to secure and organize your resources after deployment. To learn about Azure Resource Manager templates, see [Template deployment overview](/azure/azure-resource-manager/templates/overview).

An Azure Database for PostgreSQL flexible server instance is the parent resource for one or more databases within a region. It provides the scope for management policies that apply to its databases: login, firewall, users, roles, and configurations.

1. Create a file called `postgres-flexible-server-template.json`, and copy the following JSON definition into it.

    ```json
    {
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "serverName": {
        "type": "string"
        },
        "location": {
        "type": "string",
        "defaultValue": "[resourceGroup().location]"
        },
        "version": {
        "type": "string",
        "defaultValue": "16"
        },
        "availabilityZone": {
        "type": "string",
        "defaultValue": "1"
        },
        "activeDirectoryAuth": {
        "type": "string",
        "defaultValue": "Disabled"
        },
        "passwordAuth": {
        "type": "string",
        "defaultValue": "Enabled"
        },
        "administratorLogin": {
        "type": "string",
        "defaultValue": "adminuser"
        },
        "administratorLoginPassword": {
        "type": "secureString"
        },
        "skuTier": {
        "type": "string",
        "defaultValue": "GeneralPurpose"
        },
        "skuName": {
        "type": "string",
        "defaultValue": "Standard_D4ds_v5"
        },
        "storageType": {
        "type": "string",
        "defaultValue": "Premium_LRS"
        },
        "storageSizeGB": {
        "type": "int",
        "defaultValue": 128
        },
        "storageTier": {
        "type": "string",
        "defaultValue": "P10"
        },
        "storageAutoGrow": {
        "type": "string",
        "defaultValue": "Enabled"
        },
        "highAvailabilityMode": {
        "type": "string",
        "defaultValue": "ZoneRedundant"
        },
        "standbyAvailabilityZone": {
        "type": "string",
        "defaultValue": "2"
        },
        "backupRetentionDays": {
        "type": "int",
        "defaultValue": 7
        },
        "geoRedundantBackup": {
        "type": "string",
        "defaultValue": "Disabled"
        },
        "publicNetworkAccess": {
        "type": "string",
        "defaultValue": "Enabled"
        },
        "tags": {
        "type": "object",
        "defaultValue": {
            "Environment": "PostgreSQL Quickstart"
        }
        },
        "firewallRules": {
        "type": "array"
        }
    },
    "resources": [
        {
        "type": "Microsoft.DBforPostgreSQL/flexibleServers",
        "apiVersion": "2024-08-01",
        "name": "[parameters('serverName')]",
        "location": "[parameters('location')]",
        "sku": {
            "tier": "[parameters('skuTier')]",
            "name": "[parameters('skuName')]"
        },
        "properties": {
            "version": "[parameters('version')]",
            "administratorLogin": "[parameters('administratorLogin')]",
            "administratorLoginPassword": "[parameters('administratorLoginPassword')]",
            "authConfig": {
            "activeDirectoryAuth": "[parameters('activeDirectoryAuth')]",
            "passwordAuth": "[parameters('passwordAuth')]"
            },
            "network": {
            "publicNetworkAccess": "[parameters('publicNetworkAccess')]"
            },
            "highAvailability": {
            "mode": "[parameters('highAvailabilityMode')]",
            "standbyAvailabilityZone": "[parameters('standbyAvailabilityZone')]"
            },
            "storage": {
            "autoGrow": "[parameters('storageAutoGrow')]",
            "storageSizeGB": "[parameters('storageSizeGB')]",
            "tier": "[parameters('storageTier')]",
            "type": "[parameters('storageType')]"
            },
            "backup": {
            "backupRetentionDays": "[parameters('backupRetentionDays')]",
            "geoRedundantBackup": "[parameters('geoRedundantBackup')]"
            },
            "availabilityZone": "[parameters('availabilityZone')]",
            "tags": "[parameters('tags')]"
        }
        },
        {
        "copy": {
            "name": "createFirewallRules",
            "count": "[length(range(0, if(greater(length(parameters('firewallRules')), 0), length(parameters('firewallRules')), 1)))]",
            "mode": "serial",
            "batchSize": 1
        },
        "type": "Microsoft.Resources/deployments",
        "apiVersion": "2020-10-01",
        "name": "[format('firewallRules-{0}', range(0, if(greater(length(parameters('firewallRules')), 0), length(parameters('firewallRules')), 1))[copyIndex()])]",
        "properties": {
            "expressionEvaluationOptions": {
            "scope": "inner"
            },
            "mode": "Incremental",
            "parameters": {
            "ip": {
                "value": "[parameters('firewallRules')[range(0, if(greater(length(parameters('firewallRules')), 0), length(parameters('firewallRules')), 1))[copyIndex()]]]"
            },
            "serverName": {
                "value": "[parameters('serverName')]"
            }
            },
            "template": {
            "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "serverName": {
                "type": "string"
                },
                "ip": {
                "type": "object"
                }
            },
            "resources": [
                {
                "type": "Microsoft.DBforPostgreSQL/flexibleServers/firewallRules",
                "apiVersion": "2024-08-01",
                "name": "[format('{0}/{1}', parameters('serverName'), parameters('ip').name)]",
                "properties": {
                    "startIpAddress": "[parameters('ip').startIPAddress]",
                    "endIpAddress": "[parameters('ip').endIPAddress]"
                }
                }
            ]
            }
        },
        "dependsOn": [
            "[resourceId('Microsoft.DBforPostgreSQL/flexibleServers', parameters('serverName'))]"
        ]
        }
    ]
    }
    ```

These resources are defined in the [Microsoft.DBforPostgreSQL/flexibleServers](/azure/templates/microsoft.dbforpostgresql/flexibleservers?tabs=json&pivots=deployment-language-arm-template) and [Microsoft.DBforPostgreSQL/flexibleServers/firewallRules](/azure/templates/microsoft.dbforpostgresql/flexibleservers/firewallrules?tabs=json&pivots=deployment-language-arm-template) templates.

2. Select **Open Cloud Shell** from the following code block, to open Azure Cloud Shell. Copy and paste the code, replace the argument placeholders with your own values, and select **Enter**.

    ```azurecli-interactive
    az group create --name <resource-group> --location <region>
    az deployment group create --name QuickstartAzureDatabaseForPostgreSQLFlexibleServer --resource-group <resource-group> --template-file <path-to-template-file> --parameters serverName=<server> administratorLoginPassword=<admin-password> firewallRules="[{'name':'ClientIPAddress','startIPAddress':'$(curl ipinfo.io/ip)','endIPAddress':'$(curl ipinfo.io/ip)'}]"
    ```

---

## Databases available in an Azure Database for PostgreSQL  instance

By default, a database called **postgres** is created in your instance. The [postgres](https://www.postgresql.org/docs/current/static/app-initdb.html) database is a default database that's meant for use by users, utilities, and third-party applications.

A second database that is created on every instance is **azure_maintenance**. Although you can connect to this database, you have minimum permissions granted so you can barely do anything in it.

Finally, there's database **azure_sys**, which is used to host some objects used by features like [query store](../monitor/concepts-query-store.md) and [index tuning](../monitor/concepts-index-tuning.md).

> [!NOTE]
> Connections to your Azure Database for PostgreSQL flexible server instance typically communicate over port 5432. An exception to this is when you're connecting via a connection pooler like the built-in [PgBouncer](../connectivity/../connectivity/concepts-pgbouncer.md), which is integrated with Azure Database for PostgreSQL. Built-in PgBouncer listens on port 6432.
> When you try to connect from within a corporate network, outbound traffic over port 5432 (or 6432 if you're connecting through PgBouncer) might be blocked by your network's firewall. If that's the case, you won't be able to connect to your instance, unless your IT department allows you to route traffic from your computer to the target instance, via the necessary port (5432 or 6432).

## Get the connection information

To connect to your instance, you need to have its fully qualified name and the credentials of the user with which you want to connect. You should have noted those values from when you deployed the instance, earlier in this article. If you didn't, you can retrieve everything but the password of the administrator user. If you forgot the password assigned to your instance, you can always reset it. To learn how to do it, see [reset admin password](how-to-manage-server-portal.md#reset-admin-password).

## [Portal](#tab/portal-get-connection)

Using the [Azure portal](https://portal.azure.com/):

1. Open the **Overview** page of your new instance.

    :::image type="content" source="./media/quickstart-create-server/overview-copy-information.png" alt-text="Screenshot that shows the Overview page." lightbox="./media/quickstart-create-server/overview-copy-information.png":::

2.  Copy the value of **Endpoint**, and save it somewhere to use it later. Hover your cursor over each field, and the copy symbol appears to the right of the text. Select the copy symbol as needed to copy the values.

    :::image type="content" source="./media/quickstart-create-server/overview-copy-server-name.png" alt-text="Screenshot that shows how to copy the server name from the Overview page." lightbox="./media/quickstart-create-server/overview-copy-server-name.png":::

3.  Copy the value of **Administrator login**, and save it somewhere to use it later. Hover your cursor over each field, and the copy symbol appears to the right of the text. Select the copy symbol as needed to copy the values.

    :::image type="content" source="./media/quickstart-create-server/overview-copy-admin-login-name.png" alt-text="Screenshot that shows how to the admin user name from the Overview page." lightbox="./media/quickstart-create-server/overview-copy-admin-login-name.png":::

 ## [CLI](#tab/cli-create-get-connection)

The [Azure Cloud Shell](/azure/cloud-shell/overview) is a free interactive shell that you can use to run the steps in this article. It has common Azure tools preinstalled and configured to use with your account.

To open the Cloud Shell, just select **Open Cloud Shell** from the upper right corner of a code block. You can also open Cloud Shell in a separate browser tab, by going to [https://shell.azure.com/bash](https://shell.azure.com/bash). Select **Copy** to copy the blocks of code, paste them into the Cloud Shell, and select **Enter** to run them.

If you prefer to install and use Azure CLI locally, this quickstart requires version 2.67.0 or later. Run `az --version` to find the version currently installed. If you need to install or upgrade Azure CLI, see [Install Azure CLI](/cli/azure/install-azure-cli).

1. Run the following command to retrieve the fully qualified name of the instance and the name of the administrator user:

    ```azurecliinteractive
    az postgres flexible-server show \
      --resource-group <resource-group> \
      --name <server> \
      --query "{serverName:fullyQualifiedDomainName, adminUser:administratorLogin}" \
      --output table
    ```

---

## Connect using psql

There are many applications you can use to connect to your Azure Database for PostgreSQL flexible server instance. If your client computer has PostgreSQL installed, you can use a local instance of [psql](https://www.postgresql.org/docs/current/static/app-psql.html) to connect to an Azure Database for PostgreSQL flexible server instance. If it isn't installed on your machine, [download the ready-to-use package](https://www.postgresql.org/download) that targets your platform and install it.

Once installed, you can use the psql command-line utility to connect to the Azure Database for PostgreSQL flexible server instance.

1. Run the following psql command to connect to an Azure Database for PostgreSQL flexible server instance.

   ```bash
   psql "host=<server> port=<port> user=<admin-user> dbname=postgres sslmode=require"
   ```

   For example, the following command connects to the default database called `postgres` on your Azure Database for PostgreSQL flexible server instance `production-flexible-server.postgres.database.azure.com` using a user name called `adminuser`. When prompted, type the password corresponding to that user.

   ```bash
   psql "host=production-flexible-server.postgres.database.azure.com port=5432 user=adminuser dbname=postgres sslmode=require"
   ```

   After you connect, the psql utility displays a postgres prompt where you type sql commands. In the initial connection output, a warning might appear because the psql you're using might be a different version than that of the Azure Database for PostgreSQL flexible server instance version.

   Example psql output:

   ```output
    psql (14.13, server 16.4)
    WARNING: psql major version 14, server major version 16.
            Some psql features might not work.
    SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
    Type "help" for help.

    postgres=>
   ```

    If there's no firewall rule on the instance for the public IP address from which you're trying to connect, you receive an error like:

    ```output 
    psql: error: connection to server at "<server>.postgres.database.azure.com" (###.###.###.###), port 5432 failed: Connection timed out
            Is the server running on that host and accepting TCP/IP connections?
    ```

2. Create a blank database called `user_database` at the prompt by typing the following command:

    ```sql
    CREATE DATABASE user_database;
    ```

3. At the prompt, execute the following command to switch connections to the newly created database `user_database`:

    ```sql
    \c user_database
    ```

4. Type  `\q`, and then select **Enter** to quit psql.

You connected to the Azure Database for PostgreSQL flexible server instance via psql, and you created a blank user database.

## Clean up resources

You can clean up the resources that you created in this quickstart in one of two ways. You can delete the Azure resource group, which includes all the resources in the resource group. If you want to keep other resources deployed in the same resource group intact, you can delete only the Azure Database for PostgreSQL flexible server instance.

## [Portal](#tab/portal-delete-resources)

Using the [Azure portal](https://portal.azure.com/):

To delete the entire resource group, including the newly created server.

1. Select **Resource groups**.

    :::image type="content" source="./media/quickstart-create-server/resource-groups.png" alt-text="Screenshot that shows how to select Resource groups." lightbox="./media/quickstart-create-server/resource-groups.png":::

2. Search for the resource group that you want to delete, and select its name.

    :::image type="content" source="./media/quickstart-create-server/resource-group-select.png" alt-text="Screenshot that shows how to select one resource group." lightbox="./media/quickstart-create-server/resource-group-select.png":::

3. In the **Overview** page of the resource group chosen, select **Delete resource group**.

    :::image type="content" source="./media/quickstart-create-server/resource-group-delete.png" alt-text="Screenshot that shows how to initiate the deletion of one resource group." lightbox="./media/quickstart-create-server/resource-group-delete.png":::

4. Enter the name of the resource group in the **Enter resource group name to confirm deletion** text box.

    :::image type="content" source="./media/quickstart-create-server/resource-group-delete-confirm.png" alt-text="Screenshot that shows how to confirm the deletion of one resource group." lightbox="./media/quickstart-create-server/resource-group-delete-confirm.png":::

5. Select **Delete**.

    :::image type="content" source="./media/quickstart-create-server/resource-group-delete-delete.png" alt-text="Screenshot that shows the Delete button." lightbox="./media/quickstart-create-server/resource-group-delete-delete.png":::

To delete only the newly created server.

1. Locate your server in the portal, if you don't have it open. One way to do it is by typing the name of the server in the search bar. When the resource with the matching name is shown, select that resource.

2. In the **Overview** page, select **Delete**.

    :::image type="content" source="./media/quickstart-create-server/server-delete.png" alt-text="Screenshot that shows the Delete button in the Overview page." lightbox="./media/quickstart-create-server/server-delete.png":::

3. Select **I have read and understand that this server, as well as any databases it contains, will be deleted.**.

    :::image type="content" source="./media/quickstart-create-server/confirm-deletion-terms.png" alt-text="Screenshot that shows the checkbox to acknowledge the terms under which a server is deleted." lightbox="./media/quickstart-create-server/confirm-deletion-terms.png":::

4. Select **Delete**.

    :::image type="content" source="./media/quickstart-create-server/trigger-delete.png" alt-text="Screenshot that shows the Delete button in the Delete server pane." lightbox="./media/quickstart-create-server/trigger-delete.png":::

## [CLI](#tab/cli-delete-resources)

To delete the entire resource group, including the newly created server, execute the following command:

```azurecliinteractive
az group delete --name <resource-group>
```

To delete only the newly created server, execute the following command:

```azurecliinteractive
az postgres flexible-server delete \
  --resource-group <resource-group> \
  --name <name>
```

---