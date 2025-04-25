---
title: Use Microsoft Entra ID and native DocumentDB users for authentication with Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn how to manage authentication and set up Microsoft Entra ID users for authentication on Azure Cosmos DB for MongoDB vCore clusters.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 04/20/2025
appliesto:
  - ✅ MongoDB vCore
---

# Use Microsoft Entra ID users for authentication with Azure Cosmos DB for MongoDB vCore

> [!IMPORTANT]
> Microsoft Entra ID authentication in Azure Cosmos DB for MongoDB vCore is currently in preview.
> This preview version is provided without a service level agreement, and it isn't recommended
> for production workloads. Certain features might not be supported or might have constrained
> capabilities.

In this article, you configure administrative Microsoft Entra ID users to be used with Azure Cosmos DB for MongoDB vCore. You also learn how to use a Microsoft Entra ID token with Azure Cosmos DB for MongoDB vCore. Microsoft Entra ID user can be a user or a service principal.

Microsoft Entra ID users added to the cluster are going to be in addition to native DocumentDB users defined on the cluster. An Azure Cosmos DB for MongoDB vCore cluster is created with one built-in native DocumentDB user. You can add more native DocumentDB users after cluster provisioning is completed.

## Prerequisites

1. [An Azure Cosmos DB for MongoDB vCore cluster](./quickstart-portal.md)
1. [A Microsoft Entra ID tenant](/entra/identity-platform/quickstart-create-new-tenant)  

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

To add or remove Microsoft Entra ID users with administrative permissions on cluster, follow these steps:

1. Get OpenID Connect (OIDC) identifier for the security principal such as Entra ID user that needs to be added to Azure Cosmos DB for MongoDB vCore cluster.
    # [Azure portal](#tab/portal)
    1. Search for 'Microsoft Entra ID' in [Azure portal](https://portal.azure.com/).
    1. Open 'Microsoft Entra ID' service.
    1. On the **Overview** page of Microsoft Entra ID service in the **Overview** section, search for the user to be added, e.g. dbadmin@contoso.com.
    1. Choose the user account in the search results.
    1. On the **Overview** tab of the **Overview** page of the user account, copy **Object ID** identifier.
        1. Object ID has 12345678-90ab-cdef-1234-1234567890ab format.
        1. This is the OIDC identifier used to log in to Azure Cosmos DB for MongoDB vCore cluster.
        1. 
    # [Azure CLI](#tab/cli)
    1. ```azurecli
       az rest --method GET --url https://graph.microsoft.com/v1.0/users/{user-name}
       ```
       1. {user-name} is the Entra ID account for authentication. For example, user@tenant.onmicrosoft.com.
       1. **id** field in the output is the OIDC identifier.
1. Add Entra ID user as an administrator to the cluster:
    ```azurecli
    az rest --method PUT \
    --url https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.DocumentDB/mongoClusters/{cluster-name}/users/{oidc-identifier}?api-version=2025-04-01-preview \ 
    -- body { "location": "<cluster-region>", "properties": { "identityProvider": { "type": "MicrosoftEntraID", "properties": { "principalType": "User" } }, "roles": [{"db": "admin", "role": "dbOwner"}] } }
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

## Connect to Azure Cosmos DB for MongoDB using Microsoft Entra ID authentication

### Sign in to the user's Azure subscription

Start by authenticating with Microsoft Entra ID by using the [Azure CLI](/cli/azure/get-started-with-azure-cli). This step isn't required in Azure Cloud Shell.

```azurecli
az login
```

The command opens a browser window to the Microsoft Entra ID authentication page. It requires you to give your Microsoft Entra ID user name and password.

The user account name you use to authenticate (for example, user@tenant.onmicrosoft.com) is the one the access token will be generated for in the next step.

### Connection string for OIDC authentication using Microsoft Entra ID access token

Use the following connection string to connect to an Azure Cosmos DB for MonogDB vCore cluster using OIDC authentication:

```mongodb
mongodb+srv://<cluster-name>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=MONGODB-OIDC&retrywrites=false&maxIdleTimeMS=120000
```

### .NET code samples

The following C# code illustrates how to create a MongoDB OIDC client and connect to an Azure Cosmos DB for MongoDB vCore cluster. 

```csharp
// Azure Cosmos DB for MongoDB connection string for Entra ID authentication via OIDC
			string conn = "mongodb+srv://[cluster-name].global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=MONGODB-OIDC&retrywrites=false&maxIdleTimeMS=120000";

            MongoClient? client = null;
            try
            {
				// Call to create an OIDC MongoDB client instance
                client = CreateOidcClient(conn, connPoolSize: 1, enableDriverLogging: false, appName: null);
				// Basic read/write test using OIDC client connection
                QuickTestAsync(client).GetAwaiter().GetResult();                
            }
            catch (Exception? ex)
            {
                while (ex != null)
                {
                    Log.Error($"{ex.Message} ({ex.GetType().FullName})");
                    Log.Error(ex.StackTrace ?? string.Empty);
                    ex = ex.InnerException;
                }
            }
            finally
            {
                client?.Dispose();
            }
        }
		

		// Optional: Sample read/write operations
        private static async Task QuickTestAsync(MongoClient client)
        {
            // Setting database and collection to write to and read from
			IMongoDatabase database = client.GetDatabase("test");
            IMongoCollection<BsonDocument> collection = database.GetCollection<BsonDocument>("test");

            collection.InsertOne(new BsonDocument { { "_id", 1 } });
            Console.WriteLine("Inserted 1 document.");

            FilterDefinition<BsonDocument> filter = new BsonDocument { { "_id", 1 } };
            using (IAsyncCursor<BsonDocument> cursor = await collection.FindAsync(filter))
            {
                foreach (BsonDocument doc in cursor.ToEnumerable())
                {
                    Console.WriteLine(doc);
                }
            }
        }
		
		// MongoDB OIDC client instantiation
        internal static MongoClient CreateOidcClient(string conn, int connPoolSize, bool enableDriverLogging, string appName)
        {
            MongoClientSettings clientSettings = MongoClientSettings.FromConnectionString(conn);
            clientSettings.Credential = MongoCredential.CreateOidcCredential(new EntraIdCallbackForUser());
            clientSettings.MinConnectionPoolSize = connPoolSize;
            clientSettings.MaxConnectionPoolSize = connPoolSize;

            if (!string.IsNullOrWhiteSpace(appName))
            {
                clientSettings.ApplicationName = appName;
            }

            if (enableDriverLogging)
            {
                clientSettings.ClusterConfigurator = cb => new MongoClientCommandLogger().RegisterClusterBuilder(cb, useMongoDefaultTrace: false);
            }

            clientSettings.Freeze();
            return new MongoClient(clientSettings);
        }

    internal class EntraIdCallbackForUser : IOidcCallback
    {
		// This is Azure Entra ID tenant where Entra ID users added to the cluster are hosted. 
        private const string TenantId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx";

        // Azure Cosmos DB for MongoDB vCore audience claim
        private static readonly string[] Scopes = { "https://ossrdbms-aad.database.windows.net/.default" };

        public EntraIdCallbackForUser()
        {
        }

        public OidcAccessToken GetOidcAccessToken(
            OidcCallbackParameters parameters,
            CancellationToken cancellationToken)
        {
            DefaultAzureCredential credential = new DefaultAzureCredential(includeInteractiveCredentials: true);
            AccessToken accessToken = credential.GetToken(new TokenRequestContext(Scopes, TenantId));

            TimeSpan expiresIn = accessToken.ExpiresOn - DateTimeOffset.UtcNow;
            return new OidcAccessToken(accessToken.Token, expiresIn);
        }

        public async Task<OidcAccessToken> GetOidcAccessTokenAsync(
            OidcCallbackParameters parameters,
            CancellationToken cancellationToken)
        {
            DefaultAzureCredential credential = new DefaultAzureCredential(includeInteractiveCredentials: true);
            AccessToken accessToken = await credential.GetTokenAsync(new TokenRequestContext(Scopes, TenantId));

            TimeSpan expiresIn = accessToken.ExpiresOn - DateTimeOffset.UtcNow;
            return new OidcAccessToken(accessToken.Token, expiresIn);
        }

        internal static Tuple<string, string> GetToken()
        {
            DefaultAzureCredential credential = new DefaultAzureCredential(includeInteractiveCredentials: true);
            AccessToken accessToken = credential.GetToken(new TokenRequestContext(Scopes, TenantId));
            Console.WriteLine($"{accessToken.TokenType}: Expires on {accessToken.ExpiresOn}; Refresh on {accessToken.RefreshOn}");

            JwtSecurityToken securityToken = new JwtSecurityTokenHandler().ReadJwtToken(accessToken.Token);
            //Console.WriteLine();
            //Console.WriteLine(JsonConvert.SerializeObject(securityToken));

            // audience claims
            Console.WriteLine();
            foreach (string claim in securityToken.Audiences)
            {
                Console.WriteLine(claim);
            }

            // expiration
            Console.WriteLine(securityToken.ValidTo.ToUniversalTime().ToString("yyyy-MM-dd HH:mm:ssZ"));

            // oid
            string entraOid = securityToken.Payload["oid"].ToString() ?? string.Empty;
            Console.WriteLine(entraOid);

            // kid
            Console.WriteLine(securityToken.Header.Kid);

            return new Tuple<string, string>(entraOid, accessToken.Token);
        }
    }
```


## Preview limitations

The following section describes functional limits in the Azure Cosmos DB for MongoDB vCore service when Microsoft Entra ID preview is used.
- Entra ID isn't supported on replica clusters.
- Entra ID isn't supported on restored clusters.

## Next steps

- Learn about [authentication in Azure Cosmos DB for MongoDB vCore](./authentication-entra-id.md)
- Review [Microsoft Entra ID fundamentals](/entra/fundamentals/whatis)
