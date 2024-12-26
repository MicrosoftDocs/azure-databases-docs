---
title: Troubleshoot CLI Errors
description: This topic gives guidance on troubleshooting common issues with Azure CLI when using Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: troubleshooting
ms.custom:
  - devx-track-azurecli
---

# Troubleshoot Azure Database for MySQL - Flexible Server CLI errors

This article helps you troubleshoot common issues with Azure CLI when using Azure Database for MySQL flexible server.

## Command not found

If you receive an error that a command **is misspelled or not recognized by the system**, this could mean that CLI version on your client machine might not be up to date. Run `az upgrade` to upgrade to latest version. Doing an upgrade of your CLI version can help resolve issues with incompatibilities of a command due to any API changes.

## Debug deployment failures

Currently, Azure CLI doesn't support turning on debug logging, but you can retrieve debug logging by doing the following steps.

> [!NOTE]  
>  
> - Replace `examplegroup` and `exampledeployment` with the correct resource group and deployment name for your Azure Database for MySQL flexible server instance.
> - You can see the Deployment name in the deployments page in your resource group. See [how to find the deployment name](/azure/azure-resource-manager/templates/deployment-history?tabs=azure-portal).

1. List the deployments in resource group to identify the Azure Database for MySQL Flexible Server deployment.

    ```azurecli
    az deployment operation group list \
      --resource-group examplegroup \
      --name exampledeployment
    ```

1. Get the request content of the Azure Database for MySQL flexible server deployment.

    ```azurecli
    az deployment operation group list \
      --name exampledeployment \
      -g examplegroup \
      --query [].properties.request
    ```

1. Examine the response content.

    ```azurecli
    az deployment operation group list \
      --name exampledeployment \
      -g examplegroup \
      --query [].properties.response
    ```

## Error codes

| Error code | Mitigation |
| --- | --- |
| MissingSubscriptionRegistration | Register your subscription with the resource provider. Run the command `az provider register --namespace Microsoft.DBMySQL` to resolve the issue. |
| InternalServerError | Try to view the activity logs for your server to see if there's more information. Run the command `az monitor activity-log list --correlation-id <enter correlation-id>`. You can try the same CLI command after a few minutes. If the issue persists, [report it](https://github.com/Azure/azure-cli/issues) or reach out to Microsoft support. |
| ResourceNotFound | Resource being referenced can't be found. You can check resource properties, or check if the resource is deleted or in another subscription. |
| LocationNotAvailableForResourceType | - Check availability of Azure Database for MySQL flexible server in [Azure regions](https://azure.microsoft.com/global-infrastructure/services/?products=mysql).<br />- Check if the Azure Database for MySQL flexible server instance Resource types is registered with your subscription. |
| ResourceGroupBeingDeleted | Resource group is being deleted. Wait for deletion to complete. |
| PasswordTooLong | The provided password is too long. It must contain between 8 and 128 characters. Your password must contain characters from three of the following categories: English uppercase letters, English lowercase letters, numbers (0 through 9), and nonalphanumeric characters (!, $, #, %, etc.). |
| PasswordNotComplex | The provided password isn't complex enough. It must contain between 8 and 128 characters. Your password must contain characters from three of the following categories: English uppercase letters, English lowercase letters, numbers (0 through 9), and nonalphanumeric characters (!, $, #, %, etc.). |
| PasswordTooShort | It must contain between 8 and 128 characters. Your password must contain characters from three of the following categories: English uppercase letters, English lowercase letters, numbers (0 through 9), and nonalphanumeric characters (!, $, #, %, etc.). |
| SubscriptionNotFound | The requested subscription wasn't found. Run `az account list all` to see all your current subscriptions. |
| InvalidParameterValue | An invalid value was given to a parameter. Check the [CLI reference docs](/cli/azure/mysql/flexible-server) to see the correct values supported for the arguments. |
| InvalidLocation | An invalid location was specified. Check availability of Azure Database for MySQL flexible server in [Azure regions](https://azure.microsoft.com/global-infrastructure/services/?products=mysql) |
| InvalidServerName | Identified an invalid server name. Check the server name. Run the command [az mysql flexible-server list](/cli/azure/mysql/flexible-server#az-mysql-flexible-server-list) to see all list of Azure Database for MySQL flexible server instances available. |
| InvalidResourceIdSegment | A syntax error was identified in your Azure Resource Manager template. Use a JSON formatter tool to validate the JSON to identify the syntax error. |
| InvalidUserName | Enter a valid username. The admin user name can't be azure_superuser, azure_pg_admin, admin, administrator, root, guest, or public. It can't start with pg_. |
| BlockedUserName | The admin user name can't be azure_superuser, azure_pg_admin, admin, administrator, root, guest, or public. It can't start with pg_. Avoid using these patterns in the admin name. |

## Next step

> [!div class="nextstepaction"]
> [report the issue](https://github.com/Azure/azure-cli/issues)
