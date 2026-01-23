---
title: Manage Firewall Rules - Azure CLI
description: Create and manage firewall rules for Azure Database for MySQL - Flexible Server using Azure CLI command line.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan, randolphwest
ms.date: 01/07/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - devx-track-azurecli
  - horz-security
ms.devlang: azurecli
---

# Manage firewall rules for Azure Database for MySQL using Azure CLI

Azure Database for MySQL flexible server supports two mutually exclusive network connectivity methods to connect to your flexible server. The two options are:

- Public access (allowed IP addresses)
- Private access (virtual network Integration)

In this article, you focus on creating an Azure Database for MySQL flexible server instance with **Public access (allowed IP addresses)** by using Azure CLI. This article provides an overview of Azure CLI commands you can use to create, update, delete, list, and show firewall rules after creating a server. By using *Public access (allowed IP addresses)*, you restrict connections to the Azure Database for MySQL flexible server instance to allowed IP addresses only. You need to allow the client IP addresses in the firewall rules. For more information, see [Public access (allowed IP addresses)](concepts-networking-public.md#public-access-allowed-ip-addresses). You can define the firewall rules at the time of server creation (recommended) or add them later.

## Launch Azure Cloud Shell

The [Azure Cloud Shell](/azure/cloud-shell/overview) is a free interactive shell that you can use to run the steps in this article. It has common Azure tools preinstalled and configured to use with your account.

To open the Cloud Shell, select **Try it** from the upper right corner of a code block. You can also open Cloud Shell in a separate browser tab by going to [https://shell.azure.com/bash](https://portal.azure.com/#cloudshell). Select **Copy** to copy the blocks of code, paste it into the Cloud Shell, and select **Enter** to run it.

If you prefer to install and use the CLI locally, this quickstart requires Azure CLI version 2.0 or later. Find the version by using `az --version`. If you need to install or upgrade, see [Install Azure CLI](/cli/azure/install-azure-cli).

## Prerequisites

Sign in to your account by using the [az login](/cli/azure/reference-index#az-login) command. Note the **ID** property, which refers to **Subscription ID** for your Azure account.

```azurecli-interactive
az login
```

Select the specific subscription under your account by using the [az account set](/cli/azure/account#az-account-set) command. Use the **ID** value from the **az login** output as the value for the **subscription** argument in the command. If you have multiple subscriptions, choose the appropriate subscription in which the resource should be billed. To get all your subscriptions, use [az account list](/cli/azure/account#az-account-list).

```azurecli
az account set --subscription <subscription id>
```

## Create firewall rule during flexible server using Azure CLI

Use the `az mysql flexible-server --public access` command to create the Azure Database for MySQL flexible server instance with *Public access (allowed IP addresses)* and configure the firewall rules while creating the server. Use the **-public-access** switch to provide the allowed IP addresses that can connect to the server. Provide a single IP address or a range of IP addresses to include in the allowed list. The IP address range must be dash-separated and can't contain any spaces. The following examples show various options to create an Azure Database for MySQL flexible server instance by using Azure CLI.

For the complete list of configurable CLI parameters, see the Azure CLI [reference documentation](/cli/azure/mysql/flexible-server). For example, you can optionally specify the resource group in the following commands.

## Examples

The following examples demonstrate different ways to configure firewall rules during server creation. 

Each example shows how to specify IP addresses by using the `--public-access` parameter with different formats (single IP, IP range, Azure services, or all IPs).

- Create an Azure Database for MySQL flexible server instance with public access and add the client IP address to have access to the server.

  ```azurecli-interactive
  az mysql flexible-server create --public-access <my_client_ip>
  ```

- Create an Azure Database for MySQL flexible server instance with public access and add the range of IP address to have access to this server.

  ```azurecli-interactive
  az mysql flexible-server create --public-access <start_ip_address-end_ip_address>
  ```

- Create an Azure Database for MySQL flexible server instance with public access and allow applications from Azure IP addresses to connect to your server.

  ```azurecli-interactive
  az mysql flexible-server create --public-access 0.0.0.0
  ```

  > [!IMPORTANT]  
  > This option configures the firewall to allow public access from Azure services and resources within Azure to this server, including connections from the subscriptions of other customers. When selecting this option, ensure your sign-in and user permissions limit access to only authorized users.

- Create an Azure Database for MySQL flexible server instance with public access and allow all IP address.

  ```azurecli-interactive
  az mysql flexible-server create --public-access all
  ```

  > [!WARNING]  
  > This command creates a firewall rule with start IP address=0.0.0.0, end IP address=255.255.255.255 and no IP addresses are blocked. Any host on the Internet can access this server. Use this rule only temporarily and only on test servers that don't contain sensitive data.

- Create an Azure Database for MySQL flexible server instance with public access and with no IP address.

  ```azurecli-interactive
  az mysql flexible-server create --public-access none
  ```

  > [!NOTE]  
  > Don't create a server without any firewall rules. If you don't add any firewall rules, no client can connect to the server.

## Create and manage firewall rule after server creation

Use the **az mysql flexible-server firewall-rule** command in Azure CLI to create, delete, list, show, and update firewall rules.

Commands:

- **create**: Create an Azure Database for MySQL flexible server firewall rule.
- **list**: List the Azure Database for MySQL flexible server firewall rules.
- **update**: Update an Azure Database for MySQL flexible server firewall rule.
- **show**: Show the details of an Azure Database for MySQL flexible server firewall rule.
- **delete**: Delete an Azure Database for MySQL flexible server firewall rule.

For the complete list of configurable CLI parameters, see the Azure CLI [reference documentation](/cli/azure/mysql/flexible-server). For example, in the following commands, you can optionally specify the resource group.

### Create a firewall rule

Use the `az mysql flexible-server firewall-rule create` command to create a new firewall rule on the server.
To allow access to a range of IP addresses, provide the IP address as the start and end IP addresses, as in this example.

```azurecli-interactive
az mysql flexible-server firewall-rule create --resource-group testGroup --name mydemoserver --start-ip-address 13.83.152.0 --end-ip-address 13.83.152.15
```

To allow access for a single IP address, provide the single IP address, as in this example.

```azurecli-interactive
az mysql flexible-server firewall-rule create --resource-group testGroup --name mydemoserver --start-ip-address 1.1.1.1
```

To allow applications from Azure IP addresses to connect to your Azure Database for MySQL flexible server instance, provide the IP address `0.0.0.0` as the start IP, as in this example.

```azurecli-interactive
az mysql flexible-server firewall-rule create --resource-group testGroup --name mydemoserver --start-ip-address 0.0.0.0
```

> [!IMPORTANT]  
> This option configures the firewall to allow public access from Azure services and resources within Azure to this server, including connections from the subscriptions of other customers. When selecting this option, make sure your authentication and user permissions limit access to only authorized users.

Upon success, each create command output lists the details of the firewall rule created in JSON format (by default). If there's a failure, the result shows an error message text instead.

### List firewall rules

Use the `az mysql flexible-server firewall-rule list` command to list the existing server firewall rules on the server. Specify the server name in the **-name** switch.

```azurecli-interactive
az mysql flexible-server firewall-rule list --name mydemoserver
```

The output lists the rules, if any, in JSON format (by default). You can use the **-output table** switch to output the results in a more readable table format.

```azurecli-interactive
az mysql flexible-server firewall-rule list --name mydemoserver --output table
```

### Update a firewall rule

Use the `az mysql flexible-server firewall-rule update` command to update an existing firewall rule on the server. Provide the name of the existing firewall rule as input, and the start IP address and end IP address attributes to update.

```azurecli-interactive
az mysql flexible-server firewall-rule update --name mydemoserver --rule-name FirewallRule1 --start-ip-address 13.83.152.0 --end-ip-address 13.83.152.1
```

If the command succeeds, the command output lists the details of the firewall rule updated in JSON format (by default). If the command fails, the output shows an error message text instead.

> [!NOTE]  
> If the firewall rule doesn't exist, the update command creates the rule.

### Show firewall rule details

Use the `az mysql flexible-server firewall-rule show` command to show the existing firewall rule details from the server. Provide the name of the existing firewall rule as input.

```azurecli-interactive
az mysql flexible-server firewall-rule show --name mydemoserver --rule-name FirewallRule1
```

If the command succeeds, the command output lists the details of the firewall rule specified in JSON format (by default). If the command fails, the output shows an error message text instead.

### Delete a firewall rule

Use the `az mysql flexible-server firewall-rule delete` command to delete an existing firewall rule from the server. Provide the name of the current firewall rule.

```azurecli-interactive
az mysql flexible-server firewall-rule delete --name mydemoserver --rule-name FirewallRule1
```

If the command succeeds, there's no output. If the command fails, an error message text is displayed.

## Related content

- [Connectivity and networking concepts for Azure Database for MySQL - Flexible Server](concepts-networking.md)
- [Azure Database for MySQL flexible server firewall rules](concepts-networking-public.md#public-access-allowed-ip-addresses)
- [Manage firewall rules for Azure Database for MySQL - Flexible Server using the Azure portal](security-how-to-manage-firewall-portal.md)
