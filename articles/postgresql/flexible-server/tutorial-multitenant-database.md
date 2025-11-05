---
title: 'Tutorial: Design multitenant database with elastic clusters'
description: Learn how to design a scalable multitenant application with Azure Database for PostgreSQL elastic clusters.
author: mulander
ms.author: adamwolk
ms.reviewer: maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: tutorial
#Customer intent: As an developer, I want to design a PostgreSQL database and scale it out using elastic clusters so that my multi-tenant application runs efficiently for all tenants.
---

# Tutorial: Design a multitenant database with elastic clusters

In this tutorial, we will use Azure Database for PostgreSQL with elastic clusters to learn how to design a multi-tenant application which benefits from horizontal scale-out.

> [!div class="checklist"]
> * Prerequisites
> * Use psql utility to create a schema
> * Shard tables across nodes
> * Ingest sample data
> * Query tenant data
> * Share data between tenants
> * Customize the schema per-tenant

## Prerequisites

Create an elastic cluster in one of the following ways:
- [Create an elastic cluster using the Portal](quickstart-create-elastic-cluster-portal.md)
- [Create an elastic cluster using Bicep](quickstart-create-elastic-cluster-bicep.md)
- [Create an elastic cluster with ARM template](quickstart-create-elastic-cluster-arm-template.md)

## Use psql utility to create a schema

Once connected to the elastic cluster using psql, you can configure your elastic cluster. This tutorial walks you through creating an application platform that allows companies to track their ad campaigns.

> [!NOTE]
>
> When distributing data across your cluster, any unique data contraints are scoped to their distribution "shard". In our multi-tenant example,  application data uniqueness is enforced per tenant (e.g. company ID).  For this reason, our distributed table definitions for primary and foreign key constraints always include the company ID column.

Let's create a table to hold our multi-tenant company information, and another table for their campaigns. In the psql console, run these commands:

```sql
CREATE TABLE companies (
  id bigserial PRIMARY KEY,
  name text NOT NULL,
  image_url text,
  created_at timestamp without time zone NOT NULL,
  updated_at timestamp without time zone NOT NULL
);

CREATE TABLE campaigns (
  id bigserial,
  company_id bigint REFERENCES companies (id),
  name text NOT NULL,
  cost_model text NOT NULL,
  state text NOT NULL,
  monthly_budget bigint,
  blocked_site_urls text[],
  created_at timestamp without time zone NOT NULL,
  updated_at timestamp without time zone NOT NULL,

  PRIMARY KEY (company_id, id)
);
```

Each campaign pays to run ads. Let's add our ads table in psql with the following code:

```sql
CREATE TABLE ads (
  id bigserial,
  company_id bigint,
  campaign_id bigint,
  name text NOT NULL,
  image_url text,
  target_url text,
  impressions_count bigint DEFAULT 0,
  clicks_count bigint DEFAULT 0,
  created_at timestamp without time zone NOT NULL,
  updated_at timestamp without time zone NOT NULL,

  PRIMARY KEY (company_id, id),
  FOREIGN KEY (company_id, campaign_id)
    REFERENCES campaigns (company_id, id)
);
```

Finally, we want to track statistics based upon ad clicks and impressions:

```sql
CREATE TABLE clicks (
  id bigserial,
  company_id bigint,
  ad_id bigint,
  clicked_at timestamp without time zone NOT NULL,
  site_url text NOT NULL,
  cost_per_click_usd numeric(20,10),
  user_ip inet NOT NULL,
  user_data jsonb NOT NULL,

  PRIMARY KEY (company_id, id),
  FOREIGN KEY (company_id, ad_id)
    REFERENCES ads (company_id, id)
);

CREATE TABLE impressions (
  id bigserial,
  company_id bigint,
  ad_id bigint,
  seen_at timestamp without time zone NOT NULL,
  site_url text NOT NULL,
  cost_per_impression_usd numeric(20,10),
  user_ip inet NOT NULL,
  user_data jsonb NOT NULL,

  PRIMARY KEY (company_id, id),
  FOREIGN KEY (company_id, ad_id)
    REFERENCES ads (company_id, id)
);
```

You can now see the newly created tables from psql by running:

```postgres
\dt
```

## Shard tables across nodes
Up until this point, we have created standard Postgres tables, but we ultimately need to create distributed tables acroos our elastic cluster.  Distributed tables within an elastic cluster store data on different nodes based upon the values defined by our "distribution column". This column is used to determine row placement across the underlying worker nodes.

Let's set up our distribution column to be company_id, which will act as our multi-tenant identifier. In psql, run these functions:

```sql
SELECT create_distributed_table('companies',   'id');
SELECT create_distributed_table('campaigns',   'company_id');
SELECT create_distributed_table('ads',         'company_id');
SELECT create_distributed_table('clicks',      'company_id');
SELECT create_distributed_table('impressions', 'company_id');
```

> [!NOTE]
>
> Distributing tables is necessary to take advantage of elastic clusters of Azure Database for PostgreSQL performance features. Unless you distribute your tables and/or schemas, your cluster nodes will not participate in any distributed queries or operations.

## Ingest sample data

Outside of psql now, in the normal command line, download sample data sets:

```bash
for dataset in companies campaigns ads clicks impressions geo_ips; do
  curl -O https://raw.githubusercontent.com/Azure-Samples/azure-postgresql-elastic-clusters/main/multi-tenant/${dataset}.csv
done
```

Back inside psql, bulk load the data. Be sure to run psql in the same directory where you downloaded the data files.

```sql
SET client_encoding TO 'UTF8';

\copy companies from 'companies.csv' with csv
\copy campaigns from 'campaigns.csv' with csv
\copy ads from 'ads.csv' with csv
\copy clicks from 'clicks.csv' with csv
\copy impressions from 'impressions.csv' with csv
```

Your data within your distributed tables is now spread across your elastic cluster worker nodes.

## Query tenant data

When your application requests data for a specific company, the database can now efficiently execute the query on the appropriate worker node. For example, the following query (`company_id = 5`) filters down ads and impressions. Try running it in psql to see the results.

```sql
SELECT a.campaign_id,
       RANK() OVER (
         PARTITION BY a.campaign_id
         ORDER BY a.campaign_id, count(*) DESC
       ), count(*) AS n_impressions, a.id
  FROM ads AS a
  JOIN impressions AS i
    ON i.company_id = a.company_id
   AND i.ad_id      = a.id
 WHERE a.company_id = 5
GROUP BY a.campaign_id, a.id
ORDER BY a.campaign_id, n_impressions DESC;
```

## Share data between tenants

Until now, all our tables have been distributed across our cluster by `company_id`. However, some types of data naturally "belong" to all tenants, and can be placed alongside all tenant distributions. For instance, all companies in our ad platform might want to get geographical information for their audience based on the IP address details.

Let's create a reference table to hold this geographic IP information. Run the following commands in psql:

```sql
CREATE TABLE geo_ips (
  addrs cidr NOT NULL PRIMARY KEY,
  latlon point NOT NULL
    CHECK (-90  <= latlon[0] AND latlon[0] <= 90 AND
           -180 <= latlon[1] AND latlon[1] <= 180)
);
CREATE INDEX ON geo_ips USING gist (addrs inet_ops);
```

Next, let's identify `geo_ips` as a "reference table", which our cluster will manage by storing a synchronized table on every clustered worker node.

```sql
SELECT create_reference_table('geo_ips');
```

Now, let's load our reference table with our sample data. Remember to run this command from the directory where you downloaded the dataset file.

```sql
\copy geo_ips from 'geo_ips.csv' with csv
```

SQL statements which join the clicks table with geo_ips are now efficient on any and all nodes. Notice this join to find the locations of every IP that clicked on ad 290. Try running the query in psql:

```sql
SELECT c.id, clicked_at, latlon
  FROM geo_ips, clicks c
 WHERE addrs >> c.user_ip
   AND c.company_id = 5
   AND c.ad_id = 290;
```

## Customize the schema per-tenant

In some instances, your individual tenants might need to store special information not needed by others. However, all tenants share a common definition with an identical database schema. Where can the extra data go?

One solution is to use a flexible column type like PostgreSQL's JSONB. Our schema has a JSONB field in `clicks` called `user_data`. A company (say company 5), can use this column to track information about whether a user is on a mobile device.

Here's a query company 5 can use to find who clicks more: mobile, or traditional visitors.

```sql
SELECT
  user_data->>'is_mobile' AS is_mobile,
  count(*) AS count
FROM clicks
WHERE company_id = 5
GROUP BY user_data->>'is_mobile'
ORDER BY count DESC;
```

PostgreSQL includes a powerful feature which allows us to index a specific portion or subset of our data.  We can further optimize our query for company 5 by creating a [partial index](https://www.postgresql.org/docs/current/static/indexes-partial.html).

```sql
CREATE INDEX click_user_data_is_mobile
ON clicks ((user_data->>'is_mobile'))
WHERE company_id = 5;
```

Additionally, another way to improve performance across queries including our JSONB column is to create a [GIN index](https://www.postgresql.org/docs/16/gin-intro.html) on every underling key and value within our JSONB column.

```sql
CREATE INDEX click_user_data
ON clicks USING gin (user_data);

-- this speeds up queries like, "which clicks have the is_mobile key present in user_data?"

SELECT id
  FROM clicks
 WHERE user_data ? 'is_mobile'
   AND company_id = 5;
```

## Next step

In this tutorial, we learned how to create an elastic cluster. We connected to our elastic cluster using psql, created a schema, and distributed our data. We learned to index and query data both within and between tenants, and to customize the schema per tenant.

> [!div class="nextstepaction"]
> [Learn more about elastic clusters](concepts-elastic-clusters.md)