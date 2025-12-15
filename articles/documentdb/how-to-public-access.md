---
title: Enable and manage public access in Azure DocumentDB
description: Enable public access and manage public access settings for an Azure DocumentDB cluster.
author: abinav2307
ms.author: abramees
ms.topic: how-to
ms.date: 01/06/2025
#Customer Intent: As a database adminstrator, I want to configure public access, so that I can connect to Azure DocumentDB cluster using public IP address.
---

# Manage public access on your Azure DocumentDB cluster

You can use cluster-level firewall rules to manage public access to an Azure DocumentDB cluster. Public access can be enabled from a specific IP address or a range of IP addresses on the public Internet.  

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

## Enable public access *during cluster creation* in the Azure portal

> [!NOTE]
> If no firewall rules are added to your Azure DocumentDB cluster, public network access to the cluster is disabled. If you don't add any firewall rules or [private endpoints](./how-to-private-link.md) during cluster creation, your cluster is created in a locked-down state. To enable access to a locked-down cluster, you must add firewall rules for public access or create private endpoints for private access after the cluster is created.

To enable public access during cluster creation:

1. [Start cluster creation and complete the **Basics** tab for a new Azure DocumentDB cluster](./quickstart-portal.md#create-a-cluster).
1. On the **Networking** tab, select **Public access (allowed IP addresses)** in the **Connectivity method** section to open the firewall rules creation controls. 
1. To add firewall rules, in the **Firewall rules** section, type in the firewall rule name, start IP v4 address, and end IP v4 address.
    - To allow a single IP address, enter the same address in both the **Start IP address** and **End IP address** fields.

    :::image type="content" source="media/how-to-public-access/add-firewall-rule-during-cluster-creation.png" alt-text="Screenshot of the firewall rule addition during a new Azure DocumentDB cluster creation.":::

1. To quickly add your current public IP address (the address of the machine or device from which you’re accessing the Azure portal), select **Add current client IP address**.
    
    > [!TIP]
    > Verify your IP address before saving the configuration. In some cases, the IP address detected by the Azure portal may differ from the IP address used when accessing the Internet. To check your actual IP address, use a search engine to find tools like *what is my IP*.

1. To allow cluster access from any IP address on the Internet, select **Add 0.0.0.0 - 255.255.255.255**. Even with this rule in place, users must authenticate with the correct username and password to access the cluster. However, it’s recommended to allow global access only temporarily and for non-production databases.

## Manage existing cluster-level firewall rules through the Azure portal

You can modify firewall rules for an existing cluster through the Azure portal.

To **add** a firewall rule:

1. On the Azure DocumentDB cluster page, under **Settings**, select **Networking**.
1. In the **Public access**, in the **Firewall rules** section, type in the firewall rule name, start IP v4 address, and end IP v4 address. 
    - To allow a single IP address, enter the same address in both the **Start IP address** and **End IP address** fields.

    :::image type="content" source="media/how-to-public-access/firewall-rule-settings-management.png" alt-text="Screenshot of the firewall rule settings management on an Azure DocumentDB cluster." lightbox="media/how-to-public-access/firewall-rule-settings-management-extended.png":::

1. To quickly add your current public IP address (the address of the machine or device from which you’re accessing the Azure portal), select **Add current client IP address**.
    
    > [!TIP]
    > Verify your IP address before saving the configuration. In some cases, the IP address detected by the Azure portal may differ from the IP address used when accessing the Internet. To check your actual IP address, use a search engine to find tools like *what is my IP*.
    
1. To allow cluster access from any IP address on the Internet, select **Add 0.0.0.0 - 255.255.255.255**. Even with this rule in place, users must authenticate with the correct username and password to access the cluster. However, it’s recommended to allow global access only temporarily and for non-production databases.
1. Select **Save** on the toolbar to save the changes in cluster-level firewall rules. Wait for the confirmation that the update was successful.

To **remove** a firewall rule on your cluster, follow these steps:
1. On the Azure DocumentDB cluster page, under **Settings**, select **Networking**.
1. In the **Public access**, in the **Firewall rules** section, locate the firewall rule to delete. 
1. Select delete icon next to the firewall rule.
1. Select **Save** on the toolbar to save the changes in cluster-level firewall rules. Wait for the confirmation that the update was successful.

## Connect from Azure
There's an easy way to grant cluster access to applications hosted on Azure, such as an Azure Web Apps application or those applications running in an Azure VM. 

1. On the portal page for your cluster, under **Networking**, in the **Public access**, select the **Allow Azure services and resources to access this cluster** checkbox.
1. Select **Save** on the toolbar to save the changes. Wait for the confirmation that the update was successful.

> [!IMPORTANT] 
> Enabling this option allows connections from any Azure service, including from services and hosts in other customer subscriptions. Ensure your login credentials and user permissions restrict access to authorized users only.

## Disable public access
To disable public access on a cluster:
1. On the portal page for your cluster, under **Networking**, in the **Public access**, remove all firewall rules.
1. Clear the **Allow Azure services and resources to access this cluster** checkbox.
1. Select **Save** on the toolbar to save the changes. Wait for the confirmation that the update was successful.

## Related content
- [Learn more about database security in Azure DocumentDB](./security.md)
- [See guidance on how to enable private access](./how-to-private-link.md)
- [Migrate to Azure DocumentDB](./migration-options.md)
