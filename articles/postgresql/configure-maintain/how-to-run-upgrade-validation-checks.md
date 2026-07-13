---
title: Upgrade Validation Checks in Azure Database for PostgreSQL Flexible Server
description: This article describes how to run upgrade validation checks for Azure Database for PostgreSQL flexible server before performing a major version upgrade.
#customer intent: As a database administrator, I want to run upgrade validation checks before a major version upgrade, so that I can identify and resolve blocking issues in advance.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
ai-usage: ai-assisted
ms.custom:
  - references_regions
  - build-2026
---

# Run upgrade validation checks (Preview) in Azure Database for PostgreSQL flexible server

This article describes how to run upgrade validation checks for Azure Database for PostgreSQL flexible server.

Upgrade validation checks help you identify compatibility problems and upgrade blockers before you start a major version upgrade. They validate upgrade readiness independently from the actual upgrade operation.

> [!NOTE]  
> Upgrade validation checks validate upgrade readiness only. They don't perform the actual major version upgrade.

## Prerequisites

Before running upgrade validation checks, review the supported upgrade paths and limitations documented in [Major version upgrades in Azure Database for PostgreSQL](concepts-major-version-upgrade.md).

## Steps to run upgrade validation checks

### [Portal](#tab/portal-major-version-upgrade-validation-checks)

Use the [Azure portal](https://portal.azure.com/):

1. From the resource menu, select **Overview**.

1. The server status must be **Ready** for the **Upgrade** button to be enabled.

   :::image type="content" source="media/how-to-run-upgrade-validation-checks/server-status.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server." lightbox="media/how-to-run-upgrade-validation-checks/server-status.png":::

1. Select **Upgrade**.

   :::image type="content" source="media/how-to-run-upgrade-validation-checks/upgrade-button.png" alt-text="Screenshot showing the Upgrade button through which you can initiate the major version upgrade of an Azure Database for PostgreSQL flexible server." lightbox="media/how-to-run-upgrade-validation-checks/upgrade-button.png":::

1. Expand **PostgreSQL version to upgrade**, and select the major version for which you want to validate the upgrade.

   :::image type="content" source="media/how-to-run-upgrade-validation-checks/set-postgresql-version.png" alt-text="Screenshot showing the Upgrade pane, from where you can select the major version to which you want to upgrade." lightbox="media/how-to-run-upgrade-validation-checks/set-postgresql-version.png"::: 

1. For **Action**, select **Validate and upgrade** to run the validation rules and, if they all pass, it immediately upgrades the server to the selected target version. It warns you about the consequences of initiating the upgrade.

   :::image type="content" source="media/how-to-run-upgrade-validation-checks/action.png" alt-text="Screenshot showing the Action option configured as Validate only." lightbox="media/how-to-run-upgrade-validation-checks/action.png"::: 

1. Select **Start**.

   :::image type="content" source="media/how-to-run-upgrade-validation-checks/start.png" alt-text="Screenshot showing the Start button, to initiate the upgrade." lightbox="media/how-to-run-upgrade-validation-checks/start.png"::: 

1. The validation process starts and performs upgrade readiness checks against the server.

1. Wait for the validation operation to complete. Keep the validation status pane open to monitor progress and review validation results.

1. After validation completes, if no blocking issues are detected, you can download the successful report as a CSV file or you can select the **Upgrade** button to proceed with the upgrade of the server to the selected target version.

     :::image type="content" source="media/how-to-run-upgrade-validation-checks/upgrade-validation-success.png" alt-text="Screenshot showing successful completion of upgrade validation checks." lightbox="media/how-to-run-upgrade-validation-checks/upgrade-validation-success.png":::

1. After validation completes, if blocking issues are detected, review the reported errors and fix them before retrying validation.

    :::image type="content" source="media/how-to-run-upgrade-validation-checks/upgrade-validation-failure.png" alt-text="Screenshot showing failed upgrade validation checks with remediation guidance for blocking issues." lightbox="media/how-to-run-upgrade-validation-checks/upgrade-validation-failure.png":::

### [CLI](#tab/cli-major-version-upgrade-validation-checks)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

---

## Review validation results

After the upgrade validation checks finish, review the validation findings to identify any upgrade blocking problems.

### Review validation findings in the portal

The validation results pane displays:
- Validation checks that succeeded
- Validation checks that failed
- Detailed descriptions and remediation guidance for failed checks

You can also download the validation results as a `.csv` file for offline review or sharing with your operations team.

:::image type="content" source="media/how-to-run-upgrade-validation-checks/upgrade-validation-csv-output.png" alt-text="Screenshot showing the Download .csv button for in the Pre-upgrade validation pane." lightbox="media/how-to-run-upgrade-validation-checks/upgrade-validation-csv-output.png":::

The downloaded report includes:
- Validation check name
- Validation result
- Error details
- Remediation recommendations for blocking problems

### Review detailed validation logs

Upgrade validation checks also generate upgrade validation logs that you can download from the **Server logs** page.

> [!NOTE]  
> To download validation logs, you must enable server logs on the server. For more information, see [Download PostgreSQL and upgrade logs](../monitor/how-to-configure-server-logs.md).

To access validation logs:

1. In the Azure portal, go to your Azure Database for PostgreSQL flexible server.

1. Select **Server logs** under the **Monitoring** section.

1. Locate the generated `pg_upgrade` log files.

1. Download the log files for detailed validation output and troubleshooting information.

## Related content

- [Major version upgrades in Azure Database for PostgreSQL](concepts-major-version-upgrade.md)
- [How to perform major version upgrade](how-to-perform-major-version-upgrade.md)
- [Download PostgreSQL and upgrade logs](../monitor/how-to-configure-server-logs.md)
