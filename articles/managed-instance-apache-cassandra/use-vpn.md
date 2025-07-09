---
title: Use a VPN with Azure Managed Instance for Apache Cassandra
description: Discover how to secure your cluster with a VPN when you use Azure Managed Instance for Apache Cassandra.
author: IriaOsara
ms.author: iriaosara
ms.service: azure-managed-instance-apache-cassandra
ms.topic: how-to
ms.date: 02/08/2024
ms.devlang: azurecli

---
# Use a VPN with Azure Managed Instance for Apache Cassandra

Azure Managed Instance for Apache Cassandra nodes require access to many other Azure services when they're injected into your virtual network. Normally, access is enabled by ensuring that your virtual network has outbound access to the internet. If your security policy prohibits outbound access, you can configure firewall rules or user-defined routes for the appropriate access. For more information, see [Required outbound network rules](network-rules.md).

If you have internal security concerns about data exfiltration, your security policy might prohibit direct access to these services from your virtual network. By using a virtual private network (VPN) with Azure Managed Instance for Apache Cassandra, you can ensure that data nodes in the virtual network communicate with only a single VPN endpoint, with no direct access to any other services.

## How it works

A virtual machine (VM) called the operator is part of each Azure Managed Instance for Apache Cassandra, and it helps to manage the cluster. By default, the operator is in the same virtual network as the cluster. The operator and data VMs have the same network security group (NSG) rules, which isn't ideal for security reasons. It also lets you prevent the operator from reaching necessary Azure services when you set up NSG rules for your subnet.

Using a VPN as your connection method for Azure Managed Instance for Apache Cassandra lets the operator be in a different virtual network than the cluster by using the private link service. The operator is in a virtual network that has access to the necessary Azure services, and the cluster is in a virtual network that you control.

:::image type="content" source="./media/use-vpn/vpn-design.png" alt-text="Diagram that shows a VPN design." lightbox="./media/use-vpn/vpn-design.png" border="true":::

With the VPN, the operator can now connect to a private IP address inside the address range of your virtual network called a private endpoint. The private link routes the data between the operator and the private endpoint through the Azure backbone network to avoid exposure to the public internet.

## Security benefits

We want to prevent attackers from accessing the virtual network where the operator is deployed and attempting to steal data. Security measures are in place to make sure that the operator can reach only necessary Azure services.

* **Service endpoint policies:** These policies offer granular control over egress traffic within the virtual network, in particular to Azure services. By using service endpoints, they establish restrictions. Policies permit data access exclusively to specified Azure services like Azure Monitor, Azure Storage, and Azure Key Vault. These policies ensure that data egress is limited solely to predetermined Azure Storage accounts, which enhances security and data management within the network infrastructure.
* **Network security groups:** These groups are used to filter network traffic to and from the resources in an Azure virtual network. All traffic is blocked from the operator to the internet. Only traffic to certain Azure services is allowed through a set of NSG rules.

## Use a VPN with Azure Managed Instance for Apache Cassandra

1. Create an Azure Managed Instance for Apache Cassandra cluster by using `VPN` as the value for the `--azure-connection-method` option:

    ```bash
    az managed-cassandra cluster create \
    --cluster-name "vpn-test-cluster" \
    --resource-group "vpn-test-rg" \
    --location "eastus2" \
    --azure-connection-method "VPN" \
    --initial-cassandra-admin-password "password"
    ```

1. Use the following command to see the cluster properties:

    ```bash
    az managed-cassandra cluster show \
    --resource-group "vpn-test-rg" \
    --cluster-name "vpn-test-cluster"
    ```

    From the output, make a copy of the `privateLinkResourceId` value.

1. In the Azure portal, [create a private endpoint](../cosmos-db/how-to-configure-private-endpoints.md) by following these steps:
    1. On the **Resource** tab, select **Connect to an Azure resource by resource ID or alias** as the connection method and select **Microsoft.Network/privateLinkServices** as the resource type. Enter the `privateLinkResourceId` value from the previous step.
    1. On the **Virtual Network** tab, select your virtual network's subnet, and select the **Statically allocate IP address** option.
    1. Validate and create.

   > [!NOTE]
   > At the moment, the connection between the management service and your private endpoint requires approval from the [Azure Managed Instance for Apache Cassandra team](mailto:cassandra-preview@microsoft.com).

1. Get the IP address of your private endpoint's network interface.

1. Create a new datacenter by using the IP address from the previous step as the `--private-endpoint-ip-address` parameter.

## Related content

- Learn about [hybrid cluster configuration](configure-hybrid-cluster.md) in Azure Managed Instance for Apache Cassandra.
