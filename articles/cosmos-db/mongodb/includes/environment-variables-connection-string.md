---
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.topic: include
ms.date: 08/23/2024
ms.custom: sfi-ropc-blocked
---
To use the **CONNECTION STRING** values within your code, set this value in the local environment running the application. To set the environment variable, use your preferred terminal to run the following commands:

#### [Windows](#tab/windows)

```powershell
$env:COSMOS_CONNECTION_STRING = "<cosmos-connection-string>"
```

#### [Linux / macOS](#tab/linux+macos)

```bash
export COSMOS_CONNECTION_STRING="<cosmos-connection-string>"
```

#### [.env](#tab/dotenv)

A `.env` file is a standard way to store environment variables in a project. Create a `.env` file in the root of your project. Add the following lines to the `.env` file:

```dotenv
COSMOS_CONNECTION_STRING="<cosmos-connection-string>"
```

---
