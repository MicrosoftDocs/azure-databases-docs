---
title: "Tutorial: Design Multitenant Database with Elastic Clusters"
description: Learn how to design a scalable multitenant application with Azure Database for PostgreSQL elastic clusters.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 11/05/2025
ms.service: azure-database-postgresql
ms.topic: tutorial
---

# Tutorial: Design a multitenant database with elastic clusters

In this tutorial, you use Azure Database for PostgreSQL with elastic clusters to learn how to design a multitenant application that benefits from horizontal scale-out.

> [!div class="checklist"]
> - Prerequisites
> - Use psql utility to create a schema
> - Shard tables across nodes
> - Ingest sample data
> - Query tenant data
> - Share data between tenants
> - Customize the schema per-tenant

## Prerequisites

Create an elastic cluster in one of the following ways:
- [Create an elastic cluster using the Portal](../elastic-clusters/quickstart-create-elastic-cluster-portal.md)
- [Create an elastic cluster using Bicep](../elastic-clusters/quickstart-create-elastic-cluster-bicep.md)
- [Create an elastic cluster with ARM template](../elastic-clusters/quickstart-create-elastic-cluster-arm-template.md)

## Use psql utility to create a schema

After you connect to the elastic cluster by using psql, you can configure your elastic cluster. This tutorial walks you through creating an application platform that allows companies to track their ad campaigns.

> [!NOTE]
> When distributing data across your cluster, any unique data constraints are scoped to their distribution "shard". In our multitenant example, application data uniqueness is enforced per tenant (for example, company ID). For this reason, our distributed table definitions for primary and foreign key constraints always include the company ID column.

Create a table to hold your multitenant company information, and another table for their campaigns. In the psql console, run these commands:

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

Each campaign pays to run ads. Add your ads table in psql with the following code:

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

Finally, you want to track statistics based upon ad selects and impressions:

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

Up until this point, you created standard Postgres tables, but you ultimately need to create distributed tables across your elastic cluster. Distributed tables within an elastic cluster store data on different nodes based upon the values defined by your distribution column. This column is used to determine row placement across the underlying worker nodes.

Set up your distribution column to be company_id, which acts as your multitenant identifier. In psql, run these functions:

```sql
SELECT create_distributed_table('companies',   'id');
SELECT create_distributed_table('campaigns',   'company_id');
SELECT create_distributed_table('ads',         'company_id');
SELECT create_distributed_table('clicks',      'company_id');
SELECT create_distributed_table('impressions', 'company_id');
```

> [!NOTE]  
> To take advantage of elastic clusters with Azure Database for PostgreSQL performance features, you need to distribute tables. Unless you distribute your tables and schemas, your cluster nodes don't participate in any distributed queries or operations.

## Ingest sample data

Outside of psql, in the normal command line, download sample data sets:

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

Until now, you distributed all your tables across your cluster by `company_id`. However, some types of data naturally "belong" to all tenants and can be placed alongside all tenant distributions. For instance, all companies in your ad platform might want to get geographical information for their audience based on the IP address details.

Create a reference table to hold this geographic IP information. Run the following commands in psql:

```sql
CREATE TABLE geo_ips (
  addrs cidr NOT NULL PRIMARY KEY,
  latlon point NOT NULL
    CHECK (-90  <= latlon[0] AND latlon[0] <= 90 AND
           -180 <= latlon[1] AND latlon[1] <= 180)
);
CREATE INDEX ON geo_ips USING gist (addrs inet_ops);
```

Next, identify `geo_ips` as a "reference table". Your cluster manages this table by storing a synchronized table on every clustered worker node.

```sql
SELECT create_reference_table('geo_ips');
```

Now, load your reference table with your sample data. Remember to run this command from the directory where you downloaded the dataset file.

```sql
\copy geo_ips from 'geo_ips.csv' with csv
```

SQL statements that join the selected table with `geo_ips` are now efficient on all nodes. Notice this join to find the locations of every IP that selected on ad 290. Try running the query in psql:

```sql
SELECT c.id, clicked_at, latlon
  FROM geo_ips, clicks c
 WHERE addrs >> c.user_ip
   AND c.company_id = 5
   AND c.ad_id = 290;
```

## Customize the schema per tenant

In some instances, your individual tenants might need to store special information that other tenants don't need. However, all tenants share a common definition with an identical database schema. Where can you put the extra data?

One solution is to use a flexible column type like PostgreSQL's JSONB. Our schema has a JSONB field in `clicks` called `user_data`. A company (say company 5) can use this column to track information about whether a user is on a mobile device.

Here's a query company 5 can use to find who selects more: mobile or traditional visitors.

```sql
SELECT
  user_data->>'is_mobile' AS is_mobile,
  count(*) AS count
FROM clicks
WHERE company_id = 5
GROUP BY user_data->>'is_mobile'
ORDER BY count DESC;
```

PostgreSQL includes a powerful feature that allows you to index a specific portion or subset of your data. You can further optimize your query for company 5 by creating a [partial index](https://www.postgresql.org/docs/current/static/indexes-partial.html).

```sql
CREATE INDEX click_user_data_is_mobile
ON clicks ((user_data->>'is_mobile'))
WHERE company_id = 5;
```

Additionally, another way to improve performance across queries that include your JSONB column is to create a [GIN index](https://www.postgresql.org/docs/16/gin-intro.html) on every underlying key and value within your JSONB column.

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

> [!div class="nextstepaction"]
> [Learn more about elastic clusters](../elastic-clusters/concepts-elastic-clusters.md)
