---
title: Pre-upgrade Validation Checks
description: This article describes how to run Pre-Upgrade Validation Checks (PVC) for Azure Database for PostgreSQL flexible server before performing a major version upgrade.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
ms.custom:
  - references_regions
  - build-2026
---

# Run pre-upgrade validation checks (Preview)

This article describes how to run Pre-Upgrade Validation Checks (PVC) for Azure Database for PostgreSQL flexible server.

Pre-Upgrade Validation Checks (PVC) help identify compatibility issues and upgrade blockers before starting a major version upgrade by validating upgrade readiness independently from the actual upgrade operation.

> [!NOTE]
> Pre-Upgrade Validation Checks validate upgrade readiness only. They don't perform the actual major version upgrade.

## Prerequisites

Before running Pre-Upgrade Validation Checks:

- Ensure the server is in the **Ready** state.
- Ensure the target PostgreSQL major version is supported by Azure Database for PostgreSQL flexible server.
- Review the supported upgrade paths and limitations documented in [Major version upgrades in Azure Database for PostgreSQL flexible server](concepts-major-version-upgrade.md).

## Run pre-upgrade validation checks

Using the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server instance that you want to validate.

1. From the resource menu, select **Overview**.

1. Select **Upgrade**.

1. In the **Upgrade** pane, select the target PostgreSQL version.

1. Select **Validate Only**.

:::image type="content" source="media/how-to-run-upgrade-validation-checks/upgrade-validation-validate-only.png" alt-text="Screenshot showing the Upgrade pane with the Validate Only option selected for running Pre-Upgrade Validation Checks." lightbox="media/how-to-run-upgrade-validation-checks/upgrade-validation-validate-only.png":::

1. The validation process starts and performs upgrade readiness checks against the server.

7. Wait for the validation operation to complete. Keep the validation status pane open to monitor progress and review validation results.

1. After validation completes:
   - If no blocking issues are detected, validation completes successfully.

 :::image type="content" source="media/how-to-run-upgrade-validation-checks/upgrade-validation-success.png" alt-text="Screenshot showing successful completion of Pre-Upgrade Validation Checks." lightbox="media/how-to-run-upgrade-validation-checks/upgrade-validation-success.png":::

   - If blocking issues are detected, review the reported errors and remediate them before retrying validation.

:::image type="content" source="media/how-to-run-upgrade-validation-checks/upgrade-validation-failure.png" alt-text="Screenshot showing failed Pre-Upgrade Validation Checks with remediation guidance for blocking issues." lightbox="media/how-to-run-upgrade-validation-checks/upgrade-validation-failure.png":::

1. Select **Operation details** to review validation progress and results.

Validation checks don't restart the server or initiate the major version upgrade process.

## Review validation results

After Pre-Upgrade Validation Checks complete, review the validation findings to identify any upgrade blocking issues.

### Review validation findings in the portal

The validation results pane displays:
- Validation checks that succeeded
- Validation checks that failed
- Detailed descriptions and remediation guidance for failed checks

You can also download the validation results as a `.csv` file for offline review or sharing with your operations team.

:::image type="content" source="media/how-to-run-upgrade-validation-checks/upgrade-validation-csv-output.png" alt-text="Screenshot showing the CSV download option for Pre-Upgrade Validation Checks results." lightbox="media/how-to-run-upgrade-validation-checks/upgrade-validation-csv-output.png":::

The downloaded report includes:
- Validation check name
- Validation result
- Error details
- Remediation recommendations for blocking issues

### Review detailed validation logs

Pre-Upgrade Validation Checks also generate upgrade validation logs that can be downloaded from the **Server logs** page.

> [!NOTE]
> To download validation logs, Server Logs must be enabled on the server. For more information, see [Configure capture of PostgreSQL server logs and major version upgrade logs](../monitor/how-to-configure-server-logs.md).

To access validation logs:

1. In the Azure portal, go to your Azure Database for PostgreSQL flexible server instance.

1. Select **Server logs** under the **Monitoring** section.

1. Locate the generated `pg_upgrade` log files.

1. Download the log files for detailed validation output and troubleshooting information.

## Related content

- [Major version upgrade](concepts-major-version-upgrade.md)
