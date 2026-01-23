---
title: "Quickstart: Create a Flexible Server Instance"
description: Quickstart guide to creating and managing an Azure Database for PostgreSQL flexible server instance.
author: gbowerman
ms.author: guybo
ms.reviewer: maghan
ms.date: 01/23/2026
ms.service: azure-database-postgresql
ms.topic: quickstart
ai-usage: ai-assisted
---

# Quickstart: Create an Azure Database for PostgreSQL flexible server

Azure Database for PostgreSQL is a managed service that you can use to run, manage, and scale highly available PostgreSQL databases in the cloud.

This quickstart shows you how to create an Azure Database for PostgreSQL flexible server instance by using the Azure portal, Azure CLI, or Azure Resource Manager (ARM) templates.

## Prerequisites

Before you begin, make sure you have:

- An Azure subscription. If you don't have one, create a [free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Appropriate permissions to create resources in your subscription.

## Understand what you're creating

An Azure Database for PostgreSQL flexible server instance includes:

- A configured set of [compute and storage resources](concepts-compute.md).
- Deployment within an [Azure resource group](/azure/azure-resource-manager/management/overview).
- A `postgres` database created by default.
- An `azure_maintenance` database for managed service processes.
- An `azure_sys` database for query store and index tuning features.

> [!NOTE]
> Connections typically use port 5432, or port 6432 if connecting through the built-in [PgBouncer](../connectivity/concepts-pgbouncer.md) connection pooler.

## Create server using Azure portal

### Navigate to the creation wizard

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. Select **Create a resource** in the upper-left corner.
1. Under **Categories**, select **Databases**.
1. Find and select **Azure Database for PostgreSQL flexible server**.
1. Select **Create**.

### Configure basic settings

#### Project details

| Setting | Suggested value | Notes |
|---------|----------------|-------|
| **Subscription** | Your subscription | Choose where to bill the resource |
| **Resource group** | myresourcegroup | Create new or select existing |

#### Server details

| Setting | Suggested value | Description |
|---------|----------------|-------------|
| **Server name** | mydemoserver-pgsql | Must be globally unique. Domain `.postgres.database.azure.com` is added automatically |
| **Region** | Region closest to you | Consider compliance, data residency, pricing, and proximity to users |
| **PostgreSQL version** | Latest available | Currently supported: **[!INCLUDE [major-versions-ascending](../includes/major-versions-ascending.md)]** |
| **Workload type** | Development | Development uses Burstable SKUs. Production uses General Purpose or Memory Optimized. |
| **Availability zone** | No preference | Useful to colocate with your application |

#### High availability

| Option | SLA | Description |
|--------|-----|-------------|
| Disabled | 99.9% | Single server with no standby |
| Same zone | 99.95% | Standby in the same availability zone |
| Zone redundant | 99.99% | Standby in a different availability zone |

#### Authentication

| Setting | Description | Recommended |
|---------|-------------|-------------|
| **Authentication method** | How users authenticate | - **PostgreSQL authentication only** (for quickstart)<br>- **Microsoft Entra authentication** (for production)<br>- **Both** (for flexibility) |
| **Admin username** | adminuser | - Must be 1-63 characters<br>- Only numbers and letters<br>- Can't start with `pg_`<br>- Can't be system reserved names |
| **Password** | Complex password | 8-128 characters with uppercase, lowercase, numbers, and special characters |

### Configure compute and storage

Select **Configure server** to customize:

#### Compute tier

| Tier | Use case | Description |
|------|----------|-------------|
| **Burstable** | Development | For workloads that don't need continuous full CPU |
| **General Purpose** | Production | Most common production workloads |
| **Memory Optimized** | High-memory workloads | Workloads requiring high memory-to-CPU ratio |

#### Storage settings

| Setting | Can change later | Description |
|---------|-----------------|-------------|
| **Storage type** | ❌ No | Premium SSD or Premium SSD v2 |
| **Storage size** | ✅ Yes (increase only) | Can't shrink after creation |
| **Performance tier** | ✅ Yes | Controls IOPS and throughput |
| **Storage autogrow** | ✅ Yes | Autoexpand when approaching limits |

#### Backup settings

| Setting | Can change later | Description |
|---------|-----------------|-------------|
| **Backup retention** | ✅ Yes | 7-35 days |
| **Backup redundancy** | ❌ No | Locally redundant, Zone redundant, or Geo-redundant |
| **Geo-redundancy** | ❌ No | Available only in [Azure paired regions](/azure/reliability/cross-region-replication-azure) |

### Configure networking

Choose your connectivity method (can't be changed after creation):

#### Public access (allowed IP addresses)

Connect through a public endpoint by using firewall rules.

**Settings:**

| Setting | Description |
|---------|-------------|
| **Allow public access** | Enable public access to configure firewall rules |
| **Allow Azure services** | Permit connections from all Azure services |
| **Add current client IP** | Add your IP address to allow list |

#### Private access (virtual network Integration)

Connect through a private endpoint within a virtual network. For more information, see [Network with private access for Azure Database for PostgreSQL](../network/concepts-networking-private.md).

### Configure security

| Setting | Can change later | Options |
|---------|-----------------|---------|
| **Data encryption key** | ❌ No | Service-managed or Customer-managed |

### Add resource tags (optional)

Organize resources with name-value pairs:

| Name | Value | Purpose |
|------|-------|---------|
| Environment | Development | Identify environment type |
| CostCenter | IT-Dept | Track costs by department |
| Owner | admin@contoso.com | Identify responsible party |

### Review and create

1. Select **Review + create**.
1. Review all configurations.
1. Select **Create** to deploy.

Deployment typically takes 5-10 minutes. When complete, select **Go to resource** to access your server.

## Create server using Azure CLI

### Prerequisites for CLI

[!INCLUDE [cli-run-local-sign-in](../../../includes/cli-run-local-sign-in.md)]

If you use Azure Cloud Shell, you're already signed in.

### Create server with CLI

Create a server with one command:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group myresourcegroup \
  --name mydemoserver-pgsql \
  --location eastus \
  --admin-user myadmin \
  --admin-password <password> \
  --sku-name Standard_D4ds_v5 \
  --tier GeneralPurpose \
  --public-access 0.0.0.0 \
  --storage-size 128 \
  --tags "Environment=Development"
```

### CLI parameters reference

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--resource-group` | Resource group name | myresourcegroup |
| `--name` | Globally unique server name | mydemoserver-pgsql |
| `--location` | Azure region | eastus |
| `--admin-user` | Administrator username | myadmin |
| `--admin-password` | Administrator password | YourPassword123! |
| `--sku-name` | Compute SKU | Standard_D4ds_v5 |
| `--tier` | Compute tier | Burstable, GeneralPurpose, MemoryOptimized |
| `--storage-size` | Storage in GB | 128 |
| `--public-access` | IP addresses allowed | 0.0.0.0 (all Azure services), IP address, or IP range |
| `--version` | PostgreSQL version | 16 |
| `--high-availability` | HA mode | Disabled, SameZone, ZoneRedundant |
| `--backup-retention` | Backup retention days | 7-35 |

### Advanced CLI example

Create a zone-redundant highly available server:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group myresourcegroup \
  --name mydemoserver-pgsql-ha \
  --location eastus \
  --admin-user myadmin \
  --admin-password <password> \
  --sku-name Standard_D4ds_v5 \
  --tier GeneralPurpose \
  --storage-size 256 \
  --storage-type PremiumV2_LRS \
  --high-availability ZoneRedundant \
  --zone 1 \
  --standby-zone 2 \
  --backup-retention 14 \
  --public-access 0.0.0.0
```

## Create server using ARM template

### ARM template overview

Azure Resource Manager (ARM) templates let you define infrastructure as code. Use templates for repeatable deployments.

### Minimal ARM template

Save this file as `postgres-server-template.json`:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "serverName": {
      "type": "string",
      "metadata": {
        "description": "Server name must be globally unique"
      }
    },
    "administratorLogin": {
      "type": "string",
      "minLength": 1,
      "maxLength": 63,
      "metadata": {
        "description": "Administrator username"
      }
    },
    "administratorLoginPassword": {
      "type": "securestring",
      "minLength": 8,
      "metadata": {
        "description": "Administrator password"
      }
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]",
      "metadata": {
        "description": "Server location"
      }
    }
  },
  "resources": [
    {
      "type": "Microsoft.DBforPostgreSQL/flexibleServers",
      "apiVersion": "2024-08-01",
      "name": "[parameters('serverName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "Standard_D4ds_v5",
        "tier": "GeneralPurpose"
      },
      "properties": {
        "administratorLogin": "[parameters('administratorLogin')]",
        "administratorLoginPassword": "[parameters('administratorLoginPassword')]",
        "version": "16",
        "storage": {
          "storageSizeGB": 128,
          "type": "Premium_LRS",
          "autoGrow": "Enabled"
        },
        "backup": {
          "backupRetentionDays": 7,
          "geoRedundantBackup": "Disabled"
        },
        "network": {
          "publicNetworkAccess": "Enabled"
        },
        "highAvailability": {
          "mode": "Disabled"
        }
      }
    }
  ],
  "outputs": {
    "serverFQDN": {
      "type": "string",
      "value": "[reference(parameters('serverName')).fullyQualifiedDomainName]"
    }
  }
}
```

### Deploy the ARM template

```azurecli-interactive
az group create --name myresourcegroup --location eastus

az deployment group create \
  --resource-group myresourcegroup \
  --template-file postgres-server-template.json \
  --parameters \
    serverName=mydemoserver-pgsql \
    administratorLogin=myadmin \
    administratorLoginPassword=<password>
```

## Get connection information

After creating your server, retrieve connection details:

### Using Azure portal

1. Go to your server in the Azure portal.
1. Open the **Overview** page.
1. Copy these values:
   - **Server name** (Endpoint): `mydemoserver-pgsql.postgres.database.azure.com`
   - **Administrator login**: `myadmin`

### Using Azure CLI

```azurecli-interactive
az postgres flexible-server show \
  --resource-group myresourcegroup \
  --name mydemoserver-pgsql \
  --query "{serverName:fullyQualifiedDomainName, adminUser:administratorLogin}" \
  --output table
```

## Connect using psql

### Install psql

If you don't have PostgreSQL client tools, [download PostgreSQL](https://www.postgresql.org/download) for your platform.

### Connect to your server

```bash
psql "host=mydemoserver-pgsql.postgres.database.azure.com port=5432 dbname=postgres user=myadmin sslmode=require"
```

When prompted, enter the administrator password you set during server creation.

### Connection string format

```
host=<server-name>.postgres.database.azure.com port=5432 dbname=<database-name> user=<admin-user> password=<password> sslmode=require
```

### Verify connection

After connecting, you should see:

```output
psql (14.13, server 16.4)
WARNING: psql major version 14, server major version 16.
         Some psql features might not work.
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
Type "help" for help.

postgres=>
```

### Create a database

```sql
CREATE DATABASE user_database;
\c user_database
\q
```

## Troubleshooting connection issues

### Firewall blocking connection

If you see:

```output
connection to server at "mydemoserver-pgsql.postgres.database.azure.com" (###.###.###.###), port 5432 failed: Connection timed out
```

**Solution**: Add your IP address to the firewall rules:

```azurecli-interactive
az postgres flexible-server firewall-rule create \
  --resource-group myresourcegroup \
  --name mydemoserver-pgsql \
  --rule-name AllowMyIP \
  --start-ip-address <your-ip> \
  --end-ip-address <your-ip>
```

### SSL required but not configured

Ensure your connection string includes `sslmode=require`.

## Clean up resources

When you finish the quickstart, delete the resources to avoid charges.

### Delete the entire resource group

```azurecli-interactive
az group delete --name myresourcegroup --yes
```

### Delete only the server

```azurecli-interactive
az postgres flexible-server delete \
  --resource-group myresourcegroup \
  --name mydemoserver-pgsql \
  --yes
```

## Related content

- [Firewall rules in Azure Database for PostgreSQL](../security/security-firewall-rules.md)
- [Connect and query overview for Azure Database for PostgreSQL](../connectivity/how-to-connect-query-guide.md)
