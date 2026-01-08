---
title: "Quickstart: Create with Azure Libraries (SDK) for Python"
description: In this Quickstart, learn how to create an Azure Database for PostgreSQL flexible server instance using Azure libraries (SDK) for Python.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 01/08/2026
ms.service: azure-database-postgresql
ms.topic: quickstart
ms.custom:
  - devx-track-python-sdk
  - references_regions
---

# Manage Azure Database for PostgreSQL with Azure SDK for Python

In this quickstart, you learn how to use the Azure Python SDK to interact with an Azure Database for PostgreSQL flexible server instance.

Azure Database for PostgreSQL is a managed service for running, managing, and scaling highly available PostgreSQL databases in the cloud. You can use the Python SDK to provision an Azure Database for PostgreSQL flexible server instance, multiple servers, or multiple databases on a server.

You can perform the following operations with this library:

- Create a PostgreSQL flexible server instance
- Manage databases
- Configure firewall rules
- Perform scaling operations
- Back up and restore

This guide helps you explore the basic functionalities of this SDK, including creating a flexible server instance, reviewing the created server, creating a database, and deleting the instance.

## Prerequisites

### Account with active subscription

An Azure account with an active subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

### Install the libraries

Install the following Azure Python libraries.

```bash
pip install azure-mgmt-resource
pip install azure-identity
pip install azure-mgmt-postgresqlflexibleservers
```

### Run the login command

Log in to your account using `azurecli` to authenticate your account.

```azurecli-interactive
az login
```

Once this command is executed, select a valid account to sign in and later select the subscription ID from the list to log in.

## Create the server

Create a `create_postgres_flexible_server.py` file and include the following code.

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.postgresqlflexibleservers import PostgreSQLManagementClient

def main():
    client = PostgreSQLManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="<subscription-id>",
    )

    response = client.servers.begin_create(
        resource_group_name="<resource-group-name>",
        server_name="<server-name>",
        parameters={
            "location": "<region>",
            "properties": {
                "administratorLogin": "<admin-username>",
                "administratorLoginPassword": "<password>",
                "availabilityZone": "1",
                "backup": {"backupRetentionDays": 7, "geoRedundantBackup": "Disabled"},
                "createMode": "Create",
                "highAvailability": {"mode": "ZoneRedundant"},
                "network": {
                    "delegatedSubnetResourceId": "/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.Network/virtualNetworks/<vnet-name>/subnets/<subnet-name>",
                    "privateDnsZoneArmResourceId": "/subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.Network/privateDnsZones/<private-DNS-zone-name>.postgres.database.azure.com",
                },
                "version": "<pg-version>",
            },
            "sku": {"name": "<sku-name>", "tier": "<tier-type>"},
            "tags": {"ElasticServer": "1"},
        },
    ).result()
    print(response)

if __name__ == "__main__":
    main()
```

Replace the following parameters with your data:

- **subscription-id**: Your own subscription ID.
- **resource-group**: Name the resource group you want to use. If it doesn't exist, the script creates a new one.
- **server-name**: A unique name that identifies your Azure Database for PostgreSQL flexible server instance. The domain name `postgres.database.azure.com` is appended to the server name you provided. The server name must be at least three characters and at most 63 characters and can only contain lowercase letters, numbers, and hyphens.
- **Location**: The Azure region where you want to create your Azure Database for PostgreSQL flexible server instance. It defines the geographical location where your server and its data reside. Choose a region close to your users for reduced latency. The location should be specified in the Azure region short names format, like `westus2`, `eastus`, or `northeurope`.
- **admin-username**: The primary administrator username for the server. After the server has been created, you can create additional users.
- **password**: A password for the primary administrator for the server. It must contain between 8 and 128 characters. Your password must contain characters from three categories: English uppercase letters, English lowercase letters, numbers (0 through 9), and nonalphanumeric characters (!, $, #, %, etc.).

You can also add values for other parameters like vnet-name, subnet-name, private-DNS-zone, and customize other parameters like storage size, engine version, etc.

> [!NOTE]  
> The DefaultAzureCredential class tries to authenticate using various methods, such as environment variables, managed identities, or the Azure CLI.  
> Make sure you have one of these methods set up. You can find more information on authentication in the [Azure SDK documentation](/python/api/overview/azure/identity-readme?view=azure-python#defaultazurecredential&preserve-view=true).
>
> Running this code initiates the instance creation process, which might take a few minutes to complete.

## Review deployed resources

You can use the Python SDK, Azure portal, Azure CLI, Azure PowerShell, and various other tools to validate the deployment and review the deployed resources. Some examples are provided below.

### Validate deployment with Python SDK

Add the `check_server_created` function to your existing script to use the servers attribute of the [PostgreSQLManagementClient](/python/api/azure-mgmt-rdbms/azure.mgmt.rdbms.postgresql_flexibleservers.postgresqlmanagementclient?view=azure-python&preserve-view=true) instance to check if the Azure Database for PostgreSQL flexible server instance was created:

```python
def check_server_created(subscription_id, resource_group, server_name):
    # Authenticate with your Azure account
    credential = DefaultAzureCredential()

    # Create PostgreSQL management client
    postgres_client = PostgreSQLManagementClient(credential, subscription_id)

    try:
        server = postgres_client.servers.get(resource_group, server_name)
        if server:
            print(f"Server '{server_name}' exists in resource group '{resource_group}'.")
            print(f"Server state: {server.state}")
        else:
            print(f"Server '{server_name}' not found in resource group '{resource_group}'.")
    except Exception as e:
        print(f"Error occurred: {e}")
        print(f"Server '{server_name}' not found in resource group '{resource_group}'.")
```

Call it with the appropriate parameters.

```python
 check_server_created(subscription_id, resource_group, server_name)
```

> [!NOTE]  
> The `check_server_created` function returns the server state as soon as the server is provisioned. However, the server might take a few minutes to become fully available. Ensure you wait for the server to be Ready before connecting to it. It would return the state, ID, name, location, and other parameters in response to the postgres_client.servers.get method.

## Create database using Python

Create a database in your flexible server instance with this sample code

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.postgresqlflexibleservers import PostgreSQLManagementClient

def main():
    client = PostgreSQLManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=<subscription-id>,
    )
    # Create database
    response = client.databases.begin_create(
        resource_group_name="<resource-group-name>",
        server_name="<server-name>",
        database_name="<database-name>",
        parameters={"properties": {"charset": "utf8", "collation": "en_US.utf8"}},
    ).result()
    print(response)

if __name__ == "__main__":
    main()
```

#### Replace the following parameters with your data

- **subscription-id**: Your own [subscription ID](/azure/azure-portal/get-subscription-tenant-id#find-your-azure-subscription).
- **resource-group-name**: Name the resource group you want to use. The script creates a new resource group if it doesn't exist.
- **sever-name**: The name of the Azure database flexible server instance that you created before
- **database-name**: The name of the database you want to create.

## Clean up resources

If you no longer need the Azure Database for PostgreSQL flexible server instance, you can delete it and the associated resource group using either the Portal, Python SDK, or Azure CLI.

### Use Python SDK to delete the instance

Create a 'delete_server.py' file to delete the Azure Databases for PostgreSQL Server instance that was created.

### [Python](#tab/Python)

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.postgresqlflexibleservers import PostgreSQLManagementClient

def main():
    client = PostgreSQLManagementClient(
          credential=DefaultAzureCredential(),
          subscription_id=<subscription-id>,)
    client.servers.begin_delete(
          resource_group_name=<rg-name>,
          server_name=<server-name>,
    ).result()
if __name__ == "__main__":
    main()
```

### [CLI](#tab/CLI)

```azurecli-interactive
az postgres flexible-server delete \
  --resource-group <resource-group> \
  --name <server-name>
```

---

## Related content

- [Create an Azure Database for PostgreSQL](quickstart-create-server.md)
