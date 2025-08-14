---
title: Major Version Upgrade FAQ
description: Major Version Upgrade FAQ
author: xboxeer
ms.author: yuzheng1
ms.reviewer: yuzheng1, maghan
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
