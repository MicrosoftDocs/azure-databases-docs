---
title: Live migrate data from Apache Cassandra to the Azure Cosmos DB for Apache Cassandra by using dual-write proxy and Apache Spark
description: Learn how to live migrate data from an Apache Cassandra database to the Azure Cosmos DB for Apache Cassandra by using dual-write proxy and Apache Spark.
author: TheovanKraay
ms.author: thvankra
ms.service: azure-cosmos-db
ms.subservice: apache-cassandra
ms.topic: how-to
ms.date: 06/05/2025
#customer intent: As a database administrator, I want to know how to live migrate data to Azure Cosmos DB for Apache Cassandra from a native Apache Cassandra cluster.
---

# Live migrate data from Apache Cassandra to the Azure Cosmos DB for Apache Cassandra by using dual-write proxy and Apache Spark

API for Cassandra in Azure Cosmos DB is a great choice for enterprise workloads that run on Apache Cassandra for various reasons: 

- **No overhead of managing and monitoring:** It eliminates the overhead of managing and monitoring a myriad of settings across operating systems, Java virtual machines, and yaml files and their interactions.
- **Significant cost savings:** You can save cost with Azure Cosmos DB, which includes the cost of virtual machines, bandwidth, and any applicable licenses. You don’t have to manage the data centers, servers, SSD storage, networking, and electricity costs.
- **Ability to use existing code and tools:** Azure Cosmos DB provides wire protocol level compatibility with existing Cassandra SDKs and tools. This compatibility ensures you can use your existing codebase with Azure Cosmos DB for Apache Cassandra with trivial changes.

Azure Cosmos DB doesn't support the native Apache Cassandra gossip protocol for replication. Where zero downtime is a requirement for migration, a different approach is necessary. This tutorial describes how to live migrate data to Azure Cosmos DB for Apache Cassandra from a native Apache Cassandra cluster using a [dual-write proxy](https://github.com/Azure-Samples/cassandra-proxy) and [Apache Spark](https://spark.apache.org/). 

The following image illustrates the pattern. The dual-write proxy is used to capture live changes. Historical data is copied in bulk using Apache Spark. The proxy can accept connections from your application code with few or no configuration changes. It routes all requests to your source database and asynchronously route writes to API for Cassandra while bulk copy is happening.

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/managed-instance-apache-cassandra/live-migration.gif" alt-text="Animation that shows the live migration of data to Azure Managed Instance for Apache Cassandra." border="false":::

## Prerequisites

- [Provision an Azure Cosmos DB for Apache Cassandra account](manage-data-dotnet.md#create-a-database-account).
- [Review the basics of connecting to an Azure Cosmos DB for Apache Cassandra](connect-spark-configuration.md).
- Review the [supported features in the Azure Cosmos DB for Apache Cassandra](support.md) to ensure compatibility.
- [Use cqlsh for validation](support.md#cql-shell).
- Ensure you have network connectivity between your source cluster and target API for Cassandra endpoint.
- Ensure that you previously migrated the keyspace/table scheme from your source Cassandra database to your target API for Cassandra account.

> [!IMPORTANT]
> If you have a requirement to preserve Apache Cassandra `writetime` during migration, the following flags must be set when creating tables:
>
> ```sql
> with cosmosdb_cell_level_timestamp=true and cosmosdb_cell_level_timestamp_tombstones=true and cosmosdb_cell_level_timetolive=true
> ``` 
>
> For example:
>
> ```sql
> CREATE KEYSPACE IF NOT EXISTS migrationkeyspace WITH REPLICATION= {'class': 'org.apache.> cassandra.locator.SimpleStrategy', 'replication_factor' : '1'};
> ```
>
> ```sql
> CREATE TABLE IF NOT EXISTS migrationkeyspace.users (
>  name text,
>  userID int,
>  address text,
>  phone int,
>  PRIMARY KEY ((name), userID)) with cosmosdb_cell_level_timestamp=true and > cosmosdb_cell_level_timestamp_tombstones=true and cosmosdb_cell_level_timetolive=true;
> ```

## Provision a Spark cluster

We recommend that you use Azure Databricks. Use a runtime which supports Spark 3.0 or higher.

> [!IMPORTANT]
> You need to ensure that your Azure Databricks account has network connectivity with your source Apache Cassandra cluster. This setup might require virtual network injection. For more information, see [Deploy Azure Databricks in your Azure virtual network](/azure/databricks/administration-guide/cloud-configurations/azure/vnet-inject).

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/cosmos-db/databricks-runtime.png" alt-text="Screenshot that shows finding the Azure Databricks runtime version.":::

## Add Spark dependencies

Add the Apache Spark Cassandra Connector library to your cluster to connect to both native and Azure Cosmos DB Cassandra endpoints. In your cluster, select **Libraries** > **Install New** > **Maven**, and then add `com.datastax.spark:spark-cassandra-connector-assembly_2.12:3.0.0` in Maven coordinates.

> [!IMPORTANT]
> If you have a requirement to preserve Apache Cassandra `writetime` for each row during the migration, we recommend using [this sample](https://github.com/Azure-Samples/cassandra-migrator). The dependency JAR in this sample also contains the Spark connector, so you should install this version instead of the connector assembly described previously.
>
> This sample is also useful if you want to perform a row comparison validation between source and target after historic data load is complete. For more information, see [Run the historical data load](migrate-data-dual-write-proxy.md#run-the-historical-data-load) and [Validate the source and target](migrate-data-dual-write-proxy.md#validate-the-source-and-target). 

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/cosmos-db/databricks-search-packages.png" alt-text="Screenshot that shows searching for Maven packages in Azure Databricks.":::

Select **Install**, and then restart the cluster when installation is complete.

> [!NOTE]
> Be sure to restart the Azure Databricks cluster after the Cassandra Connector library is installed.

## Install the dual-write proxy

For optimal performance during dual writes, we recommend that you install the proxy on all nodes in your source Cassandra cluster.

```bash
#assuming you do not have git already installed
sudo apt-get install git 

#assuming you do not have maven already installed
sudo apt install maven

#clone repo for dual-write proxy
git clone https://github.com/Azure-Samples/cassandra-proxy.git

#change directory
cd cassandra-proxy

#compile the proxy
mvn package
```

## Start the dual-write proxy

We recommend that you install the proxy on all nodes in your source Cassandra cluster. At minimum, run the following command to start the proxy on each node. Replace `<target-server>` with an IP or server address from one of the nodes in the target cluster. Replace `<path to JKS file>` with path to a local .jks file, and replace `<keystore password>` with the corresponding password.  

```bash
java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar localhost <target-server> --proxy-jks-file <path to JKS file> --proxy-jks-password <keystore password>
```

Starting the proxy in this way assumes that the following are true:

- Source and target endpoints have the same username and password.
- Source and target endpoints implement Secure Sockets Layer (SSL).

If your source and target endpoints can't meet these criteria, read on for further configuration options.

### Configure SSL

For SSL, you can either implement an existing keystore, for example, the one that your source cluster uses, or create a self-signed certificate by using `keytool`:

```bash
keytool -genkey -keyalg RSA -alias selfsigned -keystore keystore.jks -storepass password -validity 360 -keysize 2048
```
You can also disable SSL for source or target endpoints if they don't implement SSL. Use the `--disable-source-tls` or `--disable-target-tls` flags:

```bash
java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar localhost <target-server> \
  --source-port 9042 --target-port 10350 --proxy-jks-file <path to JKS file> \
  --proxy-jks-password <keystore password> --target-username <username> \
  --target-password <password> --disable-source-tls true  --disable-target-tls true 
```

> [!NOTE]
> Make sure that your client application uses the same keystore and password as the ones used for the dual-write proxy when you build SSL connections to the database via the proxy.

### Configure the credentials and port

By default, your client app passes the source credentials. The proxy uses the credentials to make connections to the source and target clusters. As mentioned earlier, this process assumes that the source and target credentials are the same. You must specify a different username and password for the target API for Cassandra endpoint separately when starting the proxy:

```bash
java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar localhost <target-server> \
  --proxy-jks-file <path to JKS file> --proxy-jks-password <keystore password> \
  --target-username <username> --target-password <password>
```

The default source and target ports, when not specified, is 9042. In this case, API for Cassandra runs on port `10350`. Use `--source-port` or `--target-port` to specify port numbers: 

```bash
java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar localhost <target-server> \
  --source-port 9042 --target-port 10350 --proxy-jks-file <path to JKS file> \
  --proxy-jks-password <keystore password> --target-username <username> --target-password <password>
```

### Deploy the proxy remotely

There might be circumstances in which you don't want to install the proxy on the cluster nodes themselves. You might prefer to install it on a separate machine. In that scenario, specify the IP address of `<source-server>`:

```bash
java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar <source-server> <destination-server>
```

> [!WARNING]
> Installing and running the proxy remotely on a separate machine rather than running it on all nodes in your source Apache Cassandra cluster affects performance while the live migration occurs. While this configuration works functionally, the client driver can't open connections to all nodes within the cluster. The client relies on the single coordinator node where the proxy is installed to make connections.  

### Allow zero application code changes

By default, the proxy listens on port 29042. Change the application code to point to this port. You can, instead, change the port that the proxy listens on. You might make this change if you want to eliminate application-level code changes by:

- Having the source Cassandra server run on a different port.
- Having the proxy run on the standard Cassandra port 9042.

```bash
java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar source-server destination-server --proxy-port 9042
```

> [!NOTE]
> Installing the proxy on cluster nodes doesn't require restart of the nodes. If you have many application clients and prefer to run the proxy on the standard Cassandra port 9042 in order to eliminate application-level code changes, change the [Apache Cassandra default port](https://cassandra.apache.org/doc/stable/cassandra/overview/faq/index.html). You then need to restart the nodes in your cluster and configure the source port to be the new port that you defined for your source Cassandra cluster. 
>
> In the following example, we change the source Cassandra cluster to run on port 3074, and we start the cluster on port 9042:
>
>```bash
>java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar source-server destination-server \
>  --proxy-port 9042 --source-port 3074
>``` 

### Force protocols

The proxy has functionality to force protocols, which might be necessary if the source endpoint is more advanced than the target or is otherwise unsupported. In that case, you can specify `--protocol-version` and `--cql-version` to force the protocol to comply with the target:

```bash
java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar source-server destination-server \
  --protocol-version 4 --cql-version 3.11
```

After the dual-write proxy is running, you need to change the port on your application client and restart. Or change the Cassandra port and restart the cluster, if you choose that approach. The proxy starts forwarding writes to the target endpoint. For information, see [monitoring and metrics](https://github.com/Azure-Samples/cassandra-proxy#monitoring).

## Run the historical data load

To load the data, create a Scala notebook in your Azure Databricks account. Replace your source and target Cassandra configurations with the corresponding credentials, and replace the source and target keyspaces and tables. Add more variables for each table as required to the following sample, and then run. After your application starts sending requests to the dual-write proxy, you're ready to migrate historical data. 

> [!IMPORTANT]
> Before you migrate the data, increase the container throughput to the amount required for your application to migrate quickly. Scaling the throughput before starting the migration helps you to migrate your data in less time. To help safeguard against rate-limiting during the historical data load, you can enable server-side retries (SSR) in API for Cassandra. For instructions on how to enable SSR and more information, see [Prevent rate-limiting errors for Azure Cosmos DB for Apache Cassandra operations](prevent-rate-limiting-errors.md).

```scala
import com.datastax.spark.connector._
import com.datastax.spark.connector.cql._
import org.apache.spark.SparkContext

// source cassandra configs
val sourceCassandra = Map( 
    "spark.cassandra.connection.host" -> "<Source Cassandra Host>",
    "spark.cassandra.connection.port" -> "9042",
    "spark.cassandra.auth.username" -> "<USERNAME>",
    "spark.cassandra.auth.password" -> "<PASSWORD>",
    "spark.cassandra.connection.ssl.enabled" -> "true",
    "keyspace" -> "<KEYSPACE>",
    "table" -> "<TABLE>"
)

//target cassandra configs
val targetCassandra = Map( 
    "spark.cassandra.connection.host" -> "<Source Cassandra Host>",
    "spark.cassandra.connection.port" -> "10350",
    "spark.cassandra.auth.username" -> "<USERNAME>",
    "spark.cassandra.auth.password" -> "<PASSWORD>",
    "spark.cassandra.connection.ssl.enabled" -> "true",
    "keyspace" -> "<KEYSPACE>",
    "table" -> "<TABLE>",
    //throughput related settings below - tweak these depending on data volumes. 
    "spark.cassandra.output.batch.size.rows"-> "1",
    "spark.cassandra.output.concurrent.writes" -> "1000",
    "spark.cassandra.connection.remoteConnectionsPerExecutor" -> "1",
    "spark.cassandra.concurrent.reads" -> "512",
    "spark.cassandra.output.batch.grouping.buffer.size" -> "1000",
    "spark.cassandra.connection.keep_alive_ms" -> "600000000"
)

//set timestamp to ensure it is before read job starts
val timestamp: Long = System.currentTimeMillis / 1000

//Read from source Cassandra
val DFfromSourceCassandra = sqlContext
  .read
  .format("org.apache.spark.sql.cassandra")
  .options(sourceCassandra)
  .load
  
//Write to target Cassandra
DFfromSourceCassandra
  .write
  .format("org.apache.spark.sql.cassandra")
  .options(targetCassandra)
  .option("writetime", timestamp)
  .mode(SaveMode.Append)
  .save
```

> [!NOTE]
> In the preceding Scala sample, you notice that `timestamp` is being set to the current time before reading all the data in the source table. Then, `writetime` is being set to this backdated time stamp. This approach ensures that records that are written from the historical data load to the target endpoint can't overwrite updates that come in with a later time stamp from the dual-write proxy while historical data is being read.

> [!IMPORTANT]
> If you need to preserve *exact* time stamps for any reason, you should take a historical data migration approach that preserves time stamps, such as [this sample](https://github.com/Azure-Samples/cassandra-migrator). The dependency JAR in the sample also contains the Spark connector, so you don't need to install the Spark connector assembly mentioned in the earlier prerequisites. Having both installed in your Spark cluster causes conflicts.

## Validate the source and target

After the historical data load is complete, your databases should be in sync and ready for cutover. We recommend that you validate the source and target to ensure they match before finally cutting over.

> [!NOTE]
> If you used the [Cassandra migrator](https://github.com/Azure-Samples/cassandra-migrator) sample mentioned previously for preserving `writetime`, this sample includes the capability to [validate the migration](https://github.com/Azure-Samples/cassandra-migrator#validate-migration) by [comparing rows](https://github.com/Azure-Samples/cassandra-migrator/blob/main/build_files/src/main/scala/com/cassandra/migrator/validation/RowComparisonFailure.scala) in source and target based on certain tolerances. 

## Next step

> [!div class="nextstepaction"]
> [Introduction to the Azure Cosmos DB for Apache Cassandra](introduction.md)
