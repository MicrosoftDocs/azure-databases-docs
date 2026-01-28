---
title: Stop/start automation tasks
description: This article describes how to stop/start an Azure Database for PostgreSQL flexible server instance by using automation tasks.
author: danyal-bukhari # GitHub alias
ms.author: dabukhari # Microsoft alias
ms.reviewer: maghan
ms.date: 10/13/2024
ms.service: azure-database-postgresql
ms.subservice: data-movement
ms.topic: quickstart
---

# Quickstart: Manage Azure Database for PostgreSQL  using automation tasks

> [!NOTE]
> If a free trial is available, you can find more information about it [here](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

You can create automation tasks for your Azure Database for PostgreSQL flexible server instance to start or stop the server on a predefined schedule. Set the Interval and Frequency values on the task's Configure tab to automatically start or stop the server a specific number of times every day, week, or month. The automation task continues to work until you delete or disable the task.

You can also set up automation tasks for other routine tasks such as 'Send monthly cost for resource' and 'Scale Azure Database for PostgreSQL'.

## How do automation tasks differ from Azure Automation?

Automation tasks are more basic and lightweight than [Azure Automation](/azure/automation/overview). You can only create an automation task at the Azure resource level. An automation task is a logic app resource that runs a workflow powered by the [multitenant Azure Logic Apps service](/azure/logic-apps/logic-apps-overview). You can view and edit the underlying workflow by opening the task in the workflow designer after it has completed at least one run.

In contrast, Azure Automation is a comprehensive cloud-based automation and configuration service providing consistent management across Azure and non-Azure environments.

## Pricing

Creating an automation task doesn't immediately incur charges. Underneath, an automation task is powered by a workflow in a logic app resource hosted in multitenant Azure Logic Apps; thus, the [Consumption pricing model](/azure/logic-apps/logic-apps-pricing) applies to automation tasks. Metering and billing are based on the trigger and action executions in the underlying logic app workflow.

## Prerequisites

- An Azure account and subscription.
- An Azure Database for PostgreSQL flexible server instance you want to manage.

## Create an automation task to stop the server

1. In the [Azure portal](https://portal.azure.com), find the Azure Database for PostgreSQL flexible server resource you want to manage.
1. On the resource navigation menu, in the **Automation** section, select **Tasks**.
:::image type="content" source="media/create-automation-tasks/azure-postgres-menu-automation-section.png" alt-text="Screenshot showing Azure portal and Azure Database for PostgreSQL flexible server resource menu with 'Tasks' selected." lightbox="media/create-automation-tasks/azure-postgres-menu-automation-section.png":::

1. On the **Tasks** pane, select **Add a task** to select a task template.
:::image type="content" source="media/create-automation-tasks/add-automation-task.png" alt-text="Screenshot that shows the 'Tasks' pane with 'Add a task' selected." lightbox="media/create-automation-tasks/add-automation-task.png":::

1. Under **Select a template**, select the task for stopping your Azure Database for PostgreSQL flexible server instance.
:::image type="content" source="media/create-automation-tasks/select-task-template.png" alt-text="Screenshot that shows the 'Add a task' pane with 'Stop PostgreSQL flexible server' template selected." lightbox="media/create-automation-tasks/select-task-template.png":::

1. Under **Authenticate**, in the **Connections** section, select **Create** for every connection that appears in the task so that you can provide authentication credentials for all the connections. The types of connections in each task vary based on the task.
:::image type="content" source="media/create-automation-tasks/create-authenticate-connections.png" alt-text="Screenshot that shows the selected 'Create' option for the Azure Resource Manager connection." lightbox="media/create-automation-tasks/create-authenticate-connections.png":::

1. When prompted, **sign in with your Azure account** credentials.
:::image type="content" source="media/create-automation-tasks/create-connection-sign-in.png" alt-text="Screenshot that shows the selection, 'Sign in'.":::

1. Each successfully authenticated connection looks similar to this example:
:::image type="content" source="media/create-automation-tasks/create-connection-success.png" alt-text="Screenshot that shows successfully created connection." lightbox="media/create-automation-tasks/create-connection-success.png":::

1. After you authenticate all the connections, select Next: **Configure**.

1. Under **Configure**, provide a name for the task and any other information required. When you're done, select **Review + create**.
:::image type="content" source="media/create-automation-tasks/provide-task-information.png" alt-text="Screenshot that shows the required information for the selected task." lightbox="media/create-automation-tasks/provide-task-information.png":::

1. Tasks that send email notifications require an email address.

> [!NOTE]
> You can't change the task name after creation, so consider a name that still applies if you edit the underlying workflow. Changes you make to the underlying workflow apply only to the task you created, not the task template.
>  
> For example, if you name your task `Stop-Instance-Weekly` but later edit the underlying workflow to run daily, you can't change it to `Stop-Instance-Daily`.

The task you've created, which is automatically live and running, appears on the **Tasks** list.

:::image type="content" source="media/create-automation-tasks/automation-tasks-list.png" alt-text="Screenshot that shows the automation tasks list." lightbox="media/create-automation-tasks/automation-tasks-list.png":::

## Create an automation task to start the server

You can apply the same steps outlined above to create separate automation tasks for starting the Azure Database for PostgreSQL flexible server instance at a specific time. Here's how:

1. Follow the steps outlined in the "Create an automation task" section until you reach the "Select a template" stage.
1. Here, instead of selecting the "Stop PostgreSQL flexible server" task, select the template for "Start PostgreSQL flexible server."
1. Proceed to fill in the rest of the required details as described in the subsequent steps, defining the specific schedule at which you want the server to start in the 'Configure' section.

## Review task history

To view a task's history of runs along with their status:

1. In the [Azure portal](https://portal.azure.com), find the Azure Database for PostgreSQL flexible server resource you want to manage.
1. On the resource navigation menu, in the **Automation** section, select **Tasks**.
1. find the task you want to review in the tasks list. In that task's **Runs** column, select **View**.

Here are the possible statuses for a run:

 | Status | Description |
 | --- | --- |
 | **Canceled** | The task was canceled while running. |
 | **Failed** | The task has at least one failed action, but no subsequent actions exist to handle the failure. |
 | **Running** | The task is currently running. |
 | **Succeeded** | All actions succeeded. A task can still finish successfully if an action fails, but a subsequent action exists to handle the failure. |
 | **Waiting** | The run hasn't started yet and is paused because an earlier task instance is still running. |

 For more information, see [Review runs history in monitoring view](/azure/logic-apps/monitor-logic-apps#review-runs-history).

## Edit the task

To change a task, you have these options:

Edit the task "inline" to change its properties, such as connection information or configuration information, such as your email address.
- Edit the task's underlying workflow in the workflow designer.

### Edit the task inline

1. In the [Azure portal](https://portal.azure.com), find the Azure Database for PostgreSQL flexible server resource you want to manage.
1. On the resource navigation menu, in the **Automation** section, select **Tasks**.
1. find the task you want to update in the tasks list. Open the task's ellipses (**...**) menu, and select **Edit inline**.
1. By default, the **Authenticate** tab shows existing connections.
1. To add new authentication credentials or select different existing authentication credentials for a connection, open the connection's ellipses (**...**) menu and select either **Add new connection** or, if available, different authentication credentials.
1. To update other task properties, select **Next: Configure**.
1. When you're done, select **Save**

### Edit the task's underlying workflow

- For details on editing the underlying workflow, refer to [Edit the task's underlying workflow](/azure/logic-apps/create-automation-tasks-azure-resources#edit-the-tasks-underlying-workflow)

## Related content

- [Manage logic apps in the Azure portal](/azure/logic-apps/manage-logic-apps-with-azure-portal).
