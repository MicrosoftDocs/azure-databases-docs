---
title: "Create an Elastic Cluster in Azure Database for PostgreSQL Flexible Server"
description: Guide to create an elastic cluster in Azure Database for PostgreSQL.
#customer intent: As a user, I want to create an elastic cluster so that I can run a horizontally scalable PostgreSQL database.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: elastic-clusters
ms.topic: quickstart
---

# Create an elastic cluster in Azure Database for PostgreSQL flexible server

Azure Database for PostgreSQL with elastic cluster is a managed service that you use to run, manage, and scale highly available PostgreSQL databases in the cloud with horizontal scale-out capability. This quickstart covers how to create an elastic cluster.

If you don't have an Azure subscription, create a [free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

You create an elastic cluster, like a flexible server, with a configured set of [compute and storage resources](../compute-storage/concepts-compute.md). You create the cluster within an [Azure resource group](/azure/azure-resource-manager/management/overview). The steps outlined in [Create an Azure Database for PostgreSQL](../configure-maintain/quickstart-create-server.md) equally apply to elastic clusters. This section outlines the changes in the process.

## Steps to create an elastic cluster

### [Portal](#tab/portal-create-elastic-cluster)

Use the [Azure portal](https://portal.azure.com/#view/Microsoft_Azure_OSSDatabases/CreatePostgreSqlFlexibleServerFullBlade):

1. After filling out the basic information, select the **Configure server** link.

   :::image type="content" source="./media/create-elastic-cluster/1-elastic-clusters-create-cluster.png" alt-text="Screenshot of the Azure portal showing Compute + storage section and an actionable Configure server link." lightbox="./media/create-elastic-cluster/1-elastic-clusters-create-cluster.png":::

1. From the **Cluster** section, select the **Elastic cluster** option.

    :::image type="content" source="./media/create-elastic-cluster/2-elastic-clusters-create-cluster.png" alt-text="Screenshot of the top section of Compute + storage configuration page. Server is selected. Elastic cluster is cleared." lightbox="./media/create-elastic-cluster/2-elastic-clusters-create-cluster.png":::

1. Specify the node count and configure the compute size.

    :::image type="content" source="./media/create-elastic-cluster/3-elastic-clusters-create-cluster.png" alt-text="Screenshot of Compute + storage configuration with elastic clusters. Elastic cluster is selected. Node count input box has a value of 4. Compute tier and size options are visible." lightbox="./media/create-elastic-cluster/3-elastic-clusters-create-cluster.png":::

1. Save your changes and verify your choices on the main configuration page. To change the name of the default database on which the Citus extension is created, use the **Database name** text box. Then, select **Review + create** to review your selections.

    :::image type="content" source="./media/create-elastic-cluster/4-elastic-clusters-create-cluster.png" alt-text="Screenshot of main configuration page. The Compute + storage section has a new line Sharding Schema/Row and a line stating four nodes. Database name field is available to change the default database name from postgres to any other of your preference." lightbox="./media/create-elastic-cluster/4-elastic-clusters-create-cluster.png":::

1. Select **Create** to provision the server.

    :::image type="content" source="./media/create-elastic-cluster/5-elastic-clusters-create-cluster.png" alt-text="Screenshot showing the Review + create tab, where you can review details of the cluster before starting deployment." lightbox="./media/create-elastic-cluster/5-elastic-clusters-create-cluster.png":::

1. The deployment starts.

    :::image type="content" source="./media/create-elastic-cluster/6-elastic-clusters-create-cluster.png" alt-text="Screenshot showing the deployment in progress." lightbox="./media/create-elastic-cluster/6-elastic-clusters-create-cluster.png":::


1. When the deployment finishes, you can select **Pin to dashboard**. This action creates a tile for this server on your Azure portal dashboard as a shortcut to the server's **Overview** page. Selecting **Go to resource** opens the server's **Overview** page.

   :::image type="content" source="./media/create-elastic-cluster/7-elastic-clusters-create-cluster.png" alt-text="Screenshot showing the deployment completed." lightbox="./media/create-elastic-cluster/7-elastic-clusters-create-cluster.png":::

   By default, a **postgres** database is created under your server. You can change the name of this default database at cluster provisioning time only. The [postgres](https://www.postgresql.org/docs/current/static/app-initdb.html) database is a default database meant for users, utilities, and applications. (The other default database is **azure_maintenance**. Its function is to separate the managed service processes from user actions. You can't access this database.)

    > [!NOTE]
    > Connections to your Azure Database for PostgreSQL flexible server communicate over port 5432 and 6432 (PgBouncer). When you try to connect from within a corporate network, outbound traffic over port 5432 and 6432 might not be allowed by your network's firewall. If so, you can't connect to your server unless your IT department opens port 5432 and 6432. Elastic clusters also use port 7432 and 8432 (PgBouncer) for load balanced connections across the cluster nodes and might need to be allow listed in a similar way by your IT department.

### [CLI](#tab/cli-create-elastic-cluster)

Use the [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create) command to deploy an elastic cluster.

> [!NOTE]  
> Complete the following command with parameters and values that vary, depending on how you want to configure other features of the provisioned server.

To deploy the cluster with `postgres` as the database name, use the following command:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --location <location>
  --node-count <node_count>
```

To deploy the cluster with a database name other than `postgres`, use the following command:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --location <location>
  --node-count <node_count>
  --database-name <default_database_name> ...
```

---

## Get the connection information

When you create your elastic cluster instance, the portal creates a default database with the name you provide. To connect to your database server, you need your full server name and the credentials of the administrator. You noted those values earlier in the quickstart article. If you didn't, you can easily find the server name and authentication information on the server **Overview** page in the portal.

Open your server's **Overview** page. Make a note of the **Server name** and the **Administrator login**. Hover your cursor over each field, and the copy symbol appears to the right of the text. Select the copy symbol as needed to copy the values.

:::image type="content" source="./media/create-elastic-cluster/8-elastic-clusters-create-cluster.png" alt-text="Screenshot of the server Overview page." lightbox="./media/create-elastic-cluster/8-elastic-clusters-create-cluster.png":::

<a name="connect-to-the-postgresql-database-using-psql"></a>

## Connect to the Azure Database for PostgreSQL database by using psql

You can use many applications to connect to your Azure Database for PostgreSQL flexible server. If your client computer has PostgreSQL installed, you can use a local instance of [psql](https://www.postgresql.org/docs/current/static/app-psql.html) to connect to an Azure Database for PostgreSQL flexible server. Use the psql command-line utility to connect to the Azure Database for PostgreSQL flexible server.

1. Run the following psql command to connect to an Azure Database for PostgreSQL flexible server.

   ```bash
   psql --host=<servername> --port=<port> --username=<user> --dbname=<dbname>
   ```

   For example, the following command connects to the default database called **postgres** on your Azure Database for PostgreSQL flexible server **mydemoserver.postgres.database.azure.com** by using access credentials. Enter the `<server_admin_password>` you chose when prompted for password.

   ```bash
   psql --host=mydemoserver-pg.postgres.database.azure.com --port=5432 --username=myadmin --dbname=postgres
   ```

   To connect to a random node in the cluster, use port 7432.

   ```bash
   psql --host=mydemoserver-pg.postgres.database.azure.com --port=7432 --username=myadmin --dbname=postgres
   ```

   After you connect, the psql utility displays a postgres prompt where you type SQL commands. In the initial connection output, a warning might appear because the psql you're using might be a different version than the Azure Database for PostgreSQL flexible server version.

   Example psql output:

   ```javascript
   psql (12.3 (Ubuntu 12.3-1.pgdg18.04+1), server 13.2)
   WARNING: psql major version 12, server major version 13.
         Some psql features might not work.
   SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
   Type "help" for help.
   ```

   > [!TIP]  
   > If the firewall isn't configured to allow the IP address of your client, the following error occurs:
   >  
   > psql: FATAL: no pg_hba.conf entry for host `<IP address>`, user "myadmin", database "postgres", SSL on FATAL: SSL connection is required. Specify SSL options and retry.
   >  
   > Confirm your client's IP is allowed in the firewall rules.

1. Create a blank schema called `exampleschema` at the prompt by typing the following command:

    ```bash
    CREATE SCHEMA exampleschema;
    ```

1. At the prompt, execute the following command to make the schema `exampleschema` distributed:

    ```sql
    SELECT citus_schema_distribute('exampleschema');
    ```

1. Type `\q`, and then select the Enter key to quit psql.

You connected to the elastic cluster by using psql, and you created a blank schema and made it distributed.

## Clean up resources

> [!TIP]
> Other quickstarts in this collection build on this quickstart. If you plan to continue working with quickstarts, don't clean up the resources that you created in this quickstart. If you don't plan to continue, follow these steps to delete the resources that this quickstart created in the portal.

To clean up the resources that you created in this quickstart, use one of the following methods. [Delete the Azure resource group](/azure/azure-resource-manager/management/delete-resource-group) to remove all the resources in the resource group. If you want to keep the other resources, only [delete the server](../configure-maintain/how-to-delete-server.md).

## Related content
- [Design multitenant database with elastic clusters](../configure-maintain/tutorial-multitenant-database.md).
