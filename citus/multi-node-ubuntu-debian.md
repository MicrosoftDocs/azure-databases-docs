---
title: Multi-Node Citus Clusters on Ubuntu or Debian
description: Learn how to install multi-node Citus on Debian or Ubuntu so you can build a distributed PostgreSQL cluster.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: how-to
monikerRange: "citus-13 || citus-14"
---

# Multi-node Citus clusters on Ubuntu or Debian

This article describes the steps needed to set up a multi-node Citus cluster on your own Linux machines by using deb packages.

## Configure all nodes

### 1. Add repository

```bash
# Add Citus repository for package manager
curl https://install.citusdata.com/community/deb.sh | sudo bash
```

### 2. Install PostgreSQL + Citus and initialize a database

```bash
# install the server and initialize db
sudo apt-get -y install postgresql-17-citus-13.0

# preload citus extension
sudo pg_conftool 17 main set shared_preload_libraries citus
```

This process installs a centralized configuration in `/etc/postgresql/17/main`, and creates a database in `/var/lib/postgresql/17/main`.

### 3. Configure connection and authentication

Before you start the database, change its access permissions. By default the database server listens only to clients on localhost. As a part of this step, instruct it to listen on all IP interfaces, and then configure the client authentication file to allow all incoming connections from the local network.

```bash
sudo pg_conftool 17 main set listen_addresses '*'
```

```bash
sudo vi /etc/postgresql/17/main/pg_hba.conf
```

```bash
# Allow unrestricted access to nodes in the local network. The following ranges
# correspond to 24, 20, and 16-bit blocks in Private IPv4 address spaces.
host    all             all             10.0.0.0/8              trust

# Also allow the host unrestricted access to connect to itself
host    all             all             127.0.0.1/32            trust
host    all             all             ::1/128                 trust
```

> [!NOTE]  
> Your DNS settings might differ. Also, these settings are too permissive for some environments. For more information, see [Increasing worker security](cluster-management.md#increasing-worker-security). The PostgreSQL manual [explains how](http://www.postgresql.org/docs/current/static/auth-pg-hba-conf.html) to make them more restrictive.

## 4. Start database servers, create Citus extension

```bash
# start the db server
sudo service postgresql restart
# and make it start automatically when computer does
sudo update-rc.d postgresql enable
```

You must add the Citus extension to **every database** you would like to use in a cluster. The following example adds the extension to the default database named `postgres`.

```bash
# add the citus extension
sudo -i -u postgres psql -c "CREATE EXTENSION citus;"
```

## Configure the coordinator node

The following steps must be completed **only** on the coordinator node after the previously mentioned steps are completed.

### 1. Add worker node information

Inform the coordinator about its workers. To add this information, call a UDF, which adds the node information to the pg_dist_node catalog table. For our example, assume that there are two workers (named worker-101, worker-102). Add the workers' DNS names (or IP addresses) and server ports to the table.

```bash
# Register the hostname that future workers will use to connect
# to the coordinator node.
#
# You'll need to change the example, 'coord.example.com',
# to match the actual hostname

sudo -i -u postgres psql -c \
  "SELECT citus_set_coordinator_host('coord.example.com', 5432);"

# Add the worker nodes.
#
# Similarly, you'll need to change 'worker-101' and 'worker-102' to the
# actual hostnames

sudo -i -u postgres psql -c "SELECT * from citus_add_node('worker-101', 5432);"
sudo -i -u postgres psql -c "SELECT * from citus_add_node('worker-102', 5432);"
```

### 2. Verify that installation succeeded

To verify that the installation succeeded, check that the coordinator node picked up the desired worker configuration. This command, when run in the psql shell, should output the worker nodes added to the pg_dist_node table.

```bash
sudo -i -u postgres psql -c "SELECT * FROM citus_get_active_worker_nodes();"
```

## Ready to use Citus

After you complete the installation process, you're ready to use your Citus cluster. The new Citus database is accessible in psql through the postgres user:

```bash
sudo -i -u postgres psql
```

## Related content

- [Multi-node overview](multi-node.md)
