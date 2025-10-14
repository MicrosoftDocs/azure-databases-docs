---
title: Add private endpoint connections
description: This article describes how to add private endpoint connections to an Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 03/30/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to add private endpoint connections to an Azure Database for PostgreSQL.
---

# Add private endpoint connections

Azure Database for PostgreSQL flexible server is an Azure Private Link service. This means that you can create private endpoints so that your client applications can connect privately and securely to your Azure Database for PostgreSQL flexible server.

A private endpoint to your Azure Database for PostgreSQL flexible server is a network interface that you can inject in a subnet of an Azure virtual network. Any host or service that can route network traffic to that subnet, are able to communicate with your flexible server so that the network traffic doesn't have to traverse the internet. All traffic is sent privately using Microsoft backbone.

For more information about Azure Private Link and Azure Private Endpoint, see [Azure Private Link frequently asked questions](/azure/private-link/private-link-faq).

## [Portal](#tab/portal-add-private-endpoint-connections)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Networking**.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/public-access-networking-disabled.png":::

3. If you have the required permissions to deploy a private endpoint, you can create it by selecting **Create private endpoint**.

    :::image type="content" source="./media/how-to-networking/add-private-endpoint-connection.png" alt-text="Screenshot showing how to begin adding a new private endpoint." lightbox="./media/how-to-networking/add-private-endpoint-connection.png":::

> [!NOTE]
> To learn about the necessary permissions to deploy a private endpoint, see [Azure RBAC permissions for Azure Private Link](/azure/private-link/rbac-permissions).

4. In the **Basics** page, fill all the details required. Then, select **Next: Resource**.

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-basics.png" alt-text="Screenshot showing the Basics page of Create a private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-basics.png":::

5. Use the following table to understand the meaning of the different fields available in the **Basics** page, and as guidance to fill the page:

    | Setting | Suggested value | Description |
    | --- | --- | --- |
    | **Subscription** | Select the name of the [subscription](/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings#subscriptions) in which you want to create the resource. It automatically selects the subscription in which your server is deployed. | A subscription is an agreement with Microsoft to use one or more Microsoft cloud platforms or services, for which charges accrue based on either a per-user license fee or on cloud-based resource consumption. If you have multiple subscriptions, choose the subscription in which you'd like to be billed for the resource. |
    | **Resource group** | The [resource group](/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) in the selected subscription, in which you want to create the private endpoint. It can be an existing resource group, or you can select **Create new**, and provide a name in that subscription which is unique among the existing resource group names. It automatically selects the resource group in which your server is deployed. | A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution, or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can easily deploy, update, and delete them as a group. |
    | **Name** | The name that you want to assign to the private endpoint. | A unique name that identifies the private endpoint through which you could connect to your Azure Database for PostgreSQL flexible server. |
    | **Network Interface Name** | The name that you want to assign to the network interface associated to the private endpoint. | A unique name that identifies the network interface associated to the private endpoint. |
    | **Region** | The name of one of the [regions in which you can create private endpoints for Azure Database for PostgreSQL flexible server](/azure/private-link/availability#databases). | The region you select must match that of the virtual network in which you plan to deploy the private endpoint. |


6. In the **Resource** page, fill all the details required. Then, select **Next: Virtual Network**.

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-resource.png" alt-text="Screenshot showing the Resource page of Create a private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-resource.png":::

7. Use the following table to understand the meaning of the different fields available in the **Resource** page, and as guidance to fill the page:

    | Setting | Suggested value | Description |
    | --- | --- | --- |
    | **Resource type** | Automatically set to `Microsoft.DBforPostgreSQL/flexibleServers` | This value is automatically chosen for you, and corresponds to the type of resource that an Azure Database for PostgreSQL flexible server is, to the eyes of Azure Private Link. |
    | **Resource** | Automatically set to the name of the Azure Database for PostgreSQL flexible server for which you're creating the private endpoint. | The name of the resource to which the private endpoint connects to. |
    | **Target sub-resource** | Automatically set to `postgresqlServer`. | The type of subresource for the resource selected, that your private endpoint is able to access. |

8. In the **Virtual Network** page, fill all the details required. Then, select **Next: DNS**.

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-virtual-network.png" alt-text="Screenshot showing the Virtual Network page of Create a private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-virtual-network.png":::

9. Use the following table to understand the meaning of the different fields available in the **Virtual Network** page, and as guidance to fill the page:

    | Setting | Suggested value | Description |
    | --- | --- | --- |
    | **Virtual network** | Automatically set to the first (sorted in alphabetical order) virtual network available in the subscription and region selected. | Only virtual networks on which you have permissions, in the currently selected subscription and region, are listed. |
    | **Subnet** | Automatically set to the name of the Azure Database for PostgreSQL flexible server for which you're creating the private endpoint. | Only subnets in the currently selected virtual network are listed. |
    | **Network policy for private endpoints** | By default, network policies are disabled for a subnet in a virtual network. You can enable network policies either for network security groups only, for user-defined routes only, or for both. | To use network policies like user-defined routes and network security group support, network policy support must be enabled for the subnet. This setting only applies to private endpoints in the subnet and affects all private endpoints in the subnet. For other resources in the subnet, access is controlled based on security rules in the network security group. For more information, see [Manage network policies for private endpoints](/azure/private-link/disable-private-endpoint-network-policy). |
    | **Private IP configuration** | Automatically set to dynamically allocate one of the available IP addresses in the range assigned to the selected subnet. | This IP address is the one assigned to the network interface associated to the private endpoint. It can be dynamically allocated from the range assigned to the selected subnet, or you can decide which specific address you want to assign to it. After the private endpoint is created, you can't change its IP address, regardless of which of the two allocation modes you select during creation. |
    | **Application security group** | No application security group is assigned by default. You can choose an existing one, or you can create one and assign it. | Application security groups enable you to configure network security as a natural extension of an application's structure, allowing you to group virtual machines and define network security policies based on those groups. You can reuse your security policy at scale without manual maintenance of explicit IP addresses. The platform handles the complexity of explicit IP addresses and multiple rule sets, allowing you to focus on your business logic. For more information, see [Application security groups](/azure/virtual-network/application-security-groups). |

10. In the **DNS** page, fill all the details required. Then, select **Next: Tags**.

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-dns.png" alt-text="Screenshot showing the DNS page of Create a private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-dns.png":::

11. Use the following table to understand the meaning of the different fields available in the **DNS** page, and as guidance to fill the page:

    | Setting | Suggested value | Description |
    | --- | --- | --- |
    | **Integrate with private DNS zone** | Enabled by default. | Select **Yes** if you want your private endpoint to be integrated with an Azure private DNS zone, or **No** if you want to use your own DNS servers, or if you want to resolve the name of the endpoint by using host files in the machines from which you want to connect through the private endpoint. For more information, see [Private endpoint DNS configuration](/azure/private-link/private-endpoint-overview#dns-configuration). If you configure private DNS zone integration, the private DNS zone is automatically linked to the virtual network in which you create the private endpoint. |
    | **Configuration name** | Automatically set for you to `privatelink-postgres-database-azure-com`. | The name assigned to DNS configuration which is associated to the private DNS zone. |
    | **Subscription** | Select the name of the [subscription](/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings#subscriptions) in which you want to create the private DNS zone. It automatically selects the subscription in which your server is deployed. | A subscription is an agreement with Microsoft to use one or more Microsoft cloud platforms or services, for which charges accrue based on either a per-user license fee or on cloud-based resource consumption. If you have multiple subscriptions, choose the subscription in which you'd like to be billed for the resource. |
    | **Resource group** | The [resource group](/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) in the selected subscription, in which you want to create the private DNS zone. It must be an existing resource group. It automatically selects the resource group in which your server is deployed. | A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution, or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can easily deploy, update, and delete them as a group. |
    | **Private DNS zone** | Automatically set for you to `privatelink.postgres.database.azure.com`. | This name is the one assigned to the private DNS zone resource. |

12. In the **Tags** page, fill all the details required. Then, select **Next: Review + create**.

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-tags.png" alt-text="Screenshot showing the Tags page of Create a private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-tags.png":::

13. Use the following table to understand the meaning of the different fields available in the **Tags** page, and as guidance to fill the page:

    | Setting | Suggested value | Description |
    | --- | --- | --- |
    | **Name** | Leave empty. | Name of the tag that you want to assign to your private endpoint and private DNS zone (if you selected private DNS zone integration in the **DNS** page). |
    | **Value** | Leave empty. | Value that you want to assign to the tag with the given name, and that you want to assign to your private endpoint and private DNS zone (if you selected private DNS zone integration in the **DNS** page). |
    | **Resource** | Leave by default. | You can select to which resources you want the given tag assigned. It can be the private endpoint, the private DNS zone (if you selected private DNS zone integration in the **DNS** page), or both. |

14. In the **Review + create** page, make sure that everything is configured as you wanted to. Then, select **Create**.

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-review-create.png" alt-text="Screenshot showing the Review + create page of Create a private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-review-create.png":::

15. A deployment is initiated, and you see a notification when the deployment completes. 

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-deployment-succeeded.png" alt-text="Screenshot showing the successful deployment of the private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-deployment-succeeded.png":::

## [CLI](#tab/cli-add-private-endpoint-connection)

If you have the required permissions to deploy a private endpoint and to approve the private endpoint connection to your server, you can create the private endpoint connection via the [az network private-endpoint create](/cli/azure/network/private-endpoint#az-network-private-endpoint-create) command.

To create the private endpoint and assign to its network interface an IP address dynamically allocated from the range assigned to the selected subnet:

```azurecli-interactive
# Retrieve the resource identifier of the server to which you want to connect via the private endpoint
server_id=$(az postgres flexible-server show --resource-group <resource_group> --name <server> --query id --output tsv)
az network private-endpoint create --connection-name <connection> --name <private_endpoint> --private-connection-resource-id $server_id --resource-group <resource_group> --subnet <subnet> --group-id sites --vnet-name <virtual_network>  
```

To create the private endpoint and assign to its network interface an IP address statically allocated from the range assigned to the selected subnet:

```azurecli-interactive
# Retrieve the resource identifier of the server to which you want to connect via the private endpoint
server_id=$(az postgres flexible-server show --resource-group <resource_group> --name <server> --query id --output tsv)
az network private-endpoint create --connection-name <connection> --name <private_endpoint> --private-connection-resource-id $server_id --resource-group <resource_group> --subnet <subnet> --group-id postgresqlServer --vnet-name <virtual_network> --location <location> --ip-config name=<ip_config> group-id=postgresqlServer member-name=postgresqlServer private-ip-address=<private_ip_address>
```

If you had the required permissions, the private endpoint connection should be automatically approved. If that's the case, the output of the following command would show `status` as `Approved`, and `description` as `Auto-Approved`:

```azurecli-interactive
az network private-endpoint show --resource-group <resource_group> --name <private_endpoint> --query privateLinkServiceConnections[?name==\'<connection>\'].privateLinkServiceConnectionState
```

The `az network private-endpoint create` creates a `privatelink.postgres.database.azure.com` private DNS zone, if it doesn't exist. And it links the private DNS zone to the virtual network in which the private endpoint is created. However, it doesn't create a DNS zone group in the private endpoint If you want, you can integrate your private endpoint with a private DNS zone. To do so, 

```azurecli-interactive
az network private-endpoint dns-zone-group create --resource-group <resource_group> --endpoint-name <endpoint> --name default --private-dns-zone privatelink.postgres.database.azure.com --zone-name privatelink-postgres-database-azure-com
```

If you try to create the private endpoint with a statically allocated private IP address, and the address specified is already used by some other network interface, you get the following error:

```output
Code: PrivateIPAddressIsAllocated
Message: IP configuration /subscriptions/<subscription>/resourceGroups/<resource_group>/providers/Microsoft.Network/networkInterfaces/<network_interface>.nic.<guid>/ipConfigurations/privateEndpointIpConfig.<guid> is using the private IP address <private_ip_address> which is already allocated to resource /subscriptions/<subscription>/resourceGroups/<resource_group>/providers/Microsoft.Network/networkInterfaces/<network_interface>.nic.<guid>/ipConfigurations/privateEndpointIpConfig.<guid>.
```

If you try to create the private endpoint and the virtual network referenced via the `--subscription`, `--resource-group` and `--vnet-name` parameters doesn't exist. Or if the virtual network exists, but the region in which it's deployed doesn't match the region in which you're trying to deploy the private endpoint, you get the following error:

```output
Code: InvalidResourceReference
Message: Resource /subscriptions/<subscription>/resourceGroups/<resource_group>/providers/Microsoft.Network/virtualNetworks/<virtual_network> referenced by resource /subscriptions/<subscription>/resourceGroups/<resource_group>/providers/Microsoft.Network/privateEndpoints/<private_endpoint> was not found. Please make sure that the referenced resource exists, and that both resources are in the same region.
```

If you try to create the private endpoint and one already exists with the same name, but you specify a different value for `--connection-name` or for `--vnet-name`, you get the following error:

```output
Code: CannotChangePrivateLinkConnectionOnPrivateEndpoint
Message: Cannot change the private link connection on private endpoint /subscriptions/<subscription>/resourceGroups/<resource_group>/providers/Microsoft.Network/privateEndpoints/<private_endpoint>. Please ensure you are not updating the details of existing private link connection: '/subscriptions/<subscription>/resourceGroups/<resource_group>/providers/Microsoft.Network/privateEndpoints/<private_endpoint>/privateLinkServiceConnections/<connection>'. That is not allowed.
```

If you try to create the private endpoint and one already exists with the same name, but you specify a different value for `--subnet`, you get the following error:

```output
Code: CannotChangeSubnetOnExistingPrivateEndpoint
Message: Cannot change the subnet in which the network interface for private endpoint /subscriptions/<subscription>/resourceGroups/<resource_group>/providers/Microsoft.Network/privateEndpoints/<private_endpoint> is created. Current subnet: '/subscriptions/<subscription>/resourceGroups/<resource_group>/providers/Microsoft.Network/virtualNetworks/<virtual_network>/subnets/<current_subnet>.' Requested subnet: '/subscriptions/<subscription>/resourceGroups/<resource_group>/providers/Microsoft.Network/virtualNetworks/<virtual_network>/subnets/<requested_subnet>.'
```

If you try to create the private endpoint and one already exists with the same name, but you specify a different value for `--location`, you get the following error:

```output
Code: InvalidResourceLocation
Message: The resource '<private_endpoint>' already exists in location '<current_location>' in resource group '<resource_group>'. A resource with the same name cannot be created in location '<requested_location>'. Please select a new resource name.
```

---

## Related content

- [Networking](how-to-networking.md).
- [Enable public access](how-to-networking-servers-deployed-public-access-enable-public-access.md).
- [Disable public access](how-to-networking-servers-deployed-public-access-disable-public-access.md).
- [Add firewall rules](how-to-networking-servers-deployed-public-access-add-firewall-rules.md).
- [Delete firewall rules](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md).
- [Delete private endpoint connections](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md).
- [Approve private endpoint connections](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md).
- [Reject private endpoint connections](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md).
