---
title: "Sign into Azure include file"
description: This include file provides a script to sign in to Azure using Azure CLI.
author: gbowerman
ms.author: guybo
ms.reviewer: maghan
ms.date: 01/23/2026
ms.service: azure-database-postgresql
ms.topic: include
---

For this script, use Azure CLI locally as it takes too long to run in Cloud Shell.

### Sign in to Azure

Use the following script to sign in using a specific subscription.

```azurecli-interactive
subscription="<subscriptionId>" # add subscription here

az account set -s $subscription # ...or use 'az login'
```

For more information, see [set active subscription](/cli/azure/account#az-account-set) or [log in interactively](/cli/azure/reference-index#az-login)
