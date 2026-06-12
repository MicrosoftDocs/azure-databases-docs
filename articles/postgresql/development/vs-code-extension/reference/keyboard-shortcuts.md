---
title: Keyboard Shortcuts Reference for the PostgreSQL Extension for Visual Studio Code
description: Keyboard shortcuts for the PostgreSQL extension for Visual Studio Code.
author: mmcfarland
ms.author: mmcfarland
ms.reviewer: nachoalonsoportillo, maghan
ms.date: 06/08/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: reference
---

# Keyboard shortcuts reference

## Extension keybindings

| Action | Windows/Linux | macOS | When |
| --- | --- | --- | --- |
| Execute Query (PostgreSQL) | ctrl+shift+e | cmd+shift+e | editorTextFocus && editorLangId == 'sql' |
| Execute Query (PostgreSQL) | shift+enter | shift+enter | editorTextFocus && editorLangId == 'sql' |
| Execute Current Statement (PostgreSQL) | ctrl+shift+enter | ctrl+shift+enter | editorTextFocus && editorLangId == 'sql' |
| Connect (PostgreSQL) | ctrl+shift+c | cmd+shift+c | editorTextFocus && editorLangId == 'sql' |
| Disconnect (PostgreSQL) | ctrl+shift+d | cmd+shift+d | editorTextFocus && editorLangId == 'sql' |
| Open PostgreSQL view | ctrl+alt+d | cmd+alt+d | - |
| Copy Name | ctrl+c | cmd+c | sideBarFocus && activeViewlet == workbench.view.extension.objectExplorer |

## Results grid shortcuts

These shortcuts apply when the query results grid is focused. Customize them via the `pgsql.shortcuts` setting.

| Action | Keybinding |
| --- | --- |
| Toggle Result Pane | ctrl+alt+R |
| Focus Results Grid | ctrl+alt+G |
| Toggle Message Pane | ctrl+alt+Y |
| Previous Grid | ctrl+up |
| Next Grid | ctrl+down |
| Copy Selection | ctrl+C |
| Select All | ctrl+A |
| Change Column Width | ctrl+alt+S |

## Related content

- [Commands reference](commands.md)
- [Settings reference](settings.md)
- [Query editor and IntelliSense](../query-editor-intellisense.md)
