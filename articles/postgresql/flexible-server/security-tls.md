---
title: Transport Layer Security (TLS) in Azure Database for PostgreSQL overview
description: Learn about secure connectivity with an Azure Database for PostgreSQL flexible server instance using TLS.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 12/02/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: concept-article
ms.custom:
  - sfi-image-nochange
  - horz-security
  -

---
# fix content to keep this link working: https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/security-tls#certificate-pinning-issues


# Transport Layer Security (TLS) in Azure Database for PostgreSQL

## Introduction

Azure Database for PostgreSQL requires all client connections to use Transport Layer Security (TLS), an industry-standard protocol that encrypts communications between your database server and client applications. TLS supersedes the older SSL protocol, with only TLS versions 1.2 and 1.3 recognized as secure. The integrity of TLS security relies on three pillars:

1. Using only TLS versions 1.2 or 1.3.
2. Client validates the server's TLS certificate issued by a Certificate Authority (CA) in a chain of CAs started by a trusted root CA.
3. Negotiating a secure cipher suite between server and client.

## Trusted root certs and cert rotations

[!INCLUDE [certificate-rotation](includes/certificate-rotation.md)]


### Root CAs used by Azure Database for PostgreSQL

Root CAs are the top-level authorities in the certificate chain. Azure Database for PostgreSQL currently uses dual-signed certificates issued by an ICA anchored by the following root CAs:

- [DigiCert Global Root G2](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt)
- [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt)

China regions currently use the following CAs:

- [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt)
- [DigiCert Global Root CA](https://cacerts.digicert.com/DigiCertGlobalRootCA.crt)
- After Spring Festival (Chinese New Year) 2026: [Digicert Global Root G2](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt). We recommend that you prepare for this change in advance by adding the new root CA to your trusted root store.

### About Intermediate CAs and server certificate rotations

Azure Database for PostgreSQL uses intermediate CAs (ICAs) to issue server certificates. Microsoft periodically rotates these ICAs and the server certificates they issue to maintain security. These rotations are routine and not announced in advance.

The current rotation of intermediate CAs for `DigiCert Global Root CA` (see [Certificate rotation above](#trusted-root-certs-and-cert-rotations)) started in November 2025 and scheduled to be completed in Q1 of 2026 replaces intermediate CAs as follows. If you followed the recommended practices below then this change requires no changes in your environment.

#### Old CA chain

This information is provided for reference only. Do not use intermediate CAs or server certificates in your trusted root store.

- `DigiCert Global Root G2`
  - `Microsoft Azure RSA TLS Issuing CA 03 / 04 / 07 / 08`
    - Server certificate

#### New CA chain

This information is provided for reference only. Do not use intermediate CAs or server certificates in your trusted root store.

- `DigiCert Global Root G2`
  - `Microsoft TLS RSA Root G2`
    - `Microsoft TLS G2 RSA CA OCSP 02 / 04 / 06 / 08 / 10 / 12 / 14 / 16`
      - Server certificate

### Read replicas

With root CA migration from [DigiCert Global Root CA](https://cacerts.digicert.com/DigiCertGlobalRootCA.crt) to [DigiCert Global Root G2](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt) not completed in all regions, it's possible for newly created read replicas to be on a newer root CA certificate than the primary server. Therefore, you should add [DigiCert Global Root CA](https://cacerts.digicert.com/DigiCertGlobalRootCA.crt) to the read replicas trusted store.

### Certificate chains

A certificate chain is a hierarchical sequence of certificates issued by trusted Certificate Authorities (CAs), starting at the root CA which issues intermediate CA (ICA) certificates. ICAs may issue certificates for lower ICAs. The lowest ICA in the chain will issue individual server certificates. The chain of trust is established by verifying each certificate in the chain up to the root CA certificate.

### Reducing connection failures

Utilizing recommended TLS configurations helps reduce the risk of connection failures due to certificate rotations or changes in intermediate CAs. Specifically, avoid trusting intermediate CAs or individual server certificates, as these practices can lead to unexpected connection issues when Microsoft updates the certificate chain.

> [!IMPORTANT]
> Changes in root CAs are announced ahead of time to help you prepare your client applications; however, server certificate rotations and changes to intermediate CAs are routine and therefore not announced.

> [!CAUTION]
> Using ***[unsupported (client) configurations](#trusted-root-certs-and-cert-rotations)*** will cause unexpected connection failures.

## Recommended configurations for TLS

### Best configuration

- Set the `ssl_min_protocol_version` server parameter to `TLSv1.3` to enforce the latest, most secure TLS version.
- Use `sslmode=verify-all` for PostgreSQL connections to ensure full certificate and hostname verification. Depending on your DNS configuration with Private Endpoints or VNET integration, `verify-all` might not be possible; therefore you may use `verify-ca` instead.
- Always maintain the [complete set of Azure root certificates in your trusted root store](https://learn.microsoft.com/azure/security/fundamentals/azure-ca-details?tabs=root-and-subordinate-cas-list#certificate-authority-details).

### Good configuration

- Set the `ssl_min_protocol_version` server parameter to `TLSv1.3`. If you must support TLS 1.2, do not set the minimal version.
- Use `sslmode=verify-all` or `sslmode=verify-ca` for PostgreSQL connections to ensure full or partial certificate verification.
- Ensure that the trusted root store contains the root CA certificate currently used by Azure Database for PostgreSQL:
  - [DigiCert Global Root G2](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt)
  - [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt)

### Supported, not recommended

We strongly advise against the following configurations:

- Disable TLS completely by setting `require_secure_transport` to `OFF` and setting the client-side to `sslmode=disable`.
- Using client-side `sslmode` settings `disable`, `allow`, `prefer` or `require` since they do not authenticate the server.

### Unsupported configurations; do **not** use

Azure PostgreSQL does not announce changes about intermediate CA changes or individual server certificate rotations; therefore, the following configurations are unsupported when using `sslmode` settings `verify-ca` or `verify-all`:

- You use intermediate CA certificates in your trusted store.
- You use certificate pinning, such as, using individual server certificates in your trusted store.

> [!CAUTION]
> Your applications will fail to connect to the database servers without warning whenever Microsoft changes the certificate chain’s intermediate CAs or rotates the server certificate.

### Certificate pinning issues

> [!NOTE]
> If you are not using sslmode=verify-full or sslmode=verify-ca settings in your client application connection string, then certificate rotations don't affect you. Therefore, you don't need to follow the steps in this section.

Never use certificate pinning in your applications since it breaks certificate rotation such as the current certificate change of intermediate CAs. If you don't know what certificate pinning is, it is unlikely that you are using it. To check for [certificate pinning](/azure/security/fundamentals/certificate-pinning), perform the following steps:

1. Produce your list of certificates that are in your trusted root store. Examples can be found in these articles:
    1. [Combine and update root CA certificates for Java applications](security-tls-how-to-connect#combine-and-update-root-ca-certificates-for-java-applications).
    1. Open the trusted root store on your client machine export the list of certificates.
1. You are using certificate pinning if you have intermediate CA certificates or individual PostgreSQL server certificates in your trusted root store.
1. To remove certificate pinning, remove all the certificates from your trusted root store and add the [recommended root CA certificates](#recommended-configurations-for-tls).

If you are experiencing issues due to the intermediate certificate even after following these steps, contact [Microsoft support](/azure-portal/supportability/how-to-create-azure-support-request). Include in the title ICA Rotation 2026.

## Other considerations for TLS

### Insecure and secure TLS versions

Several government entities worldwide maintain guidelines for TLS regarding network security. In the United States, these organizations include the Department of Health and Human Services and the National Institute of Standards and Technology. The level of security that TLS provides is most affected by the TLS protocol version and the supported cipher suites.

Azure Database for PostgreSQL supports TLS version 1.2 and 1.3. In RFC 8996, the Internet Engineering Task Force (IETF) explicitly states that TLS 1.0 and TLS 1.1 must not be used. Both protocols were deprecated by the end of 2019.
All incoming connections that use earlier insecure versions of the TLS protocol, such as TLS 1.0 and TLS 1.1, are denied by default.

The IETF released the TLS 1.3 specification in RFC 8446 in August 2018, and TLS 1.3 is the recommended version since it is faster and more secure than TLS 1.2.

Although we don't recommend it, if needed, you can disable TLS for connections to your Azure Database for PostgreSQL. You can update the `require_secure_transport` server parameter to `OFF`.

> [!IMPORTANT]
> We strongly recommend that you use the latest versions of TLS 1.3 to encrypt your database connections. You can specify the minimal TLS version by setting the `ssl_min_protocol_version` server parameter to `TLSv1.3`. Do not set the `ssl_max_protocol_version` server parameter.

### Cipher suites

A [cipher suite](https://en.wikipedia.org/wiki/Cipher_suite) is a set of algorithms that include a cipher, a key-exchange algorithm, and a hashing algorithm. They're used together with the TLS certificate and the TLS version to establish a secure TLS connection. Most TLS clients and servers support multiple cipher suites and sometimes multiple TLS versions.
During the establishment of the connection, the client and server [negotiate the TLS version and cipher suite to use through a handshake](https://en.wikipedia.org/wiki/Cipher_suite#Full_handshake:_coordinating_cipher_suites). During this handshake the following occurs:

- Client sends a list of acceptable cipher suites.
- Server selects the best (by its own definition) cipher suite from the list and informs the client of the choice.

### TLS features not available in Azure Database for PostgreSQL

At this time, Azure Database for PostgreSQL doesn't implement the following TLS features:

- TLS certificate-based client authentication through TLS with mutual authentication (mTLS).
- Custom server certificates (bring your own TLS certificates).

## Related content

- [Configure TLS client settings to connect to Azure Database for PostgreSQL](security-connect-tls.md)
- [Validating client configuration and troubleshooting connection failures](security-tls-validation-and-troubleshooting.md)
