---
title: Connect With Private Access in the Azure Portal
description: This article walks you through using the Azure portal to create and connect to an Azure Database for MySQL - Flexible Server instance with private access.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom:
  - mvc
  - mode-ui
  - linux-related-content
---

# Connect Azure Database for MySQL - Flexible Server with private access connectivity method

Azure Database for MySQL Flexible Server is a managed service that runs, manages, and scales highly available MySQL servers in the cloud. This quickstart shows you how to create an Azure Database for MySQL Flexible Server instance in a virtual network by using the Azure portal.

[!INCLUDE [flexible-server-free-trial-note](../includes/flexible-server-free-trial-note.md)]

## Sign in to the Azure portal

Sign in to the [Azure portal](https://portal.azure.com). Enter your credentials to sign in to the portal. The default view is your service dashboard.

## Create an Azure Database for MySQL Flexible Server instance

You create an Azure Database for MySQL Flexible Server instance with a defined set of [compute and storage resources](./concepts-compute-storage.md). You create the server within an [Azure resource group](/azure/azure-resource-manager/management/overview).

Complete these steps to create an Azure Database for MySQL Flexible Server instance:

1. Search for and select **Azure Database for MySQL servers** in the portal:

   :::image type="content" source="media/quickstart-create-connect-server-vnet/search-flexible-server-in-portal.png" alt-text="Screenshot that shows a search for Azure Database for MySQL servers." lightbox="media/quickstart-create-connect-server-vnet/search-flexible-server-in-portal.png":::

1. Select **Add**.

1. On the **Select Azure Database for MySQL deployment option** page, select **Flexible server** as the deployment option:

   :::image type="content" source="media/quickstart-create-connect-server-vnet/deployment-option.png" alt-text="Screenshot that shows the Flexible server option." lightbox="media/quickstart-create-connect-server-vnet/deployment-option.png":::

1. On the **Basics** tab, enter the **subscription**, **resource group** , **region**, **administrator username** and **administrator password**. With the default values, this provisions an Azure Database for MySQL Flexible Server instance of version 5.7 with Burstable Sku using 1 vCore, 2 GiB Memory, and 32 GiB storage. The backup retention is seven days. You can change the configuration.

   :::image type="content" source="media/quickstart-create-connect-server-vnet/mysql-flexible-server-create-portal.png" alt-text="Screenshot that shows the Basics tab of the Flexible server page." lightbox="media/quickstart-create-connect-server-vnet/mysql-flexible-server-create-portal.png":::

   > [!TIP]  
   > For faster data loads during migration, increasing the IOPS to the maximum size supported by computing the size and later scaling it back to save cost is recommended.

1. Go to the **Networking** tab, select **private access**.You can't change the connectivity method after you create the server. Select **Create virtual network** to create a new virtual network **vnetenvironment1**.

   :::image type="content" source="media/quickstart-create-connect-server-vnet/create-new-vnet-for-mysql-server.png" alt-text="Screenshot that shows the Networking tab with new VNET." lightbox="media/quickstart-create-connect-server-vnet/create-new-vnet-for-mysql-server.png":::

1. Select **OK** once you've provided the virtual network name and subnet information.

   :::image type="content" source="media/quickstart-create-connect-server-vnet/show-server-vnet-information.png" alt-text="Screenshot of Review VNET information." lightbox="media/quickstart-create-connect-server-vnet/show-server-vnet-information.png":::

1. Select **Review + create** to review your Azure Database for MySQL Flexible Server configuration.

1. Select **Create** to provision the server. Provisioning can take a few minutes.

1. Wait until the deployment is complete and successful.

   :::image type="content" source="media/quickstart-create-connect-server-vnet/deployment-success.png" alt-text="Screenshot that shows the Networking settings with new VNET." lightbox="media/quickstart-create-connect-server-vnet/deployment-success.png":::

1. Select **Go to resource** to view the server's **Overview** page opens.

## Create Azure Linux virtual machine

Since the server is in a virtual network, you can only connect to the server from other Azure services in the same virtual network as the server. To connect and manage the server, let's create a Linux virtual machine. The virtual machine must be created in the **same region** and **same subscription**. The Linux virtual machine can be used as SSH tunnel to manage your database server.

1. Go to your resource group in which the server was created. Select **Add**.
1. Select **Ubuntu Server 18.04 LTS**
1. In the **Basics** tab, under **Project details**, make sure the correct subscription is selected and then choose to **Create new** resource group. Type *myResourceGroup* for the name.

1. Under **Instance details**, type *myVM* for the **Virtual machine name**, choose the same **Region** as your database server.

1. Under **Administrator account**, select **SSH public key**.

1. In **Username** type *azureuser*.

1. For **SSH public key source**, leave the default of **Generate new key pair**, and then type *myKey* for the **Key pair name**.

1. Under **Inbound port rules** > **Public inbound ports**, choose **Allow selected ports** and then select **SSH (22)** and **HTTP (80)** from the dropdown list.

1. Select **Networking** page to configure the virtual network. For the virtual network, choose the **vnetenvironment1** created for the Azure Database for MySQL Flexible Server instance.

   :::image type="content" source="media/quickstart-create-connect-server-vnet/vm-vnet-configuration.png" alt-text="Screenshot of the select existing virtual network of the Azure Database for MySQL Flexible Server instance." lightbox="media/quickstart-create-connect-server-vnet/vm-vnet-configuration.png":::

1. Select **Manage subnet configuration** to create a new subnet for the server.

   :::image type="content" source="media/quickstart-create-connect-server-vnet/vm-manage-subnet-integration.png" alt-text="Screenshot of manage subnet." lightbox="media/quickstart-create-connect-server-vnet/vm-manage-subnet-integration.png":::

1. Add a new subnet for the virtual machine.

   :::image type="content" source="media/quickstart-create-connect-server-vnet/vm-add-new-subnet.png" alt-text="Screenshot of adding a new subnet for virtual machine." lightbox="media/quickstart-create-connect-server-vnet/vm-add-new-subnet.png":::

1. After the subnet has been created successfully, close the page.
   :::image type="content" source="media/quickstart-create-connect-server-vnet/subnetcreate-success.png" alt-text="Screenshot of success with adding a new subnet for virtual machine." lightbox="media/quickstart-create-connect-server-vnet/subnetcreate-success.png":::

1. Select **Review + Create**.
1. Select **Create**. When the **Generate new key pair** window opens, select **Download private key and create resource**. Your key file is downloaded as **myKey.pem**.

   > [!IMPORTANT]  
   > Make sure you know where the `.pem` file was downloaded, you need the path to it in the next step.

1. When the deployment is finished, select **Go to resource**.

   :::image type="content" source="media/quickstart-create-connect-server-vnet/vm-create-success.png" alt-text="Screenshot of deployment success." lightbox="media/quickstart-create-connect-server-vnet/vm-create-success.png":::

1. On the page for your new VM, select the public IP address and copy it to your clipboard.

## Install MySQL client tools

Create an SSH connection with the VM using Bash or PowerShell. At your prompt, open an SSH connection to your virtual machine. Replace the IP address with the one from your VM, and replace the path to the `.pem` with the path to where the key file was downloaded.

```console
ssh -i .\Downloads\myKey1.pem azureuser@10.111.12.123
```

   > [!TIP]  
   > The SSH key you created can be used the next time you create a VM in Azure. Select the **Use a key stored in Azure** for **SSH public key source** the next time you create a VM. You already have the private key on your computer, so you won't need to download anything.

You need to install mysql-client tool to connect to the server.

```bash
sudo apt-get update
sudo apt-get install mysql-client
```

Connections to the database are enforced with SSL; hence you need to download the public SSL certificate.

```bash
wget --no-check-certificate https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem
```

## Connect to the server from Azure Linux virtual machine

With the [mysql.exe](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) client tool installed, we can now connect to the server from your local environment.

```bash
mysql -h mydemoserver.mysql.database.azure.com -u mydemouser -p --ssl-mode=REQUIRED --ssl-ca=DigiCertGlobalRootCA.crt.pem
```

## Clean up resources

You've created an Azure Database for MySQL Flexible Server instance in a resource group. If you don't expect to need these resources in the future, you can delete them by deleting the resource group or the Azure Database for MySQL Flexible Server instance. To delete the resource group, complete these steps:

1. Search for and select **Resource groups**in the Azure portal.
1. In the list of resource groups, select the name of your resource group.
1. In the **Overview** page for your resource group, select **Delete resource group**.
1. In the confirmation dialog box, type the name of your resource group and then select **Delete**.

## Next step

> [!div class="nextstepaction"]
> [Tutorial: Build a PHP (Laravel) and Azure Database for MySQL - Flexible Server app on Azure App Service](tutorial-php-database-app.md)
