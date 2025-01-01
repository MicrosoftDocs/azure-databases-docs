---
title: "Quickstart: Create with Azure libraries (SDK) for Python"
description: In this Quickstart, learn how to create an Azure Database for PostgreSQL - Flexible Server instance using Azure libraries (SDK) for Python.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 09/25/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom:
  - devx-track-python-sdk
---

# Quickstart: Use an Azure libraries (SDK) for Python to create an Azure Database for PostgreSQL - Flexible Server instance

In this quickstart, you learn how to use the [Azure libraries (SDK) for Python](/azure/developer/python/sdk/azure-sdk-overview?view=azure-python&preserve-view=true)  
to create an Azure Database for PostgreSQL flexible server instance.

Azure Database for PostgreSQL flexible server is a managed service that you use to run, manage, and scale highly available PostgreSQL databases in the cloud. You can use Python SDK to provision an Azure Database for PostgreSQL flexible server instance, multiple servers, or multiple databases on a server.

You can perform the following operations with this library:

1. Creating a PostgreSQL Flexible Server
1. Managing Databases
1. Configuring Firewall Rules
1. Scaling Operations
1. Back up and Restore

## Prerequisites

An Azure account with an active subscription. [Create one for free](https://azure.microsoft.com/free/).

## Create the Server

First, install the required packages.

```bash
pip install azure-mgmt-resource
pip install azure-identity
pip install azure-mgmt-postgresqlflexibleservers
```

Create a `create_postgres_flexible_server.py` file and include the following code.

```python
from azure.identity import DefaultAzureCredential

from azure.mgmt.postgresqlflexibleservers import PostgreSQLManagementClient

def main():
    client = PostgreSQLManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="ffffffff-ffff-ffff-ffff-ffffffffffff",
    )

    response = client.servers.begin_create(
        resource_group_name="testrg",
        server_name="pgtestsvc4",
        parameters={
            "location": "westus",
            "properties": {
                "administratorLogin": "cloudsa",
                "administratorLoginPassword": "<password>",
                "availabilityZone": "1",
                "backup": {"backupRetentionDays": 7, "geoRedundantBackup": "Disabled"},
                "createMode": "Create",
                "highAvailability": {"mode": "ZoneRedundant"},
                "network": {
                    "delegatedSubnetResourceId": "/subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourceGroups/testrg/providers/Microsoft.Network/virtualNetworks/test-vnet/subnets/test-vnet-subnet",
                    "privateDnsZoneArmResourceId": "/subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourcegroups/testrg/providers/Microsoft.Network/privateDnsZones/test-private-dns-zone.postgres.database.azure.com",
                },
                "storage": {"autoGrow": "Disabled", "storageSizeGB": 512, "tier": "P20"},
                "version": "12",
            },
            "sku": {"name": "Standard_D4s_v3", "tier": "GeneralPurpose"},
            "tags": {"ElasticServer": "1"},
        },
    ).result()
    print(response)

# x-ms-original-file: specification/postgresql/resource-manager/Microsoft.DBforPostgreSQL/preview/2023-12-01-preview/examples/ServerCreate.json
if __name__ == "__main__":
    main()
```

Replace the following parameters with your data:

- **subscription_id**: Your own [subscription ID](/azure/azure-portal/get-subscription-tenant-id#find-your-azure-subscription).
- **resource_group**: The name of the resource group you want to use. The script creates a new resource group if it doesn't exist.
- **server_name**: A unique name that identifies your Azure Database for PostgreSQL flexible server instance. The domain name `postgres.database.azure.com` is appended to the server name you provide. The server name must be at least three characters and at most 63 characters, and can only contain lowercase letters, numbers, and hyphens.
- **location**: The Azure region where you want to create your Azure Database for PostgreSQL flexible server instance. It defines the geographical location where your server and its data reside. Choose a region close to your users for reduced latency. The location should be specified in the format of Azure region short names, like `westus2`, `eastus`, or `northeurope`.
- **administrator_login**: The primary administrator username for the server. You can create additional users after the server has been created.
- **administrator_login_password**: A password for the primary administrator for the server. It must contain between 8 and 128 characters. Your password must contain characters from three of the following categories: English uppercase letters, English lowercase letters, numbers (0 through 9), and nonalphanumeric characters (!, $, #, %, etc.).

You can also customize other parameters like storage size, engine version, etc.

> [!NOTE]  
> The DefaultAzureCredential class will try to authenticate using various methods, such as environment variables, managed identities, or the Azure CLI.  
> Make sure you have one of these methods set up. You can find more information on authentication in the [Azure SDK documentation](/python/api/overview/azure/identity-readme?view=azure-python#defaultazurecredential&preserve-view=true).

## Review deployed resources

You can use the Python SDK, Azure portal, Azure CLI, Azure PowerShell, and various other tools to validate the deployment and review the deployed resources. Some examples are provided below.

# [Python SDK](#tab/PythonSDK)

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
> The `check_server_created` function will return the server state as soon as the server is provisioned. However, it might take a few minutes for the server to become fully available. Ensure that you wait for the server to be in the Ready state before connecting to it. It would return the state, id, name, location etc parameters in the response to the postgres_client.servers.get method.

Create a database in your flexible server with this sample code

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.postgresqlflexibleservers import PostgreSQLManagementClient

def main():
    client = PostgreSQLManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="ffffffff-ffff-ffff-ffff-ffffffffffff",
    )
    #Create database
    response = client.databases.begin_create(
        resource_group_name=<rg-name>,
        server_name=<server-name>,
        database_name=<database-name>,
        parameters={"properties": {"charset": "utf8", "collation": "en_US.utf8"}},
    ).result()
    print(response)

if __name__ == "__main__":
    main()
```
Replace the following parameters with your data:

- **subscription_id**: Your own [subscription ID](/azure/azure-portal/get-subscription-tenant-id#find-your-azure-subscription).
- **resource_group**: The name of the resource group you want to use. The script creates a new resource group if it doesn't exist.
- **sever_name**: The name of the Azure database flexible server instance that you created before

You can also delete the created database

```sql
from azure.identity import DefaultAzureCredential
from azure.mgmt.postgresqlflexibleservers import PostgreSQLManagementClient

def main():
    client = PostgreSQLManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="ffffffff-ffff-ffff-ffff-ffffffffffff",
    )

    client.databases.begin_delete(
        resource_group_name="TestGroup",
        server_name="testserver",
        database_name="db1",
    ).result()

if __name__ == "__main__":
    main()
```

# [CLI](#tab/CLI)

```azurecli
az resource list --resource-group <resource_group>
```

# [PowerShell](#tab/PowerShell)

```azurepowershell
Get-AzResource -ResourceGroupName <resource_group>
```

---

## Clean up resources

If you no longer need the Azure Database for PostgreSQL flexible server instance, you can delete it and the associated resource group using the following methods.

# [Python SDK](#tab/PythonSDK)

Create a 'delete_server.py' file to delete the flexi server instance that was created.

```sql
from azure.identity import DefaultAzureCredential
from azure.mgmt.postgresqlflexibleservers import PostgreSQLManagementClient

def main():
    client = PostgreSQLManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=<subscription-id>,
    )

    client.servers.begin_delete(
        resource_group_name=<rg-name>,
        server_name=<server-name>,
    ).result()
if __name__ == "__main__":
    main()
```

# [CLI](#tab/CLI)

```azurecli
az group delete --name <resource_group>
```

# [PowerShell](#tab/PowerShell)

```azurepowershell
Remove-AzResourceGroup -Name <resource_group>
```

---

## Related content

- [Create an Azure Database for PostgreSQL - Portal](quickstart-create-server-python-sdk.md)
- [Create an Azure Database for PostgreSQL - Azure CLI](quickstart-create-server-cli.md)
- [Create an Azure Database for PostgreSQL - ARM template](quickstart-create-server-arm-template.md)
- [Create an Azure Database for PostgreSQL - Bicep](quickstart-create-server-bicep.md)
