---
title: "Initiate the cutover (online)"
description: Initiate the cutover (online).
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 07/17/2025
ms.service: azure-database-postgresql
ms.topic: include
---
## Initiate the cutover

You can initiate the cutover using Azure portal or Azure CLI.

#### [Portal](#tab/portal)

For **Validate and migrate** option, completing of the online migration requires the user to complete an additional step, which is to trigger the cutover action. After the copying or cloning of the base data is complete, the migration moves to the `Waiting for user action` status and the `Waiting for cutover trigger` substatus. In this status, the user can trigger the cutover from the portal by selecting the migration.

Before initiating cutover, it's important to ensure that:

- Writes to the source are stopped - `latency` value is 0 or close to 0. The `latency` information can be obtained from the migration details screen as shown below:
- `latency` value decreases to 0 or close to 0
- The `latency` value indicates when the target last synced with the source. Writing to the source can be stopped at this point, and a cutover can be initiated. In case there's heavy traffic at the source, it's recommended to stop writes first so that `latency` can come close to 0, and then a cutover is initiated.

The cutover operation applies all pending changes from the source server to the target server, and completes the migration. If you trigger a cutover, even with nonzero `latency`, the replication stops until that point in time. All the data on the source until the cutover point is then applied to the target. If you experience a latency of 15 minutes at the cutover point, all the changes made to data in the last 15 minutes are applied to the target.

The time depends on the backlog of changes occurring in the last 15 minutes. Hence, it's recommended that the latency goes to zero or near zero before triggering the cutover.

- The migration moves to the `Succeeded` status when the `Migrating data` substatus or the cutover (in online migration) finishes successfully. If there's a problem at the `Migrating data` substatus, the migration moves into a `Failed` status.

#### [CLI](#tab/cli)

For **Validate and migrate** option, completing of the online migration requires the user to complete an additional step, which is to trigger the cutover action. After the copying or cloning of the base data is complete, the migration moves to the `Waiting for user action` status and the `Waiting for cutover trigger` substatus. In this state, the user can trigger the cutover through the CLI using the command below. The cutover can also be triggered from the portal by selecting the migration name in the migration grid.

Before initiating cutover, it's important to ensure that:

- Writes to the source are stopped - `latency` value is 0 or close to 0. The `latency` information can be obtained from the migration details screen as shown below:
- `latency` value decreases to 0 or close to 0
- The `latency` value indicates when the target last synced with the source. Writing to the source can be stopped at this point, and a cutover can be initiated. In case there's heavy traffic at the source, it's recommended to stop writes first so that `latency` can come close to 0, and then a cutover is initiated.

The cutover operation applies all pending changes from the source server to the target server, and completes the migration. If you trigger a cutover, even with nonzero `latency`, the replication stops until that point in time. All the data on the source until the cutover point is then applied to the target. If you experience a latency of 15 minutes at the cutover point, all the changes made to data in the last 15 minutes are applied to the target.

The time depends on the backlog of changes occurring in the last 15 minutes. Hence, it's recommended that the latency goes to zero or near zero before triggering the cutover.

- The migration moves to the `Succeeded` status when the `Migrating data` substatus or the cutover (in online migration) finishes successfully. If there's a problem at the `Migrating data` substatus, the migration moves into a `Failed` status.

To trigger the cutover, use the following command:

    ```azurecli-interactive
    az postgres flexible-server migration update --subscription <subscription_id> --resource-group <resource_group> --name <server> --migration-name <migration> --cutover
    ```

---
