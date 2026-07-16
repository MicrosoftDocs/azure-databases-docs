---
title: Update Application Client Certificates in Azure Database for PostgreSQL Flexible Server
description: Learn about updating Java clients with Azure Database for PostgreSQL flexible server using TLS.
#customer intent: As a user, I want to update the trusted root certificates in my keystore, so that my application can maintain a secure TLS connection.
author: Tameika-MSFT
ms.author: talawren
ms.reviewer: maghan
ms.date: 07/14/2026
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
---

# Update application client certificates in Azure Database for PostgreSQL flexible server

When you connect applications to Azure Database for PostgreSQL, the application client must install trusted root certificates. The following sections guide you through updating the trusted root certificates for applications. This process is a common scenario for applications connecting to an Azure Database for PostgreSQL flexible server.

[!INCLUDE [certificate-rotation](includes/certificate-rotation.md)]

## Import root CA certificates in Java key store on the client, for certificate pinning scenarios

Custom-written Java applications use a default keystore, called `cacerts`, which contains trusted certificate authority (CA) certificates. It's also often known as Java trust store. A certificates file named `cacerts` resides in the security properties directory, `java.home\lib\security`, where `java.home` is the runtime environment directory (the `jre` directory in the SDK or the top-level directory of the Java™ 2 Runtime Environment).
To update client root CA certificates for client certificate pinning scenarios with PostgreSQL, use the following directions:

1. Check the `cacerts` Java keystore to see if it already contains required certificates. You can list certificates in Java keystore by using the following command:

    ```powershell
      keytool -list -v -keystore ..\lib\security\cacerts > outputfile.txt
    ```
    
    If the necessary certificates aren't present in the Java key store on the client, as you can check in the output, proceed with the following directions:

1. Make a backup copy of your custom keystore.

1. Download [certificates](security-tls.md), and save them locally where you can reference them.

1. Generate a combined CA certificate store that includes all needed root CA certificates. The following example shows using `DefaultJavaSSLFactory` for PostgreSQL JDBC users.

    ```powershell
        keytool -importcert -alias PostgreSQLServerCACert  -file D:\ DigiCertGlobalRootG2.crt.pem   -keystore truststore -storepass password -noprompt
    
        keytool -importcert -alias PostgreSQLServerCACert2  -file "D:\ Microsoft ECC Root Certificate Authority 2017.crt.pem" -keystore truststore -storepass password  -noprompt
    
        keytool -importcert -alias PostgreSQLServerCACert  -file D:\ DigiCertGlobalRootCA.crt.pem   -keystore truststore -storepass password -noprompt
    ```

1. Replace the original keystore file with the new generated one:

    ```java
    System.setProperty("javax.net.ssl.trustStore","path_to_truststore_file");
    System.setProperty("javax.net.ssl.trustStorePassword","password");
    ```

1. Replace the original root CA PEM file with the combined root CA file and restart your application or client.

    For more information on configuring client certificates with PostgreSQL JDBC driver, see this [documentation](https://jdbc.postgresql.org/documentation/ssl/).

    > [!NOTE]  
    > To import certificates to client certificate stores, you might have to convert certificate .crt files to .pem format. You can use **[OpenSSL utility to do these file conversions](../security/security-tls.md)**.

## Get a list of trusted certificates in Java Key Store programmatically

By default, Java stores the trusted certificates in a special file named `cacerts` that is located inside the Java installation folder on the client.
The following example reads `cacerts` and loads it into a **KeyStore** object:

```java
private KeyStore loadKeyStore() {
    String relativeCacertsPath = "/lib/security/cacerts".replace("/", File.separator);
    String filename = System.getProperty("java.home") + relativeCacertsPath;
    FileInputStream is = new FileInputStream(filename);
    KeyStore keystore = KeyStore.getInstance(KeyStore.getDefaultType());
    String password = "changeit";
    keystore.load(is, password.toCharArray());

    return keystore;
}
```

The default password for `cacerts` is `changeit`, but it should be different on a real client, as administrators recommend changing the password immediately after Java installation.
After you load the **KeyStore** object, use the **PKIXParameters** class to read the certificates present.

```java
public void whenLoadingCacertsKeyStore_thenCertificatesArePresent() {
    KeyStore keyStore = loadKeyStore();
    PKIXParameters params = new PKIXParameters(keyStore);
    Set<TrustAnchor> trustAnchors = params.getTrustAnchors();
    List<Certificate> certificates = trustAnchors.stream()
      .map(TrustAnchor::getTrustedCert)
      .collect(Collectors.toList());

    assertFalse(certificates.isEmpty());
}
```

## Update root CA certificates when using clients in Azure App Services, for certificate pinning scenarios

For Azure App Services connecting to an Azure Database for PostgreSQL flexible server, two possible scenarios exist for updating client certificates. The scenario depends on how you're using SSL with your application deployed to Azure App Services.

- The platform adds new certificates to App Service before changes occur in your Azure Database for PostgreSQL flexible server. If you're using the SSL certificates included on App Service platform in your application, no action is needed. For more information, see [Add and manage TLS/SSL certificates in Azure App Service](/azure/app-service/configure-ssl-certificate) in the Azure App Service documentation.
- If you're explicitly including the path to SSL certificate file in your code, you need to download the new certificate and update the code to use it. A good example of this scenario is when you use custom containers in App Service as described in the [Tutorial: Configure a sidecar container for custom container in Azure App Service](/azure/app-service/tutorial-multi-container-app#configure-database-variables-in-wordpress) in the Azure App Service documentation.

## Update root CA certificates when using clients in Azure Kubernetes Service (AKS), for certificate pinning scenarios

If you're trying to connect to the Azure Database for PostgreSQL using applications hosted in Azure Kubernetes Services (AKS) and pinning certificates, it's similar to access from a dedicated customer's host environment. Refer to the steps [here](/azure/aks/ingress-tls).

## Update root CA certificates for .NET (Npgsql) users on Windows, for certificate pinning scenarios

For .NET (Npgsql) users on Windows connecting to Azure Database for PostgreSQL flexible server, make sure **all three** Microsoft RSA Root Certificate Authority 2017, DigiCert Global Root G2, and DigiCert Global Root CA all exist in Windows Certificate Store, Trusted Root Certification Authorities. If any certificates don't exist, import the missing certificate.

## Update root CA certificates for other clients, for certificate pinning scenarios

For other PostgreSQL client users, you can merge two CA certificate files by using the following format:

```output
-----BEGIN CERTIFICATE-----
(Root CA1: DigiCertGlobalRootCA.crt.pem)
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
(Root CA2: Microsoft ECC Root Certificate Authority 2017.crt.pem)
-----END CERTIFICATE-----
```

## Related content

- [Security in Azure Database for PostgreSQL](../security/security-overview.md)
