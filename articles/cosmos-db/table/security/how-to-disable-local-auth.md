---
title: Disable local authentication
titleSuffix: Azure Cosmos DB for Table
description: 
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: how-to
ms.date: 09/09/2024
#Customer Intent: As a security user, I want to disable local auth in an Azure Cosmos DB for Table account, so that my developers or applications can no longer access the account in an insecure manner.
---

# Disable local authentication with Azure Cosmos DB for Table

:::image type="complex" source="media/how-to-disable-local-auth/map.svg" border="false" alt-text="Diagram of the current location ('Prepare') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, and Solution. The 'Prepare' location is currently highlighted.
:::image-end:::

This article covers the process of disabling local auth for an Azure Cosmos DB for Table account. This is a step that should be performed on new accounts in secure workloads or existing accounts being migrated to a secure workload pattern.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

## Disable key-based authentication

TODO

### [New account](#tab/new-account)

1. TODO. Name file *deploy-new-account.bicep*.

    ```bicep
    
    ```

1. TODO

    ```azurecli-interactive
    az group deployment create `
        --resource-group "<name-of-existing-resource-group>" `
        --template-file deploy-new-account.bicep
    ```

### [Existing account](#tab/existing-account)

1. TODO. Name file *update-existing-account.bicep*.

    ```bicep
    
    ```

1. TODO. Name file *update-existing-account-params.json*.

    ```json

    ```

1. TODO

    ```azurecli-interactive
    az group deployment create `
        --resource-group "<name-of-existing-resource-group>" `
        --parameters @update-existing-account-params.json `
        --template-file update-existing-account.bicep
    ```

---

## Validate that authentication is disabled

Attempt to use the Azure SDK to connect to Azure Cosmos DB for Table using a resource-owner password credential (ROPC). This attempt should fail. If required, code samples for common programming languages are provided below

### [C#](#tab/csharp)

```csharp

```

> [!IMPORTANT]
> This code sample uses the []() library from NuGet.

### [JavaScript](#tab/javascript)

```javascript

```

> [!IMPORTANT]
> This code sample uses the []() library from npm.

### [TypeScript](#tab/typescript)

```typescript

```

> [!IMPORTANT]
> This code sample uses the []() library from npm.

### [Python](#tab/python)

```python

```

> [!IMPORTANT]
> This code sample uses the []() library from PyPI.

---

## Next step

> [!div class="nextstepaction"]
> [Grant your identity control-plane access](how-to-grant-control-plane-access.md)
