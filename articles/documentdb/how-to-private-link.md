---
title: Use Azure Private Link with Azure DocumentDB
description: Use Azure Private Link to connect to Azure DocumentDB over a private endpoint in a virtual network.
author: khelanmodi
ms.author: khelanmodi
ms.custom:
  - ignite-2023
  - devx-track-azurecli
ms.topic: how-to
ms.date: 05/28/2025
# CustomerIntent: As a security administrator, I want to use Azure Private Link so that I can ensure that database connections occur over privately-managed virtual network endpoints.
---

# Enable private access in Azure DocumentDB

Azure Private Link is a powerful service that allows users to connect to Azure DocumentDB through a designated private endpoint. This private endpoint consists of private IP addresses located in a subnet within your own virtual network. The endpoint enables you to restrict access to the Azure DocumentDB product solely over private IPs. The risk of data exfiltration is substantially reduced, by integrating Private Link with stringent NSG policies. For a deeper understanding of private endpoints, consider checking out [What is Azure Private Link?](/azure/private-link/private-endpoint-overview).

> [!NOTE]
> Private Link secures your connection, however, it doesn't prevent your Azure DocumentDB endpoints from being resolved by public DNS. The filtration of incoming requests is handled at the application level, not at the transport or network level.

Private Link offers the flexibility to access the Azure DocumentDB either from within your virtual network or from any connected peered virtual network. Additionally, resources linked to Private Link are accessible on-premises via private peering, through VPN or Azure ExpressRoute.

To establish a connection, Azure DocumentDB with Private Link supports both automatic and manual approval methods.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

## Create a cluster with a private endpoint by using the Azure portal

Follow these steps to create a new Azure DocumentDB cluster with a private endpoint by using the Azure portal:

1. Sign in to the [Azure portal](https://portal.azure.com), then select **Create a resource** in the upper left-hand corner of the Azure portal. 

1. On the **Create a resource** page, select **Databases** and then select **Azure DocumentDB**.

1. On the Select API option page, on the **MongoDB** tile, select Create.

1. Choose the **cluster** resource type.

1. On the **Create an Azure DocumentDB** cluster page, select or create a **Resource group**, enter a **Cluster name** and Location, and enter and confirm the administrator Password.

1. Select Next: **Networking**.

1. Select **Networking** tab, for Connectivity method, select **Private access**.

1. On the Create private endpoint screen, enter or select appropriate values for:

    | Setting | Value |
    | ------- | ----- |
    | Resource group | Select a resource group.|
    | Name | Enter any name for your private endpoint. If this name is taken, create a unique one. |
    | Network Interface name | Enter any name for your Network Interface. If this name is taken, create a unique one. |
    | Location | Select the region where you want to deploy Private Link. Create the private endpoint in the same location where your virtual network exists.|
    | Resource type | Select `Microsoft.DocumentDB/mongoClusters`. |
    | Target resource | Select the Azure DocumentDB resource you created. |
    | Target subresource | Select the type of subresource for the resource selected previously that your private endpoint should have the ability to access. |
    | Virtual network | Select your virtual network. |
    | Subnet | Select your subnet. |
    | Integrate with private DNS zone | Select **Yes**. To connect privately with your private endpoint, you need a DNS record. We recommend that you integrate your private endpoint with a private DNS zone. You can also use your own DNS servers or create DNS records by using the host files on your virtual machines. When you select yes for this option, a private DNS zone group is also created. DNS zone group is a link between the private DNS zone and the private endpoint. This link helps you to auto update the private DNS zone when there's an update to the private endpoint. For example, when you add or remove regions, the private DNS zone is automatically updated. |
    | Configuration name |Select your subscription and resource group. The private DNS zone is determined automatically. You can't change it by using the Azure portal.|

1. Select **Ok**. 

1. Select **Next: Tags** > **Review + create**. On the **Review + create** page, then select **Create**.

## Enable private access on an existing cluster

To create a private endpoint to a node in an existing cluster, open the
**Networking** page for the cluster.

1. Select **Add private endpoint**.

   :::image type="content" source="media/howto-private-access/networking.jpg" alt-text="Screenshot of selecting Add private endpoint on the Networking screen.":::

2. On the **Basics** tab of the **Create a private endpoint** screen, confirm the **Subscription**, **Resource group**, and
   **Region**. Enter a **Name** for the endpoint, such as *my-cluster-1*, and a **Network interface name**, such as *my-cluster-1-nic*.

   > [!NOTE]
   >
   > Unless you have a good reason to choose otherwise, we recommend picking a
   > subscription and region that match those of your cluster. The
   > default values for the form fields might not be correct. Check them and
   > update if necessary.

3. Select **Next: Resource**. Choose "Microsoft.DocumentDB/mongoClusters" for **Resource type**, and choose the target cluster for **Resource**. For **Target sub-resource**, choose "MongoCluster".

4. Select **Next: Virtual Network**. Choose the desired **Virtual network** and
   **Subnet**. Under **Private IP configuration**, select **Statically allocate IP address** or keep the default, **Dynamically allocate IP address**.

5. Select **Next: DNS**.

6. Under **Private DNS integration**, for **Integrate with private DNS zone**, keep the default **Yes** or select **No**.

> [!NOTE]
> Private DNS integration needs to be enabled on the cluster for proper DNS resolution.

7. Select **Next: Tags**, and add any desired tags.

8. Select **Review + create**. Review the settings, and select
   **Create** when satisfied.


## Create a private endpoint by using Azure CLI

Run the following Azure CLI script to create a private endpoint named *myPrivateEndpoint* for an existing Azure DocumentDB account. Replace the variable values with the details for your environment.

```azurecli-interactive
# Resource group where the Azure DocumentDB account and virtual network resources are located  
ResourceGroupName="myResourceGroup" 

# Name of the existing Azure DocumentDB account  
ClusterName="myMongoCluster" 

# Subscription ID where the Azure DocumentDB account and virtual network resources are located  
SubscriptionId="<your Azure subscription ID>"  

# API type of your Azure DocumentDB account: Sql, SqlDedicated, MongoCluster, Cassandra, Gremlin, or Table 
SubResourceType="MongoCluster"  

# Name of the virtual network to create  
VNetName="myVnet"  

# Name of the subnet to create  
SubnetName="mySubnet"  

# Name of the private endpoint to create  
PrivateEndpointName="myPrivateEndpoint"  

# Name of the private endpoint connection to create 
PrivateConnectionName="myConnection" 

az network vnet create \
  --name $VNetName \
  --resource-group $ResourceGroupName \
  --subnet-name $SubnetName 

az network vnet subnet update \
  --name <name> \
  --resource-group $ResourceGroupName \
  --vnet-name $VNetName \
  --disable-private-endpoint-network-policies true 

az network private-endpoint create \
  --name $PrivateEndpointName \
  --resource-group $ResourceGroupName \
  --vnet-name $VNetName \
  --subnet $SubnetName \
  --private-connection-resource-id "/subscriptions/$SubscriptionId/resourceGroups/$ResourceGroupName/providers/Microsoft.DocumentDB/mongoClusters/$ClusterName" \
  --group-ids MongoCluster --connection-name $PrivateConnectionName 
```

### Integrate the private endpoint with a private DNS zone
After you create the private endpoint, you should integrate it with a private DNS zone by using the following Azure CLI script:

> [!NOTE]
> Private DNS integration needs to be enabled on the cluster for proper DNS resolution.

```azurecli-interactive
#Zone name differs based on the API type and group ID you are using. 
zoneName="privatelink.mongocluster.cosmos.azure.com" 

az network private-dns zone create \
  --resource-group $ResourceGroupName \
  --name $zoneName 

az network private-dns link vnet create --resource-group $ResourceGroupName \
  --zone-name $zoneName \
  --name <dns-link-name> \
  --virtual-network $VNetName \
  --registration-enabled false 

#Create a DNS zone group
az network private-endpoint dns-zone-group create \
  --resource-group $ResourceGroupName \
  --endpoint-name <pe-name> \
  --name <zone-group-name> \
  --private-dns-zone $zoneName \
  --zone-name mongocluster 
```

## Get connection string to connect
Always use `mongodb+srv` connection string to connect to database from a client with a private IP address that has access to the private endpoint assigned to Azure DocumentDB cluster.

1. Select an existing Azure DocumentDB cluster.
1. On the cluster sidebar, under **Settings**, select **Connection strings**.
1. Copy global read-write or self connection string for native DocumentDB authentication or [Microsoft Entra ID authentication](./how-to-connect-role-based-access-control.md).
> [!NOTE]
> On a replica cluster only self connection strings are provided.
1. Use copied connection string in your application or management tools to connect to the cluster.

## MongoClusters commands on Private Link 
```azurecli-interactive
az network private-link-resource list \
  -g <rg-name> \
  -n <resource-name> \
  --type Microsoft.DocumentDB/mongoClusters 
```

## Verify and troubleshoot private endpoint connectivity

After you create a private endpoint for your Azure DocumentDB cluster, it's important to verify that DNS resolution is working correctly and that your applications can connect through the private endpoint.

### Verify private endpoint status

First, confirm that the private endpoint is properly provisioned and connected:

1. In the Azure portal, navigate to your Azure DocumentDB cluster.
1. On the cluster sidebar, under **Settings**, select **Networking**.
1. Verify that the private endpoint appears in the list with a status of **Approved**.
1. Select the private endpoint name to view its details, including the private IP address assigned.

You can also use Azure CLI to check the private endpoint status:

```azurecli-interactive
az network private-endpoint show \
  --resource-group $ResourceGroupName \
  --name $PrivateEndpointName
```

### Test DNS resolution

Azure DocumentDB uses SRV records for service discovery when using the `mongodb+srv` connection string format. To verify that DNS resolution is working correctly, test the DNS resolution from a virtual machine or resource within the same virtual network or a peered network.

#### Windows DNS testing

From a Windows machine connected to the virtual network, use the following commands:

1. Test the SRV record resolution:

   ```powershell
   Resolve-DnsName -Name _mongodb._tcp.<your-cluster-name>.mongocluster.cosmos.azure.com -Type SRV
   ```

   The output should show SRV records pointing to your cluster nodes within the private DNS zone.

1. Resolve the individual node hostnames to verify they resolve to private IP addresses:

   ```powershell
   Resolve-DnsName -Name <your-node-hostname>.mongocluster.cosmos.azure.com
   ```

   The output should display private IP addresses (for example, 10.x.x.x) instead of public IP addresses.

1. Use `nslookup` as an alternative:

   ```powershell
   nslookup -type=SRV _mongodb._tcp.<your-cluster-name>.mongocluster.cosmos.azure.com
   nslookup <your-node-hostname>.mongocluster.cosmos.azure.com
   ```

#### Linux and macOS DNS testing

From a Linux or macOS machine connected to the virtual network, use the following commands:

1. Test the SRV record resolution:

   ```bash
   dig _mongodb._tcp.<your-cluster-name>.mongocluster.cosmos.azure.com SRV
   ```

   The output should show SRV records with targets pointing to your cluster nodes.

1. Resolve the individual node hostnames:

   ```bash
   dig <your-node-hostname>.mongocluster.cosmos.azure.com
   ```

   The A records should resolve to private IP addresses in your virtual network's address space.

1. Use `nslookup` as an alternative:

   ```bash
   nslookup -type=SRV _mongodb._tcp.<your-cluster-name>.mongocluster.cosmos.azure.com
   nslookup <your-node-hostname>.mongocluster.cosmos.azure.com
   ```

### Common troubleshooting scenarios

If you encounter connectivity issues, check the following:

**DNS resolution fails or returns public IP addresses**

- Verify that the private DNS zone is correctly linked to your virtual network.
- Confirm that the DNS zone group is properly configured on the private endpoint.
- Check that your virtual network's DNS settings are set to use Azure-provided DNS (168.63.129.16) or a custom DNS server that forwards queries to Azure DNS.
- Ensure you're testing from a resource within the virtual network or a properly peered network.

**Connection timeouts or failures**

- Verify that Network Security Group (NSG) rules on the subnet allow outbound connectivity on port 27017 (MongoDB default port).
- Confirm that the private endpoint's network interface has the correct private IP address assigned.
- Check that the application or client is using the correct connection string format (`mongodb+srv`).
- Ensure that firewall rules on the Azure DocumentDB cluster allow connections from the private endpoint.

**Private DNS zone not resolving**

- Verify that the private DNS zone name matches the expected format: `privatelink.mongocluster.cosmos.azure.com`.
- Check that A records exist in the private DNS zone for your cluster nodes.
- Confirm that the virtual network link is active and properly configured in the private DNS zone.

### View private endpoint details

To view detailed information about your private endpoint configuration, use the following Azure CLI command:

```azurecli-interactive
az network private-endpoint show \
  --resource-group $ResourceGroupName \
  --name $PrivateEndpointName \
  --query '{Name:name, PrivateIpAddress:customDnsConfigs[0].ipAddresses[0], FQDN:customDnsConfigs[0].fqdn, ProvisioningState:provisioningState}' \
  --output table
```

This command displays key information including the private IP address, fully qualified domain name (FQDN), and provisioning state.

## Related content
- [Learn more about database security in Azure DocumentDB](./security.md)
- [See guidance on how to enable public access](./how-to-public-access.md)
- [Migrate to Azure DocumentDB](./migration-options.md)
