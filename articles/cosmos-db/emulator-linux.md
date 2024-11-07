---
title: Linux-based emulator (preview)
titleSuffix: Azure Cosmos DB for NoSQL
description: Use the Azure Cosmos DB Linux-based emulator to test your applications against API for NoSQL endpoints.
author: sajeetharan
ms.author: sasinnat
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

| | Support |
|---|---|
| **Create database** | ✅ Supported |
| **Read database** | ✅ Supported |
| **Delete database** | ✅ Supported |
| **Read database feed** | ✅ Supported |
| **Create database twice conflict** | ✅ Supported |
| **Create collection** | ✅ Supported |
| **Read collection** | ✅ Supported |
| **Update collection** | ✅ Supported |
| **Delete collection** | ✅ Supported |
| **Read collection feed** | ✅ Supported |
| **Create collection twice conflict** | ✅ Supported |
| **Create collection with custom index policy** | ✅ Supported |
| **Create collection with ttl expiration** | ✅ Supported |
| **Create partitioned collection** | ✅ Supported |
| **Get and change collection performance** | ✅ Supported |
| **Create document** | ✅ Supported |
| **Read document** | ✅ Supported |
| **Update document** | ✅ Supported |
| **Patch document** | ✅ Supported |
| **Delete document** | ✅ Supported |
| **Read document feed** | ✅ Supported |
| **Insert large document** | ✅ Supported |
| **Create and read document with utf data** | ✅ Supported |
| **Query with sql query spec** | ✅ Supported |
| **Query with equality** | ✅ Supported |
| **Query with and filter and projection** | ⚠️ Not yet implemented |
| **Query with and filter** | ⚠️ Not yet implemented |
| **Query with equals on id** | ✅ Supported |
| **Query with inequality** | ⚠️ Not yet implemented |
| **Query with range operators on numbers** | ⚠️ Not yet implemented |
| **Query with range operators on strings** | ⚠️ Not yet implemented |
| **Query with range operators date times** | ⚠️ Not yet implemented |
| **Query with order by** | ✅ Supported |
| **Query with order by numbers** | ✅ Supported |
| **Query with order by strings** | ⚠️ Not yet implemented |
| **Query with aggregates** | ⚠️ Not yet implemented |
| **Query with subdocuments** | ⚠️ Not yet implemented |
| **Query with joins** | ⚠️ Not yet implemented |
| **Query with two joins** | ⚠️ Not yet implemented |
| **Query with two joins and filter** | ⚠️ Not yet implemented |
| **Query with single join** | ⚠️ Not yet implemented |
| **Query with string math and array operators** | ⚠️ Not yet implemented |
| **Query with paging** | ⚠️ Not yet implemented |
| **Query partitioned collection in parallel** | ⚠️ Not yet implemented |
| **Query with order by for partitioned collection** | ⚠️ Not yet implemented |
| **Stored procedure** | ❌ Not planned |
| **Triggers** | ❌ Not planned |
| **UDFs** | ❌ Not planned |

## Limitations

In addition to features not yet supported or not planned, the following list includes current limitations of the emulator.

- The .NET SDK for Azure Cosmos DB doesn't support bulk execution in the emulator.
- The .NET SDK doesn't support HTTP mode in the emulator.

## Reporting issues

If you encounter issues with using this version of the emulator, open an issue in the GitHub repository (<https://github.com/Azure/azure-cosmos-db-emulator-docker>) and tag it with the label `cosmosEmulatorVnextPreview`.
