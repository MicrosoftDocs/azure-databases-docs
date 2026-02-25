---
title: Single-Node Citus Cluster on Fedora, CentOS, or Red Hat
description: Learn how to install single-node Citus on RHEL, CentOS, or Fedora so you can start using distributed PostgreSQL.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: how-to
monikerRange: "citus-13 || citus-14"
---

# Single-node Citus cluster on Fedora, CentOS, or Red Hat

This section describes the steps needed to set up a single-node Citus cluster on your own Linux machine from RPM packages.

## 1. Install PostgreSQL 17 and the Citus extension

```sh
# Add Citus repository for package manager
curl https://install.citusdata.com/community/rpm.sh | sudo bash

# install Citus extension
sudo yum install -y citus130_17
```

## 2. Initialize the Cluster

Let's create a new database on disk. For convenience with PostgreSQL Unix domain socket connections, use the postgres user.

```sh
# this user has access to sockets in /var/run/postgresql
sudo su - postgres

# include path to postgres binaries
export PATH=$PATH:/usr/pgsql-17/bin

cd ~
mkdir citus
initdb -D citus
```

Citus is a PostgreSQL extension. To tell PostgreSQL to use this extension, you need to add it to a configuration variable called `shared_preload_libraries`:

```sh
echo "shared_preload_libraries = 'citus'" >> citus/postgresql.conf
```

## 3. Start the database server

Finally, start an instance of PostgreSQL for the new directory:

```sh
pg_ctl -D citus -o "-p 9700" -l citus_logfile start
```

After you add Citus to `shared_preload_libraries`, Citus hooks into some deep parts of PostgreSQL, swapping out the query planner and executor. Here, you load the user-facing side of Citus such as the functions you call:

```sh
psql -p 9700 -c "CREATE EXTENSION citus;"
```

## 4. Verify that installation succeeded

Verify that the installation succeeded and Citus is installed:

```sh
psql -p 9700 -c "select citus_version();"
```

You should see details of the Citus extension.

After you complete the installation process, you're ready to use your Citus cluster. To help you get started, see [Multitenant applications](tutorial-multi-tenant.md). This tutorial has instructions on setting up a Citus cluster with sample data in minutes.

## Related content

- [Single-node overview](single-node.md)
- [Single-node on Ubuntu or Debian](single-node-debian.md)
- [Single-node on Docker](single-node-docker.md)
