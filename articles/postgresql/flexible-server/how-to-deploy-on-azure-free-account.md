---
title: Use an Azure free account to try for free
description: Guidance on how to deploy an Azure Database for PostgreSQL flexible server instance for free using an Azure Free Account.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 09/10/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - template-how-to
---

# Use an Azure free account to try Azure Database for PostgreSQL flexible server for free

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL flexible server is a managed service that you use to run, manage, and scale highly available PostgreSQL databases in the cloud. With an Azure free account, you can use Azure Database for PostgreSQL flexible server for **free for 12 months** with **monthly limits** of up to:
- **750 hours** of **Burstable B1MS** instance, enough hours to run a database instance continuously each month.
- **32 GB storage and 32 GB backup storage**.

This article shows you how to create and use an Azure Database for PostgreSQL flexible server instance for free using an [Azure free account](https://azure.microsoft.com/free/).

## Prerequisites

To complete this tutorial, you need:

- An Azure free account. If you don't have one, [create a free account](https://azure.microsoft.com/free/) before you begin.

## Create an Azure Database for PostgreSQL flexible server instance

1. Sign in to the [Azure portal](https://portal.azure.com/) with your Azure free account.

    The default view is your service dashboard.

1. To create an Azure Database for PostgreSQL flexible server instance, search for and select **Azure Database for PostgreSQL servers**:

    :::image type="content" source="media/how-to-deploy-on-azure-free-account/select-postgresql.png" alt-text="Screenshot that shows how to search and select Azure Database for PostgreSQL flexible server.":::

    Alternatively, you can search for and navigate to **Free Services**, and then select **Azure Database for PostgreSQL** tile from the list:

1. Select **Create**.

1. Enter the basic settings for a new **Azure Database for PostgreSQL flexible server** instance.

    :::image type="content" source="media/how-to-deploy-on-azure-free-account/basic-settings-postgresql.png" alt-text="Screenshot that shows the Basic Settings for creating an Azure Database for PostgreSQL flexible server instance." lightbox="media/how-to-deploy-on-azure-free-account/basic-settings-postgresql.png":::

    | Setting | Suggested Value | Description |
    | --- | --- | --- |
    | Subscription | Your subscription name | Select the Free Trial Azure subscription. |
    | Resource group | Your resource group | Enter a new resource group or an existing one from your subscription. |
    | Server name | mydemoserver-pgsql | Specify a unique name to identify your Flexible Server. The domain name *postgres.database.azure.com* is appended to the server name you provide. The server name can contain only lowercase letters, numbers, and the hyphen (-) character. It must contain between 3 and 63 characters. |
    | Region | The region closest to your users | Select a location from the list, preferably the location that's closest to your users. |
    | PostgreSQL version | The latest major version | Use the latest PostgreSQL major version unless you have specific requirements otherwise. |
    | Workload type | Development | For a free trial, select **Development** workload. For a production workload, choose Small/Medium-size or Large-size depending on your requirements. |
    | Compute + storage | Default | Select the SKU of the compute and storage that better accommodates your performance and cost needs. |
    | Availability zone | No preference | If your application (hosted on Azure VMs, virtual machine scale sets or AKS instance) is provisioned in a specific availability zone, create your flexible server in the same availability zone. Collocating the application and database improves performance by reducing network latency across zones. If you choose **No preference**, a default AZ is selected for you. |
    | High availability | Default | Leave the High Availability option unchecked. |
    | Authentication method | PostgreSQL authentication only | Select the authentication method that suits your authentication needs for this instance of PostgreSQL. |
    | Admin username | myadmin | Create a sign-in account to use when you connect to the server. The admin username must contain between 1 and 63 characters, must only contain numbers and letters, can't start with **pg_** and can't be **azure_superuser**, **azure_pg_admin**, **admin**, **administrator**, **root**, **guest**, or **public**. |
    | Password | Your password | Specify a password for the server admin account. The password must contain between 8 and 128 characters. It must also contain characters from three of the following four categories: English uppercase letters, English lowercase letters, numbers (0 through 9), and non-alphanumeric characters (!, $, #, %, and so on). Your password cannot contain all or part of the login name. Part of a login name is defined as three or more consecutive alphanumeric characters. |

1. For **Compute + storage** setting, keep the default values populated upon selecting **Development** workload type.

    :::image type="content" source="media/how-to-deploy-on-azure-free-account/compute-storage-default-postgresql.png" alt-text="Screenshot that shows the default values for compute + storage settings.":::

    Select **Configure Server** to review and customize the **Compute + storage** setting.

    Make sure to select Burstable B1MS Instance (1-2 vCores), specify to include storage of less than or equal to 32 GB, and keep the default settings for the remaining options.

    :::image type="content" source="media/how-to-deploy-on-azure-free-account/compute-storage-postgresql.png" alt-text="Screenshot that shows the Compute + Storage Configure Server blade, to choose B1MS SKU and 32GB Storage." lightbox="media/how-to-deploy-on-azure-free-account/compute-storage-postgresql.png":::

    Select **Save** to continue with the configuration.

1. Select **Networking** tab to configure how to reach your server.

    Azure Database for PostgreSQL flexible server provides two ways to connect:
    - Public access (allowed IP addresses) and Private endpoint
    - Private access (VNet Integration)

    With public access, access to your server is limited to allowed IP addresses that you include in a firewall rule or to applications which can reach the instance of Azure Database for PostgreSQL flexible server via private endpoints. This method prevents external applications and tools from connecting to the server and any databases on the server, unless you create a rule to open the firewall for a specific IP address or range, or create a private endpoint.

    With private access, access to your server is limited to your virtual network. For more information about connectivity methods, [**see Networking overview**](concepts-networking-private.md).

    For the purposes of this tutorial, enable public access to connect to the server.

    > [!NOTE]  
    > Azure Database for PostgreSQL flexible server support for Private Endpoints in Preview requires enablement of **Enable Private Endpoints for PostgreSQL flexible servers** [preview feature in your subscription](/azure/azure-resource-manager/management/preview-features).
    > Only **after preview feature is enabled** you can create servers which are PE capable, i.e. can be networked using Private Link.

1. On the **Networking** tab, for **Connectivity method** select **Public access (allowed IP addresses) and Private endpoint**.

1. Leave **Allow public access to this resource through the internet using a public IP address** enabled in this case, since you want the instance to be accessible from the public IP address with which your workstation navigates on the Internet. By disabling this check box, the only incoming traffic which would be permitted would be the one coming through private endpoints.

1. For configuring **Firewall rules**, select **Add current client IP address**.

    :::image type="content" source="media/how-to-deploy-on-azure-free-account/networking-postgresql.png" alt-text="Screenshot that shows the networking options to be chosen, and highlights the add current client IP address button.":::

1. To review your Azure Database for PostgreSQL flexible server configuration, select **Review + create**.

    :::image type="content" source="media/how-to-deploy-on-azure-free-account/review-create-postgresql.png" alt-text="Screenshot that shows the Review + create blade." lightbox="media/how-to-deploy-on-azure-free-account/review-create-postgresql.png":::

    > [!IMPORTANT]  
    > When creating the Azure Database for PostgreSQL flexible server instance using your Azure free account, you will see an **Estimated cost per month** in the **Compute + Storage: Cost Summary** blade and the **Review + Create** tab. However, as long as you stay within the monthly limits of your Azure free account (refer to the [**Monitor and track free services usage**](#monitor-and-track-free-services-usage) section below for usage information). There is no charge for the service. We are currently working to improve the **Cost Summary** experience for free services.

1. Select **Create** to provision the server.

    Provisioning can take a few minutes.

1. On the toolbar, select **Notifications** (the bell icon) to monitor the deployment process.

    After the deployment is complete, select **Pin to dashboard**, to create a tile for the Azure Database for PostgreSQL flexible server instance on your Azure portal dashboard. This tile is a shortcut to the server's **Overview** page. When you select **Go to resource**, the server's **Overview** page opens.

    By default, a **postgres** database is created under your server. The postgres database is a default database that's meant for use by users, utilities, and third-party applications. (The other default database is **azure_maintenance**. Its function is to separate the managed service processes from user actions. You can't access this database.)

## Connect and query

Now that you've created an Azure Database for PostgreSQL flexible server instance in a resource group, you can connect to server and query databases by using the following Connect and query quickstarts:
- [psql](quickstart-create-server.md#connect-using-psql).
- [Azure CLI](connect-azure-cli.md).
- [Python](connect-python.md).
- [Java](connect-java.md).
- [.NET](connect-csharp.md).
- [Connect to a server in VNET](quickstart-create-connect-server-vnet.md).

## Monitor and track free services usage

You're not charged for Azure Database for PostgreSQL flexible server services that are included for free with your Azure free account unless you exceed the free service limits. To remain within the limits, use the Azure portal to track and monitor your free services usage.

1. In the Azure portal, search for **Subscriptions** and select the Azure free account - **Free Trial** subscription.
1. On the **Overview** page, scroll down to show the tile **Top free services by usage**, and then select **View all free services**.

    :::image type="content" source="media/how-to-deploy-on-azure-free-account/free-services-usage-overview.png" alt-text="Screenshot that shows the Free Trial subscription overview page and highlights View all free services." lightbox="media/how-to-deploy-on-azure-free-account/free-services-usage-overview.png":::

1. Locate the below meters related to **Azure Database for PostgreSQL – Flexible Server** to track usage:

    | Meter | Description | Monthly Limit |
    | --- | --- | --- |
    | Azure Database for PostgreSQL, Flexible Server Burstable BS Series Compute, B1MS | Tracks Compute usage in terms of number of hours of running | 750 Hours per month - Burstable B1MS Compute Tier |
    | Azure Database for PostgreSQL, Flexible Server Storage, Data Stored | Tracks Data Storage Provisioned in terms of GB used per month | 32 GB per month |

    :::image type="content" source="media/how-to-deploy-on-azure-free-account/free-services-tracking.png" alt-text="Screenshot that shows the View and track usage information blade on Azure portal for all free services." lightbox="media/how-to-deploy-on-azure-free-account/free-services-tracking.png":::

    - Meter: Identifies the unit of measure for the service being consumed.
    - Usage/Limit: Current month's usage and limit for the meter.
    - Status: Usage status of the service. Based on your usage, you can have one of the following statutes:
    - Not in use: You haven't used the meter or the usage for the meter hasn't reached the billing system.
    - Exceeded on \<Date\>: You've exceeded the limit for the meter on \<Date\>.
    - Unlikely to Exceed: You're unlikely to exceed the limit for the meter.
    - Exceeds on \<Date\>: You're likely to exceed the limit for the meter on \<Date\>.

    > [!IMPORTANT]  
    > With an Azure free account, you also get $200 in credit to use in 30 days. During this time, any usage beyond the free monthly amounts of services will be deducted from this credit.
    > At the end of your first 30 days or after you spend your $200 credit (whichever comes first), you'll only pay for what you use beyond the free monthly amounts of services. To keep getting free services after 30 days, move to pay-as-you-go pricing. If you don't move to pay as you go, you can't purchase Azure services beyond your $200 credit—and eventually your account and services will be disabled.
    > For more information, see [**Azure free account FAQ**](https://azure.microsoft.com/free/free-account-faq/).

## Clean up resources

If you're using the Azure Database for PostgreSQL flexible server instance for development, testing, or predictable, time-bound production workloads, optimize usage by starting and stopping the server on-demand. After you stop the server, it remains in that state for seven days unless restarted sooner. For more information, see Start/Stop Server to lower TCO. When your Azure Database for PostgreSQL flexible server instance is stopped, there's no Compute usage, but Storage usage is still considered.

Alternatively, if you don't expect to need these resources in the future, you can delete them by deleting the resource group, or you can just delete the Azure Database for PostgreSQL flexible server instance.

- To delete the resource group, complete the following steps:
    1. In the Azure portal, search for and select **Resource groups**.
    1. In the list of resource groups, select the name of your resource group.
    1. On the **Overview** page for your resource group, select **Delete resource group.**
    1. In the confirmation dialog box, type the name of your resource group, and then select **Delete**.

- To delete the Azure Database for PostgreSQL flexible server instance, on the **Overview** page for the server, select **Delete**.

## Related content

- [Deploy a Django app with App Service and PostgreSQL](/azure/app-service/tutorial-python-postgresql-app).
