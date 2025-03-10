---
title: Built-in Store Procedure in Azure Database for MySQL - Flexible Server
description: Learn about the Built-in Store Procedure of Azure Database for MySQL - Flexible Server.
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
author: xboxeer
ms.author: yuzheng1
ms.date: 03/10/2025 
---
# **Built-in Stored Procedures in Azure Database for MySQL**  

## **Overview**  
Azure Database for MySQL provides several built-in stored procedures to simplify and automate advanced database management tasks. These stored procedures help users configure features such as data-in replication, binlog cleanup, and plugin management efficiently.  

This article introduces those built-in stored procedures available in Azure Database for MySQL, their functionalities, and how to use them.  

## **Current Available Built-in Stored Procedures**  

### **1. Data-in Replication Management**  
Azure Database for MySQL provides stored procedures to manage Data-in Replication, including starting, stopping, checking status, and resetting replication.  

For details on these procedures, refer to [How to configure Azure Database for MySQL - Flexible Server data-in replication](how-to-data-in-replication.md).  

### **2. Plugin Management**

Azure Database for MySQL supports the **Validate Password Plugin**, which enforces password strength policies. Users can enable or disable this plugin using the following stored procedures:  

#### **Enable the Validate Password Plugin**  
```sql
CALL az_install_validate_password_plugin();
```
After enabling the plugin, you can view and configure related parameters on the Server Parameters page in the Azure portal.

#### **Disable the Validate Password Plugin**  
```sql
CALL az_uninstall_validate_password_plugin();
```
This removes the plugin.

## **Conclusion**  
Azure Database for MySQL provides built-in stored procedures that simplify advanced database management tasks. These procedures enable users to set up replication, manage binlogs, and enable plugins efficiently. By applying these tools, database administrators can enhance performance, optimize storage, and ensure seamless data synchronization.  

