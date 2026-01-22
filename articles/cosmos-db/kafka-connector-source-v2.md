---
title: Kafka Connect Source Connector V2
description: Azure Cosmos DB source connector v2 provides the capability to read data from the Azure Cosmos DB Change Feed and publish this data to a Kafka topic. Kafka Connect for Azure Cosmos DB is a connector to read from and write data to Azure Cosmos DB. 
author: xinlian
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 11/03/2024
ms.author: xinlian
appliesto:
  - ✅ NoSQL
---

# Kafka Connect for Azure Cosmos DB - source connector v2

Kafka Connect for Azure Cosmos DB is a connector to read from and write data to Azure Cosmos DB. The Azure Cosmos DB source connector provides the capability to read data from the Azure Cosmos DB Change Feed and publish this data to a Kafka topic.

## Prerequisites

* Start with the [Confluent platform setup](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/cosmos/azure-cosmos-kafka-connect/docs/Confluent_Platform_Setup.md) because it gives you a complete environment to work with. If you don't wish to use Confluent Platform, then you need to install and configure Zookeeper, Apache Kafka, Kafka Connect, yourself. You also need to install and configure the Azure Cosmos DB connectors manually.
* Create an Azure Cosmos DB account, container [setup guide](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/cosmos/azure-cosmos-kafka-connect/docs/CosmosDB_Setup.md)
* Bash shell - This shell doesn’t work in Cloud Shell or WSL1.
* Download [Java 11+](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html)
* Download [Maven](https://maven.apache.org/download.cgi)

## Install the source connector

If you're using the recommended [Confluent platform setup](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/cosmos/azure-cosmos-kafka-connect/docs/Confluent_Platform_Setup.md), the Azure Cosmos DB source connector is included in the installation, and you can skip this step.

Otherwise, you can use JAR file from latest [Release](https://mvnrepository.com/artifact/com.azure.cosmos.kafka/azure-cosmos-kafka-connect) and install the connector manually. To learn more, see these [instructions](https://docs.confluent.io/current/connect/managing/install.html#install-connector-manually). You can also package a new JAR file from the source code:

```bash
# clone the azure-sdk-for-java repo if you haven't done so already
git clone https://github.com/Azure/azure-sdk-for-java.git
cd sdk/cosmos

mvn -e -DskipTests -Dgpg.skip -Dmaven.javadoc.skip=true -Dcodesnippet.skip=true -Dspotbugs.skip=true -Dcheckstyle.skip=true -Drevapi.skip=true -pl ,azure-cosmos,azure-cosmos-tests -am clean install
mvn -e -DskipTests -Dgpg.skip -Dmaven.javadoc.skip=true -Dcodesnippet.skip=true -Dspotbugs.skip=true -Dcheckstyle.skip=true -Drevapi.skip=true -pl ,azure-cosmos-kafka-connect clean install

# include the following JAR file in Kafka Connect installation
ls target/azure-cosmos-kafka-connect-*.jar
```

## Create a Kafka topic

Create a Kafka topic using Confluent Control Center. For this scenario, we create a Kafka topic named "apparels" and write nonschema embedded JSON data to the topic. To create a topic inside the Control Center, see [create Kafka topic doc](https://docs.confluent.io/platform/current/quickstart/ce-docker-quickstart.html#step-2-create-ak-topics).

## Create the source connector

### Create the source connector in Kafka Connect

To create the Azure Cosmos DB source connector in Kafka Connect, use the following JSON config. Make sure to replace the placeholder values for `azure.cosmos.account.endpoint`, `azure.cosmos.account.key` properties that you saved from the Azure Cosmos DB setup guide in the prerequisites.

```json
{
  "name": "cosmosdb-source-connector-v2",
  "config": {
    "connector.class": "com.azure.cosmos.kafka.connect.CosmosSourceConnector",
    "tasks.max": "5",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "false",
    "azure.cosmos.account.endpoint":"{endpoint}",
    "azure.cosmos.account.key":"{masterKey}",
    "azure.cosmos.application.name": "{applicationName}",
    "azure.cosmos.source.database.name":"{database}",
    "azure.cosmos.source.containers.includedList":"{container}",
    "azure.cosmos.source.changeFeed.maxItemCountHint":"500",
    "azure.cosmos.source.containers.topicMap":"{topic}#{container}",
    "azure.cosmos.source.metadata.storage.type":"Cosmos",
    "azure.cosmos.source.metadata.storage.name":"{metadataContainerName}"
  }
}
```

For more information on each of the above configuration properties, see the [source properties](#source-configuration-properties) section. Once you have all the values filled out, save the JSON file somewhere locally. You can use this file to create the connector using the REST API.

#### Create connector using Control Center

An easy option to create the connector is from the Confluent Control Center portal. Follow the [Confluent setup guide](https://docs.confluent.io/platform/current/quickstart/ce-docker-quickstart.html#step-3-install-a-ak-connector-and-generate-sample-data) to create a connector from Control Center. When setting up, instead of using the `DatagenConnector` option, use the `CosmosDBSourceConnector` tile instead. When configuring the source connector, fill out the values as filled in the JSON file.

Alternatively, in the connectors page, you can upload the JSON file built from the previous section by using the **Upload connector config file** option.

:::image type="content" source="./media/kafka-connector-source-v2/upload-source-connector-config.png" lightbox="./media/kafka-connector-source-v2/upload-source-connector-config.png" alt-text="Screenshot of 'Upload connector config file' option in the Browse connectors dialog.":::

#### Create connector using REST API

Create the source connector using the Kafka Connect REST API

```bash
# Curl to Kafka connect service
curl -H "Content-Type: application/json" -X POST -d @<path-to-JSON-config-file> http://localhost:8083/connectors
```

## Insert document into Azure Cosmos DB

1. Sign into the [Azure portal](https://portal.azure.com/learn.docs.microsoft.com) and navigate to your Azure Cosmos DB account.
1. Open the **Data Explore** tab and select **Databases**
1. Open the "kafkaconnect" database and "kafka" container you created earlier.
1. To create a new JSON document, in the API for NoSQL pane, expand "kafka" container, select **Items**, then select **New Item** in the toolbar.
1. Now, add a document to the container with the following structure. Paste the following sample JSON block into the Items tab, overwriting the current content:

   ``` json
 
   {
     "id": "2",
     "productId": "33218897",
     "category": "Women's Outerwear",
     "manufacturer": "Contoso",
     "description": "Black wool pea-coat",
     "price": "49.99",
     "shipping": {
       "weight": 2,
       "dimensions": {
         "width": 8,
         "height": 11,
         "depth": 3
       }
     }
   }
 
   ```

1. Select **Save**.
1. Confirm the document is saved by viewing the Items on the left-hand menu.

### Confirm data written to Kafka topic

1. Open Kafka Topic UI on `http://localhost:9000`.
1. Select the Kafka "apparels" topic you created.
1. Verify that the document you inserted into Azure Cosmos DB earlier appears in the Kafka topic.

### Cleanup

To delete the connector from the Confluent Control Center, navigate to the source connector you created and select the **Deletion** icon.

:::image type="content" source="./media/kafka-connector-source-v2/delete-source-connector.png" lightbox="./media/kafka-connector-source-v2/delete-source-connector.png" alt-text="Screenshot of delete option in the source connector dialog.":::

Alternatively, use the connector’s REST API:

```bash
# Curl to Kafka connect service
curl -X DELETE http://localhost:8083/connectors/cosmosdb-source-connector
```

To delete the created Azure Cosmos DB service and its resource group using Azure CLI, refer to these [steps](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/cosmos/azure-cosmos-kafka-connect/docs/CosmosDB_Setup.md#cleanup).

## Source configuration properties

The following settings are used to configure the Kafka source connector. These configuration values determine which Azure Cosmos DB container is consumed, data from which Kafka topics is written, and formats to serialize the data. For an example with default values, see this [configuration file](https://github.com/microsoft/kafka-connect-cosmosdb/blob/dev/src/docker/resources/source.example.json).

| Config Property Name                                              | Default                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|:------------------------------------------------------------------|:-------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| `connector.class`                                                 | None                     | Class name of the Azure Cosmos DB source. It should be set to `com.azure.cosmos.kafka.connect.CosmosSourceConnector`                                                                                                                                                                                                                                                                                                                                                                                      |
| `azure.cosmos.account.endpoint`                                   | None                     | Cosmos DB Account Endpoint Uri                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `azure.cosmos.account.environment`                                | `Azure`                  | The Azure environment of the Cosmos DB account: `Azure`, `AzureChina`, `AzureUsGovernment`, `AzureGermany`.                                                                                                                                                                                                                                                                                                                                                                                               |
| `azure.cosmos.account.tenantId`                                   | `""`                     | The tenantId of the Cosmos DB account. Required for `ServicePrincipal` authentication.                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `azure.cosmos.auth.type`                                          | `MasterKey`              | There are two auth types are supported currently: `MasterKey`(PrimaryReadWriteKeys, SecondReadWriteKeys, PrimaryReadOnlyKeys, SecondReadWriteKeys), `ServicePrincipal`                                                                                                                                                                                                                                                                                                                                    |
| `azure.cosmos.account.key`                                        | `""`                     | Cosmos DB Account Key (only required if `auth.type` is `MasterKey`)                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `azure.cosmos.auth.aad.clientId`                                  | `""`                     | The clientId/ApplicationId of the service principal. Required for `ServicePrincipal` authentication.                                                                                                                                                                                                                                                                                                                                                                                                      |
| `azure.cosmos.auth.aad.clientSecret`                              | `""`                     | The client secret/password of the service principal.                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `azure.cosmos.mode.gateway`                                       | `false`                  | Flag to indicate whether to use gateway mode. By default it's false, means SDK uses direct mode.                                                                                                                                                                                                                                                                                                                                                                                                          |
| `azure.cosmos.preferredRegionList`                                | `[]`                     | Preferred regions list to be used for a multi region Cosmos DB account. This is a comma separated value (for example, `[East US, West US]` or `East US, West US`) provided preferred regions to be used as hint. You should use a collocated kafka cluster with your Cosmos DB account and pass the kafka cluster region as preferred region.                                                                                                                                                             |
| `azure.cosmos.application.name`                                   | `""`                     | Application name. It is added as the userAgent suffix.                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `azure.cosmos.throughputControl.enabled`                          | `false`                  | A flag to indicate whether throughput control is enabled.                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `azure.cosmos.throughputControl.account.endpoint`                 | `""`                     | Cosmos DB Throughput Control Account Endpoint Uri.                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `azure.cosmos.throughputControl.account.environment`              | `Azure`                  | The Azure environment of the Cosmos DB account: `Azure`, `AzureChina`, `AzureUsGovernment`, `AzureGermany`.                                                                                                                                                                                                                                                                                                                                                                                               |
| `azure.cosmos.throughputControl.account.tenantId`                 | `""`                     | The tenantId of the Cosmos DB account. Required for `ServicePrincipal` authentication.                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `azure.cosmos.throughputControl.auth.type`                        | `MasterKey`              | There are two auth types are supported currently: `MasterKey`(PrimaryReadWriteKeys, SecondReadWriteKeys, PrimaryReadOnlyKeys, SecondReadWriteKeys), `ServicePrincipal`                                                                                                                                                                                                                                                                                                                                    |
| `azure.cosmos.throughputControl.account.key`                      | `""`                     | Cosmos DB Throughput Control Account Key (only required if `throughputControl.auth.type` is `MasterKey`).                                                                                                                                                                                                                                                                                                                                                                                                 |
| `azure.cosmos.throughputControl.auth.aad.clientId`                | `""`                     | The clientId/ApplicationId of the service principal. Required for `ServicePrincipal` authentication.                                                                                                                                                                                                                                                                                                                                                                                                      |
| `azure.cosmos.throughputControl.auth.aad.clientSecret`            | `""`                     | The client secret/password of the service principal.                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `azure.cosmos.throughputControl.preferredRegionList`              | `[]`                     | Preferred regions list to be used for a multi region Cosmos DB account. This is a comma separated value (for example, `[East US, West US]` or `East US, West US`) provided preferred regions to be used as hint. You should use a collocated kafka cluster with your Cosmos DB account and pass the kafka cluster region as preferred region.                                                                                                                                                             |
| `azure.cosmos.throughputControl.mode.gateway`                     | `false`                  | Flag to indicate whether to use gateway mode. By default it's false, means SDK uses direct mode.                                                                                                                                                                                                                                                                                                                                                                                                          |
| `azure.cosmos.throughputControl.group.name`                       | `""`                     | Throughput control group name. Since customer is allowed to create many groups for a container, the name should be unique.                                                                                                                                                                                                                                                                                                                                                                                |
| `azure.cosmos.throughputControl.targetThroughput`                 | `-1`                     | Throughput control group target throughput. The value should be larger than 0.                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `azure.cosmos.throughputControl.targetThroughputThreshold`        | `-1`                     | Throughput control group target throughput threshold. The value should be between (0,1].                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `azure.cosmos.throughputControl.priorityLevel`                    | `None`                   | Throughput control group priority level. The value can be None, High, or Low.                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `azure.cosmos.throughputControl.globalControl.database.name`      | `""`                     | Database which is used for throughput global control.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `azure.cosmos.throughputControl.globalControl.container.name`     | `""`                     | Container which is used for throughput global control.                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `azure.cosmos.throughputControl.globalControl.renewIntervalInMS`  | `-1`                     | This controls how often the client is going to update the throughput usage of itself and adjust its own throughput share based on the throughput usage of other clients. Default is 5 s, the allowed min value is 5 s.                                                                                                                                                                                                                                                                                    |
| `azure.cosmos.throughputControl.globalControl.expireIntervalInMS` | `-1`                     | This controls how quickly we detect the client has been offline and hence allow its throughput share to be taken by other clients. Default is 11 s, the allowed min value is 2 * renewIntervalInMS + 1.                                                                                                                                                                                                                                                                                                   |                         
| `azure.cosmos.source.database.name`                               | None                     | Cosmos DB database name.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `azure.cosmos.source.containers.includeAll`                       | `false`                  | Flag to indicate whether reading from all containers.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `azure.cosmos.source.containers.includedList`                     | `[]`                     | Containers included. This config is ignored if azure.cosmos.source.containers.includeAll is true.                                                                                                                                                                                                                                                                                                                                                                                                         |
| `azure.cosmos.source.containers.topicMap`                         | `[]`                     | A comma delimited list of Kafka topics mapped to Cosmos containers. For example: topic1#con1, topic2#con2. By default, container name is used as the name of the kafka topic to publish data to, can use this property to override the default config                                                                                                                                                                                                                                                     |
| `azure.cosmos.source.changeFeed.startFrom`                        | `Beginning`              | ChangeFeed Start from settings (Now, Beginning or a certain point in time (UTC) for example 2020-02-10T14:15:03). The default value is 'Beginning'.                                                                                                                                                                                                                                                                                                                                                       |
| `azure.cosmos.source.changeFeed.mode`                             | `LatestVersion`          | ChangeFeed mode (LatestVersion or AllVersionsAndDeletes).                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `azure.cosmos.source.changeFeed.maxItemCountHint`                 | `1000`                   | The maximum number of documents returned in a single change feed request. But the number of items received might be higher than the specified value if multiple items are changed by the same transaction.                                                                                                                                                                                                                                                                                                |
| `azure.cosmos.source.metadata.poll.delay.ms`                      | `300000`                 | Indicates how often to check the metadata changes (including container split/merge, adding/removing/recreated containers). When changes are detected, it reconfigures the tasks. Default is 5 minutes.                                                                                                                                                                                                                                                                                                    |
| `azure.cosmos.source.metadata.storage.type`                       | `Kafka`                  | The storage type of the metadata. Two types are supported: Cosmos, Kafka.                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `azure.cosmos.source.metadata.storage.name`                       | `_cosmos.metadata.topic` | The resource name of the metadata storage. If metadata storage type is Kafka topic, then this config refers to kafka topic name, the metadata topic is created if it doesn't already exist, else it uses the pre created topic. If metadata storage type is `Cosmos`, then this config refers to container name, for `MasterKey` auth, this container is created with `AutoScale` with 4000 RU if not already exists, for `ServicePrincipal` auth, it requires the container to be created ahead of time. |
| `azure.cosmos.source.messageKey.enabled`                          | `true`                   | Whether to set the kafka record message key.                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `azure.cosmos.source.messageKey.field`                            | `id`                     | The field to use as the message key.                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |


## Supported data types

The Azure Cosmos DB source connector converts JSON document to schema and supports the following JSON data types:

| JSON data type | Schema type |
| :--- | :--- |
| Array | Array |
| Boolean | Boolean | 
| Number | Float32<br>Float64<br>Int8<br>Int16<br>Int32<br>Int64|
| Null | String |
| Object (JSON)| Struct|
| String | String |

## Next steps

* Kafka Connect for Azure Cosmos DB [sink connector](kafka-connector-sink-v2.md)
