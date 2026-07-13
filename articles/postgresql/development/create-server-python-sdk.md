---
title: "Quickstart: Create an Azure PostgreSQL Flexible Server by using the Azure SDK for Python"
description: This document is a quickStart guide for Azure SDK library for Python to create, update, and delete an Azure PostgreSQL flexible server.
#customer intent: As a Python developer, I want to provision an Azure Database for PostgreSQL flexible server programmatically, so that I can automate database deployments in my applications.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: development
ms.topic: quickstart
ms.custom:
  - devx-track-python-sdk
  - references_regions
---

# Create an Azure Database for PostgreSQL flexible server by using the Azure SDK for Python

In this quickstart, you learn how to use the Azure Python SDK to interact with an Azure Database for PostgreSQL flexible server.

Azure Database for PostgreSQL is a managed service for running, managing, and scaling highly available PostgreSQL databases in the cloud. You can use the Python SDK to provision an Azure Database for PostgreSQL flexible server, multiple servers, or multiple databases on a server.

You can perform the following operations with this library:

- Create a PostgreSQL flexible server
- Manage databases
- Configure firewall rules
- Perform scaling operations
- Back up and restore

This guide helps you explore the basic functionalities of this SDK, including creating a flexible server, reviewing the created server, creating a database, and deleting the instance.

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
- **server-name**: A unique name that identifies your Azure Database for PostgreSQL flexible server. The domain name `postgres.database.azure.com` is appended to the server name you provide. The server name must be at least three characters and at most 63 characters. It can only contain lowercase letters, numbers, and hyphens.
- **Location**: The Azure region where you want to create your Azure Database for PostgreSQL flexible server. It defines the geographical location where your server and its data reside. Choose a region close to your users for reduced latency. Specify the location in the Azure region short names format, such as `westus2`, `eastus`, or `northeurope`.
- **admin-username**: The primary administrator username for the server. After the server has been created, you can create additional users.
- **password**: A password for the primary administrator for the server. It must contain between 8 and 128 characters. Your password must contain characters from three categories: English uppercase letters, English lowercase letters, numbers (0 through 9), and nonalphanumeric characters (!, $, #, %, etc.).

You can also add values for other parameters like vnet-name, subnet-name, private-DNS-zone, and customize other parameters like storage size, engine version, etc.

> [!NOTE]  
> The DefaultAzureCredential class tries to authenticate using various methods, such as environment variables, managed identities, or the Azure CLI.  
> Make sure you have one of these methods set up. You can find more information on authentication in the [Azure SDK documentation](/python/api/overview/azure/identity-readme?view=azure-python#defaultazurecredential&preserve-view=true).
>
> Running this code initiates the instance creation process, which might take a few minutes to complete.

## Review deployed resources

To validate the deployment and review the deployed resources, use the Python SDK, Azure portal, Azure CLI, Azure PowerShell, or other tools. The following sections provide some examples.

### Validate deployment with Python SDK

Add the `check_server_created` function to your existing script to use the `servers` attribute of the [PostgreSQLManagementClient](/python/api/azure-mgmt-rdbms/azure.mgmt.rdbms.postgresql_flexibleservers.postgresqlmanagementclient?view=azure-python&preserve-view=true) instance to check if the Azure Database for PostgreSQL flexible server was created:

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

Call the function with the appropriate parameters.

```python
 check_server_created(subscription_id, resource_group, server_name)
```

> [!NOTE]  
> The `check_server_created` function returns the server state as soon as the server is provisioned. However, the server might take a few minutes to become fully available. Ensure you wait for the server to be Ready before connecting to it. The `postgres_client.servers.get` method returns the state, ID, name, location, and other parameters.

## Create database using Python

Create a database in your flexible server by using this sample code.

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
- **server-name**: The name of the Azure database flexible server that you created earlier.
- **database-name**: The name of the database you want to create.

## Clean up resources

If you no longer need the Azure Database for PostgreSQL flexible server, delete it and the associated resource group by using either the portal, Python SDK, or Azure CLI.

### Use Python SDK to delete the instance

Create a `delete_server.py` file to delete the Azure Databases for PostgreSQL Server instance that you created.

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

- [Quickstart: Create an Azure Database for PostgreSQL flexible server](../configure-maintain/quickstart-create-server.md)
