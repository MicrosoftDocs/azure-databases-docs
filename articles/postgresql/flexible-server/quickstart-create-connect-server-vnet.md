---
title: Connect with private access in the Azure portal
description: This article shows how to create and connect to Azure Database for PostgreSQL flexible server with private access or virtual network using the Azure portal.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom:
  - mvc
  - mode-ui
  - linux-related-content
---

# Connect Azure Database for PostgreSQL flexible server with the private access connectivity method

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL flexible server is a managed service that you can use to run, manage, and scale highly available PostgreSQL servers in the cloud. This quickstart shows you how to create an Azure Database for PostgreSQL flexible server instance in a virtual network by using the Azure portal.



If you don't have an Azure subscription, create a [free Azure account](https://azure.microsoft.com/free/) before you begin.

## Sign in to the Azure portal

Sign in to the [Azure portal](https://portal.azure.com). Enter your credentials to sign in to the portal. The default view is your service dashboard.

## Create an Azure Database for PostgreSQL flexible server

You create an Azure Database for PostgreSQL flexible server instance with a defined set of [compute and storage resources](concepts-compute.md). You create the server within an [Azure resource group](/azure/azure-resource-manager/management/overview).

Complete these steps to create an Azure Database for PostgreSQL flexible server instance:

1. Search for and select **Azure Database for PostgreSQL servers** in the portal:

   :::image type="content" source="./media/quickstart-create-connect-server-vnet/search-flexible-server-in-portal.png" alt-text="Screenshot that shows a search for Azure Database for PostgreSQL servers." lightbox="./media/quickstart-create-connect-server-vnet/search-flexible-server-in-portal.png":::

2. Select **Add**.

<!-- This no longer happens. 3. On the **Select Azure Database for PostgreSQL deployment option** page, select **Flexible server** as the deployment option:

    :::image type="content" source="./media/quickstart-create-connect-server-vnet/deployment-option.png" alt-text="Screenshot that shows the Flexible server option." lightbox="./media/quickstart-create-connect-server-vnet/deployment-option.png":::
-->
4. On the **Basics** tab, enter the **subscription**, **resource group**, **region**, and **server name**.  With the default values, this will provision an Azure Database for PostgreSQL flexible server instance of version 12 with General purpose pricing tier  using 2 vCores, 8 GiB RAM, and 28 GiB storage. The backup retention is **seven** days. You can use **Development** workload to default to a lower-cost pricing tier.

    :::image type="content" source="./media/quickstart-create-connect-server-vnet/postgres-create-basics.png" alt-text="Screenshot that shows the Basics tab of the Azure Database for PostgreSQL flexible server page." lightbox="./media/quickstart-create-connect-server-vnet/postgres-create-basics.png":::

5. In the **Basics** tab, enter  a unique **admin username** and **admin password**.

    :::image type="content" source="./media/quickstart-create-connect-server-vnet/db-administrator-account.png" alt-text="Screenshot that shows the admin user information page." lightbox="./media/quickstart-create-connect-server-vnet/db-administrator-account.png":::

6.  Go to the **Networking** tab, and select **private access**. You can't change the connectivity method after you create the server. Select **Create virtual network** to create a new  virtual network **vnetenvironment1**. Select **OK** once you have provided the virtual network name and subnet information.

    :::image type="content" source="./media/quickstart-create-connect-server-vnet/create-new-vnet-for-postgres-server.png" alt-text="Screenshot that shows the Networking tab with new VNET." lightbox="./media/quickstart-create-connect-server-vnet/create-new-vnet-for-postgres-server.png":::

7. Select **Review + create** to review your Azure Database for PostgreSQL flexible server configuration.

8. Select **Create** to provision the server. Provisioning can take a few minutes.

9. Wait until the deployment is complete and successful.

   :::image type="content" source="./media/quickstart-create-connect-server-vnet/deployment-success.png" alt-text="Screenshot that shows deployment success." lightbox="./media/quickstart-create-connect-server-vnet/deployment-success.png":::

9.  Select **Go to resource** to view the server's **Overview** page.

## Create an Azure Linux virtual machine

Since the server is in a virtual network, you can only connect to the server from other Azure services in the same virtual network as the server. To connect and manage the server, let's create a Linux virtual machine. The virtual machine must be created in the **same region** and **same subscription**. The Linux virtual machine can be used as an SSH tunnel to manage your Azure Database for PostgreSQL flexible server instance. 

1. Go to your resource group in which the server was created. Select **Add**.
2. Select **Ubuntu Server 18.04 LTS**.
3. In the **Basics** tab, under **Project details**, make sure the correct subscription is selected and then choose to **Create new** resource group. Type *myResourceGroup* for the name.

   :::image type="content" source="~/reusable-content/ce-skilling/azure/media/virtual-machines/project-details.png" alt-text="Screenshot of the Project details section showing where you select the Azure subscription and the resource group for the virtual machine." lightbox="~/reusable-content/ce-skilling/azure/media/virtual-machines/project-details.png"::: 

2. Under **Instance details**, type *myVM* for the **Virtual machine name**, and choose the same **Region** as your Azure Database for PostgreSQL flexible server instance.

   :::image type="content" source="~/reusable-content/ce-skilling/azure/media/virtual-machines/instance-details.png" alt-text="Screenshot of the Instance details section where you provide a name for the virtual machine and select its region, image and size." lightbox="~/reusable-content/ce-skilling/azure/media/virtual-machines/instance-details.png":::

3. Under **Administrator account**, select **SSH public key**.

4. In **Username** type *azureuser*.

5. For **SSH public key source**, leave the default of **Generate new key pair**, and then type *myKey* for the **Key pair name**.

   :::image type="content" source="~/reusable-content/ce-skilling/azure/media/virtual-machines/administrator-account.png" alt-text="Screenshot of the Administrator account section where you select an authentication type and provide the administrator credentials." lightbox="~/reusable-content/ce-skilling/azure/media/virtual-machines/administrator-account.png":::

6. Under **Inbound port rules** > **Public inbound ports**, choose **Allow selected ports** and then select **SSH (22)** and **HTTP (80)** from the drop-down.

   :::image type="content" source="~/reusable-content/ce-skilling/azure/media/virtual-machines/inbound-port-rules.png" alt-text="Screenshot of the inbound port rules section where you select what ports inbound connections are allowed on." lightbox="~/reusable-content/ce-skilling/azure/media/virtual-machines/inbound-port-rules.png":::

7. Select the **Networking** page to configure the virtual network. For the virtual network, choose the **vnetenvironment1** created for the database server.

   :::image type="content" source="./media/quickstart-create-connect-server-vnet/vm-vnet-configuration.png" alt-text="Screenshot of select existing virtual network of the database server." lightbox="./media/quickstart-create-connect-server-vnet/vm-vnet-configuration.png":::

8. Select **Manage subnet configuration** to create a new subnet for the server.

    :::image type="content" source="./media/quickstart-create-connect-server-vnet/vm-manage-subnet-integration.png" alt-text="Screenshot of manage subnet." lightbox="./media/quickstart-create-connect-server-vnet/vm-manage-subnet-integration.png":::

9. Add the new subnet for the virtual machine.

    :::image type="content" source="./media/quickstart-create-connect-server-vnet/vm-add-new-subnet.png" alt-text="Screenshot of adding a new subnet for virtual machine." lightbox="./media/quickstart-create-connect-server-vnet/vm-add-new-subnet.png"::: 

10. After the subnet has been created successfully, close the page.

    :::image type="content" source="./media/quickstart-create-connect-server-vnet/subnet-create-success.png" alt-text="Screenshot of success with adding a new subnet for virtual machine." lightbox="./media/quickstart-create-connect-server-vnet/subnet-create-success.png":::

11. Select **Review + Create**.
12. Select **Create**. When the **Generate new key pair** window opens, select **Download private key and create resource**. Your key file will be downloaded as **myKey.pem**.

    >[!IMPORTANT]
    > Make sure you know where the `.pem` file was downloaded. You will need the path to it in the next step.

13. When the deployment is finished, select **Go to resource** to view the virtual machine **Overview** page.

14. Select the public IP address and copy it to your clipboard.

    :::image type="content" source="~/reusable-content/ce-skilling/azure/media/virtual-machines/ip-address.png" alt-text="Screenshot showing how to copy the IP address for the virtual machine." lightbox="~/reusable-content/ce-skilling/azure/media/virtual-machines/ip-address.png":::

## Install PostgreSQL client tools

Create an SSH connection with the VM using Bash or PowerShell. At your prompt, open an SSH connection to your virtual machine. Replace the IP address with the one from your VM, and replace the path to the `.pem` with the path to where the key file was downloaded.

```console
ssh -i .\Downloads\myKey1.pem azureuser@10.111.12.123
```

> [!TIP]
> The SSH key you created can be used the next time you create a VM in Azure. Just select the **Use a key stored in Azure** for **SSH public key source** the next time you create a VM. You already have the private key on your computer, so you won't need to download anything.

You need to install the postgresql-client tool to be able to connect to the server.

```bash
sudo apt-get update
sudo apt-get install postgresql-client
```

Connections to the database are enforced with SSL, hence you need to download the public SSL certificate.

```bash
wget --no-check-certificate https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem
```

## Connect to the server from Azure Linux virtual machine
With the **psql** client tool installed, we can now connect to the server from your local environment.

```bash
psql --host=mydemoserver-pg.postgres.database.azure.com --port=5432 --username=myadmin --dbname=postgres --set=sslmode=require --set=sslrootcert=DigiCertGlobalRootCA.crt.pem
```

## Clean up resources
You have now created an Azure Database for PostgreSQL flexible server instance in a resource group. If you don't expect to need these resources in the future, you can delete them by deleting the resource group, or you can just delete the Azure Database for PostgreSQL flexible server instance. To delete the resource group, complete the following steps:

1. In the Azure portal, search for and select **Resource groups**.
1. In the list of resource groups, select the name of your resource group.
1. In the **Overview** page for your resource group, select **Delete resource group**.
1. In the confirmation dialog box, type the name of your resource group, and then select **Delete**.

## Related content

- [Manage Azure Database for PostgreSQL flexible server](how-to-manage-server-portal.md).
- [Quickstart: Use Python to connect and query data from an Azure Database for PostgreSQL flexible server](connect-python.md).
- [Quickstart: Use Java to connect and query data from an Azure Database for PostgreSQL flexible server](connect-java.md).
- [Quickstart: Use .NET (C#) to connect and query data from an Azure Database for PostgreSQL flexible server](connect-csharp.md).
- [Quickstart: Use Go language to connect and query data from an Azure Database for PostgreSQL flexible server](connect-go.md).
- [Quickstart: Use PHP to connect and query data from an Azure Database for PostgreSQL flexible server](connect-php.md).
- [Quickstart: Use Azure CLI to connect and query data from an Azure Database for PostgreSQL flexible server](connect-azure-cli.md).
- [Quickstart: Import data from Azure Database for PostgreSQL flexible server in Power BI](connect-with-power-bi-desktop.md).
