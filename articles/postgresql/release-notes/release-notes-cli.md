---
title: Release notes for the CLI module for Azure Database for PostgreSQL flexible server
description: Release notes for the CLI module for Azure Database for PostgreSQL.
#customer intent: As a usermanaging Azure Database for PostgreSQL flexible servers, I want to review the latest CLI release notes so that I can understand what's changed before I update my Azure CLI version.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: overview
---

# Release notes for the CLI module for Azure Database for PostgreSQL flexible server

This article provides the latest news and updates regarding the evolution of the Azure Database for PostgreSQL module shipped with each release of Azure CLI.

## Azure CLI releases

### July 07, 2026 - Version 2.88.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server create`, `restore`, `geo-restore`, `replica create` | Add `--federated-client-id` and `--backup-federated-client-id` to support multitenant application registration. |
| `az postgresql flexible-server maintenance-event list`, `show`, `apply-now`, `reschedule` | Add commands for maintenance events. |

### June 02, 2026 - Version 2.87.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server create`, `update` | [BREAKING CHANGE] Remove `--high-availability` in favor of `--zonal-resiliency`. |
| `az postgres flexible-server upgrade` | [BREAKING CHANGE] Remove the enum for `--version`. |
| `az postgres flexible-server create`, `update` | [BREAKING CHANGE] Remove deprecated `--cluster-option` and update validation logic. |
| `az postgres flexible-server index-tuning` | [BREAKING CHANGE] Remove support for the command group. |
| `az postgres flexible-server backup create` | [BREAKING CHANGE] Remove backup name requirement and auto-generate backup names. |
| `az postgres flexible-server create`, `geo-restore`, `restore`, `revive-dropped` | [BREAKING CHANGE] Stop creating or altering networking components, and stop supporting `--address-prefixes` and `--subnet-prefixes`. |
| `az postgres flexible-server replica create` | [BREAKING CHANGE] Stop creating or altering networking components, and stop supporting `--address-prefixes` and `--subnet-prefixes`. |
| `az postgres flexible-server backup`, `db`, `firewall-rule`, `long-term-retention`, `migration`, `replica create` | [BREAKING CHANGE] Standardize use of `--name` and `--server-name` across commands. |
| `az postgres flexible-server long-term-retention` | [BREAKING CHANGE] Remove support for the command group. |

### May 05, 2026 - Version 2.86.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server create`, `replica create`, `restore`, `geo-restore`, `revive-dropped` | Add [BREAKING CHANGE] announcement for command behavior related to network resources. |
| `az postgres flexible-server create` | Add [BREAKING CHANGE] announcement for deprecation of `--cluster-option`. |
| `az postgres flexible-server server-logs list` | Fix `AttributeError` when listing log files. |
| `az postgres flexible-server` | Improve validation logic and error message style. |
| `az postgres flexible-server replica create` | Add `--storage-type` to select `PremiumV2_LRS` for read replicas. |
| `az postgres flexible-server create` | Update help text for `--storage-auto-grow` to reflect the default value. |
| `az postgres flexible-server update` | Restart is no longer required for scaling Premium SSD v2 storage size. |
| `az postgres flexible-server create`, `upgrade` | Block SSDv2 creation for PostgreSQL versions earlier than 14. |

### April 07, 2026 - Version 2.85.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server long-term-retention` | Add [BREAKING CHANGE] announcement for command group removal. |

### March 03, 2026 - Version 2.84.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server migrate-network` | Add command to migrate flexible server network mode. |

### February 03, 2026 - Version 2.83.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server create`, `georestore`, `replica` | Allow SSDv2 servers to create replica and geo-restore. |

### January 13, 2026 - Version 2.82.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server update`, `fabric-mirroring` | Allow HA-enabled servers to start fabric mirroring for PostgreSQL version 17+. |
| `az postgres flexible-server create`, `update` | Show high availability with zonal resiliency argument. |
| `az postgres flexible-server create`, `update` | Enable high availability for `PremiumV2_LRS` storage. |
| `az postgres flexible-server index-tuning` | Deprecate and redirect to `az postgres flexible-server autonomous-tuning`. |
| `az postgres flexible-server autonomous-tuning list-index-recommendations`, `list-table-recommendations` | Add support to list index and table recommendations. |
| `az postgres flexible-server update` | Fix bug when using `--standby-zone` while enabling high availability. |
| `az postgres flexible-server upgrade` | Allow major version upgrade to PostgreSQL 18. |
| `az postgres flexible-server create` | Add database name field for create with cluster. |
| `az postgres flexible-server backup`, `db`, `firewall-rule`, `identity`, `long-term-retention`, `microsoft-entra-admin`, `migration`, `parameter`, `replica list` | Allow `--ids` for list commands. |
| `az postgres flexible-server create` | Change database name field to default to `None`. |
| `az postgres flexible-server replica create` | Add `--name` argument to specify read replica name. |

### December 02, 2025 - Version 2.81.0

| Commands | Comments |
| --- | --- |
| `az postgres server`, `db`, `server-logs` | [BREAKING CHANGE] Remove single server commands. |
| `az postgres flexible-server create` | [BREAKING CHANGE] Remove default value for `--version`, and remove `--create-default-database` and `--database-name`. |

### September 02, 2025 - Version 2.77.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server create`, `update`, `restore` | `Premium SSD V2` isn't supported with Burstable compute tier. |
| `az postgres flexible-server update` | Bypass fabric-mirroring validation to allow updating high availability status for PostgreSQL 11 and 12 servers. |

### August 05, 2025 - Version 2.76.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server replica create`, `promote` | Enable replica operations for elastic cluster operations. |
| `az postgres flexible-server create` | Fix failed IP address check. |

### July 01, 2025 - Version 2.75.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server create` | Extend EOL support for PostgreSQL 11 and 12. |

### June 03, 2025 - Version 2.74.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server create`, `db` | Fix `--database-name` validation. |

### May 20, 2025 - Version 2.73.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server create` | [BREAKING CHANGE] Set default value of `--create-default-database` to `Disabled`. |
| `az postgres flexible-server create` | [BREAKING CHANGE] Set default PostgreSQL version to 17. |
| `az postgres flexible-server stop-replication` | [BREAKING CHANGE] Remove deprecated command and use `az postgres flexible-server replica promote`. |
| `az postgres flexible-server create`, `upgrade` | [BREAKING CHANGE] Remove support for PostgreSQL 12. |
| `az postgres flexible-server create`, `update`, `ad-admin` | [BREAKING CHANGE] Rename deprecated references to Microsoft Entra. |
| `az postgres flexible-server update` | [BREAKING CHANGE] Add user confirmation on certain update operations. |
| `az postgres flexible-server create` | Set public access network to disabled when `None` is passed. |
| `az postgres flexible-server create`, `db create` | Add validation for database name. |
| `az postgres flexible-server create` | Set default SKU from location capability API. |

### May 06, 2025 - Version 2.72.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server upgrade` | Add server capability API check to `--version` and allow upgrades to PostgreSQL 17 when available. |

### April 01, 2025 - Version 2.71.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server update` | Fix bug where geo-backup data encryption properties weren't updated. |
| `az postgres flexible-server fabric-mirroring` | Fix space-separated list handling for `start` and `update-databases`. |
| `az postgres flexible-server create` | Support adding admin during create when `--active-directory-auth` is enabled, and don't generate a password when `--password-auth` is disabled. |

### March 04, 2025 - Version 2.70.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server index-tuning` | Support tuning options operations. |

### February 11, 2025 - Version 2.69.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server geo-restore` | Add `--restore-time` parameter. |
| `az postgres flexible-server fabric-mirroring start`, `stop`, `update-databases` | Disable fabric mirroring on HA servers. |
| `az postgres flexible-server update` | Fix scaling up node count on elastic clusters. |

### January 14, 2025 - Version 2.68.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server create` | Create elastic cluster by setting `--cluster-option` to `ElasticCluster`. |
| `az postgres flexible-server list` | Add `--show-cluster` argument to list elastic clusters. |
| `az postgres flexible-server fabric-mirroring`, `identity` | Support system-assigned managed identity and database fabric mirroring. |
| `az postgres flexible-server update` | Add `--node-count` to scale up elastic clusters. |

### November 19, 2024 - Version 2.67.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server long-term-retention start`, `pre-check`, `list`, `show` | Add commands for long-term retention backups. |
| `az postgres flexible-server create` | Support provisioning PostgreSQL flexible servers with version 17. |

### November 05, 2024 - Version 2.66.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server replica create` | Add support for `--tags`. |
| `az postgres flexible-server replica create` | Allow replica creation from storage auto-grow enabled primary servers. |
| `az postgres flexible-server backup create`, `delete` | Add commands to create and delete backups. |

### October 01, 2024 - Version 2.65.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server update` | Support case-insensitive input for `--tier`, `--performance-tier`, `--sku`, and `--maintenance-window`. |
| `az postgres flexible-server migration create` | Add `AWS_AURORA` as a migration source type. |

### August 06, 2024 - Version 2.63.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server create` | [BREAKING CHANGE] Update default PostgreSQL version to 16. |
| `az postgres flexible-server create` | Fix bug when using an existing subnet during server creation. |
| `az postgres flexible-server restore` | Fix bug when using resource ID as `--source-server`. |

### July 09, 2024 - Version 2.62.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server restore` | Add support to restore to a new server by using `PremiumV2_LRS` storage type. |
| `az postgres flexible-server migration create` | Fix migration runtime resource ID input handling in migration parameters. |
| `az postgres flexible-server firewall-rule create` | Correct firewall rule name and IP range validators. |
| `az postgres flexible-server update` | Add argument to enable or disable public access. |
| `az postgres flexible-server create` | Add `--create-default-database` to allow disabling default database creation. |
| `az postgres flexible-server upgrade` | Unblock major version upgrade for Burstable tier from CLI. |
| `az postgres flexible-server update` | Correct setting `--maintenance-window` to be disabled. |

### May 21, 2024 - Version 2.61.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server migration create` | Add private endpoint support for migrations by allowing migration runtime resource ID as a command-line argument. |

### April 30, 2024 - Version 2.60.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server upgrade` | Add capability to perform major version upgrade to PG16. |

### March 05, 2024 - Version 2.58.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server list-skus` | Fix table output from `list-skus`. |

### February 06, 2024 - Version 2.57.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server private-endpoint-connection` | Add commands to list, show, approve, reject, and delete private endpoint connections. |
| `az postgres flexible-server private-link-resource` | Add commands to list and show private link resources. |
| `az postgres flexible-server replica stop-replication` | Deprecate command and recommend `az postgres flexible-server replica promote`. |

### January 09, 2024 - Version 2.56.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server virtual-endpoint` | Add support for virtual endpoints for PostgreSQL flexible server instances. |
| `az postgres flexible-server replica promote` | Add capability to stop replication and promote to primary or standalone server with the selection of planned or force data syncs. |
| `az postgres flexible-server server-logs list` | List server log files for PostgreSQL flexible server instances. |
| `az postgres flexible-server server-logs download` | Download server log files for PostgreSQL flexible server instances. |
| `az postgres flexible-server create` | Add capability to set storage type to PremiumV2_LRS and provide values for IOPS and throughput during creation. |
| `az postgres flexible-server update` | Add capability to update the values of IOPS and throughput during update. |
| `az postgres flexible-server migration create` | Add migration options (`Migrate`, `Validate`, and `ValidateAndMigrate`) using `--migration-option` and a JSON file that supports additional properties such as `sourceType` and `sslMode`. |

### December 05, 2023 - Version 2.55.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server replica create` | Add support for parameters such as `--tier`, `--sku-name`, and `--storage-size` during replica creation. |
| `az postgres flexible-server update` | Add support for custom IOPS updates using `--performance-tier`. |
| `az postgres flexible-server advanced-threat-protection-setting show` | Show advanced threat protection setting. |
| `az postgres flexible-server advanced-threat-protection-setting update` | Update advanced threat protection setting using `--state` as `Enabled` or `Disabled`. |

### November 14, 2023 - Version 2.54.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server geo-restore` | Add cross subscription geo-restore support for PostgreSQL flexible server instances. |
| `az postgres flexible-server restore` | Add cross subscription restore support for PostgreSQL flexible server instances. |
| `az postgres flexible-server upgrade` | Add MVU support for PG version 15. |

### September 26, 2023 - Version 2.53.0

| Commands | Comments |
| --- | --- |
| `az postgres flexible-server create`, `update` | Add capability to enable or disable storage autogrow during creation and update. |

## Contacts

For any questions or suggestions you have about Azure Database for PostgreSQL, send an email to the Azure Database for PostgreSQL Team ([@Ask Azure Database for PostgreSQL](mailto:AskAzureDBforPostgreSQL@service.microsoft.com)). This email address isn't a technical support alias.

In addition, consider the following points of contact as appropriate:

- To contact Azure Support, [file a ticket from the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To fix an issue with your account, file a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) in the Azure portal.
- To provide feedback or to request new features, create an entry via [UserVoice](https://feedback.azure.com/forums/597976-azure-database-for-postgresql).

## Related content

- [Create an Azure Database for PostgreSQL](../configure-maintain/quickstart-create-server.md).
