---
title: Durable Functions in Azure HorizonDB
description: Use the pg_durable extension to define and run fault-tolerant, long-running workflows directly inside Azure HorizonDB, including retries, scheduling, signals, and HTTP calls, without external orchestrators.
author: abeomor
ms.author: abeomorogbe
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-horizondb
ms.subservice: development
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom: 
  - build-2026
ai-usage: ai-assisted
# customer intent: As a developer building long-running or scheduled workflows in Azure HorizonDB, I want to run them durably inside the database so that they survive crashes and don't require an external orchestrator.
---

# Durable functions with pg_durable for Azure HorizonDB (Preview)

`pg_durable` is the durable execution engine inside Azure HorizonDB. It lets you define long-running, multi-step SQL workflows (embedding pipelines, ETL jobs, AI calls, scheduled jobs, approval flows) and run them with the same reliability guarantees you'd expect from a dedicated orchestrator like [Durable Functions](/azure/azure-functions/durable-functions/durable-functions-overview), without leaving Postgres.

`pg_durable` is also the execution layer underneath [durable AI pipelines](../ai/ai-pipelines.md). If you're using AI pipelines, `pg_durable` is what makes them survive crashes, retry on failure, and resume from the last completed step.

> [!NOTE]  
> `pg_durable` is in **preview**.

## What "durable" means

A durable function in `pg_durable` is persisted to disk every step of the way. That gives you a specific set of guarantees you don't get from a plain `BEGIN ... COMMIT` block or a cron job:

- **Survives database crashes and restarts.** Completed steps aren't re-executed when the server comes back up. In-progress steps resume from the last checkpoint. Pending steps run when the worker comes back online.
- **Survives long waits.** A workflow can sleep for hours, wait for a cron schedule, or block on an external signal, and still pick up where it left off.
- **Survives failures.** Failed steps can be retried automatically without rerunning the whole function.
- **Captures identity.** A function executes with the privileges of the user who started it, not the privileges of the background worker. Multitenant workloads stay isolated.
- **Stays observable from SQL.** You can inspect status, history, execution count, and outputs through the same interface you use for everything else in HorizonDB: a `SELECT` statement.

What durability **doesn't** do automatically: it doesn't make nonidempotent external operations safe to retry on its own. If a step calls an external API that charges money, design the step to be idempotent (for example, by passing an idempotency key).

## When to use pg_durable

Use `pg_durable` when you have to work that:

- Takes long enough to fail in the middle (embedding generation across millions of rows, a multi-step ETL job, a backfill).
- Needs to be retried on failure without redoing the parts that already succeeded.
- Needs to run on a schedule (every hour, every weekday at 9 AM).
- Needs to wait for an external event (an approval, a webhook, a signal from another system).
- Coordinates multiple steps with branching, joining, or racing.
- Is currently implemented as an external orchestrator + a Postgres database, where most of the work is the database part.

If your workload is a single short transactional statement, you don't need `pg_durable`. Use a regular `INSERT` / `UPDATE`.

## How it works

A durable function is a graph of steps that you build with a SQL DSL and submit with `df.start()`. The graph is persisted, then a background worker executes it.

Two key ideas:

- **Function graph and execution state are stored in HorizonDB itself**, in the `df` and `duroxide` schemas. Backups, point-in-time restore, and high availability all apply to your workflow state automatically. No separate orchestrator state to manage.
- **The background worker is started by `shared_preload_libraries`.** It detects the extension after `CREATE EXTENSION` and begins executing functions. If the database restarts, the worker reattaches to running instances and resumes them.

> [!NOTE]  
> The execution engine inside `pg_durable` is built on [Duroxide](https://github.com/microsoft/duroxide), Microsoft's open-source durable execution runtime for Rust (inspired by the Durable Task Framework and Temporal). The `duroxide` schema name reflects this: that's where Duroxide persists orchestration history, correlation IDs, and replay state. The deterministic-replay, correlated-event-ID, and durable-timer guarantees you get from `pg_durable` come directly from Duroxide.

## Enable pg_durable

To enable `pg_durable` on Azure HorizonDB, first configure a parameter group, then create the extension in each database.

Use these setup articles:

- [Load shared libraries](../extensions/how-to-load-libraries.md)
- [Allow extensions](../extensions/how-to-allow-extensions.md)
- [Create extensions](../extensions/how-to-create-extensions.md)

1. Create a parameter group for your server.
2. Set `shared_preload_libraries` to include `pg_textsearch`.
3. Set `azure.extensions` to include `pg_textsearch`.
4. Apply the parameter group to the server.
5. Connect to each target database and run:

Create the extension in each database where you want to use it:

```sql
CREATE EXTENSION IF NOT EXISTS pg_durable;
```

`CREATE EXTENSION` provisions the `df` schema (function graphs and monitoring views) and the `duroxide` schema (execution state). The background worker detects the extension within a few seconds and is ready to run functions.

## Your first durable function

```sql
-- Start a one-step durable function
SELECT df.start('SELECT ''Hello, durable world!''');
-- Returns an 8-character instance ID, for example: a1b2c3d4

-- Check status
SELECT df.status('a1b2c3d4');

-- Get the result
SELECT df.result('a1b2c3d4');
```

Even a one-step function is durable: if the database restarts after `df.start()` and before the worker picks it up, the function still runs.

> [!NOTE]  
> `df.start()` submits a workflow asynchronously and returns immediately. For multi-step workflows, use `df.list_instances()`, `df.instance_info()`, `df.status()`, or `df.result()` to confirm completion before validating side effects.

## Program model

A durable function is a graph built from steps, operators, and built-in functions. Plain SQL strings are autowrapped, so you don't need to call `df.sql()` explicitly.

### Operators

| Operator | Meaning | Example |
| --- | --- | --- |
| `~>` | Sequence - run left, then right | `'SELECT 1' ~> 'SELECT 2'` |
| `&` | Join - run in parallel, wait for all | `'SELECT 1' & 'SELECT 2'` |
| `|` | Race - run in parallel, first wins | `fast_query | df.sleep(30)` |
| `?>` `!>` | If / else - branch on a boolean condition | `cond ?> then_branch !> else_branch` |
| `@>` | Loop - repeat forever (prefix operator) | `@> body` |
| `|=>` | Name - capture a step's result | `'SELECT id FROM users LIMIT 1' |=> 'user_id'` |

### Useful built-ins

| Function | Purpose |
| --- | --- |
| `df.sleep(seconds)` | Pause for N seconds. Durable across restarts. |
| `df.wait_for_schedule(cron)` | Wait until the next time a cron expression matches. |
| `df.wait_for_signal(name, timeout)` | Block until an external `df.signal()` arrives. |
| `df.http(url, method, body, headers, timeout)` | Make an HTTP call as a durable activity, with retry on transient failure. |
| `df.if(cond, then, else)` | Conditional branch. |
| `df.loop(body, cond)` | Repeat while a SQL condition is truthy. |
| `df.join(a, b)` / `df.race(a, b)` | Parallel and race execution. |
| `df.join3(a, b, c)` | For three-way parallel execution. |
| `df.start(body, label, database)` | Submit a durable function and return its instance ID. |
| `df.cancel(id, reason)` | Cancel a running instance. |
| `df.status(id)` / `df.result(id)` | Inspect outcome. |
| `df.explain(input)` | Render the function graph for visualization. |

Read more about all [pg_durable features](https://github.com/microsoft/pg_durable/blob/main/USER_GUIDE.md). 

### Variables

`|=>` captures a step's result with a name; later steps reference it as `$name`.

```sql
SELECT df.start(
    'SELECT 100 AS amount' |=> 'total'
    ~> 'SELECT $total * 2 AS doubled'
);
```

## Usage examples

### Multi-step ETL with retries

A daily ETL that cleans up, loads, indexes, and logs:

```sql
SELECT df.start(
    'DELETE FROM target WHERE loaded_at < now() - INTERVAL ''1 day'''
    ~> 'INSERT INTO target SELECT * FROM staging'
    ~> 'REINDEX TABLE target'
    ~> 'INSERT INTO etl_log (job, finished_at) VALUES (''nightly'', now())',
    'nightly-etl'
);
```

If the database restarts between the `DELETE` and the `INSERT`, the worker resumes from the `INSERT` - it doesn't rerun the `DELETE`.

### Scheduled job (cron)

Run a maintenance task every weekday at 9 AM:

```sql
SELECT df.start(
    @> (
        df.wait_for_schedule('0 9 * * 1-5')
        ~> 'CALL refresh_materialized_views()'
    ),
    'weekday-refresh'
);
```

If you want to stop this job, You can run the `cancel` function. 
```sql
SELECT df.cancel('a1b2c3d4', 'stop test cron job');
```

### Approval workflow with timeout

Wait up to 24 hours for an external approval signal, then commit or reject:

```sql
SELECT df.start(
    'SELECT order_id, total FROM orders WHERE id = 1' |=> 'order'
    ~> df.wait_for_signal('approval', 86400) |=> 'sig'
    ~> df.if(
        'SELECT NOT ($sig::jsonb->>''timed_out'')::boolean
            AND ($sig::jsonb->''data''->>''approved'')::boolean',
        'UPDATE orders SET status = ''approved'' WHERE id = $order_id',
        'UPDATE orders SET status = ''rejected'' WHERE id = $order_id'
    ),
    'order-approval'
);

-- Later, approve from anywhere
SELECT df.signal('a1b2c3d4', 'approval',
                 '{"approved": true, "approver": "jane@contoso.com"}');
```

### Durable HTTP call

`df.http()` makes external calls as durable activities - 5xx responses, network errors, and timeouts are retried automatically.

```sql
SELECT df.start(
    df.http('https://api.example.com/users/123', 'GET') |=> 'user'
    ~> 'INSERT INTO users_cache (data) VALUES (($user::jsonb->>''body'')::jsonb)',
    'fetch-user'
);
```
Read more about allowed [HTTP security in pg_durable](https://github.com/microsoft/pg_durable/blob/main/docs/http-security.md). 

## Observe and operate

Everything is queryable from SQL. There's no separate UI or service to learn.

```sql
-- All instances
SELECT * FROM df.list_instances();

-- Filter by status
SELECT * FROM df.list_instances() WHERE status = 'Running';
SELECT * FROM df.list_instances() WHERE status = 'Failed';

-- Detail for one instance
SELECT * FROM df.instance_info('a1b2c3d4');

-- Execution history (useful for retried or looped functions)
SELECT * FROM df.instance_executions('a1b2c3d4', 20);

-- The function graph as it ran
SELECT * FROM df.instance_nodes('a1b2c3d4');

-- System-wide metrics
SELECT * FROM df.metrics();
```

To check that the worker is alive:

```sql
SELECT epoch_id, last_seen_at, now() - last_seen_at AS time_since_last_heartbeat
FROM df._worker_epoch;
```

A `time_since_last_heartbeat` under 15 seconds means the worker is healthy. Anything larger, or no rows at all, means the worker is down or hasn't initialized.

## Identity and isolation

Durable functions execute with the privileges of the user who submitted them, not with the worker's privileges. `pg_durable` captures both `session_user` and `current_user` at submission time, so functions submitted under a `SET ROLE` context run with that effective role.

This means:

- Users only see and modify data they already have permissions to access.
- Non-superusers can't escalate privileges by submitting a durable function.
- Multitenant workloads stay isolated as long as your role and grant model is correct.

## Interaction with replicas, backup, and PITR

- **Backup and PITR.** Function graph (`df` schema) and execution state (`duroxide` schema) are stored in regular tables and are included in HorizonDB backups. A point-in-time restore restores both.
- **Read replicas.** The background worker only runs on the primary. Read replicas can query the `df.*` monitoring views but don't execute functions.
- **Failover.** After a failover, the worker on the new primary picks up where the old primary left off. Running instances resume from their last checkpoint.

## Compared to external orchestrators

| Aspect | External orchestrator | `pg_durable` |
| --- | --- | --- |
| Deployment | Separate service, separate identity, separate state store | One database |
| State durability | Orchestrator's storage layer | Same backups, HA, and PITR as your data |
| Identity | Workers run under a service identity | Functions execute as the submitting user |
| Failure modes | Network between orchestrator and database | None - same process |
| Best for | Cross-system orchestration that touches many services | Workloads where most of the work is in or near Postgres |

`pg_durable` isn't trying to replace external orchestrators for cross-system pipelines. It's the right choice when most of the work is database work - embeddings, transforms, AI calls, scheduled maintenance - and adding another service is more cost than benefit.

## Limitations during preview

- `df.http()` retries on 5xx and network errors. 4xx responses are returned to the workflow for you to handle; they aren't retried automatically.
- The background worker services a single database per instance. Multi-database fan-out is supported through `df.start(..., database => 'other_db')` from a function running in the worker's database.
- Function definitions and execution state aren't portable across major versions of `pg_durable` during **preview**. Drain or cancel running instances before upgrading.

## Related content

- [Implement durable AI pipelines in Azure HorizonDB (Preview)](../ai/ai-pipelines.md)
- [AI functions in the azure_ai extension for Azure HorizonDB (Preview)](../ai/ai-functions.md)
- [Generate vector embeddings using the create_embeddings() AI function (Preview)](../ai/generate-vector-embeddings.md)
- [Allow extensions in Azure HorizonDB (Preview)](../extensions/how-to-allow-extensions.md)
- [Duroxide on GitHub](https://github.com/microsoft/duroxide)
