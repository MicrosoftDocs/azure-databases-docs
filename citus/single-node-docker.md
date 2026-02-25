---
title: "Docker (Mac or Linux)"
description: Learn how to run Citus using Docker on Mac or Linux so you can quickly test distributed PostgreSQL features.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: how-to
monikerRange: "citus-13 || citus-14"
---

# Docker (Mac or Linux)

> [!NOTE]  
> **The Docker image is intended for development/testing purposes only**, and isn't prepared for production use.

You can start Citus in Docker with one command:

```bash
# start the image
docker run -d --name citus -p 5432:5432 -e POSTGRES_PASSWORD=mypass \
           citusdata/citus:13.0

# verify it's running, and that Citus is installed:
psql -U postgres -h localhost -d postgres -c "SELECT * FROM citus_version();"
```

You should see the latest version of Citus.

Once you have the cluster up and running, you can visit our tutorials on multitenant applications or real-time analytics to get started with Citus in minutes.

> [!NOTE]  
> If you already have PostgreSQL running on your machine, you might encounter this error when starting the Docker containers:
>
> ```output
> Error starting userland proxy:
> Bind for 0.0.0.0:5432: unexpected error address already in use
> ```
>
> This error occurs when the Citus image attempts to bind to the standard PostgreSQL port 5432. To fix this error, choose a different port with the -p option. You need to also use the new port in the psql command.

## Related content

- [Single-node overview](single-node.md)
- [Single-node on Ubuntu or Debian](single-node-debian.md)
- [Single-node on Fedora, CentOS, or Red Hat](single-node-rhel.md)
