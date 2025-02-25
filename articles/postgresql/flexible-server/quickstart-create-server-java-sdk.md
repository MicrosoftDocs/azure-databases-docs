---
title: "Quickstart: Create With Azure Libraries (SDK) For Java"
description: This document is a QuickStart guide for Azure SDK library for Java to create, update, and delete an Azure PostgreSQL Flexible Server Instance.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 02/24/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: quickstart
---

# Quickstart: Use Azure (SDK) libraries in Java to create, update, and delete an Azure Database for PostgreSQL instance

In this quickstart, you learn how to use the Azure SDK libraries in Java to create, update, and delete an Azure PostgreSQL Flexible Server instance. Azure Database for PostgreSQL flexible server is a managed service that allows you to run, manage, and scale highly available PostgreSQL databases in the cloud. Using the Java SDK, you can provision an Azure Database for PostgreSQL flexible server instance, multiple servers, or multiple databases on a server. Azure Java SDK for PostgreSQL Flexible Server instance can help with all the following operations: 

1. **Creating Azure PostgreSQL Flexible Servers**:\
You can create new Flexible Servers instances with specified configurations such as location, SKU, storage, and version.

2. **Updating Azure PostgreSQL Flexible Servers**:\
You can update existing PostgreSQL flexible servers, including changing configurations like administrator login, password, SKU, storage, and version.

3. **Deleting Azure PostgreSQL Flexible Servers**:\
You can delete existing Azure PostgreSQL flexible server instances.

4. **Retrieving Azure PostgreSQL Flexible Server Information**:\
You can retrieve details about existing PostgreSQL flexible servers, including their configurations, status, and other metadata.

5. **Managing Databases**:\
You can create, update, delete, and retrieve databases within the Azure PostgreSQL flexible server instance.

6. **Managing Firewall Rules**:\
You can create, update, delete, and retrieve firewall rules for an instance to control access.

7. **Managing Configuration Settings**:\
You can manage configuration settings for an Azure PostgreSQL flexible server instance, including retrieving and updating server parameters.

## Prerequisites

- [An Azure account with an active subscription](https://azure.microsoft.com/free/).
- Java Development Kit (JDK) with latest version
- Download Maven for using the Azure Java SDK library
- [Azure CLI](/cli/azure/install-azure-cli) installed on your local machine.

## Setting up your account using az cli

Before using the Azure SDK for Java to create, update, or delete an Azure Database for PostgreSQL flexible server instance, you must log in to your Azure account using the Azure CLI.

- Log in to your account using [az CLI](/cli/azure/authenticate-azure-cli-interactively)

```azurecli-interactive
az login
```

- Fetch your tenant id for your account

```azurecli-interactive
az account show --query tenantId --output tsv
```

### Create project

Create a new Maven project in your preferred IDE and then add the dependencies mentioned below for Azure Database for PostgreSQL Flexible Server library. 
Once you create a Maven project there is a pom.xml file that would be created. Please ensure that all dependencies are added under the `<dependencies>` tag in this file.

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-core-management</artifactId>
    <version>1.16.2</version>
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
    <version>2.47.0</version>
</dependency>
    <dependency>
    <groupId>com.azure.resourcemanager</groupId>
    <artifactId>azure-resourcemanager-postgresqlflexibleserver</artifactId>
    <version>1.1.0</version>
</dependency>
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-core-http-netty</artifactId>
    <version>1.15.10</version>
</dependency>
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-slf4j-impl</artifactId>
    <version>2.20.0</version>  
</dependency>
```
> [!NOTE]  
> Please check the latest version for all the dependencies before adding them in your file.

### Create Azure Databases for PostgreSQL Flexible Server Instance

To create a PostgreSQL flexible server instance, create a file named `CreateServer.java` with the following code.

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

This example demonstrates creating a Azure Database for PostgreSQL flexible instance server using the `PostgreSqlManager` class. Before calling the create method it authenticates against the TokenCredential and AzureProfile. Once that is done it defines the Flexible server instance with your given configuration.

Replace the following parameters in the code with your data:

- `subscription-id`: Your Azure subscription ID.
- `tenant-id` : The tenant id your your entra account you can get this from the portal or by using CLI
- `resource-group-name`: The name of your resource group.
- `server-name`: A unique name for your PostgreSQL server.
- `location`: The Azure region for your server.
- `admin-username`: The administrator username.
- `admin-password`: The administrator password.

### Authentication

There are different ways to authenticate your credentials, in this example we have used `DefaultAzureCredentialBuilder`  used to configure and create a DefaultAzureCredential object, which is a credential that can be used to authenticate with Azure services. Login using Azure CLI as mentioned in the prerequisites.

### Run the file
Make sure that you have created a maven project and execute below commands, please make sure you run these commands everytime you add a new dependency in your `pom.xml` file to install that dependency in your local repository:
```cli
mvn clean install
```
To run the file you can use your IDE to run this code or use command line to run the java file.
```cli
javac <file-name>.java
java <file-name>
```
> [!NOTE]  
> Running this code will initiate the instance creation process, which might take a few minutes to complete.

You can review the deployed flexible server instance through Azure portal, Azure CLI, Azure PowerShell, and various other tools to validate the deployment and review the deployed resources.

### Create Database in Azure Databases for PostgreSQL Flexible Server Instance

You can add a new database to your created server. Make sure you have your Azure Database for PostgreSQL Flexible Server instance up and running.

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

### Update the data - Azure Databases for PostgreSQL Flexible Server Instance

Create a `UpdateServer.java` file.

You can also update server data using the Azure PostgreSQL Flexible server Java SDK.

For example, you can update the version, admin username, password, etc., using the `update` method.

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

You can clean up the created flexible server instances by deleting the flexible server instance with the Azure SDK for Java.

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

public class ReadInstance {
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
- `tenant-id` : The tenant id your your entra account you can get this from the portal or by using CLI
- `server-name`: The name of the Azure database flexible server instance that you created.

You can also delete the resource group created through the Portal, CLI, or PowerShell. Follow the steps mentioned in the CLI and PowerShell section if you want to delete it using CLI or PowerShell.

Replace placeholders with your details and run the file.

Alternatively, you can remove the resource group using:
- **Azure CLI**: `az group delete --name <resource_group>`
- **PowerShell**: `Remove-AzResourceGroup -Name <resource_group>`
- **Azure portal**: Navigate to the resource group and delete it.

## Related content

- [Quickstart: Create an instance of Azure Database for PostgreSQL - Flexible Server](quickstart-create-server.md)
