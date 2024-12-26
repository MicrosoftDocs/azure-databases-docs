---
title: CLI Script - Create an Azure Database for MySQL - Flexible Server Database in a VNet
description: This Azure CLI sample script shows how to create a Azure Database for MySQL - Flexible Server database in a VNet (private access connectivity method) and connect to the server from a VM within the VNet.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: sample
ms.custom:
  - mvc
  - devx-track-azurecli
ms.devlang: azurecli
---

# Create an Azure Database for MySQL - Flexible Server database in a VNet using Azure CLI

This sample CLI script creates an Azure Database for MySQL - Flexible Server in a VNet ([private access connectivity method](../concepts-networking-vnet.md)) and connects to the server from a VM within the VNet.

> [!NOTE]  
> The connectivity method cannot be changed after creating the server. For example, if you create server using *Private access (VNet Integration)*, you cannot change to *Public access (allowed IP addresses)* after creation. To learn more about connectivity methods, see [Connectivity and networking concepts for Azure Database for MySQL - Flexible Server](../concepts-networking.md).

[!INCLUDE [quickstarts-free-trial-note](../../includes/flexible-server-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

## Sample script

[!INCLUDE [cli-launch-cloud-shell-sign-in.md](~/reusable-content/ce-skilling/azure/includes/cli-launch-cloud-shell-sign-in.md)]

### Run the script

:::code language="azurecli" source="~/azure_cli_scripts/mysql/flexible-server/create-server-private-access/create-connect-server-in-vnet.sh" id="FullScript":::

## Test connectivity to the MySQL server from the VM

Use the following steps to test connectivity to the MySQL server from the VM by connecting using SSH, downloading MySQL tools, and then using them to connect to the MySQL server.

1. To SSH into the VM, start by getting the public IP address and then use MySQL tools to connect

   ```csharp
   PUBLIC_IP=$(az vm list-ip-addresses --resource-group $RESOURCE_GROUP --name $VM --query "[].virtualMachine.network.publicIpAddresses[0].ipAddress" --output tsv)

   ssh azureuser@$PUBLIC_IP
   ```

1. Download MySQL tools and connect to the server. Substitute <server_name> and <admin_user> with your values.

   ```bash
   sudo apt-get update
   sudo apt-get install mysql-client

   wget --no-check-certificate https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem

   mysql -h <replace_with_server_name>.mysql.database.azure.com -u mysqladmin -p --ssl-mode=REQUIRED --ssl-ca=DigiCertGlobalRootCA.crt.pem
   ```

## Clean up resources

[!INCLUDE [cli-clean-up-resources.md](~/reusable-content/ce-skilling/azure/includes/cli-clean-up-resources.md)]

```azurecli
az group delete --name $RESOURCE_GROUP
```

## Sample reference

This script uses the following commands. Each command in the table links to command specific documentation.

| **Command** | **Notes** |
| --- | --- |
| [az group create](/cli/azure/group#az-group-create) | Creates a resource group in which all resources are stored |
| [az mysql flexible-server create](/cli/azure/mysql/flexible-server#az-mysql-flexible-server-create) | Creates a Flexible Server that hosts the databases. |
| [az network vnet subnet create](/cli/azure/network/vnet/subnet#az-network-vnet-subnet-create) | Creates a subnet within the VNet. |
| [az vm create](/cli/azure/vm#az-vm-create) | Creates an Azure Virtual Machine. |
| [az vm open-port](/cli/azure/vm#az-vm-open-port) | Opens a VM to inbound traffic on specified ports. |
| [az group delete](/cli/azure/group#az-group-delete) | Deletes a resource group including all nested resources. |

## Related content

- [Azure CLI samples for Azure Database for MySQL - Flexible Server](../sample-scripts-azure-cli.md)
- [Azure CLI documentation](/cli/azure)
