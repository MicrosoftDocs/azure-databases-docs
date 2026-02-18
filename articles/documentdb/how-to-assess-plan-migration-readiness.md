---
title: Assess for readiness and plan migration
description: Assess an existing MongoDB installation to determine if it's suitable for migration to Azure DocumentDB.
author: sandnair
ms.author: sandnair
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 10/24/2023
# CustomerIntent: As a database owner, I want to assess my existing MongoDB installation so that I can ensure that I can migrate to Azure DocumentDB.
---

# Assess a MongoDB installation and plan for migration to Azure DocumentDB

Carry out up-front planning tasks and make critical decisions before migrating your data to Azure DocumentDB. These decisions make your migration process run smoothly.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

- An existing MongoDB installation.

## Assess the compatibility and readiness of your resources for migration

Before planning your migration, assess the state of your existing MongoDB resources to help plan for migration. 
Use the **Azure DocumentDB Migration extension** in VS Code to assess the [compatibility and readiness](compatibility-features.md) of your workloads while planning the migration from MongoDB to Azure DocumentDB. The end-to-end assessment and find out the actions that you need to take to seamlessly run your workloads on Azure DocumentDB. The assessment report presents findings at the account, database, and collection levels, each marked as Critical, Warning, or Informational based on severity to aid prioritization. The report includes:

- **Unsupported Features and Syntax**: It flags unsupported MongoDB features, commands, query syntax, and index types, with usage frequency to prioritize fixes.

- **Resource-Specific Recommendations**: Each finding includes the affected resource name, actionable recommendations, and relevant technical details for remediation.

- **Environment Overview**: Summarizes key aspects of the source MongoDB environment—such as version, license, instance type, and stats for databases and collections.

- **Compatibility and Platform Constraints**: Details Azure DocumentDB-specific quotas, limits, and potential shard key incompatibilities for sharded workloads.

### Run an Assessment

1. To get started, install the **Azure DocumentDB Migration** extension in VS Code. This will automatically install its prerequisite, the **DocumentDB for VS Code** extension.
2. Open the **DocumentDB for VS Code** extension. 
1. Add the MongoDB server you want to assess for migration to the **Document DB Connections** list.
1. Expand the selected connection, then Right-click and choose **Data Migration...**.
:::image type="content" source="media/how-to-assess-plan-migration-readiness/documentdb-connections.png" alt-text="Screenshot of the Right Click menu in Document DB Connections.":::
1. From the command palette, select **Pre-Migration Assessment for Azure DocumentDB**.
 :::image type="content" source="media/how-to-assess-plan-migration-readiness/command-palette.png" alt-text="Screenshot of the command palette in Visual Studio Code.":::
1. The assessment wizard guides you through three steps. In the **Start Validation** step, select **Run Validation** to verify credentials, prerequisites, and connectivity before proceeding. 
:::image type="content" source="media/how-to-assess-plan-migration-readiness/start-validation.png" alt-text="Screenshot of the Start Validation step in the assessment wizard.":::

    > [!Important]
    > To perform an assessment, the connected MongoDB user must have the [readAnyDatabase](https://www.mongodb.com/docs/manual/reference/built-in-roles/#mongodb-authrole-readAnyDatabase) and [clusterMonitor](https://www.mongodb.com/docs/manual/reference/built-in-roles/#mongodb-authrole-clusterMonitor) roles assigned on the source instance. If you selected the **Include role & user details in assessment** check box, the user must have [userAdminAnyDatabase](https://www.mongodb.com/docs/manual/reference/built-in-roles/#mongodb-authrole-userAdminAnyDatabase) or [root](https://www.mongodb.com/docs/manual/reference/built-in-roles/#mongodb-authrole-root) roles assigned on the source instance.

6. In the **Fill in Assessment Details** step, provide the necessary inputs:
    :::image type="content" source="media/how-to-assess-plan-migration-readiness/fill-assessment-details.png" alt-text="Screenshot of the Fill in Assessment Details step in the assessment wizard.":::
    - Enter a title in the **Assessment name** field.
    - Select **vCore** from the **Offering** dropdown.
    - Provide the path to MongoDB logs.
    > [!TIP]
    > While optional, specifying the logs path allows for more detailed findings at the collection level. If omitted, the tool relies on data from the `serverStatus` command, which only reflects feature usage since the last restart. Allow sufficient time to pass after the last server restart for an accurate workload assessment.

    - Provide the path to data assessment logs.
    > [!TIP]
    > Though optional, supplying data assessment logs enhances workload insights. These logs are generated by scanning data and reading verbose logs. The data assessment runs independently as a CLI before initiating the migration assessment, and the resulting JSON is used here. Download the data assessment CLI [here](https://aka.ms/MongoMigrationDataAssessment).

7. Select **Start Assessment** to begin the assessment process.
8. In the **Get Your Report** step, wait for the assessment to complete. The duration depends on the size of your source server.
:::image type="content" source="media/how-to-assess-plan-migration-readiness/assessment-in-progress.png" alt-text="Screenshot of the Get Your Report step in the assessment wizard while assessment is in progress.":::
9. Once the assessment is finished, select **Download Report** to retrieve the HTML report.
:::image type="content" source="media/how-to-assess-plan-migration-readiness/assessment-completed.png" alt-text="Screenshot of the Get Your Report step in the assessment wizard after assessment is completed.":::

### View Past Assessments

Reviewing previous assessments can be valuable. Use the **View Past Assessments** tab to access detailed historical reports. The assessment list includes all assessments initiated on the current machine for the selected connection.

:::image type="content" source="media/how-to-assess-plan-migration-readiness/view-all-assessments.png" alt-text="Screenshot of the View Past Assessment tab in the extension.":::

### FAQ

#### How do I proceed if the "Run Validation" step fails?

Check the error message displayed in the extension to determine the cause of the validation failure. Common issues include an inability to connect to the MongoDB endpoint or insufficient user privileges on the connected server.

To run an assessment, ensure that the connected MongoDB user has the [`readAnyDatabase`](https://www.mongodb.com/docs/manual/reference/built-in-roles/#mongodb-authrole-readAnyDatabase) and [`clusterMonitor`](https://www.mongodb.com/docs/manual/reference/built-in-roles/#mongodb-authrole-clusterMonitor) roles assigned on the source instance.

Use [`grantRolesToUser`](https://www.mongodb.com/docs/manual/reference/method/db.grantRolesToUser/) to assign the necessary roles to the current user.

#### How can I view collection and database names in "Feature Compatibility" assessments?

The `serverStatus` command is used for feature compatibility assessments. However, this command doesn't provide database or collection names, which prevents the extension from reporting them.

For more detailed assessment results, rerun the assessment and specify the folder containing MongoDB logs in the **Log Folder Path** field.

#### How do I configure my source server firewall to prevent connectivity issues?

Ensure that the source MongoDB instance allows incoming connections from your machine.

#### How many assessments can I run concurrently?

There's no limit to the number of assessments you can run at the same time. However, running multiple assessments in parallel strain the compute resources on both your machine and the source server, potentially affecting performance.

#### What information is included in an assessment report?

The report begins with key details about the assessment, including a summary of the source MongoDB environment. This section covers the source MongoDB version, license type, and instance type. It also lists the assessed databases and collections, along with their assessment summaries and migration readiness.

Findings are categorized into **Critical**, **Warning**, and **Informational**, helping you prioritize them based on importance.

The assessment includes checks for:

| Category | Description |
| --- | --- |
| **Collection Options** | Identifies unsupported collection settings, such as time-series configurations and collations. |
| **Features** | Detects unsupported database commands, query syntax, and operators, including aggregation pipeline queries. The extra details column shows how frequently each feature was used on the source instance. |
| **Limits and Quotas** | Highlights Azure DocumentDB quotas and limitations. |
| **Indexes** | Flags unsupported MongoDB index types and properties. |
| **Shard Keys** | Identifies unsupported shard key configurations. |

#### What type of logs does the extension generate?

The extension records errors, warnings, and other diagnostic logs in the default log directory:

- **Windows** - `C:\Users\<username>\.dmamongo\logs\`
- **Linux** - `~/.dmamongo/logs`
- **macOS** - `/Users/<username>/.dmamongo/logs`

> [!NOTE]
> A separate log file is created for each day. By default, the extension stores the last seven log files.

## Capacity planning

### Cluster Tier
Begin with a cluster tier that aligns with your source database configurations. Conduct load and performance tests to determine the optimal balance between cost and performance.

### Storage Tier
Ensure your target account is provisioned with adequate storage to meet your data requirements during and after migration. Start by migrating a small dataset to assess storage consumption, then scale the estimate based on the total data size to determine the necessary storage allocation. Reserve extra space to accommodate incoming data and future growth.

## Next step

> [!div class="nextstepaction"]
> [Migrate data from MongoDB to Azure DocumentDB](migration-options.md)
