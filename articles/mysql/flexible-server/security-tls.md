---
title: Transport Layer Security (TLS) in Azure Database for MySQL Overview
description: Learn about secure connectivity with an Azure Database for MySQL flexible server instance using TLS.
author: techlake
ms.author: hganten
ms.reviewer: maghan, randolphwest
ms.date: 01/07/2026
ms.service: azure-database-mysql
ms.subservice: security
ms.topic: concept-article
ms.custom:
  - horz-security
  - references_regions
---

# Transport Layer Security (TLS) in Azure Database for MySQL

Azure Database for MySQL requires all client connections to use Transport Layer Security (TLS), an industry-standard protocol that encrypts communications between your database server and client applications. TLS supersedes the older SSL protocol, with only TLS versions 1.2 and 1.3 recognized as secure. The integrity of TLS security relies on three pillars:

- Using only TLS versions 1.2 or 1.3.
- Client validates the server's TLS certificate issued by a Certificate Authority (CA) in a chain of CAs started by a trusted root CA.
- Negotiating a secure cipher suite between server and client.

## TLS Configurations in Azure Database for MySQL Flexible Server

Azure Database for MySQL Flexible Server supports connecting your client applications to the Azure Database for MySQL Flexible Server instance using Secure Sockets Layer (SSL) with Transport layer security (TLS) encryption. TLS is an industry-standard protocol that ensures encrypted network connections between your database server and client applications, allowing you to adhere to compliance requirements.

Azure Database for MySQL Flexible Server supports encrypted connections using Transport Layer Security (TLS 1.2) by default, and all incoming connections with TLS 1.0 and TLS 1.1 are denied by default. The encrypted connection enforcement or TLS version configuration on your Flexible Server can be configured and changed.

Following are the different configurations of SSL and TLS settings you can have for your Flexible Server:

> [!IMPORTANT]  
> According to [Removal of Support for the TLS 1.0 and TLS 1.1 Protocols](https://dev.mysql.com/doc/refman/8.0/en/encrypted-connection-protocols-ciphers.html#encrypted-connection-deprecated-protocols), we previously planned to fully deprecate TLS 1.0 and 1.1 by September 2024. However, due to dependencies identified by some customers, we decided to extend the timeline.
>
> - Starting on August 31, 2025, we began the forced upgrade for all servers still using TLS 1.0 or 1.1. After this date, any connections relying on TLS 1.0 or 1.1 might stop working at any time.
>
> To avoid service disruptions, we recommend that customers complete their migration to TLS 1.2 as soon as possible to avoid service disruptions.

| Scenario | Server parameter settings | Description |
| --- | --- | --- |
| Disable TLS enforcement | `require_secure_transport = OFF` | If your legacy application doesn't support encrypted connections, you can disable enforcement of encrypted connections. |
| Enforce TLS with TLS version < 1.2 (deprecated in September 2024) | `require_secure_transport = ON` and `tls_version = TLS 1.0` or `TLS 1.1` | No longer available! |
| Enforce TLS with TLS version = 1.2(Default configuration) | `require_secure_transport = ON` and `tls_version = TLS 1.2` | Default configuration. |
| Enforce TLS with TLS version = 1.3 | `require_secure_transport = ON` and `tls_version = TLS 1.3` | Recommended configuration; supported only with Azure Database for MySQL Flexible Server version v8.0 and later. |

> [!NOTE]  
> Changes to TLS Cipher aren't supported. FIPS compliant cipher suites are enforced by default when the `tls_version` is set to `TLS 1.2` or `TLS 1.3`.

Review [connect using SSL/TLS](security-tls-how-to-connect.md#verify-the-tls-connection) to learn how to identify the TLS version.

## Trusted root certs and cert rotations

[!INCLUDE [certificate-rotation](includes/certificate-rotation.md)]

### Root CAs used by Azure Database for MySQL

Root CAs are the top-level authorities in the certificate chain. Azure Database for MySQL currently uses dual-signed certificates issued by an ICA anchored by the following root CAs:

- [DigiCert Global Root G2](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt)
- [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt)

China regions currently use the following CAs:

- [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt)
- [DigiCert Global Root CA](https://cacerts.digicert.com/DigiCertGlobalRootCA.crt)
- After Spring Festival (Chinese New Year) 2026: [Digicert Global Root G2](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt). We recommend that you prepare for this change in advance by adding the new root CA to your trusted root store.

### About Intermediate CAs

Azure Database for MySQL uses intermediate CAs (ICAs) to issue server certificates. Microsoft periodically rotates these ICAs and the server certificates they issue to maintain security. These rotations are routine and not announced in advance.

The current rotation of intermediate certificate authorities for `DigiCert Global Root G2` (see [Certificate rotation](#trusted-root-certs-and-cert-rotations)) started in November 2025 and scheduled to be completed in Q1 of 2026 replaces intermediate CAs as follows. If you followed the [recommended practices](#recommended-configurations-for-tls), then this change requires no changes in your environment.

#### Old CA chain

This information is provided for reference only. Don't use intermediate CAs or server certificates in your trusted root store.

- `DigiCert Global Root G2`
  - `Microsoft Azure RSA TLS Issuing CA 03 / 04 / 07 / 08`
    - Server certificate

#### New CA chain

This information is provided for reference only. Don't use intermediate CAs or server certificates in your trusted root store.

- `DigiCert Global Root G2`
  - `Microsoft TLS RSA Root G2`
    - `Microsoft TLS G2 RSA CA OCSP 02 / 04 / 06 / 08 / 10 / 12 / 14 / 16`
      - Server certificate

### Certificate chains

A certificate chain is a hierarchical sequence of certificates issued by trusted Certificate Authorities (CAs), starting at the root CA, which issues intermediate CA (ICA) certificates. ICAs might issue certificates for lower ICAs. The lowest ICA in the chain issues individual server certificates. The chain of trust is established by verifying each certificate in the chain up to the root CA certificate.

### Reducing connection failures

Utilizing recommended TLS configurations helps reduce the risk of connection failures due to certificate rotations or changes in intermediate CAs. Specifically, avoid trusting intermediate CAs or individual server certificates, as these practices can lead to unexpected connection issues when Microsoft updates the certificate chain.

> [!IMPORTANT]  
> Changes in root CAs are announced ahead of time to help you prepare your client applications; however, server certificate rotations and changes to intermediate CAs are routine and therefore not announced.

> [!CAUTION]  
> Using *[unsupported (client) configurations](#trusted-root-certs-and-cert-rotations)* can cause unexpected connection failures.

## Recommended configurations for TLS

### Best configuration

- Enforce the latest, most secure TLS version by setting the `require_secure_transport = ON` and `tls_version = TLS 1.3`.
- Use full verification from client applications (settings vary by client).
- Always maintain the [complete set of Azure root certificates in your trusted root store](/azure/security/fundamentals/azure-ca-details?tabs=root-and-subordinate-cas-list#certificate-authority-details).

### Good configuration

- Set the `require_secure_transport = ON` and `tls_version = TLS 1.3`. If you must support TLS 1.2, don't set the `tls_version`.
- Use full verification from client applications (This varies by client).
- Ensure that the trusted root store contains the root CA certificate currently used by Azure Database for MySQL:
  - [DigiCert Global Root G2](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt)
  - [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt)

### Supported, not recommended

We strongly advise against disable TLS completely by setting `require_secure_transport` to `OFF`

### Unsupported configurations; do not use

Azure MySQL doesn't announce changes about intermediate CA changes or individual server certificate rotations; therefore, the following configurations are unsupported:

- You use intermediate CA certificates in your trusted store.
- You use certificate pinning, such as, using individual server certificates in your trusted store.

> [!CAUTION]  
> Your applications fail to connect to the database servers without warning whenever Microsoft changes the certificate chain's intermediate CAs or rotates the server certificate.

## Other considerations for TLS

### Insecure and secure TLS versions

Several government entities worldwide maintain guidelines for TLS regarding network security. In the United States, these organizations include the Department of Health and Human Services and the National Institute of Standards and Technology. The level of security that TLS provides is most affected by the TLS protocol version and the supported cipher suites.

Azure Database for MySQL supports TLS version 1.2 and 1.3. In RFC 8996, the Internet Engineering Task Force (IETF) explicitly states that TLS 1.0 and TLS 1.1 must not be used. Both protocols were deprecated by the end of 2019.
All incoming connections that use earlier insecure versions of the TLS protocol, such as TLS 1.0 and TLS 1.1, are denied by default.

The IETF released the TLS 1.3 specification in RFC 8446 in August 2018, and TLS 1.3 is the recommended version since it's faster and more secure than TLS 1.2.

Although we don't recommend it, if needed, you can disable TLS for connections to your Azure Database for MySQL. You can update the `require_secure_transport` server parameter to `OFF`.

### Cipher suites

A [cipher suite](https://en.wikipedia.org/wiki/Cipher_suite) is a set of algorithms that include a cipher, a key-exchange algorithm, and a hashing algorithm. They're used together with the TLS certificate and the TLS version to establish a secure TLS connection. Most TLS clients and servers support multiple cipher suites and sometimes multiple TLS versions.
During the establishment of the connection, the client and server [negotiate the TLS version and cipher suite to use through a handshake](https://en.wikipedia.org/wiki/Cipher_suite#Full_handshake:_coordinating_cipher_suites). During this handshake, the following occurs:

- Client sends a list of acceptable cipher suites.
- Server selects the best (by its own definition) cipher suite from the list and informs the client of the choice.

### TLS features not available in Azure Database for MySQL

At this time, Azure Database for MySQL doesn't implement the following TLS features:

- TLS certificate-based client authentication through TLS with mutual authentication (mTLS).
- Custom server certificates (bring your own TLS certificates).

## Related content

- [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](security-tls-how-to-connect.md)
- [Root certificate rotation for Azure Database for MySQL](security-tls-root-certificate-rotation.md)
- [Frequently asked questions for certificate rotation for Azure Database for MySQL](security-tls-root-certificate-rotation-faq.md)
