---
title: "Migrate MySQL On-Premises to Azure Database for MySQL Introduction"
description: "Migration guide from MySQL on-premises to Azure Data base for MySQL"
author: saikondapalli11
ms.author: skondapalli
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: migration-guide
ms.topic: how-to
---

# Migrate MySQL on-premises to Azure Database for MySQL

This migration guide is designed to provide stackable and actionable information for MySQL customers and software integrators seeking to migrate their MySQL workloads to Azure Database for MySQL (see [overview](../../overview.md). This guide provides applicable knowledge that applies to most cases and offers guidance on planning and executing a successful MySQL migration.

The process of migrating existing databases and MySQL workloads to the cloud can present challenges related to workload functionality and the connectivity of existing applications. The information presented throughout this guide offers helpful links and recommendations that focus on a successful migration and ensure workloads and applications continue to operate as originally intended.

The information provided centers on a customer journey using the Microsoft [Cloud Adoption Framework](/azure/cloud-adoption-framework/get-started/) to perform assessment, migration, and post-optimization activities for an Azure Database for MySQL environment.

## MySQL

MySQL has a rich history in the open-source community and has become widely popular among corporations worldwide for use in websites and other business-critical applications. This guide assists administrators who have been tasked with scoping, planning, and executing the migration. Administrators who are new to MySQL can also review the [MySQL Documentation](https://dev.mysql.com/doc/) for more in-depth information on the internal workings of MySQL. Additionally, this guide links to several reference articles throughout each section, pointing you to helpful information and tutorials.

## PaaS

[Azure Database for MySQL](../../overview.md) is a Platform as a Service (PaaS) offering by Microsoft, where the MySQL environment is fully managed. In this fully managed environment, operating system and software updates are automatically applied, ensuring the implementation of high availability and data protection.

**Comparison of MySQL environments**

This guide focuses entirely on migrating on-premises MySQL workloads to the Platform as a Service (PaaS) Azure Database for MySQL offering, due to its various advantages over Infrastructure as a Service (IaaS), including scale-up and scale-out capabilities, pay-as-you-go pricing, high availability, security, and manageability features.

## Next step

> [!div class="nextstepaction"]
> [Migrate MySQL on-premises to Azure Database for MySQL: Representative Use Case](02-representative-use-case.md)
