---
title: Migrate Data from DynamoDB to Azure Cosmos DB for NoSQL
description: Learn about data migration options from DynamoDB to Azure Cosmos DB, and walk through an offline migration process by using Azure services.
author: abhirockzz
ms.author: guabhishek
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.collection:
 - migration
 - aws-to-azure
ms.topic: how-to
ms.date: 02/21/2025
appliesto:
  - ✅ NoSQL
---

# Migrate data from DynamoDB to Azure Cosmos DB for NoSQL

This article focuses on *data migration* from Amazon DynamoDB to Azure Cosmos DB for NoSQL. Before you begin, it's important to understand the difference between data migration and application migration:

- Data migration likely has many steps, including exporting data from the source system (DynamoDB in this case), doing additional processing such as transformations, and finally writing the data to Azure Cosmos DB.
- Application migration includes refactoring your application to use Azure Cosmos DB instead of DynamoDB. This process could include adapting and rewriting queries, redesigning partitioning strategies, indexing, ensuring consistency, and more.

Depending on your requirements, you can migrate data in parallel with migrating an application. But data migration is often a prerequisite to application migration. To learn more about application migration, see [Migrate your application from Amazon DynamoDB to Azure Cosmos DB](dynamo-to-cosmos.md).

## Migration techniques

Various migration techniques are available. Two frequently used techniques are:

- **Online migration**: Choose this technique if your applications can't tolerate downtime and you need real-time data migration.
- **Offline migration**: If your application can be temporarily stopped during a maintenance window, you can perform data migration in offline mode. First, you export the data from DynamoDB to an intermediate location. Then, you import the data to Azure Cosmos DB.

  There are several options for this technique. This article covers one such option.

Select a technique based on your specific requirements. It's also possible to combine them. For example, you could migrate data in bulk by using an offline process and then switch to an online mode. This choice might be suitable if you need to (temporarily) continue using DynamoDB in parallel with Azure Cosmos DB and you want the data to be synchronized in real time.

We recommend that you thoroughly evaluate and test the options by using a proof-of-concept phase before actual migration. This phase can help assess complexity, assess feasibility, and fine-tune your migration plan.

### Offline migration approaches

The approach that this article follows is just one of the many ways to migrate data from DynamoDB to Azure Cosmos DB. It has its own set of pros and cons. Here's a non-exhaustive list of approaches for offline migration:

| Approach | Pros | Cons |
|----------|------|------|
| Export from DynamoDB to S3, load to Azure Data Lake Storage Gen2 by using Azure Data Factory, and write to Azure Cosmos DB by using Spark on Azure Databricks. | Decouples storage and processing. Spark provides scalability and flexibility (additional data transformations, processing). | Multistage process increases complexity and overall latency. Requires knowledge of Spark. |
| Export from DynamoDB to S3, and use Azure Data Factory to read from S3 and write to Azure Cosmos DB. | Low/No-code approach. Spark skillset not required. Suitable for simple data transformations. | Complex transformation might be difficult to implement. |
| Use Spark on Azure Databricks to read from DynamoDB and write to Azure Cosmos DB. | Fit for small datasets, because direct processing avoids extra storage costs. Supports complex transformations (Spark). | Higher cost on the DynamoDB side due to RCU consumption. (S3 export not used.) Requires knowledge of Spark. |

### Online migration approaches

Online migration generally uses a change data capture (CDC) mechanism to stream data changes from DynamoDB. These changes often tend to be real time or near real time. You need to build another component to process the streaming data and write it to Azure Cosmos DB. Here's a non-exhaustive list of approaches for online migration:

| Approach | Pros | Cons |
|----------|------|------|
| Use DynamoDB CDC with DynamoDB Streams, process by using AWS Lambda, and write to Azure Cosmos DB. | DynamoDB Streams provides an ordering guarantee. Event-driven processing. Suitable for simple data transformations. | DynamoDB Streams data retention is 24 hours. Need to write custom logic (Lambda function). |
| Use DynamoDB CDC with Kinesis Data Streams, process by using Kinesis or Flink, and write to Azure Cosmos DB. | Supports complex data transformations (windowing/aggregation with Flink) and provides better control over processing. Retention is flexible (from 24 hours, extendable to 365 days). | No ordering guarantee. Need to write custom logic (Flink job, Kinesis Data Streams consumer). Requires stream processing expertise. |

## Offline migration walkthrough

This section covers how to use Azure Data Factory, Azure Data Lake Storage, and Spark on Azure Databricks for data migration. The following diagram illustrates the main steps.

:::image type="content" source="./media/migrate-data-dynamodb-to-cosmosdb/architecture.png" alt-text="Diagram of the three main steps in the process of offline migration." lightbox="./media/migrate-data-dynamodb-to-cosmosdb/architecture.png":::

1. Export data from a DynamoDB table to S3 in DynamoDB JSON format by using the native DynamoDB export capability.
2. Write the DynamoDB table data in S3 to Data Lake Storage Gen2 by using an Azure Data Factory pipeline.
3. Process the data in Azure Storage by using Spark on Azure Databricks, and write the data to Azure Cosmos DB.

### Prerequisites

Before you proceed, create the following items:

- [Azure Cosmos DB account](quickstart-portal.md#create-an-account)
- [Storage account](/azure/storage/common/storage-account-create?toc=%2Fazure%2Fstorage%2Fblobs%2Ftoc.json&bc=%2Fazure%2Fstorage%2Fblobs%2Fbreadcrumb%2Ftoc.json&tabs=azure-portal) of type *Standard general-purpose v2*
- [Azure data factory](/azure/data-factory/quickstart-create-data-factory)
- AWS account and Amazon DynamoDB tables to migrate data from

> [!TIP]
> If you want to try this walkthrough in a new DynamoDB table, you can use [this data loader tool](https://github.com/AzureCosmosDB/migration-dynamodb-to-cosmosdb-nosql/tree/main/data_loader) to populate your table with sample data.

### Step 1: Export data from DynamoDB to Amazon S3

DynamoDB S3 export is a built-in solution for exporting DynamoDB data to an Amazon S3 bucket. For steps on how to execute this process, including setting up necessary S3 permissions, follow the [DynamoDB documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/S3DataExport_Requesting.html). DynamoDB supports DynamoDB JSON and Amazon Ion as the file formats for exported data.

This walkthrough uses data exported in DynamoDB JSON format.

### Step 2: Use Azure Data Factory to transfer S3 data to Azure Storage

Clone the GitHub repository to your local machine by using the following command. The repository contains the Azure Data Factory pipeline template and the Spark notebook that you'll use later in this article.

```bash
git clone https://github.com/AzureCosmosDB/migration-dynamodb-to-cosmosdb-nosql
```

Use the Azure portal to create linked services:

1. In the Azure portal, go to your Azure data factory. Select **Launch Studio** to open Azure Data Factory Studio.

1. [Create an Azure Data Factory linked service for Amazon S3](/azure/data-factory/connector-amazon-simple-storage-service?tabs=data-factory#create-an-amazon-simple-storage-service-s3-linked-service-using-ui). Enter the details for the S3 bucket to which you exported table data earlier.

1. [Create an Azure Data Lake Storage Gen2 linked service](/azure/data-factory/connector-azure-data-lake-storage?tabs=data-factory#create-an-azure-data-lake-storage-gen2-linked-service-using-ui). Enter the details for the storage account that you created earlier.

:::image type="content" source="./media/migrate-data-dynamodb-to-cosmosdb/linked-services.png" alt-text="Screenshot that shows selections for creating linked services in the Azure portal." lightbox="./media/migrate-data-dynamodb-to-cosmosdb/linked-services.png":::

Use the Azure portal to [create an Azure Data Factory pipeline](/azure/data-factory/concepts-pipelines-activities?tabs=data-factory#creating-a-pipeline-with-ui). A Data Factory pipeline is a logical grouping of activities that together perform a task.

1. In Data Factory Studio, go to the **Author** tab.

1. Select the plus sign. On the menu that appears, select **Pipeline**, and then select **Import from pipeline template**.

   :::image type="content" source="./media/migrate-data-dynamodb-to-cosmosdb/pipeline-import.png" alt-text="Screenshot that shows selections for importing a pipeline from a template." lightbox="./media/migrate-data-dynamodb-to-cosmosdb/pipeline-import.png":::

1. Select the template file (**S3ToADLSGen2.zip**) that you cloned from the GitHub repository.

1. In the configuration, select the linked services that you created for Amazon S3 and Azure Data Lake Storage Gen2. Then select **Use this template** to create the pipeline.

   :::image type="content" source="./media/migrate-data-dynamodb-to-cosmosdb/use-linked-services.png" alt-text="Screenshot that shows boxes for selecting linked services for a template file." lightbox="./media/migrate-data-dynamodb-to-cosmosdb/use-linked-services.png":::

1. Select the pipeline, go to **Source**, and edit the source (Amazon S3) dataset.

   :::image type="content" source="./media/migrate-data-dynamodb-to-cosmosdb/edit-source-dataset.png" alt-text="Screenshot of editing a source dataset." lightbox="./media/migrate-data-dynamodb-to-cosmosdb/edit-source-dataset.png":::

1. In **File path**, enter the path to the exported files in your Amazon S3 bucket.

   :::image type="content" source="./media/migrate-data-dynamodb-to-cosmosdb/edit-source-dataset-2.png" alt-text="Screenshot of the tab for entering a file path to exported files." lightbox="./media/migrate-data-dynamodb-to-cosmosdb/edit-source-dataset-2.png":::

   > [!IMPORTANT]
   > You can also edit the sink dataset to update the name of the storage container in which the data from S3 will be stored. The container is named `s3datacopy` by default.

1. After you finish making changes, select **Publish all** to publish the pipeline.

To trigger the pipeline manually:

1. Choose the pipeline. At the top of the pipeline editor, select **Add trigger**.

2. Select **Trigger now**, and then select **Ok**.

   :::image type="content" source="./media/migrate-data-dynamodb-to-cosmosdb/pipeline-trigger.png" alt-text="Screenshot of selections for triggering a pipeline manually." lightbox="./media/migrate-data-dynamodb-to-cosmosdb/pipeline-trigger.png":::

As the pipeline continues to run, you can [monitor it](/azure/data-factory/monitor-visually#monitor-pipeline-runs). After it finishes successfully, check the list of containers in the Azure storage account that you created earlier.

:::image type="content" source="./media/migrate-data-dynamodb-to-cosmosdb/pipeline-run.png" alt-text="Screenshot of the area for monitoring a pipeline run." lightbox="./media/migrate-data-dynamodb-to-cosmosdb/pipeline-run.png":::

Verify that a new container was created, along with the contents of the S3 bucket.

:::image type="content" source="./media/migrate-data-dynamodb-to-cosmosdb/container-created.png" alt-text="Screenshot of a created storage container." lightbox="./media/migrate-data-dynamodb-to-cosmosdb/container-created.png":::

### Step 3: Import Data Lake Storage Gen2 data into Azure Cosmos DB by using Spark on Azure Databricks

This section covers how to use the [Azure Cosmos DB Spark connector](https://github.com/Azure/azure-cosmosdb-spark) to write data in Azure Cosmos DB. The Azure Cosmos DB Spark connector provides Apache Spark support for the Azure Cosmos DB NoSQL API. You can use it to read from and write to Azure Cosmos DB via Apache Spark DataFrames in Python and Scala.

Start by creating an [Azure Databricks workspace](/azure/databricks/getting-started/free-trial#portal). To learn about version compatibility for components like the Azure Cosmos DB Spark connector, Apache Spark, JVM, Scala, and Databricks Runtime, refer to the [compatibility matrix](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/cosmos/azure-cosmos-spark_3-5_2-12#version-compatibility).

:::image type="content" source="./media/migrate-data-dynamodb-to-cosmosdb/databricks-spark-version.png" alt-text="Screenshot that shows a Databricks Runtime version in the creation of an Azure Databricks workspace." lightbox="./media/migrate-data-dynamodb-to-cosmosdb/databricks-spark-version.png":::

After you create the Azure Databricks workspace, follow the [documentation to install the appropriate Spark connector version](/azure/databricks/libraries/package-repositories#maven-libraries). The rest of the steps in this article work with connector version 4.36.0 with Spark 3.5.0 on Databricks Runtime 15.4 (with Scala 2.12). For the Maven coordinates of the connector, see the [Maven Central repository](https://central.sonatype.com/artifact/com.azure.cosmos.spark/azure-cosmos-spark_3-5_2-12/4.36.0).

:::image type="content" source="./media/migrate-data-dynamodb-to-cosmosdb/spark-connector-maven-package.png" alt-text="Screenshot of Spark connector versions in the Maven Central repository." lightbox="./media/migrate-data-dynamodb-to-cosmosdb/spark-connector-maven-package.png":::

[A notebook on GitHub](https://github.com/AzureCosmosDB/migration-dynamodb-to-cosmosdb-nosql/blob/main/migration.ipynb) (`migration.ipynb`) has the Spark code for reading data from Data Lake Storage Gen2 and writing it to Azure Cosmos DB. [Import the notebook](/azure/databricks/notebooks/notebook-export-import#import-a-notebook) into your Azure Databricks workspace.

#### Configure Microsoft Entra ID authentication

Use [OAuth 2.0 credentials with Microsoft Entra ID service principals](/azure/databricks/connect/storage/azure-storage#connect-to-azure-data-lake-storage-gen2-or-blob-storage-using-azure-credentials) to connect to Azure Storage from Azure Databricks. Follow the [documentation](/azure/databricks/connect/storage/aad-storage-service-principal) to complete these steps:

1. Register a Microsoft Entra ID application, and create a new client secret. This is a one-time step.

   As part of the process, note the client ID, client secret, and tenant ID. You'll use them in subsequent steps.

1. In your Azure storage account, under **Access control (IAM)**, assign the **Storage Blob Data Reader** role to the Microsoft Entra ID application that you created.

Follow these steps to configure Microsoft Entra ID authentication for Azure Cosmos DB:

1. In the Azure Cosmos DB account, under **Access control (IAM)**, assign the **Cosmos DB Operator** role to the Microsoft Entra ID application that you created.

1. Use the following command in the Azure CLI to create the Azure Cosmos DB role definition and get the role definition ID. If you don't have the [Azure CLI set up](/cli/azure/get-started-with-azure-cli), you can choose to use [Azure Cloud Shell](/azure/cloud-shell/get-started/classic?tabs=azurecli) directly from the Azure portal instead.

    ```azurecli
    az cosmosdb sql role definition create --resource-group "<resource-group-name>" --account-name "<account-name>" --body '{
            "RoleName": "<role-definition-name>",
            "Type": "CustomRole",
            "AssignableScopes": ["/"],
            "Permissions": [{
                "DataActions": [
                    "Microsoft.DocumentDB/databaseAccounts/readMetadata",
                    "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*",
                    "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*"
                ]
            }]
        }'
    
    // List the role definition you created to fetch its unique identifier in the JSON output. Record the id value of the JSON output.
    
    az cosmosdb sql role definition list --resource-group "<resource-group-name>" --account-name "<account-name>"
    ```

1. After you create the role definition and obtain the role definition ID, use the following command to [get the service principal ID associated with the Microsoft Entra ID application](/entra/identity-platform/app-objects-and-service-principals?tabs=azure-cli#list-service-principals-associated-with-an-app). Replace `AppId` with the client ID of the Microsoft Entra ID application.

    ```azurecli
    SP_ID=$(az ad sp list --filter "appId eq '{AppId}'" | jq -r '.[0].id')
    ```

1. Create the role assignment by using the following command. Make sure to replace the resource group name, Azure Cosmos DB account name, and role definition ID.

    ```azurecli
    az cosmosdb sql role assignment create --resource-group <enter resource group name> --account-name <enter cosmosdb account name> --scope "/" --principal-id $SP_ID --role-definition-id <enter role definition ID> --scope "/"
    ```

#### Run steps in the notebook

Run the first two steps to install required dependencies:

```bash
pip install azure-cosmos azure-mgmt-cosmosdb azure.mgmt.authorization

dbutils.library.restartPython()
```

The third step reads DynamoDB data from Data Lake Storage Gen2 and stores it in a DataFrame. Before you run the step, replace the following information with the corresponding values in your setup:

| Variable             | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `storage_account_name` | Azure storage account name.                                                  |
| `container_name`       | Azure storage container name. For example: `s3datacopy`.                               |
| `file_path`            | Path to the folder that contains the exported JSON files in the Azure storage container. For example: `AWSDynamoDB/01738047791106-7ba095a9/data/*`. |
| `client_id`            | Application (client) ID of the Microsoft Entra ID application (found on the **Overview** page). |
| `tenant_id`            | Directory (tenant) ID of the Microsoft Entra ID application (found on the **Overview** page). |
| `client_secret`        | Value of the client secret associated with the Microsoft Entra ID application (found in **Certificates & secrets**). |

If necessary, you can run the next cell (the fourth step) to execute any data transformations or implement custom logic. For example, you could add an `id` field to your data before writing it to Azure Cosmos DB.

Run the fifth step to create the Azure Cosmos DB database and container. Use the [Catalog API of the Azure Cosmos DB Spark connector](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/cosmos/azure-cosmos-spark_3/docs/catalog-api.md). Replace the following information with the corresponding values in your setup:

| Variable            | Description                                                                                          |
|---------------------|--------------------------------------------------------------------------------------------------|
| `cosmosEndpoint`     | URI of the Azure Cosmos DB account.                                                                     |
| `cosmosDatabaseName` | Name of the Azure Cosmos DB database that you want to create.                                               |
| `cosmosContainerName` | Name of the Azure Cosmos DB container that you want to create.                                             |
| `subscriptionId`     | Azure subscription ID.                                                                           |
| `resourceGroupName`  | Azure Cosmos DB resource group name.                                                                  |
| `partitionKeyPath`   | Partition key for the container. For example: `/id`.                                                     |
| `throughput`         | Container throughput. For example: `1000`.<br><br> Be mindful of the throughput that you associate with the container. You might need to adjust this value, depending on the volume of data to be migrated. |
| `client_id`          | Application (client) ID of the Microsoft Entra ID application (found on the **Overview** page).           |
| `tenant_id`          | Directory (tenant) ID of the Microsoft Entra ID application (found on the **Overview** page).              |
| `client_secret`      | Value of the client secret associated with the Microsoft Entra ID application (found in **Certificates & secrets**). |

Run the sixth and final step to write data to Azure Cosmos DB. Replace the following information with the corresponding values in your setup:

| Variable            | Description                                                                                          |
|---------------------|--------------------------------------------------------------------------------------------------|
| `cosmosEndpoint`     | URI of the Azure Cosmos DB account.                                                                     |
| `cosmosDatabaseName` | Name of the Azure Cosmos DB database that you want to create.                                               |
| `cosmosContainerName` | Name of the Azure Cosmos DB container that you want to create.                                             |
| `subscriptionId`     | Azure subscription ID.                                                                           |
| `resourceGroupName`  | Azure Cosmos DB resource group name.                                                                  |
| `client_id`          | Application (client) ID of the Microsoft Entra ID application (found on the **Overview** page).           |
| `tenant_id`          | Directory (tenant) ID of the Microsoft Entra ID application (found on the **Overview** page).              |
| `client_secret`      | Value of the client secret associated with the Microsoft Entra ID application (found in **Certificates & secrets**). |

After the cell execution finishes, check the Azure Cosmos DB container to verify that the data was migrated successfully.

## Related content

- [Migrate your application from Amazon DynamoDB to Azure Cosmos DB](dynamo-to-cosmos.md)
