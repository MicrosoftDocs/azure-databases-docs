---
title: Redeploy SSIS Packages to SQL Single Database
titleSuffix: Azure Database Migration Service
description: Learn how to migrate or redeploy SQL Server Integration Services packages and projects to Azure SQL Database single database using the Azure Database Migration Service and Data Migration Assistant.
author: abhims14
ms.author: abhishekum
ms.reviewer: randolphwest
ms.date: 10/28/2025
ms.service: azure-database-migration-service
ms.topic: how-to
ms.collection:
  - sql-migration-content
ms.custom:
  - sfi-image-nochange
---

# Redeploy SSIS packages to Azure SQL Database with Azure Database Migration Service

[!INCLUDE [deprecation-announcement-dms-classic-sql](includes/deprecation-announcement-dms-classic-sql.md)]

If you use SQL Server Integration Services (SSIS) and want to migrate your SSIS projects/packages from the source SSISDB hosted by SQL Server to the destination SSISDB hosted by Azure SQL Database, you can redeploy them using the Integration Services Deployment Wizard. You can launch the wizard from within SQL Server Management Studio (SSMS).

If the version of SSIS you use is earlier than 2012, before redeploying your SSIS projects/packages into the project deployment model, you first need to convert them by using the Integration Services Project Conversion Wizard, which can also be launched from SSMS. For more information, see the article [Converting projects to the project deployment model](/sql/integration-services/packages/deploy-integration-services-ssis-projects-and-packages#convert).

> [!NOTE]  
> The Azure Database Migration Service (DMS) currently doesn't support the migration of a source SSISDB to Azure SQL Database, but you can redeploy your SSIS projects/packages using the following process.

In this article, you learn how to:

> [!div class="checklist"]
> - Assess source SSIS projects/packages.
> - Migrate SSIS projects/packages to Azure.

## Prerequisites

To complete these steps, you need:

- SSMS version 17.2 or later.

- An instance of your target database server to host SSISDB. If you don't already have one, create a [logical SQL server](/azure/azure-sql/database/logical-servers) (without a database) using the Azure portal by navigating to the SQL Server (logical server only) [form](https://portal.azure.com/#create/Microsoft.SQLServer).

- SSIS must be provisioned in Azure Data Factory (ADF) containing Azure-SSIS Integration Runtime (IR) with the destination SSISDB hosted by SQL Database (as described in the article [Provision the Azure-SSIS Integration Runtime in Azure Data Factory](/azure/data-factory/tutorial-deploy-ssis-packages-azure)).

## Assess source SSIS projects/packages

Your SSIS projects/packages are assessed/validated as they're redeployed to the destination SSISDB hosted by Azure SQL Database.

## Migrate SSIS projects/packages

To migrate SSIS projects/packages to Azure SQL Database, perform the following steps.

1. Open SSMS, and then select **Options** to display the **Connect to Server** dialog box.

1. On the **Login** tab, specify the information necessary to connect to the server that will host the destination SSISDB.

   :::image type="content" source="media/how-to-migrate-ssis-packages/dms-ssis-login-tab.png" alt-text="Screenshot of SSIS Login tab.":::

1. On the **Connection Properties** tab, in the **Connect to database** text box, select or enter **SSISDB**, and then select **Connect**.

   :::image type="content" source="media/how-to-migrate-ssis-packages/dms-ssis-conncetion-properties-tab.png" alt-text="Screenshot of SSIS Connection Properties tab.":::

1. In the SSMS Object Explorer, expand the **Integration Services Catalogs** node, expand **SSISDB**, and if there are no existing folders, then right-click **SSISDB** and create a new folder.

1. Under **SSISDB**, expand any folder, right-click **Projects**, and then select **Deploy Project**.

   :::image type="content" source="media/how-to-migrate-ssis-packages/dms-ssis-ssisdb-node-expanded.png" alt-text="Screenshot of SSIS SSISDB node expanded.":::

1. In the Integration Services Deployment Wizard, on the **Introduction** page, review the information, and then select **Next**.

   :::image type="content" source="media/how-to-migrate-ssis-packages/dms-deployment-wizard-introduction-page.png" alt-text="Screenshot of Deployment Wizard Introduction page.":::

1. On the **Select Source** page, specify the existing SSIS project that you want to deploy.

   If SSMS is also connected to the SQL Server hosting the source SSISDB, select **Integration Services catalog**, and then enter the server name and project path in your catalog to deploy your project directly.

   Alternately, select **Project deployment file**, and then specify the path to an existing project deployment file (.ispac) to deploy your project.

   :::image type="content" source="media/how-to-migrate-ssis-packages/dms-deployment-wizard-select-source-page.png" alt-text="Screenshot of Deployment Wizard Select Source page." lightbox="media/how-to-migrate-ssis-packages/dms-deployment-wizard-select-source-page.png":::

1. Select **Next**.

1. On the **Select Destination** page, specify the destination for your project.

   1. In the Server name text box, enter the fully qualified server name (<server_name>.database.windows.net).

   1. Provide the authentication information, and then select **Connect**.

      :::image type="content" source="media/how-to-migrate-ssis-packages/dms-deployment-wizard-select-destination-page.png" alt-text="Screenshot of Deployment Wizard Select Destination page." lightbox="media/how-to-migrate-ssis-packages/dms-deployment-wizard-select-destination-page.png":::

   1. Select **Browse** to specify the destination folder in SSISDB, and then select **Next**.

   > [!NOTE]  
   > The **Next** button is enabled only after you select **Connect**.

1. On the **Validate** page, view any errors/warnings, and then if necessary, modify your packages accordingly.

   :::image type="content" source="media/how-to-migrate-ssis-packages/dms-deployment-wizard-validate-page.png" alt-text="Screenshot of Deployment Wizard Validate page.":::

1. Select **Next**.

1. On the **Review** page, review your deployment settings.

   > [!NOTE]  
   > You can change your settings by selecting **Previous** or by selecting any of the step links in the left pane.

1. Select **Deploy** to start the deployment process.

1. After the deployment process is completed, you can view the Results page, which displays the success or failure of each deployment action.

   1. If any action failed, in the **Result** column, select **Failed** to display an explanation of the error.

   1. Optionally, select **Save Report** to save the results to an XML file.

1. Select **Close** to exit the Integration Services Deployment Wizard.

If the deployment of your project succeeds without failure, you can select any packages it contains to run on your Azure-SSIS IR.

## Related content

- [Database Migration Guide](/data-migration/)
