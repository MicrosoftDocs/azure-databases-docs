---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 09/17/2024
ms.custom: subject-msia
zone_pivot_groups: azure-interface-cli-powershell
---

The current Azure CLI session could be signed in with a human identity (your account), a managed identity, a workload identity, or a service principal. No matter what type of identity you use with Azure CLI, to steps to get the details of the identity can be similar. For more information, see [Microsoft Entra identity fundamentals](/entra/fundamentals/identity-fundamental-concepts#identity).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

::: zone pivot="azure-interface-cli"

[!INCLUDE [Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

::: zone-end

::: zone pivot="azure-interface-powershell"

[!INCLUDE [Azure PowerShell prerequisites](~/reusable-content/azure-powershell/azure-powershell-requirements-no-header.md)]

::: zone-end

## Get signed in account identity

Use the command line to query the graph for information about your account's unique identifier.

::: zone pivot="azure-interface-cli"

1. Get the details for the currently logged-in account using [`az ad signed-in-user`](/cli/azure/ad/signed-in-user#az-ad-signed-in-user-show).

    ```azurecli-interactive
    az ad signed-in-user show
    ```

1. The command outputs a JSON response containing various fields.

    ```json
    {
      "@odata.context": "<https://graph.microsoft.com/v1.0/$metadata#users/$entity>",
      "businessPhones": [],
      "displayName": "Jayden Philips",
      "givenName": "Jayden",
      "id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
      "jobTitle": "Senior Sales Representative",
      "mail": "<jayden@adventure-works.com>",
      "mobilePhone": null,
      "officeLocation": "Redmond",
      "preferredLanguage": null,
      "surname": "Philips",
      "userPrincipalName": "<jayden@adventure-works.com>"
    }
    ```

    > [!TIP]
    > Record the value of the `id` field. In this example, that value would be `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb`. This value can then be used in various scripts to grant your current account role-based access control permissions to Azure resources.

::: zone-end

::: zone pivot="azure-interface-powershell"

1. Get the details for the currently logged-in account using [`Get-AzADUser`](/powershell/module/az.resources/get-azaduser).

    ```azurepowershell-interactive
    Get-AzADUser -SignedIn | Format-List `
        -Property Id, DisplayName, Mail, UserPrincipalName
    ```

1. The command outputs a list response containing various fields.

    ```output
    Id                : aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb
    DisplayName       : Jayden Philips
    Mail              : jayden@adventure-works.com
    UserPrincipalName : jayden@adventure-works.com
    ```

    > [!TIP]
    > Record the value of the `id` field. In this example, that value would be `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb`. This value can then be used in various scripts to grant your current account role-based access control permissions to Azure resources.

::: zone-end
