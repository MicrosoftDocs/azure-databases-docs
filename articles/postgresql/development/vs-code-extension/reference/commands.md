---
title: Commands Reference for the PostgreSQL Extension for Visual Studio Code
description: Complete list of commands in the PostgreSQL extension for Visual Studio Code.
author: mmcfarland
ms.author: mmcfarland
ms.reviewer: nachoalonsoportillo, maghan
ms.date: 06/08/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: reference
---

# Commands reference

This page lists user-facing commands registered by the PostgreSQL extension. Generated from `package.json` (91 commands).

## PGSQL

| Command | ID | Keybinding |
| --- | --- | --- |
| Add Microsoft Entra Account | `pgsql.addAadAccount` | - |
| Add New Connection | `pgsql.addNewConnection` | - |
| Analyze Query Performance | `pgsql.copilot.analyzeQueryPerformance` | - |
| Ask AI about this Query | `pgsql.copilot.chatWithEditor` | - |
| Backups | `pgsql.showServerDashboardBackups` | - |
| Cancel Query (PostgreSQL) | `pgsql.cancelQuery` | - |
| Change Connection (PostgreSQL) | `pgsql.changeConnection` | - |
| Change Database (PostgreSQL) | `pgsql.changeDatabase` | - |
| Change Schema (PostgreSQL) | `pgsql.changeSchema` | - |
| Choose SQL handler for this file | `pgsql.chooseLanguageFlavor` | - |
| Clear "Don't Show Again" settings for intro pages | `pgsql.clearSkipIntroSettings` | - |
| Clear All Query History | `pgsql.clearAllQueryHistory` | - |
| Clear cached Azure PostgreSQL deployment metadata | `pgsql.clearStagedFlexProfiles` | - |
| Clear Microsoft Entra account token cache | `pgsql.clearAzureAccountTokenCache` | - |
| Clear query inclusion preferences for AI analysis | `pgsql.clearQueryInclusionPreferences` | - |
| Clone Server | `pgsql.cloneServer` | - |
| Compare Application Migration File Pairs | `pgsql.migration.compareConvertedAppFile` | - |
| Compare DDL Migration File Pairs | `pgsql.migration.compareConvertedDDLFile` | - |
| Connect (PostgreSQL) | `pgsql.connect` | ctrl+shift+c (Mac: cmd+shift+c) |
| Connect (PostgreSQL) | `pgsql.connectWithUriOwnership` | - |
| Connect AI | `pgsql.copilot.connectDatabaseInAgentMode` | - |
| Connect with PSQL | `pgsql.psqlTerminalDatabase` | - |
| Copy all messages | `pgsql.copyAll` | - |
| Copy Name | `pgsql.copyObjectName` | ctrl+c (Mac: cmd+c) |
| Copy Query | `pgsql.copyQueryHistory` | - |
| Create Azure HorizonDB | `pgsql.createAzureHorizonDb` | - |
| Create Azure PostgreSQL Flexible Server | `pgsql.createAzureFlexServer` | - |
| Create New Docker Instance | `pgsql.createDockerServer` | - |
| Create New Server | `pgsql.createNewServer` | - |
| Create New Server | `pgsql.azureDeployments.create` | - |
| Create Server Group | `pgsql.createServerGroup` | - |
| Dashboard | `pgsql.showServerDashboard` | - |
| Delete | `pgsql.deleteQueryHistory` | - |
| Delete | `pgsql.migration.deleteProject` | - |
| Disconnect | `pgsql.disconnectObjectExplorerNode` | - |
| Disconnect (PostgreSQL) | `pgsql.disconnect` | ctrl+shift+d (Mac: cmd+shift+d) |
| Durable Workbench: Refresh Capabilities | `pgsql.durableWorkbench.refreshCapabilities` | - |
| Edit Connection | `pgsql.editConnection` | - |
| Edit Server Group | `pgsql.editServerGroup` | - |
| Execute Current Statement (PostgreSQL) | `pgsql.runCurrentStatement` | ctrl+shift+enter (Mac: ctrl+shift+enter) |
| Execute Query (PostgreSQL) | `pgsql.runQuery` | ctrl+shift+e (Mac: cmd+shift+e), shift+enter (Mac: shift+enter) |
| Execute Query (PostgreSQL) | `pgsql.runQueryWithUriOwnership` | - |
| Explain Query | `pgsql.copilot.explainQuery` | - |
| Getting Started Guide | `pgsql.showGettingStarted` | - |
| Give Feedback | `pgsql.userFeedback` | - |
| Network Configuration | `pgsql.showServerDashboardNetworkConfiguration` | - |
| New Query | `pgsql.newQuery` | - |
| New Query | `pgsql.objectExplorerNewQuery` | - |
| Only show connected servers | `pgsql.objectExplorerShowOnlyConnected` | - |
| Open in Azure Portal | `pgsql.azureDeployments.openPortal` | - |
| Open Migration Project | `pgsql.migration.migrationProject` | - |
| Open Migration Project | `pgsql.migration.openProject` | - |
| Open Query | `pgsql.openQueryHistory` | - |
| Open Query History in Command Palette | `pgsql.commandPaletteQueryHistory` | - |
| Pause Query History Capture | `pgsql.pauseQueryHistoryCapture` | - |
| Pipelines & Workflows | `pgsql.durableWorkbench.open` | - |
| Properties | `pgsql.showObjectProperties` | - |
| Refresh | `pgsql.refreshObjectExplorerNode` | - |
| Refresh IntelliSense Cache | `pgsql.rebuildIntelliSenseCache` | - |
| Refresh Migrations | `pgsql.migration.refreshMigrations` | - |
| Remove | `pgsql.deleteServerGroup` | - |
| Remove | `pgsql.removeObjectExplorerNode` | - |
| Remove Completed | `pgsql.azureDeployments.clearAll` | - |
| Remove Deployment | `pgsql.azureDeployments.deleteDeployment` | - |
| Remove Microsoft Entra Account | `pgsql.removeAadAccount` | - |
| Restart server | `pgsql.azureServerRestart` | - |
| Restore from Backup | `pgsql.restoreFromBackup` | - |
| Reveal in Explorer | `pgsql.migration.revealProject` | - |
| Reveal Query Result (PostgreSQL) | `pgsql.revealQueryResultPanel` | - |
| Rewrite Query | `pgsql.copilot.rewriteQuery` | - |
| Run file with PSQL | `pgsql.psqlRunFile` | - |
| Run Query | `pgsql.runQueryHistory` | - |
| Script as Alter | `pgsql.scriptAlter` | - |
| Script as Create | `pgsql.scriptCreate` | - |
| Script as Drop | `pgsql.scriptDelete` | - |
| Script as Execute | `pgsql.scriptExecute` | - |
| Search Objects | `pgsql.searchObjects` | - |
| Select Top 1000 | `pgsql.scriptSelect` | - |
| Server Logs | `pgsql.showServerDashboardServerLogs` | - |
| Server Parameters | `pgsql.showServerDashboardServerParameters` | - |
| Show connected & disconnected servers | `pgsql.objectExplorerShowAllServers` | - |
| Show PostgreSQL Extension Logs | `pgsql.showExtensionLogs` | - |
| Show PostgreSQL Tools Service Logs | `pgsql.showToolsServiceLogs` | - |
| Start Query History Capture | `pgsql.startQueryHistoryCapture` | - |
| Start server | `pgsql.azureServerStart` | - |
| Stop server | `pgsql.azureServerStop` | - |
| Use Database | `pgsql.chooseDatabase` | - |
| Visualize Query Plan (PostgreSQL) | `pgsql.visualizeQueryPlan` | - |
| Visualize Query Plan from Editor | `pgsql.visualizeQueryPlanFromEditor` | - |
| Visualize Schema | `pgsql.visualizeSchema` | - |
| Visualize Schema | `pgsql.visualizeSchemaNode` | - |

:::image type="content" source="commands/default-connection-dialog-default.png" alt-text="Screenshot of the connection dialog." lightbox="commands/default-connection-dialog-default.png":::

:::image type="content" source="commands/default-terminal-run-file.png" alt-text="Screenshot of the terminal." lightbox="commands/default-terminal-run-file.png":::

:::image type="content" source="commands/default-create-server-default.png" alt-text="Screenshot of the create server experience." lightbox="commands/default-create-server-default.png":::

:::image type="content" source="commands/default-server-dashboard-default.png" alt-text="Screenshot of the server dashboard." lightbox="commands/default-server-dashboard-default.png":::

:::image type="content" source="commands/default-query-editor-default.png" alt-text="Screenshot of the query editor." lightbox="commands/default-query-editor-default.png":::

:::image type="content" source="commands/default-object-explorer-default.png" alt-text="Screenshot of the object explorer." lightbox="commands/default-object-explorer-default.png":::

:::image type="content" source="commands/default-oracle-migration-migration-project-setup.png" alt-text="Screenshot of the Oracle migration experience." lightbox="commands/default-oracle-migration-migration-project-setup.png":::

:::image type="content" source="commands/default-query-plan-default.png" alt-text="Screenshot of the query plan visualizer." lightbox="commands/default-query-plan-default.png":::

## Related content

- [Settings reference](settings.md)
- [Keyboard shortcuts reference](keyboard-shortcuts.md)
- [PostgreSQL extension for Visual Studio Code](../postgresql-extension-overview.md)
