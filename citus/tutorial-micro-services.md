---
title: Microservices
description: This article describes Microservices.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: tutorial
monikerRange: "citus-13 || citus-14"
---

# Citus microservices tutorial

In this tutorial, you use Citus as the storage backend for multiple microservices. The tutorial demonstrates a sample setup and basic operation of such a cluster.

> [!NOTE]  
> This tutorial assumes that you have Citus installed and running. If you don't have Citus running, you can set up Citus locally by using one of the options from [Getting Started](getting-started.md).

## Distributed schemas

Distributed schemas are relocatable within a Citus cluster. The system can rebalance them as a whole unit across the available nodes, allowing to efficiently share resources without manual allocation.

By design, microservices own their storage layer. We don't assume the type of tables and data that they create and store. We provide a schema for every service and assume that they use a distinct ROLE to connect to the database. When a user connects, their role name is put at the beginning of the search_path, so if the role matches with the schema name you don't need any application changes to set the correct search_path.

We use three services in our example:

- user service
- time service
- ping service

To start, connect to the Citus coordinator by using psql.

**If you are using native PostgreSQL**, as installed in [Getting Started](getting-started.md), the coordinator node is running on port 9700.

```bash
psql -p 9700
```

**If you use Docker**, you can connect by running psql with the docker exec command:

```bash
docker exec -it citus psql -U postgres
```

Create the database roles for every service:

```sql
CREATE USER user_service;
CREATE USER time_service;
CREATE USER ping_service;
```

You can distribute a schema in Citus in two ways:

Manually by calling citus_schema_distribute(schema_name) function:

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

Alternatively, enable citus.enable_schema_based_sharding configuration variable:

```sql
SET citus.enable_schema_based_sharding TO ON;

CREATE SCHEMA AUTHORIZATION user_service;
CREATE SCHEMA AUTHORIZATION time_service;
CREATE SCHEMA AUTHORIZATION ping_service;
```

You can change the variable for the current session or permanently in postgresql.conf. When you set the parameter to ON, all created schemas are distributed by default.

You can list the currently distributed schemas:

```sql
select * from citus_schemas;
```

```output
schema_name  | colocation_id | schema_size | schema_owner
--------------+---------------+-------------+--------------
user_service |             5 | 0 bytes     | user_service
time_service |             6 | 0 bytes     | time_service
ping_service |             7 | 0 bytes     | ping_service
(3 rows)
```

## Creating tables

You need to connect to the Citus coordinator for every microservice. Use the c command to swap the user within an existing psql instance.

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

For this tutorial, we use services that you can obtain by cloning this public repository:

```git clone https://github.com/citusdata/citus-example-microservices.git```
The repository contains the ping, time, and user service. All of them have an app.py that we run.
```python

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
Before you run the services, edit the user/app.py, ping/app.py, and time/app.py files to provide the [connection configuration](https://www.psycopg.org/docs/module.html#psycopg2.connect) for your Citus cluster:
``` python

# Database configuration

db_config = {
    'host': 'localhost',
    'database': 'citus',
    'user': 'ping_service',
    'port': 9700
}

```
After making the changes, save all modified files and move on to the next step of running the services.

## Running the services

Change into each app directory and run the apps in their own Python environment.
```bash

cd user
pipenv install
pipenv shell
python app.py

```
Repeat the preceding steps for the time and ping services. When you finish, you can use the API.

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
Get the current time:
```bash

curl http://localhost:5001/current_time

```
Run the ping against example.com:
```bash

curl -X POST -H "Content-Type: application/json" -d '{"host": "example.com"}' http://localhost:5002/ping

```
## Exploring the database

After calling some API functions, the system stores data. You can check if the citus_schemas table reflects what you expect:
```sql

select * from citus_schemas;

```
```output

schema_name | colocation_id | schema_size | schema_owner
--------------+---------------+-------------+--------------
user_service |             1 | 112 kB      | user_service
time_service |             2 | 32 kB       | time_service
ping_service |             3 | 32 kB       | ping_service
(3 rows)

```
When you create the schemas, you don't specify which machines to use. Citus automatically chooses the machines. You can see where each schema resides with the following query:
```sql

select nodename,nodeport, table_name, pg_size_pretty(sum(shard_size))
  from citus_shards
group by nodename,nodeport, table_name;

```
```output

nodename | nodeport |         table_name         | pg_size_pretty
-----------+----------+----------------------------+----------------
localhost |     9701 | time_service.query_details | 32 kB
localhost |     9702 | user_service.users         | 112 kB
localhost |     9702 | ping_service.ping_results | 32 kB

```
We can see that the time service landed on node localhost:9701 while the user and ping service share space on the second worker localhost:9702. This is a toy example, and the data sizes here are ignorable, but let's assume that we're annoyed by the uneven storage space utilization between the nodes. It would make more sense to have the two smaller time and ping services reside on one machine while the large user service resides alone.

You can fix this issue by asking Citus to rebalance the cluster by disk size:
```sql

select citus_rebalance_start();

```
```output

NOTICE: Scheduled 1 moves as job 1
DETAIL: Rebalance scheduled as background job
HINT: To monitor progress, run: SELECT * FROM citus_rebalance_status();
citus_rebalance_start
-----------------------
                     1
(1 row)

```
When the operation completes, you can check how the new layout looks:
```sql

select nodename,nodeport, table_name, pg_size_pretty(sum(shard_size))
  from citus_shards
group by nodename,nodeport, table_name;

```
```output

nodename | nodeport |         table_name         | pg_size_pretty
-----------+----------+----------------------------+----------------
localhost |     9701 | time_service.query_details | 32 kB
localhost |     9701 | ping_service.ping_results | 32 kB
localhost |     9702 | user_service.users         | 112 kB
(3 rows)

```
According to our expectations, the schemas are moved and we have a more balanced cluster. This operation is transparent for the applications. We don't even need to restart them, and they continue serving queries.

By completing this tutorial, you reached the end of using Citus as storage for microservices.

## Related content

- [Multitenant applications tutorial](tutorial-multi-tenant.md)
- [What is Citus?](what-is-citus.md)
