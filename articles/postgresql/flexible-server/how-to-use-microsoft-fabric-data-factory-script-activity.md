---
title: Using script activity in Fabric Data Factory
description: Guide on using script activity in the Azure Database for PostgreSQL connector in Fabric Data Factory
author: KazimMir
ms.author: v-kmir
ms.reviewer: danyal.bukhari
ms.date: 04/25/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Using script activity in Fabric Data Factory

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

In this article, you learn how to create a script activity in Fabric Data Factory to run custom PostgreSQL queries. Script activity allows users to execute various types of PostgreSQL commands, such as, Data Manipulation Language (DML) and Data Definition Language (DDL) directly in their pipelines. 

**DML statements:** `INSERT`, `UPDATE`, `DELETE`, and `SELECT`

**DDL statements:**`CREATE`, `ALTER`, and `DROP`

## Prerequisites

- An Azure Database for PostgreSQL flexible server instance. To learn more, go to [Create an Azure Database for PostgreSQL flexible server](/azure/postgresql/flexible-server/quickstart-create-server)
- A Microsoft Fabric Data Factory [Data pipeline](/fabric/data-factory/pipeline-landing-page)

## Creating a script activity

1. In Microsoft Fabric, select your workspace, switch to **Data factory** and select the **New item** button. Search and select the **Data pipeline** tile in the **New item** sidebar displayed

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/create-a-new-fabric-data-factory-pipeline.png" alt-text="Screenshot that shows where to select new pipeline." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/create-a-new-fabric-data-factory-pipeline.png":::

1. Provide a name in the **New pipeline** popup and select the **Create** button to create a Data pipeline

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/new-pipeline-name.png" alt-text="Screenshot showing the dialog to give the new pipeline a name." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/new-pipeline-name.png":::


1. Select  **Activities** menu and **Script** button from the menu options displayed

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/create-script-activity.png" alt-text="Screenshot that shows where to select Script Activity." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/create-script-activity.png":::

1. With the Script activity selected on the data pipeline canvas, in the **General tab**, give your script activity a name.

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/script-activity-name.png" alt-text="Screenshot that shows box to provide a name to the script activity." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/script-activity-name.png":::
   
1. Switch into the **Settings** tab and select your Azure Database for PostgreSQL connection, or create a new one using the **More** option. [Learn more about connecting to your data with the new modern get data experience for data pipelines](/fabric/data-factory/modern-get-data-experience-pipeline)

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/script-activity-settings-connection.png" alt-text="Screenshot that shows an example setting for connection." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/script-activity-settings-connection.png":::

1. Select either the **Query** or **NonQuery** option depending on your script.

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/tab-non-query.png" alt-text="Screenshot that highlights Query and non Query radio buttons." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/tab-non-query.png":::

   The script activity supports both query and nonquery statements.

   ### [Query](#tab/query)

   Query statements execute PostgreSQL statements that return results. Often `SELECT` statements. A Query statement returns records of data.

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/settings-query.png" alt-text="Screenshot that shows a sample of query script." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/settings-query.png":::

   Sample of a payload with a Query.
   
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

   ### [NonQuery](#tab/non-query)

   NonQuery statements execute PostgreSQL statements that don't return any results. Often `INSERT`, `UPDATE`, or `DELETE` statements. Returns the number of rows affected.

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/settings-non-query.png" alt-text="Screenshot that shows a sample of NonQuery script." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/settings-non-query.png":::

   Sample of a payload with a NonQuery.

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

### Creating multiple scripts inside one Script Activity

You have the option of having multiple queries in one script activity by selecting `+` button multiples times next to **Script** to add a new script input

:::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/plus-script.png" alt-text="Screenshot that shows an example of creating a new script input box." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/plus-script.png":::

Select `+` button two times to add two new script inputs

:::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/multi-script.png" alt-text="Screenshot that shows how to add a new script block input box." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/multi-script.png":::

You have the option of deleting query input boxes selecting on the delete icon next to **Script** to delete an existing script input.

:::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/delete-script-activity.png" alt-text="Screenshot that shows how to delete a script block." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/delete-script-activity.png":::

Sample of a payload with two separate queries.

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

### Script Parameters

> [!IMPORTANT]
> Multi-query statements using output parameters aren't supported. You need to split any output queries into separate script blocks within the same or different script activity.

Script activity supports two types of script parameters, positional and named parameters. Named parameters are based on the name of the parameters and are specified as `@<name>` in the queries. Positional parameters are based on the index of the parameters and are specified in the query in order as `$<position number>` with a starting index of 1.

#### Named Parameters (recommended)

Named parameters should have an `@` prefix to the name of the parameter.
Named parameters as output parameters should be set the value as null with the **Treat as null** box checked in the UI, and with the payload left blank or null. The value in the text should be null. 

:::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/output-parameter-example.png" alt-text="Screenshot that shows an output parameter example with treat as null checked in the UI." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/output-parameter-example.png":::

The name set within the procedure for output is the name used within the **resultSets** data output. The name set in the UI output row is used for the name of **outputParameters**.

Sample result from the UI execution
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

Payload sample for output parameter.

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

#### Positional Parameters

> [!IMPORTANT]
>  Multi-query statements using positional parameters aren't supported. You need to ensure that any queries with positional parameters are in separate script blocks within the same or different script activity.

To use positional parameters, use a placeholder of `$<positional number>` in your query. Under parameters the `name` field must be left blank in the UI and specified as `null` in the payload.

**Ex. Valid positional parameter example**

:::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/multiple-scripts-positional-parameters.png" alt-text="Screenshot that shows a valid positional parameter example." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/multiple-scripts-positional-parameters.png":::

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

**Ex. Invalid positional parameter example**

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

### Advanced Settings

#### Script block execution time-out

You can configure a timeout in minutes for each individual script block run. If any script block within your script activity exceeds the specified timeout, the entire activity fails.

:::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/script-block-timeout.png" alt-text="Screenshot that shows an advanced setting in script activity to set script block execution timeout." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/script-block-timeout.png":::

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

#### Logging

Logging can be used to log PostgreSQL Notices to an external Blob Storage or to internal storage.

##### External storage

For external logging, drop down the "Advanced" tab then check **Enable logging** and **External storage**. Add a blob storage account by creating a new linked service for your blob storage account. You can optionally provide a folder path, if left blank it places the logs under "scriptactivity-logs" folder.

:::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/logging-external-storage.png" alt-text="Screenshot that shows external logging example." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/logging-external-storage.png":::

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


##### Activity output

For activity output logging, expand the **Advanced** section and check **Enable logging** and **Activity output**. These options enable the logging in the activity output.

:::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/logging-activity-output.png" alt-text="Screenshot that shows an activity output logging example." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/logging-activity-output.png":::

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

- [Learn more about Script activity in Microsoft Fabric Data Factory](/fabric/data-factory/script-activity).
- [Learn more about Azure Database for PostgreSQL Data Pipeline Connector in Microsoft Fabric Data Factory](/fabric/data-factory/connector-azure-database-for-postgresql-overview).
- [Learn more about Copy activity to work with Azure Database for PostgreSQL flexible server in Microsoft Fabric Data Factory Data Pipeline](how-to-use-microsoft-fabric-data-factory-copy-activity.md).