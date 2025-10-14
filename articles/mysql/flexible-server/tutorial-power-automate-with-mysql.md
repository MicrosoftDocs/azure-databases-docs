---
title: Create a Power Automate Flow
description: Create a Power Automate flow with Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom: sfi-image-nochange
---

# Tutorial: Create a Power Automate flow app with Azure Database for MySQL - Flexible Server

Power Automate is a service that helps you create automated workflows between your favorite apps and services to synchronize files, get notifications, collect data, and more. Here are a few examples of what you can do with Power Automate.

- Automate business processes
- Move business data between systems on a schedule
- Connect to more than 500 data sources or any publicly available API
- Perform CRUD (create, read, update, delete) operations on data

This quickstart shows how to create an automated workflow using Power automate flow with [Azure Database for MySQL Flexible Server connector (Preview)](/connectors/azuremysql/).

## Prerequisites

- An account on [make.powerautomate.com](https://make.powerautomate.com).

- An Azure account and subscription. If you don't have a subscription, [sign up for a free Azure account](https://azure.microsoft.com/free).

- Create an Azure Database for MySQL Flexible Server instance using [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md) <br/> or [Quickstart: Create an instance of Azure Database for MySQL - Flexible Server by using the Azure CLI](quickstart-create-server-cli.md) if you don't have one.
- Populate the Azure Database for MySQL Flexible Server database with this [sample data](https://raw.githubusercontent.com/Azure-Samples/mysql-database-samples/main/mysqltutorial.org/mysql-classicmodesl.sql).

[Having issues? Let us know.](https://github.com/MicrosoftDocs/azure-docs/issues)

## Overview of cloud flows

Create a cloud flow when you want your automation to be triggered either automatically, instantly, or via a schedule. Here are types of flows you can create and then use with Azure Database for MySQL Flexible Server connector.

| **Flow type** | **Use case** | **Automation target** |
| --- | --- | --- |
| Automated cloud flows | Create an automation that is triggered by an event such as arrival of an email from a specific person, or a mention of your company in social media. | Connectors for cloud or on-premises services connect your accounts and enable them to talk to each other. |
| Instant cloud flows | Start an automation with a select of a button. You can automate for repetitive tasks from your Desktop or Mobile devices. For example, instantly send a reminder to the team with a push of a button from your mobile device. | Wide range of tasks such as requesting an approval, an action in Teams or SharePoint. |
| Scheduled flows | Schedule an automation such as daily data upload to SharePoint or a database. | Tasks that need to be automated on a schedule. |

For this tutorial, we'll use **instant cloud flow** that can be triggered manually from any device, easy-to-share instant flows automate tasks so you don't have to repeat yourself.

## Specify an event to start the flow

Follow the steps to create an instant cloud flow with a manual trigger.

1. In [Power Automate](https://make.powerautomate.com), select **Create** from the navigation bar on the left.
1. Under **Start from blank*, select **Instant cloud flow**.
1. Give your flow a name in the **Flow name" field and select **Manually trigger a flow**.

   :::image type="content" source="media/tutorial-power-automate-with-mysql/create-instant-cloud-flow.png" alt-text="Screenshot that shows how to create instant cloud flow app." lightbox="media/tutorial-power-automate-with-mysql/create-instant-cloud-flow.png":::

1. Select the **Create** button at the bottom of the screen.

## Create a MySQL operation

An operation is an action. Power Automate flow allows you to add one or more advanced options and multiple actions for the same trigger. For example, add an advanced option that sends an email message as high priority. In addition to sending mail when an item is added to a list created in Microsoft Lists, create a file in Dropbox that contains the same information.

1. Once the flow app is created, select **Next Step** to create an operation.
1. In the box that shows Search connectors and actions, enter **Azure Database for MySQL**.
1. Select **Azure Database for MySQL** connector and then select **Get Rows** operation. Get rows operation allows you to get all the rows from a table or query.

   :::image type="content" source="media/tutorial-power-automate-with-mysql/azure-mysql-connector-add-action.png" alt-text="Screenshot that shows how to view all the actions for Azure Database for MySQL Flexible Server connector.":::

1. Add a new Azure Database for MySQL Flexible Server connection and enter the **authentication type**,**server name**, **database name**, **username**, **password**. Select **encrypt connection** if SSL is enabled on your MySQL server.

   :::image type="content" source="media/tutorial-power-automate-with-mysql/add-mysql-connection-information.png" alt-text="Screenshot of adding a new MySQL connection for Azure Database for MySQL Flexible Server.":::

   > [!NOTE]  
   > If you get an error **Test connection failed. Details: Authentication to host `'servername'` for user `'username'` using method 'mysql_native_password' failed with message: Access denied for user `'username'@'IP address'`(using password: YES)**, please update the firewall rules on the Azure Database for MySQL Flexible Server instance in the [Azure protal](https://portal.azure.com) with this IP address.

1. After the connection is successfully added, provide the **servername, database name and table name** parameters for **Get Rows** operation using the newly added connection. Select **advanced options** to add more filters or limit the number of rows returned.

   :::image type="content" source="media/tutorial-power-automate-with-mysql/get-rows-from-table.png" alt-text="Screenshot that shows configuring Get Rows operation.":::

1. Select **Save**.

## Test and run your flow

After saving the flow, we need to test it and run the flow app.

1. Select **Flow checker** to see if there are any errors that need to be resolved.
1. Select **Test** and then select **Manually** to test the trigger.
1. Select **Run flow**.
1. When the flow is successfully executed, you can select **click to download** in the output section to see the JSON response received.

   :::image type="content" source="media/tutorial-power-automate-with-mysql/run-flow-to-get-rows-from-table.png" alt-text="Screenshot that shows output of the run.":::

## Triggers

Azure Database for MySQL Flexible Server connector supports triggers for when an item is created in Azure Database for MySQL Flexible Server or when an item is modified. A trigger is just an event that starts a cloud flow. Before using triggers, make sure your table schema has "created_at" and "updated_at" columns which are of type timestamp. The trigger use these columns to understand when a new item was create or modified and initiate the automated flow.

| Trigger | Description |
| --- | --- |
| [When an item is created](/connectors/azuremysql/#when-an-item-is-created) | Triggers a flow when an item is created in Azure Database for MySQL Flexible Server (Available only for Power Automate.) |
| [When an item is modified](/connectors/azuremysql/#when-an-item-is-modified) | Triggers a flow when an item is modified in Azure Database for MySQL Flexible Server. (Available only for Power Automate.) |

## Next step

> [!div class="nextstepaction"]
> [Azure Database for MySQL Flexible Server connector](/connectors/azuremysql/)
