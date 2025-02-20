---
title: Data migration from DynamoDB to Azure Cosmos DB for NoSQL
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn about data migration options from DynamoDB to Azure Cosmos DB and walk through an offline migration process using Azure Data Factory, Azure Data Lake Storage, and Spark on Azure Databricks.
author: abhirockzz
ms.author: guabhishek
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 02/21/2025
---

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

## Introduction

This article focuses on the data migration from Amazon DynamoDB to Azure Cosmos DB for NoSQL. While there are multiple factors to consider for a migration, one key aspect is understanding the difference between application and data migration. Since DynamoDB already contains application data, you'll first need to migrate it to Azure Cosmos DB. This should be done in the data migration phase which will likely have many substeps including exporting, data transformations, and writing data into Azure Cosmos DB. This can be done in parallel to application migration, but it’s often a prerequisite to it.  

Application migration includes refactoring your application to use Azure Cosmos DB instead of DynamoDB. Depending on your application, this could include adapting and rewriting queries, redesigning partitioning strategies, indexing, consistency, and other components. In the final cutover phase, you'll need to point your application to Azure Cosmos DB and start writing application data to it directly.

> [!IMPORTANT]
> Refer to [Migrate your application from Amazon DynamoDB to Azure Cosmos DB](dynamo-to-cosmos.md) to dive into application migration. 

## Migration options

There are various migration strategies available; two frequently utilized techniques are offline and online migration. The selection should be based on your specific requirements. It's also possible to implement either one independently or employ a combination of both approaches.

1. **Online migration**: Choose this approach if your applications can't tolerate downtime and real-time data migration is required. Refer to the section [Overview of other offline migration approaches](#overview-of-other-offline-migration-approaches) for options.
2. **Offline migration**: If your application can be temporarily stopped during a maintenance window, data migration can be performed in offline mode by exporting the data from DynamoDB to an intermediate location, and then importing it into Azure Cosmos DB. There are several options for this approach. This article covers one such method. Refer to the section [Overview of online migration approaches](#overview-of-online-migration-approaches) for a list of alternatives.

> [!TIP]
> You could also follow an approach where data is migrated in bulk using an offline process and then switch to an online mode. This might be suitable if you have a need to (temporarily) continue using DynamoDB in parallel with Azure Cosmos DB and want the data to be synchronized in real-time.

## Offline migration walkthrough

This section covers how to use Azure Data Factory, Azure Data Lake Storage, and Spark on Azure Databricks for data migration.

![Solution overview](images/architecture.png)

1. First, data from DynamoDB table is exported to S3 (in DynamoDB JSON format) using native DynamoDB export capability.
2. The DynamoDB table data in S3 is written to Azure Data Lake Storage using an Azure Data Factory pipeline. Azure Data Lake Storage is a cloud-based, enterprise data lake solution built on Azure Blob Storage. Azure Data Lake Storage Gen2 is a configurable capability of a StorageV2 (General Purpose V2) Azure Storage which can be enabled by selecting the option to Enable hierarchical namespace when creating the Azure storage account. Azure Data Factory is a managed cloud service built for complex hybrid extract-transform-load (ETL), extract-load-transform (ELT), and data integration projects. 
3. Finally, data in Azure storage is processed using Spark on Azure Databricks and written to Azure Cosmos DB. Azure Databricks is a unified, open analytics platform for building, deploying, sharing, and maintaining enterprise-grade data, analytics, and AI solutions at scale. It provides an optimized, efficient, and simple platform for running Apache Spark workloads.

## Prerequisites

Before you proceed, make sure you complete the following:

- [Create a storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?toc=%2Fazure%2Fstorage%2Fblobs%2Ftoc.json&bc=%2Fazure%2Fstorage%2Fblobs%2Fbreadcrumb%2Ftoc.json&tabs=azure-portal) of type *Standard general-purpose v2*. 
- [Create an Azure data factory](https://learn.microsoft.com/en-us/azure/data-factory/quickstart-create-data-factory)

You should also have an Amazon Web Services (AWS) account and Amazon DynamoDB tables to migrate data from.

> [!TIP]
> If you're looking to try this out in a new DynamoDB table, you can use this [data loader utility](https://github.com/AzureCosmosDB/migration-dynamodb-to-cosmosdb-nosql/tree/main/data_loader) to populate your table with sample data.

## Step 1: Export data from DynamoDB to Amazon S3

DynamoDB S3 export is a built-in solution for exporting DynamoDB data to an Amazon S3 bucket. Follow the [DynamoDB documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/S3DataExport_Requesting.html) for exact steps on how to execute this process, including setting up necessary S3 permissions, etc. DynamoDB supports DynamoDB JSON and Amazon Ion as the file formats for exported data. 

Once data is exported to a S3 bucket, proceed to the next step.

## Step 2: Use Azure Data Factory to transfer S3 data into Azure Storage

Clone the GitHub repository to your local machine. It contains the Azure Data Factory pipeline template and the Spark notebook that you use later on.

```bash
git clone https://github.com/AzureCosmosDB/migration-dynamodb-to-cosmosdb-nosql
```

In the Azure portal, navigate to the Azure data factory created earlier, select **Launch Studio** to open Azure Data Factory Studio, and complete the following steps:

1. Create an [Azure Data Factory linked service for Amazon S3](https://learn.microsoft.com/en-us/azure/data-factory/connector-amazon-simple-storage-service?tabs=data-factory#create-an-amazon-simple-storage-service-s3-linked-service-using-ui). Enter the details for the S3 bucket to which you exported table data earlier. 
1. Next, create an [Azure Data Lake Storage (ADLS) Gen2 linked service](https://learn.microsoft.com/en-us/azure/data-factory/connector-azure-data-lake-storage?tabs=data-factory#create-an-azure-data-lake-storage-gen2-linked-service-using-ui). Enter the details for the storage account created earlier.

![Create linked services](images/linked-services.png)

Use the [Azure portal to create a new pipeline](https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities?tabs=data-factory#creating-a-pipeline-with-ui). A Data Factory pipeline is a logical grouping of activities that together perform a task. 

1. Navigate to the **Author** tab in Data Factory Studio, then select the plus sign and choose **Pipeline** from the menu. 
1. From the submenu, choose **Import from pipeline template** and use the template file (*S3ToADLSGen2.zip*) that you cloned from the GitHub repository.

![Import pipeline](images/pipeline-import.png)

In the configuration, select the linked services that you created for Amazon S3 and ADLS Gen2, and choose **Use this template** to create the pipeline.

![Select linked services](images/use-linked-services.png)

Select the pipeline, navigate to **Source**, and edit the source (Amazon S3) dataset.

![Edit source dataset](images/edit-source-dataset.png)

In **File path**, enter the path to the exported files in your Amazon S3 bucket.

![Edit source dataset S3 bucket path](images/edit-source-dataset-2.png)

> [!IMPORTANT]
> You can also edit the sink dataset to update the name of the storage container in which the data from S3 will be stored. If not, the container is named `s3datacopy` by default.

Once the changes are complete, choose **Publish all** to publish the pipeline. To trigger the pipeline manually:

1. Choose the pipeline, select **Add trigger** at the top of the pipeline editor
2. Select **Trigger now**, and choose **Ok**. 

![Trigger pipeline manually](images/pipeline-trigger.png)

As the pipeline continues to execute, [you can monitor it](https://learn.microsoft.com/en-us/azure/data-factory/monitor-visually#monitor-pipeline-runs). Once it completes successfully, check the list of containers in the Azure Storage account created earlier.

![Monitor pipeline](images/pipeline-run.png)

Verify that a new container was created along with the contents of S3 bucket.

![Verify storage container](images/container-created.png)

## Step 3: Import ADLS data into Azure Cosmos DB using Spark on Azure Databricks

This section covers how to use the [Azure Cosmos DB Spark connector](https://github.com/Azure/azure-cosmosdb-spark) to write data in Azure Cosmos DB. Azure Cosmos DB OLTP Spark connector provides Apache Spark support for Azure Cosmos DB NoSQL API. It allows you to read from and write to Azure Cosmos DB via Apache Spark DataFrames in Python and Scala.

Start by creating an [Azure Databricks workspace](https://learn.microsoft.com/en-us/azure/databricks/getting-started/free-trial#portal). To do that, review the compatibility matrix in terms of versions of various components including the Azure Cosmos DB Spark connector, Apache Spark, JVM, Scala, and Databricks Runtime. Refer to [this documentation](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/cosmos/azure-cosmos-spark_3-5_2-12#version-compatibility) for an exhaustive list.

![Databricks version](images/databricks-spark-version.png)

Once the Databricks workspace is created, [follow the documentation](https://learn.microsoft.com/en-us/azure/databricks/libraries/package-repositories#maven-libraries) to install the appropriate connector version. The rest of the steps in this article work with the connector version `4.36.0` with Spark `3.5.0` on Databricks `15.4` (with Scala `2.12`). Here are the  Maven coordinates of the connector – [com.azure.cosmos.spark:azure-cosmos-spark_3-5_2-12:4.36.0](https://central.sonatype.com/artifact/com.azure.cosmos.spark/azure-cosmos-spark_3-5_2-12/4.36.0)

![Spark connector for Azure Cosmos DB NoSQL](images/spark-connector-maven-pkg.png)

The GitHub repository [contains a notebook](https://github.com/AzureCosmosDB/migration-dynamodb-to-cosmosdb-nosql/blob/main/migration.ipynb) (`migration.ipynb`) with the Spark code to read data from ADLS and write it to Azure Cosmos DB. [Import the notebook](https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-export-import#import-a-notebook) into your Databricks workspace.

### Configure authentication

Use [OAuth 2.0 credentials with Microsoft Entra ID service principals](https://learn.microsoft.com/en-us/azure/databricks/connect/storage/azure-storage#connect-to-azure-data-lake-storage-gen2-or-blob-storage-using-azure-credentials) to connect to Azure storage from Azure Databricks. Follow the [steps in the documentation](https://learn.microsoft.com/en-us/azure/databricks/connect/storage/aad-storage-service-principal) to complete these steps:

1. Register a Microsoft Entra ID application, and create a new client secret. This is a one-time step. As part of the process, note the client ID, client secret, and tenant ID as these will be used in subsequent steps. 
1. In your Azure Storage account, under **Access control (IAM)**, assign the `Storage Blob Data Reader` role to the Microsoft Entra ID application you had created.

Follow these steps to configure Microsoft Entra ID authentication for Azure Cosmos DB:

1. Create an Azure Cosmos DB account (if you don’t already have one).
1. In the Azure Cosmos DB account, under **Access control (IAM)**, assign the `Cosmos DB Operator` role to the Microsoft Entra ID application you had created.
1. Use the Azure CLI to create the Azure Cosmos DB role definition and get the role definition ID

> [!TIP]
> If you don’t have the [Azure CLI setup](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli), you can choose to use [Azure Cloud Shell](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/classic?tabs=azurecli) directly from the Azure portal instead. 

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

1. Once you have created the role definition and obtained the role definition ID, use the following command to [get service principal ID associated with the Microsoft Entra ID application](https://learn.microsoft.com/en-us/entra/identity-platform/app-objects-and-service-principals?tabs=azure-cli#list-service-principals-associated-with-an-app). Replace `AppId` with client ID of the Microsoft Entra ID application:

```azurecli
SP_ID=$(az ad sp list --filter "appId eq '{AppId}'" | jq -r '.[0].id')
```

1. Now, create the role assignment using the below command. Make sure to replace resource group name, Azure Cosmos DB account name, and the role definition ID.

```azurecli
az cosmosdb sql role assignment create --resource-group <enter resource group name> --account-name <enter cosmosdb account name> --scope "/" --principal-id $SP_ID --role-definition-id <enter role definition ID> --scope "/"
```

### Execute the steps in the notebook

The first two steps are required to install required dependencies:

```python
pip install azure-cosmos azure-mgmt-cosmosdb azure.mgmt.authorization
dbutils.library.restartPython()
```

The third step reads DynamoDB data from ADLS and stores it in a data frame. Before running it, replace the following information with the corresponding values in your setup:

| Variable             | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `storage_account_name` | Azure storage account name                                                  |
| `container_name`       | Azure storage container name, for example, s3datacopy                               |
| `file_path`            | Path to the file in Azure storage container, for example, AWSDynamoDB/01738047791106-7ba095a9/data/* |
| `client_id`            | The application (client) ID of the Entra ID application (found on the Overview page) |
| `tenant_id`            | The directory (tenant) ID of the Entra ID application (found on the Overview page) |
| `client_secret`        | Value of the client secret associated with the Entra ID application (found in Certificates & secrets) |

> [!NOTE]
> If necessary, you can run the next step to execute any data transformations or implement custom logic. For example, this could be adding a `id` field to your data before writing it Azure Cosmos DB.

Run **step 5** to create the Azure Cosmos DB database and container. This is done using the [Catalog API of the Azure Cosmos DB Spark connector](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/cosmos/azure-cosmos-spark_3_2-12/docs/catalog-api.md). Replace the following information with the corresponding values in your setup:

| Variable            | Description                                                                                          |
|---------------------|--------------------------------------------------------------------------------------------------|
| `cosmosEndpoint`     | URI of the Cosmos DB account                                                                     |
| `cosmosDatabaseName` | Name of the Cosmos DB database you want to create                                               |
| `cosmosContainerName` | Name of the Cosmos DB container you want to create                                             |
| `subscriptionId`     | Azure Subscription ID                                                                           |
| `resourceGroupName`  | Cosmos DB resource group name                                                                  |
| `partitionKeyPath`   | Partition key for the container, for example, `/id`                                                     |
| `throughput`         | Container throughput, for example, `1000`. Be mindful of the throughput you associate with the container – you may need to adjust this depending on the volume of data to be migrated. |
| `client_id`          | The application (client) ID of the Entra ID application (found on the Overview page)           |
| `tenant_id`          | The directory (tenant) ID of the Entra ID application (found on the Overview page)              |
| `client_secret`      | Value of the client secret associated with the Entra ID application (found in Certificates & secrets) |

Finally, run the last (**step 6**) to write data Azure Cosmos DB. Replace the following information with the corresponding values in your setup:

| Variable            | Description                                                                                          |
|---------------------|--------------------------------------------------------------------------------------------------|
| `cosmosEndpoint`     | URI of the Cosmos DB account                                                                     |
| `cosmosDatabaseName` | Name of the Cosmos DB database you want to create                                               |
| `cosmosContainerName` | Name of the Cosmos DB container you want to create                                             |
| `subscriptionId`     | Azure Subscription ID                                                                           |
| `resourceGroupName`  | Cosmos DB resource group name                                                                  |
| `client_id`          | The application (client) ID of the Entra ID application (found on the Overview page)           |
| `tenant_id`          | The directory (tenant) ID of the Entra ID application (found on the Overview page)              |
| `client_secret`      | Value of the client secret associated with the Entra ID application (found in Certificates & secrets) |

After the cell execution completes, check the Azure Cosmos DB container to verify that the data has been migrated successfully.

## Overview of other offline migration approaches

coming soon

## Overview of online migration approaches

coming soon


## Next steps

> [!div class="nextstepaction"] 
> [Migrate your application from Amazon DynamoDB to Azure Cosmos DB](dynamo-to-cosmos.md)
