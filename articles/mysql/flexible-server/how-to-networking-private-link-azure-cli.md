---
title: Private Link Using Azure CLI
description: Learn how to configure private link for Azure Database for MySQL - Flexible Server by using the Azure CLI.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - devx-track-azurecli
---

# Create and manage Private Link for Azure Database for MySQL - Flexible Server using Azure CLI

In this article, you learn how to use Azure CLI to create a private endpoint for accessing Azure Database for MySQL Flexible Server from a VM in a VNet.

### Launch Azure Cloud Shell

The [Azure Cloud Shell](/azure/cloud-shell/overview) is a free interactive shell that you can use to run the steps in this article. It has standard Azure tools preinstalled and configured to use with your account.

To open the Cloud Shell, select **Try it** from the upper right corner of a code block. You can also open Cloud Shell in a separate browser tab by going to [https://shell.azure.com/bash](https://portal.azure.com/#cloudshell). Select **Copy** to copy the blocks of code, paste it into the Cloud Shell, and select **Enter** to run it.

If you prefer to install and use the CLI locally, this quickstart requires Azure CLI version 2.0 or later. Run `az --version` to find the version. See [Install Azure CLI](/cli/azure/install-azure-cli) if you need to install or upgrade.

### Prerequisites

You must log in to your account using the [az login](/cli/azure/reference-index#az-login) command. Note the **id** property, which refers to **Subscription ID** for your Azure account.

```azurecli-interactive
az login
```

Select the specific subscription under your account using [az account set](/cli/azure/account#az-account-set) command. In the command, note the **id** value from the **az login** output to use as the value for **subscription** argument. If you have multiple subscriptions, choose the appropriate subscription in which the resource should be billed. Use [az account list](/cli/azure/account#az-account-list) to get all your subscriptions.

```azurecli-interactive
az account set --subscription <subscription id>
```

### Create a resource group

Before creating any resource, you must create a resource group to host the Virtual Network. Create a resource group with [az group create](/cli/azure/group). This example creates a resource group named *myResourceGroup* in the *westeurope* location:

```azurecli-interactive
az group create --name myResourceGroup --location westeurope
```

### Create a Virtual Network

Create a Virtual Network with [az network vnet create](/cli/azure/network/vnet). This example creates a default Virtual Network named *myVirtualNetwork* with one subnet named *mySubnet*:

```azurecli-interactive
az network vnet create \
 --name myVirtualNetwork \
 --resource-group myResourceGroup \
 --subnet-name mySubnet
```

### Disable subnet private endpoint policies

Azure deploys resources to a subnet within a virtual network, so you need to create or update the subnet to disable private endpoint [network policies](/azure/private-link/disable-private-endpoint-network-policy). Update a subnet configuration named *mySubnet* with [az network vnet subnet update](/cli/azure/network/vnet/subnet#az-network-vnet-subnet-update):

```azurecli-interactive
az network vnet subnet update \
 --name mySubnet \
 --resource-group myResourceGroup \
 --vnet-name myVirtualNetwork \
 --disable-private-endpoint-network-policies true
```

### Create the VM

Create a VM with `az vm create`. When prompted, provide a password to be used as the sign-in credentials for the VM. This example creates a VM named *myVm*:

```azurecli-interactive
az vm create \
  --resource-group myResourceGroup \
  --name myVm \
  --image Win2019Datacenter
```

> [!NOTE]  
> Record the VM's public IP address as it's needed to connect from the internet in the next step.

### Create the Azure Database for MySQL Flexible Server instance with public access in the resource group

Create an Azure Database for MySQL Flexible Server instance with public access and add the client IP address to access it.

```azurecli-interactive
az mysql flexible-server create \
  --name mydemoserver \
  --resource-group myResourcegroup \
  --location westeurope \
  --admin-user mylogin \
  --admin-password <server_admin_password> \
  --public-access <my_client_ip>
```

> [!NOTE]  
> In some cases, the Azure Database for MySQL Flexible Server instance and the VNet-subnet are in different subscriptions. In these cases, you must ensure the following configurations:
>  
> - Make sure that both subscriptions have the **Microsoft.DBforMySQL/flexibleServer** resource provider registered. For more information, refer to [resource-manager-registration](/azure/azure-resource-manager/management/resource-providers-and-types).

### Create the Private Endpoint

Create a private endpoint for Azure Database for MySQL Flexible Server in your Virtual Network:

```azurecli-interactive
az network private-endpoint create \
    --name myPrivateEndpoint \
    --resource-group myResourceGroup \
    --vnet-name myVirtualNetwork  \
    --subnet mySubnet \
    --private-connection-resource-id $(az resource show -g myResourcegroup -n mydemoserver --resource-type "Microsoft.DBforMySQL/flexibleServers" --query "id" -o tsv) \
    --group-id mysqlServer \
    --connection-name myConnection \
    --location location
 ```

### Configure the Private DNS Zone

Create a Private DNS Zone for the Azure Database for MySQL Flexible Server domain and create an association link with the Virtual Network.

```azurecli-interactive
az network private-dns zone create --resource-group myResourceGroup \
   --name  "privatelink.mysql.database.azure.com"
az network private-dns link vnet create --resource-group myResourceGroup \
   --zone-name  "privatelink.mysql.database.azure.com"\
   --name MyDNSLink \
   --virtual-network myVirtualNetwork \
   --registration-enabled false

# Query for the network interface ID
$networkInterfaceId=$(az network private-endpoint show --name myPrivateEndpoint --resource-group myResourceGroup --query 'networkInterfaces[0].id' -o tsv)

az resource show --ids $networkInterfaceId --api-version 2019-04-01 -o json
# Copy the content for privateIPAddress and FQDN matching the MySQL flexible server name

# Create DNS records
az network private-dns record-set a create --name myserver --zone-name privatelink.mysql.database.azure.com --resource-group myResourceGroup
az network private-dns record-set a add-record --record-set-name myserver --zone-name privatelink.mysql.database.azure.com --resource-group myResourceGroup -a <Private IP Address>
```

> [!NOTE]  
> The FQDN in the customer's DNS setting does not resolve the private IP configured. You must set up a DNS zone for the configured FQDN as shown[here](/azure/dns/dns-operations-recordsets-portal).

### Connect to a VM from the internet

Connect to the VM *myVm* from the internet as follows:

1. In the portal's search bar, enter *myVm*.

1. Select the **Connect** button. After selecting the **Connect** button, **Connect to virtual machine** opens.

1. Select **Download RDP File**. Azure creates a Remote Desktop Protocol (*.rdp*) file and downloads it to your computer.

1. Open the *downloaded.rdp* file.

    1. If prompted, select **Connect**.

. Enter the username and password you specified when creating the VM.
        > [!NOTE]  
        > You might need to select **More choices** **Use a different account**, to specify the credentials you entered when you created the VM.
1. Select **OK**.

1. You might receive a certificate warning during the sign-in process. Select **Yes** or **Continue** if you receive a certificate warning.

1. Once the VM desktop appears, minimize it to return to your local desktop.

### Access the Azure Database for MySQL Flexible Server instance privately from the VM

1. In the Remote Desktop of *myVM*, open PowerShell.

1. Enter `nslookup mydemomysqlserver.privatelink.mysql.database.azure.com`.

    You'll receive a message similar to this:

    ```azurepowershell
    Server:  UnKnown
    Address:  168.63.129.16
    Non-authoritative answer:
    Name:    mydemomysqlserver.privatelink.mysql.database.azure.com
    Address:  10.1.3.4
    ```

1. Test the private link connection for the Azure Database for MySQL Flexible Server instance using any available client. The following example uses [MySQL Workbench](https://dev.mysql.com/doc/workbench/en/wb-installing-windows.html) to do the operation.

1. In **New connection**, enter or select this information:

    | Setting | Value |
    | --- | --- |
    | Connection Name | Select the connection name of your choice. |
    | Hostname | Select *mydemoserver.privatelink.mysql.database.azure.com* |
    | Username | Enter username as *username@servername* provided during the Azure Database for MySQL Flexible Server instance creation. |
    | Password | Enter a password provided during the Azure Database for MySQL Flexible Server instance creation. |

1. Select Connect.

1. Browse databases from left menu.

1. (Optionally) Create or query information from the Azure Database for MySQL Flexible Server database.

1. Close the remote desktop connection to myVm.

### Clean up resources

When no longer needed, you can use `az group delete` to remove the resource group and all the resources it has:

```azurecli-interactive
az group delete --name myResourceGroup --yes
```

## Additional Private Link CLI commands

List private linkable sub-resources (groupIds)

```azurecli-interactive
az network private-link-resource list --id {PrivateLinkResourceID}  // or -g MyResourceGroup -n MySA --type Microsoft.Storage/storageAccounts
```

List private endpoint connections on a given resource

```azurecli-interactive
az network private-endpoint-connection list --id {PrivateLinkResourceID}
```

Approve private endpoint connections on a given resource

```azurecli-interactive
az network private-endpoint-connection approve --id {PrivateEndpointConnectionID}  --description "Approved!"
```

Reject private endpoint connections on a given resource

```azurecli-interactive
az network private-endpoint-connection reject --id {PrivateEndpointConnectionID}  --description "Rejected!"
```

Delete private endpoint connections on a given resource

```azurecli-interactive
az network private-endpoint-connection delete --id {PrivateEndpointConnectionID}
```

## Related content

- [Create and manage Private Link for Azure Database for MySQL - Flexible Server using the portal](how-to-networking-private-link-portal.md)
- [manage connectivity](concepts-networking.md)
- [Data encryption with customer managed keys for Azure Database for MySQL - Flexible Server](concepts-customer-managed-key.md)
- [Microsoft Entra authentication for Azure Database for MySQL - Flexible Server](concepts-azure-ad-authentication.md)
