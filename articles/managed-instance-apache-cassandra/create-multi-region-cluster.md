---
title: Configure a Multi-region Cluster for Apache Cassandra
description: This quickstart shows how to configure a multi-region cluster with Azure Managed Instance for Apache Cassandra.
author: TheovanKraay
ms.author: thvankra
ms.service: azure-managed-instance-apache-cassandra
ms.topic: quickstart
ms.date: 11/02/2021
ms.custom: mode-other, devx-track-azurecli, kr2b-contr-experiment, sfi-ropc-blocked
ms.devlang: azurecli
---

# Quickstart: Create a multi-region cluster with Azure Managed Instance for Apache Cassandra

Azure Managed Instance for Apache Cassandra is a fully managed service for pure open-source Apache Cassandra clusters. The service also allows configurations to be overridden, depending on the specific needs of each workload, for maximum flexibility and control.

This quickstart demonstrates how to use the Azure CLI commands to configure a multi-region cluster in Azure.

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

* This article requires the Azure CLI version 2.30.0 or later. If you're using Azure Cloud Shell, the latest version is already installed.
* Use an [Azure virtual network](/azure/virtual-network/virtual-networks-overview) with connectivity to your self-hosted or on-premises environment. For more information on how to connect on-premises environments to Azure, see [Connect an on-premises network to Azure](/azure/architecture/reference-architectures/hybrid-networking/).

## Set up the network environment<a id="create-account"></a>

Because all datacenters provisioned with this service must be deployed into dedicated subnets by using virtual network injection, configure appropriate network peering in advance of deployment. For this quickstart, create a cluster with two datacenters in separate regions: East US and East US 2. First, create the virtual networks for each region.

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. Create a resource group named `cassandra-mi-multi-region`:

   ```azurecli-interactive
   az group create --location eastus2 --name cassandra-mi-multi-region
   ```

1. Create the first virtual network in East US 2 with a dedicated subnet:

   ```azurecli-interactive
   az network vnet create \
     --name vnetEastUs2 \
     --location eastus2 \
     --resource-group cassandra-mi-multi-region \
     --address-prefix 10.0.0.0/16 \
     --subnet-name dedicated-subnet
   ```

1. Create the second virtual network in East US, also with a dedicated subnet:

   ```azurecli-interactive
    az network vnet create \
      --name vnetEastUs \
      --location eastus \
      --resource-group cassandra-mi-multi-region \
      --address-prefix 192.168.0.0/16 \
      --subnet-name dedicated-subnet
   ```

   We explicitly add different IP address ranges to ensure that there are no errors with peering.

1. Peer the first virtual network to the second virtual network:

   ```azurecli-interactive
   az network vnet peering create \
     --resource-group cassandra-mi-multi-region \
     --name MyVnet1ToMyVnet2 \
     --vnet-name vnetEastUs2 \
     --remote-vnet vnetEastUs \
     --allow-vnet-access \
     --allow-forwarded-traffic
   ```

1. To connect the two virtual networks, create another peering between the second virtual network and the first:

   ```azurecli-interactive
   az network vnet peering create \
     --resource-group cassandra-mi-multi-region \
     --name MyVnet2ToMyVnet1 \
     --vnet-name vnetEastUs \
     --remote-vnet vnetEastUs2 \
     --allow-vnet-access \
     --allow-forwarded-traffic
   ```

   If you add more regions, each virtual network requires peering from it to all other virtual networks, and from all other virtual networks to it.

1. Check the output of the previous command. Make sure that the value of `peeringState` is now `Connected`. You can also check this result by running the following command:

   ```azurecli-interactive
   az network vnet peering show \
     --name MyVnet1ToMyVnet2 \
     --resource-group cassandra-mi-multi-region \
     --vnet-name vnetEastUs2 \
     --query peeringState
   ```

1. Apply some special permissions to both virtual networks. Azure Managed Instance for Apache Cassandra requires these permissions. Run the following command. Replace `<SubscriptionID>` with your subscription ID:

   ```azurecli-interactive
   az role assignment create \
     --assignee a232010e-820c-4083-83bb-3ace5fc29d0b \
     --role 4d97b98b-1d4f-4787-a291-c67834d212e7 \
     --scope /subscriptions/<SubscriptionID>/resourceGroups/cassandra-mi-multi-region/providers/Microsoft.Network/virtualNetworks/vnetEastUs2

   az role assignment create     \
     --assignee a232010e-820c-4083-83bb-3ace5fc29d0b \
     --role 4d97b98b-1d4f-4787-a291-c67834d212e7 \
     --scope /subscriptions/<SubscriptionID>/resourceGroups/cassandra-mi-multi-region/providers/Microsoft.Network/virtualNetworks/vnetEastUs
    ```

   The `assignee` and `role` values in the previous command are fixed values. Enter these values exactly as shown in the command.

If you encounter errors when you run `az role assignment create`, you might not have permissions to run it. Check with your administrator for permissions.

## Create a multi-region cluster<a id="create-account"></a>

1. Deploy the cluster resource. Replace `<Subscription ID>` with your subscription ID. The deployment can take 5 to 10 minutes.

   ```azurecli-interactive
   resourceGroupName='cassandra-mi-multi-region'
   clusterName='test-multi-region'
   location='eastus2'
   delegatedManagementSubnetId='/subscriptions/<SubscriptionID>/resourceGroups/cassandra-mi-multi-region/providers/Microsoft.Network/virtualNetworks/vnetEastUs2/subnets/dedicated-subnet'
   initialCassandraAdminPassword='myPassword'

    az managed-cassandra cluster create \
      --cluster-name $clusterName \
      --resource-group $resourceGroupName \
      --location $location \
      --delegated-management-subnet-id $delegatedManagementSubnetId \
      --initial-cassandra-admin-password $initialCassandraAdminPassword \
      --debug
   ```

1. After the cluster resource is created, you're ready to create a datacenter. First, create a datacenter in East US 2. Replace `<SubscriptionID>` with your subscription ID. This action can take up to 10 minutes.

   ```azurecli-interactive
   resourceGroupName='cassandra-mi-multi-region'
   clusterName='test-multi-region'
   dataCenterName='dc-eastus2'
   dataCenterLocation='eastus2'
   delegatedManagementSubnetId='/subscriptions/<SubscriptionID>/resourceGroups/cassandra-mi-multi-region/providers/Microsoft.Network/virtualNetworks/vnetEastUs2/subnets/dedicated-subnet'

    az managed-cassandra datacenter create \
       --resource-group $resourceGroupName \
       --cluster-name $clusterName \
       --data-center-name $dataCenterName \
       --data-center-location $dataCenterLocation \
       --delegated-subnet-id $delegatedManagementSubnetId \
       --node-count 3
   ```

1. Create a datacenter in East US. Replace `<SubscriptionID>` with your subscription ID:

   ```azurecli-interactive
   resourceGroupName='cassandra-mi-multi-region'
   clusterName='test-multi-region'
   dataCenterName='dc-eastus'
   dataCenterLocation='eastus'
   delegatedManagementSubnetId='/subscriptions/<SubscriptionID>/resourceGroups/cassandra-mi-multi-region/providers/Microsoft.Network/virtualNetworks/vnetEastUs/subnets/dedicated-subnet'
   virtualMachineSKU='Standard_D8s_v4'
   noOfDisksPerNode=4

    az managed-cassandra datacenter create \
      --resource-group $resourceGroupName \
      --cluster-name $clusterName \
      --data-center-name $dataCenterName \
      --data-center-location $dataCenterLocation \
      --delegated-subnet-id $delegatedManagementSubnetId \
      --node-count 3
      --sku $virtualMachineSKU \
      --disk-capacity $noOfDisksPerNode \
      --availability-zone false
   ```  

   You can choose the value for `--sku` from the following available product tiers:

   * Standard_E8s_v4
   * Standard_E16s_v4
   * Standard_E20s_v4
   * Standard_E32s_v4
   * Standard_DS13_v2
   * Standard_DS14_v2
   * Standard_D8s_v4
   * Standard_D16s_v4
   * Standard_D32s_v4

   Note also that `--availability-zone` is set to `false`. To enable availability zones, set it to `true`. Availability zones increase the availability service-level agreement (SLA) of the service. For more information, see [Service-level agreements for Azure Managed Instance for Apache Cassandra](https://azure.microsoft.com/support/legal/sla/managed-instance-apache-cassandra/v1_0/).

   Availability zones aren't supported in all regions. Deployments fail if you select a region where availability zones aren't supported. For supported regions, see [Azure regions with availability zones](/azure/reliability/availability-zones-region-support).

   The successful deployment of availability zones is also subject to the availability of compute resources in all the zones in the specific region. Deployments might fail if the product tier that you selected, or capacity, isn't available across all zones.

1. After the second datacenter is created, get the node status to verify that all the Cassandra nodes came up successfully:

    ```azurecli-interactive
    resourceGroupName='cassandra-mi-multi-region'
    clusterName='test-multi-region'

    az managed-cassandra cluster status\
       --cluster-name $clusterName \
       --resource-group $resourceGroupName
    ```

1. Then use CQLSH to [connect to your cluster](create-cluster-cli.md#connect-to-your-cluster). Use the following CQL query to update the replication strategy in each keyspace to include all datacenters across the cluster (system tables are updated automatically):

   ```bash
   ALTER KEYSPACE "ks" WITH REPLICATION = {'class': 'NetworkTopologyStrategy', 'dc-eastus2': 3, 'dc-eastus': 3};
   ```

1. Finally, if you add a datacenter to a cluster that already contains data, you need to run `rebuild` to replicate the historical data. In this case, assume that the `dc-eastus2` datacenter already has data. In the Azure CLI, run the following command to run `nodetool rebuild` on each node in your new `dc-eastus` datacenter. Replace `<ip address>` with the IP address of the node:

    ```azurecli-interactive
    az managed-cassandra cluster invoke-command \
      --resource-group $resourceGroupName \
      --cluster-name $clusterName \
      --host <ip address> \
      --command-name nodetool --arguments rebuild="" "dc-eastus2"=""
    ``` 

   *Don't* allow application clients to write to the new datacenter until after you apply keyspace replication changes. Otherwise, rebuild doesn't work. Then you need to create a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) so that our team can run `repair` for you.

## Troubleshooting

If you encounter an error when you apply permissions to your virtual network by using the Azure CLI, you can apply the same permission manually from the Azure portal. An example error might be "Cannot find user or service principal in graph database for `e5007d2c-4b13-4a74-9b6a-605d99f03501`."  For more information, see [Use the Azure portal to add an Azure Cosmos DB service principal](add-service-principal.md).

The Azure Cosmos DB role assignment is used for deployment purposes only. Azure Managed Instanced for Apache Cassandra has no back-end dependencies on Azure Cosmos DB.

## Clean up resources

If you aren't going to continue to use this managed instance cluster, follow these steps to delete it:

1. On the left menu of the Azure portal, select **Resource groups**.
1. From the list, select the resource group that you created for this quickstart.
1. On the resource group **Overview** pane, select **Delete resource group**.
1. On the next pane, enter the name of the resource group to delete, and then select **Delete**.

## Next step

In this quickstart, you learned how to create a multi-region cluster by using the Azure CLI and Azure Managed Instance for Apache Cassandra. You can now start working with the cluster.

> [!div class="nextstepaction"]
> [Manage Azure Managed Instance for Apache Cassandra resources by using the Azure CLI](manage-resources-cli.md)
