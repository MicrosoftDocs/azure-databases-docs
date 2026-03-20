---
title: Small Database Migration
description: This article describes the steps needed to migrate a small PostgreSQL database to a Citus cluster on Microsoft Azure.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
monikerRange: "citus-13 || citus-14"
---

# Small database migration

For smaller environments that can tolerate a little downtime, use a straightforward pg_dump/pg_restore process. Here are the steps.

1. Save the database structure from your development database:

   ```bash
   pg_dump \
      --format=plain \
      --no-owner \
      --schema-only \
      --file=schema.sql \
      --schema=target_schema \
      postgres://user:pass@host:5432/db
   ```

1. Connect to the Citus cluster using psql and create the schema:

   ``` psql
   \i schema.sql
   ```

1. Run your `create_distributed_table` and `create_reference_table` statements. If you get an error about foreign keys, it's typically due to the order of operations. Drop foreign keys before distributing tables and then readd them.

1. Put the application into maintenance mode, and disable any other writes to the old database.

1. Save the data from the original production database to disk with `pg_dump`:

   ```bash
   pg_dump \
      --format=custom \
      --no-owner \
      --data-only \
      --file=data.dump \
      --schema=target_schema \
      postgres://user:pass@host:5432/db
   ```

1. Import into Citus using `pg_restore`:

   ```bash
   # remember to use connection details for Citus,
   # not the source database
   pg_restore  \
      --host=host \
      --dbname=dbname \
      --username=username \
      data.dump

   # it'll prompt you for the connection password
   ```

1. Test application.

1. Launch!

## Related content

- [Data migration](migration-data.md)
- [Large data migration with replication](migration-data-big.md)
- [Migration overview](migrating.md)
