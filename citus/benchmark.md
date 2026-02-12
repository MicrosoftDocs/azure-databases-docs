---
title: Benchmark Setup with Citus and Pgbench
description: Learn how to benchmark Citus write throughput with pgbench so you can measure database performance.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
monikerRange: "citus-13 || citus-14"
---

# Benchmark setup with Citus and pgbench

This article provides step-by-step instructions to benchmark Citus' write throughput. For these benchmark steps, use [Citus Cloud](citus-cloud.md) to create test clusters and a standard benchmarking tool called [pgbench](https://www.postgresql.org/docs/current/static/pgbench.html).

> [!NOTE]  
> New users can no longer onboard to Citus Cloud on Amazon Web Services (AWS). Citus is still available as open source and in the cloud on Microsoft Azure as a fully integrated deployment option.
>
> See [Managed Service](citus-cloud.md).

For more information on general throughput numbers based on these tests, see [Migrate Production Data](migrate/migration-data.md).

## Create Citus cluster

The easiest way to start a Citus Cluster is by visiting the Citus Cloud dashboard. This dashboard allows you to choose different coordinator and worker node configurations and charges you by the hour. Once you pick your desired cluster setup, select the **Create New Formation** button.

:::image type="content" source="media/write-throughput-benchmark/coordinator-worker-slider.png" alt-text="Screenshot of formation configuration.":::

A pop-up asks you the AWS region (US East, US West) for your formation. Remember the region where you created your Citus Cloud formation for the next step.

Citus Cloud automatically tunes your cluster based on your hardware configuration. If you plan to run the following steps on your own cluster, make sure to increase `max_connections = 300` on the coordinator and worker nodes.

## Create an instance to run pgbench

pgbench is a standard benchmarking tool provided by PostgreSQL. pgbench repeatedly runs given SQL commands and measures the number of completed transactions per second.

Since pgbench itself consumes CPU power, run it on a separate machine from the machine running your Citus cluster. pgbench's own documentation also points out that putting it on the same machine as the tested database can skew test results.

In these tests, create a separate EC2 instance to run pgbench, and place the instance in the same AWS region as your Citus cluster. Use a large EC2 (m4.16xlarge) instance to ensure pgbench itself doesn't become the performance bottleneck.

## Install pgbench

After creating a new EC2 instance, install pgbench on the instance. Pgbench 10 runs across all Citus versions, and the following instructions assume that you use pgbench 10.

- For **Debian** based system:

  ```bash
  sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
  sudo apt-get install wget ca-certificates
  wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
  sudo apt-get update
  sudo apt-get install postgresql-10
  ```

- For **RedHat** based system:

  Follow the [yum installation guide](https://www.postgresql.org/download/linux/redhat/).

## Benchmark INSERT throughput

This section shows how to benchmark INSERT throughput on your Citus cluster. You create a distributed table, set up pgbench with a custom SQL file, and run parallel INSERT operations to measure transactions per second.

### Initialize and distribute tables

Before you start, tell pgbench to initialize the benchmarking environment by creating test tables. Then, connect to the Citus coordinator node and distribute the table that you're going to run INSERT benchmarks on.

To initialize the test environment and distribute the related table, get a connection string to the cluster. You can get this connection string from your Citus Cloud dashboard. Then, run the following two commands:

```bash
pgbench -i connection_string_to_coordinator

psql connection_string_to_coordinator -c "SELECT create_distributed_table('pgbench_history', 'aid');"
```

### Create SQL file for pgbench

Pgbench runs the given SQL commands repeatedly and reports results. For this benchmark run, use the INSERT command that comes with pgbench.

To create the related SQL commands, create a file named `insert.sql` and paste the following lines into it:

``` psql
\set nbranches :scale
\set ntellers 10 * :scale
\set naccounts 100000 * :scale
\set aid random(1, :naccounts)
\set bid random(1, :nbranches)
\set tid random(1, :ntellers)
\set delta random(-5000, 5000)
INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);
```

## Benchmark INSERT commands

By default, pgbench opens a single connection to the database and sends INSERT commands through this connection. To benchmark write throughput, open parallel connections to the database and issue concurrent commands. Use pgbench's `-j` parameter to specify the number of concurrent threads and `-c` parameter to specify the number of concurrent connections. Set the duration for your tests to 30 seconds by using the `-T` parameter.

To run pgbench with these parameters, type:

```bash
pgbench connection_string_to_coordinator -j 64 -c 256 -f insert.sql -T 30
```

These parameters open 256 concurrent connections to Citus. If you're running Citus on your own instances, you need to increase the default `max_connections` setting.

## Benchmark UPDATE throughput

This section shows how to benchmark UPDATE throughput on your Citus cluster. You create a distributed table, set up pgbench with a custom SQL file, and run parallel UPDATE operations to measure transactions per second.

### Initialize and distribute tables

Before you start, tell pgbench to initialize the benchmarking environment by creating test tables. Then, connect to the Citus coordinator node and distribute the table that you're going to run UPDATE benchmarks on.

To initialize the test environment and distribute the related table, get a connection string to the cluster. You can get this connection string from your Citus Cloud dashboard. Then, run the following two commands:

```bash
pgbench -i connection_string_to_coordinator

# INSERT and UPDATE tests run on different distributed tables
psql connection_string_to_coordinator -c "SELECT create_distributed_table('pgbench_accounts', 'aid');"
```

### Create SQL file for pgbench

pgbench runs the given SQL commands repeatedly and reports results. For this benchmark run, use one of the UPDATE commands that comes with pgbench.

To create the related SQL commands, create a file named `update.sql` and paste the following lines into it:

``` psql
\set naccounts 100000 * :scale
\set aid random(1, :naccounts)
\set delta random(-5000, 5000)
UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;
```

## Benchmark UPDATE commands

By default, pgbench opens a single connection to the database and sends UPDATE commands through this connection. To benchmark write throughput, open parallel connections to the database and send concurrent commands. Use pgbench's `-j` parameter to specify the number of concurrent threads and the `-c` parameter to specify the number of concurrent connections. Set the duration for your tests to 30 seconds by using the `-T` parameter.

To run pgbench with these parameters, type the following command:

```bash
pgbench connection_string_to_coordinator -j 64 -c 256 -f update.sql -T 30
```

These parameters open 256 concurrent connections to Citus. If you run Citus on your own instances, you need to increase the default `max_connections` setting.

## Related content

- [Performance tuning](performance-tuning.md)
- [What is Citus?](what-is-citus.md)
