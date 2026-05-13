---
title: Major Version Upgrade FAQ
description: Major Version Upgrade FAQ
author: hariramt
ms.author: hariramt
ms.reviewer: maghan
ms.date: 06/11/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
---

# Frequently asked questions (FAQs)

- Q: **Can I upgrade directly from MySQL 5.7 to 8.4 (or skip major versions)?**

    A. Cross-major version upgrades (for example, upgrading directly from MySQL 5.7 to 8.4) aren't supported. You must upgrade from 5.7 to 8.0 and then from 8.0 to 8.4. In the future, if new MySQL major versions are released, direct upgrades skipping major versions won't be supported. Each major version upgrade must be performed sequentially.

- Q: **Will this cause downtime of the server, and if so, how long?**

    A. To have minimal downtime during upgrades, follow the steps mentioned under [Perform minimal downtime major version upgrade using read replicas](./how-to-upgrade.md#perform-minimal-downtime-major-version-upgrade-using-read-replicas). The server is unavailable during the upgrade process, so we recommend you perform this operation during your planned maintenance window. The estimated downtime depends on the database size, storage size provisioned (IOPs provisioned), and the number of tables on the database. The upgrade time is directly proportional to the number of tables on the server. To estimate the downtime for your server environment, we recommend first performing an upgrade on a restored copy of the server.

- Q: **I'm using an HA server. Can I expect a near zero downtime experience for a major version upgrade, similar to routine maintenance?**

    A. No. Major version upgrades differ significantly from routine maintenance. The replication between HA primary and standby servers across major versions is not stable, which prevents us from offering a near zero downtime experience during such upgrades in Azure Database for MySQL.

- Q: **What happens to my backups after the upgrade?**

    A. All backups (automated/on-demand) taken before a major version upgrade are restored to a server with the previous version when used for restoration. All the backups (automated/on-demand) taken after a major version upgrade are restored to the server with the upgraded version. It's highly recommended to take an on-demand backup before you perform the major version upgrade for an easy rollback.

## Known issues and limitations

### AAD Authentication blocked on Replica

After upgrade from version 5.7 to 8.0 on replica, if any AAD Entra update operation is performed on the source server running 5.7 before upgrading it, authentication method on the replica changes from 'MySQL and Entra auth' to 'MySQL auth only'. This blocks AAD authentication on replica.

#### Resolution

Change AAD Entra auth only after the hierarchy is upgraded to same version.
- Upgrade source to 8.0 and set required Entra Admin user.
- Create new replica on version 8.0
- Drop old replica with broken replication (if facing this error)
- Use new replica

### Slowness or High CPU usage in 8.0 compared to 5.7

Depending on the workload, slowness or High CPU usage can be observed in version 8.0 compared to 5.7. It is recommended to upgrade a read replica or restore and upgrade to MySQL Flexible 8.0 Server. The replica should be used to test and tune production load/queries before upgrading the primary.

#### Resolution

If the slowness is observed with queries such as update/insert/delete, then enabling "Accelerated Logs" on your server under 'Settings -> Compute + Storage' in the side pane of your server's portal page might help.