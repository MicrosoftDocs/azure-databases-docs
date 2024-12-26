---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 10/01/2024
ms.custom: subject-msia
zone_pivot_groups: azure-interface-portal-cli-powershell
---

The current Azure CLI session could be signed in with a human identity (your account), a managed identity, a workload identity, or a service principal. No matter what type of identity you use with Azure CLI, to steps to get the details of the identity can be similar. For more information, see [Microsoft Entra identity fundamentals](/entra/fundamentals/identity-fundamental-concepts#identity).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

::: zone pivot="azure-interface-cli"

[!INCLUDE [Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

::: zone-end

::: zone pivot="azure-interface-portal"

::: zone-end

::: zone pivot="azure-interface-shell"

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
      "displayName": "Kai Carter",
      "givenName": "Kai",
      "id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
      "jobTitle": "Senior Sales Representative",
      "mail": "<kai@adventure-works.com>",
      "mobilePhone": null,
      "officeLocation": "Redmond",
      "preferredLanguage": null,
      "surname": "Carter",
      "userPrincipalName": "<kai@adventure-works.com>"
    }
    ```

    > [!TIP]
    > Record the value of the `id` field. In this example, that value would be `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb`. This value can then be used in various scripts to grant your current account role-based access control permissions to Azure resources.

::: zone-end

::: zone pivot="azure-interface-portal"

Use the in-portal panes for Microsoft Entra ID to get details of your currently signed-in user account.

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. On the **Home** pane, locate and select the **Microsoft Entra ID** option.

    :::image source="media/get-signed-in-identity/home-entra-id-option.png" lightbox="media/get-signed-in-identity/home-entra-id-option-full.png" alt-text="Screenshot of the Microsoft Entra ID option in the 'Home' page of the Azure portal.":::

    > [!TIP]
    > If this option is not listed, select **More services** and then search for **Microsoft Entra ID** using the search term **"Entra"**.

1. Within the **Overview** pane for the Microsoft Entra ID tenant, select **Users** inside the **Manage** section of the service menu.

    :::image source="media/get-signed-in-identity/users-option-service-menu.png" alt-text="Screenshot of the 'Users' option in the service menu for the Microsoft Entra ID tenant.":::

1. In the list of users, select the identity (user) that you want to get more details about.

    :::image source="media/get-signed-in-identity/users-list.png" alt-text="Screenshot of the list of users for a Microsoft Entra ID tenant with an example user highlighted.":::

    > [!NOTE]
    > This screenshot illustrates an example user named *"Kai Carter"* with a principal of `kai@adventure-works.com`.

1. On the details pane for the specific user, observe the value of the **Object ID** property.

    :::image source="media/get-signed-in-identity/user-details.png" alt-text="Screenshot of the details pane for a specific user in a Microsoft Entra ID tenant with their unique 'Object ID' highlighted.":::

    > [!TIP]
    > Record the value of the **Object ID** property. In this example, that value would be `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb`. This value can then be used in various scripts to grant your current account role-based access control permissions to Azure resources.

::: zone-end

::: zone pivot="azure-interface-shell"

1. Get the details for the currently logged-in account using [`Get-AzADUser`](/powershell/module/az.resources/get-azaduser).

    ```azurepowershell-interactive
    Get-AzADUser -SignedIn | Format-List `
        -Property Id, DisplayName, Mail, UserPrincipalName
    ```

1. The command outputs a list response containing various fields.

    ```output
    Id                : aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb
    DisplayName       : Kai Carter
    Mail              : kai@adventure-works.com
    UserPrincipalName : kai@adventure-works.com
    ```

    > [!TIP]
    > Record the value of the `id` field. In this example, that value would be `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb`. This value can then be used in various scripts to grant your current account role-based access control permissions to Azure resources.

::: zone-end
