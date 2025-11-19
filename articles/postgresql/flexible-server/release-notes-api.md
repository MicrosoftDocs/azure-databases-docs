---
title: API release notes
description: API release notes for Azure Database for PostgreSQL.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: overview
ms.custom:
  - references_regions
  - build-2023
---

# API release notes - Azure Database for PostgreSQL 

This page provides latest news and updates regarding the recommended API versions to be used. **The API versions that are not listed here might be supported, but will be retired soon.** The documentation for the latest Stable API version is available [here](/rest/api/postgresql/).

## API Releases

> [!NOTE]
> Every Stable and Preview API version is cumulative. This means that it includes the previous features in addition to the features included under the Comments column.

| API Version | Stable/Preview | Comments |
| --- | --- | --- |
| [2025-08-01](/rest/api/postgresql/operation-groups?view=rest-postgresql-2025-08-01-preview&preserve-view=true) | Stable (GA) | Earlier GA features +<br>PG 18 support<br>PG 17 support<br>Adds support for specifying default database name in an Elastic Cluster<br>Adds support for table recommendations<br>Corrects HTTP response codes to reflect what each API can return<br>Adds example for CMK-based data encryption with automatic key version update<br>Adds example for creation of server in Microsoft owned virtual network<br>Renames files for better representation of their contents<br>Renames operation IDs to improve organization, clarity, and navigation<br>Improves metadata of local definitions<br>Improves descriptions for consistency<br> |
| 2025-06-01-preview | Preview | Renames files for better representation of their contents<br>Renames operations to improve organization, clarity, and navigation<br>Adds example for CMK-based data encryption with automatic key version update<br>Adds example for creation of server in Microsoft owned virtual network<br>Adds support for table recommendations<br>Adds support for specifying default database name in an Elastic Cluster<br>Removes support for server parameter tuning feature<br>Improves descriptions<br>Improves metadata of local definitions<br>Corrects HTTP response codes to reflect what each API can return<br> |
| 2025-01-01-preview | Preview | Adds support for server parameter tuning feature<br> |
| 2024-11-01-preview | Preview | Index tuning<br>Added source types for migration<br>PG 17 support<br>UltraSSD_LRS storage type support<br>Elastic Clusters on flexible server instances<br> |
| [2024-08-01](/rest/api/postgresql/operation-groups?view=rest-postgresql-2024-08-01-preview&preserve-view=true) | Stable (GA) | Earlier GA features +<br>Geo + CMK - Revive Dropped<br>Storage auto growth<br>IOPS scaling<br>New location capability api<br>Long Term Retention Backup<br>Server Logs<br>Migrations<br>Migration Pre-validation<br>Read replicas - Switchover (Site swap)<br>Read replicas - Virtual Endpoints<br>Private Endpoints<br>Azure Defender / Threat Protection APIs<br>PG 16 support<br>PremiumV2_LRS storage type support<br>Location capability changes for SSDv2<br>Migration Roles<br>Migration Instance Resource Id to support Private endpoint Migrations<br>On-demand backup<br>System assigned managed identity<br> |
| 2023-06-01-preview| Preview | Earlier GA features   +<br>Migration Prevalidation<br>Read replicas - Switchover (Site swap)<br>Read replicas - Virtual Endpoints<br>Private Endpoints<br>Azure Defender\Threat Protection APIs<br>PG 16 support<br>PremiumV2_LRS storage type support<br>Location capability changes for SSDv2<br>Quota Usage API<br> |
| 2023-03-01-preview | Preview | New GA version features (2022-12-01) +<br>Geo + CMK<br>Storage auto growth<br>IOPS scaling<br>New location capability API<br>Azure Defender<br>Server Logs<br>Migrations<br> |
| [2022-12-01](/rest/api/postgresql/operation-groups?view=rest-postgresql-2022-12-01&preserve-view=true) | Stable (GA) | Earlier GA features +<br>EntraID<br>CMK<br>Backups<br>Administrators<br>Replicas<br>GeoRestore<br>MVU<br> |
| 2022-05-01-preview | Preview | CheckMigrationNameAvailability<br>Migrations<br> |
| [2021-06-01](/rest/api/postgresql/operation-groups?view=rest-postgresql-2021-06-01&preserve-view=true) | Stable (GA) | Earlier GA features +<br>Server CRUD<br>CheckNameAvailability<br>Configurations (Server parameters)<br>Database<br>Firewall rules<br>Private<br>DNS zone suffix<br>PITR<br>Server Restart<br>Server Start<br>Server Stop<br>Maintenance window<br>Virtual network subnet usage<br> |

## Using preview versions of API from Terraform

**[Terraform](https://www.hashicorp.com/products/terraform)** is an infrastructure-as-code (IaC) software tool created by HashiCorp. Users define and provide data center infrastructure using a declarative configuration language known as HashiCorp Configuration Language (HCL), or optionally JSON. Terraform is a common way to perform IaC management for Azure Database for PostgreSQL based on GA Azure RM API, in addition to [Azure Resource Manager (ARM) Templates](/azure/azure-resource-manager/templates/overview)
Terraform community releases regular updates for **[Azure Resource Manager (AzureRM) Terraform provider](https://registry.terraform.io/providers/tfproviders/azurerm/latest/docs/resources/postgresql_flexible_server)** based on Azure Resource Manager API version in General Availability (GA). 
 If particular feature currently is in Preview API and hasn't been yet incorporated into GA API and AzureRM Terraform provider, you can use **AzAPI Terraform provider** to call Preview API directly from Terraform. **The AzAPI provider** is a thin layer on top of the  Azure Resource Manager REST APIs. The AzAPI provider enables you to manage any Azure resource type using any API version.
The AzAPI provider is a thin layer on top of the Azure ARM REST APIs. The AzAPI provider enables you to manage any Azure resource type using any API version. This provider complements the AzureRM provider by enabling the management of new Azure resources and properties (including private preview).

 AzAPI provider features the following benefits:

* Supports all Azure services:
* Private preview services and features
* Public preview services and features
* All API versions
* Full Terraform state file fidelity
* Properties and values are saved to state
* No dependency on Swagger
* Common and consistent Azure authentication

The [AzAPI2AzureRM](https://github.com/Azure/azapi2azurerm/releases) is an open source tool that is designed to help migrate from the AzAPI provider to the AzureRM provider.

## Contacts

For any questions or suggestions you might have on Azure Database for PostgreSQL, send an email to the Azure Database for PostgreSQL Team ([@Ask Azure Database for PostgreSQL](mailto:AskAzureDBforPostgreSQL@service.microsoft.com)). Note that this email address isn't a technical support alias.

In addition, consider the following points of contact as appropriate:

- To contact Azure Support, [file a ticket from the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To fix an issue with your account, file a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) in the Azure portal.
- To provide feedback or to request new features, create an entry via [UserVoice](https://feedback.azure.com/forums/597976-azure-database-for-postgresql).

## Related content

- [Create an Azure Database for PostgreSQL](quickstart-create-server.md).
