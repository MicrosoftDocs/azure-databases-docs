---
title: Restore to custom restore point in Azure HorizonDB
description: This article describes how to restore to custom restore point an Azure HorizonDB.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: how-to
#customer intent: As a user, I want to learn how to restore to custom restore point an Azure HorizonDB.
---

# Restore to custom restore point in Azure HorizonDB

This article provides step-by-step instructions to perform a restore of an Azure HorizonDB  to a custom restore point.

## Steps to restore to custom restore point

### [Portal](#tab/portal-restore-custom-point)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB .

2. In the resource menu, select **Overview**.

    :::image type="content" source="./media/how-to-restore-server/overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/how-to-restore-server/overview.png":::

3. Select the **Restore** button.

    :::image type="content" source="./media/how-to-restore-server/restore-button.png" alt-text="Screenshot showing the location of the Restore button in the Overview page." lightbox="./media/how-to-restore-server/restore-button.png":::

4. You're redirected to the **Create Azure HorizonDB  - Restore** wizard, from where you can configure some settings for the new cluster that is getting created. In the **Point-in-time-restore (PITR)** section, select **Select a custom restore point**.

    :::image type="content" source="./media/how-to-restore-server/custom-restore-point.png" alt-text="Screenshot showing the Select a custom restore point radio button selected." lightbox="./media/how-to-restore-server/custom-restore-point.png":::

5. In **Custom restore point (UTC)**, select a date from the calendar control, and specify a time in the time text box. Select a restore point based on your requirements. The most recent available restore point is always at least 5 minutes behind the current time.

    :::image type="content" source="./media/how-to-restore-server/custom-restore-point-date-time.png" alt-text="Screenshot showing the date picker and time textbox, available to configure the custom restore point." lightbox="./media/how-to-restore-server/custom-restore-point-date-time.png":::

> [!NOTE]
>  Point-in-time restore is limited to timestamps that are at least 300 seconds earlier than the current time. Select a restore point that is at least 5 minutes in the past.

6. Use the following table to understand the meaning of the different fields available in the **Basics** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Project details** | | | | |
    | | **Subscription** | The name of the [subscription](/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings#subscriptions) in which you want to create the resource. | A subscription is an agreement with Microsoft to use one or more Microsoft cloud platforms or services, for which charges accrue based on either a per-user license fee or on cloud-based resource consumption. | An existing Azure HorizonDB  instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | | **Resource group** | The [resource group](/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) in the selected subscription, in which you want to create the resource. It can be an existing resource group, or you can select **Create new**, and provide a name in that subscription which is unique among the existing resource group names. | A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution, or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can easily deploy, update, and delete them as a group | An existing Azure HorizonDB  instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | **Source details** | | | | |
    | | **Source server** | The name of the server whose backup you want to restore on the newly deployed server. | | |
    | | **Earliest restore point** | The oldest backup of the source server available to restore from. the server whose backup you want to restore on the newly deployed server. Backups are automatically deleted, based on the backup retention period configured on the source server. | | |
    | | **Point-in-time-restore (PITR)** | Possible options are **Latest restore point (Now)**, **Select a custom restore point**, and **Select Fast restore point (Restore using full backup only)**. | To restore to latest restore point, select **Latest restore point (Now)**. | |
    | **Server details** | | | | |
    | | **Name** | The name that you want to assign to the newly deployed server, on top of which a backup of the source is restored. | A unique name that identifies your Azure HorizonDB  instance. The domain name `postgres.database.azure.com` is appended to the server name you provide, to conform the fully qualified host name by which you can use a Domain Naming System server to resolve the IP address of your instance. | Although the server name can't be changed after server creation, you can use the point in time recovery feature, to restore the server under a different name. An alternative approach to continue using the existing server, but being able to refer to it using a different server name, would use the [virtual endpoints](../read-replica/../read-replica/../read-replica/concepts-read-replicas-virtual-endpoints.md) to create a writer endpoint with the new desired name. With this approach, you could refer to the instance by its original name, or that assigned to the write virtual endpoint. |
    | | **Location** | The name of one of the [regions in which the service is supported](../overview.md#azure-regions). Point in time restore only supports the deployment of the new server in the same region in which the source server exists. | Compliance, data residency, pricing, proximity to your users, or availability of other services in the same region, are some of the requirements you should use when choosing the region. | The service doesn't offer a feature to automatically and transparently relocate an instance to a different region. |
    | | **PostgreSQL version** | The version selected by default. | Point in time restore only supports the deployment of the new server with the exact same major version used by the source server. Currently those versions are: **[!INCLUDE [major-versions-ascending](../includes/major-versions-ascending.md)]** | Azure HorizonDB  supports in-place upgrade, via [major version upgrade](../configure-maintain/how-to-perform-major-version-upgrade.md). |
    | | **Availability zone** | Your preferred [availability zone](/azure/reliability/availability-zones-overview). | You can choose in which availability zone you want your server to be deployed. Being able to choose the availability zone in which your instance is deployed, is useful to colocate it with your application. If you choose *No preference*, a default availability zone is automatically assigned to your instance during its creation. | Although the availability zone in which an instance is deployed can't be changed after its creation, you can use the point in time recovery feature to restore the server under a different name on a different availability zone. |
    | | **Compute + storage** | Assigns the same type and size of compute and same size of storage, as the ones used by the source server at the time the backup is restored. However, if you select the **Configure server** link, you can change the type of storage allocated to the new server, and whether or not it should be provisioned with geo-redundant backups. | | After the new server is deployed, its compute options can be scaled up or down. |

7. If you want to change the type of storage assigned to the new server, or if you want to deploy it with geo-redundant backups, select **Configure server**:

    :::image type="content" source="./media/how-to-restore-server/configure-server-button.png" alt-text="Screenshot showing the location of the Configure server link." lightbox="./media/how-to-restore-server/configure-server-button.png":::

8. The **Compute** opens to show compute options for the new server:

    :::image type="content" source="./media/how-to-restore-server/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/how-to-restore-server/configure-server-page.png":::

9. Use the following table to understand the meaning of the different fields available in the **Compute +** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Compute** | | | | |
    | | **Compute size** | Change the processor and vcores as per your needs. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure HorizonDB ](../compute-storage/concepts-compute.md). | Can be changed after instance is created. |
    | **Replicas** | | | | |
    | | **High Availability** | Choose *Zone redundant - Replica ina different availability zone* or  *Disabled* based upon your high availability needs. |
    | | **Readable high availability replicas** | use the slider to configure number of replicas.

    | **Backups** | | | | |
    | | **Backup retention period (in days)** | Can't be changed and is automatically set to 7. | The default backup retention period is 7 days. |
    
10. Once all the new server is configured to your needs, select **Review + create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-review-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="./media/how-to-restore-server/restore-point-review-create.png":::

11. Review that all configurations for the new deployment are correctly set, and select **Create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-create.png" alt-text="Screenshot showing the location of the Create button." lightbox="./media/how-to-restore-server/restore-point-create.png":::

12. A new deployment is launched to create your new Azure HorizonDB  and restore the most recent data available on the source server at the time of restore:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-progress.png" alt-text="Screenshot that shows the deployment in progress to create your new Azure HorizonDB , on which the most recent data available on the source server is restored." lightbox="./media/how-to-restore-server/restore-point-deployment-progress.png":::

13. When the deployment completes, you can select **Go to resource**, to get you to the **Overview** page of your new Azure HorizonDB , and start using it:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-completed.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure HorizonDB ." lightbox="./media/how-to-restore-server/restore-point-deployment-completed.png":::

> [!NOTE]
> - The value passed to the `--restore-time` parameter represents the point in time, in UTC, to restore from (ISO8601 format).
> - If the `--restore-time` parameter isn't present, its value defaults to the current time in the system from where the command is executed.
> - If the value passed is in the future, the backend service that receives the request normalizes it to the current date and time.
> - If the value passed is earlier than the earliest restore point available on the source server, you receive an InternalServerError.

---

## Related content



