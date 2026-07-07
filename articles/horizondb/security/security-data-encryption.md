---
title: Data Encryption at Rest in Azure HorizonDB
description: Learn how data encryption works in Azure HorizonDB.
#customer intent: As a user, I want to understand how data is encrypted at rest in Azure HorizonDB so that I can confirm my data meets security requirements.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 07/07/2026
ms.service: azure-horizondb
ms.subservice: security
ms.topic: concept-article
ms.custom:
  - horz-security
---

# Data encryption at rest in Azure HorizonDB (Preview)

All data managed by an Azure HorizonDB instance is always encrypted at rest. This data includes all system and user databases, cluster logs, write-ahead log segments, and backups. The underlying storage handles encryption through [Server-side encryption of Azure Disk Storage](/azure/virtual-machines/disk-encryption).

## Encryption at rest with service managed keys (SMK)

Azure HorizonDB supports data encryption at rest by using **service managed keys (SMK)**. Data encryption by using service managed keys is the default mode for Azure HorizonDB. In this mode, the service automatically manages the encryption keys that encrypt your data. You don't need to take any action to enable or manage encryption in this mode.

To achieve encryption of your data, Azure HorizonDB uses [Azure Storage encryption for data at rest](/azure/storage/common/storage-service-encryption).

## Benefits provided by service managed keys

Data encryption by using **service managed keys** for Azure HorizonDB provides the following benefits:

- The service automatically and fully controls data access.
- The service automatically and fully controls your key's life cycle, including rotation of the key.
- You don't need to worry about managing data encryption keys.
- Data encryption based on service managed keys doesn't negatively affect the performance of your workloads.
- It simplifies the management of encryption keys (including their regular rotation) and the management of the identities used to access those keys.

## Related content

- [Azure Storage encryption for data at rest](/azure/storage/common/storage-service-encryption)
