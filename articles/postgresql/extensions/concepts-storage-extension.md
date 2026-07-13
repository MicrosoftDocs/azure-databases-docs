---
title: Azure Storage Extension in Azure Database for PostgreSQL Flexible Server
description: This article describes the Azure Storage extension in Azure Database for PostgreSQL flexible server to import and export data.
#customer intent: As a user, I want to move data between my flexible server and Azure Storage, so that I can import and export data without external tools.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 07/10/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: reference
---

# Azure storage extension in Azure Database for PostgreSQL flexible server

The Azure Database for PostgreSQL extension for Azure Storage enables direct data movement between your PostgreSQL flexible server and Azure Storage accounts. It supports both import and export operations in multiple file formats. By using this extension, you simplify data workflows by allowing SQL-based access to blob storage, making it easier to integrate PostgreSQL with other Azure services.

This extension reduces the need for external Extract, Transform, and Load (ETL) and Extract, Load, and Transform (ELT) tools by enabling SQL native commands to interact with blob containers.

It works with public and private access configurations, including PostgreSQL flexible servers whose network interface is injected in a virtual network of your own infrastructure.

The extension supports sending requests to Azure Storage service by using [authorization with Shared Key](how-to-configure-azure-storage-extension.md#to-use-authorization-with-shared-key) or by using [authorization with Microsoft Entra ID](how-to-configure-azure-storage-extension.md#to-use-authorization-with-microsoft-entra-id) managed identity assigned to your server.

Given its superior security, Microsoft highly recommends the use of authorization with Microsoft Entra ID.

To use the `azure_storage` extension from any of the databases of an Azure Database for PostgreSQL flexible server, you need to [allow the extension](../extensions/how-to-allow-extensions.md#allow-extensions-in-azure-database-for-postgresql-flexible-server), [load its library](../extensions/how-to-load-libraries.md), and [create the extension](../extensions/how-to-create-extensions.md) in the database from where you want to use its functionality.

## Related content

- [Configure the Azure Storage extension](how-to-configure-azure-storage-extension.md).
- [Extensions and modules](../extensions/concepts-extensions.md).
