---
title: Spring Boot Application with Azure Kubernetes Service
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to deploy a Spring Boot application to Azure Kubernetes Service and perform CRUD operations on data in Azure Cosmos DB for NoSQL.
author: markjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: java
ms.topic: how-to
ms.date: 09/03/2025
ms.author: mjbrown
ms.custom: mode-api, devx-track-azurecli, build-2023, build-2023-dataai
appliesto:
  - ✅ NoSQL
---

# Spring Boot Application with Azure Cosmos DB for NoSQL and Azure Kubernetes Service

> [!NOTE]
> For Spring Boot applications, we recommend using Azure Spring Apps. However, you can still use Azure Kubernetes Service as a destination. See [Java Workload Destination Guidance](https://aka.ms/javadestinations) for advice.

In this tutorial, you set up and deploy a Spring Boot application that exposes REST APIs to perform CRUD operations on data in Azure Cosmos DB (API for NoSQL account). You package the application as Docker image, push it to Azure Container Registry, deploy to Azure Kubernetes Service and test the application.

## Prerequisites

- An Azure account with an active subscription. Create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) if you don't have an Azure subscription.
- [Java Development Kit (JDK) 8](/java/openjdk/download#openjdk-8). Point your `JAVA_HOME` environment variable to the path where the JDK is installed.
- [Azure CLI](/cli/azure/install-azure-cli) to create Azure services.
- [Docker](https://docs.docker.com/engine/install/) to manage images and containers.
- A recent version of [Maven](https://maven.apache.org/download.cgi) and [Git](https://www.git-scm.com/downloads).
- [curl](https://curl.se/download.html) to invoke REST APIs exposed the applications.

## Create Azure services

In this section, you create Azure services required for this tutorial.

- Azure Cosmos DB
- Azure Container Registry
- Azure Kubernetes Service

### Create a resource group for the Azure resources used in this tutorial

1. Sign in to your Azure account using Azure CLI:

   ```azurecli
   az login
   ```

1. Choose your Azure Subscription:

   ```azurecli
   az account set -s <enter subscription ID>
   ```

1. Create a resource group.

   ```azurecli
   az group create --name=cosmosdb-springboot-aks-rg --location=eastus
   ```

    > [!NOTE]
    > Replace `cosmosdb-springboot-aks-rg` with a unique name for your resource group.
    
### Create an Azure Cosmos DB for NoSQL database account

Use this command to create an [Azure Cosmos DB for NoSQL database account](manage-with-cli.md#create-an-azure-cosmos-db-account) using the Azure CLI.

```azurecli
az cosmosdb create --name <enter account name> --resource-group <enter resource group name>
```

### Create a private Azure Container Registry using the Azure CLI

> [!NOTE]
> Replace `cosmosdbspringbootregistry` with a unique name for your registry.

```azurecli
az acr create --resource-group cosmosdb-springboot-aks-rg --location eastus \
    --name cosmosdbspringbootregistry --sku Basic
```

### Create a Kubernetes cluster on Azure using the Azure CLI

1. The following command creates a Kubernetes cluster in the *cosmosdb-springboot-aks-rg* resource group, with *cosmosdb-springboot-aks* as the cluster name, with Azure Container Registry (ACR) `cosmosdbspringbootregistry` attached:

    ```azurecli
    az aks create \
        --resource-group cosmosdb-springboot-aks-rg \
        --name cosmosdb-springboot-aks \
        --node-count 1 \
        --generate-ssh-keys \
        --attach-acr cosmosdbspringbootregistry \
        --dns-name-prefix=cosmosdb-springboot-aks-app
    ```

    > [!NOTE]
    > This command might take a while to complete.

1. If you don't have `kubectl` installed, you can do so using the Azure CLI.

   ```azurecli
   az aks install-cli
   ```

1. Get access credentials for the Azure Kubernetes Service cluster.

   ```azurecli
   az aks get-credentials --resource-group=cosmosdb-springboot-aks-rg --name=cosmosdb-springboot-aks
   
   kubectl get nodes
   ```

## Build the application

1. Clone the application and change into the right directory.

    ```bash
    git clone https://github.com/Azure-Samples/cosmosdb-springboot-aks.git
    
    cd cosmosdb-springboot-aks
    ```

1. Use `Maven` to build the application. At the end of this step, you should have the application JAR file created in the `target` folder.

   ```bash
   ./mvnw install
   ```

## Run the application locally

If you intend to run the application on Azure Kubernetes Service, skip this section and move on to [Push Docker image to Azure Container Registry](#push-docker-image-to-azure-container-registry)

1. Before you run the application, update the `application.properties` file with the details of your Azure Cosmos DB account.

   ```properties
   azure.cosmos.uri=https://<enter Azure Cosmos DB db account name>.azure.com:443/
   azure.cosmos.key=<enter Azure Cosmos DB db primary key>
   azure.cosmos.database=<enter Azure Cosmos DB db database name>
   azure.cosmos.populateQueryMetrics=false
   ```

   > [!NOTE]
   > The database and container (called `users`) are created automatically once you start the application.

1. Run the application locally.

   ```bash
   java -jar target/*.jar
   ```

## Push Docker image to Azure Container Registry

1. Build the Docker image

   ```bash
   docker build -t cosmosdbspringbootregistry.azurecr.io/spring-cosmos-app:v1 .
   ```

   > [!NOTE]
   > Replace `cosmosdbspringbootregistry` with the name of your Azure Container Registry

1. Log into Azure Container Registry.

   ```azurecli
   az acr login -n cosmosdbspringbootregistry
   ```

1. Push image to Azure Container Registry and list it.

   ```azurecli
   docker push cosmosdbspringbootregistry.azurecr.io/spring-cosmos-app:v1

   az acr repository list --name cosmosdbspringbootregistry --output table
   ```

## Deploy application to Azure Kubernetes Service

1. Edit the `Secret` in `app.yaml` with the details of your Azure Cosmos DB setup.

    ```yml
    ...
    apiVersion: v1
    kind: Secret
    metadata:
      name: app-config
    type: Opaque
    stringData:
      application.properties: |
        azure.cosmos.uri=https://<enter Azure Cosmos DB db account name>.azure.com:443/
        azure.cosmos.key=<enter Azure Cosmos DB db primary key>
        azure.cosmos.database=<enter Azure Cosmos DB db database name>
        azure.cosmos.populateQueryMetrics=false
    ...
    ```

    > [!NOTE]
    > The database and a container (`users`) are created automatically once you start the application.

1. Deploy to Kubernetes and wait for the `Pod` to transition to `Running` state:

    ```bash
    kubectl apply -f deploy/app.yaml

    kubectl get pods -l=app=spring-cosmos-app -w
    ```

   > [!NOTE]
   > You can check application logs using: `kubectl logs -f $(kubectl get pods -l=app=spring-cosmos-app -o=jsonpath='{.items[0].metadata.name}') -c spring-cosmos-app`

## Access the application

If the application is running in Kubernetes and you want to access it locally over port `8080`, run this command:

```bash
kubectl port-forward svc/spring-cosmos-app-internal 8080:8080
```

Test the application by invoking the REST endpoints. You can also navigate to the `Data Explorer` menu of the Azure Cosmos DB account in the Azure portal and access the `users` container to confirm the result of the operations.

1. Create new users

    ```bash
    curl -i -X POST -H "Content-Type: application/json" -d '{"email":"john.doe@foobar.com", "firstName": "John", "lastName": "Doe", "city": "NYC"}' http://localhost:8080/users
    
    curl -i -X POST -H "Content-Type: application/json" -d '{"email":"mr.jim@foobar.com", "firstName": "mr", "lastName": "jim", "city": "Seattle"}' http://localhost:8080/users
    ```
    
    If successful, you should get an HTTP `201` response.

1. Update a user

    ```bash
    curl -i -X POST -H "Content-Type: application/json" -d '{"email":"john.doe@foobar.com", "firstName": "John", "lastName": "Doe", "city": "Dallas"}' http://localhost:8080/users
    ```

1. List all users

    ```bash
    curl -i http://localhost:8080/users
    ```

1. Get an existing user

    ```bash
    curl -i http://localhost:8080/users/john.doe@foobar.com
    ```
    
    You should get back a JSON payload with the user details. For example:
    
    ```json
    {
      "email": "john.doe@foobar.com",
      "firstName": "John",
      "lastName": "Doe",
      "city": "Dallas"
    }
    ```

1. Try to get a user that doesn't exist

    ```bash
    curl -i http://localhost:8080/users/not.there@foobar.com
    ```
    
    You should receive an HTTP `404` response.

1. Replace a user

    ```bash
    curl -i -X PUT -H "Content-Type: application/json" -d '{"email":"john.doe@foobar.com", "firstName": "john", "lastName": "doe","city": "New Jersey"}' http://localhost:8080/users/
    ```

1. Try to replace user that doesn't exist

    ```bash
    curl -i -X PUT -H "Content-Type: application/json" -d '{"email":"not.there@foobar.com", "firstName": "john", "lastName": "doe","city": "New Jersey"}' http://localhost:8080/users/
    ```
        
    You should receive an HTTP `404` response.

1. Delete a user

    ```bash
    curl -i -X DELETE http://localhost:8080/users/mr.jim@foobar.com
    ```

1. Delete a user that doesn't exist

    ```bash
    curl -X DELETE http://localhost:8080/users/go.nuts@foobar.com
    ```
    
    You should receive an HTTP `404` response.

### Access the application using a public IP address (optional)

Creating a Service of type `LoadBalancer` in Azure Kubernetes Service results in an Azure Load Balancer getting provisioned. You can then access the application using its public IP address. 

1. Create a Kubernetes Service of type `LoadBalancer`

    > [!NOTE]
    > This step creates an Azure Load Balancer with a public IP address.

    ```bash
    kubectl apply -f deploy/load-balancer-service.yaml
    ```

1. Wait for the Azure Load Balancer to get created. Until then, the `EXTERNAL-IP` for the Kubernetes Service remains in `<pending>` state.

    ```bash
    kubectl get service spring-cosmos-app -w
    
    NAME                TYPE           CLUSTER-IP   EXTERNAL-IP   PORT(S)          AGE
    spring-cosmos-app   LoadBalancer   10.0.68.83   <pending>     8080:31523/TCP   6s
    ```

    > [!NOTE]
    > `CLUSTER-IP` value might differ in your case

1. Once Azure Load Balancer creation completes, the `EXTERNAL-IP` is available.

    ```bash
    NAME                TYPE           CLUSTER-IP   EXTERNAL-IP   PORT(S)          AGE
    spring-cosmos-app   LoadBalancer   10.0.68.83   20.81.108.180   8080:31523/TCP   18s
    ```
   
   > [!NOTE]
   > `EXTERNAL-IP` value might differ in your case

1. Use the public IP address

   Terminate the `kubectl watch` process and repeat the previous `curl` commands with the public IP address along with port `8080`. For example, to list all users:

   ```bash
    curl -i http://20.81.108.180:8080/users
   ```
    
   > [!NOTE]
   > Replace `20.81.108.180` with the public IP address for your environment

## Kubernetes resources for the application

Here are some of the key points related to the Kubernetes resources for this application:

- The Spring Boot application is a Kubernetes `Deployment` based on the [Docker image in Azure Container Registry](https://github.com/Azure-Samples/cosmosdb-springboot-aks/blob/main/deploy/app.yaml#L21)
- Azure Cosmos DB configuration is mounted in `application.properties` at path `/config` [inside the container](https://github.com/Azure-Samples/cosmosdb-springboot-aks/blob/main/deploy/app.yaml#L26).
- This mount is made possible using a [Kubernetes `Volume`](https://github.com/Azure-Samples/cosmosdb-springboot-aks/blob/main/deploy/app.yaml#L15) that in turn refers to a [Kubernetes Secret](https://github.com/Azure-Samples/cosmosdb-springboot-aks/blob/main/deploy/app.yaml#L49), which was created along with the application. You can run this command to confirm that this file is present within the application container:

    ```bash
    kubectl exec -it $(kubectl get pods -l=app=spring-cosmos-app -o=jsonpath='{.items[0].metadata.name}') -c spring-cosmos-app -- cat /config/application.properties
    ```

- [Liveness and Readiness probes](https://github.com/Azure-Samples/cosmosdb-springboot-aks/blob/main/deploy/app.yaml#L34) configuration for this application refer to the HTTP endpoints that are made available by [Spring Boot Actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html) when a Spring Boot application is [deployed to a Kubernetes environment](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.endpoints.kubernetes-probes) - `/actuator/health/liveness` and `/actuator/health/readiness`. 
- A [ClusterIP Service](https://github.com/Azure-Samples/cosmosdb-springboot-aks/blob/main/deploy/app.yaml#L61) can be created to access the REST endpoints of the Spring Boot application *internally* within the Kubernetes cluster.
- A [LoadBalancer Service](https://github.com/Azure-Samples/cosmosdb-springboot-aks/blob/main/deploy/load-balancer-service.yaml) can be created to access the application via a public IP address.

## Clean up resources

[!INCLUDE [cosmosdb-delete-resource-group](../includes/cosmos-db-delete-resource-group.md)]

## Next step

> [!div class="nextstepaction"]
> [Spring Data Azure Cosmos DB v3 for API for NoSQL](sdk-java-spring-data-v3.md)
