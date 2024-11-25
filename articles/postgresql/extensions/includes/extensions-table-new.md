---
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan, randolphwest
ms.date: 11/19/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
---

## List of extensions

Below is the list of extensions available.

### address_standardizer

[address_standardizer](http://postgis.net/docs/manual-2.5/Address_Standardizer.html) is used to parse an address into constituent elements. Generally used to support geocoding address normalization step.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 3.5.0 |
| PostgreSQL 16 | 3.3.3 |
| PostgreSQL 15 | 3.3.1 |
| PostgreSQL 14 | 3.2.3 |
| PostgreSQL 13 | 3.2.3 |
| PostgreSQL 12 | 3.2.3 |
| PostgreSQL 11 | 3.2.3 |

### address_standardizer_data_us

[address_standardizer_data_us](http://postgis.net/docs/manual-2.5/Address_Standardizer.html) is the Address Standardizer US dataset example.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 3.5.0 |
| PostgreSQL 16 | 3.3.3 |
| PostgreSQL 15 | 3.3.1 |
| PostgreSQL 14 | 3.2.3 |
| PostgreSQL 13 | 3.2.3 |
| PostgreSQL 12 | 3.2.3 |
| PostgreSQL 11 | 3.2.3 |

### age (preview)

[age](https://age.apache.org/) provides graph database capabilities.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | N/A |
| PostgreSQL 16 | 1.5.0 <sup>1</sup> |
| PostgreSQL 15 | 1.5.0 <sup>1</sup> |
| PostgreSQL 14 | 1.5.0 <sup>1</sup> |
| PostgreSQL 13 | 1.5.0 <sup>1</sup> |
| PostgreSQL 12 | N/A |
| PostgreSQL 11 | N/A |

<sup>1</sup> Enable corresponding libraries in the `shared_preload_libraries` server parameter.

### amcheck

[amcheck](https://www.postgresql.org/docs/13/amcheck.html) provides functions for verifying relation integrity.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.4 |
| PostgreSQL 16 | 1.3 |
| PostgreSQL 15 | 1.3 |
| PostgreSQL 14 | 1.3 |
| PostgreSQL 13 | 1.2 |
| PostgreSQL 12 | 1.2 |
| PostgreSQL 11 | 1.1 |

### anon (preview)

[anon](https://postgresql-anonymizer.readthedocs.io/) provides data anonymization tools.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.3.2 <sup>1</sup> |
| PostgreSQL 16 | 1.3.2 <sup>1</sup> |
| PostgreSQL 15 | 1.3.2 <sup>1</sup> |
| PostgreSQL 14 | 1.3.2 <sup>1</sup> |
| PostgreSQL 13 | 1.3.2 <sup>1</sup> |
| PostgreSQL 12 | 1.3.2 <sup>1</sup> |
| PostgreSQL 11 | 1.3.2 <sup>1</sup> |

<sup>1</sup> Enable corresponding libraries in the `shared_preload_libraries` server parameter.

### azure_ai

(azure_ai)[/azure/postgresql/flexible-server/generative-ai-azure-overview] provides Azure AI and ML Services integration for PostgreSQL.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | N/A |
| PostgreSQL 16 | 1.1.0 |
| PostgreSQL 15 | 1.1.0 |
| PostgreSQL 14 | 1.1.0 |
| PostgreSQL 13 | 1.1.0 |
| PostgreSQL 12 | 1.1.0 |
| PostgreSQL 11 | N/A |

### azure_storage

[azure_storage](/azure/postgresql/flexible-server/concepts-storage-extension) provides Azure integration for PostgreSQL.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | N/A |
| PostgreSQL 16 | 1.5 <sup>1</sup> |
| PostgreSQL 15 | 1.5 <sup>1</sup> |
| PostgreSQL 14 | 1.5 <sup>1</sup> |
| PostgreSQL 13 | 1.5 <sup>1</sup> |
| PostgreSQL 12 | 1.5 <sup>1</sup> |
| PostgreSQL 11 | N/A |

<sup>1</sup> Enable corresponding libraries in the `shared_preload_libraries` server parameter.

### bloom

[bloom](https://www.postgresql.org/docs/current/bloom.html) provides an index access method based on Bloom filters.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.0 |
| PostgreSQL 16 | 1.0 |
| PostgreSQL 15 | 1.0 |
| PostgreSQL 14 | 1.0 |
| PostgreSQL 13 | 1.0 |
| PostgreSQL 12 | 1.0 |
| PostgreSQL 11 | 1.0 |

### btree_gin

[btree_gin](https://www.postgresql.org/docs/current/btree-gin.html) provides support for indexing common datatypes in GIN.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.3 |
| PostgreSQL 16 | 1.3 |
| PostgreSQL 15 | 1.3 |
| PostgreSQL 14 | 1.3 |
| PostgreSQL 13 | 1.3 |
| PostgreSQL 12 | 1.3 |
| PostgreSQL 11 | 1.3 |

### btree_gist

[btree_gist](https://www.postgresql.org/docs/current/btree-gist.html) provides support for indexing common datatypes in GiST.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.7 |
| PostgreSQL 16 | 1.7 |
| PostgreSQL 15 | 1.7 |
| PostgreSQL 14 | 1.6 |
| PostgreSQL 13 | 1.5 |
| PostgreSQL 12 | 1.5 |
| PostgreSQL 11 | 1.5 |

### citext

[citext](https://www.postgresql.org/docs/current/citext.html) is a data type for case-insensitive character strings.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.6 |
| PostgreSQL 16 | 1.6 |
| PostgreSQL 15 | 1.6 |
| PostgreSQL 14 | 1.6 |
| PostgreSQL 13 | 1.6 |
| PostgreSQL 12 | 1.6 |
| PostgreSQL 11 | 1.5 |

### cube

[cube](https://www.postgresql.org/docs/current/cube.html) is a data type for multidimensional cubes.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.5 |
| PostgreSQL 16 | 1.5 |
| PostgreSQL 15 | 1.5 |
| PostgreSQL 14 | 1.5 |
| PostgreSQL 13 | 1.4 |
| PostgreSQL 12 | 1.4 |
| PostgreSQL 11 | 1.4 |

### dblink

Use [dblink](https://www.postgresql.org/docs/current/dblink.html) to connect to other PostgreSQL databases from within a database.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.2 |
| PostgreSQL 16 | 1.2 |
| PostgreSQL 15 | 1.2 |
| PostgreSQL 14 | 1.2 |
| PostgreSQL 13 | 1.2 |
| PostgreSQL 12 | 1.2 |
| PostgreSQL 11 | 1.2 |

### dict_int

[dict_int](https://www.postgresql.org/docs/current/dict-int.html) provides a text search dictionary template for integers.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.0 |
| PostgreSQL 16 | 1.0 |
| PostgreSQL 15 | 1.0 |
| PostgreSQL 14 | 1.0 |
| PostgreSQL 13 | 1.0 |
| PostgreSQL 12 | 1.0 |
| PostgreSQL 11 | 1.0 |

### dict_xsyn

[dict_xsyn](https://www.postgresql.org/docs/current/dict-xsyn.html) provides a text search dictionary template for extended synonym processing.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.0 |
| PostgreSQL 16 | 1.0 |
| PostgreSQL 15 | 1.0 |
| PostgreSQL 14 | 1.0 |
| PostgreSQL 13 | 1.0 |
| PostgreSQL 12 | 1.0 |
| PostgreSQL 11 | 1.0 |

### earthdistance

[earthdistance](https://www.postgresql.org/docs/current/earthdistance.html) calculate great-circle distances on the surface of the Earth.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.1 |
| PostgreSQL 16 | 1.1 |
| PostgreSQL 15 | 1.1 |
| PostgreSQL 14 | 1.1 |
| PostgreSQL 13 | 1.1 |
| PostgreSQL 12 | 1.1 |
| PostgreSQL 11 | 1.1 |

### fuzzystrmatch

[fuzzystrmatch](https://www.postgresql.org/docs/current/fuzzystrmatch.html) determine similarities and distance between strings.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.2 |
| PostgreSQL 16 | 1.2 |
| PostgreSQL 15 | 1.1 |
| PostgreSQL 14 | 1.1 |
| PostgreSQL 13 | 1.1 |
| PostgreSQL 12 | 1.1 |
| PostgreSQL 11 | 1.1 |

### hstore

[hstore](https://www.postgresql.org/docs/current/hstore.html) is a data type for storing sets of (key, value) pairs.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.8 |
| PostgreSQL 16 | 1.8 |
| PostgreSQL 15 | 1.8 |
| PostgreSQL 14 | 1.8 |
| PostgreSQL 13 | 1.7 |
| PostgreSQL 12 | 1.6 |
| PostgreSQL 11 | 1.5 |

### hypopg

[hypopg](https://github.com/HypoPG/hypopg) provides hypothetical indexes for PostgreSQL.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.4.0 |
| PostgreSQL 16 | 1.4.0 |
| PostgreSQL 15 | 1.4.0 |
| PostgreSQL 14 | 1.4.0 |
| PostgreSQL 13 | 1.4.0 |
| PostgreSQL 12 | 1.4.0 |
| PostgreSQL 11 | 1.4.0 |

### intagg

[intagg](https://www.postgresql.org/docs/current/intagg.html) is an obsolete extension that provides an integer aggregator and enumerator.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.1 |
| PostgreSQL 16 | 1.1 |
| PostgreSQL 15 | 1.1 |
| PostgreSQL 14 | 1.1 |
| PostgreSQL 13 | 1.1 |
| PostgreSQL 12 | 1.1 |
| PostgreSQL 11 | 1.1 |

### intarray

[intarray](https://www.postgresql.org/docs/current/intarray.html) provides functions, operators, and index support for 1-D arrays of integers.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.5 |
| PostgreSQL 16 | 1.5 |
| PostgreSQL 15 | 1.5 |
| PostgreSQL 14 | 1.5 |
| PostgreSQL 13 | 1.3 |
| PostgreSQL 12 | 1.2 |
| PostgreSQL 11 | 1.2 |

### isn

[isn](https://www.postgresql.org/docs/current/isn.html) provides data types for international product numbering standards.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.2 |
| PostgreSQL 16 | 1.2 |
| PostgreSQL 15 | 1.2 |
| PostgreSQL 14 | 1.2 |
| PostgreSQL 13 | 1.2 |
| PostgreSQL 12 | 1.2 |
| PostgreSQL 11 | 1.2 |

### lo

[lo](https://www.postgresql.org/docs/current/lo.html) provides Large Object maintenance.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.1 |
| PostgreSQL 16 | 1.1 |
| PostgreSQL 15 | 1.1 |
| PostgreSQL 14 | 1.1 |
| PostgreSQL 13 | 1.1 |
| PostgreSQL 12 | 1.1 |
| PostgreSQL 11 | 1.1 |

### login_hook

[login_hook](https://github.com/splendiddata/login_hook) is a hook to execute `login_hook.login()` at login time.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.5 |
| PostgreSQL 16 | 1.5 |
| PostgreSQL 15 | 1.4 |
| PostgreSQL 14 | 1.4 |
| PostgreSQL 13 | 1.4 |
| PostgreSQL 12 | 1.4 |
| PostgreSQL 11 | 1.4 |

### ltree

[ltree](https://www.postgresql.org/docs/current/ltree.html) is a data type for hierarchical tree-like structures.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.3 |
| PostgreSQL 16 | 1.2 |
| PostgreSQL 15 | 1.2 |
| PostgreSQL 14 | 1.2 |
| PostgreSQL 13 | 1.2 |
| PostgreSQL 12 | 1.1 |
| PostgreSQL 11 | 1.1 |

### oracle_fdw

[oracle_fdw](https://github.com/laurenz/oracle_fdw) is a foreign data wrapper for Oracle databases.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.2 |
| PostgreSQL 16 | 1.2 |
| PostgreSQL 15 | 1.2 |
| PostgreSQL 14 | 1.2 |
| PostgreSQL 13 | 1.2 |
| PostgreSQL 12 | 1.2 |
| PostgreSQL 11 | N/A |

### orafce

[orafce](https://github.com/orafce/orafce) provides functions and operators that emulate a subset of functions and packages from the Oracle RDBMS.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 4.9 |
| PostgreSQL 16 | 4.4 |
| PostgreSQL 15 | 3.24 |
| PostgreSQL 14 | 3.18 |
| PostgreSQL 13 | 3.18 |
| PostgreSQL 12 | 3.18 |
| PostgreSQL 11 | 3.7 |

### pageinspect

[pageinspect](https://www.postgresql.org/docs/current/pageinspect.html) inspects the contents of database pages at a low level.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.12 |
| PostgreSQL 16 | 1.12 |
| PostgreSQL 15 | 1.11 |
| PostgreSQL 14 | 1.9 |
| PostgreSQL 13 | 1.8 |
| PostgreSQL 12 | 1.7 |
| PostgreSQL 11 | 1.7 |

### pgaudit

[pgaudit](https://www.pgaudit.org/) provides auditing functionality.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 16.0 <sup>1</sup> |
| PostgreSQL 16 | 16.0 <sup>1</sup> |
| PostgreSQL 15 | 1.7 <sup>1</sup> |
| PostgreSQL 14 | 1.6.2 <sup>1</sup> |
| PostgreSQL 13 | 1.5 <sup>1</sup> |
| PostgreSQL 12 | 1.4.3 <sup>1</sup> |
| PostgreSQL 11 | 1.3.2 <sup>1</sup> |

<sup>1</sup> Enable corresponding libraries in the `shared_preload_libraries` server parameter.

### pg_buffercache

[pg_buffercache](https://www.postgresql.org/docs/current/pgbuffercache.html) examines the shared buffer cache.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.5 |
| PostgreSQL 16 | 1.4 |
| PostgreSQL 15 | 1.3 |
| PostgreSQL 14 | 1.3 |
| PostgreSQL 13 | 1.3 |
| PostgreSQL 12 | 1.3 |
| PostgreSQL 11 | 1.3 |

### pg_cron

[pg_cron](https://github.com/citusdata/pg_cron) is a job scheduler for PostgreSQL.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.6 <sup>1</sup> |
| PostgreSQL 16 | 1.6 <sup>1</sup> |
| PostgreSQL 15 | 1.6 <sup>1</sup> |
| PostgreSQL 14 | 1.6 <sup>1</sup> |
| PostgreSQL 13 | 1.6 <sup>1</sup> |
| PostgreSQL 12 | 1.6 <sup>1</sup> |
| PostgreSQL 11 | 1.4-1 <sup>1</sup> |

<sup>1</sup> Enable corresponding libraries in the `shared_preload_libraries` server parameter.

### pgcrypto

[pgcrypto](https://www.postgresql.org/docs/current/pgcrypto.html) provides cryptographic functions.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.3 |
| PostgreSQL 16 | 1.3 |
| PostgreSQL 15 | 1.3 |
| PostgreSQL 14 | 1.3 |
| PostgreSQL 13 | 1.3 |
| PostgreSQL 12 | 1.3 |
| PostgreSQL 11 | 1.3 |

### pg_freespacemap

[pg_freespacemap](https://www.postgresql.org/docs/current/pgfreespacemap.html) examines the free space map (FSM).

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.2 |
| PostgreSQL 16 | 1.2 |
| PostgreSQL 15 | 1.2 |
| PostgreSQL 14 | 1.2 |
| PostgreSQL 13 | 1.2 |
| PostgreSQL 12 | 1.2 |
| PostgreSQL 11 | 1.2 |

### pg_hint_plan

[pg_hint_plan](https://github.com/ossc-db/pg_hint_plan) makes it possible to tweak PostgreSQL execution plans using so-called hints in SQL comments.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.7.0 <sup>1</sup> |
| PostgreSQL 16 | 1.6.0 <sup>1</sup> |
| PostgreSQL 15 | 1.5 <sup>1</sup> |
| PostgreSQL 14 | 1.4 <sup>1</sup> |
| PostgreSQL 13 | 1.3.7 <sup>1</sup> |
| PostgreSQL 12 | 1.3.7 <sup>1</sup> |
| PostgreSQL 11 | 1.3.7 <sup>1</sup> |

<sup>1</sup> Enable corresponding libraries in the `shared_preload_libraries` server parameter.

### pglogical

[pglogical](https://github.com/2ndQuadrant/pglogical) manages PostgreSQL Logical Replication.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 2.4.5 <sup>1</sup> |
| PostgreSQL 16 | 2.4.4 <sup>1</sup> |
| PostgreSQL 15 | 2.4.2 <sup>1</sup> |
| PostgreSQL 14 | 2.4.1 <sup>1</sup> |
| PostgreSQL 13 | 2.4.1 <sup>1</sup> |
| PostgreSQL 12 | 2.4.1 <sup>1</sup> |
| PostgreSQL 11 | 2.4.1 <sup>1</sup> |

<sup>1</sup> Enable corresponding libraries in the `shared_preload_libraries` server parameter.

### pg_partman

[pg_partman](https://github.com/pgpartman/pg_partman) manages partitioned tables by time or ID.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 5.0.1 <sup>1</sup> |
| PostgreSQL 16 | 5.0.1 <sup>1</sup> |
| PostgreSQL 15 | 4.7.1 <sup>1</sup> |
| PostgreSQL 14 | 4.6.1 <sup>1</sup> |
| PostgreSQL 13 | 4.5.0 <sup>1</sup> |
| PostgreSQL 12 | 4.5.0 <sup>1</sup> |
| PostgreSQL 11 | 4.5.0 <sup>1</sup> |

<sup>1</sup> Enable corresponding libraries in the `shared_preload_libraries` server parameter.

### pg_prewarm

Prewarm relation data with [pg_prewarm](https://www.postgresql.org/docs/current/pgprewarm.html).

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.2 <sup>1</sup> |
| PostgreSQL 16 | 1.2 <sup>1</sup> |
| PostgreSQL 15 | 1.2 <sup>1</sup> |
| PostgreSQL 14 | 1.2 <sup>1</sup> |
| PostgreSQL 13 | 1.2 <sup>1</sup> |
| PostgreSQL 12 | 1.2 <sup>1</sup> |
| PostgreSQL 11 | 1.2 <sup>1</sup> |

<sup>1</sup> Enable corresponding libraries in the `shared_preload_libraries` server parameter.

### pg_repack

[pg_repack](https://reorg.github.io/pg_repack/) reorganizes tables in PostgreSQL databases with minimal locks.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.4.7 |
| PostgreSQL 16 | 1.4.7 |
| PostgreSQL 15 | 1.4.7 |
| PostgreSQL 14 | 1.4.7 |
| PostgreSQL 13 | 1.4.7 |
| PostgreSQL 12 | 1.4.7 |
| PostgreSQL 11 | 1.4.7 |

### pgRouting

[pgRouting](https://pgrouting.org/) provides geospatial routing functionality.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | N/A |
| PostgreSQL 16 | N/A |
| PostgreSQL 15 | 3.5.0 |
| PostgreSQL 14 | 3.3.0 |
| PostgreSQL 13 | 3.3.0 |
| PostgreSQL 12 | 3.3.0 |
| PostgreSQL 11 | 3.3.0 |

### pgrowlocks

[pgrowlocks](https://www.postgresql.org/docs/current/pgrowlocks.html) shows row-level locking information.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.2 |
| PostgreSQL 16 | 1.2 |
| PostgreSQL 15 | 1.2 |
| PostgreSQL 14 | 1.2 |
| PostgreSQL 13 | 1.2 |
| PostgreSQL 12 | 1.2 |
| PostgreSQL 11 | 1.2 |

### pg_squeeze

[pg_squeeze](https://github.com/cybertec-postgresql/pg_squeeze) removes unused space from a relation.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.7 <sup>1</sup> |
| PostgreSQL 16 | 1.6 <sup>1</sup> |
| PostgreSQL 15 | 1.6 <sup>1</sup> |
| PostgreSQL 14 | 1.5 <sup>1</sup> |
| PostgreSQL 13 | 1.5 <sup>1</sup> |
| PostgreSQL 12 | 1.5 <sup>1</sup> |
| PostgreSQL 11 | 1.5 <sup>1</sup> |

<sup>1</sup> Enable corresponding libraries in the `shared_preload_libraries` server parameter.

### pg_stat_statements

Track execution statistics of all SQL statements executed, with [pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html).

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.11 <sup>1</sup> |
| PostgreSQL 16 | 1.10 <sup>1</sup> |
| PostgreSQL 15 | 1.10 <sup>1</sup> |
| PostgreSQL 14 | 1.9 <sup>1</sup> |
| PostgreSQL 13 | 1.8 <sup>1</sup> |
| PostgreSQL 12 | 1.7 <sup>1</sup> |
| PostgreSQL 11 | 1.6 <sup>1</sup> |

<sup>1</sup> Enable corresponding libraries in the `shared_preload_libraries` server parameter.

### pgstattuple

Show tuple-level statistics, with [pgstattuple](https://www.postgresql.org/docs/current/pgstattuple.html).

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.5 |
| PostgreSQL 16 | 1.5 |
| PostgreSQL 15 | 1.5 |
| PostgreSQL 14 | 1.5 |
| PostgreSQL 13 | 1.5 |
| PostgreSQL 12 | 1.5 |
| PostgreSQL 11 | 1.5 |

### pg_trgm

[pg_trgm](https://www.postgresql.org/docs/current/pgtrgm.html) provides text similarity measurement and index searching based on trigrams.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.6 |
| PostgreSQL 16 | 1.6 |
| PostgreSQL 15 | 1.6 |
| PostgreSQL 14 | 1.6 |
| PostgreSQL 13 | 1.5 |
| PostgreSQL 12 | 1.4 |
| PostgreSQL 11 | 1.4 |

### pg_visibility

[pg_visibility](https://www.postgresql.org/docs/current/pgvisibility.html) examine the visibility map and page-level visibility info.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.2 |
| PostgreSQL 16 | 1.2 |
| PostgreSQL 15 | 1.2 |
| PostgreSQL 14 | 1.2 |
| PostgreSQL 13 | 1.2 |
| PostgreSQL 12 | 1.2 |
| PostgreSQL 11 | 1.2 |

### pgvector

[pgvector](https://github.com/pgvector/pgvector) is a vector data type and `ivfflat` and `hnsw` access methods.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 0.7.0 |
| PostgreSQL 16 | 0.7.0 |
| PostgreSQL 15 | 0.7.0 |
| PostgreSQL 14 | 0.7.0 |
| PostgreSQL 13 | 0.7.0 |
| PostgreSQL 12 | 0.7.0 |
| PostgreSQL 11 | 0.5.1 |

### plpgsql

[PL/pgSQL](https://www.postgresql.org/docs/current/plpgsql.html) is a SQL procedural language.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.0 |
| PostgreSQL 16 | 1.0 |
| PostgreSQL 15 | 1.0 |
| PostgreSQL 14 | 1.0 |
| PostgreSQL 13 | 1.0 |
| PostgreSQL 12 | 1.0 |
| PostgreSQL 11 | 1.0 |

### plv8

[PL/JavaScript (v8)](https://github.com/plv8/plv8) is a trusted procedural language.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 3.1.7 |
| PostgreSQL 16 | 3.1.7 |
| PostgreSQL 15 | 3.1.7 |
| PostgreSQL 14 | 3.0.0 |
| PostgreSQL 13 | 3.0.0 |
| PostgreSQL 12 | 3.0.0 |
| PostgreSQL 11 | 3.0.0 |

### postgis

[PostGIS](https://www.postgis.net/) geometry and geography spatial types and functions.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 3.5.0 |
| PostgreSQL 16 | 3.3.3 |
| PostgreSQL 15 | 3.3.1 |
| PostgreSQL 14 | 3.2.3 |
| PostgreSQL 13 | 3.2.3 |
| PostgreSQL 12 | 3.2.3 |
| PostgreSQL 11 | 3.2.3 |

### postgis_raster

[PostGIS](https://www.postgis.net/) raster types and functions.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 3.5.0 |
| PostgreSQL 16 | 3.3.3 |
| PostgreSQL 15 | 3.3.1 |
| PostgreSQL 14 | 3.2.3 |
| PostgreSQL 13 | 3.2.3 |
| PostgreSQL 12 | 3.2.3 |
| PostgreSQL 11 | 3.2.3 |

### postgis_sfcgal

[PostGIS](https://www.postgis.net/) SFCGAL functions.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 3.5.0 |
| PostgreSQL 16 | 3.3.3 |
| PostgreSQL 15 | 3.3.1 |
| PostgreSQL 14 | 3.2.3 |
| PostgreSQL 13 | 3.2.3 |
| PostgreSQL 12 | 3.2.3 |
| PostgreSQL 11 | 3.2.3 |

### postgis_tiger_geocoder

[PostGIS](https://www.postgis.net/) tiger geocoder and reverse geocoder.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 3.5.0 |
| PostgreSQL 16 | 3.3.3 |
| PostgreSQL 15 | 3.3.1 |
| PostgreSQL 14 | 3.2.3 |
| PostgreSQL 13 | 3.2.3 |
| PostgreSQL 12 | 3.2.3 |
| PostgreSQL 11 | 3.2.3 |

### postgis_topology

[PostGIS topology](https://postgis.net/docs/Topology.html) spatial types and functions.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 3.5.0 |
| PostgreSQL 16 | 3.3.3 |
| PostgreSQL 15 | 3.3.1 |
| PostgreSQL 14 | 3.2.3 |
| PostgreSQL 13 | 3.2.3 |
| PostgreSQL 12 | 3.2.3 |
| PostgreSQL 11 | 3.2.3 |

### postgres_fdw

[postgres_fdw](https://www.postgresql.org/docs/current/postgres-fdw.html) is a foreign-data wrapper for remote PostgreSQL servers.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.1 |
| PostgreSQL 16 | 1.1 |
| PostgreSQL 15 | 1.1 |
| PostgreSQL 14 | 1.1 |
| PostgreSQL 13 | 1.0 |
| PostgreSQL 12 | 1.0 |
| PostgreSQL 11 | 1.0 |

### postgres_protobuf

[postgres_protobuf](https://github.com/mpartel/postgres-protobuf) provides protocol buffers for PostgreSQL.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 0.2 |
| PostgreSQL 16 | 0.2 |
| PostgreSQL 15 | 0.2 |
| PostgreSQL 14 | 0.2 |
| PostgreSQL 13 | 0.2 |
| PostgreSQL 12 | 0.2 |
| PostgreSQL 11 | N/A |

### semver

[semver](https://pgxn.org/dist/semver/doc/semver.html) provides a semantic version data type.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 0.32.1 |
| PostgreSQL 16 | 0.32.1 |
| PostgreSQL 15 | 0.32.0 |
| PostgreSQL 14 | 0.32.0 |
| PostgreSQL 13 | 0.32.0 |
| PostgreSQL 12 | 0.32.0 |
| PostgreSQL 11 | 0.32.0 |

### session_variable

[session_variable](https://github.com/splendiddata/session_variable) provides registration and manipulation of session variables and constants.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 3.3 |
| PostgreSQL 16 | 3.3 |
| PostgreSQL 15 | 3.3 |
| PostgreSQL 14 | 3.3 |
| PostgreSQL 13 | 3.3 |
| PostgreSQL 12 | 3.3 |
| PostgreSQL 11 | 3.3 |

### sslinfo

[sslinfo](https://www.postgresql.org/docs/current/sslinfo.html) provides information about SSL certificates.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.2 |
| PostgreSQL 16 | 1.2 |
| PostgreSQL 15 | 1.2 |
| PostgreSQL 14 | 1.2 |
| PostgreSQL 13 | 1.2 |
| PostgreSQL 12 | 1.2 |
| PostgreSQL 11 | 1.2 |

### tablefunc

[tablefunc](https://www.postgresql.org/docs/current/tablefunc.html) provides functions that manipulate whole tables, including crosstab.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.0 |
| PostgreSQL 16 | 1.0 |
| PostgreSQL 15 | 1.0 |
| PostgreSQL 14 | 1.0 |
| PostgreSQL 13 | 1.0 |
| PostgreSQL 12 | 1.0 |
| PostgreSQL 11 | 1.0 |

### tds_fdw

[tds_fdw](https://github.com/tds-fdw/tds_fdw) is a foreign data wrapper for querying a TDS database (SAP ASE or SQL Server).

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 2.0.3 |
| PostgreSQL 16 | 2.0.3 |
| PostgreSQL 15 | 2.0.3 |
| PostgreSQL 14 | 2.0.3 |
| PostgreSQL 13 | 2.0.3 |
| PostgreSQL 12 | 2.0.3 |
| PostgreSQL 11 | 2.0.3 |

### timescaledb

[timescaledb](https://github.com/timescale/timescaledb) enables scalable inserts and complex queries for time-series data.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | N/A |
| PostgreSQL 16 | 2.13.0 <sup>1</sup> |
| PostgreSQL 15 | 2.10.0 <sup>1</sup> |
| PostgreSQL 14 | 2.10.0 <sup>1</sup> |
| PostgreSQL 13 | 2.10.0 <sup>1</sup> |
| PostgreSQL 12 | 2.10.0 <sup>1</sup> |
| PostgreSQL 11 | 1.7.4 <sup>1</sup> |

<sup>1</sup> Enable corresponding libraries in the `shared_preload_libraries` server parameter.

### tsm_system_rows

[tsm_system_rows](https://www.postgresql.org/docs/13/tsm-system-rows.html) is a `TABLESAMPLE` method which accepts number of rows as a limit.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.0 |
| PostgreSQL 16 | 1.0 |
| PostgreSQL 15 | 1.0 |
| PostgreSQL 14 | 1.0 |
| PostgreSQL 13 | 1.0 |
| PostgreSQL 12 | 1.0 |
| PostgreSQL 11 | 1.0 |

### tsm_system_time

[tsm_system_time](https://www.postgresql.org/docs/current/tsm-system-time.html) is a `TABLESAMPLE` method which accepts time in milliseconds as a limit.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.0 |
| PostgreSQL 16 | 1.0 |
| PostgreSQL 15 | 1.0 |
| PostgreSQL 14 | 1.0 |
| PostgreSQL 13 | 1.0 |
| PostgreSQL 12 | 1.0 |
| PostgreSQL 11 | 1.0 |

### unaccent

[unaccent](https://www.postgresql.org/docs/current/unaccent.html) provides a text search dictionary that removes accents.

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.1 |
| PostgreSQL 16 | 1.1 |
| PostgreSQL 15 | 1.1 |
| PostgreSQL 14 | 1.1 |
| PostgreSQL 13 | 1.1 |
| PostgreSQL 12 | 1.1 |
| PostgreSQL 11 | 1.1 |

### uuid-ossp

[uuid-ossp](https://www.postgresql.org/docs/current/uuid-ossp.html) generates universally unique identifiers (UUIDs).

| PostgreSQL version | Extension version |
| --- | --- |
| PostgreSQL 17 | 1.1 |
| PostgreSQL 16 | 1.1 |
| PostgreSQL 15 | 1.1 |
| PostgreSQL 14 | 1.1 |
| PostgreSQL 13 | 1.1 |
| PostgreSQL 12 | 1.1 |
| PostgreSQL 11 | 1.1 |
