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
Azure Database for MySQL provides several built-in stored procedures to simplify and automate advanced database management tasks. These stored procedures help users configure features such as data-in replication, Undolog cleanup, and plugin management efficiently.  

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

### 3. **Undolog Cleanup**
In some cases your undolog may grow large, and you may want to clean it up. Azure Database for MySQL provides a stored procedure to help you with this task.
1. First execute the following command to check your table space
```sql
SELECT NAME, FILE_SIZE, STATE FROM INFORMATION_SCHEMA.INNODB_TABLESPACES WHERE SPACE_TYPE = 'Undo' AND STATE = 'active' ORDER BY NAME;
```
2. If you find that your undolog is large, call the following command to create a new table space
```sql
call az_create_undo_tablespace(X)
```
Current we only support maximum 8 table spaces, including 2 default ones), so the X value should be  X >=3 and X <=8, when the command finished, the newly created one STATE should be in active state.
3. Execute the following command to deactivate the innodb_undo_001(default one)
```sql
call az_deactivate_undo_tablespace(1)
```
Then wait for the state of innodb_undo_001 to be empty. (it mean undo log has been truncated)
4. Execute the following command to activate the innodb_undo_001(default one)
```sql
call az_activate_undo_tablespace(1)
```
Then wait for the state of innodb_undo_001 to be active.
5. Repeat the 1-4 steps for the innodb_undo_002.
6. execute ```call az_deactivate_undo_tablespace(3)``` to deactivate the newly created table space,  wait for the state to be empty. Then execute call ```az_drop_undo_tablespace(3)``` to drop the newly created table space. 
You can not drop the default ones(innodb_undo_001, innodb_undo_002), only drop the one you just created, in this example it is x_undo_003.Before dropping, first deactivate x_undo_003 to empty state.

## **Conclusion**  
Azure Database for MySQL provides built-in stored procedures that simplify advanced database management tasks. These procedures enable users to set up replication, manage Undolog, and enable plugins efficiently. By applying these tools, database administrators can enhance performance, optimize storage, and ensure seamless data synchronization.  
