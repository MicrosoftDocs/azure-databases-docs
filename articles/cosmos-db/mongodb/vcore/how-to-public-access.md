---
title: Enable and manage public access in Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Enable pubic access and manage public access settings for an Azure Cosmos DB for MongoDB vCore cluster.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 01/02/2025
#Customer Intent: As a database adminstrator, I want to configure public access, so that I can connect to Azure Cosmos DB for MongoDB vCore cluster using public IP address.
---

# Manage public access on your Azure Cosmos DB for MongoDB vCore cluster

[!INCLUDE[MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

Cluster-level firewall rules can be used to manage public access to an Azure Cosmos DB for MongoDB vCore cluster. Public access can be enabled from a specified IP address or a range of IP addresses in the public Internet.

## Prerequisites

- An existing Azure Cosmos DB for MongoDB vCore cluster.
  - If you don't have an Azure subscription, [create an account for free](https://azure.microsoft.com/free).
  - If you have an existing Azure subscription, [create a new Azure Cosmos DB for MongoDB vCore cluster](quickstart-portal.md).

## Enable public access *during cluster creation* in the Azure portal

> [!NOTE] 
> If you don't add any firewall rules on your Azure Cosmos DB for MongoDB vCore cluster, public networking access to your cluster is going to be disabled. If you don't add any firewall rules or private endpoints during cluster creation, your cluster is going to be created locked-down. To enable access to a locked-down cluster, you need to enable public access by adding firewall rules or enable private access by adding private endpoints after cluster creation is completed.

To enable public access when your cluster is created, follow these steps:

1. Follow the steps to [start cluster creation and complete the **Basics** tab for a new Azure Cosmos DB for MongoDB vCore cluster](./quickstart-portal.md#create-a-cluster).
1. On the **Networking** tab, select **Public access (allowed IP addresses)** in the **Connectivity method** section to open firewall rules creation controls. 
1. To add firewall rules, in the **Firewall rules** section, type in the firewall rule name, start IP v4 address, and end IP v4 address. You can specify a single IP address or a range of addresses. If you want to limit the rule to a single IP address, type the same address in the **Start IP address** and **End IP address** fields.

    :::image type="content" source="media/how-to-public-access/add-firewall-rule-during-cluster-creation.png" alt-text="Screenshot of the firewall rule addition during a new Azure Cosmos DB for MongoDB vCore cluster creation.":::

1. To add current client public IP address of the machine or device where Azure portal is opened, select **Add current client IP address** to create a firewall rule with the public IP address of your computer, as perceived by the Azure system.

Verify your IP address before saving this configuration. In some situations, the IP address observed by Azure portal differs from the IP address used when accessing the Internet and Azure services. Thus, you may need to change the start IP and end IP to make the rule function as expected. Use a search engine or other online tool to check your own IP address. For example, search for *what is my IP*.

1. To enable access your cluster for the whole Internet, you can also select **Add 0.0.0.0 - 255.255.255.255**. In this situation, clients still must log in with the correct username and password to use the cluster. Nevertheless, it's best to allow worldwide access for only short periods of time and for only non-production databases.

## Manage existing cluster-level firewall rules through the Azure portal

To **add** a firewall rule your cluster, follow these steps:

1. On the Azure Cosmos DB for MongoDB vCore cluster page, under **Settings**, select **Networking**.
1. In the **Public access**, in the **Firewall rules** section, type in the firewall rule name, start IP v4 address, and end IP v4 address. You can specify a single IP address or a range of addresses. If you want to limit the rule to a single IP address, type the same address in the **Start IP address** and **End IP address** fields.
1. To add current client public IP address of the machine or device where Azure portal is opened, select **Add current client IP address** to create a firewall rule with the public IP address of your computer, as perceived by the Azure system.

Verify your IP address before saving this configuration. In some situations, the IP address observed by Azure portal differs from the IP address used when accessing the Internet and Azure services. Thus, you may need to change the start IP and end IP to make the rule function as expected. Use a search engine or other online tool to check your own IP address. For example, search for *what is my IP*.

1. To enable access for your cluster to the whole Internet, you can also select **Add 0.0.0.0 - 255.255.255.255**. In this situation, clients still must log in with the correct username and password to use the cluster. Nevertheless, it's best to allow worldwide access for only short periods of time and for only non-production databases.
1. Select **Save** on the toolbar to save the changes in cluster-level firewall rules. Wait for the confirmation that the update was successful.

To **remove** a firewall rule on your cluster, follow these steps:
1. On the Azure Cosmos DB for MongoDB vCore cluster page, under **Settings**, select **Networking**.
1. In the **Public access**, in the **Firewall rules** section, locate the firewall rule to delete. 
1. Select delete icon next to the firewall rule.
1. Select **Save** on the toolbar to save the changes in cluster-level firewall rules. Wait for the confirmation that the update was successful.

## Connect from Azure
There's an easy way to grant cluster access to applications hosted on Azure, such as an Azure Web Apps application or those applications running in an Azure VM. 

1. On the portal page for your cluster, under **Networking**, in the **Public access**, select the checkbox **Allow Azure services and resources to access this cluster**
1. Select **Save** on the toolbar to save the changes. Wait for the confirmation that the update was successful.

> [!IMPORTANT] 
> This option configures the firewall to allow all connections from Azure, including connections from the subscriptions of other customers. When selecting this option, make sure your login and user permissions limit access to only authorized users.

## Related content

- [Learn more about database security in Azure Cosmos DB for MongoDB vCore](./security.md)
- [See guidance on how to enable private access](./how-to-private-link.md)
- [Migrate to Azure Cosmos DB for MongoDB vCore](./migration-options.md)
