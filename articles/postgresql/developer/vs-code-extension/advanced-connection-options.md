---
title: "Advanced connection options"
description: "Use advanced PostgreSQL connection features such as connection strings, certificate files, and SSH tunnels in Visual Studio Code."
author: mmcfarland
ms.author: mattmcfarland
ms.date: 05/11/2026
ms.service: postgresql
ms.subservice: vs-code-pgsql-extensions
ms.topic: how-to
---


# Advanced connection options

This article covers the advanced connection features in the PostgreSQL extension for Visual Studio Code. Use these options when you need to reuse an existing connection string, supply certificate files for stricter TLS validation, or connect through a bastion host with an SSH tunnel.

> [!TIP]
> For standard authentication, SSL mode selection, server groups, and saved connections, see [Connections and identity](connections.md).

## Use connection string input mode

Select the **Connection String** tab (under **Connect via:**) in the connection dialog to paste an existing connection definition. The extension parses the string automatically and populates the connection fields.

# [Visual Studio Code](#tab/vscode)

:::image type="content" source="./media/screenshots/vscode/connection-dialog/connection-string-tab.png" alt-text="Connection String tab with textarea and parsed Connection Details panel" lightbox="./media/screenshots/vscode/connection-dialog/connection-string-tab.png":::

# [Cursor](#tab/cursor)

:::image type="content" source="./media/screenshots/cursor/connection-dialog/connection-string-tab.png" alt-text="Connection String tab with textarea and parsed Connection Details panel" lightbox="./media/screenshots/cursor/connection-dialog/connection-string-tab.png":::

---

The page uses a two-column layout:

- **Left column** — a text area labeled **Connection String** where you paste the string. A hint below the text area reads **Please omit password from the connection string**.
- **Right column** — a read-only **Connection Details** panel that shows the parsed **Server name**, **User name**, and **Database name** values as they are extracted.

Parsing happens live as you type or paste. If the parser detects a missing server or user value, a validation error appears above the text area.

### Supported formats

The extension recognizes nine connection string formats:

| Format | Prefix or trigger | Example |
|---|---|---|
| PostgreSQL URI | `postgres://` or `postgresql://` | `postgresql://user:password@host:5432/dbname?sslmode=require` |
| JDBC | `jdbc:postgresql://` | `jdbc:postgresql://host:5432/dbname` |
| Semicolon-separated (key=value) | Contains `;` | `host=localhost;port=5432;dbname=mydb;user=postgres;password=secret` |
| `psql` command line | `psql` | `psql -h host -p 5432 -U user -d dbname` |
| Environment variable exports | `export` | `export PGHOST=localhost` followed by `PGPORT`, `PGUSER`, `PGDATABASE`, `PGPASSWORD` |
| Node.js | `new Client` | `new Client({ host: "localhost", port: 5432, user: "postgres", database: "mydb" })` |
| Python (psycopg2) | `psycopg2.connect` | `psycopg2.connect(user="postgres", password="secret", host="localhost", port=5432, database="mydb")` |
| PHP | `pg_connect` | `pg_connect("host=localhost port=5432 dbname=mydb user=postgres")` |
| Ruby | `PG::Connection.new` | `PG::Connection.new(host: "localhost", port: "5432", user: "postgres", database: "mydb")` |

The parser extracts **host**, **user**, **port**, **database**, and **password** from all formats. If a password field is already filled in the dialog, the parser preserves the existing value.

> [!NOTE]
> After parsing, you can still open the **Advanced** drawer to configure settings that connection strings don't carry, such as SSH tunnels or the per-connection AI access mode (**Copilot access mode** in Visual Studio Code, **AI access mode** in Cursor).

## Configure certificate files

Use the certificate file settings in the **SSL** accordion section of the **Advanced Connection Settings** drawer when your environment requires mutual TLS or explicit certificate authority validation.

# [Visual Studio Code](#tab/vscode)

:::image type="content" source="./media/screenshots/vscode/connection-dialog/ssl-certificate-fields.png" alt-text="SSL section showing root certificate mode dropdown and certificate fields" lightbox="./media/screenshots/vscode/connection-dialog/ssl-certificate-fields.png":::

# [Cursor](#tab/cursor)

:::image type="content" source="./media/screenshots/cursor/connection-dialog/ssl-certificate-fields.png" alt-text="SSL section showing root certificate mode dropdown and certificate fields" lightbox="./media/screenshots/cursor/connection-dialog/ssl-certificate-fields.png":::

---

### SSL root certificate mode

The **SSL root certificate mode** dropdown controls how the extension supplies the root CA certificate. Choose one of the following values:

| Mode | Behavior |
|---|---|
| **None** | No root certificate is used. The extension does not verify the server certificate chain. |
| **System** | The extension uses your operating system's trusted certificate store. This mode requires **Verify-Full** SSL mode; the extension enforces this automatically. |
| **Custom file** | A text field labeled **SSL root certificate filename** appears. Enter the path to a PEM-encoded root CA certificate file. |

> [!IMPORTANT]
> When you select **System**, the SSL mode is set to **Verify-Full** automatically. If you change the SSL mode to another value while **System** is active, a validation error appears: "Verify-Full SSL mode is required when using the system certificate store."

### Client certificate fields

Configure mutual TLS by providing paths in these fields within the **SSL** section:

| Field label | Property | Description |
|---|---|---|
| **SSL certificate filename** | `sslcert` | Path to the client certificate file. |
| **SSL key filename** | `sslkey` | Path to the client's private key file. |
| **SSL root certificate filename** | `sslrootcert` | Path to the root CA certificate (visible only when **SSL root certificate mode** is **Custom file**). |
| **SSL CRL filename** | `sslcrl` | Path to a certificate revocation list file. |
| **Use SSL compression** | `sslcompression` | Enables compression on the SSL connection. |

> [!TIP]
> For **Verify-CA** and **Verify-Full** modes, always configure the root certificate so the extension can validate the server certificate. Use **System** mode to rely on your operating system's trusted CA store without specifying a file path.

## Connect through an SSH tunnel

SSH tunneling routes the PostgreSQL connection through an encrypted SSH channel. Use this approach when the database is not directly reachable from your workstation—for example, when the server resides in a private network behind a bastion host.

# [Visual Studio Code](#tab/vscode)

:::image type="content" source="./media/screenshots/vscode/connection-dialog/ssh-tunnel-fields.png" alt-text="SSH Tunnel section with Enable SSH Tunneling toggled on" lightbox="./media/screenshots/vscode/connection-dialog/ssh-tunnel-fields.png":::

# [Cursor](#tab/cursor)

:::image type="content" source="./media/screenshots/cursor/connection-dialog/ssh-tunnel-fields.png" alt-text="SSH Tunnel section with Enable SSH Tunneling toggled on" lightbox="./media/screenshots/cursor/connection-dialog/ssh-tunnel-fields.png":::

---

### Enable the tunnel

1. Open the connection dialog and select **Advanced** to open the **Advanced Connection Settings** drawer.
1. Expand the **SSH Tunnel** accordion section.
1. Check the **Enable SSH Tunneling** toggle. The SSH connection fields appear.

### SSH tunnel fields

| Field label | Description |
|---|---|
| **host** | Hostname or IP address of the SSH server (bastion host). |
| **port** | SSH server port number (default: `22`). |
| **username** | Username to authenticate with the SSH server. |
| **Authentication** | SSH authentication method. Choose **Password**, **Identity File**, or **SSH Agent**. |

The remaining fields change depending on the selected authentication method:

| Authentication method | Additional fields shown |
|---|---|
| **Password** | **password/passphrase** — enter the SSH password. **Save Password/Passphrase** checkbox to persist the credential. |
| **Identity File** | **Identity file** — enter the full path to your SSH private key (for example, `~/.ssh/id_ed25519`). **password/passphrase** — enter the key passphrase if the private key is encrypted. **Save Password/Passphrase** checkbox. |
| **SSH Agent** | No additional fields. The extension delegates authentication to your system's SSH agent (`ssh-agent` on macOS and Linux, OpenSSH Authentication Agent service on Windows). |

### How the tunnel works

When the SSH tunnel is enabled, the extension establishes the SSH connection first, creates a local port forward, and then connects to PostgreSQL through that forward. Because of this:

- The **Server name** in the main connection fields should be the database address **as seen from the SSH host**, which is often `localhost` or a private IP.
- The **Port** should be the PostgreSQL port on the target host (typically `5432`).
- SSH tunnel establishment adds connection latency. Consider increasing the **Connect timeout** value in the advanced options if timeouts occur.

## Choose the right advanced option

| Scenario | Recommended feature |
|---|---|
| You have an existing PostgreSQL URI, app snippet, or `psql` command | Select the **Connection String** tab to populate the fields automatically. |
| Your organization requires custom CA files or mutual TLS | Configure the SSL certificate fields in the **SSL** section of the advanced drawer. |
| You need to use your OS certificate store for server verification | Set **SSL root certificate mode** to **System** and **SSL mode** to **Verify-Full**. |
| The database is reachable only through a jump box or bastion host | Enable the SSH tunnel in the **SSH Tunnel** section of the advanced drawer. |

## Related content

- [Connections and identity](connections.md)
- [Quickstart: Connect and query](quickstart-connect-query.md)
- [Create a PostgreSQL server](create-server.md)
- [Query editor and IntelliSense](query-editor-intellisense.md)
- [Settings reference](reference/settings.md)
