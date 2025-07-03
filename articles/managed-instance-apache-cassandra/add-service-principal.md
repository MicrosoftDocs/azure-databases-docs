---
title: Add Azure Cosmos DB Service Principal for Azure Managed Instance for Apache Cassandra
description: Learn how to add an Azure Cosmos DB service principal to an existing virtual network for Azure Managed Instance for Apache Cassandra.
author: TheovanKraay
ms.service: azure-managed-instance-apache-cassandra
ms.topic: how-to
ms.date: 11/02/2021
ms.author: thvankra
ms.custom: sfi-image-nochange
---

# Use the Azure portal to add Azure Cosmos DB service principal

For successful deployment into an existing virtual network, Azure Managed Instance for Apache Cassandra requires the Azure Cosmos DB service principal with a role (such as Network Contributor) that allows the action `Microsoft.Network/virtualNetworks/subnets/join/action`. In some circumstances, you might be required to add these permissions manually. This article shows you how to use the Azure portal to assign the Azure Cosmos DB service principal.

## Add Azure Cosmos DB service principal

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. Go to the target virtual network in your subscription, select the **Access control (IAM)** tab, and select **Add role assignment**.

   :::image type="content" source="./media/add-service-principal/service-principal-1.png" alt-text="Screenshot that shows Add role assignment." lightbox="./media/add-service-principal/service-principal-1.png" border="true":::

1. Search for the **Network Contributor** role, highlight it, and then select the **Members** tab.

   :::image type="content" source="./media/add-service-principal/service-principal-2.png" alt-text="Screenshot that shows Add Network Contributor." lightbox="./media/add-service-principal/service-principal-2.png" border="true":::

   > [!NOTE]
   > You don't need to have a role with permissions as expansive as Network Contributor. This example is used for simplicity. You can also create a customer role with narrower permissions, as long as it allows the action `Microsoft.Network/virtualNetworks/subnets/join/action`.

1. Ensure that **User, group, or service principal** is selected for **Assign access to**. Then click **Select members** to search for the **Azure Cosmos DB** service principal. Select it in the pane on the right.

   :::image type="content" source="./media/add-service-principal/service-principal-3.png" alt-text="Screenshot that shows selecting the Azure Cosmos DB service principal." lightbox="./media/add-service-principal/service-principal-3.png" border="true":::

1. Select the **Review + assign** tab, and then select **Review + assign**. The Azure Cosmos DB service principal is now assigned.

   :::image type="content" source="./media/add-service-principal/service-principal-4.png" alt-text="Screenshot that shows Review + assign." lightbox="./media/add-service-principal/service-principal-4.png" border="true":::

## Related content

In this article, you learned how to assign the Azure Cosmos DB service principal with an appropriate role to a virtual network, to allow managed Cassandra deployments. Learn more about Azure Managed Instance for Apache Cassandra with the following articles:

* [Overview of Azure Managed Instance for Apache Cassandra](introduction.md)
* [Manage Azure Managed Instance for Apache Cassandra resources by using the Azure CLI](manage-resources-cli.md)
