---
title: Common Error Messages
description: Learn how to resolve common Citus errors so you can maintain reliable distributed PostgreSQL applications.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
monikerRange: "citus-13 || citus-14"
---

# Common error messages

When working with Citus distributed databases, you might encounter error messages related to connections, transactions, constraints, and distributed operations. This reference guide provides explanations and resolutions for the most common errors encountered during development and production use. Understanding these errors helps you troubleshoot issues and build robust distributed applications.

## Couldn't receive query results

This error occurs when the coordinator node can't connect to a worker node.

```sql
SELECT 1 FROM companies WHERE id = 2928;
```

ERROR: connection to the remote node localhost:5432 failed with the following error: could not connect to server: Connection refused
            Is the server running on host "localhost" (127.0.0.1) and accepting
            TCP/IP connections on port 5432?

### Resolution

To fix this error, check that the worker node accepts connections and that Azure DNS resolves correctly.

## Canceling the transaction since it was involved in a distributed deadlock

Deadlocks can happen not only in a single-node database but also in a distributed database. Queries that execute across multiple nodes can cause deadlocks. Citus recognizes distributed deadlocks and defuses them by aborting one of the queries involved.

You can see this behavior by distributing rows across worker nodes and then running two concurrent transactions with conflicting updates:

```sql
CREATE TABLE lockme (id int, x int);
SELECT create_distributed_table('lockme', 'id');

-- id=1 goes to one worker, and id=2 another
INSERT INTO lockme VALUES (1,1), (2,2);

--------------- TX 1 ----------------  --------------- TX 2 ----------------
BEGIN;
                                       BEGIN;
UPDATE lockme SET x = 3 WHERE id = 1;
                                       UPDATE lockme SET x = 4 WHERE id = 2;
UPDATE lockme SET x = 3 WHERE id = 2;
                                       UPDATE lockme SET x = 4 WHERE id = 1;
```

ERROR: canceling the transaction since it was involved in a distributed deadlock

### Resolution

Detecting deadlocks and stopping them is part of normal distributed transaction handling. It allows an application to retry queries or take another course of action.

## Couldn't connect to server: Can't assign requested address

```sql
WARNING: connection error: localhost:9703
DETAIL: could not connect to server: Cannot assign requested address
```
This error occurs when there are no more sockets available by which the coordinator can respond to worker requests.

### Resolution

Configure the operating system to reuse TCP sockets. Execute this resolution on the shell in the coordinator node:

```bash
sysctl -w net.ipv4.tcp_tw_reuse=1
```

This resolution allows reusing sockets in TIME_WAIT state for new connections when it's safe from a protocol viewpoint. Default value is 0 (disabled).

## SSL error: certificate verify failed

As of Citus 8.1, nodes are required to talk to one another by using SSL by default. If SSL isn't enabled on a PostgreSQL server when Citus is first installed, the install process enables it. This enabling includes creating and self-signing an SSL certificate.

However, if a root certificate authority file exists (typically in `~/.postgresql/root.crt`), then the certificate is checked unsuccessfully against that CA at connection time. The PostgreSQL documentation about [SSL support](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBQ-SSL-CERTIFICATES) warns:

> For backward compatibility with earlier versions of PostgreSQL, if a root CA file exists, the behavior of sslmode=require will be the same as that of verify-ca, meaning the server certificate is validated against the CA. Relying on this behavior is discouraged, and applications that need certificate validation should always use verify-ca or verify-full.

### Resolution

Possible solutions are to sign the certificate, turn off SSL, or remove the root certificate. Also a node might have trouble connecting to itself without the help of `local_hostname`.

## Couldn't connect to any active placements

When all available worker connection slots are in use, further connections fail.

```sql
WARNING: connection error: hostname:5432
ERROR: could not connect to any active placements
```

### Resolution

This error happens most often when copying data into Citus in parallel. The COPY command opens up one connection per shard. Running M concurrent copies into a destination with N shards results in M\*N connections. To solve the error, reduce the shard count of target distributed tables, or run fewer `\copy` commands in parallel.

## Remaining connection slots are reserved for nonreplication superuser connections

This error occurs when PostgreSQL runs out of available connections to serve concurrent client requests.

### Resolution

The [max_connections](https://www.postgresql.org/docs/current/static/runtime-config-connection.html#GUC-MAX-CONNECTIONS) GUC adjusts the limit, with a typical default of 100 connections. Each connection consumes resources, so adjust sensibly. When increasing `max_connections`, you should increase [memory limits](https://www.postgresql.org/docs/current/static/runtime-config-resource.html#RUNTIME-CONFIG-RESOURCE-MEMORY) too.

[PgBouncer](https://pgbouncer.github.io/) can also help by queuing connection requests that exceed the connection limit. (Our `cloud_topic` has a built-in PgBouncer instance.)

## PgBouncer can't connect to server

In a self-hosted Citus cluster, this error indicates that the coordinator node isn't responding to PgBouncer.

### Resolution

To ensure the server is running and accepting connections, try connecting directly to the server with psql.

## Relation *foo* isn't distributed

This error no longer occurs in the current version of Citus. It was caused by attempting to join local and distributed tables in the same query.

### Resolution

Upgrade to Citus 10.0 or higher.

## Unsupported clause type

This error no longer occurs in the current version of Citus. It used to happen when executing a join with an inequality condition:

```sql
SELECT *
 FROM identified_event ie
 JOIN field_calculator_watermark w ON ie.org_id = w.org_id
WHERE w.org_id = 42
  AND ie.version > w.version
LIMIT 10;
```

ERROR: unsupported clause type

### Resolution

Upgrade to Citus 7.2 or higher.

## Can't open new connections after the first modification command within a transaction

This error no longer occurs in the current version of Citus except in certain unusual shard repair scenarios. It used to happen when updating rows in a transaction and then running another command, which would open new coordinator-to-worker connections.

```sql
BEGIN;
-- run modification command that uses one connection
DELETE FROM http_request
 WHERE site_id = 8
   AND ingest_time < now() - '1 week'::interval;

-- now run a query that opens connections to more workers
SELECT count(*) FROM http_request;
```

```sql
ERROR: cannot open new connections after the first modification command within a transaction
```

### Resolution

Upgrade to Citus 7.2 or higher.

## Can't create uniqueness constraint

As a distributed system, Citus can guarantee uniqueness only if a unique index or primary key constraint includes a table's distribution column. The shards are split so that each shard contains nonoverlapping partition column values. The index on each worker node can locally enforce its part of the constraint.

Trying to make a unique index on a nondistribution column generates an error:

```sql
ERROR: creating unique indexes on non-partition columns is currently unsupported
```

Enforcing uniqueness on a nondistribution column would require Citus to check every shard on every INSERT to validate, which defeats the goal of scalability.

### Resolution

There are two ways to enforce uniqueness on a nondistribution column:

- Create a composite unique index or primary key that includes the desired column (*C*), but also includes the distribution column (*D*). This resolution isn't quite as strong a condition as uniqueness on *C* alone, but it ensures that the values of *C* are unique for each value of *D*. For instance if distributing by `company_id` in a multitenant system, this approach would make *C* unique within each company.
- Use a reference table rather than a hash distributed table. This resolution is only suitable for small tables, since the contents of the reference table are duplicated on all nodes.

## Function create_distributed_table doesn't exist

```sql
SELECT create_distributed_table('foo', 'id');
/*
ERROR:  function create_distributed_table(unknown, unknown) does not exist
LINE 1: SELECT create_distributed_table('foo', 'id');
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
*/
```

### Resolution

When basic `user_defined_functions` aren't available, check whether the Citus extension is properly installed. Running `\dx` in psql lists installed extensions.

One way to end up without extensions is by creating a new database in a PostgreSQL server, which requires extensions to be reinstalled. See `create_db` to learn how to do it right.

## STABLE functions used in UPDATE queries can't be called with column references

Each PostgreSQL function is marked with a [volatility](https://www.postgresql.org/docs/current/static/xfunc-volatility.html), which indicates whether the function can update the database, and whether the function's return value can vary over time given the same inputs. A `STABLE` function is guaranteed to return the same results given the same arguments for all rows within a single statement, while an `IMMUTABLE` function is guaranteed to return the same results given the same arguments forever.

Nonimmutable functions can be inconvenient in distributed systems because they can introduce subtle changes when run at slightly different times across shards. Differences in database configuration across nodes can also interact harmfully with nonimmutable functions.

One of the most common ways this issue occurs is by using the `timestamp` type in PostgreSQL, which unlike `timestamptz` doesn't keep a record of time zone. Interpreting a timestamp column makes reference to the database timezone, which can be changed between queries, hence functions operating on timestamps aren't immutable.

Citus doesn't allow distributed queries that filter results by using stable functions on columns. For instance:

```sql
-- foo_timestamp is timestamp, not timestamptz
UPDATE foo SET ... WHERE foo_timestamp < now();
```

```sql
ERROR: STABLE functions used in UPDATE queries cannot be called with column references
```

In this case, the comparison operator `<` between timestamp and timestamp isn't immutable.

### Resolution

Avoid stable functions on columns in a distributed UPDATE statement. In particular, whenever working with times use `timestamptz` rather than `timestamp`. Having a time zone in timestamp makes calculations immutable.

## Related content

- [Diagnostic queries](diagnostic-queries.md)
- [FAQ](faq-citus.yml)
- [What is Citus?](what-is-citus.md)
