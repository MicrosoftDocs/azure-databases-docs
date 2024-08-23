---
ms.service: azure-cosmos-db
ms.subservice: postgresql
ms.topic: include
ms.date: 08/23/2024
---

It's sometimes possible that database requests from your application fail.
Such issues can happen under different scenarios, such as network failure
between app and database, incorrect password, etc. Some issues may be
transient, and resolve themselves in a few seconds to minutes. You can
configure retry logic in your app to overcome the transient errors.

Configuring retry logic in your app helps improve the end user experience.
Under failure scenarios, users will merely wait a bit longer for the
application to serve requests, rather than experience errors.

The example below shows how to implement retry logic in your app. The sample
code snippet tries a database request every 60 seconds (up to five times) until
it succeeds. The number and frequency of retries can be configured based on
your application's needs.
