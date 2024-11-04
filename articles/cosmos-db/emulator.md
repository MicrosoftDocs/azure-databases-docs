---
title: Emulator (Docker/local)
titleSuffix: Azure Cosmos DB
description: Use the Azure Cosmos DB local or docker-based emulator to test your applications against multiple API endpoints.
author: sajeetharan
ms.author: sasinnat
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 10/09/2024
# CustomerIntent: As a developer, I want to use the Azure Cosmos DB emulator so that I can develop my application against a database during development.
---


# What is the Azure Cosmos DB emulator?

The Azure Cosmos DB emulator provides a local environment that emulates the Azure Cosmos DB service designed for development purposes. Using the emulator, you can develop and test your application locally, without creating an Azure subscription or incurring any service costs. When you're satisfied with how your application is working with the emulator, you can transition to using an Azure Cosmos DB account with minimal friction.

> [!IMPORTANT]
> We do not recommend the use of the emulator for production workloads.

> [!Tip] 
> Visit our new **[Samples Gallery](https://aka.ms/AzureCosmosDB/Gallery)** for the latest samples for building new apps


## Differences between the emulator and cloud service

The emulator provides an environment on your developer workspace that isn't capable of emulating every aspect of the Azure Cosmos DB service. Here are a few key differences in functionality between the emulator and the equivalent cloud service.

> [!IMPORTANT]
> The Linux emulator currently doesn't support developer machines running on Apple silicon series or Microsoft ARM chips. A temporary workaround is to install a Windows virtual machine and run the emulator on that platform.

- The emulator's **Data Explorer** pane is only supported in the API for NoSQL and API for MongoDB.
- The emulator only supports **provisioned throughput**. The emulator doesn't support **serverless** throughput.
- The emulator uses a well-known key when it starts. You can't regenerate the key for the running emulator. To use a different key, you must [start the emulator with the custom key specified](#authentication).
- The emulator can't be replicated across geographical regions or multiple instances. Only a single running instance of the emulator is supported. The emulator can't be scaled out.
- The emulator ideally supports up to 10 fixed-size containers at 400 RU/s or 5 unlimited-size containers. Theoretically, you can create more containers, but you could experience performance degradation with the emulator.
- The emulator only supports the [Session](consistency-levels.md#session-consistency) and [Strong](consistency-levels.md#strong-consistency) consistency levels. The emulator isn't a scalable service and doesn't actually implement the consistency levels. The emulator only flags the configured consistency level for testing purposes.
- The emulator constraints the unique identifier of items to a size of **254** characters.
- The emulator supports a maximum of five `JOIN` statements per query.

The emulator's features may lag behind the pace of new features for the cloud service. There could potentially be new features and changes in the cloud service that have a small delay before they're available in the emulator.

## Authentication

Every request made against the emulator must be authenticated using a key over TLS/SSL. The emulator ships with a single account configured to use a well-known authentication key. By default, these credentials are the only credentials permitted for use with the emulator:

| | Value |
| --- | --- |
| **Endpoint** | `localhost:8081` |
| **Key** | `C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==` |
| **Connection string** | `AccountEndpoint=https://localhost:8081/;AccountKey=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==;` |

> [!TIP]
> With the Windows (local) emulator, you can also customize the key used by the emulator. For more information, see [Windows emulator arguments](emulator-windows-arguments.md).

## Import emulator certificate

In some cases, you may wish to manually import the TLS/SS certificate from the emulator's running container into your host machine. This step avoids bad practices like disabling TLS/SSL validation in the SDK. For more information, see [import certificate](how-to-develop-emulator.md#import-the-emulators-tlsssl-certificate).

## Linux based Emulator (Preview)

The next generation of the Azure Cosmos DB Emulator is entirely linux based. It supports running on Apple silicon series or Microsoft ARM chips, without requiring any workarounds to install a Windows virtual machine.

> [!IMPORTANT] 
> This version of the emulator currently supports [gateway mode](./nosql/sdk-connection-modes.md#available-connectivity-modes) only, with a select subset of features (see [below](#feature-support)). It only supports the NoSQL API.

### Components

* **Data explorer** - interactively explore the data in the emulator. By default this runs on port 1234, for example http://localhost:1234.
* **Azure Cosmos DB emulator** - a local version of the Azure Cosmos DB database service. By default, this runs on port 8081, for example http://localhost:8081.

### Prerequisites

This emulator is provided as a docker container. You must have [docker](https://www.docker.com/) installed in your operating system. 

### Installation

Execute the following to download the docker image:

```shell
docker pull mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview
```

### Running

To run the container, execute the below:

```shell
docker run -d -p 8081:8081 -p 1234:1234 mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview
```

Check the image is running:

```shell
docker ps
```

You should see an output like the below. 

```shell
CONTAINER ID   IMAGE                                                             COMMAND                  CREATED         STATUS         PORTS                                                                                  NAMES
c1bb8cf53f8a   mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview  "/bin/bash -c /home/…"   5 seconds ago   Up 5 seconds   0.0.0.0:1234->1234/tcp, :::1234->1234/tcp, 0.0.0.0:8081->8081/tcp, :::8081->8081/tcp   wonderful_tu
```

The emulator gateway endpoint runs on port 8081 and the data explorer on port 1234. Copy `http://localhost:1234` into your browser to access the data explorer. It may take a few seconds for data explorer to come up. The gatewat endpoint should be available immediately. 


### Docker Commands

The following table summarizes the available Docker commands for configuring the Cosmos DB Emulator, detailing the corresponding arguments, environment variables, allowed values, default settings, and descriptions of their functionalities.

| Requirement                                                                                                  | Arg                       | Env              | Allowed values                               | Default                          | Description                                                                                                                         |
|--------------------------------------------------------------------------------------------------------------|---------------------------|------------------|---------------------------------------------|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Print the settings to stdout from the container                                                             | `--help`, `-h`           | N/A              | N/A                                         | N/A                              | Display information on available configuration                                                                                     |
| Set the port of the Cosmos endpoint                                                                          | `--port [INT]`           | PORT             | INT                                         | 8081                             | The port of the Cosmos endpoint on the container. You still need to publish this port (e.g. `-p 8081:8081`).                     |
| Specify the protocol used by the Cosmos endpoint                                                             | `--protocol`             | PROTOCOL         | `https`, `http`, `https-insecure`         | `http`                           | The protocol of the Cosmos endpoint on the container.                                                                               |
| Enable the data explorer                                                                                     | `--enable-explorer`       | ENABLE_EXPLORER  | `true`, `false`                            | `true`                           | Enable running the Cosmos Data Explorer on the same container.                                                                      |
| Set the port used by the data explorer                                                                        | `--explorer-port`         | EXPLORER_PORT    | INT                                         | 1234                             | The port of the Cosmos Data Explorer on the container. You still need to publish this port (e.g. `-p 1234:1234`).                 |
| User should be able to specify the protocol used by the explorer, otherwise default to what the Cosmos endpoint is using | `--explorer-protocol`     | EXPLORER_PROTOCOL | `https`, `http`, `https-insecure`         | `<the value of --protocol>`     | The protocol of the Cosmos Data Explorer on the container. Defaults to the protocol setting on the Cosmos endpoint.                |
| Specify the key via file                                                                                    | `--key-file [PATH]`      | KEY_FILE         | PATH                                        | `<default secret>`              | Override default key with key in key file. You need to mount this file into the container (e.g. if KEY_FILE=/mykey, you'd add an option like the following to your docker run: `--mount type=bind,source=./myKey,target=/myKey`) |
| Set the data path                                                                                           | `--data-path [PATH]`      | DATA_PATH        | PATH                                        | `/data`                          | Specify a directory for data. Frequently used with `docker run --mount` option (e.g. if DATA_PATH=/usr/cosmos/data, you'd add an option like the following to your docker run: `--mount type=bind,source=./.local/data,target=/usr/cosmos/data`) |
| Specify the cert path to be used for https                                                                   | `--cert-path [PATH]`     | CERT_PATH        | PATH                                        | `<default cert>`                | Specify a path to a certificate for securing traffic. You need to mount this file into the container (e.g. if CERT_PATH=/mycert.pfx, you'd add an option like the following to your docker run: `--mount type=bind,source=./mycert.pfx,target=/mycert.pfx`) |
| Specify the cert secret to be used for https                                                                | N/A                       | CERT_SECRET      | string                                      | `<default secret>`              | The secret for the certificate specified on CERT_PATH.                                                                             |
| Set the log level                                                                                           | `--log-level [LEVEL]`    | LOG_LEVEL        | `quiet`, `error`, `warn`, `info`, `debug`, `trace` | `info`                          | The verbosity of logs that will be emitted by the emulator and data explorer.                                                      |
| Enable diagnostic info being sent to Microsoft                                                              | `--enable-telemetry`      | ENABLE_TELEMETRY | `true`, `false`                           | `true`                           | Enable sending telemetry to Microsoft to help us improve the product.                                                               |


### Feature support

The new vNext emulator is a re-architecture based on Linux. As a result, not all features are supported, and some features will also not be supported in the future. The below table shows current status of feature support.

| Feature/operation name                       | Status                   |
|----------------------------------------------|--------------------------|
| Create database                              | Supported                |
| Read database                                | Supported                |
| Delete database                              | Supported                |
| Read database feed                           | Supported                |
| Create database twice conflict               | Supported                |
| Create collection                            | Supported                |
| Read collection                              | Supported                |
| Update collection                            | Supported                |
| Delete collection                            | Supported                |
| Read collection feed                         | Supported                |
| Create collection twice conflict             | Supported                |
| Create collection with custom index policy   | Supported                |
| Create collection with ttl expiration        | Supported                |
| Create partitioned collection                | Supported                |
| Get and change collection performance        | Supported                |
| Create document                              | Supported                |
| Read document                                | Supported                |
| Update document                              | Supported                |
| Delete document                              | Supported                |
| Read document feed                           | Supported                |
| Insert large document                        | Supported                |
| Create and read document with utf data       | Supported                |
| Query with sql query spec                    | Supported                |
| Query with equality                          | Supported                |
| Query with and filter and projection         | Not yet implemented      |
| Query with and filter                        | Not yet implemented      |
| Query with equals on id                      | Supported                |
| Query with inequality                        | Not yet implemented      |
| Query with range operators on numbers        | Not yet implemented      |
| Query with range operators on strings        | Not yet implemented      |
| Query with range operators date times        | Not yet implemented      |
| Query with order by                          | Supported                |
| Query with order by numbers                  | Supported                |
| Query with order by strings                  | Not yet implemented      |
| Query with aggregates                        | Not yet implemented      |
| Query with subdocuments                      | Not yet implemented      |
| Query with joins                             | Not yet implemented      |
| Query with two joins                         | Not yet implemented      |
| Query with two joins and filter              | Not yet implemented      |
| Query with single join                       | Not yet implemented      |
| Query with string math and array operators   | Not yet implemented      |
| Query with paging                            | Not yet implemented      |
| Query partitioned collection in parallel     | Not yet implemented      |
| Query with order by for partitioned collection | Not yet implemented    |
| Stored procedure                             | Will not be supported    |
| Triggers                                     | Will not be supported    |
| UDFs                                         | Will not be supported    |

### Limitations

In addition to features not yet supported or not planned as above, the following are current limitations of the vNext emulator.

- The .NET SDK for Azure Cosmos DB does not support bulk execution API in the new emulator.
- The .NET SDK does not support http mode in the new emulator in the new emulator.

## Raising issues

If you encounter issues with using this version of the emulator, please open an issue in the repo [here](https://github.com/Azure/azure-cosmos-db-emulator-docker) and tag it with label `cosmosEmulatorVnextPreview`.

## Next step

> [!div class="nextstepaction"]
> [Get started using the Azure Cosmos DB emulator for development](how-to-develop-emulator.md)