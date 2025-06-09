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
ms.date: 05/27/2025
ms.custom:
  - devx-track-rust
  - build-2025
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database developer, I want to build a Rust console application to quickly and securely connect to and query my database and collections.
---

# Configure Microsoft Entra ID authentication for an Azure Cosmos DB for MongoDB vCore cluster

In this article, you learn how to configure Microsoft Entra ID authentication for an Azure Cosmos DB for MongoDB vCore. The steps in this guide configure an existing Azure Cosmos DB for MongoDB vCore cluster to use Microsoft Entra ID authentication with your human identity (currently signed-in account). Microsoft Entra ID authentication enables secure and seamless access to your database by using your organization's existing identities. This guide goes through the steps to set up authentication, register users or service principals, and validate the configuration.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prereq-existing-cluster.md)]

[!INCLUDE[Prerequisite - Azure CLI](includes/prereq-azure-cli.md)]

## Get signed-in identity metadata

First, get the unique identifier for your currently signed-in identity.

1. Get the details for the currently logged-in account using `az ad signed-in-user`.

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

1. Record the value of the `id` property. This property is the unique identifier for your principal and is sometimes referred to as the **principal ID**. You use this value in the next series of steps.

## Configure existing cluster for authentication

When you create an Azure Cosmos DB for MongoDB vCore cluster, the cluster is configured for native authentication by default. Use the Azure CLI to configure your existing cluster to support Microsoft Entra ID authentication. Then, configure the cluster to map a user to your signed-in identity.

1. Now, get the `authConfig` property from your existing cluster using `az resource show`.

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
      "allowedModes": [
        "NativeAuth"
      ]
    }
    ```

1. Then, update the existing cluster with an HTTP `PATCH` operation by adding the `MicrosoftEntraID` value to `allowedModes`.

    ```azurecli-interactive
    az resource patch \
        --resource-group "<resource-group-name>" \
        --name "<cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --properties '{"authConfig":{"allowedModes":["MicrosoftEntraID","NativeAuth"]}}' \
        --latest-include-preview
    ```

    > [!TIP]
    > If you're using the Azure Cloud Shell, you can upload/download files directly to the shell. For more information, see [managed files in Azure Cloud Shell](/azure/cloud-shell/using-the-shell-window#upload-and-download-files).
    >
    > Also, if you prefer to use the Azure REST API directly with `az rest`, use this alternative command:
    >
    > ```azurecli-interactive
    > az rest \
    >     --method "PUT" \
    >     --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>?api-version=2025-04-01-preview" \
    >     --body '{"location":"<cluster-region>","properties":{"authConfig":{"allowedModes":["MicrosoftEntraID","NativeAuth"]}}}'
    > ```
    >

1. Validate that the configuration was successful by using `az resource show` again and observing the entire cluster's configuration which includes `properties.authConfig`.

    ```azurecli-interactive
    az resource show \
        --resource-group "<resource-group-name>" \
        --name "<cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --latest-include-preview
    ```

    ```output
    {
      ...
      "properties": {
        ...
        "authConfig": {
          "allowedModes": [
            "MicrosoftEntraID",
            "NativeAuth"
          ]
        },
        ...
      },
      ...
    }
    ```

1. Use `az resource create` to create a new resource of type `Microsoft.DocumentDB/mongoClusters/users`. Compose the name of the resource by concatenating the **name of the parent cluster** and the **principal ID** of your identity.
 
    ```azurecli-interactive
    az resource create \
        --resource-group "<resource-group-name>" \
        --name "<cluster-name>/users/<principal-id>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters/users" \
        --location "<cluster-region>" \
        --properties '{"identityProvider":{"type":"MicrosoftEntraID","properties":{"principalType":"User"}},"roles":[{"db":"admin","role":"dbOwner"}]}' \
        --latest-include-preview
    ```

    > [!TIP]
    > For example, if your parent resource is named `example-cluster` and your principal ID was `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb`, the name of the resource would be:
    >
    > ```json
    > "example-cluster/users/aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"
    > ```
    >
    > Also, if you're registering a service principal, like a managed identity, you would replace the `identityProvider.properties.principalType` property's value with `ServicePrincipal`.
    > 
    > Finally, if you prefer to use the Azure REST API directly with `az rest`, use this alternative command:
    >
    > ```azurecli-interactive
    > az rest \
    >     --method "PUT" \
    >     --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>/users/<principal-id>?api-version=2025-04-01-preview" \
    >     --body '{"location":"<cluster-region>","properties":{"identityProvider":{"type":"MicrosoftEntraID","properties":{"principalType":"User"}},"roles":[{"db":"admin","role":"dbOwner"}]}}'
    > ```
    >

> [!NOTE]
> Microsoft Entra ID users added to the cluster are going to be in addition to native DocumentDB users defined on the same cluster. An Azure Cosmos DB for MongoDB vCore cluster is created with at least one built-in native DocumentDB user. You can add more native DocumentDB users after cluster provisioning is completed.

## Connect to the cluster

You can connect to the cluster using either a connection URI or a custom settings object from the driver for your preferred language. In either option, the **scheme** must be set to `mongodb+srv` to connect to the replica set. The **host** is at either the `*.global.mongocluster.cosmos.azure.com` or `*.mongocluster.cosmos.azure.com` domain depending on whether you're using the current cluster or global read-write endpoint. The `+srv` scheme and the `*.global.*` host ensures that your client is dynamically connected to the appropriate writable cluster in a multi-cluster configuration even if a region swap operation occurs. In a single-cluster configuration, you can use either host indiscriminately.

The `tls` setting must also be enabled. The remaining recommended settings are best practice configuration settings.

| Option | Value |
| --- | --- |
| *scheme* | `mongodb+srv` |
| *host* | `<cluster-name>.global.mongocluster.cosmos.azure.com` or `<cluster-name>.mongocluster.cosmos.azure.com` |
| `tls` | `true` |
| `authMechanism` | `MONGODB-OIDC` |
| `retrywrites` | `false` |
| `maxIdleTimeMS` | `120000` |

### [Connection URI](#tab/connection-uri)

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

## Related content

- [Microsoft Entra ID authentication in Azure Cosmos DB for MongoDB vCore overview](entra-authentication.md)
- Check [limitations of Microsoft Entra ID](./limits.md#authentication-and-access-control-rbac) in Azure Cosmos DB for MongoDB vCore
- [Connect using a console application](how-to-build-dotnet-console-app.md)
