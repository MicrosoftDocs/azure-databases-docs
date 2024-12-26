---
title: Manage firewall rules - Azure portal
description: Create and manage firewall rules for Azure Database for PostgreSQL - Flexible Server using the Azure portal
author: GennadNY
ms.author: guybo
ms.reviewer: maghan
ms.date: 04/28/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - ignite-2023
---

# Create and manage firewall rules for Azure Database for PostgreSQL - Flexible Server using the Azure portal

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL flexible server supports two types of mutually exclusive network connectivity methods to connect to your flexible server. The two options are:

* Public access (allowed IP addresses). That method can be further secured by using [Private Link](concepts-networking-private-link.md) based networking with AAzure Database for PostgreSQL flexible server in Preview. 
* Private access (VNet Integration)

This article focuses on creation of an Azure Database for PostgreSQL flexible server instance with **Public access (allowed IP addresses)** using Azure portal and provides an overview of managing firewall rules after creation of the Azure Database for PostgreSQL flexible server instance. With *Public access (allowed IP addresses)*, the connections to the Azure Database for PostgreSQL flexible server instance are restricted to allowed IP addresses only. The client IP addresses need to be allowed in firewall rules. To learn more about it, refer to [Public access (allowed IP addresses)](concepts-networking.md#public-access-allowed-ip-addresses). The firewall rules can be defined at the time of server creation (recommended) but can be added later as well. In this article, we'll provide an overview on how to create and manage firewall rules using public access (allowed IP addresses).

## Create a firewall rule when creating a server

1. Select **Create a resource** (+) in the upper-left corner of the  portal.
2. Select **Databases** > **Azure Database for PostgreSQL**. You can also enter **PostgreSQL** in the search box to find the service.
<!--Note this no longer appears in portal creation. 3. Select **Flexible Server** as the deployment option.-->
4. Fill out the **Basics** form.
5. Go to the **Networking** tab to configure how you want to connect to your server.
6. In the **Connectivity method**, select *Public access (allowed IP addresses)*. To create the **Firewall rules**, specify the Firewall rule name and single IP address, or a range of addresses. If you want to limit the rule to a single IP address, type the same address in the field for Start IP address and End IP address. Opening the firewall enables administrators, users, and applications to access any database on the Azure Database for PostgreSQL flexible server instance to which they have valid credentials.
   > [!Note]
   > Azure Database for PostgreSQL flexible server instance creates a firewall at the server level. It prevents external applications and tools from connecting to the server and any databases on the server, unless you create a rule to open the firewall for specific IP addresses.
7. Select **Review + create** to review your Azure Database for PostgreSQL flexible server configuration.
8.  Select **Create** to provision the server. Provisioning can take a few minutes.

## Create a firewall rule after server is created

1. In the [Azure portal](https://portal.azure.com/), select the Azure Database for PostgreSQL flexible server instance on which you want to add firewall rules.
2. On the Flexible Server page, under **Settings** heading, click **Networking** to open the Networking page.

   <!--![Azure portal - click Connection Security](media/howto-manage-firewall-portal/1-connection-security.png)-->

3. Select **Add current client IP address** in the firewall rules. This automatically creates a firewall rule with the public IP address of your computer, as perceived by the Azure system.

   <!--![Azure portal - click Add My IP](media/howto-manage-firewall-portal/2-add-my-ip.png)-->

4. Verify your IP address before saving the configuration. In some situations, the IP address observed by Azure portal differs from the IP address used when accessing the internet and Azure servers. Therefore, you may need to change the Start IP address and End IP address to make the rule function as expected.

   You can use a search engine or other online tool to check your own IP address. For example, search for "what is my IP."

   <!--![Bing search for What is my IP](media/howto-manage-firewall-portal/3-what-is-my-ip.png)-->

5. Add more address ranges. In the firewall rules for the Azure Database for PostgreSQL flexible server instance, you can specify a single IP address, or a range of addresses. If you want to limit the rule to a single IP address, type the same address in the field for Start IP address and End IP address. Opening the firewall enables administrators, users, and applications to access any database on the Azure Database for PostgreSQL flexible server instance to which they have valid credentials.

   <!--![Azure portal - firewall rules](media/howto-manage-firewall-portal/4-specify-addresses.png)-->

6. Select **Save** on the toolbar to save this firewall rule. Wait for the confirmation that the update to the firewall rules was successful.

   <!--![Azure portal - click Save](media/howto-manage-firewall-portal/5-save-firewall-rule.png)-->

## Connecting from Azure

You may want to enable resources or applications deployed in Azure to connect to your Azure Database for PostgreSQL flexible server instance. This includes web applications hosted in Azure App Service, running on an Azure VM, an Azure Data Factory data management gateway and many more. 

When an application within Azure attempts to connect to your server, the firewall verifies that Azure connections are allowed. You can enable this setting by selecting the **Allow public access from Azure services and resources within Azure to this server** option in the portal from the **Networking** tab and hit **Save**.

The resources don't need to be in the same virtual network (VNet) or resource group for the firewall rule to enable those connections. If the connection attempt isn't allowed, the request doesn't reach the Azure Database for PostgreSQL flexible server instance.

> [!IMPORTANT]
> This option configures the firewall to allow all connections from Azure including connections from the subscriptions of other customers. When selecting this option, make sure your login and user permissions limit access to only authorized users.
>
> We recommend choosing the **Private access (VNet Integration)** to securely access Azure Database for PostgreSQL flexible server.
>
## Manage existing firewall rules through the Azure portal

Repeat the following steps to manage the firewall rules.

- To add the current computer, select + **Add current client IP address** in the firewall rules. Click **Save** to save the changes.
- To add additional IP addresses, type in the Rule Name, Start IP Address, and End IP Address. Click **Save** to save the changes.
- To modify an existing rule, click any of the fields in the rule and modify. Click **Save** to save the changes.
- To delete an existing rule, click the ellipsis […] and click **Delete** to remove the rule. Click **Save** to save the changes.

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Next steps

- Learn more about [Networking in Azure Database for PostgreSQL - Flexible Server](concepts-networking.md)
- Understand more about [Azure Database for PostgreSQL - Flexible Server firewall rules](concepts-networking.md#public-access-allowed-ip-addresses)
- [Create and manage Azure Database for PostgreSQL - Flexible Server firewall rules using Azure CLI](how-to-manage-firewall-cli.md).
