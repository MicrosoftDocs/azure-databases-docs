---
title: Enable LDAP Authentication in Azure Managed Instance for Apache Cassandra
description: Learn how to enable LDAP authentication in Azure Managed Instance for Apache Cassandra in your clusters and datacenters.
author: TheovanKraay
ms.author: thvankra
ms.service: azure-managed-instance-apache-cassandra
ms.topic: how-to
ms.date: 06/05/2025
ms.custom: sfi-image-nochange, sfi-ropc-blocked
#customer intent: As a database administrator, I want to set up LDAP authentication in Azure Managed Instance for Apache Cassandra.
---

# Enable LDAP authentication in Azure Managed Instance for Apache Cassandra

Azure Managed Instance for Apache Cassandra provides automated deployment and scaling operations for managed open-source Apache Cassandra datacenters. This article discusses how to enable Lightweight Directory Access Protocol (LDAP) authentication to your clusters and datacenters.

> [!IMPORTANT]
> LDAP authentication is in public preview.
>
> This feature is provided without a service-level agreement. We don't recommend it for production workloads. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## Prerequisites

- If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.
- An Azure Managed Instance for Apache Cassandra cluster. For more information, see [Create an Azure Managed Instance for Apache Cassandra cluster from the Azure portal](create-cluster-portal.md).

## Deploy an LDAP server in Azure

In this section, you create a simple LDAP server on a virtual machine in Azure. If you already have an LDAP server running, you can skip ahead to [Enable LDAP authentication](ldap.md#enable-ldap-authentication).

1. Deploy a virtual machine in Azure by using Ubuntu Server 18.04 Long-Term Support (LTS). For detailed instructions, see [Deploy an Ubuntu server](visualize-prometheus-grafana.md#deploy-an-ubuntu-server).

1. Give your server a Domain Name System (DNS) name.

   :::image type="content" source="./media/ldap/dns.jpg" alt-text="Screenshot that shows the virtual machine DNS name in the Azure portal." lightbox="./media/ldap/dns.jpg" border="true":::

1. Install Docker on the virtual machine. For a tutorial, see [Install and use Docker on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04).

1. In the home directory, copy and paste the following text and select **Enter**. This command creates a file that contains a test LDAP user account.

    ```shell
    mkdir ldap-user && cd ldap-user && cat >> user.ldif <<EOL
    dn: uid=admin,dc=example,dc=org
    uid: admin
    cn: admin
    sn: 3
    objectClass: top
    objectClass: posixAccount
    objectClass: inetOrgPerson
    loginShell: /bin/bash
    homeDirectory: /home/admin
    uidNumber: 14583102
    gidNumber: 14564100
    userPassword: admin
    mail: admin@example.com
    gecos: admin
    EOL 
    ```

1. Go back to the home directory.

    ```shell
    cd ..
    ```

1. Run the following command. Replace `<dnsname>` with the DNS name that you created for your LDAP server earlier. This command deploys an LDAP server with Transport Layer Security (TLS) enabled to a Docker container and copies the user file that you created earlier to the container.  

    ```shell
    sudo docker run --hostname <dnsname>.uksouth.cloudapp.azure.com --name <dnsname> -v $(pwd)/ldap-user:/container/service/slapd/assets/test --detach osixia/openldap:1.5.0
    ```

1. Copy out the certificates folder from the container. Replace `<dnsname>` with the DNS name that you created for your LDAP server.

    ```shell
    sudo docker cp <dnsname>:/container/service/slapd/assets/certs certs
    ```

1. Verify that the DNS name is correct.

    ```shell
    openssl x509 -in certs/ldap.crt -text
    ```

   :::image type="content" source="./media/ldap/dns-verify.jpg" alt-text="Screenshot that shows output from the command to verify the certificate." lightbox="./media/ldap/dns-verify.jpg" border="true":::

1. Copy the `ldap.crt` file to [clouddrive](/azure/cloud-shell/persisting-shell-storage) in the Azure CLI for use later.

1. Add the user to the LDAP. Replace `<dnsname>` with the DNS name that you created for your LDAP server.

    ```shell
    sudo docker container exec <dnsname> ldapadd -H ldap://<dnsname>.uksouth.cloudapp.azure.com -D "cn=admin,dc=example,dc=org" -w admin -f /container/service/slapd/assets/test/user.ldif
    ```

## Enable LDAP authentication

> [!IMPORTANT]
> If you skipped the previous section because you already have an LDAP server, be sure that it has server Secure Sockets Layer certificates enabled. The `subject alternative name (dns name)` specified for the certificate must also match the domain of the server that LDAP is hosted on, or authentication fails.

1. Currently, LDAP authentication is a public preview feature. Run the following command to add the required Azure CLI extension:

   ```azurecli-interactive
   az extension add --upgrade --name cosmosdb-preview
   ```

1. Set the authentication method to `Ldap` on the cluster. Replace `<resource group>` and `<cluster name>` with the appropriate values.

   ```azurecli-interactive
   az managed-cassandra cluster update -g <resource group> -c <cluster name> --authentication-method "Ldap"
   ```

1. Now set properties at the datacenter level. Replace `<resource group>` and `<cluster name>` with the appropriate values. Replace `<dnsname>` with the DNS name that you created for your LDAP server.

   The following command is based on the LDAP setup in the earlier section. If you skipped that section because you already have an existing LDAP server, provide the corresponding values for that server instead. Ensure that you uploaded a certificate file like `ldap.crt` to your [cloud drive](/azure/cloud-shell/persisting-shell-storage) in the Azure CLI.

   ```azurecli-interactive
   ldap_search_base_distinguished_name='dc=example,dc=org'
   ldap_server_certificates='/usr/csuser/clouddrive/ldap.crt'
   ldap_server_hostname='<dnsname>.uksouth.cloudapp.azure.com'
   ldap_service_user_distinguished_name='cn=admin,dc=example,dc=org'
   ldap_service_user_password='admin'
    
   az managed-cassandra datacenter update -g `<resource group>` -c `<cluster name>` -d datacenter-1 \
     --ldap-search-base-dn $ldap_search_base_distinguished_name \
     --ldap-server-certs $ldap_server_certificates \
     --ldap-server-hostname $ldap_server_hostname \
     --ldap-service-user-dn $ldap_service_user_distinguished_name \
     --ldap-svc-user-pwd $ldap_service_user_password
   ```

1. After this command finishes, you should be able to use [CQLSH](https://cassandra.apache.org/doc/stable/cassandra/managing/tools/cqlsh.html) or any Apache Cassandra open-source client driver to connect to your managed instance datacenter with the user added in the previous step.

   ```shell
   export SSL_VALIDATE=false
   cqlsh --debug --ssl <data-node-ip> -u <user> -p <password>
   ```

## Related content

- [LDAP authentication with Microsoft Entra ID](/azure/active-directory/fundamentals/auth-ldap)
- [Manage Azure Managed Instance for Apache Cassandra resources by using the Azure CLI](manage-resources-cli.md)
- [Deploy a Managed Apache Spark Cluster with Azure Databricks](deploy-cluster-databricks.md)
