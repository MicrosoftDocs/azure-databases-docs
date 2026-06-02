---
title: "Settings reference"
description: "Complete list of settings in the PostgreSQL extension for Visual Studio Code."
author: mmcfarland
ms.author: mattmcfarland
ms.date: 05/31/2026
ms.service: postgresql
ms.subservice: vs-code-pgsql-extensions
ms.topic: reference
---


# Settings reference

This page lists all settings contributed by the PostgreSQL extension. Generated from `package.json` (43 settings).

## Connections

| Setting | Type | Default | Scope | Description |
|---|---|---|---|---|
| `pgsql.azureActiveDirectory` | string; one of `AuthCodeGrant`, `DeviceCode` | `"AuthCodeGrant"` | application | Chooses which Authentication method to use |
| `pgsql.connections` | array | — | resource | Connection profiles defined in 'User Settings' are shown under 'PostgreSQL: Connect' command in the command palette. |
| `pgsql.maxConnections` | number | `10` | resource | The maximum number of simultanious connections to open at __per profile + database__. Connections to the same server, but to different databases, does not count to the same total.  The default value is 10. |
| `pgsql.maxRecentConnections` | number | `5` | window | The maximum number of recently used connections to store in the connection list. |
| `pgsql.serverGroups` | array | — | resource | Server groups |

## Query Editor & Results

| Setting | Type | Default | Scope | Description |
|---|---|---|---|---|
| `pgsql.copyIncludeHeaders` | boolean | `false` | resource | [Optional] Configuration options for copying results from the Results View |
| `pgsql.copyRemoveNewLine` | boolean | `true` | resource | [Optional] Configuration options for copying multi-line results from the Results View |
| `pgsql.intelliSense.enableIntelliSense` | boolean | `true` | window | Should IntelliSense be enabled |
| `pgsql.messagesDefaultOpen` | boolean | `true` | resource | True for the messages pane to be open by default; false for closed |
| `pgsql.openQueryResultsInTabByDefault` | boolean | `false` | application | Automatically display query results in a new tab instead of the query pane. |
| `pgsql.openQueryResultsInTabByDefaultDoNotShowPrompt` | boolean | `false` | application | Do not show prompts to display query results in a new tab. |
| `pgsql.persistQueryResultTabs` | boolean | `false` | window | Should query result selections and scroll positions be saved when switching tabs (may impact performance) |
| `pgsql.resultsFontFamily` | string | — | resource | Set the font family for the results grid; set to blank to use the editor font |
| `pgsql.resultsFontSize` | number, null | — | resource | Set the font size for the results grid; set to blank to use the editor size |
| `pgsql.resultsGrid.autoSizeColumns` | boolean | `true` | — | Automatically adjust the column widths based on the visible rows in the result set. Could have performance problems with a large number of columns or large cells |
| `pgsql.saveAsCsv.delimiter` | string | `","` | resource | [Optional] Delimiter for separating data items when saving results as CSV |
| `pgsql.saveAsCsv.encoding` | string | `"utf-8"` | resource | [Optional] File encoding used when saving results as CSV |
| `pgsql.saveAsCsv.includeHeaders` | boolean | `true` | resource | [Optional] When true, column headers are included when saving results as CSV |
| `pgsql.saveAsCsv.lineSeparator` | string | — | resource | [Optional] Character(s) used for separating rows when saving results as CSV |
| `pgsql.saveAsCsv.textIdentifier` | string | `"\""` | resource | [Optional] Character used for enclosing text fields when saving results as CSV |
| `pgsql.shortcuts` | object | See below | resource | Shortcuts related to the results window |
| `pgsql.showBatchTime` | boolean | `false` | resource | [Optional] Should execution time be shown for individual batches |
| `pgsql.showConnectionStatusLens` | boolean | `true` | application | Show connection status in the editor lens area. |
| `pgsql.splitPaneSelection` | string; one of `next`, `current`, `end` | `"next"` | resource | [Optional] Configuration options for which column new result panes should open in |

## Query History

| Setting | Type | Default | Scope | Description |
|---|---|---|---|---|
| `pgsql.enableQueryHistoryCapture` | boolean | `true` | window | Enable Query History Capture |
| `pgsql.enableQueryHistoryFeature` | boolean | `true` | window | Should Query History feature be enabled |
| `pgsql.queryHistoryLimit` | number | `20` | window | Number of query history entries to show in the Query History view |

## Copilot

| Setting | Type | Default | Scope | Description |
|---|---|---|---|---|
| `pgsql.copilot.accessMode` | string; one of `ro`, `rw` | `"rw"` | window | Choose between `Read Only` or `Read/Write` mode for the `@pgsql` AI chat agent. |
| `pgsql.copilot.autoAttachQuery` | string; one of `ask`, `always`, `never` | `"ask"` | window | Control whether SQL query text is included when analyzing query plans with AI. |
| `pgsql.copilot.enable` | boolean | `true` | window | Enable the `@pgsql` AI chat agent (requires reload) |
| `pgsql.copilot.modelOptions` | object | — | window | Set the model options for the `@pgsql` AI chat agent.<br/>⚠️ This can impact the performance of the agent or even break it; only change this if you know what you are doing. |

## Object Explorer

| Setting | Type | Default | Scope | Description |
|---|---|---|---|---|
| `pgsql.objectExplorer.expandTimeout` | number | `45` | — | The timeout in seconds for expanding a node in Object Explorer. The default value is 45 seconds. |

## PSQL Terminal

| Setting | Type | Default | Scope | Description |
|---|---|---|---|---|
| `pgsql.pgBinaryDirs` | array | — | — | List of absolute paths to PG binary directories. Restart the editor after changing this setting. |

## Feature Toggles

| Setting | Type | Default | Scope | Description |
|---|---|---|---|---|
| `pgsql.enableExperimentalFeatures` | boolean | `false` | application | Enables experimental features in the PostgreSQL extension. The features are not production-ready and may have bugs or issues. Restart the editor after changing this setting. |
| `pgsql.enableMigrations` | boolean | `true` | window | Enable Oracle to PostgreSQL migration features including the migrations view, migration commands, and migration language model tools |
| `pgsql.enableServerDashboard` | boolean | `true` | window | Enable Server Dashboards with metrics (Preview). |

## Diagnostics

| Setting | Type | Default | Scope | Description |
|---|---|---|---|---|
| `pgsql.logDebugInfo` | boolean | `false` | window | [Optional] Log debug output to the developer console (Help -> Toggle Developer Tools) |
| `pgsql.piiLogging` | boolean | `false` | — | Should Personally Identifiable Information (PII) be logged in the Azure Logs output channel and the output channel log file. |
| `pgsql.toolsService.logLevel` | string; one of `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG` | `"INFO"` | application | Log level for the PostgreSQL Tools Service (requires restart). |
| `pgsql.tracingLevel` | string; one of `All`, `Off`, `Critical`, `Error`, `Warning`, `Information`, `Verbose` | `"All"` | — | [Optional] Log level for backend services. |

## Provisioning

| Setting | Type | Default | Scope | Description |
|---|---|---|---|---|
| `pgsql.flexProvisioning.deploymentRetentionDays` | number | `30` | application | Number of days to keep completed Azure PostgreSQL Flexible Server deployment metadata for automatic resume. Passwords are stored in the editor's secret store and deleted immediately after successful or failed deployments. Run 'PGSQL: Clear cached Azure PostgreSQL deployment metadata' to remove entries immediately. |

## General

| Setting | Type | Default | Scope | Description |
|---|---|---|---|---|
| `azureResourceGroups.selectedSubscriptions` | array | — | — | Selected Subscriptions |
| `pgsql.horizonCreate.enableAiModelManagement` | boolean | `false` | application | Preview: shows the AI Model Management UI in the **Create Azure HorizonDB** wizard. This feature is in preview and may change. Restart the wizard after toggling. |

## Complex default values

### `pgsql.shortcuts`

```json
{
  "_comment": "Short cuts must follow the format (ctrl)+(shift)+(alt)+[key]",
  "event.toggleResultPane": "ctrl+alt+R",
  "event.focusResultsGrid": "ctrl+alt+G",
  "event.toggleMessagePane": "ctrl+alt+Y",
  "event.prevGrid": "ctrl+up",
  "event.nextGrid": "ctrl+down",
  "event.copySelection": "ctrl+C",
  "event.copyWithHeaders": "",
  "event.copyAllHeaders": "",
  "event.maximizeGrid": "",
  "event.selectAll": "ctrl+A",
  "event.saveAsJSON": "",
  "event.saveAsCSV": "",
  "event.saveAsExcel": "",
  "event.changeColumnWidth": "ctrl+alt+S"
}
```


## Related content

- [Commands reference](commands.md)
- [Keyboard shortcuts reference](keyboard-shortcuts.md)
- [PostgreSQL extension overview](../pgsql-extension-overview.md)
