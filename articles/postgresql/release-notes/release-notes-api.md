---
title: Release notes for the REST APIs for Azure Database for PostgreSQL
description: Release notes for the REST APIs for Azure Database for PostgreSQL.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: overview
ai-usage: ai-assisted
---

# Release notes for the REST APIs for Azure Database for PostgreSQL

This page provides latest news and updates regarding the recommended API versions to be used. **The API versions that are not listed here might be supported, but will be retired soon.** The documentation for the latest Stable API version is available [here](/rest/api/postgresql/).

## API releases

This section summarizes the feature changes across all Azure Database for PostgreSQL API versions from 2021-06-01 onwards. Features are organized alphabetically within each version section, and each section stays focused on the changes that matter most.

| API version | Status | Description |
| --- | --- | --- |
| [2026-04-01-preview](#2026-04-01-preview-preview) | Preview | Enhanced tuning options with filtered recommendations and network migration support. |
| [2026-01-01-preview](#2026-01-01-preview-preview) | Preview | Added major version upgrade precheck and captured logs support. |
| [2025-08-01](#2025-08-01-stable) | Stable | Promoted all preview features to stable release. |
| [2025-06-01-preview](#2025-06-01-preview-preview) | Preview | Enhanced backup and migration capabilities. |
| [2025-01-01-preview](#2025-01-01-preview-preview) | Preview | Enhanced backup operations and improved server capabilities. |
| [2024-11-01-preview](#2024-11-01-preview-preview) | Preview | Added tuning recommendations and enhanced migration validation. |
| [2024-08-01](#2024-08-01-stable) | Stable | Stabilized virtual endpoints and enhanced backup management. |
| [2024-03-01-preview](#2024-03-01-preview-preview) | Preview | Added virtual endpoints and improved location-based availability checks. |
| [2023-12-01-preview](#2023-12-01-preview-preview) | Preview | Added backup creation operations and improved capabilities list. |
| [2023-06-01-preview](#2023-06-01-preview-preview) | Preview | Enhanced migration capabilities and threat protection settings. |
| [2023-03-01-preview](#2023-03-01-preview-preview) | Preview | Added long-term retention (LTR) backup support and enhanced replica management. |
| [2022-12-01](#2022-12-01-stable) | Stable | First major stable release with migration support. |
| [2022-05-01-preview](#2022-05-01-preview-preview) | Preview | Introduced migration support for online and offline migrations from PostgreSQL sources. |
| [2022-03-08-preview](#2022-03-08-preview-preview) | Preview | Enhanced data encryption support and improved error handling. |
| [2022-01-20-preview](#2022-01-20-preview-preview) | Preview | Added support for data encryption and enhanced diagnostics. |
| [2021-06-01](#2021-06-01-stable) | Stable | Initial stable release of the new PostgreSQL Flexible Server API model. |

### 2026-04-01-preview (Preview)

Enhanced tuning options with filtered recommendations and network migration support.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Advanced Threat Protection | Unchanged | Advanced threat protection configuration |
| Backup & Restore | Unchanged | Automatic and on-demand backup creation |
| Captured Logs | Unchanged | Query and transaction log capture operations |
| Capabilities | Unchanged | List capabilities by location and by server |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Unchanged | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Long-Term Retention | Unchanged | Configure and manage LTR backups |
| Maintenance Events | Enhanced | Maintenance event filtering and analytics |
| Migrations | Unchanged | Migration with private endpoint and role support |
| Name Availability | Unchanged | Location-based name availability checks |
| Network Mode Migration | New | Migrate servers between network modes |
| Operations | Unchanged | List available management operations |
| Performance Tuning | Enhanced | Filtered index and table recommendations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Quota Usage | Unchanged | Track quota usage for flexible servers |
| Read Replicas | Unchanged | Replica creation and management operations |
| Server Upgrades | Unchanged | Major version upgrade precheck operations |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |
| Virtual Endpoints | Unchanged | Read-write virtual endpoint management |

### 2026-01-01-preview (Preview)

Added major version upgrade precheck and captured logs support.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Advanced Threat Protection | Unchanged | Advanced threat protection configuration |
| Backup & Restore | Unchanged | Automatic and on-demand backup creation |
| Captured Logs | New | Query and transaction log capture operations |
| Capabilities | Unchanged | List capabilities by location and by server |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Unchanged | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Long-Term Retention | Unchanged | Configure and manage LTR backups |
| Maintenance Events | New | Manage and query maintenance events |
| Migrations | Unchanged | Migration with private endpoint and role support |
| Name Availability | Unchanged | Location-based name availability checks |
| Operations | Unchanged | List available management operations |
| Performance Tuning | Enhanced | Filtered index and table recommendations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Quota Usage | Unchanged | Track quota usage for flexible servers |
| Read Replicas | Unchanged | Replica creation and management operations |
| Server Upgrades | New | Major version upgrade precheck operations |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |
| Virtual Endpoints | Unchanged | Read-write virtual endpoint management |

### 2025-08-01 (Stable)

Promoted all preview features to stable release.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Advanced Threat Protection | Unchanged | Advanced threat protection configuration |
| Backup & Restore | Unchanged | Automatic and on-demand backup creation |
| Capabilities | Unchanged | List capabilities by location and by server |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Unchanged | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Long-Term Retention | Unchanged | Configure and manage LTR backups |
| Migrations | Unchanged | Migration with private endpoint and role support |
| Name Availability | Unchanged | Location-based name availability checks |
| Operations | Unchanged | List available management operations |
| Performance Tuning | Unchanged | Index and table optimization recommendations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Quota Usage | Unchanged | Track quota usage for flexible servers |
| Read Replicas | Unchanged | Replica creation and management operations |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |
| Virtual Endpoints | Unchanged | Read-write virtual endpoint management |

### 2025-06-01-preview (Preview)

Enhanced backup and migration capabilities.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Advanced Threat Protection | Unchanged | Advanced threat protection configuration |
| Backup & Restore | Enhanced | Automatic and on-demand backup creation |
| Capabilities | Unchanged | List capabilities by location and by server |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Unchanged | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Log Files | Unchanged | Access server log files |
| Long-Term Retention | Unchanged | Configure and manage LTR backups |
| Migrations | Enhanced | Migration with private endpoint and role support |
| Name Availability | Unchanged | Location-based name availability checks |
| Operations | Unchanged | List available management operations |
| Performance Tuning | Enhanced | Filtered index and table recommendations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Quota Usage | Unchanged | Track quota usage for flexible servers |
| Read Replicas | Unchanged | Replica creation and management operations |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |
| Virtual Endpoints | Unchanged | Read-write virtual endpoint management |

### 2025-01-01-preview (Preview)

Enhanced backup operations and improved server capabilities.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Backup & Restore | Enhanced | Automatic and on-demand backup operations |
| Capabilities | Unchanged | List capabilities by location and by server |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Unchanged | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Log Files | Unchanged | Access server log files |
| Long-Term Retention | Unchanged | Configure and manage LTR backups |
| Migrations | Unchanged | Enhanced validation and improved error reporting |
| Name Availability | Unchanged | Location-based name availability checks |
| Operations | Unchanged | List available management operations |
| Performance Tuning | Unchanged | Index and table optimization recommendations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Quota Usage | New | Track quota usage for flexible servers |
| Read Replicas | Unchanged | Replica creation and management operations |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |
| Threat Protection | Unchanged | Advanced threat protection settings and alerts |
| Virtual Endpoints | Unchanged | Read-write virtual endpoint management |

### 2024-11-01-preview (Preview)

Added tuning recommendations and enhanced migration validation.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Backup & Restore | Unchanged | On-demand backup creation and deletion |
| Capabilities | Unchanged | List capabilities by location and by server |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Unchanged | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Log Files | Unchanged | Access server log files |
| Long-Term Retention | Unchanged | Configure and manage LTR backups |
| Migrations | Enhanced | Enhanced validation and improved error reporting |
| Name Availability | Unchanged | Location-based name availability checks |
| Operations | Unchanged | List available management operations |
| Performance Tuning | New | Index and table optimization recommendations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Read Replicas | Unchanged | Replica creation and management operations |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |
| Threat Protection | Unchanged | Advanced threat protection settings and alerts |
| Virtual Endpoints | Unchanged | Read-write virtual endpoint management |

### 2024-08-01 (Stable)

Stabilized virtual endpoints and enhanced backup management.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Backup & Restore | Unchanged | On-demand backup creation and deletion |
| Capabilities | Unchanged | List capabilities by location and by server |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Unchanged | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Log Files | Unchanged | Access server log files |
| Long-Term Retention | Unchanged | Configure and manage LTR backups |
| Migrations | Unchanged | Advanced validation and filtering for migrations |
| Name Availability | Unchanged | Location-based name availability checks |
| Operations | Unchanged | List available management operations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Read Replicas | Unchanged | Replica creation and management operations |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |
| Threat Protection | Unchanged | Advanced threat protection settings and alerts |
| Virtual Endpoints | Unchanged | Read-write virtual endpoint management |

### 2024-03-01-preview (Preview)

Added virtual endpoints and improved location-based availability checks.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Backup & Restore | Unchanged | On-demand backup creation and deletion |
| Capabilities | Enhanced | List capabilities by location and by server |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Unchanged | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Log Files | Unchanged | Access server log files |
| Long-Term Retention | Unchanged | Configure and manage LTR backups |
| Migrations | Unchanged | Advanced validation and filtering for migrations |
| Name Availability | Enhanced | Location-based name availability checks |
| Operations | Unchanged | List available management operations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Read Replicas | Unchanged | Replica creation and management operations |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |
| Threat Protection | Unchanged | Advanced threat protection settings and alerts |
| Virtual Endpoints | New | Read-write virtual endpoint management |

### 2023-12-01-preview (Preview)

Added backup creation operations and improved capabilities list.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Backup & Restore | Enhanced | On-demand backup creation and deletion |
| Capabilities | Enhanced | List server capabilities and supported features |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Unchanged | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Log Files | Unchanged | Access server log files |
| Long-Term Retention | Unchanged | Configure and manage LTR backups |
| Migrations | Unchanged | Advanced validation and filtering for migrations |
| Operations | Unchanged | List available management operations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Read Replicas | Unchanged | Replica creation and management operations |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |
| Threat Protection | Unchanged | Advanced threat protection settings and alerts |

### 2023-06-01-preview (Preview)

Enhanced migration capabilities and threat protection settings.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Backup & Restore | Unchanged | Point-in-time restore with enhanced filtering |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Unchanged | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Log Files | Unchanged | Access server log files |
| Long-Term Retention | Unchanged | Configure and manage LTR backups |
| Migrations | Enhanced | Advanced validation and filtering for migrations |
| Operations | Unchanged | List available management operations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Read Replicas | Unchanged | Replica creation and management operations |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |
| Threat Protection | New | Advanced threat protection settings and alerts |

### 2023-03-01-preview (Preview)

Added long-term retention (LTR) backup support and enhanced replica management.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Backup & Restore | Enhanced | Point-in-time restore with enhanced filtering |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Unchanged | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Log Files | Unchanged | Access server log files |
| Long-Term Retention | New | Configure and manage LTR backups |
| Migrations | Unchanged | Full lifecycle management for database migrations |
| Operations | Unchanged | List available management operations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Read Replicas | Enhanced | Replica creation and management operations |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |

### 2022-12-01 (Stable)

First major stable release with migration support.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Backup & Restore | Unchanged | Point-in-time restore from automated backups |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Unchanged | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Log Files | Unchanged | Access server log files |
| Migrations | Unchanged | Full lifecycle management for database migrations |
| Operations | Unchanged | List available management operations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |

### 2022-05-01-preview (Preview)

Introduced migration support for online and offline migrations from PostgreSQL sources.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Backup & Restore | Unchanged | Point-in-time restore from automated backups |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Unchanged | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Log Files | Unchanged | Access server log files |
| Migrations | New | Full lifecycle management for database migrations |
| Operations | Unchanged | List available management operations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |

### 2022-03-08-preview (Preview)

Enhanced data encryption support and improved error handling.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Backup & Restore | Unchanged | Point-in-time restore from automated backups |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | Enhanced | Improved key rotation and auto-update capabilities |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Log Files | Unchanged | Access server log files |
| Operations | Unchanged | List available management operations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |

### 2022-01-20-preview (Preview)

Added support for data encryption and enhanced diagnostics.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Backup & Restore | Unchanged | Point-in-time restore from automated backups |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Data Encryption | New | Customer-managed key support via Azure Key Vault |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Log Files | Unchanged | Access server log files |
| Operations | Unchanged | List available management operations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |

### 2021-06-01 (Stable)

Initial stable release of the new PostgreSQL Flexible Server API model.

| Feature/Operation | Status | Details |
| --- | --- | --- |
| Administrators | Unchanged | Manage Microsoft Entra ID server administrators |
| Backup & Restore | Unchanged | Point-in-time restore from automated backups |
| Configurations | Unchanged | Manage server parameters and settings |
| Databases | Unchanged | Create, read, update, delete database operations |
| Firewall Rules | Unchanged | IP-based firewall rule management |
| Log Files | Unchanged | Access server log files |
| Operations | Unchanged | List available management operations |
| Private Endpoints | Unchanged | Private endpoint connection management |
| Private Link Resources | Unchanged | List private link resource groups |
| Servers | Unchanged | Core server CRUD operations (create, read, update, delete) |

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

- [Create an Azure Database for PostgreSQL](../configure-maintain/quickstart-create-server.md).
