---
title: "MySQL On-Premises to Azure Database for MySQL Sample Applications"
description: "Download extra documentation we created for this Migration Guide and learn how to configure."
author: saikondapalli11
ms.author: skondapalli
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: migration-guide
ms.topic: how-to
ms.custom:
  - devx-track-arm-template
---

# Migrate MySQL on-premises to Azure Database for MySQL sample applications

Migrating MySQL databases from on-premises environments to Azure Database for MySQL can be a game-changer for your applications. This article explores the process through the lens of sample applications, providing practical insights and real-world examples. You can better understand the challenges and solutions involved by examining how different types of applications handle the migration. This guide walks you through preparing your applications, executing the migration, and optimizing performance post-migration. Whether you're dealing with web applications, enterprise systems, or data analytics platforms, this article equips you with the knowledge to ensure a smooth and successful transition to Azure.

## Overview

This article explains how to deploy a sample application with an end-to-end MySQL migration guide and to review available server parameters.

## Environment setup

[Download more documentation](https://github.com/Azure/azure-mysql/blob/master/MigrationGuide/MySQL%20Migration%20Guide_v1.1%20Appendix%20A.pdf) we created for this Migration Guide and learn how to configure an environment to perform the guide's migration steps for the sample conference demo application.

## Azure Resource Manager (ARM) templates

### Secure

The ARM template deploys all resources with private endpoints. The ARM template effectively removes any access to the PaaS services from the internet.

[Secure ARM template](https://github.com/Azure/azure-mysql/tree/master/MigrationGuide/arm-templates/ExampleWithMigration)

### Nonsecure

The ARM template deploys resources using standard deployment where all resources are available from the internet.

[Nonsecure ARM template](https://github.com/Azure/azure-mysql/tree/master/MigrationGuide/arm-templates/ExampleWithMigrationSecure)

## Default server parameters MySQL 5.5 and Azure Database for MySQL

You can find the [full listing of default server parameters of MySQL 5.5 and Azure Database for MySQL](https://github.com/Azure/azure-mysql/blob/master/MigrationGuide/MySQL%20Migration%20Guide_v1.1%20Appendix%20C.pdf) in our GitHub repository.
