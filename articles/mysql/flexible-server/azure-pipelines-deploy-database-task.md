---
title: Azure Pipelines Task
description: Enable an Azure Database for MySQL - Flexible Server CLI task for using with Azure Pipelines.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
---

# Azure Pipelines for Azure Database for MySQL - Flexible Server

You can automatically deploy your database updates to Azure Database for MySQL Flexible Server after every successful build with **Azure Pipelines**. You can use Azure CLI task to update the database either with a SQL file or an inline SQL script against the database. This task can be run on cross-platform agents running on Linux, macOS, or Windows operating systems.

## Prerequisites

- An Azure account. If you don't have one, [get a free trial](https://azure.microsoft.com/free/).

- [Azure Resource Manager service connection](/azure/devops/pipelines/library/connect-to-azure) to your Azure account
- Microsoft hosted agents have Azure CLI pre-installed. However if you are using private agents, [install Azure CLI](/cli/azure/install-azure-cli) on the computer(s) that run the build and release agent. If an agent is already running on the machine on which the Azure CLI is installed, restart the agent to ensure all the relevant stage variables are updated.

This quickstart uses the resources created in either of these guides as a starting point:

- Create an Azure Database for MySQL Flexible Server instance by using the [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md) or [Quickstart: Create an instance of Azure Database for MySQL - Flexible Server by using the Azure CLI](quickstart-create-server-cli.md).

## Use SQL file

The following example illustrates how to pass database arguments and run ```execute``` command

```azurecli
- task: AzureCLI@2
  displayName: Azure CLI
  inputs:
    azureSubscription: <Name of the Azure Resource Manager service connection>
    scriptLocation: inlineScript
    arguments:
      -SERVERNAME mydemoserver `
      -DBNAME pollsdb `
      -DBUSER pollsdbuser`
      -DBPASSWORD pollsdbpassword
    inlineScript: |
      az login --allow-no-subscription
      az mysql flexible-server execute --name $(SERVERNAME) \
      --admin-user $(DBUSER) --admin-password '$(DBPASSWORD)' \
      --database-name $(DBNAME) \
      --file-path /code/sql/db-schema-update.sql
```

## Use inline SQL script

The following example illustrates how to run an inline SQL script using ```execute``` command .

```azurecli
- task: AzureCLI@2
  displayName: Azure CLI
  inputs:
    azureSubscription: <Name of the Azure Resource Manager service connection>
    scriptLocation: inlineScript
    arguments:
      -SERVERNAME mydemoserver `
      -DBNAME pollsdb `
      -DBUSER pollsdbuser`
      -DBPASSWORD pollsdbpassword
      -INLINESCRIPT
    inlineScript: |
      az login --allow-no-subscription
      az mysql flexible-server execute --name $(SERVERNAME) \
      --admin-user $(DBUSER) --admin-password '$(DBPASSWORD)' \
      --database-name $(DBNAME) \
      --query-text "UPDATE items SET items.retail = items.retail * 0.9 WHERE items.id =100;"
```

## Task inputs

You can see the full list of all the task inputs when using Azure CLI task with Azure Pipelines.

| Parameter | Description |
| :--- | :--- |
| azureSubscription | (Required) Provide the Azure Resource Manager subscription for the deployment. This parameter is shown only when the selected task version is 0.* as Azure CLI task v1.0 supports only Azure Resource Manager subscriptions. |
| scriptType | (Required) Provide the type of script. Supported scripts are PowerShell, PowerShell Core, Bat, Shell, and script. When running on a **Linux agent**, select one of the following: ```bash``` or ```pscore``` . When running **Windows agent**, select one of the following: ```batch```,```ps``` and ```pscore```. |
| scriptLocation | (Required) Provide the path to script, for example real file path or use ```Inline script``` when providing the scripts inline. The default value is ```scriptPath```. |
| scriptPath | (Required) Fully qualified path of the script(.ps1 or .bat or .cmd when using Windows-based agent else <code>.ps1 </code> or <code>.sh </code> when using linux-based agent) or a path relative to the default working directory. |
| inlineScript | (Required) You can write your scripts inline here. When using Windows agent, use PowerShell or PowerShell Core or batch scripting whereas use PowerShell Core or shell scripting when using Linux-based agents. For batch files use the prefix \"call\" before every Azure command. You can also pass predefined and custom variables to this script using arguments.<br />Example for PowerShell/PowerShellCore/shell:``` az --version az account show```<br />Example for batch: ``` call az --version call az account show```. |
| arguments | (Optional) Provide all the arguments passed to the script. For examples ```-SERVERNAME mydemoserver```. |
| powerShellErrorActionPreference | (Optional) Prepends the line <b>$ErrorActionPreference = 'VALUE'</b> at the top of your PowerShell/PowerShell Core script. The default value is stop. Supported values are stop, continue, and silentlyContinue. |
| addSpnToEnvironment | (Optional) Adds service principal ID and key of the Azure endpoint you chose to the script's execution environment. You can use these variables: <b>$env:servicePrincipalId, $env:servicePrincipalKey and $env:tenantId</b> in your script. This is honored only when the Azure endpoint has Service Principal authentication scheme. The default value is false. |
| useGlobalConfig | (Optional) If this is false, this task will use its own separate [Azure CLI configuration directory](/cli/azure/azure-cli-configuration#cli-configuration-file)Azure CLI configuration directory</a>. This can be used to run Azure CLI tasks in <b>parallel</b> releases"<br />Default value: false</td> |
| workingDirectory | (Optional) Current working directory where the script is run. Empty is the root of the repo (build) or artifacts (release), which is $(System.DefaultWorkingDirectory). |
| failOnStandardError | (Optional) If this is true, this task will fail when any errors are written to the StandardError stream. Unselect the checkbox to ignore standard errors and rely on exit codes to determine the status. The default value is false. |
| powerShellIgnoreLASTEXITCODE | (Optional) If this is false, the line <code>if ((Test-Path -LiteralPath variable:\\LASTEXITCODE)) { exit $LASTEXITCODE }</code> is appended to the end of your script. This will cause the last exit code from an external command to be propagated as the exit code of PowerShell. Otherwise the line is not appended to the end of your script. The default value is false. |
| Having issues with CLI Task, see [how to troubleshoot Build and Release](/azure/devops/pipelines/troubleshooting/troubleshooting). |

## Related content

- [Azure Resource Group Deployment](/azure/devops/pipelines/tasks/deploy/azure-resource-group-deployment)
- [Azure Web App Deployment](/azure/devops/pipelines/tasks/deploy/azure-rm-web-app-deployment)
