---
title: Manage Virtual Networks - Azure CLI
description: Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure CLI.
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

# Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure CLI

Azure Database for MySQL Flexible Server supports two types of mutually exclusive network connectivity methods to connect to your Azure Database for MySQL Flexible Server instance. The two options are:

- Public access (allowed IP addresses)
- Private access (virtual network integration)

This article focuses on creation of MySQL server with **Private access (virtual network Integration)** using Azure CLI. With *Private access (virtual network integration)*, you can deploy your Azure Database for MySQL Flexible Server instance into your own [Azure Virtual Network](/azure/virtual-network/virtual-networks-overview). Azure Virtual Networks provide private and secure network communication. In Private access, the connections to the Azure Database for MySQL Flexible Server instance are restricted to only within your virtual network. To learn more about it, refer to [Private Network Access using virtual network integration for Azure Database for MySQL - Flexible Server](concepts-networking-vnet.md).

In Azure Database for MySQL Flexible Server, you can only deploy the server to a virtual network and subnet during creation of the server. After the Azure Database for MySQL Flexible Server instance is deployed to a virtual network and subnet, you can't move it to another virtual network, subnet or to *Public access (allowed IP addresses)*.

## Launch Azure Cloud Shell

The [Azure Cloud Shell](/azure/cloud-shell/overview) is a free interactive shell that you can use to run the steps in this article. It has common Azure tools preinstalled and configured to use with your account.

To open the Cloud Shell, just select **Try it** from the upper right corner of a code block. You can also open Cloud Shell in a separate browser tab by going to [https://shell.azure.com/bash](https://portal.azure.com/#cloudshell). Select **Copy** to copy the blocks of code, paste it into the Cloud Shell, and select **Enter** to run it.

If you prefer to install and use the CLI locally, this quickstart requires Azure CLI version 2.0 or later. Run `az --version` to find the version. If you need to install or upgrade, see [Install Azure CLI](/cli/azure/install-azure-cli).

## Prerequisites

You need to sign in to your account using the [az login](/cli/azure/reference-index#az-login) command. Note the **ID** property, which refers to **Subscription ID** for your Azure account.

```azurecli-interactive
az login
```

Select the specific subscription under your account using [az account set](/cli/azure/account#az-account-set) command. Make a note of the **ID** value from the **az login** output to use as the value for **subscription** argument in the command. If you have multiple subscriptions, choose the appropriate subscription in which the resource should be billed. To get all your subscription, use [az account list](/cli/azure/account#az-account-list).

```azurecli
az account set --subscription <subscription id>
```

## Create an Azure Database for MySQL Flexible Server instance using CLI

You can use the `az mysql flexible-server` command to create the Azure Database for MySQL Flexible Server instance with *Private access (virtual network integration)*. This command uses Private access (virtual network integration) as the default connectivity method. A virtual network and subnet are created for you if none is provided. You can also provide the already existing virtual network and subnet using subnet ID. <!-- You can provide the **vnet**,**subnet**,**vnet-address-prefix** or**subnet-address-prefix** to customize the virtual network and subnet.--> There are various options to create an Azure Database for MySQL Flexible Server instance using CLI as shown in the following examples.

> [!IMPORTANT]  
> Using this command will delegate the subnet to **Microsoft.DBforMySQL/flexibleServers**. This delegation means that only Azure Database for MySQL Flexible Server instances can use that subnet. No other Azure resource types can be in the delegated subnet.
>

Refer to the Azure CLI [reference documentation](/cli/azure/mysql/flexible-server) for the complete list of configurable CLI parameters. For example, in the following commands you can optionally specify the resource group.

- Create an Azure Database for MySQL Flexible Server instance using default virtual network, subnet with default address prefix.

    ```azurecli-interactive
    az mysql flexible-server create
    ```

- Create an Azure Database for MySQL Flexible Server instance using already existing virtual network and subnet. If provided virtual network and subnet don't exist, then virtual network and subnet with default address prefix are created.

    ```azurecli-interactive
    az mysql flexible-server create --vnet myVnet --subnet mySubnet
    ```

- Create an Azure Database for MySQL Flexible Server instance using already existing virtual network, subnet, and using the subnet ID. The provided subnet shouldn't have any other resource deployed in it and this subnet are delegated to **Microsoft.DBforMySQL/flexibleServers**, if not already delegated.

    ```azurecli-interactive
    az mysql flexible-server create --subnet /subscriptions/{SubID}/resourceGroups/{ResourceGroup}/providers/Microsoft.Network/virtualNetworks/{VNetName}/subnets/{SubnetName}
    ```

    > [!NOTE]  
    > The virtual network and subnet should be in the same region and subscription as your Azure Database for MySQL Flexible Server instance.
<
- Create an Azure Database for MySQL Flexible Server instance using a new virtual network, subnet with nondefault address prefix.

    ```azurecli-interactive
    az mysql flexible-server create --vnet myVnet --address-prefixes 10.0.0.0/24 --subnet mySubnet --subnet-prefixes 10.0.0.0/24
    ```

Refer to the Azure CLI [reference documentation](/cli/azure/mysql/flexible-server) for the complete list of configurable CLI parameters.

## Related content

- [networking in Azure Database for MySQL Flexible Server](concepts-networking.md)
- [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-virtual-network-portal.md)
- [Azure Database for MySQL Flexible Server virtual network](./concepts-networking-vnet.md#private-access-virtual-network-integration)
