---
title: Use Microsoft Entra ID and native DocumentDB users for authentication with Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn how to manage authentication and set up Microsoft Entra ID users for authentication on Azure Cosmos DB for MongoDB vCore clusters.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 04/14/2025
appliesto:
  - ✅ MongoDB vCore
---

# Use Microsoft Entra ID users for authentication with Azure Cosmos DB for MongoDB vCore

> [!IMPORTANT]
> Microsoft Entra ID authentication in Azure Cosmos DB for MongoDB vCore is currently in preview.
> This preview version is provided without a service level agreement, and it's not recommended
> for production workloads. Certain features might not be supported or might have constrained
> capabilities.

In this article, you configure administrative Microsoft Entra ID users to be used with Azure Cosmos DB for MongoDB vCore. You also learn how to use a Microsoft Entra ID token with Azure Cosmos DB for MongoDB vCore. Microsoft Entra ID user can be a user or a service principal.

Microsoft Entra ID users added to the cluster are going to be in addition to native DocumentDB users defined on the cluster. An Azure Cosmos DB for MongoDB vCore cluster is created with one built-in native DocumentDB user. You can add more native DocumentDB users after cluster provisioning is completed.

## Prerequisites

Users need to be allowed to sign in to Azure Cosmos DB for MongoDB vCore in the Microsoft Entra ID tenant. These steps should be performed **once** for the Microsoft Entra ID *tenant* that is going to be used for authentication on Azure Cosmos DB for MongoDB vCore clusters.

> [!IMPORTANT]
> Microsoft Entra ID tenant administrator permissions are needed to make the change. See [guidance for troubleshooting permissions](/entra/identity/enterprise-apps/add-application-portal-configure#prerequisites).

# [Azure portal](#tab/portal)

1. Search for 'Microsoft Entra ID' in [Azure portal](https://portal.azure.com/).
1. Open 'Microsoft Entra ID' service.
1. On the **Overview** page of Microsoft Entra ID service in the **Overview** section, search for 'b4fa09d8-5da5-4352-83d9-05c2a44cf431' application ID.
1. Choose 'Azure Cosmos DB for MongoDB vCore AAD Authentication' enterprise application in the search results.
1. In the **Azure Cosmos DB for MongoDB vCore AAD Authentication** enterprise application, choose **Properties** page.
1. Set **Enabled for users to sign-in?** to **Yes** and save the change.

# [Azure CLI](#tab/cli)

```azurecli
az ad sp update --id b4fa09d8-5da5-4352-83d9-05c2a44cf431 --set accountEnabled=true
```
---

> [!NOTE]
> Editing enterprise application's properties such as "Enabled for users to sign-in" requires permissions granted to a user with privileges to update enterprise application properties. users, such as **Enterprise application owner**, must have the *"update enterprise application properties"* permisssion. For more information, see [Microsoft Entra least privileged users by task - Enterprise applications](/entra/identity/user-based-access-control/delegate-by-task#enterprise-applications).

## Enable Microsoft Entra ID authentication method on Azure Cosmos DB for MongoDB vCore cluster

When an Azure Cosmos DB for MongoDB vCore cluster is created, only native DocumentDB authentication is enabled on it. To allow Microsoft Entra ID users access cluster's database, Microsoft Entra ID authentication method should be enabled. Follow these steps to enable Microsoft Entra ID authentication method in [Azure CLI](/cli/azure/get-started-with-azure-cli):

1. Enable Microsoft Entra ID authentication on cluster in addition to the native DocumentDB authentication:
    ```azurecli
    az rest --method PUT --url https://management.azure.com/subscriptions/<subscriptionId>/resourceGroups/<resourceGroup>/providers/Microsoft.DocumentDB/mongoClusters/<clusterName>?api-version=2025-04-01-preview --body "{'location': '<cluterRegion>', 'properties': {'authConfig': {'allowedModes': ['MicrosoftEntraID', 'NativeAuth'] } } }"
    ```
1. Verify that Microsoft Entra ID authentication method is enabled on the cluster:
    ```azurecli
    az rest --method GET --url https://management.azure.com/subscriptions/<subscriptionId>/resourceGroups/<resourceGroup>/providers/Microsoft.DocumentDB/mongoClusters/<clusterName>?api-version=2025-04-01-preview
    ```

If you see the following in the output, Microsoft Entra ID authentication method is enabled on the cluster.

```azurecli
    "authConfig": {
      "allowedModes": [
        "MicrosoftEntraID",
        "NativeAuth" 
    ] 
}
```

## Add Microsoft Entra ID administrative users to Azure Cosmos DB for MongoDB vCore cluster

To add or remove Microsoft Entra ID users with administative permissions on cluster, follow these steps:

1. Get OpenID Connect (OIDC) identifier for the security principal such as Entra ID user that needs to be added to Azure Cosmos DB for MongoDB vCore cluster.
    1. Search for 'Microsoft Entra ID' in [Azure portal](https://portal.azure.com/).
    1. Open 'Microsoft Entra ID' service.
    1. On the **Overview** page of Microsoft Entra ID service in the **Overview** section, search for the user to be added, e.g. dbadmin@contoso.com.
    1. Choose the user account in the search results.
    1. On the **Overview** tab of the **Overview** page of the user account, copy **Object ID** identifier.
        1. Object ID has 12345678-90ab-cdef-1234-1234567890ab format.
        1. This is the OIDC identifier used to login to Azure Cosmos DB for MongoDB vCore cluster.
1. Add Entra ID user as an administrator to the cluster:
    ```azurecli
    az rest --method PUT \
    --url https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.DocumentDB/mongoClusters/{cluster-name}/users/{oidc-identifier}?api-version=2025-04-01-preview \ 
    -- body { "location": "**cluster-region**", "properties": { "identityProvider": { "type": "MicrosoftEntraID", "properties": { "principalType": "User" } }, "roles": [{"db": "admin", "role": "dbOwner"}] } }
    ```
1. Verify that Entra ID account is added to the cluster: 
    ```azurecli
    az rest --method GET \
    --url https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.DocumentDB/mongoClusters/{cluster-name}/users?api-version=2025-04-01-preview
    ```
1. Remove Entra ID user from the cluster: 
    ```azurecli
    az rest --method DELETE \
    --url https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.DocumentDB/mongoClusters/{cluster-name}/users/{oidc-identifier}?api-version=2025-04-01-preview 
    ```

## Connect to Azure Cosmos for MongoDB using Microsoft Entra ID authentication

Microsoft Entra ID integration works with standard MongoDB client tools like **MongoDB Shell**, which aren't Microsoft Entra ID aware and support only specifying the OpenID Connect (OIDC) identificator and password when you're connecting to MongoDB. In such cases, the Microsoft Entra ID token is passed as the password.

We tested the following clients:

- **Mongo Shell command line**.
- **Compass**.

Use the following procedures to authenticate with Microsoft Entra ID as an Azure Cosmos DB for MongoDB vCore user. You can follow along on an Azure virtual machine, or on your local machine.

### Sign in to the user's Azure subscription

Start by authenticating with Microsoft Entra ID by using the [Azure CLI](/cli/azure/get-started-with-azure-cli). This step isn't required in Azure Cloud Shell.

```azurecli
az login
```

The command opens a browser window to the Microsoft Entra ID authentication page. It requires you to give your Microsoft Entra ID user name and password.

The user account name you use to authenticate (for example, user@tenant.onmicrosoft.com) is the one the access token will be generated for in the next step.

### Retrieve the Microsoft Entra ID access token

Use the Azure CLI to acquire an access token for the Microsoft Entra ID authenticated user to access Azure Cosmos for MongoDB. Here's an example:

```azurecli-interactive
az account get-access-token --resource-type arm
```

After authentication is successful, Microsoft Entra ID returns an access token for current Azure subscription:

```json
{
  "accessToken": "[TOKEN]",
  "expiresOn": "[expiration_date_and_time]",
  "subscription": "[subscription_id]",
  "tenant": "[tenant_id]",
  "tokenType": "Bearer"
}
```

The TOKEN is a Base64 string. It encodes all the information about the authenticated user and is associated with the Azure Cosmos DB for MongoDB vCore service. The token is valid for at least 5 minutes with the maximum of 90 minutes. The **expiresOn** defines actual token expiration time.

### Use a token as a password for signing in with Mongo Shell

When connecting, it's best to use the access token as the MongoDB user password.

While using [the Mongo Shell command-line client](https://www.mongodb.com/try/download/shell), the access token needs to be passed through an environment variable. The reason is that the access token exceeds the password length that Mongo Shell can accept directly.

Here's a Windows example:

```cmd
set MONGOPASSWORD=<TOKEN value from the previous step>
```

```powerShell
$env:MONGOPASSWORD='<TOKEN value from the previous step>'
```

Here's a Linux/macOS example:

```bash
export MONGOPASSWORD=<TOKEN value from the previous step>
```

You can also combine the previous two steps together using command substitution. The token retrieval can be encapsulated into a variable and passed directly as a value for `MONGOPASSWORD` environment variable:

```bash
export MONGOPASSWORD=$(az account get-access-token --resource https://token.MongoDB.cosmos.azure.com --query "[accessToken]" -o tsv)
```


> [!NOTE]
> Make sure MONGOPASSWORD variable is set to the Microsoft Entra ID access token for your
> subscription for Microsoft Entra ID authentication. If you need to do MongoDB user authentication
> from the same session you can set MONGOPASSWORD to the MongoDB user password
> or clear the MONGOPASSWORD variable value to enter the password interactively.
> Authentication would fail with the wrong value in MONGOPASSWORD.

Now you can initiate a connection with Azure Cosmos DB for MongoDB vCore using the Microsoft Entra ID user account that the access token was generated for. You would do it as you usually do with the user account as the user and without 'password' parameter in the command line:

```sql
mongosh "host=mycluster.global.MongoDB.cosmos.azure.com user=user@tenant.onmicrosoft.com sslmode=require"
```

### Use a token as a password for signing in with Compass

To connect by using a Microsoft Entra ID token with Compass, follow these steps:

1. Copy Entra ID connection string to the **URI** field. 
1. Open **Advanced Connect Options**.
1. On the **Authentication** tab, select **OIDC**. 
1. Enter the Microsoft Entra ID access token when you're prompted.

Here are some essential considerations when you're connecting:

- Be sure to use [OIDC identifier](#add-microsoft-entra-id-administrative-users-to-azure-cosmos-db-for-mongodb-vcore-cluster) for the Entra ID user as the user name.
- The access token's validity is 5 minutes to 90 minutes. You should get the access token before initiating the sign-in to Azure Cosmos for MongoDB.

You're now authenticated to your Azure Cosmos for MongoDB vCore cluster in Compass through Microsoft Entra ID authentication.

## Preivew limitations

The following section describes functional limits in the Azure Cosmos DB for MongoDB vCore service when Microsoft Entra ID preview is used.
- Entra ID is not supported on replica clusters.
- Entra ID is not supported on restored clusters. 

## Next steps

- Learn about [authentication in Azure Cosmos DB for MongoDB vCore](./concepts-authentication.md)
- Check out [Microsoft Entra ID limits and limitations in Azure Cosmos DB for MongoDB vCore](./reference-limits.md#azure-active-directory-authentication)
- Review [Microsoft Entra ID fundamentals](/entra/fundamentals/whatis)
- [Learn more about SQL GRANT in MongoDB](https://www.MongoDB.org/docs/current/sql-grant.html)
