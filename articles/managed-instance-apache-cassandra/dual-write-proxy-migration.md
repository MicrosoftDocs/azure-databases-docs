---
title: Live migration to Azure Managed Instance for Apache Cassandra using Apache Spark and a dual-write proxy
description: Learn how to migrate to Azure Managed Instance for Apache Cassandra by using Apache Spark and a dual-write proxy.
author: TheovanKraay
ms.author: thvankra
ms.service: azure-managed-instance-apache-cassandra
ms.topic: tutorial
ms.date: 06/09/2025
#customer intent: As a developer, I want to live migrate an Apache Cassandra cluster to Azure Managed Instance for Apache Cassandra.
---

# Live migration to Azure Managed Instance for Apache Cassandra by using a dual-write proxy

Where possible, we recommend that you use the Apache Cassandra native capability to migrate data from your existing cluster into Azure Managed Instance for Apache Cassandra by configuring a [hybrid cluster](configure-hybrid-cluster.md). This capability uses Apache Cassandra's gossip protocol to replicate data from your source datacenter into your new managed-instance datacenter in a seamless way. 

There might be some scenarios where your source database version isn't compatible, or a hybrid cluster setup is otherwise not feasible. This tutorial describes how to migrate data to Azure Managed Instance for Apache Cassandra in a live fashion by using a [dual-write proxy](https://github.com/Azure-Samples/cassandra-proxy) and Apache Spark. The dual-write proxy is used to capture live changes, while historical data is copied in bulk using Apache Spark. The benefits of this approach are:

- **Minimal application changes**. The proxy can accept connections from your application code with few or no configuration changes. It routes all requests to your source database and asynchronously route writes to a secondary target. 
- **Client wire protocol dependency**. Because this approach isn't dependent on back-end resources or internal protocols, it can be used with any source or target Cassandra system that implements the Apache Cassandra wire protocol.

The following image illustrates the approach.

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/managed-instance-apache-cassandra/live-migration.gif" alt-text="Animation that shows the live migration of data to Azure Managed Instance for Apache Cassandra." border="false":::

## Prerequisites

- Provision an Azure Managed Instance for Apache Cassandra cluster by using the [Azure portal](create-cluster-portal.md) or the [Azure CLI](create-cluster-cli.md). Ensure that you can [connect to your cluster with CQLSH](./create-cluster-portal.md#connect-to-your-cluster).

- [Provision an Azure Databricks account inside your Managed Cassandra virtual network](deploy-cluster-databricks.md). Ensure that the account has network access to your source Cassandra cluster. This example creates a Spark cluster in this account for the historical data load.

- Ensure that you already migrated the keyspace/table scheme from your source Cassandra database to your target Cassandra managed-instance database.

## Provision a Spark cluster

We recommend that you select Azure Databricks runtime version 7.5, which supports Spark 3.0.

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/cosmos-db/databricks-runtime.png" alt-text="Screenshot that shows finding the Azure Databricks runtime version.":::

## Add Spark dependencies

You need to add the Apache Spark Cassandra Connector library to your cluster to connect to any wire protocol compatible Apache Cassandra endpoints. In your cluster, select **Libraries** > **Install New** > **Maven**, and then add `com.datastax.spark:spark-cassandra-connector-assembly_2.12:3.0.0` in Maven coordinates.

> [!IMPORTANT]
> If you have a requirement to preserve Apache Cassandra `writetime` for each row during the migration, we recommend using [this sample](https://github.com/Azure-Samples/cassandra-migrator). The dependency jar in this sample also contains the Spark connector, so install this version instead of the connector assembly.
>
> This sample is also useful if you want to perform a row comparison validation between source and target after historic data load is complete. See [Run the historical data load](dual-write-proxy-migration.md#run-the-historical-data-load) and [Validate the source and target](dual-write-proxy-migration.md#validate-the-source-and-target).

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

We recommend that you install the proxy on all nodes in your source Cassandra cluster. At minimum, run the following command to start the proxy on each node. Replace `<target-server>` with an IP or server address from one of the nodes in the target cluster. Replace `<path to JKS file>` with path to a local jks file, and replace `<keystore password>` with the corresponding password.  

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
  --proxy-jks-password <keystore password> --target-username <username> --target-password <password> \
  --disable-source-tls true  --disable-target-tls true 
```

> [!NOTE]
> Make sure your client application uses the same keystore and password as the ones used for the dual-write proxy when you build SSL connections to the database that use the proxy.

### Configure the credentials and port

By default, the source credentials are passed through from your client app. The proxy uses the credentials for making connections to the source and target clusters. As mentioned earlier, this process assumes that the source and target credentials are the same. If necessary, you can specify a different username and password for the target Cassandra endpoint separately when starting the proxy:

```bash
java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar localhost <target-server> \
  --proxy-jks-file <path to JKS file> --proxy-jks-password <keystore password> \
  --target-username <username> --target-password <password>
```

The default source and target ports, when not specified, is 9042. If either the target or the source Cassandra endpoint runs on a different port, you can use `--source-port` or `--target-port` to specify a different port number: 

```bash
java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar localhost <target-server> \
  --source-port 9042 --target-port 10350 --proxy-jks-file <path to JKS file> \
  --proxy-jks-password <keystore password> --target-username <username> --target-password <password>
```

### Deploy the proxy remotely

There might be circumstances in which you don't want to install the proxy on the cluster nodes themselves. You want to install it on a separate machine. In that scenario, specify the IP address of `<source-server>`:

```bash
java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar <source-server> <destination-server>
```

> [!WARNING]
> You might want to run the proxy remotely on a separate machine rather than running it on all nodes in your source Apache Cassandra cluster. If so, we recommend that you deploy the proxy to the same number of machines as you have nodes in your cluster. Set up a substitution for their IP addresses in *system.peers*. Use this [configuration in the proxy](https://github.com/Azure-Samples/cassandra-proxy#ghost-proxy). If you don't use this approach, it might affect performance while the live migration occurs, because the client driver can't open connections to all nodes in the cluster.

### Allow zero application code changes

By default, the proxy listens on port 29042. You must change the application code to point to this port. Alternatively, you can change the port that the proxy listens on. You might use this approach if you want to eliminate application-level code changes by:

- Having the source Cassandra server run on a different port.
- Having the proxy run on the standard Cassandra port 9042.

```bash
java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar source-server destination-server --proxy-port 9042
```

> [!NOTE]
> Installing the proxy on cluster nodes doesn't require restart of the nodes. If you have many application clients and prefer to run the proxy on the standard Cassandra port 9042 to eliminate any application-level code changes, change the [Apache Cassandra default port](https://cassandra.apache.org/doc/latest/). You then need to restart the nodes in your cluster, and configure the source port to be the new port that you defined for your source Cassandra cluster. 
>
> In the following example, we change the source Cassandra cluster to run on port 3074, and we start the cluster on port 9042:
>
>```bash
>java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar source-server destination-server --proxy-port 9042 --source-port 3074
>``` 

### Force protocols

The proxy has functionality to force protocols, which might be necessary if the source endpoint is more advanced than the target or is otherwise unsupported. In that case, you can specify `--protocol-version` and `--cql-version` to force the protocol to comply with the target:

```bash
java -jar target/cassandra-proxy-1.0-SNAPSHOT-fat.jar source-server destination-server --protocol-version 4 --cql-version 3.11
```

After the dual-write proxy is running, change the port on your application client and restart. Or change the Cassandra port and restart the cluster if you chose that approach. The proxy starts forwarding writes to the target endpoint. You can learn about [monitoring and metrics](https://github.com/Azure-Samples/cassandra-proxy#monitoring) available in the proxy tool. 

## Run the historical data load

To load the data, create a Scala notebook in your Azure Databricks account. Replace your source and target Cassandra configurations with the corresponding credentials, and replace the source and target keyspaces and tables. Add more variables for each table as required to the following sample, and then run. After your application starts sending requests to the dual-write proxy, you're ready to migrate historical data. 

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
    "spark.cassandra.connection.port" -> "9042",
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
> In the preceding Scala sample, `timestamp` is being set to the current time before reading all the data in the source table. Then, `writetime` is being set to this backdated time stamp. This approach ensures that records that are written from the historical data load to the target endpoint can't overwrite updates that come in with a later time stamp from the dual-write proxy while historical data is being read.

> [!IMPORTANT]
> If you need to preserve *exact* time stamps for any reason, you should take a historical data migration approach that preserves time stamps, such as [this sample](https://github.com/Azure-Samples/cassandra-migrator). The dependency jar in the sample also contains the Spark connector, so you don't need to install the Spark connector assembly mentioned in the earlier prerequisites. Having both installed in your Spark cluster causes conflicts.

## Validate the source and target

After the historical data load is complete, your databases should be in sync and ready for cutover. We recommend that you validate the source and target to ensure they match before finally cutting over.

> [!NOTE]
> If you used the [Cassandra migrator](https://github.com/Azure-Samples/cassandra-migrator) sample mentioned in the earlier sections for preserving `writetime`, you have the capability to [validate the migration](https://github.com/Azure-Samples/cassandra-migrator#validate-migration) by [comparing rows](https://github.com/Azure-Samples/cassandra-migrator/blob/main/build_files/src/main/scala/com/cassandra/migrator/validation/RowComparisonFailure.scala) in source and target based on certain tolerances. 

## Next step

> [!div class="nextstepaction"]
> [Manage Azure Managed Instance for Apache Cassandra resources using Azure CLI](manage-resources-cli.md)
