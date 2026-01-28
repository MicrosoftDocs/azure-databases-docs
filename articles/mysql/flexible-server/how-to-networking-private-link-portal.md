---
title: Configure Private Link by Using the Azure Portal
description: Learn how to use the Azure portal to configure Private Link for Azure Database for MySQL - Flexible Server.
author: aditivgupta
ms.author: adig
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - sfi-image-nochange
---

# Create and manage Private Link for Azure Database for MySQL - Flexible Server using the portal

This tutorial describes how to configure an Azure Database for MySQL Flexible Server instance to use Private Link for secure connectivity.

### Sign in to Azure

Sign in to the [Azure portal](https://portal.azure.com).

### Create the virtual network

In this section, you create a Virtual Network and the subnet to host the VM used to access your Private Link resource.

1. On the upper-left side of the screen, select **Create a resource** > **Networking** > **Virtual network**.
1. In **Create virtual network**, then select this information:

   | Setting | Value |
   | --- | --- |
   | Name | Enter *MyVirtualNetwork*. |
   | Address space | Enter *10.1.0.0/16*. |
   | Subscription | Select your subscription. |
   | Resource group | Select **Create new**, enter *myResourceGroup*, then select **OK**. |
   | Location | Select **West Europe**. |
   | Subnet - Name | Enter *mySubnet*. |
   | Subnet - Address range | Enter *10.1.0.0/24*. |

| 1. Leave the rest as default and select **Create**. |

### Create a Virtual Machine

1. On the upper-left side of the screen in the Azure portal, select **Create a resource** > **Compute** > **Virtual Machine**.

1. In **Create a virtual machine - Basics**, then select this information:

   | Setting | Value |
   | --- | --- |
   | **PROJECT DETAILS** | |
   | Subscription | Select your subscription. |
   | Resource group | Select the created resource group `myResourceGroup`. |
   | **INSTANCE DETAILS** | |
   | Virtual machine name | Enter *myVm*. |
   | Region | Select **West Europe**. |
   | Availability options | Leave the default **No infrastructure redundancy required**. |
   | Image | Select **Windows Server 2019 Datacenter**. |
   | Size | Leave the default **Standard DS1 v2**. |
   | **ADMINISTRATOR ACCOUNT** | |
   | Username | Enter a username of your choosing. |
   | Password | Enter a password of your choosing. The password must be at least 12 characters long and meet the [defined complexity requirements](/azure/virtual-machines/windows/faq?toc=%2fazure%2fvirtual-network%2ftoc.json#what-are-the-password-requirements-when-creating-a-vm-). |
   | Confirm Password | Reenter password. |
   | **INBOUND PORT RULES** | |
   | Public inbound ports | Leave the default **None**. |
   | **SAVE MONEY** | |
   | Already have a Windows license? | Leave the default **No**. |

1. Select **Next: Disks**.

1. In **Create a virtual machine - Disks**, leave the defaults and select **Next: Networking**.

1. In **Create a virtual machine - Networking**, select this information:

   | Setting | Value |
   | --- | --- |
   | Virtual network | Leave the default **MyVirtualNetwork**. |
   | Address space | Leave the default **10.1.0.0/24**. |
   | Subnet | Leave the default **mySubnet (10.1.0.0/24)**. |
   | Public IP | Leave the default **(new) myVm-ip**. |
   | Public inbound ports | Select **Allow selected ports**. |
   | Select inbound ports | Select **HTTP** and **RDP**. |

1. Select **Review + create**. You're taken to the **Review + create** page, where Azure validates your configuration.

1. When you see the **Validation passed** message, select **Create**.

### Create an Azure Database for MySQL Flexible Server instance with a Private endpoint

- Create an [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md) with **Public access (allowed IP addresses) and Private endpoint** as the connectivity method.

- Select **Add Private endpoint** to create private endpoint:

  | Setting | Value |
  | --- | --- |
  | **Project details** | |
  | Subscription | Select your subscription. |
  | Resource group | Select **myResourceGroup**. You created this in the previous section. |
  | **Instance Details** | |
  | Name | Enter *myPrivateEndpoint*. If this name is taken, create a unique name. |
  | Location | Select **West Europe**. |
  | Virtual network | Select *MyVirtualNetwork*. |
  | Subnet | Select *mySubnet*. |
  | **PRIVATE DNS INTEGRATION** | |
  | Integrate with private DNS zone | Select **Yes**. |
  | Private DNS Zone | Select *(New)privatelink.mysql.database.Azure.com* |

- Select **OK** to save the Private endpoint configuration.

- After entering the remaining information in the other tabs, select **Review + create** to deploy the Azure Database for MySQL Flexible Server instance.

> [!NOTE]  
> In some cases, the Azure Database for MySQL Flexible Server instance and the virtual network subnet are in different subscriptions. In these cases, you must ensure the following configurations:
>
> - Make sure that both subscriptions have the **Microsoft.DBforMySQL/flexibleServer** resource provider registered. For more information, see [resource-manager-registration](/azure/azure-resource-manager/management/resource-providers-and-types).

## Manage private endpoints on Azure Database for MySQL Flexible Server via the Networking tab

1. Navigate to your Azure Database for MySQL Flexible Server resource in the Azure portal.

1. Go to the **Networking** section under **Settings**.

1. In the **Private endpoint** section, you can manage your private endpoints (Add, Approve, Reject, or Delete).

   :::image type="content" source="media/how-to-networking-private-link-portal/networking-private-link-portal-mysql.png" alt-text="Screenshot of networking private link portal page." lightbox="media/how-to-networking-private-link-portal/networking-private-link-portal-mysql.png":::

### Connect to a VM using Remote Desktop (RDP)

Connect to the created VM from the internet:

1. In the portal's search bar, enter *myVm*.

1. Select the **Connect** button. After selecting the **Connect** button, **Connect to virtual machine** opens.

1. Select **Download RDP File**. Azure creates a Remote Desktop Protocol (*.rdp*) file and downloads it to your computer.

1. Open the *downloaded.rdp* file.

   1. If prompted, select **Connect**.

   1. Enter the username and password you specified when creating the VM.

   > [!NOTE]  
   > You might need to select **More choices** > **Use a different account** to specify the credentials you entered when you created the VM.

1. Select **OK**.

1. You might receive a certificate warning during the sign-in process. Select **Yes** or **Continue** if you receive a certificate warning.

1. Once the VM desktop appears, minimize it to go back to your local desktop.

### Access the Azure Database for MySQL Flexible Server instance privately from the VM

1. In the Remote Desktop of *myVM*, open PowerShell.

1. Enter `nslookup myServer.privatelink.mysql.database.azure.com`.

   ```output
   Server: UnKnown
   Address: 168.63.129.16
   Non-authoritative answer:
   Name: myServer.privatelink.mysql.database.azure.com
   Address: 10.x.x.x
   ```

   > [!NOTE]  
   > Regardless of the firewall settings or public access being disabled, the ping and telnet tests verify network connectivity.

1. Test the private link connection for the Azure Database for MySQL Flexible Server instance using any available client. The following example uses [MySQL Workbench](https://dev.mysql.com/doc/workbench/en/wb-installing-windows.html) to do the operation.

1. In **New connection**, then select this information:
1. Select Connect.
1. Browse databases from the left menu.
1. (Optionally) Create or query information from the Azure Database for MySQL Flexible Server instance.
1. Close the remote desktop connection to *myVm*.

### Clean up resources

When you're done using the private endpoint, Azure Database for MySQL Flexible Server instance, and the VM, delete the resource group and all of the resources it contains:

1. Enter *myResourceGroup* in the **Search** box at the top of the portal and select *myResourceGroup* from the search results.
1. Select **Delete resource group**.
1. Enter myResourceGroup for **TYPE THE RESOURCE GROUP NAME** and select **Delete**.

## Create a private endpoint via Private Link Center

In this section, you learn how to add a private endpoint to the Azure Database for MySQL Flexible Server instance.

1. In the Azure portal, select **Create a resource** > **Networking** > **Private Link**.
1. In **Private Link Center - Overview**, select the option to **Create private endpoint**.

   :::image type="content" source="media/how-to-networking-private-link-portal/networking-private-link-center portal-mysql.png" alt-text="Screenshot of private link center portal page." lightbox="media/how-to-networking-private-link-portal/networking-private-link-center portal-mysql.png":::

1. In **Create a private endpoint - Basics**, then select the **Project details** information:
1. Select **Next: Resource**, then select this information:
1. Select **Next: Virtual Network**, then select the **Networking** information:
1. Select **Next: DNS**, then select the **PRIVATE DNS INTEGRATION** information:
1. Select **Review + create**. You're taken to the **Review + create** page, where Azure validates your configuration.
1. When you see the **Validation passed** message, select **Create**.

> [!NOTE]  
> The FQDN in the customer's DNS setting doesn't resolve the private IP configured. You must set up a DNS zone for the [configured FQDN](/azure/dns/dns-operations-recordsets-portal).

## Related content

- [Create and manage Private Link for Azure Database for MySQL - Flexible Server using Azure CLI](how-to-networking-private-link-azure-cli.md)
- [manage connectivity](concepts-networking.md)
- [add another layer of encryption to Azure Database for MySQL Flexible Server using Customer Managed Keys](security-customer-managed-key.md)
- [Microsoft Entra authentication for Azure Database for MySQL - Flexible Server](security-entra-authentication.md)
