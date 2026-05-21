---
title: Data Encryption at Rest in Azure HorizonDB
description: Learn how data encryption works in Azure HorizonDB.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: concept-article
ms.custom:
  - horz-security
---

# Data encryption at rest in Azure HorizonDB (preview)

All the data managed by an Azure HorizonDB instance is always encrypted at rest. That data includes all system and user databases, server logs, write-ahead log segments, and backups. Encryption is handled by the underlying storage through [Server-side encryption of Azure Disk Storage](/azure/virtual-machines/disk-encryption).

## Encryption at Rest with Service (SMK) 

Azure HorizonDB supports data encryption at rest using: **service managed keys (SMK)** Data encryption with service managed keys is the default mode for Azure HorizonDB. In this mode, the service automatically manages the encryption keys used to encrypt your data. You don't need to take any action to enable or manage encryption in this mode.


To achieve the encryption of your data, Azure HorizonDB uses [Azure Storage encryption for data at rest](/azure/storage/common/storage-service-encryption).

## Benefits provided by each mode (SMK)

Data encryption with **service managed keys** for Azure HorizonDB provides the following benefits:

- The service automatically and fully controls data access.
- The service automatically and fully controls your key's life cycle, including rotation of the key.
- You don't need to worry about managing data encryption keys.
- Data encryption based on service managed keys doesn't negatively affect the performance of your workloads.
- It simplifies the management of encryption keys (including their regular rotation), and the management of the identities used to access those keys.

## Related content

- [Azure Storage encryption for data at rest](/azure/storage/common/storage-service-encryption).