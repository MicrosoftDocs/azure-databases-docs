---
title: "Tutorial: Design for Microservices with Elastic Clusters"
description: This tutorial shows how to design for microservices with elastic clusters on Azure Database for PostgreSQL.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: tutorial
# customer intent: As a user, I want to learn how to use elastic clusters on Azure Database for PostgreSQL when deploying applications using the microservices architecture.
---

# Tutorial: Design for microservices with elastic clusters

In this tutorial, you use Azure Database for PostgreSQL as the storage backend for multiple microservices. The tutorial demonstrates a sample setup and basic operation of such a cluster. Learn how to:

> [!div class="checklist"]
> - Prerequisites
> - Create roles for your microservices
> - Use psql utility to create roles and distributed schemas
> - Create tables for the sample services
> - Configure services
> - Run services
> - Explore the database

## Prerequisites

Create an elastic cluster in one of the following ways:
- [Create an elastic cluster using the Portal](../elastic-clusters/quickstart-create-elastic-cluster-portal.md)
- [Create an elastic cluster using Bicep](../elastic-clusters/quickstart-create-elastic-cluster-bicep.md)
- [Create an elastic cluster with ARM template](../elastic-clusters/quickstart-create-elastic-cluster-arm-template.md)

## Create roles for your microservices

You can dynamically place distributed schemas within an elastic cluster. The system can rebalance them as a whole unit across the available nodes, so you get improved efficiency across your cluster resources without manual allocation.

When you apply schema sharding to a microservice design pattern, you create a database schema for each corresponding microservice. Also, use a distinct ROLE for each microservice when connecting to the database. When each user connects, their role name goes at the beginning of the search_path. If the role name matches the schema name, you don't need any additional application changes to set the correct search_path.

In this example, use three microservices:

- user
- time
- ping

Create the database roles for each service:

```sql
CREATE USER user_service;
CREATE USER time_service;
CREATE USER ping_service;
```

## Use psql utility to create distributed schemas

After you connect to the elastic cluster by using psql, you can complete some basic tasks.

You can distribute a schema in two ways:

- Manually by calling the `citus_schema_distribute(schema_name)` function:

```sql
CREATE SCHEMA AUTHORIZATION user_service;
CREATE SCHEMA AUTHORIZATION time_service;
CREATE SCHEMA AUTHORIZATION ping_service;

SELECT citus_schema_distribute('user_service');
SELECT citus_schema_distribute('time_service');
SELECT citus_schema_distribute('ping_service');
```

This method also allows you to convert existing regular schemas into distributed schemas.

> [!NOTE]
> You can only distribute schemas that don't contain distributed and reference tables.

- By enabling the `citus.enable_schema_based_sharding` configuration variable. You can change the variable for the current session or permanently from the coordinator node parameters. When you set the parameter to ON, all created schemas are distributed by default.

```sql
SET citus.enable_schema_based_sharding TO ON;

CREATE SCHEMA AUTHORIZATION user_service;
CREATE SCHEMA AUTHORIZATION time_service;
CREATE SCHEMA AUTHORIZATION ping_service;
```
Run the following command to list the currently distributed schemas:

```sql
SELECT * FROM citus_schemas;
```

```output
 schema_name | colocation_id | schema_size | schema_owner
-------------+---------------+-------------+--------------
 user_service |             5 | 0 bytes     | user_service
 time_service |             6 | 0 bytes     | time_service
 ping_service |             7 | 0 bytes     | ping_service
(3 rows)
```

## Create tables for the sample services

You can now connect to the elastic cluster for every microservice. In the following example, the elastic cluster database is named **Citus**. From the psql session, you can use the \c command to swap to another user.

```psql
\c citus user_service
```

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);
```

```psql
\c citus time_service
```

```sql
CREATE TABLE query_details (
    id SERIAL PRIMARY KEY,
    ip_address INET NOT NULL,
    query_time TIMESTAMP NOT NULL
);
```

```psql
\c citus ping_service
```

```sql
CREATE TABLE ping_results (
    id SERIAL PRIMARY KEY,
    host VARCHAR(255) NOT NULL,
    result TEXT NOT NULL
);
```

## Configure services

In this tutorial, we use a simple set of services. You can obtain them by cloning this public repository:

```bash
git clone https://github.com/citusdata/citus-example-microservices.git
```

```psql
$ tree
.
├── LICENSE
├── README.md
├── ping
│   ├── app.py
│   ├── ping.sql
│   └── requirements.txt
├── time
│   ├── app.py
│   ├── requirements.txt
│   └── time.sql
└── user
    ├── app.py
    ├── requirements.txt
    └── user.sql
```

Before you run the services however, edit `user/app.py`, `ping/app.py`, and `time/app.py` files providing the [connection configuration](https://www.psycopg.org/docs/module.html#psycopg2.connect) for your elastic cluster:

```python
# Database configuration
db_config = {
    'host': 'EXAMPLE.postgres.database.azure.com',
    'database': 'postgres',
    'password': 'SECRET',
    'user': 'ping_service',
    'port': 5432
}
```

After making the changes, save all modified files and move on to the next step of running the services.

## Run services

Change into every app directory and run them in their own python env.

```bash
cd user
pipenv install
pipenv shell
python app.py
```

Repeat the commands for time and ping service, after which you can use the API.

Create some users:

```bash
curl -X POST -H "Content-Type: application/json" -d '[
  {"name": "John Doe", "email": "john@example.com"},
  {"name": "Jane Smith", "email": "jane@example.com"},
  {"name": "Mike Johnson", "email": "mike@example.com"},
  {"name": "Emily Davis", "email": "emily@example.com"},
  {"name": "David Wilson", "email": "david@example.com"},
  {"name": "Sarah Thompson", "email": "sarah@example.com"},
  {"name": "Alex Miller", "email": "alex@example.com"},
  {"name": "Olivia Anderson", "email": "olivia@example.com"},
  {"name": "Daniel Martin", "email": "daniel@example.com"},
  {"name": "Sophia White", "email": "sophia@example.com"}
]' http://localhost:5000/users
```

List the created users:

```bash
curl http://localhost:5000/users
```

Get current time:

```bash
Get current time:
```

Run the ping against example.com:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"host": "example.com"}' http://localhost:5002/ping
```

## Explore the database

Now that you called some API functions, data is stored and you can check if `citus_schemas` reflects what is expected:

```sql
SELECT * FROM citus_schemas;
```

```output
 schema_name | colocation_id | schema_size | schema_owner
-------------+---------------+-------------+--------------
 user_service |             1 | 112 kB      | user_service
 time_service |             2 | 32 kB       | time_service
 ping_service |             3 | 32 kB       | ping_service
(3 rows)
```

When you created the schemas, you didn't indicate on which machines to create the schemas. It was done automatically. You can see where each schema resides with the following query:

```sql
  SELECT nodename,nodeport, table_name, pg_size_pretty(sum(shard_size))
  FROM citus_shards
  GROUP BY nodename,nodeport, table_name;
```

```output
nodename  | nodeport |         table_name         | pg_size_pretty
-----------+----------+---------------------------+----------------
 localhost |     7001 | time_service.query_details | 32 kB
 localhost |     7002 | user_service.users         | 112 kB
 localhost |     7002 | ping_service.ping_results  | 32 kB
```

For brevity of the example output on this page, instead of using `nodename` as an IP address we replace it with localhost. Assume that `localhost:7001` is node one and `localhost:7002` is node two.

You can see that the time service landed on node `localhost:7001` while the user and ping service share space on the second node `localhost:7002`. The example apps are simplistic, and the data sizes here are insignificant, but let's assume that you're affected by the uneven storage space utilization between the nodes. It would make more sense to have the two smaller time and ping services reside on one node while the large user service resides on its own node.

You can easily rebalance the cluster by disk size:

```sql
SELECT citus_rebalance_start();
```

```output
NOTICE:  Scheduled 1 moves as job 1
DETAIL:  Rebalance scheduled as background job
HINT:  To monitor progress, run: SELECT * FROM citus_rebalance_status();
 citus_rebalance_start
-----------------------
                     1
(1 row)
```

When done, you can check how our new layout looks:

```sql
  SELECT nodename,nodeport, table_name, pg_size_pretty(sum(shard_size))
  FROM citus_shards
  GROUP BY nodename,nodeport, table_name;
```

```output
 nodename  | nodeport |         table_name        | pg_size_pretty
-----------+----------+---------------------------+----------------
 localhost |     7001 | time_service.query_details | 32 kB
 localhost |     7001 | ping_service.ping_results  | 32 kB
 localhost |     7002 | user_service.users         | 112 kB
(3 rows)
```

According to expectations, the schemas are moved and we have a more balanced cluster. This operation is transparent for the applications. You don't even need to restart them, they continue serving queries.

## Next step

> [!div class="nextstepaction"]
> [Learn more about elastic clusters](../elastic-clusters/concepts-elastic-clusters.md)
