---
title: Built-in Store Procedure in Azure Database for MySQL - Flexible Server
description: Learn about the Built-in Store Procedure of Azure Database for MySQL - Flexible Server.
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
author: xboxeer
ms.author: yuzheng1
ms.date: 03/10/2025 
---
# Built-in stored procedures in Azure Database for MySQL

[!INCLUDE [applies-to-mysql-flexible-server](../includes/applies-to-mysql-flexible-server.md)]

Azure Database for MySQL provides several built-in stored procedures that simplify and automate advanced database management tasks. These stored procedures help you efficiently configure features such as data-in replication, Undo log cleanup, and plugin management.  

This article introduces the built-in stored procedures available in Azure Database for MySQL, their functionalities, and how to use them.  

## **Current available built-in stored procedures**  

### **1. Data-in replication management**  
Azure Database for MySQL provides stored procedures to manage Data-in Replication, including starting, stopping, checking status, and resetting replication.  

For details on these procedures, see [How to configure Azure Database for MySQL - Flexible Server data-in replication](how-to-data-in-replication.md).  

### **2. Plugin management**

Azure Database for MySQL supports the **Validate Password Plugin**, which enforces password strength policies. Users can enable or disable this plugin using the following stored procedures:  

#### **Enable the validate password plugin**  
```sql
CALL az_install_validate_password_plugin();
```
After enabling the plugin, you can view and configure related parameters on the Server Parameters page in the Azure portal.

#### **Disable the validate password plugin**  
```sql
CALL az_uninstall_validate_password_plugin();
```
This stored procedure removes the plugin.

> [!NOTE]  
> - For **HA (High Availability) servers**, first execute these stored procedures on the **primary** server. Then, perform a **forced failover** and reexecute the stored procedures on the new primary.  
> - For **Replica servers**, executing these stored procedures on the primary doesn't automatically sync to replicas. Manually execute them on **each** replica after running them on the primary.

### 3. **Undo log cleanup**
In some cases your undo log might grow large, and you might want to clean it up. Azure Database for MySQL provides a stored procedure to help you with this task.
1. To check your table space, first execute the following command.
    ```sql
    SELECT NAME, FILE_SIZE, STATE FROM INFORMATION_SCHEMA.INNODB_TABLESPACES WHERE SPACE_TYPE = 'Undo' AND STATE = 'active' ORDER BY NAME;
    ```
1. If you find that your undo log is large, call the following command to create a new table space.
    ```sql
    call az_create_undo_tablespace(X)
    ``` 
    Currently, we support up to eight tablespaces, including two default ones. The X value must be between 3 and 8. After the command finishes, the new tablespace should be in an active state.
1. Execute the following command to deactivate the innodb_undo_001 (default one).
    ```sql
    call az_deactivate_undo_tablespace(1)
    ```
    Then wait for the state of innodb_undo_001 to be empty(It means undo log is truncated).     
    You can verify undo log truncation by checking [Verifying and Checking Undo Tablespaces](./concepts-built-in-store-procedure.md#verifying-and-checking-undo-tablespaces)
1. Execute the following command to activate the innodb_undo_001 (default one).
    ```sql
    call az_activate_undo_tablespace(1)
    ```
    Then wait for the state of innodb_undo_001 to be active.
1. Repeat the 1-4 steps for the innodb_undo_002.
1. Execute ```call az_deactivate_undo_tablespace(3);``` to deactivate the newly created table space. Wait for the state to be empty. Then execute ```Call az_drop_undo_tablespace(3);``` to drop the newly created table space. 
   You can't drop the default ones (innodb_undo_001, innodb_undo_002). You can only drop the one you created, in this example it's x_undo_003.Before dropping, first deactivate x_undo_003 to empty state.
#### Verifying and Checking Undo Tablespaces
Check the status of the undo tablespaces:

```sql
SELECT NAME, FILE_SIZE, STATE
FROM information_schema.innodb_tablespaces
WHERE SPACE_TYPE = 'Undo'
ORDER BY NAME;
```
Repeat the query periodically until the target undo tablespace shows as empty.
A sample output might look like this:

| NAME | SPACE_TYPE | STATE |
| :--- | :--- | :--- |
|innodb_undo_001|Undo|empty|
|innodb_undo_002|Undo|active|
|x_undo_003  |Undo|active|

> [!NOTE]
> The time required for an undo log to become empty depends on its file size. Larger undo log files will take longer to clear.



### Drop problematic table 

If you encounter an error like the following when accessing a table, it may indicate table corruption:

```
Incorrect information in file: './DATABASE_NAME/TABLE_NAME.frm'
```

To resolve this issue, you can use the built-in stored procedure:

```sql
mysql.az_drop_broken_table(DBNAME, TABLENAME)
```
After executing the procedure, it is recommended to reboot the server to ensure the changes take effect.

Alternatively, you can perform a [Point-in-time restore](./how-to-restore-server-portal.md) to revert the server to a state before the issue occurred.

## **Conclusion**  
Azure Database for MySQL provides built-in stored procedures that simplify advanced database management tasks. These procedures enable you to set up replication, manage the Undo log, and enable plugins efficiently. By applying these tools, you can enhance performance, optimize storage, and ensure seamless data synchronization.  
