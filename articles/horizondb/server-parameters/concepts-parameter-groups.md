---
title: Parameter Groups
description: Learn about the parameter groups in Azure HorizonDB.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: concept-article
---

# Parameter groups in Azure HorizonDB

Parameter groups in HorizonDB act as containers for cluster configuration values that can be applied to one or more database clusters. Instead of managing configuration settings for each cluster individually, you can define them in a parameter group and connect that group with multiple clusters to ensure consistency across your environment.

Parameter groups are first-class resources in Azure and are surfaced within the specific resource group and subscription defined in their resource identifier.

## Key Concepts

- **Engine versioning**: Parameter groups are specific to a PostgreSQL engine version (for example, 17).
- **Default parameter inheritance**: When creating a group, you only need to specify a subset of parameters. Any parameters not explicitly provided are automatically seeded and merged from the system default parameter group for the target engine version.
- **Default parameter group identifier**: Every HorizonDB cluster is assigned a system-managed default parameter group upon creation. The resource identifier for this group follows the convention:
  `/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/parameterGroups/default_pg{pgVersion}`
  *(for example, `default_pg17` for PostgreSQL version 17)*
<!-- **Versioning**: Each update to a parameter group creates a new, immutable version of the data. This allows you to track configuration history and audit changes over time. **Currently, parameter groups don't support updates.**-->
- **Immediate vs. deferred application**: Some parameters (static) require a server restart to take effect, while others (dynamic) can be applied immediately.
  - **Dynamic parameters**: Modified values are applied to active clusters immediately without requiring a restart.
  - **Static parameters**: Modified values are stored in the cluster's configuration but remain "pending" until the next server restart.
  - **Apply status**: The `applyImmediately` flag (default: `false`) determines whether the system should force a restart of clusters connected to the parameter group to apply static changes immediately.
- **Read-only parameters**: Certain parameters are marked as read-only by the system for security or stability reasons.
  - **Modification forbidden**: Any attempt to include a read-only parameter in a request results in a validation error.
  - **Default values**: These read-only parameters still apply to your clusters, but always use the values defined in the system's default parameter group for the target engine version.
- **Resource uniqueness**: Parameter group names must be unique within their resource group and subscription.
- **Connections**: Parameter groups can be connected (linked or associated) with one or more **clusters**. One parameter group created in one region can't be connected to one cluster created on a different region. Connections are managed via an internal mapping system that tracks:
  - **Sync status**: Whether the cluster configuration matches the parameter group version.
<!--  - **Last applied version**: The specific data version currently running on the cluster.-->
- **Scenario: Multi-cluster connection and deferred application**:
  - Suppose **cluster A** and **cluster B** are both connected with **parameter group X**.
  - If a **static parameter** (for example, `max_connections`) is updated in parameter group X and `applyImmediately` is set to `false`:
    1. The update creates a new data version for parameter group X.
    1. The backend updates the mapping for both cluster A and cluster B to the new version in "Pending" sync status.
    1. If **cluster A** is manually restarted (or restarted due to maintenance), it picks up the new static value and its status transitions to `InSync`.
    1. **cluster B**, if not restarted, it continues to run with the _previous_ value of the static parameter, even though its target configuration in the backend points to the new version. It remains in a "Pending Restart" or "Out of Sync" state until a restart occurs.

## Best practices

- **Naming conventions**: Preferably, embed some form of encoded description in the name so that you can later identify the potential target clusters of that configuration.
<!--1. **Version tracking**: Use the `/versions` API to audit who and when changed what configuration.-->
- **Staging**: Always test new parameter groups on a development cluster before applying them to production, especially when setting `applyImmediately` to `true`.
<!--
## Resource model

### HorizonDbParameterGroup

| Property | Type | Description |
| --- | --- | --- |
| `name` | string | The unique name of the parameter group. |
| `location` | string | The Azure region where the resource resides. |
| `properties.pgVersion` | integer | The PostgreSQL engine version (for example, 17). |
| `properties.description` | string | A user-defined description of the group. |
| `properties.parameters` | array | A list of parameter objects (Name, Value, etc.). |
| `properties.applyImmediately` | boolean | If true, applies changes immediately (might trigger restart). |
-->

## Related content

- [Create parameter groups](how-to-parameter-groups-create.md)
- [Update parameter groups](how-to-parameter-groups-update.md)
- [Delete parameter groups](how-to-parameter-groups-delete.md)
- [List parameter groups](how-to-parameter-groups-list.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
- [Identity parameter group connected to a cluster](how-to-parameter-groups-identify-connected-cluster.md)
