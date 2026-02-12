---
title: Triggers on Distributed Tables
description: Learn how to use triggers on Citus distributed tables so you can automate row-level data operations.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
monikerRange: "citus-13 || citus-14"
---

# Triggers on distributed tables

Citus doesn't support creating triggers on distributed tables. As a workaround you can manually create triggers on table shards directly on the worker nodes.

> [!NOTE]  
> Triggers created with these workarounds won't automatically apply to shard copies created by future shard rebalancing. The workarounds will have to be reapplied after rebalancing.

**Trigger against just one distributed table.**

Suppose that for each row in a table we wish to record the user who last updated it. We could add an `author` column to store who it was, and rather than make a default value for the column we could use a trigger. This action prevents a user from overriding the record.

```sql
CREATE TABLE events (
  id bigserial PRIMARY KEY,
  description text NOT NULL,
  author name NOT NULL
);
SELECT create_distributed_table('events', 'id');
```

However, this is a distributed table, so a single trigger on the coordinator for the table doesn't work. We need to create a trigger for each of the table placements.

```sql
-- First create a function that all these triggers will use.

CREATE OR REPLACE FUNCTION set_author() RETURNS TRIGGER AS $$
  BEGIN
    NEW.author := current_user;
    RETURN NEW;
  END;
$$ LANGUAGE plpgsql;

-- Now create a trigger for every placement

SELECT run_command_on_shards(
  'events',
  $cmd$
    CREATE TRIGGER events_set_author BEFORE INSERT OR UPDATE ON %s
      FOR EACH ROW EXECUTE PROCEDURE set_author()
  $cmd$
);
```

Now if we try to add fake data, the author column will at least reveal who made the change:

```sql
INSERT INTO events (description,author) VALUES ('a bad thing', 'wasnt-me');

TABLE events;
```

┌────┬─────────────┬────────┐
│ id │ description │ author │
├────┼─────────────┼────────┤
│ 1 │ a bad thing │ citus │
└────┴─────────────┴────────┘

The author says "Citus" rather than "wasnt-me," showing this column can't be spoofed.

**Trigger between colocated tables.**

When two distributed tables are colocated, then we can create a trigger to modify one based on changes in the other. The idea, once again, is to create triggers on the placements, but the trigger must be between pairs of placements that are themselves colocated. Citus has a special helper function `run_command_on_colocated_placements`, which addresses this situation.

Suppose that for every value inserted into `little_vals` we want to insert one twice as large into `big_vals`.

```sql
CREATE TABLE little_vals (key int, val int);
CREATE TABLE big_vals    (key int, val int);
SELECT create_distributed_table('little_vals', 'key');
SELECT create_distributed_table('big_vals',    'key');

-- This trigger function takes the destination placement as an argument

CREATE OR REPLACE FUNCTION embiggen() RETURNS TRIGGER AS $$
  BEGIN
    IF (TG_OP = 'INSERT') THEN
      EXECUTE format(
        'INSERT INTO %s (key, val) SELECT ($1).key, ($1).val*2;',
        TG_ARGV[0]
      ) USING NEW;
    END IF;
    RETURN NULL;
  END;
$$ LANGUAGE plpgsql;

-- Next we relate the co-located tables by the trigger function
-- on each co-located placement

SELECT run_command_on_colocated_placements(
  'little_vals',
  'big_vals',
  $cmd$
    CREATE TRIGGER after_insert AFTER INSERT ON %s
      FOR EACH ROW EXECUTE PROCEDURE embiggen(%L)
  $cmd$
);
```

Then to test it:

```sql
INSERT INTO little_vals VALUES (1, 42), (2, 101);
TABLE big_vals;
```

┌─────┬─────┐
│ key │ val │
├─────┼─────┤
│   1 │ 84 │
│   2 │ 202 │
└─────┴─────┘

**Trigger between reference tables.**

> [!NOTE]  
> **This workaround is only safe in limited situations.** When using such a trigger to insert into a reference table, make sure that no concurrent updates happen on the destination table. The order in which concurrent update/delete/insert commands apply to replicas isn't guaranteed, and replicas of the reference table can get out of sync with one another. All data modification to the destination table should happen via the trigger only.

Reference tables are simpler than distributed tables in that they have exactly one shard that is replicated across all workers. To relate reference tables with a trigger, we can create a trigger for the shard on all workers.

Suppose we want to record the author of every change in `insert_target` to `audit_table`, both of which are reference tables. As long as only our trigger updates the `audit_table`, this structure is safe.

```sql
-- create the reference tables

CREATE TABLE insert_target (
  value text
);
CREATE TABLE audit_table(
  author name NOT NULL,
  value text
);
SELECT create_reference_table('insert_target');
SELECT create_reference_table('audit_table');
```

To make a trigger on each worker that updates `audit_table`, we need to know the name of that table's shard. Rather than looking up the name in the metadata tables and using it manually in `run_command_on_workers`, we can use `run_command_on_shards`. Reference tables have exactly one placement per worker node, so the following creates what we want.

```sql
SELECT run_command_on_shards(
  'audit_table',
  $cmd$
    CREATE OR REPLACE FUNCTION process_audit() RETURNS TRIGGER AS $$
      BEGIN
        INSERT INTO %s (author,value)
          VALUES (current_user,NEW.value);
        RETURN NEW;
      END;
    $$ LANGUAGE plpgsql;
  $cmd$
);

SELECT run_command_on_shards(
  'insert_target',
  $cmd$
    CREATE TRIGGER emp_audit
    AFTER INSERT OR UPDATE ON %s
      FOR EACH ROW EXECUTE PROCEDURE process_audit();
  $cmd$
);

INSERT INTO insert_target (value) VALUES ('inserted value');

TABLE audit_table;
```

┌────────┬────────────────┐
│ author │     value      │
├────────┼────────────────┤
│ citus │ inserted value │
└────────┴────────────────┘

This table shows that the trigger executed and added a row including the `author` column.

**Trigger from distributed to reference table.**

This action isn't possible.

## Related content

- [DDL commands](reference-ddl.md)
- [What is Citus?](what-is-citus.md)
