---
title: Deploy a Managed Apache Spark Cluster with Azure Databricks
description: This quickstart shows how to deploy a Managed Apache Spark cluster with Azure Databricks by using the Azure portal.
author: TheovanKraay
ms.author: thvankra
ms.service: azure-managed-instance-apache-cassandra
ms.topic: quickstart
ms.date: 11/02/2021
ms.custom:
- mode-other
- kr2b-contr-experiment
- sfi-image-nochange
---

# Quickstart: Deploy an Azure Managed Apache Spark cluster with Azure Databricks

Azure Managed Instance for Apache Cassandra provides automated deployment and scaling operations for managed open-source Apache Cassandra datacenters. This feature accelerates hybrid scenarios and helps to reduce ongoing maintenance.

This quickstart demonstrates how to use the Azure portal to create a fully managed Apache Spark cluster inside the Azure virtual network of your Azure Managed Instance for Apache Cassandra cluster. You create the Spark cluster in Azure Databricks. Later, you can create or attach notebooks to the cluster, read data from different data sources, and analyze insights.

You can also learn more with detailed instructions on [Deploy Azure Databricks in your Azure virtual network (virtual network injection)](/azure/databricks/administration-guide/cloud-configurations/azure/vnet-inject).

## Prerequisites

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Create an Azure Databricks cluster

Follow these steps to create an Azure Databricks cluster in a virtual network that has the Azure Managed Instance for Apache Cassandra:

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. On the left pane, locate **Resource groups**. Go to your resource group that contains the virtual network where your managed instance is deployed.

1. Open the **Virtual network** resource, and make a note of the **Address space**.

   :::image type="content" source="./media/deploy-cluster-databricks/virtual-network-address-space.png" alt-text="Screenshot that shows where to get the address space of your virtual network." border="true":::

1. From the resource group, select **Add** and search for **Azure Databricks** in the search field.

   :::image type="content" source="./media/deploy-cluster-databricks/databricks.png" alt-text="Screenshot that shows a search for Azure Databricks." border="true":::

1. Select **Create** to create an Azure Databricks account.

   :::image type="content" source="./media/deploy-cluster-databricks/databricks-create.png" alt-text="Screenshot that shows Azure Databricks offering with Create selected." border="true":::

1. Enter the following values:

   * **Workspace name**: Provide a name for your Azure Databricks workspace.
   * **Region**: Make sure to select the same region as your virtual network.
   * **Pricing Tier**: Select **Standard**, **Premium**, or **Trial**. For more information on these tiers, see the [Azure Databricks pricing page](https://azure.microsoft.com/pricing/details/databricks/).

   :::image type="content" source="./media/deploy-cluster-databricks/select-name.png" alt-text="Screenshot that shows a dialog box where you can enter the workspace name, region, and pricing tier for the Azure Databricks account." border="true":::

1. Select the **Networking** tab, and enter the following details:

   * **Deploy Azure Databricks workspace in your Virtual Network (VNet)**: Select **Yes**.
   * **Virtual Network**: From the dropdown list, choose the virtual network where your managed instance exists.
   * **Public Subnet Name**: Enter a name for the public subnet.
   * **Public Subnet CIDR Range**: Enter an IP range for the public subnet.
   * **Private Subnet Name**: Enter a name for the private subnet.
   * **Private Subnet CIDR Range**: Enter an IP range for the private subnet.

   To avoid range collisions, ensure that you select higher ranges. If necessary, use a [visual subnet calculator](https://www.fryguy.net/wp-content/tools/subnets.html) to divide the ranges.

   :::image type="content" source="./media/deploy-cluster-databricks/subnet-calculator.png" alt-text="Screenshot that shows the Visual Subnet Calculator with two highlighted identical network addresses." border="true":::

   The following screenshot shows example details on the networking pane.

   :::image type="content" source="./media/deploy-cluster-databricks/subnets.png" alt-text="Screenshot that shows specified public and private subnet names." border="true":::

1. Select **Review + create**, and then select **Create** to deploy the workspace.

1. Open the workspace after the workspace is created.

1. You're redirected to the Azure Databricks portal. From the portal, select **New Cluster**.

1. On the **New cluster** pane, accept default values for all fields other than the following fields:

   * **Cluster Name**: Enter a name for the cluster.
   * **Databricks Runtime Version**: We recommend that you select Azure Databricks runtime version 7.5 or later, for Spark 3.x support.

   :::image type="content" source="~/reusable-content/ce-skilling/azure/media/cosmos-db/databricks-runtime.png" alt-text="Screenshot that shows the New Cluster dialog box with an Azure Databricks runtime version selected." border="true":::

1. Expand **Advanced Options**, and add the following configuration. Make sure to replace the node IPs and credentials.

   ```java
   spark.cassandra.connection.host <node1 IP>,<node 2 IP>, <node IP>
   spark.cassandra.auth.password cassandra
   spark.cassandra.connection.port 9042
   spark.cassandra.auth.username cassandra
   spark.cassandra.connection.ssl.enabled true
   ```

1. Add the Apache Spark Cassandra Connector library to your cluster to connect to both native and Azure Cosmos DB Cassandra endpoints. In your cluster, select **Libraries** > **Install New** > **Maven**, and then add `com.datastax.spark:spark-cassandra-connector-assembly_2.12:3.0.0` in the Maven **Coordinates** field.

   :::image type="content" source="~/reusable-content/ce-skilling/azure/media/cosmos-db/databricks-search-packages.png" alt-text="Screenshot that shows searching for Maven packages in Azure Databricks.":::

1. Select **Install**.

## Clean up resources

If you aren't going to continue to use this managed instance cluster, follow these steps to delete it:

1. On the left menu of the Azure portal, select **Resource groups**.
1. From the list, select the resource group that you created for this quickstart.
1. On the resource group **Overview** pane, select **Delete resource group**.
1. On the next pane, enter the name of the resource group to delete, and then select **Delete**.

## Next step

In this quickstart, you learned how to create a fully managed Apache Spark cluster inside the virtual network of your Azure Managed Instance for Apache Cassandra cluster. Next, learn how to manage the cluster and datacenter resources.

> [!div class="nextstepaction"]
> [Manage Azure Managed Instance for Apache Cassandra resources by using the Azure CLI](manage-resources-cli.md)
