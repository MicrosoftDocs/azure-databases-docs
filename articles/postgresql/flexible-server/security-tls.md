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
---

# Transport Layer Security (TLS) in Azure Database for PostgreSQL

Azure Database for PostgreSQL requires all client connections to use Transport Layer Security (TLS), an industry-standard protocol that encrypts communications between your database server and client applications. TLS supersedes the older SSL protocol, with only TLS versions 1.2 and 1.3 recognized as secure. The integrity of TLS security relies on three pillars:

- Using only TLS versions 1.2 or 1.3.
- Client validates the server's TLS certificate issued by a Certificate Authority (CA) in a chain of CAs started by a trusted root CA.
- Negotiating a secure cipher suite between server and client.

## Trusted root certs and cert rotations

[!INCLUDE [certificate-rotation](includes/certificate-rotation.md)]

### Root CAs used by Azure Database for PostgreSQL

Root CAs are the top-level authorities in the certificate chain. Azure Database for PostgreSQL currently uses dual-signed certificates issued by an intermediate CA (ICA) anchored by the following root CAs:

- [DigiCert Global Root G2](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt)
- [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt)

China regions currently use the following CAs:

- [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt)
- [DigiCert Global Root CA](https://cacerts.digicert.com/DigiCertGlobalRootCA.crt)
- After Spring Festival (Chinese New Year) 2026: [Digicert Global Root G2](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt). Prepare for this change in advance by adding the new root CA to your trusted root store.

### About intermediate CAs

Azure Database for PostgreSQL uses intermediate CAs (ICAs) to issue server certificates. To maintain security, Microsoft periodically rotates these ICAs and the server certificates they issue. These rotations are routine and aren't announced in advance.

The current rotation of intermediate CAs for `DigiCert Global Root CA` (see [Certificate rotation](#trusted-root-certs-and-cert-rotations)) started in November 2023 and is scheduled to be completed in the first quarter of 2024. If you followed the [recommended practices](#recommended-configurations-for-tls), then this change requires no changes in your environment.

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

### Read replicas

Root CA migration from [DigiCert Global Root CA](https://cacerts.digicert.com/DigiCertGlobalRootCA.crt) to [DigiCert Global Root G2](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt) isn't completed in all regions. Therefore, it's possible for newly created read replicas to use a newer root CA certificate than the primary server. Add [DigiCert Global Root CA](https://cacerts.digicert.com/DigiCertGlobalRootCA.crt) to the read replicas trusted store.

### Certificate chains

A certificate chain is a hierarchical sequence of certificates issued by trusted Certificate Authorities (CAs). The chain starts at the root CA, which issues intermediate CA (ICA) certificates. ICAs can issue certificates for lower ICAs. The lowest ICA in the chain issues individual server certificates. You establish the chain of trust by verifying each certificate in the chain up to the root CA certificate.

### Reducing connection failures

Using the recommended TLS configurations helps reduce the risk of connection failures due to certificate rotations or changes in intermediate CAs. Specifically, don't trust intermediate CAs or individual server certificates. These practices can lead to unexpected connection issues when Microsoft updates the certificate chain.

> [!IMPORTANT]
> Microsoft announces changes in root CAs ahead of time to help you prepare your client applications. However, server certificate rotations and changes to intermediate CAs are routine and aren't announced.

> [!CAUTION]
> Using ***[unsupported (client) configurations](#trusted-root-certs-and-cert-rotations)*** causes unexpected connection failures.

## Recommended configurations for TLS

### Best configuration

- Enforce the latest, most secure TLS version by setting the `ssl_min_protocol_version` server parameter to `TLSv1.3`.
- Use `sslmode=verify-all` for PostgreSQL connections to ensure full certificate and hostname verification. Depending on your DNS configuration with Private Endpoints or VNET integration, `verify-all` might not be possible. Therefore, you can use `verify-ca` instead.
- Always maintain the [complete set of Azure root certificates in your trusted root store](/azure/security/fundamentals/azure-ca-details?tabs=root-and-subordinate-cas-list#certificate-authority-details).

### Good configuration

- Set the `ssl_min_protocol_version` server parameter to `TLSv1.3`. If you must support TLS 1.2, don't set the minimal version.
- Use `sslmode=verify-all` or `sslmode=verify-ca` for PostgreSQL connections to ensure full or partial certificate verification.
- Ensure that the trusted root store contains the root CA certificate currently used by Azure Database for PostgreSQL:
  - [DigiCert Global Root G2](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt)
  - [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt)

### Supported, not recommended

Avoid the following configurations:

- Disable TLS by setting `require_secure_transport` to `OFF` and setting the client-side to `sslmode=disable`.
- Use client-side `sslmode` settings `disable`, `allow`, `prefer`, or `require` that make your app vulnerable to man-in-the-middle attacks.

### Unsupported configurations; don't use

Azure PostgreSQL doesn't announce changes about intermediate CA changes or individual server certificate rotations. Therefore, the following configurations are unsupported when using `sslmode` settings `verify-ca` or `verify-all`:

- Using intermediate CA certificates in your trusted store.
- Using certificate pinning, such as, using individual server certificates in your trusted store.

> [!CAUTION]
> Your applications fail to connect to the database servers without warning whenever Microsoft changes the certificate chain’s intermediate CAs or rotates the server certificate.

### Certificate pinning problems

> [!NOTE]
> Certificate rotations don't affect your application if you don't use the `sslmode=verify-full` or `sslmode=verify-ca` settings in your client application connection string. Therefore, you don't need to follow the steps in this section.

Never use certificate pinning in your applications. Certificate pinning breaks certificate rotation, such as the current certificate change of intermediate CAs. If you don't know what certificate pinning is, it's unlikely that you're using it. To check for [certificate pinning](/azure/security/fundamentals/certificate-pinning):

- Produce your list of certificates that are in your trusted root store.
    - [Combine and update root CA certificates for Java applications](security-tls-how-to-connect.md#combine-and-update-root-ca-certificates-for-java-applications).
    - Open the trusted root store on your client machine and export the list of certificates.
- You're using certificate pinning if you have intermediate CA certificates or individual PostgreSQL server certificates in your trusted root store.
- To remove certificate pinning, remove all the certificates from your trusted root store and add the [recommended root CA certificates](#recommended-configurations-for-tls).

If you experience problems due to the intermediate certificate even after following these steps, contact [Microsoft support](/azure/azure-portal/supportability/how-to-create-azure-support-request). Include **ICA Rotation 2026** in the title.

## Other considerations for TLS

### Insecure and secure TLS versions

Several government entities worldwide maintain guidelines for TLS regarding network security. In the United States, these organizations include the Department of Health and Human Services and the National Institute of Standards and Technology. The level of security that TLS provides is most affected by the TLS protocol version and the supported cipher suites.

Azure Database for PostgreSQL supports TLS versions 1.2 and 1.3. In RFC 8996, the Internet Engineering Task Force (IETF) explicitly states that TLS 1.0 and TLS 1.1 must not be used. Both protocols were deprecated by the end of 2019.
By default, the service denies all incoming connections that use earlier insecure versions of the TLS protocol, such as TLS 1.0 and TLS 1.1.

The IETF released the TLS 1.3 specification in RFC 8446 in August 2018, and TLS 1.3 is the recommended version since it's faster and more secure than TLS 1.2.

Although we don't recommend it, if needed, you can disable TLS for connections to your Azure Database for PostgreSQL. You can update the `require_secure_transport` server parameter to `OFF`.

> [!IMPORTANT]
> Use the latest version of TLS 1.3 to encrypt your database connections. Specify the minimal TLS version by setting the `ssl_min_protocol_version` server parameter to `TLSv1.3`. Don't set the `ssl_max_protocol_version` server parameter.

### Cipher suites

A [cipher suite](https://en.wikipedia.org/wiki/Cipher_suite) is a set of algorithms that include a cipher, a key-exchange algorithm, and a hashing algorithm. Use them together with the TLS certificate and the TLS version to establish a secure TLS connection. Most TLS clients and servers support multiple cipher suites and sometimes multiple TLS versions.
During the establishment of the connection, the client and server [negotiate the TLS version and cipher suite to use through a handshake](https://en.wikipedia.org/wiki/Cipher_suite#Full_handshake:_coordinating_cipher_suites). During this handshake, the following occurs:

- Client sends a list of acceptable cipher suites.
- Server selects the best cipher suite from the list and informs the client of the choice.

### TLS features not available in Azure Database for PostgreSQL

At this time, Azure Database for PostgreSQL doesn't implement the following TLS features:

- TLS certificate-based client authentication through TLS with mutual authentication (mTLS).
- Custom server certificates (bring your own TLS certificates).

## Related content

- [Configure TLS client settings to connect to Azure Database for PostgreSQL](security-tls-how-to-connect.md)
- [Validating client configuration and troubleshooting connection failures](security-tls-troubleshoot.md)
