---
title: Upgrade Validation Checks
description: This article describes how to run Upgrade Validation Checks for Azure Database for PostgreSQL flexible server before performing a major version upgrade.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 06/07/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
ms.custom:
  - references_regions
  - build-2026
---

# Run upgrade validation checks (Preview)

This article describes how to run Upgrade Validation Checks for Azure Database for PostgreSQL flexible server.

Upgrade Validation Checks help identify compatibility issues and upgrade blockers before starting a major version upgrade by validating upgrade readiness independently from the actual upgrade operation.

> [!NOTE]  
> Upgrade Validation Checks validate upgrade readiness only. They don't perform the actual major version upgrade.

## Prerequisites

Before running Upgrade Validation Checks:

- Ensure the server is in the **Ready** state.
- Ensure the target PostgreSQL major version is supported by Azure Database for PostgreSQL flexible server.
- Review the supported upgrade paths and limitations documented in [Major version upgrades in Azure Database for PostgreSQL](concepts-major-version-upgrade.md).

## Run upgrade validation checks

Using the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server instance that you want to validate.

1. From the resource menu, select **Overview**.

1. Select **Upgrade**.

1. In the **Upgrade** pane, select the target PostgreSQL version.

1. Select **Validate Only**.

:::image type="content" source="media/how-to-run-upgrade-validation-checks/upgrade-validation-validate-only.png" alt-text="Screenshot showing the Upgrade pane with the Validate Only option selected for running Upgrade Validation Checks." lightbox="media/how-to-run-upgrade-validation-checks/upgrade-validation-validate-only.png":::

1. The validation process starts and performs upgrade readiness checks against the server.

1. Wait for the validation operation to complete. Keep the validation status pane open to monitor progress and review validation results.

1. After validation completes:

   - If no blocking issues are detected, validation completes successfully.

     :::image type="content" source="media/how-to-run-upgrade-validation-checks/upgrade-validation-success.png" alt-text="Screenshot showing successful completion of Upgrade Validation Checks." lightbox="media/how-to-run-upgrade-validation-checks/upgrade-validation-success.png":::

   - If blocking issues are detected, review the reported errors and remediate them before retrying validation.

:::image type="content" source="media/how-to-run-upgrade-validation-checks/upgrade-validation-failure.png" alt-text="Screenshot showing failed Upgrade Validation Checks with remediation guidance for blocking issues." lightbox="media/how-to-run-upgrade-validation-checks/upgrade-validation-failure.png":::

1. Select **Operation details** to review validation progress and results.

Validation checks don't restart the server or initiate the major version upgrade process.

## Review validation results

After Upgrade Validation Checks complete, review the validation findings to identify any upgrade blocking issues.

### Review validation findings in the portal

The validation results pane displays:
- Validation checks that succeeded
- Validation checks that failed
- Detailed descriptions and remediation guidance for failed checks

You can also download the validation results as a `.csv` file for offline review or sharing with your operations team.

:::image type="content" source="media/how-to-run-upgrade-validation-checks/upgrade-validation-csv-output.png" alt-text="Screenshot showing the CSV download option for Upgrade Validation Checks results." lightbox="media/how-to-run-upgrade-validation-checks/upgrade-validation-csv-output.png":::

The downloaded report includes:
- Validation check name
- Validation result
- Error details
- Remediation recommendations for blocking issues

### Review detailed validation logs

Upgrade Validation Checks also generate upgrade validation logs that can be downloaded from the **Server logs** page.

> [!NOTE]  
> To download validation logs, Server Logs must be enabled on the server. For more information, see [Download PostgreSQL and upgrade logs](../monitor/how-to-configure-server-logs.md).

To access validation logs:

1. In the Azure portal, go to your Azure Database for PostgreSQL flexible server instance.

1. Select **Server logs** under the **Monitoring** section.

1. Locate the generated `pg_upgrade` log files.

1. Download the log files for detailed validation output and troubleshooting information.

## Related content

- [Major version upgrades in Azure Database for PostgreSQL](concepts-major-version-upgrade.md)
- [How to perform major version upgrade](how-to-perform-major-version-upgrade.md)
- [Download PostgreSQL and upgrade logs](../monitor/how-to-configure-server-logs.md)
