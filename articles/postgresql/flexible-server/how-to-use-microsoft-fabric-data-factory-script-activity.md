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

# Using script activity in Data Factory and Synapse Analytics

## Overview

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

In this article, you learn how to create a script activity in Azure Data Factory to run custom PostgreSQL queries. Script activity allows users to execute various types of PostgreSQL commands, such as, Data Manipulation Language (DML) and Data Definition Language (DDL) directly in their pipelines. 

**DML statements:** `INSERT`, `UPDATE`, `DELETE`, and `SELECT`

**DDL statements:**`CREATE`, `ALTER`, and `DROP`

### Prerequisites

- An Azure Database for PostgreSQL flexible server instance. To learn more, go to [Create an Azure Database for PostgreSQL flexible server](/azure/postgresql/flexible-server/quickstart-create-server)
- (Optional) An Azure integration runtime [created within a managed virtual network](/azure/data-factory/managed-virtual-network-private-endpoint).
- An Azure Data Factory Linked Service [connected to Azure Database for PostgreSQL](how-to-connect-to-data-factory-private-endpoint.md)


## Creating a script activity

1. In Microsoft Fabric, select your workspace, switch to **Data factory** and select the **New item** button. Search and select the **Data pipeline** tile in the **New item** sidebar displayed

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/create-a-new-fabric-data-factory-pipeline.png" alt-text="Screenshot that shows where to select new pipeline." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/create-a-new-fabric-data-factory-pipeline.png":::

1. Provide a name in the **New pipeline** popup and select the **Create** button to create a Data pipeline

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/new-pipeline-name.png" alt-text="Screenshot showing the dialog to give the new pipeline a name." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/new-pipeline-name.png":::


1. Select  **Activities** menu and **Script** button from the menu options displayed

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/create-script-activity.png" alt-text="Screenshot that shows where to select Scripty Activity" lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/create-script-activity.png":::

1.  With the Script activity selected on the data pipeline canvas, in the **General tab**, give your script activity a name.

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/script-activity-name.png" alt-text="Screenshot that shows box to provide a name to the script activity." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/script-activity-name.png":::

1. Switch into the **Settings** tab and select your Azure Database for PostgreSQL linked service, or create a new one. Once added, to verify your connection is valid, select **Test connection**.

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/script-activity-linked-service.png" alt-text="Screenshot that shows an example setting linked service." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/script-activity-linked-service.png":::

1. Select either the **Query** or **NonQuery** option depending on your script.

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/tab-non-query.png" alt-text="Screenshot that shows highlights Query and non Query radio buttons" lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/tab-non-query.png":::

   The script activity supports both query and nonquery statements.

   ### [Query](#tab/query)

   Query statements execute PostgreSQL statements that return results. Often `SELECT` statements. A Query statement returns records of data.

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/query.png" alt-text="Screenshot that shows a sample of query script" lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/query.png":::

   Sample of a payload with a Query.
   
   ```json
   {
       "name": "Sample of select statement",
       "type": "Script",
       "dependsOn": [],
       "policy": {
           "timeout": "1.12:00:00",
           "retry": 0,
           "retryIntervalInSeconds": 30,
           "secureOutput": false,
           "secureInput": false
       },
       "userProperties": [],
       "linkedServiceName": {
           "referenceName": "AzurePostgreSQL",
           "type": "LinkedServiceReference"
       },
       "typeProperties": {
           "scripts": [
               {
                   "type": "Query",
                   "text": "SELECT * FROM sample_table WHERE sample_int = 100; "
               }
           ],
           "scriptBlockExecutionTimeout": "02:00:00"
       }
   }
   ```

   ### [NonQuery](#tab/non-query)

   NonQuery statements execute PostgreSQL statements that don't return any results. Often `INSERT`, `UPDATE`, or `DELETE` statements. Returns the number of rows affected.

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/non-query.png" alt-text="Screenshot that shows a sample of NonQuery script" lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/non-query.png":::

   Sample of a payload with a NonQuery.

   ```json
   {
       "name": "Sample of drop statements",
       "type": "Script",
       "dependsOn": [],
       "policy": {
           "timeout": "1.12:00:00",
           "retry": 0,
           "retryIntervalInSeconds": 30,
           "secureOutput": false,
           "secureInput": false
       },
       "userProperties": [],
       "linkedServiceName": {
           "referenceName": "AzurePostgreSQL1",
           "type": "LinkedServiceReference"
       },
       "typeProperties": {
           "scripts": [
               {
                   "type": "NonQuery",
                   "text": "DROP TABLE IF EXISTS sample_table; "
               }
           ],
           "scriptBlockExecutionTimeout": "02:00:00"
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
         "timeout": "1.12:00:00",
         "retry": 0,
         "retryIntervalInSeconds": 30,
         "secureOutput": false,
         "secureInput": false
      },
      "userProperties": [],
      "linkedServiceName": {
         "referenceName": "AzurePostgreSQL1",
         "type": "LinkedServiceReference"
      },
      "typeProperties": {
         "scripts": [
            {
                  "type": "Query",
                  "text": "SELECT * FROM sample_table WHERE sample_int = 100; "
            },
            {
                  "type": "Query",
                  "text": "SELECT * FROM sample_table WHERE sample_int > 250; "
            }
         ],
         "scriptBlockExecutionTimeout": "02:00:00"
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

```

Payload sample for output parameter.

```json
"scripts": [
  {
    "text": "CREATE OR REPLACE PROCEDURE swap_proc (input1 IN TEXT, input2 IN BIGINT, output1 OUT BIGINT, output2 OUT TEXT) LANGUAGE plpgsql AS $$ DECLARE BEGIN output2 := input1; output1 := input2; END $$",
    "type": "NonQuery"
  },
  {
    "text": "CALL swap_proc(@input1, @input2, null, null)",
    "type": "Query",
    "parameters": [
      {
        "name": "input1",
        "type": "String",
        "value": "Hello world",
        "direction": "Input",
        "size": 100
      },
      {
        "name": "input2",
        "type": "INT32",
        "value": 1234,
        "direction": "Input"
      },
      {
        "name": "output1",
        "type": "INT32",
        "direction": "Output"
      },
      {
        "name": "output2",
        "type": "String",
        "direction": "Output",
        "size": 100
      }
    ]
  }
]
```

#### Positional Parameters

> [!IMPORTANT]
>  Multi-query statements using positional parameters aren't supported. You need to ensure that any queries with positional parameters are in separate script blocks within the same or different script activity.

To use positional parameters, use a placeholder of `$<positional number>` in your query. Under parameters the `name` field must be left blank in the UI and specified as `null` in the payload.
```json
"scripts": [
   {
      "text": "SELECT * FROM customers WHERE first_name = $1 AND age = $2;",
      "type": "Query",
      "parameters": [
        {
          "name": null,
          "type": "String",
          "value": "John",
          "direction": "Input",
          "size": 256
        },
        {
          "name": null,
          "type": "INT32",
          "value": 52,
          "direction": "Input"
        }
      ]
   }
]
```

**Ex. Valid positional parameter example**

:::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/multiple-scripts-positional-parameters.png" alt-text="Screenshot that shows a valid positional parameter example." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/multiple-scripts-positional-parameters.png":::

```json
"scripts": [
   {
      "text": "SELECT * FROM customers WHERE first_name = $1;",
      "type": "Query",
      "parameters": [
        {
          "name": null,
          "type": "String",
          "value": "John",
          "direction": "Input",
          "size": 256
        }
      ]
   },
   {
      "text": "SELECT * FROM customers WHERE age = $2;",
      "type": "Query",
      "parameters": [
        {
          "name": null,
          "type": "INT32",
          "value": 52,
          "direction": "Input"
        }
      ]
   }
]
```

**Ex. Invalid positional parameter example**

```json
"scripts": [
   {
      "text": "SELECT * FROM customers WHERE first_name = $1; SELECT * FROM customers WHERE age = $2;",
      "type": "Query",
      "parameters": [
        {
          "name": null,
          "type": "String",
          "value": "John",
          "direction": "Input",
          "size": 256
        },
        {
          "name": null,
          "type": "INT32",
          "value": 52,
          "direction": "Input"
        }
      ]
   }
]
```

### Advanced Settings

#### Script block execution time out

You can configure a time-out in minutes for each individual script block run. If any script block within your script activity exceeds the specified time-out, the entire activity fails.

:::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/script-block-timeout.png" alt-text="Screenshot that shows an advanced setting in script activity to set script block execution time-out." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/script-block-timeout.png":::

```JSON
   "typeProperties": {
      "scripts": [
         {
               "type": "Query",
               "text": "SELECT pg_sleep(40);"
         },
         {
               "type": "Query",
               "text": "SELECT pg_sleep(40);"
         },
         {
               "type": "Query",
               "text": "SELECT pg_sleep(40);"
         }
      ],
      "scriptBlockExecutionTimeout": "00:01:00"
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

:::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-script-activity/logging-activity-output.png" alt-text="Screenshots that show an activity output logging example." lightbox="./media/how-to-use-microsoft-fabric-data-factory-script-activity/logging-activity-output.png":::

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