---
title: Adaptive Autovacuum in Azure Database for PostgreSQL Flexible Server
description: This article describes the adaptive autovacuum feature in Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to understand how adaptive autovacuum works in Azure Database for PostgreSQL flexible server, so that I can decide whether to enable it for my workloads.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: concept-article
---

# Adaptive autovacuum in Azure Database for PostgreSQL flexible server

This article documents the `adaptive_autovacuum` parameters supported by Azure Database for PostgreSQL flexible server:

- `adaptive_autovacuum.optimize_configurations`: Enables automatic tuning of a series of autovacuum settings.
- `adaptive_autovacuum.open_transaction_threshold`: Sets the age threshold in seconds to detect and mitigate old prepared transactions.

## How each parameter works

### adaptive_autovacuum.optimize_configurations

When you set this parameter to `on`, the tuning service periodically:

1. Collects and aggregates workload and table-statistics signals.
1. Evaluates rule workflows.
1. Computes candidate autovacuum parameter updates.
1. Applies updates and reloads engine configuration.
1. Writes audit entries.

If no rule conditions are met, a run can complete with no changes.

Current tunable parameters:

- `autovacuum_vacuum_cost_limit`
- `autovacuum_vacuum_threshold`
- `autovacuum_vacuum_scale_factor`
- `autovacuum_vacuum_cost_delay`
- `autovacuum_analyze_scale_factor`

> [!NOTE]
> - If you set `autovacuum_vacuum_cost_limit` to -1, the logic derives from `vacuum_cost_limit`.
> - The tuning service uses `autovacuum_freeze_max_age` as an input signal but doesn't directly tune it.

### Visibility and override behavior for tuned parameters

When this feature changes any of the five target parameters (`autovacuum_vacuum_cost_limit`, `autovacuum_vacuum_threshold`, `autovacuum_vacuum_scale_factor`, `autovacuum_vacuum_cost_delay`, `autovacuum_analyze_scale_factor`):

- The control plane Configurations endpoint (for example, GET Configurations API or `az postgres flexible-server parameter` CLI command group) doesn't show these effective runtime changes.
- To see the effective values, use data-plane queries against the PostgreSQL endpoint (for example, `SHOW <guc_name>` or `SELECT name, setting FROM pg_settings WHERE name IN (...)`).

User override semantics:

- You can set any of these five parameters directly through the portal, REST API, CLI, or any of the supported SDKs.
- If you set a parameter to the same value that the control plane Configurations endpoint currently returns, the operation is treated as a no-op and no new effective change is applied.
- User-set values override the feature-applied values at the time they're applied.
- If `adaptive_autovacuum.optimize_configurations` remains enabled, later tuning iterations can apply new values again based on rule evaluation.

### adaptive_autovacuum.open_transaction_threshold

This parameter controls orphan prepared-transaction mitigation:

- 0 means disabled.
- Greater than 0 means enabled with threshold in seconds.

When enabled, if the oldest prepared transaction exceeds the threshold, the orphan-transaction handler evaluates eligibility and can roll back old prepared transactions. The handler updates its in-memory threshold on parameter changes, so behavior follows the latest value.

Important timing detail:

- The feature first determines the oldest prepared transaction timestamp.
- That detection is poll-based, not continuous.
- The poll runs every 1,800 seconds (that is, every 30 minutes), so mitigation can only start after a poll observes an old-enough prepared transaction.

## Runtime and scheduling behavior

- The `optimize_configurations` tuning cadence is every 30 minutes.
- When you turn on `optimize_configurations`, it triggers an immediate tuning run, and then scheduled runs continue.
- The handling of `open_transaction_threshold` is event-driven from prepared-transaction observations. Mitigation runs only when age checks exceed the threshold.
- The prepared-transaction observation for `open_transaction_threshold` refreshes every 300 seconds.

### When is the `intelligentperformance` schema created after enabling?

The `intelligentperformance` schema is created under the `azure_sys` database. Its creation isn't immediate and is handled by the functionality that persists statistics used by adaptive autovacuum, rather than by the initial tuning run itself. Typically, the schema is created within 0–30 minutes after enabling the feature.

You can enable adaptive autovacuum by setting `adaptive_autovacuum.optimize_configurations` to `on` or by configuring `adaptive_autovacuum.open_transaction_threshold` to a non-zero value (that is > 0). The schema is created once the feature becomes active and begins collecting the required statistics.

Creation might be delayed or skipped if certain prerequisites aren't met.

## Limitations and prerequisites

Both controls are subject to the following requirements:

- The instance must be a primary.
- PostgreSQL isn't in recovery mode.
- The compute of the server has a minimum of 4 vCores.
- The server is a regular flexible server, not an elastic cluster. The feature isn't supported on elastic clusters.
- `adaptive_autovacuum.optimize_configurations` is supported on major versions greater than or equal to 14.
- `adaptive_autovacuum.open_transaction_threshold` is supported on major versions greater than or equal to 13.
- The adaptive autovacuum feature is currently supported on servers deployed in the following regions: Australia Central, Australia Central 2, Australia East, Australia Southeast, Austria East, Belgium Central, Brazil South, Brazil Southeast, Canada Central, Canada East, Chile Central, Denmark East, East Asia, East US, East US 2, France Central, France South, Germany North, Germany West Central, India Central, India South, India West, Indonesia Central, Israel Central, Israel Northwest, Italy North, Japan East, Japan West, Jio India Central, Jio India West, Korea Central, Korea South, Malaysia West, Mexico Central, New Zealand North, North Central US, Norway East, Norway West, Poland Central, Qatar Central, South Africa North, South Africa West, South Central US, Southeast Asia, Spain Central, Sweden Central, Sweden South, Switzerland North, Switzerland West, Taiwan North, UAE Central,  UAE North, UK South, UK West, West Central US, West Europe, West US, and West US 2.

## Auditing and observability

The system records actions from both controls in an audit view named `intelligentperformance.adaptive_tuning_events`.

### Schema of the view

Expected logical shape:

- intelligentperformance.adaptive_tuning_events
  - event_details
  - optimizer_type
  - applied_at

### Query for recent activity

To query recent activity, use the following queries:

```sql
SELECT
    applied_at,
    optimizer_type,
    event_details
FROM intelligentperformance.adaptive_tuning_events
ORDER BY applied_at DESC
LIMIT 100;
```

```sql
SELECT
    optimizer_type,
    COUNT(*) AS events
FROM intelligentperformance.adaptive_tuning_events
WHERE applied_at >= now() - interval '7 days'
GROUP BY optimizer_type
ORDER BY events DESC;
```

### Event types and interpretation

The `optimizer_type` column indicates the action source.

#### adaptive_autovacuum_configuration_changed

Source:

- `optimize_configurations` tuning path.

Payload shape:

- JSON array of parameter-change records, typically including:
  - server_parameter_name
  - previous_value
  - updated_tuned_value

Interpretation:

- Indicates autovacuum tuning changed server settings.
- Positive when subsequent workload metrics improve (dead tuple pressure, vacuum cadence, latency, CPU/IO).
- Potentially negative when changes are frequent and oscillatory and are followed by regressions.

```sql
SELECT
    applied_at,
    elem->>'server_parameter_name' AS parameter_name,
    elem->>'previous_value' AS previous_value,
    elem->>'updated_tuned_value' AS updated_value
FROM intelligentperformance.adaptive_tuning_events e
CROSS JOIN LATERAL jsonb_array_elements(e.event_details) AS elem
WHERE e.optimizer_type = 'adaptive_autovacuum_configuration_changed'
ORDER BY applied_at DESC;
```

#### orphan_transaction_rollback

Source:

- `open_transaction_threshold` mitigation path.

Payload shape:

- JSON object keyed by database, with rollback outcome details (for example attempted and successful GID rollback info).

```json
{
    "<example-database-name>": {
        "Timestamp": "2026-03-22T18:20:22.0000000Z", 
        "RollbackGids": ["<example-global-identifier-one>", "<example-global-identifier-two>"], 
        "OperationSuccessful": true
    }
}
```

    
Interpretation:

- Indicates prepared transactions were force-rolled back after crossing threshold.
- Occasional events can be healthy protective behavior.
- Frequent events usually indicate application transaction-lifecycle issues that should be investigated.

```sql
SELECT
    applied_at,
    jsonb_pretty(event_details) AS rollback_details
FROM intelligentperformance.adaptive_tuning_events
WHERE optimizer_type = 'orphan_transaction_rollback'
ORDER BY applied_at DESC
LIMIT 50;
```

### Determine whether impact is positive or negative

For `optimize_configurations`:

1. Identify change timestamps from `adaptive_autovacuum_configuration_changed`.
1. Compare 30 to 120-minute post-change windows for dead tuples, vacuum/analyze cadence, latency, CPU/IO.

For `open_transaction_threshold`:

1. Identify `orphan_transaction_rollback` events.
1. Validate whether rollback frequency is low and stabilizing.
1. Investigate application behavior if rollback events are persistent.

```sql
SELECT
    applied_at,
    optimizer_type,
    event_details
FROM intelligentperformance.adaptive_tuning_events
WHERE applied_at >= now() - interval '7 days'
ORDER BY applied_at DESC;
```

### Retention and housekeeping

Housekeeping removes older records from audit storage using a fixed and nonconfigurable retention window of 90 days.

For longer-term trend analysis, export audit rows to your own observability store.

## Related content

- [Intelligent tuning](./concepts-intelligent-tuning.md).
