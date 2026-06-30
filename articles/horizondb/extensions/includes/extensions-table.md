---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/30/2026
ms.service: azure-horizondb
ms.topic: include
ms.custom:
  - automatically generated
---

## address_standardizer

[address_standardizer](https://postgis.net/docs/manual-2.5/Address_Standardizer.html) is used to parse an address into constituent elements. Generally used to support geocoding address normalization step.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 3.5.2 |

## address_standardizer_data_us

[address_standardizer_data_us](https://postgis.net/docs/manual-2.5/Address_Standardizer.html) is the Address Standardizer US dataset example.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 3.5.2 |

## age

[age](https://age.apache.org/) (Preview) provides graph database capabilities.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.6.0 <sup>*</sup> |

<sup>*</sup> Enable corresponding libraries in the `shared_preload_libraries` parameter.

## amcheck

[amcheck](https://www.postgresql.org/docs/17/amcheck.html) provides functions for verifying relation integrity.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.4 |

## auto_explain

[auto_explain](https://www.postgresql.org/docs/current/auto-explain.html) provides a means for logging execution plans of slow statements automatically, without having to run EXPLAIN by hand.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | Without version <sup>*</sup> |

<sup>*</sup> Enable corresponding libraries in the `shared_preload_libraries` parameter.

## azure_ai

{[azure_ai](../../ai/ai-functions.md)} provides Microsoft Foundry and Azure Machine Learning Services integration for PostgreSQL.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 2.2.1 |

## azure_storage

{[azure_storage](../concepts-storage-extension.md)} provides Azure Storage integration for PostgreSQL.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.9 <sup>*</sup> |

<sup>*</sup> Enable corresponding libraries in the `shared_preload_libraries` parameter.

## bloom

[bloom](https://www.postgresql.org/docs/current/bloom.html) provides an index access method based on Bloom filters.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.0 |

## btree_gin

[btree_gin](https://www.postgresql.org/docs/current/btree-gin.html) provides support for indexing common datatypes in GIN.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.3 |

## btree_gist

[btree_gist](https://www.postgresql.org/docs/current/btree-gist.html) provides support for indexing common datatypes in GiST.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.7 |

## citext

[citext](https://www.postgresql.org/docs/current/citext.html) is a data type for case-insensitive character strings.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.6 |

## cube

[cube](https://www.postgresql.org/docs/current/cube.html) is a data type for multidimensional cubes.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.5 |

## dblink

[dblink](https://www.postgresql.org/docs/current/dblink.html) to connect to other PostgreSQL databases from within a database.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.2 |

Read the special considerations for extension [dblink](../concepts-extensions-considerations.md#dblink) in Azure HorizonDB.

## dict_int

[dict_int](https://www.postgresql.org/docs/current/dict-int.html) provides a text search dictionary template for integers.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.0 |

## dict_xsyn

[dict_xsyn](https://www.postgresql.org/docs/current/dict-xsyn.html) provides a text search dictionary template for extended synonym processing.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.0 |

## earthdistance

[earthdistance](https://www.postgresql.org/docs/current/earthdistance.html) calculates great-circle distances on the surface of the Earth.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.2 |

## fuzzystrmatch

[fuzzystrmatch](https://www.postgresql.org/docs/current/fuzzystrmatch.html) determines similarities and distance between strings.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.2 |

## hstore

[hstore](https://www.postgresql.org/docs/current/hstore.html) is a data type for storing sets of (key, value) pairs.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.8 |

## hypopg

[hypopg](https://github.com/HypoPG/hypopg) provides hypothetical indexes for PostgreSQL.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.4.1 |

## intagg

[intagg](https://www.postgresql.org/docs/current/intagg.html) is an obsolete extension that provides an integer aggregator and enumerator.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.1 |

## intarray

[intarray](https://www.postgresql.org/docs/current/intarray.html) provides functions, operators, and index support for 1-D arrays of integers.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.5 |

## isn

[isn](https://www.postgresql.org/docs/current/isn.html) provides data types for international product numbering standards.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.2 |

## lo

[lo](https://www.postgresql.org/docs/current/lo.html) provides support for managing Large Objects (also called LOs or BLOBs). This includes a data type lo and a trigger lo_manage.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.1 |

## ltree

[ltree](https://www.postgresql.org/docs/current/ltree.html) is a data type for hierarchical tree-like structures.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.3 |

## orafce

[orafce](https://github.com/orafce/orafce) provides functions and operators that emulate a subset of functions and packages from the Oracle RDBMS.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 4.9 |

## pageinspect

[pageinspect](https://www.postgresql.org/docs/current/pageinspect.html) inspects the contents of database pages at a low level.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.12 |

## pgaudit

[pgaudit](https://www.pgaudit.org/) provides auditing functionality.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 16.0 <sup>*</sup> |

<sup>*</sup> Enable corresponding libraries in the `shared_preload_libraries` parameter.

## pg_buffercache

[pg_buffercache](https://www.postgresql.org/docs/current/pgbuffercache.html) examines the shared buffer cache.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.5 |

Read the special considerations for extension [pg_buffercache](../concepts-extensions-considerations.md#pg_buffercache) in Azure HorizonDB.

## pg_cron

[pg_cron](https://github.com/citusdata/pg_cron) is a job scheduler for PostgreSQL.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.6 <sup>*</sup> |

<sup>*</sup> Enable corresponding libraries in the `shared_preload_libraries` parameter.
Read the special considerations for extension [pg_cron](../concepts-extensions-considerations.md#pg_cron) in Azure HorizonDB.

## pgcrypto

[pgcrypto](https://www.postgresql.org/docs/current/pgcrypto.html) provides cryptographic functions.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.3 |

## pg_diskann

{[pg_diskann](../../ai/vector-index-diskann.md)} is a scalable approximate nearest neighbor search algorithm for efficient vector search at any scale.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 0.7.1 |

## pg_failover_slots

[pg_failover_slots](https://github.com/EnterpriseDB/pg_failover_slots) is a logical replication slot manager for failover purposes.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | Not supported <sup>*</sup> |

<sup>*</sup> Enable corresponding libraries in the `shared_preload_libraries` parameter.
Read the special considerations for extension [pg_failover_slots](../concepts-extensions-considerations.md#pg_failover_slots) in Azure HorizonDB.

## pg_freespacemap

[pg_freespacemap](https://www.postgresql.org/docs/current/pgfreespacemap.html) examines the free space map (FSM).

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.2 |

## pglogical

[pglogical](https://github.com/2ndQuadrant/pglogical) manages PostgreSQL Logical Replication.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 2.4.5 <sup>*</sup> |

<sup>*</sup> Enable corresponding libraries in the `shared_preload_libraries` parameter.

## pg_partman

[pg_partman](https://github.com/pgpartman/pg_partman) manages partitioned tables by time or ID.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 5.0.1 <sup>*</sup> |

<sup>*</sup> Enable corresponding libraries in the `shared_preload_libraries` parameter.

## pg_partman_bgw

[pg_partman_bgw](https://github.com/pgpartman/pg_partman) manages partitioned tables by time or ID.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 5.0.1 <sup>*</sup> |

<sup>*</sup> Enable corresponding libraries in the `shared_preload_libraries` parameter.

## pg_prewarm

[pg_prewarm](https://www.postgresql.org/docs/current/pgprewarm.html) prewarms the cache with relation data.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.2 <sup>*</sup> |

<sup>*</sup> Enable corresponding libraries in the `shared_preload_libraries` parameter.
Read the special considerations for extension [pg_prewarm](../concepts-extensions-considerations.md#pg_prewarm) in Azure HorizonDB.

## pg_repack

[pg_repack](https://reorg.github.io/pg_repack/) reorganizes tables in PostgreSQL databases with minimal locks.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.5.1 |

Read the special considerations for extension [pg_repack](../concepts-extensions-considerations.md#pg_repack) in Azure HorizonDB.

## pgrowlocks

[pgrowlocks](https://www.postgresql.org/docs/current/pgrowlocks.html) shows row-level locking information.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.2 |

## pg_stat_statements

[pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html) tracks execution statistics of all SQL statements executed.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.11 <sup>*</sup> |

<sup>*</sup> Enable corresponding libraries in the `shared_preload_libraries` parameter.
Read the special considerations for extension [pg_stat_statements](../concepts-extensions-considerations.md#pg_stat_statements) in Azure HorizonDB.

## pgstattuple

[pgstattuple](https://www.postgresql.org/docs/current/pgstattuple.html) shows tuple-level statistics.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.5 |

Read the special considerations for extension [pgstattuple](../concepts-extensions-considerations.md#pgstattuple) in Azure HorizonDB.

## pg_trgm

[pg_trgm](https://www.postgresql.org/docs/current/pgtrgm.html) provides text similarity measurement and index searching based on trigrams.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.6 |

## pg_visibility

[pg_visibility](https://www.postgresql.org/docs/current/pgvisibility.html) examines the visibility map and page-level visibility info.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.2 |

## postgis

[postgis](https://www.postgis.net/) geometry and geography spatial types and functions.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 3.5.2 |

## postgis_raster

[postgis_raster](https://www.postgis.net) raster types and functions.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 3.5.2 |

## postgis_sfcgal

[postgis_sfcgal](https://www.postgis.net) sFCGAL functions.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 3.5.2 |

## postgis_tiger_geocoder

[postgis_tiger_geocoder](https://www.postgis.net) tiger geocoder and reverse geocoder.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 3.5.2 |

## postgis_topology

[postgis_topology](https://postgis.net/docs/Topology.html) spatial types and functions.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 3.5.2 |

## postgres_fdw

[postgres_fdw](https://www.postgresql.org/docs/current/postgres-fdw.html) is a foreign-data wrapper for remote PostgreSQL servers.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.1 |

Read the special considerations for extension [postgres_fdw](../concepts-extensions-considerations.md#postgres_fdw) in Azure HorizonDB.

## sslinfo

[sslinfo](https://www.postgresql.org/docs/current/sslinfo.html) provides information about SSL certificates.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.2 |

## tablefunc

[tablefunc](https://www.postgresql.org/docs/current/tablefunc.html) provides functions that manipulate whole tables, including crosstab.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.0 |

## tsm_system_time

[tsm_system_time](https://www.postgresql.org/docs/current/tsm-system-time.html) is a `TABLESAMPLE` method which accepts time in milliseconds as a limit.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.0 |

## unaccent

[unaccent](https://www.postgresql.org/docs/current/unaccent.html) provides a text search dictionary that removes accents.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.1 |

## uuid-ossp

[uuid-ossp](https://www.postgresql.org/docs/current/uuid-ossp.html) generates universally unique identifiers (UUIDs).

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 1.1 |

## vector

[vector](https://github.com/pgvector/pgvector) is a vector data type and `ivfflat` and `hnsw` access methods.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 0.8.0 |

## wal2json

[wal2json](https://github.com/eulerto/wal2json) is an output plugin for logical decoding. It means that the plugin has access to tuples produced by INSERT and UPDATE. Also, UPDATE/DELETE old row versions can be accessed depending on the configured replica identity.

| PostgreSQL version | Extension or module version |
| --- | --- |
| 17 | 2.6 <sup>*</sup> |

<sup>*</sup> Enable corresponding libraries in the `shared_preload_libraries` parameter.
