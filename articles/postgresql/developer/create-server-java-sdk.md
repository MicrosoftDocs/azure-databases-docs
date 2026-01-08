---
title: "Quickstart: Create with Azure Libraries (SDK) for Java"
description: This document is a QuickStart guide for Azure SDK library for Java to create, update, and delete an Azure PostgreSQL flexible server instance.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 01/08/2026
ms.service: azure-database-postgresql
ms.topic: quickstart
---

# Create an Azure Database for PostgreSQL instance using the Azure SDK for Java

In this quickstart, you learn how to create, update, and delete an Azure Database for PostgreSQL flexible server instance using the Azure SDK for Java. The code examples are written in Java and use the Azure SDK libraries to interact with the Azure Database for PostgreSQL service.

The Azure SDK for Java provides a set of libraries that allow you to interact with Azure services using Java. The SDK provides a consistent programming model and simplifies working with Azure services, including Azure Database for PostgreSQL.

## Prerequisites

- [An Azure account with an active subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
- Java Development Kit (JDK) with the latest version
- Download Maven for using the Azure Java SDK library
- [Azure CLI](/cli/azure/install-azure-cli) installed on your local machine

## Operations supported by Azure Java SDK

Azure SDK for Java provides `azure-resourcemanager-postgresqlflexibleserver` dependency that supports these operations for Azure Databases for PostgreSQL.

- **Creating Azure Database for PostgreSQL flexible server instances**\
  You can create a new Azure PostgreSQL flexible server instance with specified configurations such as location, SKU, storage, and version.

- **Updating Azure Database for PostgreSQL flexible server instances**\
  You can update existing Azure PostgreSQL flexible server instances, including changing configurations like administrator sign-in, password, SKU, storage, and version.

- **Deleting Azure Database for PostgreSQL flexible server instances**

- **Retrieving Azure Database for PostgreSQL information**\
  You can retrieve details about existing Azure PostgreSQL flexible server instances, including their configurations, status, and other metadata.

- **Managing databases**\
  You can create, update, delete, and retrieve databases within the Azure PostgreSQL flexible server instance.

- **Managing firewall rules**\
  You can create, update, delete, and retrieve firewall rules for an instance to control access.

- **Managing configuration settings** \
  You can manage configuration settings for an Azure PostgreSQL flexible server instance, including retrieving and updating server parameters.

## Setting up your account with az cli

Before using the Azure SDK for Java to create, update, or delete an Azure Database for PostgreSQL flexible server instance, you must sign in to your Azure account using the Azure CLI.

Sign in to your account using [az CLI](/cli/azure/authenticate-azure-cli-interactively)

```azurecli-interactive
az login
```

Fetch your tenant ID for your account as it would be needed for the code in the later.

```azurecli-interactive
az account show --query tenantId --output tsv
```

### Create project

Create a new Maven project in your preferred IDE and add the dependencies for the Azure Database for PostgreSQL library.

Once you create a Maven project, a pom.xml file that is created. Ensure all dependencies are added under this file's `<dependencies>` tag.

```xml
<dependency>
 <groupId>com.azure</groupId>
 <artifactId>azure-core-management</artifactId>
 <version>1.17.0</version>
</dependency>
<dependency>
 <groupId>com.azure</groupId>
 <artifactId>azure-identity</artifactId>
 <version>1.15.3</version>
 <scope>compile</scope>
</dependency>
<dependency>
 <groupId>com.azure.resourcemanager</groupId>
 <artifactId>azure-resourcemanager-resources</artifactId>
 <version>2.48.0</version>
</dependency>
 <dependency>
 <groupId>com.azure.resourcemanager</groupId>
 <artifactId>azure-resourcemanager-postgresqlflexibleserver</artifactId>
 <version>1.1.0</version>
</dependency>
<dependency>
 <groupId>com.azure</groupId>
 <artifactId>azure-core-http-netty</artifactId>
 <version>1.15.11</version>
</dependency>
<dependency>
 <groupId>org.apache.logging.log4j</groupId>
 <artifactId>log4j-slf4j-impl</artifactId>
 <version>2.20.0</version>
</dependency>
```

  > [!NOTE]  
  > Check the latest version for all the dependencies before adding them to your file.

### Create an Azure Database for PostgreSQL instance

To create an Azure PostgreSQL flexible server instance, create a file named `CreateServer.java` with the following code.

```java
package com.example.restservice;
import java.util.HashMap;
import java.util.Map;

import com.azure.core.credential.TokenCredential;
import com.azure.core.http.policy.HttpLogDetailLevel;
import com.azure.core.http.policy.HttpLogOptions;
import com.azure.core.management.AzureEnvironment;
import com.azure.core.management.profile.AzureProfile;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.resourcemanager.postgresqlflexibleserver.PostgreSqlManager;
import com.azure.resourcemanager.postgresqlflexibleserver.models.ActiveDirectoryAuthEnum;
import com.azure.resourcemanager.postgresqlflexibleserver.models.ArmServerKeyType;
import com.azure.resourcemanager.postgresqlflexibleserver.models.AuthConfig;
import com.azure.resourcemanager.postgresqlflexibleserver.models.DataEncryption;
import com.azure.resourcemanager.postgresqlflexibleserver.models.HighAvailability;
import com.azure.resourcemanager.postgresqlflexibleserver.models.HighAvailabilityMode;
import com.azure.resourcemanager.postgresqlflexibleserver.models.IdentityType;
import com.azure.resourcemanager.postgresqlflexibleserver.models.PasswordAuthEnum;
import com.azure.resourcemanager.postgresqlflexibleserver.models.Server;
import com.azure.resourcemanager.postgresqlflexibleserver.models.ServerVersion;
import com.azure.resourcemanager.postgresqlflexibleserver.models.Sku;
import com.azure.resourcemanager.postgresqlflexibleserver.models.SkuTier;
import com.azure.resourcemanager.postgresqlflexibleserver.models.Storage;
import com.azure.resourcemanager.postgresqlflexibleserver.models.UserAssignedIdentity;
public class CreateServer {
    public static void main(String[] args) throws Exception {
              String subscriptionId = "<subscription-id>";
              AzureProfile profile = new AzureProfile("<tenant-id>", subscriptionId, AzureEnvironment.AZURE);

              TokenCredential credential = new DefaultAzureCredentialBuilder()
              .authorityHost(profile.getEnvironment().getActiveDirectoryEndpoint()).build();
              PostgreSqlManager manager = PostgreSqlManager.authenticate(credential, profile);
              Server server = manager.servers()
              .define("<server-name>")
              .withRegion("<location>")
              .withExistingResourceGroup("<resource-group-name>")
              .withSku(new Sku().withName("Standard_D4ds_v5").withTier(SkuTier.GENERAL_PURPOSE))
              .withAuthConfig(new AuthConfig().withActiveDirectoryAuth(ActiveDirectoryAuthEnum.DISABLED)
              .withPasswordAuth(PasswordAuthEnum.ENABLED))
              .withIdentity(new UserAssignedIdentity().withType(IdentityType.NONE))
              .withDataEncryption(new DataEncryption().withType(ArmServerKeyType.SYSTEM_MANAGED))
              .withVersion(ServerVersion.ONE_SIX).withAuthConfig(null)
              .withAdministratorLogin("<user-name>")
              .withAdministratorLoginPassword("<password>").withStorage(new Storage().withStorageSizeGB(32))
              .withHighAvailability(new HighAvailability().withMode(HighAvailabilityMode.DISABLED))
              .create();
              System.out.println("Azure Database for PostgreSQL Flexible server instance is created with server name"+server.name());
    }
}
```

This example demonstrates creating an Azure Database for PostgreSQL flexible instance server using the `PostgreSqlManager` class. Before invoking the create method, it authenticates using the TokenCredential and AzureProfile. Once authenticated, it defines the Azure PostgreSQL flexible server instance with your specified configuration.

Replace the following parameters in the code with your data:

- `subscription-id`: Your Azure subscription ID.
- `tenant-id` : The tenant ID of your Microsoft Entra account. You can get this from the portal or by using the CLI
- `resource-group-name`: The name of your resource group.
- `server-name`: A unique name for your PostgreSQL server.
- `location`: The Azure region for your server.
- `admin-username`: The administrator username.
- `admin-password`: The administrator password.

### Authentication

There are different ways to authenticate your credentials. In this example, we have used `DefaultAzureCredentialBuilder` to configure and create a TokenCredential object, which is a credential that can be used to authenticate with Azure services. Sign in using Azure CLI, as mentioned in the prerequisites.

### Run the file

Make sure that you have created a maven project and executed the below commands; make sure you run these commands every time you add a new dependency in your `pom.xml` file to install that dependency in your local repository:

  ```azurecli
  mvn clean install
  ```
To run the file, you can use your IDE to run this code or use the command line to run the Java file.

  ```azurecli
  javac <file-name>.java
  java <file-name>
  ```

  > [!NOTE]  
  > Running this code initiates the instance creation process, which might take a few minutes to complete.

You can review the deployed Azure PostgreSQL flexible server instance through the Azure portal, Azure CLI, Azure PowerShell, and various other tools to validate the deployment and review the deployed resources.

### Create a database

You can add a new database to your newly created server. Make sure your Azure Database for PostgreSQL flexible server instance is up and running.

```java
package com.example.restservice;

import com.azure.core.credential.TokenCredential;
import com.azure.core.http.policy.HttpLogDetailLevel;
import com.azure.core.http.policy.HttpLogOptions;
import com.azure.core.management.AzureEnvironment;
import com.azure.core.management.profile.AzureProfile;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.resourcemanager.postgresqlflexibleserver.PostgreSqlManager;

public class CreateDatabaseSample {
    public static void main(String args[]) {
        String subscriptionId = "<subscription-id>";
        AzureProfile profile = new AzureProfile("<tenant-id>", subscriptionId, AzureEnvironment.AZURE);

        TokenCredential credential = new DefaultAzureCredentialBuilder()
        .authorityHost(profile.getEnvironment().getActiveDirectoryEndpoint()).build();
        PostgreSqlManager manager = PostgreSqlManager.authenticate(credential, profile);
        manager.databases()
        .define("<database-name>")
        .withExistingFlexibleServer("<resource-group-name>", "<server-name>")
        .withCharset("utf8")
        .withCollation("en_US.utf8")
        .create();
    }
}
```

### Update Server Data

Create a `UpdateServer.java` file.

You can also update server data using this Java SDK by calling the `update()` method from the `postgresqlflexibleserver` library.

Using the `update` method, you can update the version, admin username, password, etc.

```java
package com.example.restservice;

import com.azure.core.credential.TokenCredential;
import com.azure.core.http.policy.HttpLogDetailLevel;
import com.azure.core.http.policy.HttpLogOptions;
import com.azure.core.management.AzureEnvironment;
import com.azure.core.management.profile.AzureProfile;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.resourcemanager.postgresqlflexibleserver.PostgreSqlManager;
import com.azure.resourcemanager.postgresqlflexibleserver.models.ActiveDirectoryAuthEnum;
import com.azure.resourcemanager.postgresqlflexibleserver.models.AuthConfig;
import com.azure.resourcemanager.postgresqlflexibleserver.models.AzureManagedDiskPerformanceTiers;
import com.azure.resourcemanager.postgresqlflexibleserver.models.Backup;
import com.azure.resourcemanager.postgresqlflexibleserver.models.CreateModeForUpdate;
import com.azure.resourcemanager.postgresqlflexibleserver.models.PasswordAuthEnum;
import com.azure.resourcemanager.postgresqlflexibleserver.models.Server;
import com.azure.resourcemanager.postgresqlflexibleserver.models.Sku;
import com.azure.resourcemanager.postgresqlflexibleserver.models.SkuTier;
import com.azure.resourcemanager.postgresqlflexibleserver.models.Storage;
import com.azure.resourcemanager.postgresqlflexibleserver.models.StorageAutoGrow;

public class UpdateServer {
    public static void main(String args[]) {
         String subscriptionId = "<subscription-id>";
         AzureProfile profile = new AzureProfile("<tenant-id>", subscriptionId, AzureEnvironment.AZURE);

         TokenCredential credential = new DefaultAzureCredentialBuilder()
         .authorityHost(profile.getEnvironment().getActiveDirectoryEndpoint()).build();
         PostgreSqlManager manager = PostgreSqlManager.authenticate(credential, profile);
         PostgreSqlManager postgreSqlManager = PostgreSqlManager.configure()
         .withLogOptions(new HttpLogOptions()
         .setLogLevel(HttpLogDetailLevel.BODY_AND_HEADERS))
         .authenticate(credential, profile);
         Server resource = manager.servers()
         .getByResourceGroupWithResponse("<resource-group-name>", "<server-name>", com.azure.core.util.Context.NONE)
         .getValue();
         resource.update()
         .withSku(new Sku().withName("Standard_D16ds_v5").withTier(SkuTier.GENERAL_PURPOSE))
         .withAdministratorLoginPassword("<password>")
         .withStorage(new Storage().withStorageSizeGB(1024)
         .withAutoGrow(StorageAutoGrow.DISABLED)
         .withTier(AzureManagedDiskPerformanceTiers.P30))
         .withBackup(new Backup().withBackupRetentionDays(20))
         .withAuthConfig(new AuthConfig().withActiveDirectoryAuth(ActiveDirectoryAuthEnum.ENABLED)
         .withPasswordAuth(PasswordAuthEnum.ENABLED)
         .withTenantId("<tenant-id>"))
         .withCreateMode(CreateModeForUpdate.UPDATE)
         .apply();
         System.out.println("Updated successfully");
 }
}
```

Run the java file and review the changes made in the resource with the 'UpdateServer.java' file.

## Clean up resources

You can clean up the created flexible server instances by deleting the flexible server instance with the `delete()` method from the `postgresqlflexibleserver` library.

Create a `DeleteServer.java` file and add the following code.

```java
package com.example.restservice;

import com.azure.core.credential.TokenCredential;
import com.azure.core.http.policy.HttpLogDetailLevel;
import com.azure.core.http.policy.HttpLogOptions;
import com.azure.core.management.AzureEnvironment;
import com.azure.core.management.profile.AzureProfile;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.resourcemanager.postgresqlflexibleserver.PostgreSqlManager;

public class DeleteInstance {
    public static void main(String args[]) {
          String subscriptionId = "<subscription-id>";
          AzureProfile profile = new AzureProfile("<tenant-id>", subscriptionId, AzureEnvironment.AZURE);

          TokenCredential credential = new DefaultAzureCredentialBuilder()
          .authorityHost(profile.getEnvironment().getActiveDirectoryEndpoint()).build();
          PostgreSqlManager manager = PostgreSqlManager.authenticate(credential, profile);
          PostgreSqlManager postgreSqlManager = PostgreSqlManager.configure()
          .withLogOptions(new HttpLogOptions()
          .setLogLevel(HttpLogDetailLevel.BODY_AND_HEADERS))
          .authenticate(credential, profile);
          manager.servers().delete("<resource-group>", "<server-name>", com.azure.core.util.Context.NONE);
          System.out.println("Deleted successfully");
 }

}
```

Replace the following parameters with your data:

- `subscription-id`: Your own [subscription ID](/azure/azure-portal/get-subscription-tenant-id#find-your-azure-subscription).
- `resource-group`: The name of the resource group you want to use.
- `tenant-id` : The tenant ID of your Microsoft Entra account. You can get this from the portal or by using the CLI
- `server-name`: The name of the Azure database flexible server instance that you created.

You can also delete the resource group created through the Portal, CLI, or PowerShell. If you want to delete it using CLI or PowerShell, follow the steps mentioned in the CLI and PowerShell section.

Replace placeholders with your details and run the file.

Alternatively, you can remove the resource group using:
- **Azure CLI**: `az group delete --name <resource_group>`
- **PowerShell**: `Remove-AzResourceGroup -Name <resource_group>`
- **Azure portal**: Navigate to the resource group and delete it.

## Related content

- [Quickstart: Create an Azure Database for PostgreSQL](quickstart-create-server.md)
