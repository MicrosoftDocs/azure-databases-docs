---
title: Azure Storage Extension in Azure HorizonDB
description: This article describes the Azure Storage extension in Azure HorizonDB to import and export data.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: reference
ms.custom:
  - ignite-2024
  - sfi-image-nochange
---

# Azure storage extension for Azure HorizonDB (Preview)

The Azure HorizonDB extension for Azure Storage enables direct data movement between your Azure HorizonDB server and Azure Storage accounts, supporting both import and export operations in multiple file formats. The use of this extension simplifies data workflows by allowing SQL-based access to blob storage, making it easier to integrate PostgreSQL with other Azure services.

It reduces the need for external Extract, Transform, and Load (ETL) and Extract, Load, and Transform (ELT) tools by enabling SQL native commands to interact with blob containers.

It works with public and private access configurations, including PostgreSQL flexible server instances whose network interface is injected in a virtual network of your own infrastructure.

The extension supports sending requests to Azure Storage service using [authorization with Shared Key](how-to-configure-azure-storage-extension.md#to-use-authorization-with-shared-key), or using [authorization with Microsoft Entra ID](how-to-configure-azure-storage-extension.md#to-use-authorization-with-microsoft-entra-id) managed identity assigned to your server.

Given its superior security, Microsoft highly recommends the use of authorization with Microsoft Entra ID.

To be able to use the `azure_storage` extension from any of the databases of an Azure HorizonDB instance, you need to [allow the extension](how-to-allow-extensions.md#allow-extensions-for-azure-horizondb-preview), [load its library](how-to-load-libraries.md), and [create the extension](how-to-create-extensions.md) in the database from where you want to use its functionality.

## Related content

- [Configure the Azure Storage extension in Azure HorizonDB](how-to-configure-azure-storage-extension.md)
- [Extensions and modules in Azure HorizonDB](concepts-extensions.md)
