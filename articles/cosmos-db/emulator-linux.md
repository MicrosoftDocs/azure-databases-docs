---
title: Linux-based emulator - vNext (preview)
titleSuffix: Azure Cosmos DB for NoSQL
description: Use the Azure Cosmos DB Linux-based emulator to test your applications against API for NoSQL endpoints.
author: Sajeetharan
ms.author: sasinnat
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 11/07/2024
# CustomerIntent: As a developer, I want to use the Linux-based Azure Cosmos DB emulator so that I can develop my application against a database during development.
appliesto:
  - ✅ NoSQL
---

# Linux-based emulator - vNext (preview)

The next generation of the Azure Cosmos DB emulator is entirely Linux-based and is available as a Docker container. It supports running on a wide variety of processors and operating systems.

> [!IMPORTANT]
> This version of the emulator only supports the API for NoSQL in [gateway mode](sdk-connection-modes.md#available-connectivity-modes), with a select subset of features. For more information, see [feature support](#feature-support).

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
| Customize the gateway public endpoint | `--gateway-endpoint` | GATEWAY_PUBLIC_ENDPOINT | N/A | `localhost` | The public gateway endpoint. Defaults to `localhost`. |
| Specify the key via file | `--key-file [PATH]` | KEY_FILE | PATH | `<default secret>` | Override default key with the key specified in the file. You need to mount this file into the container (for example, if KEY_FILE=/mykey, you'd add an option like the following to your docker run: `--mount type=bind,source=./myKey,target=/myKey`) |
| Set the data path | `--data-path [PATH]` | DATA_PATH | PATH | `/data` | Specify a directory for data. Frequently used with `docker run --mount` option (for example, if DATA_PATH=/usr/cosmos/data, you'd add an option like the following to your docker run: `--mount type=bind,source=./.local/data,target=/usr/cosmos/data`) |
| Specify the cert path to be used for https | `--cert-path [PATH]` | CERT_PATH | PATH | `<default cert>` | Specify a path to a certificate for securing traffic. You need to mount this file into the container (for example, if CERT_PATH=/mycert.pfx, you'd add an option like the following to your docker run: `--mount type=bind,source=./mycert.pfx,target=/mycert.pfx`) |
| Specify the cert secret to be used for https | N/A | CERT_SECRET | string | `<default secret>` | The secret for the certificate specified on CERT_PATH. |
| Set the log level | `--log-level [LEVEL]` | LOG_LEVEL | `quiet`, `error`, `warn`, `info`, `debug`, `trace` | `info` | The verbosity of logs that emitted by the emulator and data explorer. |
| Enable OpenTelemetry OTLP exporter | `--enable-otlp` | ENABLE_OTLP_EXPORTER | `true`, `false` | `false` | Enable OpenTelemetry integration. |
| Enable console exporter | `--enable-console` | ENABLE_CONSOLE_EXPORTER | `true`, `false` | `false` | Enable console output of telemetry data (useful for debugging). |
| Enable diagnostic info being sent to Microsoft | `--enable-telemetry` | ENABLE_TELEMETRY | `true`, `false` | `true` | Enable sending usage data to Microsoft to help us improve the emulator. |


## Feature support

This emulator is in active development and preview. As a result, not all Azure Cosmos DB features are supported. Some features will also not be supported in the future. This table includes the state of various features and their level of support.

| Feature | Support |
|---|---|
| **Batch API** | ✅ Supported |
| **Bulk API** | ✅ Supported |
| **Change Feed** | ✅ Supported |
| **Create and read document with utf data** | ✅ Supported |
| **Create collection** | ✅ Supported |
| **Create collection twice conflict** | ✅ Supported |
| **Create collection with custom index policy** | ⚠️ Not yet implemented |
| **Create collection with ttl expiration** | ✅ Supported  |
| **Create database** | ✅ Supported |
| **Create database twice conflict** | ✅ Supported |
| **Create document** | ✅ Supported |
| **Create partitioned collection** | ✅ Supported |
| **Delete collection** | ✅ Supported |
| **Delete database** | ✅ Supported |
| **Delete document** | ✅ Supported |
| **Get and change collection performance** | ⚠️ Not yet implemented |
| **Insert large document** | ✅ Supported |
| **Patch document** | ✅ Supported |
| **Query partitioned collection in parallel** | ⚠️ Not yet implemented |
| **Query with aggregates** | ✅ Supported |
| **Query with and filter** | ✅ Supported |
| **Query with and filter and projection** | ✅ Supported |
| **Query with equality** | ✅ Supported |
| **Query with equals on id** | ✅ Supported |
| **Query with joins** | ✅ Supported |
| **Query with order by** | ✅ Supported |
| **Query with order by for partitioned collection** | ✅ Supported |
| **Query with order by numbers** | ✅ Supported |
| **Query with order by strings** | ✅ Supported |
| **Query with paging** | ✅ Supported |
| **Query with range operators date times** | ✅ Supported |
| **Query with range operators on numbers** | ✅ Supported |
| **Query with range operators on strings** | ✅ Supported |
| **Query with single join** | ✅ Supported |
| **Query with string math and array operators** | ✅ Supported |
| **Query with subdocuments** | ✅ Supported |
| **Query with two joins** | ✅ Supported |
| **Query with two joins and filter** | ✅ Supported |
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

## Installing certificates for Java SDK

When using the [Java SDK for Azure Cosmos DB](sdk-java-v4.md) with this version of the emulator in https mode, it is necessary to install it's certificates to your local Java trust store.

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

## OpenTelemetry support

[OpenTelemetry](https://opentelemetry.io/) is an open-source observability framework that provides a collection of tools, APIs, and SDKs for instrumenting, generating, collecting, and exporting telemetry data. The OpenTelemetry Protocol (OTLP) is the protocol used by OpenTelemetry to transmit telemetry data between components.

You can use OpenTelemetry with the emulator to monitor and trace your application. The emulator supports telemetry options, which can be configured through environment variables or command-line flags when running the Docker container.

The emulator exports the following metrics. These are available through any metrics backend that supports OTLP and provides valuable insights into the database's performance and health:

- Request Rates: Shows the traffic patterns for different operation types
- Query Execution Times: Measures the time taken to execute different queries
- Resource Utilization: CPU, memory usage and connection pool metrics
- Error Rates: Tracking of errors by type and endpoint

Detailed instructions with examples [are available in the GitHub repository](https://github.com/Azure/azure-cosmos-db-emulator-docker/blob/master/docs/opentelemetry.md).

## Use in continuous integration workflow

There are lot of benefits to using Docker containers in CI/CD pipelines, especially for stateful systems like databases. This could be in terms of cost-effectiveness, performance, reliability and consistency of your test suites. 

The emulator can be incorporated as part CI/CD pipelines. You can refer to this [GitHub repository](https://github.com/AzureCosmosDB/cosmosdb-linux-emulator-github-actions) that provides examples of how to use the emulator as part of a GitHub Actions CI workflow for .NET, Python, Java, and Go applications on both `x64` and `ARM64` architectures (demonstrated for Linux runner using `ubuntu`).

Here is an example of a GitHub Actions CI workflow that shows how to configure the emulator as a [GitHub Actions service container](https://docs.github.com/en/actions/use-cases-and-examples/using-containerized-services/about-service-containers) as part of a job in the workflow. GitHub takes care of starting the Docker container and destroys it when the job completes, without the need for manual intervention (such as using the `docker run` command).

```yml
name: CI demo app

on:
  push:
    branches: [main]
    paths:
      - 'java-app/**'
  pull_request:
    branches: [main]
    paths:
      - 'java-app/**'

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    services:
      cosmosdb:
        image: mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview
        ports:
          - 8081:8081
        env:
          PROTOCOL: https
        
    env:
      COSMOSDB_CONNECTION_STRING: ${{ secrets.COSMOSDB_CONNECTION_STRING }}
      COSMOSDB_DATABASE_NAME: ${{ vars.COSMOSDB_DATABASE_NAME }}
      COSMOSDB_CONTAINER_NAME: ${{ vars.COSMOSDB_CONTAINER_NAME }}

    steps:

      - name: Set up Java
        uses: actions/setup-java@v3
        with:
          distribution: 'microsoft'
          java-version: '21.0.0'

      - name: Export Cosmos DB Emulator Certificate
        run: |

          sudo apt update && sudo apt install -y openssl

          openssl s_client -connect localhost:8081 </dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > cosmos_emulator.cert

          cat cosmos_emulator.cert

          $JAVA_HOME/bin/keytool -cacerts -importcert -alias cosmos_emulator -file cosmos_emulator.cert -storepass changeit -noprompt
      
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run tests
        run: cd java-app && mvn test
```

This job runs on an Ubuntu runner and uses the `mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview` Docker image as a service container. It uses environment variables to configure the connection string, database name, and container name. Since in this case the job is running directly on the GitHub Actions runner machine, the **Run tests** step in the job can access the emulator is accessible using `localhost:8081` (`8081` is the port exposed by the emulator).

The **Export Cosmos DB Emulator Certificate** step is specific to Java applications since the Azure Cosmos DB Java SDK currently doesn't support `HTTP` mode in emulator. The `PROTOCOL` environment variable is set to `https` in the `services` section and this step exports the emulator certificate and import it into the Java keystore. The same applies to .NET as well.

## Reporting issues

If you encounter issues with using this version of the emulator, open an issue in the GitHub repository (<https://github.com/Azure/azure-cosmos-db-emulator-docker>) and tag it with the label `cosmosEmulatorVnextPreview`.
