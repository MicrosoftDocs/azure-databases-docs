---
title: Disable key-based authentication
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to disable key-based auth with Azure Cosmos DB for NoSQL to prevent an account from being used with insecure authentication methods.
author: seesharprun
ms.author: sidandrews
ms.reviewer: loicmazeyrat
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 09/24/2024
zone_pivot_groups: azure-interface-cli-powershell-bicep
#Customer Intent: As a security user, I want to disable key-based auth in an Azure Cosmos DB for NoSQL account, so that my developers or applications can no longer access the account in an insecure manner.
---

# Disable key-based authentication with Azure Cosmos DB for NoSQL

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

:::image type="complex" source="media/how-to-disable-key-based-authentication/map.svg" border="false" alt-text="Diagram of the current location ('Prepare') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, Network, and Reference. The 'Prepare' location is currently highlighted.
:::image-end:::

This article covers the process of disabling key-based authorization (or resource owner password credential auth) for an Azure Cosmos DB for NoSQL account. Disabling key-based authorization prevents your account from being used without the more secure Microsoft Entra authentication method. This procedure is a step that should be performed on new accounts in secure workloads. Alternatively, perform this procedure on existing accounts being migrated to a secure workload pattern.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

::: zone pivot="azure-interface-cli,azure-interface-bicep"

[!INCLUDE [Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

::: zone-end

::: zone pivot="azure-interface-shell"

[!INCLUDE [Azure PowerShell prerequisites](~/reusable-content/azure-powershell/azure-powershell-requirements-no-header.md)]

::: zone-end

## Disable key-based authentication

First, disable key-based authentication to your account so that applications are required to use Microsoft Entra authentication.

::: zone pivot="azure-interface-cli"

### [New account](#tab/new-account)

1. TODO

### [Existing account](#tab/existing-account)

1. TODO

---

::: zone-end

::: zone pivot="azure-interface-bicep"

1. TODO

::: zone-end

::: zone pivot="azure-interface-shell"

### [New account](#tab/new-account)

1. TODO

### [Existing account](#tab/existing-account)

1. TODO

---

::: zone-end

## Validate that authentication is disabled

Attempt to use the Azure SDK to connect to Azure Cosmos DB for NoSQL using a resource-owner password credential (ROPC). This attempt should fail. If necessary, code samples for common programming languages are provided here.

### [C#](#tab/csharp)

```csharp
TODO
```

> [!IMPORTANT]
> This code sample uses the [`TODO`](about:blank) library from NuGet.

### [JavaScript](#tab/javascript)

```javascript
TODO
```

> [!IMPORTANT]
> This code sample uses the [`TODO`](about:blank) package from npm.

### [TypeScript](#tab/typescript)

```typescript
TODO
```

> [!IMPORTANT]
> This code sample uses the [`TODO`](about:blank) package from npm.

### [Python](#tab/python)

```python
TODO
```

> [!IMPORTANT]
> This code sample uses the [`TODO`](about:blank) package from PyPI.

---

## Next step

> [!div class="nextstepaction"]
> [Grant your identity control plane role-based access](how-to-grant-control-plane-role-based-access.md)
