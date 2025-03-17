---
title: 'Tutorial: Design for microservices with elastic clusters'
description: This tutorial shows how to design for microservices with elastic clusters on Azure Database for PostgreSQL.
author: mulander
ms.author: adamwolk
ms.date: 02/28/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: tutorial
#customer intent: As a user, I want to learn how to use elastic clusters on Azure Database for PostgreSQL flexible server when deploying applications using the microservices architecture.
---

# Tutorial: Design for microservices with elastic clusters (preview)

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

In this tutorial, you use Azure Database for PostgreSQL as the storage backend for multiple microservices, demonstrating a sample setup and basic operation of such a cluster. Learn how to:

> [!div class="checklist"]
> * Prerequisites
> * Create roles for your microservices
> * Use psql utility to create roles and distributed schemas
> * Create tables for the sample services
> * Configure services
> * Run services
> * Explore the database


## Prerequisites

Create an elastic cluster in one of the following ways:
- [Create an elastic cluster with ARM template]()
- [Create an elastic cluster using CLI]()
- [Create an elastic cluster using the Portal]()

## Create roles for your microservices

Distributed schemas are relocatable within an elastic cluster. The system can rebalance them as a whole unit across the available nodes, allowing to efficiently share resources without manual allocation.

By design, microservices own their storage layer, we don’t make any assumptions on the type of tables and data that they create and store. We provide a schema for every service and assume that they use a distinct ROLE to connect to the database. When a user connects, their role name is put at the beginning of the search_path, so if the role matches with the schema name you don’t need any application changes to set the correct search_path.

We use three services in our example:

* user
* time
* ping

You can now create the database roles for every service:

```postgresql
CREATE USER user_service;
CREATE USER time_service;
CREATE USER ping_service;
```

## Use psql utility to create distributed schemas

Once connected to the elastic cluster using psql, you can complete some basic tasks.

There are two ways in which a schema can be distributed:

Manually by calling `citus_schema_distribute(schema_name)` function:

```postgresql
CREATE SCHEMA AUTHORIZATION userservice;
CREATE SCHEMA AUTHORIZATION timeservice;
CREATE SCHEMA AUTHORIZATION pingservice;

SELECT citus_schema_distribute('userservice');
SELECT citus_schema_distribute('timeservice');
SELECT citus_schema_distribute('pingservice');
```

This method also allows you to convert existing regular schemas into distributed schemas.

> [!NOTE]
>
> You can only distribute schemas that don't contain distributed and reference tables.

Alternative approach is to enable citus.enable_schema_based_sharding configuration variable:

```postgresql
SET citus.enable_schema_based_sharding TO ON;

CREATE SCHEMA AUTHORIZATION userservice;
CREATE SCHEMA AUTHORIZATION timeservice;
CREATE SCHEMA AUTHORIZATION pingservice;
```

The variable can be changed for the current session or permanently in coordinator node parameters. With the parameter set to ON, all created schemas are distributed by default.

You can list the currently distributed schemas by running:

```postgresql
select * from citus_schemas;
```

```plaintext
 schema_name | colocation_id | schema_size | schema_owner
-------------+---------------+-------------+--------------
 userservice |             5 | 0 bytes     | userservice
 timeservice |             6 | 0 bytes     | timeservice
 pingservice |             7 | 0 bytes     | pingservice
(3 rows)
```

## Create tables for the sample services

You now need to connect to the elastic cluster for every microservice. You can use the \c command to swap the user within an existing psql instance.

```plaintext
\c citus userservice
```

```postgresql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);
```

```plaintext
\c citus timeservice
```

```postgresql
CREATE TABLE query_details (
    id SERIAL PRIMARY KEY,
    ip_address INET NOT NULL,
    query_time TIMESTAMP NOT NULL
);
```

```plaintext
\c citus pingservice
```

```postgresql
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

```plaintext
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
    'user': 'pingservice',
    'port': 5432
}
```

After making the changes, save all modified files and move on to the next step of running the services.

## Run services

Change into every app directory and run them in their own python env.

```postgresql
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

```postgresql
select * from citus_schemas;
```

```plaintext
 schema_name | colocation_id | schema_size | schema_owner
-------------+---------------+-------------+--------------
 userservice |             1 | 112 kB      | userservice
 timeservice |             2 | 32 kB       | timeservice
 pingservice |             3 | 32 kB       | pingservice
(3 rows)
```

When you created the schemas, you didn’t indicate on which machines to create the schemas. It was done automatically. You can see where each schema resides with the following query:

```postgresql
  select nodename,nodeport, table_name, pg_size_pretty(sum(shard_size))
    from citus_shards
group by nodename,nodeport, table_name;
```

```plaintext
nodename  | nodeport |         table_name         | pg_size_pretty
-----------+----------+---------------------------+----------------
 localhost |     7001 | timeservice.query_details | 32 kB
 localhost |     7002 | userservice.users         | 112 kB
 localhost |     7002 | pingservice.ping_results  | 32 kB
```

For brevity of the example output on this page, instead of using `nodename` as an IP address we replace it with localhost. Assume that `localhost:7001` is node one and `localhost:7002` is node two.


You can see that the time service landed on node `localhost:7001` while the user and ping service share space on the second node `localhost:7002`. The example apps are simplistic, and the data sizes here are ignorable, but let’s assume that you're annoyed by the uneven storage space utilization between the nodes. It would make more sense to have the two smaller time and ping services reside on one machine while the large user service resides alone.

You can easily rebalance the cluster by disk size:

```postgresql
select citus_rebalance_start();
```

```plaintext
NOTICE:  Scheduled 1 moves as job 1
DETAIL:  Rebalance scheduled as background job
HINT:  To monitor progress, run: SELECT * FROM citus_rebalance_status();
 citus_rebalance_start
-----------------------
                     1
(1 row)
```

When done, you can check how our new layout looks:

```postgresql
  select nodename,nodeport, table_name, pg_size_pretty(sum(shard_size))
    from citus_shards
group by nodename,nodeport, table_name;
```

```plaintext
 nodename  | nodeport |         table_name        | pg_size_pretty
-----------+----------+---------------------------+----------------
 localhost |     7001 | timeservice.query_details | 32 kB
 localhost |     7001 | pingservice.ping_results  | 32 kB
 localhost |     7002 | userservice.users         | 112 kB
(3 rows)
```

According to expectations, the schemas are moved and we have a more balanced cluster. This operation is transparent for the applications. You don’t even need to restart them, they continue serving queries.


## Next step

In this tutorial, you learned how to create distributed schemas, ran microservices using them as storage. You also learned how to explore and manage schema-based sharded elastic clusters on Azure Database for PostgreSQL.

> [!div class="nextstepaction"]
> [Learn more about elastic clusters](concepts-elastic-clusters.md)
