---
title: Configure Microsoft Entra ID authentication
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn how to manage authentication and set up Microsoft Entra ID users for authentication on Azure Cosmos DB for MongoDB vCore clusters.
author: seesharprun
ms.author: sidandrews
ms.reviewer: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 09/17/2025
ms.custom:
  - devx-track-rust
  - build-2025
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database developer, I want to build a Rust console application to quickly and securely connect to and query my database and collections.
---

# Configure Microsoft Entra ID authentication for an Azure Cosmos DB for MongoDB vCore cluster

In this article, you learn how to configure [Microsoft Entra ID authentication](./entra-authentication.md) for an Azure Cosmos DB for MongoDB vCore. The steps in this guide configure an existing Azure Cosmos DB for MongoDB vCore cluster to use Microsoft Entra ID authentication with your human identity (currently signed-in account) or a Microsoft Entra ID security principal such as managed identity. Microsoft Entra ID authentication enables secure and seamless access to your database by using your organization's existing identities. This guide goes through the steps to set up authentication, register users or service principals, and validate the configuration.

When you create an Azure Cosmos DB for MongoDB vCore cluster, cluster is configured to use native authentication by default. To enable authentication using Entra ID, [turn on the Entra ID authentication method](#manage-cluster-authentication-methods) and [add Entra ID users](#manage-entra-id-users-on-the-cluster) to the cluster.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prereq-existing-cluster.md)]

[!INCLUDE[Prerequisite - Azure CLI](includes/prereq-azure-cli.md)]

## Get identity metadata

### Get unique identifier for Entra ID user management

First, get the unique identifier used to manage Entra ID principals on the cluster.

1. Get the details for *the currently logged-in account* using `az ad signed-in-user`.

    ```azurecli-interactive
    az ad signed-in-user show
    ```

1. Get the details for another account using `az ad user show`.

    ```azurecli-interactive
    az ad user show --id kai@adventure-works.com
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

1. Record the value of the `id` property. This property is the unique identifier for your principal and is sometimes referred to as the **principal ID**. You use this value in the next series of steps.

### Get friendly name using unique identifier

When you need to get a friendly name using unique identifier, follow these steps.

1. Get the details for another account using `az ad user show`.

    ```azurecli-interactive
    az ad user show --id aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb
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

1. Note the value of the `mail` and `displayName` properties.

### Get unique identifier for an Entra ID service principal

To use a managed identity in your application or to log in using Entra ID credentials in tools like the MongoDB shell or Compass, you need to retrieve the `clientID` of the managed identity.

1. Get the details for the managed identity using a `GET` REST API call. Replace variables that start with `$` sign with the actual values.

    ```azurecli-interactive
    az rest --method "GET" --url "https://management.azure.com/subscriptions/$subscription-id/resourcegroups/$resource-group-name/providers/microsoft.managedidentity/userassignedidentities/$managed-identity-name?api-version=2024-11-30" 
    ```

1. The command outputs a JSON response containing various fields.

    ```json
    {
      "location": "eastus",
      "name": "managed-identity-name",
      "properties": {
        "clientId": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        "isolationScope": "None",
        "principalId": "cccccccc-0000-1111-2222-bbbbbbbbbbbb",
        "tenantId": "dddddddd-0000-1111-2222-bbbbbbbbbbbb"
      },
      "tags": {},
      "type": "Microsoft.ManagedIdentity/userAssignedIdentities"
    }
    ```

1. Note `clientID` value in the output.

## Manage cluster authentication methods 
Use the following steps to enable Microsoft Entra ID authentication method on your existing cluster. Then, add an Entra ID user mapped to your signed-in identity to the cluster. You can have *native DocumentDB authentication only* or *native DocumentDB and Microsoft Entra ID* authentication methods enabled on the cluster.  

### [Azure portal](#tab/portal)

1. On the cluster sidebar, under **Settings**, select **Authentication**.

1. In **Authentication methods** section, select **Native DocumentDB and Microsoft Entra ID** to enable Microsoft Entra ID authentication.

    :::image type="content" source="media/how-to-configure-entra-authentication/enable-entra-id-authentication-method.png" alt-text="Screenshot that shows how to enable Microsoft Entra ID authentication method on an existing cluster." lightbox="media/how-to-configure-entra-authentication/enable-entra-id-authentication-method.png":::

1. Select **Save** to confirm the authentication method changes. 

    :::image type="content" source="media/how-to-configure-entra-authentication/save-authentication-method-change.png" alt-text="Screenshot that shows the location of Save button for confirmation of the authentication method changes on an existing cluster." lightbox="media/how-to-configure-entra-authentication/save-authentication-method-change.png":::

### [Azure CLI](#tab/cli)

1. To enable Microsoft Entra ID on the cluster, update the existing cluster with an HTTP `PATCH` operation by adding the `MicrosoftEntraID` value to `allowedModes` in the `authConfig` property.

    ```azurecli-interactive
    az resource patch \
        --resource-group "<resource-group-name>" \
        --name "<cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --properties "{\"authConfig\":{\"allowedModes\":[\"MicrosoftEntraID\",\"NativeAuth\"]}}" \
        --latest-include-preview
    ```

1. To disable Microsoft Entra ID authentication method on the cluster, update the existing cluster with an HTTP `PATCH` operation by overwriting the current values in `allowedModes` in the `authConfig` property with `NativeAuth`.

    ```azurecli-interactive
    az resource patch \
        --resource-group "<resource-group-name>" \
        --name "<cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --properties "{\"authConfig\":{\"allowedModes\":[\"NativeAuth\"]}}" \
        --latest-include-preview
    ```

### [REST APIs](#tab/rest-apis)

You can use the Azure REST API directly or wrapped into `az rest` from Azure CLI environment.

1.  Use this command to add Microsoft Entra ID authentication method to the cluster:
    
     ```azurecli-interactive
     az rest \
         --method "PUT" \
         --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>?api-version=2025-07-01-preview" \
         --body "{\"location\":\"<cluster-region>\",\"properties\":{\"authConfig\":{\"allowedModes\":[\"MicrosoftEntraID\",\"NativeAuth\"]}}}"
     ```

1.  Use this command to remove Microsoft Entra ID authentication method from the cluster and leave only native DocumentDB authentication method enabled:
    
     ```azurecli-interactive
     az rest \
         --method "PUT" \
         --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>?api-version=2025-07-01-preview" \
         --body "{\"location\":\"<cluster-region>\",\"properties\":{\"authConfig\":{\"allowedModes\":\"NativeAuth\"}}}"
     ```

    > [!TIP]
    > If you're using the Azure Cloud Shell, you can upload/download files directly to the shell. For more information, see [managed files in Azure Cloud Shell](/azure/cloud-shell/using-the-shell-window#upload-and-download-files).


---

## View authentication methods enabled on the cluster

Follow these steps to see authentication methods currently enabled on the cluster. 

### [Azure portal](#tab/portal)

1. On the cluster sidebar, under **Settings**, select **Authentication**.

1. In the **Authentication methods** section, check authentication methods currently enabled on the cluster. 

    :::image type="content" source="media/how-to-configure-entra-authentication/view-currently-enabled-authentication-methods.png" alt-text="Screenshot that shows how view authentication methods currently enabled on the cluster." lightbox="media/how-to-configure-entra-authentication/view-currently-enabled-authentication-methods.png":::

### [Azure CLI](#tab/cli)

1. Get the `authConfig` property from your existing cluster using `az resource show`.

    ```azurecli-interactive
    az resource show \
        --resource-group "<resource-group-name>" \
        --name "<cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --query "properties.authConfig" \
        --latest-include-preview
    ```

1. Observe the output. If Microsoft Entra ID authentication isn't configured, the output includes only the `NativeAuth` value in the `allowedModes` array.

    ```output
    {
      "authConfig": {
        "allowedModes": [
            "NativeAuth"
      ] }
    }
    ```

1. If Microsoft Entra ID authentication is enabled on the cluster, the output includes both the `NativeAuth` and `MicrosoftEntraID` values in the `allowedModes` array.

    ```output
    {
      "authConfig": {
        "allowedModes": [
            "NativeAuth",
            "MicrosotEntraID"
              ] }
    }
    ```

### [REST APIs](#tab/rest-apis)

1.  Use this command to check authentication methods currently enabled on the cluster:
    
     ```azurecli-interactive
     az rest \
         --method "GET" \
         --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>?api-version=2025-07-01-preview" 
     ```
1. Observe the output. If Microsoft Entra ID authentication isn't configured, the output includes only the `NativeAuth` value in the `allowedModes` array.

    ```output
    {
      "authConfig": {
        "allowedModes": [
            "NativeAuth"
      ] }
    }
    ```

1. If Microsoft Entra ID authentication is enabled on the cluster, the output includes both the `NativeAuth` and `MicrosoftEntraID` values in the `allowedModes` array.

    ```output
    {
      "authConfig": {
        "allowedModes": [
            "NativeAuth",
            "MicrosotEntraID"
              ] }
        }
    ```

---

## Manage Entra ID users on the cluster

Follow these steps to add or remove [administrative Entra ID users](./entra-authentication.md#administrative-and-nonadministrative-access-for-microsoft-entra-id-principals) to cluster. 

### [Azure portal](#tab/portal)

1. Select a cluster with [Microsoft Entra ID authentication method enabled](#manage-cluster-authentication-methods).

1. On the cluster sidebar, under **Settings**, select **Authentication**.

1. To add administrative Entra ID users:

    1. In the **Microsoft Entra ID authentication** section, select **+Add Microsoft Entra ID** to open the side panel that allows to add Entra ID users and security principals to the cluster.
    
        :::image type="content" source="media/how-to-configure-entra-authentication/open-side-panel-to-add-entra-id-users.png" alt-text="Screenshot that shows how to open the side panel that allows to add Microsoft Entra ID users and security principals to the cluster." lightbox="media/how-to-configure-entra-authentication/open-side-panel-to-add-entra-id-users.png":::
    
    1. In the **Select Microsoft Entra ID roles** side panel, select one or more Entra ID users and confirm your choice by selecting **Select**.
        
        :::image type="content" source="media/how-to-configure-entra-authentication/select-entra-id-users-to-add-to-cluster.png" alt-text="Screenshot that shows how to select and add administrative Microsoft Entra ID users and security principals to the cluster." lightbox="media/how-to-configure-entra-authentication/select-entra-id-users-to-add-to-cluster.png":::

    > [!NOTE]
    > When administrative Microsoft Entra ID users are added to the cluster, their identifiers in `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb` format not human readable names such as `kai@adventure-works.com` are added to the cluster.

1. Select **Save** to confirm the authentication method changes.
    
1. To remove administrative Entra ID users from the cluster:

    1. [Get Entra ID identifiers](#get-unique-identifier-for-entra-id-user-management) for the users to be removed from the cluster.

    1. In the **Microsoft Entra ID authentication** section, select **Remove** next to the user's identifier to remove that user from the cluster.

    :::image type="content" source="media/how-to-configure-entra-authentication/remove-entra-id-user-from-cluster.png" alt-text="Screenshot that shows location of the Remove icon used to remove Microsoft Entra ID users and security principals from the cluster." lightbox="media/how-to-configure-entra-authentication/remove-entra-id-user-from-cluster.png":::

    > [!IMPORTANT]
    > User is removed from the cluster right after **Remove** is selected.

### [Azure CLI](#tab/cli)

1. [Get the unique ID](#get-unique-identifier-for-entra-id-user-management) of the user or service principal that needs to be added to or removed from the cluster.

1. To add administrative Entra ID users, use `az resource create`. This command creates a new resource of type `Microsoft.DocumentDB/mongoClusters/users`. Compose the name of the resource by concatenating the **name of the parent cluster** and the **principal ID** of your identity.
 
    ```azurecli-interactive
    az resource create \
        --resource-group "<resource-group-name>" \
        --name "<cluster-name>/users/<principal-id>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters/users" \
        --location "<cluster-region>" \
        --properties "{\"identityProvider\":{\"type\":\"MicrosoftEntraID\",\"properties\":{\"principalType\":\"User\"}},\"roles\":[{\"db\":\"admin\",\"role\":\"root\"}]}" \
        --latest-include-preview
    ```

    > [!TIP]
    > For example, if your parent resource is named `example-cluster` and your principal ID was `aaaaaaaa-bbbb-cccc-1111-222222222222`, the name of the resource would be:
    >
    > ```json
    > "example-cluster/users/aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"
    > ```
    >
    > Also, if you're registering a service principal, like a managed identity, you would replace the `identityProvider.properties.principalType` property's value with `ServicePrincipal`.
     
1. To remove administrative Entra ID users, use `az resource delete`. This command deletes resource of type `Microsoft.DocumentDB/mongoClusters/users`. Compose the name of the resource by concatenating the **name of the parent cluster** and the **principal ID** of your identity.
 
    ```azurecli-interactive
    az resource delete \
        --resource-group "<resource-group-name>" \
        --name "<cluster-name>/users/<principal-id>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters/users" \
        --latest-include-preview
    ```
    
### [REST APIs](#tab/rest-apis)

1. [Get the unique ID](#get-unique-identifier-for-entra-id-user-management) of the user or service principal that needs to be added to or removed from the cluster.

1.  To add administrative Entra ID users to the cluster, use PUT Azure REST API call with this `az rest` command:
    
     ```azurecli-interactive
     az rest \
         --method "PUT" \
         --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>/users/<principal-id>?api-version=2025-07-01-preview" \
         --body "{\"location\":\"<cluster-region>\",\"properties\":{\"identityProvider\":{\"type\":\"MicrosoftEntraID\",\"properties\":{\"principalType\":\"User\"}},\"roles\":[{\"db\":\"admin\",\"role\":\"root\"}]}}"
     ```

    > [!TIP]
    > For example, if your parent resource is named `example-cluster` and your principal ID was `aaaaaaaa-bbbb-cccc-1111-222222222222`, the name of the resource would be:
    >
    > ```json
    > "example-cluster/users/aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"
    > ```
    >
    > Also, if you're registering a service principal, like a managed identity, you would replace the `identityProvider.properties.principalType` property's value with `ServicePrincipal`.
 
1.  To remove administrative Entra ID users from the cluster, use DELETE Azure REST API call with this `az rest` command:
    
     ```azurecli-interactive
     az rest \
         --method "DELETE" \
         --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>/users/<principal-id>?api-version=2025-07-01-preview" 
     ```
    

---


## View Entra ID users on the cluster

When you view [administrative users](./entra-authentication.md#administrative-and-nonadministrative-access-for-microsoft-entra-id-principals) on a cluster, there's always one native built-in administrative user created during cluster provisioning and all administrative Entra ID users added to the cluster listed.

Follow these steps to see all [administrative Entra ID users](./entra-authentication.md#administrative-and-nonadministrative-access-for-microsoft-entra-id-principals) added to cluster. 

### [Azure portal](#tab/portal)

1. Select a cluster with [Microsoft Entra ID authentication method enabled](#manage-cluster-authentication-methods).

1. On the cluster sidebar, under **Settings**, select **Authentication**.

1. In the **Microsoft Entra ID authentication** section, find the list of object IDs (unique identifiers) for the administrative Entra ID users added to the cluster.

    :::image type="content" source="media/how-to-configure-entra-authentication/view-entra-id-users-on-cluster.png" alt-text="Screenshot that shows how to view the list of administrative Microsoft Entra ID users on the cluster." lightbox="media/how-to-configure-entra-authentication/view-entra-id-users-on-cluster.png":::

1. To get friendly names using a unique identifier, [follow these steps](#get-friendly-name-using-unique-identifier). 

### [Azure CLI](#tab/cli)

Use commands on the **REST APIs** tab to list administrative users on the cluster.

### [REST APIs](#tab/rest-apis)

1. Use this command to list all administrative users on the cluster:
    
     ```azurecli-interactive
     az rest \
         --method "GET" \
         --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>/users?api-version=2025-07-01-preview" 
     ```
1. Observe the output. The output includes an array of administrative user accounts on the cluster. This array has one built-in native administrative users and all administrative Entra ID user and service principals added to the cluster.

    ```output
    {
      "id": "/subscriptions/<subscription-id>>/resourceGroups/<resource-group-name>>/providers/Microsoft.DocumentDB/mongoClusters/<cluser-name>>/users/<user's-unique-id>",
      "name": "user's-unique-id",
      "properties": {
        "identityProvider": {
          "properties": {
            "entraTenant": "entra-tenant-id",
            "principalType": "User"
          },
          "type": "MicrosoftEntraID"
        },
        ...
        "user": "user's-unique-id"
      },
        ...
      "type": "Microsoft.DocumentDB/mongoClusters/users"
    }
    ```

1. If Microsoft Entra ID authentication is enabled on the cluster, the output includes both the `NativeAuth` and `MicrosoftEntraID` values in the `allowedModes` array.

    ```output
    {
      "authConfig": {
        "allowedModes": [
            "NativeAuth",
            "MicrosotEntraID"
              ] }
        }
    ```


---


> [!NOTE]
> An Azure Cosmos DB for MongoDB vCore cluster is created with one built-in native DocumentDB user. You can [add more native DocumentDB users](./secondary-users.md) after cluster provisioning is completed. Microsoft Entra ID users added to the cluster are going to be in addition to native DocumentDB users defined on the same cluster.


## Connect to the cluster

You can connect to the cluster using either a connection URI or a custom settings object from the driver for your preferred language. In either option, the **scheme** must be set to `mongodb+srv` to connect to the cluster. The **host** is at either the `*.global.mongocluster.cosmos.azure.com` or `*.mongocluster.cosmos.azure.com` domain depending on whether you're using [the current cluster or global read-write endpoint](./how-to-cluster-replica.md#use-connection-strings). The `+srv` scheme and the `*.global.*` host ensures that your client is dynamically connected to the appropriate writable cluster in a multi-cluster configuration even if [a region swap operation occurs](./cross-region-replication.md#replica-cluster-promotion). In a single-cluster configuration, you can use either connection string indiscriminately.

The `tls` setting must also be enabled. The remaining recommended settings are best practice configuration settings.

| Option | Value |
| --- | --- |
| *scheme* | `mongodb+srv` |
| *host* | `<cluster-name>.global.mongocluster.cosmos.azure.com` or `<cluster-name>.mongocluster.cosmos.azure.com` |
| `tls` | `true` |
| `authMechanism` | `MONGODB-OIDC` |
| `retrywrites` | `false` |
| `maxIdleTimeMS` | `120000` |

### [Azure portal](#tab/azure-portal)

On the cluster properties page in the Azure portal, under **Settings**, open **Connection strings**. The **Connection strings** page contains connection strings for the authentication methods enabled on the cluster. Microsoft Entra ID connection strings are in the **Microsoft Entra ID** section.

- **Global**
 
    ```output
    mongodb+srv://<cluster-name>.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=MONGODB-OIDC&retrywrites=false&maxIdleTimeMS=120000
    ```

- **Cluster**

    ```output
    mongodb+srv://<cluster-name>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=MONGODB-OIDC&retrywrites=false&maxIdleTimeMS=120000
    ```


### [Node.js](#tab/nodejs)

```typescript
const AzureIdentityTokenCallback = async (params: OIDCCallbackParams, credential: TokenCredential): Promise<OIDCResponse> => {
    const tokenResponse: AccessToken | null = await credential.getToken(['https://ossrdbms-aad.database.windows.net/.default']);
    return {
        accessToken: tokenResponse?.token || '',
        expiresInSeconds: (tokenResponse?.expiresOnTimestamp || 0) - Math.floor(Date.now() / 1000)
    };
};

const clusterName: string = '<azure-cosmos-db-mongodb-vcore-cluster-name>';

const credential: TokenCredential = new DefaultAzureCredential();

const client = new MongoClient(
    `mongodb+srv://${clusterName}.global.mongocluster.cosmos.azure.com/`, {
    connectTimeoutMS: 120000,
    tls: true,
    retryWrites: true,
    authMechanism: 'MONGODB-OIDC',
    authMechanismProperties: {
        OIDC_CALLBACK: (params: OIDCCallbackParams) => AzureIdentityTokenCallback(params, credential),
        ALLOWED_HOSTS: ['*.azure.com']
    }
}
);
```

### [Python](#tab/python)

```python
class AzureIdentityTokenCallback(OIDCCallback):
    def __init__(self, credential):
        self.credential = credential

    def fetch(self, context: OIDCCallbackContext) -> OIDCCallbackResult:
        token = self.credential.get_token(
            "https://ossrdbms-aad.database.windows.net/.default").token
        return OIDCCallbackResult(access_token=token)

clusterName = "<azure-cosmos-db-mongodb-vcore-cluster-name>"

credential = DefaultAzureCredential()
authProperties = {"OIDC_CALLBACK": AzureIdentityTokenCallback(credential)}

client = MongoClient(
    f"mongodb+srv://{clusterName}.global.mongocluster.cosmos.azure.com/",
    connectTimeoutMS=120000,
    tls=True,
    retryWrites=True,
    authMechanism="MONGODB-OIDC",
    authMechanismProperties=authProperties
)
```

### [C#](#tab/csharp)

```csharp
string tenantId = "<microsoft-entra-tenant-id>";
string clusterName = "<azure-cosmos-db-mongodb-vcore-cluster-name>";

DefaultAzureCredential credential = new();
AzureIdentityTokenHandler tokenHandler = new(credential, tenantId);

MongoUrl url = MongoUrl.Create($"mongodb+srv://{clusterName}.global.mongocluster.cosmos.azure.com/");
MongoClientSettings settings = MongoClientSettings.FromUrl(url);
settings.UseTls = true;
settings.RetryWrites = false;
settings.MaxConnectionIdleTime = TimeSpan.FromMinutes(2);
settings.Credential = MongoCredential.CreateOidcCredential(tokenHandler);
settings.Freeze();

MongoClient client = new(settings);

internal sealed class AzureIdentityTokenHandler(
    TokenCredential credential,
    string tenantId
) : IOidcCallback
{
    private readonly string[] scopes = ["https://ossrdbms-aad.database.windows.net/.default"];

    public OidcAccessToken GetOidcAccessToken(OidcCallbackParameters parameters, CancellationToken cancellationToken)
    {
        AccessToken token = credential.GetToken(
            new TokenRequestContext(scopes, tenantId: tenantId),
            cancellationToken
        );

        return new OidcAccessToken(token.Token, token.ExpiresOn - DateTimeOffset.UtcNow);
    }

    public async Task<OidcAccessToken> GetOidcAccessTokenAsync(OidcCallbackParameters parameters, CancellationToken cancellationToken)
    {
        AccessToken token = await credential.GetTokenAsync(
            new TokenRequestContext(scopes, parentRequestId: null, tenantId: tenantId),
            cancellationToken
        );

        return new OidcAccessToken(token.Token, token.ExpiresOn - DateTimeOffset.UtcNow);
    }
}
```
---

## Authenticate to the cluster using Entra ID in MongoDB shell and Compass

You can use Entra ID authentication in MongoDB shell and MongoDB Compass tools. One of the common tasks performed in the tools with Entra ID authentication is management of the secondary Entra ID users on the cluster. [Administrative Entra ID user](./entra-authentication.md#administrative-and-nonadministrative-access-for-microsoft-entra-id-principals) needs to be authenticated in MongoDB shell, Compass, or other MongoDB management tool in order to manage secondary Entra ID users on the cluster.

An Azure managed identity is used to login using Entra ID to [MonogDB shell and Compass](https://www.mongodb.com/try/download/shell). Assign managed identity to an Azure virtual machine (VM) and log in to the cluster from that VM using MongoDB shell or Compass.

### Connect to the cluster using Entra ID in MongoDB shell

1. Create a [user-assigned managed identity](/entra/identity/managed-identities-azure-resources/manage-user-assigned-managed-identities-azure-portal#create-a-user-assigned-managed-identity).
1. [Assign managed identity to a virtual machine](/entra/identity/managed-identities-azure-resources/how-to-configure-managed-identities?pivots=qs-configure-portal-windows-vm#user-assigned-managed-identity).
1. [Add managed identity to the cluster](#manage-entra-id-users-on-the-cluster) as an Entra ID user using [the managed identity metadata](#get-unique-identifier-for-an-entra-id-service-principal).
1. To connect to the cluster, use the following connection string in MongoDB shell on the VM:

    ```output
    mongodb+srv://<clientID>@<cluster-name>.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=MONGODB-OIDC&retrywrites=false&maxIdleTimeMS=120000
    ```
    where `clientID` is [the managed identity's client ID](#get-identity-metadata).

### Connect to the cluster using Entra ID in MongoDB Compass

Use the following steps to use Entra ID to authenticate to the cluster in MongoDB Compass.

1. Create a [user-assigned managed identity](/entra/identity/managed-identities-azure-resources/manage-user-assigned-managed-identities-azure-portal#create-a-user-assigned-managed-identity).
1. [Assign managed identity to a virtual machine](/entra/identity/managed-identities-azure-resources/how-to-configure-managed-identities?pivots=qs-configure-portal-windows-vm#user-assigned-managed-identity).
1. [Add managed identity to the cluster](#manage-entra-id-users-on-the-cluster) as an Entra ID user using [the managed identity metadata](#get-unique-identifier-for-an-entra-id-service-principal).
1. Run MongoDB Compass on the VM.
1. Select `+` sign on the left side next to **Connections** to add a new connection.
1. Make sure **Edit Connection String** toggle is enabled in the **New Connection** window.
1. Paste connection string into the **URI** input box.
1. Open **Advanced Connection Options**.
1. On the **General** tab, make sure `mongodb+srv` is selected under **Connection String Scheme**.
1. Go to the **Authentication** tab. 
1. Make sure **OIDC** is selected.
1. Open **OIDC Options**.
1. Set **Consider Target Endpoint Trusted** option.
1. Select **Save & Connect**.

## Related content

- [Microsoft Entra ID authentication in Azure Cosmos DB for MongoDB vCore overview](entra-authentication.md)
- Check [limitations of Microsoft Entra ID](./limits.md#authentication-and-access-control-rbac) in Azure Cosmos DB for MongoDB vCore
- [Connect using a console application](how-to-build-dotnet-console-app.md)
