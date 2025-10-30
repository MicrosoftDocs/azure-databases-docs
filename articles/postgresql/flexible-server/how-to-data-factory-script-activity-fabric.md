---
title: Create a Script Activity in Microsoft Fabric Data Factory
description: Learn how to create a script activity in Microsoft Fabric Data Factory for Azure Database for PostgreSQL.
author: KazimMir
ms.author: v-kmir
ms.reviewer: danyal.bukhari
ms.date: 04/25/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Create a script activity in Microsoft Fabric Data Factory

In this article, you learn how to create a script activity in Microsoft Fabric Data Factory to run custom PostgreSQL queries. A script activity allows you to run various types of PostgreSQL commands directly in your pipelines. These commands include:

- Data Manipulation Language (DML) statements: `INSERT`, `UPDATE`, `DELETE`, and `SELECT`.
- Data Definition Language (DDL) statements: `CREATE`, `ALTER`, and `DROP`.

## Prerequisites

- An Azure Database for PostgreSQL flexible server instance. To learn more, go to [Create an Azure Database for PostgreSQL](/azure/postgresql/flexible-server/quickstart-create-server).
- A Microsoft Fabric Data Factory [data pipeline](/fabric/data-factory/pipeline-landing-page).

## Create a script activity

1. In Microsoft Fabric, select your workspace, switch to **Data factory**, and then select the **New item** button.

1. On the **New item** pane, search for **pipeline** and select the **Data pipeline** tile.

1. In the **New pipeline** dialog, enter a name and then select the **Create** button to create a data pipeline.

1. On the **Activities** menu, select the **Script** icon.

   :::image type="content" source="./media/how-to-data-factory-script-activity-fabric/create-script-activity.png" alt-text="Screenshot that shows the icon for selecting a script activity." lightbox="./media/how-to-data-factory-script-activity-fabric/create-script-activity.png":::

1. With the script activity selected on the data pipeline canvas, on the **General** tab, enter a name for the activity.

   :::image type="content" source="./media/how-to-data-factory-script-activity-fabric/script-activity-name.png" alt-text="Screenshot that shows where to enter a name for a script activity on the General tab." lightbox="./media/how-to-data-factory-script-activity-fabric/script-activity-name.png":::

1. On the **Settings** tab, select your Azure Database for PostgreSQL connection, or create a new one by using the **More** option. [Learn more about connecting to your data by using the modern get-data experience for data pipelines](/fabric/data-factory/modern-get-data-experience-pipeline).

   :::image type="content" source="media/how-to-data-factory-script-activity-fabric/script-activity-settings-connection.png" alt-text="Screenshot that shows an example setting for a connection." lightbox="media/how-to-data-factory-script-activity-fabric/script-activity-settings-connection.png":::

1. Select either the **Query** or **NonQuery** option, depending on your script.

   :::image type="content" source="media/how-to-data-factory-script-activity-fabric/tab-non-query.png" alt-text="Screenshot that highlights the query and nonquery options for a script." lightbox="media/how-to-data-factory-script-activity-fabric/tab-non-query.png":::

   The script activity supports both query and nonquery statements.

   ### [Query](#tab/query)

   Query statements execute PostgreSQL statements (often `SELECT` statements) that return results. A query statement returns records of data.

   :::image type="content" source="./media/how-to-data-factory-script-activity-fabric/settings-query.png" alt-text="Screenshot that shows a sample of a query script." lightbox="./media/how-to-data-factory-script-activity-fabric/settings-query.png":::

   Here's a sample payload with a query statement:

   ```json
   {
      "name": "Sample of select statement",
      "type": "Script",
      "dependsOn": [],
      "policy": {
         "timeout": "0.12:00:00",
         "retry": 0,
         "retryIntervalInSeconds": 30,
         "secureOutput": false,
         "secureInput": false
      },
      "typeProperties": {
         "scripts": [
               {
                  "type": "Query",
                  "text": {
                     "value": "SELECT *  FROM sample_table WHERE sample_int =100",
                     "type": "Expression"
                  }
               }
         ],
         "scriptBlockExecutionTimeout": "02:00:00"
      },
      "externalReferences": {
         "connection": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      }
   }
   ```

   ### [Nonquery](#tab/non-query)

   Nonquery statements execute PostgreSQL statements (often `INSERT`, `UPDATE`, or `DELETE` statements) that don't return any results. A nonquery statement returns the number of affected rows.

   :::image type="content" source="./media/how-to-data-factory-script-activity-fabric/settings-non-query.png" alt-text="Screenshot that shows a sample of a nonquery script." lightbox="./media/how-to-data-factory-script-activity-fabric/settings-non-query.png":::

   Here's a sample payload with a nonquery statement:

   ```json
   {
      "name": "Sample of drop statements",
      "type": "Script",
      "dependsOn": [],
      "policy": {
         "timeout": "0.12:00:00",
         "retry": 0,
         "retryIntervalInSeconds": 30,
         "secureOutput": false,
         "secureInput": false
      },
      "typeProperties": {
         "scripts": [
               {
                  "type": "NonQuery",
                  "text": {
                     "value": "DROP TABLE IF EXISTS sample_table",
                     "type": "Expression"
                  }
               }
         ],
         "scriptBlockExecutionTimeout": "02:00:00"
      },
      "externalReferences": {
         "connection": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      }
   }
   ```

## Create multiple scripts inside one script activity

On the **Settings** tab, you can configure multiple queries in one script activity. To add a new script input, select the plus (**+**) button in the **Script** area.

:::image type="content" source="./media/how-to-data-factory-script-activity-fabric/plus-script.png" alt-text="Screenshot that shows an example of the button and box for creating a new script input." lightbox="./media/how-to-data-factory-script-activity-fabric/plus-script.png":::

You can select the **+** button multiple times, depending on how many script inputs you want to create. For example, to add two new script inputs, select the **+** button two times.

:::image type="content" source="media/how-to-data-factory-script-activity-fabric/multi-script.png" alt-text="Screenshot that shows how to add a second box for script input." lightbox="media/how-to-data-factory-script-activity-fabric/multi-script.png":::

If you want to delete a query input box, select the **Delete** icon for that box.

:::image type="content" source="./media/how-to-data-factory-script-activity-fabric/delete-script-activity.png" alt-text="Screenshot that shows the Delete icon for script input boxes." lightbox="./media/how-to-data-factory-script-activity-fabric/delete-script-activity.png":::

Here's a sample payload with two separate queries:

```json
{
    "name": "Sample of multiple select statements",
    "type": "Script",
    "dependsOn": [],
    "policy": {
        "timeout": "0.12:00:00",
        "retry": 0,
        "retryIntervalInSeconds": 30,
        "secureOutput": false,
        "secureInput": false
    },
    "typeProperties": {
        "scripts": [
            {
                "type": "Query",
                "text": {
                    "value": "SELECT * FROM sample_table WHERE sample_int = 100;",
                    "type": "Expression"
                }
            },
            {
                "type": "Query",
                "text": {
                    "value": "SELECT * FROM sample_table WHERE sample_int > 250;",
                    "type": "Expression"
                }
            }
        ],
        "scriptBlockExecutionTimeout": "02:00:00"
    },
    "externalReferences": {
        "connection": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
}
```

## Use script parameters

> [!IMPORTANT]
> Multiple-query statements that use output parameters aren't supported. You need to split any output queries into separate script blocks within a script activity.

A script activity supports two types of script parameters:

- Named parameters are based on the name of the parameters and are specified as `@<name>` in the query.
- Positional parameters are based on the index of the parameters and are specified in the query (in order) as `$<position number>` with a starting index of `1`.

### Named parameters (recommended)

For named parameters as output parameters, use the `@` prefix. Set the value as `null` with the **Treat as null** box checked on the UI, and leave the payload blank or `null`. The value in the text should be `null`.

:::image type="content" source="media/how-to-data-factory-script-activity-fabric/output-parameter-example.png" alt-text="Screenshot that shows an output parameter example with checkboxes selected for treating the values as null." lightbox="media/how-to-data-factory-script-activity-fabric/output-parameter-example.png":::

The name set within the procedure for output is the name used within the `resultSets` data output. The name set in the UI output row is used for the name of `outputParameters`.

Here's a sample result from the UI execution:

```json
{
   "resultSetCount": 1,
   "recordsAffected": 0,
   "resultSets": [
      {
         "rowCount": 1,
         "rows": [
            {
               "output1": 10,
               "output2": "\"Hello World\""
            }
         ]
      }
   ],
   "outputParameters": {
      "output10": 10,
      "output20": "\"Hello World\""
   }
}
```

Here's a payload sample for the output parameter:

```json
{
    "scripts": [
        {
            "type": "NonQuery",
            "text": "CREATE OR REPLACE PROCEDURE swap_proc (input1 IN TEXT, input2 IN BIGINT, output1 OUT BIGINT, output2 OUT TEXT) LANGUAGE plpgsql AS $$ DECLARE BEGIN output2 := input1; output1 := input2; END $$ "
        },
        {
            "parameters": [
                {
                    "name": "input1",
                    "type": "String",
                    "value": "Hello world",
                    "direction": "Input"
                },
                {
                    "name": "input2",
                    "type": "Int32",
                    "value": "1234",
                    "direction": "Input"
                },
                {
                    "name": "output1",
                    "type": "Int32",
                    "value": "",
                    "direction": "Output"
                },
                {
                    "name": "output2",
                    "type": "String",
                    "value": "",
                    "direction": "Output",
                    "size": 100
                }
            ],
            "type": "Query",
            "text": "CALL swap_proc(@input1, @input2, null, null)"
        }
    ],
    "scriptBlockExecutionTimeout": "02:00:00"
}
```

### Positional parameters

> [!IMPORTANT]
> Multiple-query statements that use positional parameters aren't supported. Ensure that any queries that have positional parameters are in separate script blocks within a script activity.

To use positional parameters, use a placeholder of `$<positional number>` in your query. On the UI, under **Script parameters**, the **Name** box must be left blank. In the payload, the `name` field must be specified as `null`.

The following example shows a valid positional parameter.

:::image type="content" source="media/how-to-data-factory-script-activity-fabric/multiple-scripts-positional-parameters.png" alt-text="Screenshot that shows an example of a valid positional parameter." lightbox="media/how-to-data-factory-script-activity-fabric/multiple-scripts-positional-parameters.png":::

```json
{
    "name": "Sample for valid positional parameter",
    "type": "Script",
    "dependsOn": [],
    "policy": {
        "timeout": "0.12:00:00",
        "retry": 0,
        "retryIntervalInSeconds": 30,
        "secureOutput": false,
        "secureInput": false
    },
   "typeProperties": {
        "scripts": [
            {
                "parameters": [
                    {
                        "type": "String",
                        "value": "John",
                        "direction": "Input"
                    },
                    {
                        "type": "Int32",
                        "value": "52",
                        "direction": "Input"
                    }
                ],
                "type": "Query",
                "text": {
                    "value": "SELECT * FROM customers WHERE first_name = $1 and age = $2;",
                    "type": "Expression"
                }
            }
        ],
        "scriptBlockExecutionTimeout": "02:00:00"
    },
    "externalReferences": {
        "connection": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
}
```

The following example shows an invalid positional parameter:

```json
{
    "name": "Sample for invalid positional parameter",
    "type": "Script",
    "dependsOn": [],
    "policy": {
        "timeout": "0.12:00:00",
        "retry": 0,
        "retryIntervalInSeconds": 30,
        "secureOutput": false,
        "secureInput": false
    },
    "typeProperties": {
        "scripts": [
            {
                "parameters": [
                    {
                        "type": "String",
                        "value": "John",
                        "direction": "Input"
                    },
                    {
                        "type": "Int32",
                        "value": "52",
                        "direction": "Input"
                    }
                ],
                "type": "Query",
                "text": {
                    "value": "SELECT * FROM customers WHERE first_name = $1; SELECT * FROM customers WHERE age = $2;",
                    "type": "Expression"
                }
            }
        ],
        "scriptBlockExecutionTimeout": "02:00:00"
    },
    "externalReferences": {
        "connection": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
}
```

## Configure advanced settings

### Execution timeout for script blocks

You can configure a timeout in minutes for each script block that you run. If any script block within your script activity exceeds the specified timeout, the entire activity fails.

:::image type="content" source="./media/how-to-data-factory-script-activity-fabric/script-block-timeout.png" alt-text="Screenshot that shows an advanced setting in a script activity to set execution timeout for a script block." lightbox="./media/how-to-data-factory-script-activity-fabric/script-block-timeout.png":::

```JSON
    "typeProperties": {
        "scripts": [
            {
                "type": "Query",
                "text": {
                    "value": "SELECT pg_sleep(75);",
                    "type": "Expression"
                }
            }
        ],
        "scriptBlockExecutionTimeout": "00:01:00"
    },
    "externalReferences": {
        "connection": "9b351899-a92f-4e00-bc48-200a2c287f4c"
    }
```

### Logging

You can log PostgreSQL notices to an external Azure Blob Storage account or to internal storage.

#### External storage

To set up external logging:

1. On the **Settings** tab, expand the **Advanced** section.

1. Select the **Enable logging** checkbox and the **External storage** option.

1. Add a Blob Storage account by creating a new linked service for your Blob Storage account.

1. You can optionally provide a folder path. If you leave the **Folder path** box blank, the logs go to the `scriptactivity-logs` folder.

:::image type="content" source="./media/how-to-data-factory-script-activity-fabric/logging-external-storage.png" alt-text="Screenshot that shows an external logging example." lightbox="./media/how-to-data-factory-script-activity-fabric/logging-external-storage.png":::

```JSON
"typeProperties": {
   "scripts": [
      {
         "type": "Query",
         "text": "DO $$ BEGIN RAISE Notice 'Hello'; RAISE Notice 'World!'; END $$;"
      }
   ],
   "scriptBlockExecutionTimeout": "02:00:00",
   "logSettings": {
      "logDestination": "ExternalStore",
      "logLocationSettings": {
         "linkedServiceName": {
            "referenceName": "<Azure Blob Storage linked service name>",
            "type": "LinkedServiceReference"
         },
         "path": "<Azure Blob Storage folder path>"
      }
   }
}
```

#### Activity output

To set up logging in the activity output:

1. On the **Settings** tab, expand the **Advanced** section.

1. Select the **Enable logging** checkbox and the **Activity output** option.

:::image type="content" source="./media/how-to-data-factory-script-activity-fabric/logging-activity-output.png" alt-text="Screenshot that shows selections for setting up activity output logging." lightbox="./media/how-to-data-factory-script-activity-fabric/logging-activity-output.png":::

```JSON
"typeProperties": {
   "scripts": [
      {
         "type": "Query",
         "text": "DO $$ BEGIN RAISE Notice 'Hello'; RAISE Notice 'World!'; END $$;"
      }
   ],
   "scriptBlockExecutionTimeout": "02:00:00",
   "logSettings": {
      "logDestination": "ActivityOutput"
   }
}
```

## Related content

- [How to use a script activity](/fabric/data-factory/script-activity)
- [Azure Database for PostgreSQL connector overview](/fabric/data-factory/connector-azure-database-for-postgresql-overview)
- [Copy activity in Microsoft Fabric Data Factory](how-to-data-factory-copy-activity-fabric.md)
