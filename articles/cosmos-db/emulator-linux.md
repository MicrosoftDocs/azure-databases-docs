---
title: Linux-based emulator (preview)
titleSuffix: Azure Cosmos DB for NoSQL
description: Use the Azure Cosmos DB Linux-based emulator to test your applications against API for NoSQL endpoints.
author: TheovanKraay
ms.author: thvankra
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 11/07/2024
# CustomerIntent: As a developer, I want to use the Linux-based Azure Cosmos DB emulator so that I can develop my application against a database during development.
---

# Linux-based emulator (preview)

The next generation of the Azure Cosmos DB emulator is entirely Linux-based and is available as a Docker container. It supports running on a wide variety of processors and operating systems.

> [!IMPORTANT]
> This version of the emulator only supports the API for NoSQL in [gateway mode](nosql/sdk-connection-modes.md#available-connectivity-modes), with a select subset of features. For more information, see [feature support](#feature-support).

## Prerequisites

- [Docker](https://www.docker.com/)

## Installation

Get the Docker container image using `docker pull`. The container image is published to the [Microsoft Artifact Registry](https://mcr.microsoft.com/) as `mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview`.

```bash
docker pull mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview
```

## Running

To run the container, use `docker run`. Afterwards, use `docker ps` to validate that the container is running.

```bash
docker run --detach --publish 8081:8081 --publish 1234:1234 mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview

docker ps
```

```output
CONTAINER ID   IMAGE                                                             COMMAND                  CREATED         STATUS         PORTS                                                                                  NAMES
c1bb8cf53f8a   mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview  "/bin/bash -c /home/…"   5 seconds ago   Up 5 seconds   0.0.0.0:1234->1234/tcp, :::1234->1234/tcp, 0.0.0.0:8081->8081/tcp, :::8081->8081/tcp   <container-name>
```

> [!NOTE]
> The emulator is comprised of two components:
>
> - **Data explorer** - interactively explore the data in the emulator. By default this runs on port `1234`
> - **Azure Cosmos DB emulator** - a local version of the Azure Cosmos DB database service. By default, this runs on port `8081`.
>
> The emulator gateway endpoint is typically available on port `8081` at the address <http://localhost:8081>. To navigate to the data explorer, use the address <http://localhost:1234> in your web browser. It may take a few seconds for data explorer to be available. The gateway endpoint is typically available immediately.

> [!IMPORTANT]
> The .NET and Java SDKs don't support HTTP mode in the emulator. Since this version of the emulator starts with HTTP by default, you will need to explicitly enable HTTPS when starting the container (see below). For the Java SDK, you will also need to [install certificates](#installing-certificates-for-java-sdk).
>
> ```bash
> docker run --detach --publish 8081:8081 --publish 1234:1234 mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview --protocol https
> ```

## Docker commands

The following table summarizes the available Docker commands for configuring the emulator. This table details the corresponding arguments, environment variables, allowed values, default settings, and descriptions of each command.

| Requirement | Arg | Env | Allowed values | Default | Description |
|---|---|---|---|---|---|
| Print the settings to stdout from the container | `--help`, `-h` | N/A | N/A | N/A | Display information on available configuration |
| Set the port of the Cosmos endpoint | `--port [INT]` | PORT | INT | 8081 | The port of the Cosmos endpoint on the container. You still need to publish this port (for example, `-p 8081:8081`). |
| Specify the protocol used by the Cosmos endpoint | `--protocol` | PROTOCOL | `https`, `http`, `https-insecure` | `http` | The protocol of the Cosmos endpoint on the container. |
| Enable the data explorer | `--enable-explorer` | ENABLE_EXPLORER | `true`, `false` | `true` | Enable running the Cosmos Data Explorer on the same container. |
| Set the port used by the data explorer | `--explorer-port` | EXPLORER_PORT | INT | 1234 | The port of the Cosmos Data Explorer on the container. You still need to publish this port (for example, `-p 1234:1234`). |
| User should be able to specify the protocol used by the explorer, otherwise default to what the Cosmos endpoint is using | `--explorer-protocol` | EXPLORER_PROTOCOL | `https`, `http`, `https-insecure` | `<the value of --protocol>` | The protocol of the Cosmos Data Explorer on the container. Defaults to the protocol setting on the Cosmos endpoint. |
| Specify the key via file | `--key-file [PATH]` | KEY_FILE | PATH | `<default secret>` | Override default key with the key specified in the file. You need to mount this file into the container (for example, if KEY_FILE=/mykey, you'd add an option like the following to your docker run: `--mount type=bind,source=./myKey,target=/myKey`) |
| Set the data path | `--data-path [PATH]` | DATA_PATH | PATH | `/data` | Specify a directory for data. Frequently used with `docker run --mount` option (for example, if DATA_PATH=/usr/cosmos/data, you'd add an option like the following to your docker run: `--mount type=bind,source=./.local/data,target=/usr/cosmos/data`) |
| Specify the cert path to be used for https | `--cert-path [PATH]` | CERT_PATH | PATH | `<default cert>` | Specify a path to a certificate for securing traffic. You need to mount this file into the container (for example, if CERT_PATH=/mycert.pfx, you'd add an option like the following to your docker run: `--mount type=bind,source=./mycert.pfx,target=/mycert.pfx`) |
| Specify the cert secret to be used for https | N/A | CERT_SECRET | string | `<default secret>` | The secret for the certificate specified on CERT_PATH. |
| Set the log level | `--log-level [LEVEL]` | LOG_LEVEL | `quiet`, `error`, `warn`, `info`, `debug`, `trace` | `info` | The verbosity of logs that emitted by the emulator and data explorer. |
| Enable diagnostic info being sent to Microsoft | `--enable-telemetry` | ENABLE_TELEMETRY | `true`, `false` | `true` | Enable sending logs to Microsoft to help us improve the emulator. |

## Feature support

This emulator is in active development and preview. As a result, not all Azure Cosmos DB features are supported. Some features will also not be supported in the future. This table includes the state of various features and their level of support.

| Feature | Support |
|---|---|
| **Batch API** | ✅ Supported |
| **Bulk API** | ✅ Supported |
| **Change Feed** | ⚠️ Not yet implemented |
| **Create and read document with utf data** | ✅ Supported |
| **Create collection** | ✅ Supported |
| **Create collection twice conflict** | ✅ Supported |
| **Create collection with custom index policy** | ⚠️ Not yet implemented |
| **Create collection with ttl expiration** | ⚠️ Not yet implemented |
| **Create database** | ✅ Supported |
| **Create database twice conflict** | ✅ Supported |
| **Create document** | ✅ Supported |
| **Create partitioned collection** | ⚠️ Not yet implemented |
| **Delete collection** | ✅ Supported |
| **Delete database** | ✅ Supported |
| **Delete document** | ✅ Supported |
| **Get and change collection performance** | ⚠️ Not yet implemented |
| **Insert large document** | ✅ Supported |
| **Patch document** | ⚠️ Not yet implemented |
| **Query partitioned collection in parallel** | ⚠️ Not yet implemented |
| **Query with aggregates** | ⚠️ Not yet implemented |
| **Query with and filter** | ⚠️ Not yet implemented |
| **Query with and filter and projection** | ⚠️ Not yet implemented |
| **Query with equality** | ✅ Supported |
| **Query with equals on id** | ✅ Supported |
| **Query with joins** | ⚠️ Not yet implemented |
| **Query with order by** | ✅ Supported |
| **Query with order by for partitioned collection** | ⚠️ Not yet implemented |
| **Query with order by numbers** | ✅ Supported |
| **Query with order by strings** | ⚠️ Not yet implemented |
| **Query with paging** | ⚠️ Not yet implemented |
| **Query with range operators date times** | ⚠️ Not yet implemented |
| **Query with range operators on numbers** | ⚠️ Not yet implemented |
| **Query with range operators on strings** | ⚠️ Not yet implemented |
| **Query with single join** | ⚠️ Not yet implemented |
| **Query with string math and array operators** | ⚠️ Not yet implemented |
| **Query with subdocuments** | ⚠️ Not yet implemented |
| **Query with two joins** | ⚠️ Not yet implemented |
| **Query with two joins and filter** | ⚠️ Not yet implemented |
| **Read collection** | ✅ Supported |
| **Read collection feed** | ⚠️ Not yet implemented |
| **Read database** | ✅ Supported |
| **Read database feed** | ⚠️ Not yet implemented |
| **Read document** | ✅ Supported |
| **Read document feed** | ✅ Supported |
| **Replace document** | ✅ Supported |
| **Request Units** | ⚠️ Not yet implemented |
| **Stored procedures** | ❌ Not planned |
| **Triggers** | ❌ Not planned |
| **UDFs** | ❌ Not planned |
| **Update collection** | ⚠️ Not yet implemented |
| **Update document** | ✅ Supported |


## Limitations

In addition to features not yet supported or not planned, the following list includes current limitations of the emulator.

- The .NET SDK for Azure Cosmos DB doesn't support bulk execution in the emulator.
- The .NET and Java SDKs don't support HTTP mode in the emulator. 

## Installing certificates for Java SDK

When using the [Java SDK for Azure Cosmos DB](./nosql/sdk-java-v4.md) with this version of the emulator in https mode, it is necessary to install it's certificates to your local Java trust store.

### Get certificate

In a `bash` window, run the following: 

```bash
# If the emulator was started with /AllowNetworkAccess, replace localhost with the actual IP address of it:
EMULATOR_HOST=localhost
EMULATOR_PORT=8081
EMULATOR_CERT_PATH=/tmp/cosmos_emulator.cert
openssl s_client -connect ${EMULATOR_HOST}:${EMULATOR_PORT} </dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > $EMULATOR_CERT_PATH
```

### Install certificate

Navigate to the directory of your java installation where `cacerts` file is located (replace below with correct directory):

```bash
cd "C:/Program Files/Eclipse Adoptium/jdk-17.0.10.7-hotspot/bin"
```

Import the cert (you may be asked for a password, the default value is "changeit"):

```bash
keytool -cacerts -importcert -alias cosmos_emulator -file $EMULATOR_CERT_PATH
```

If you get an error because the alias already exists, delete it and then run the above again:

```bash
keytool -cacerts -delete -alias cosmos_emulator
```

## Reporting issues

If you encounter issues with using this version of the emulator, open an issue in the GitHub repository (<https://github.com/Azure/azure-cosmos-db-emulator-docker>) and tag it with the label `cosmosEmulatorVnextPreview`.
