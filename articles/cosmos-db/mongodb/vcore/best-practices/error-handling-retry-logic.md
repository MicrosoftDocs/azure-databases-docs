---
title: |
  Tutorial: Error Handling and Retry Logic in Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: This tutorial provides a comprehensive guide to error handling and retry logic in Azure Cosmos DB for MongoDB vCore. It explains how to classify and manage transient and permanent errors, implement exponential backoff and circuit breaker patterns, and configure retry settings in MongoDB drivers. With practical examples and best practices, this documentation ensures developers can build robust, resilient, and high-performing applications that handle failures gracefully.
author: v-smedapati
ms.author: v-smedapati
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: tutorial
ms.date: 11/29/2024
# CustomerIntent: As a developer or IT professional, I need to understand error handling and retry logic in Azure Cosmos DB for MongoDB vCore, focusing on managing transient errors, implementing retry mechanisms, and ensuring application reliability with minimal downtime.
---

# Error Handling and Retry Logic in Azure Cosmos DB for MongoDB vCore

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

When interacting with Azure Cosmos DB for MongoDB vCore, applications must handle transient and permanent errors gracefully to ensure reliability and a seamless user experience. This guide provides a comprehensive overview of error handling strategies, retry mechanisms, and best practices for building resilient applications using MongoDB drivers or other integrations.


## Types of Errors
Errors in Cosmos DB for MongoDB vCore can be broadly categorized into:

1. **Transient Errors**
    - **Description:** Temporary issues such as network failures, throttling due to exceeding Request Units (RUs), or service unavailability.
    - **Examples:**
        - HTTP status code 429 (Too Many Requests)
        - Timeout errors
    - **Handling:** Implement retry logic with exponential backoff.

1. **Permanent Errors**
    - **Description**: Errors caused by invalid requests, improper configurations, or exceeding resource limits.
    - **Examples:**
        - HTTP status code 400 (Bad Request)
        - Invalid query syntax or unsupported operations.
    - **Handling:** Log the error, provide meaningful feedback, and take corrective actions.


## Best Practices for Error Handling

1. **Classify Errors**

    - Use MongoDB driver-specific error classes to differentiate between transient and permanent errors.
    - For example, in Node.js:
        ```javascript
        try {
        // Your database operation
        } catch (error) {
            if (error.name === 'MongoNetworkError') {
                // Handle network issues
            } else if (error.code === 121) {
                // Handle schema validation errors
            } else {
                // General error handling
            }
        }
        ```

1. **Log Errors**

    - Ensure all errors are logged with sufficient context for troubleshooting. Use structured logging tools like Logstash or Azure Monitor.

1. **Graceful Fallback**

    - Provide fallback mechanisms for critical operations, such as caching or queuing failed requests for later processing.

1. **Client-Side Validation**

    - Validate data and queries on the client side to minimize avoidable server-side errors.


## Retry Logic
Retrying operations after transient errors is a key aspect of building resilient applications. Follow these guidelines:

1. **Exponential Backoff**
    - Implement retries with incremental delays between attempts to reduce the load on the database.
    - Example in Node.js:
        ```javascript
        const retryOperation = async (operation, retries, delay) => {
        for (let i = 0; i < retries; i++) {
            try {
            return await operation();
            } catch (error) {
            if (i === retries - 1 || !isTransientError(error)) {
                throw error;
            }
            await new Promise(res => setTimeout(res, delay * Math.pow(2, i))); // Exponential backoff
            }
        }
        };
        ```
1. **Circuit Breaker Pattern**
    - Prevent repeated retries during prolonged failures by temporarily halting operations and monitoring the system state.
    - Libraries like [Opossum](https://github.com/nodeshift/opossum). can help implement this.
1. **Retry Settings in Drivers**
    - Configure retries using MongoDB drivers’ built-in settings:
        - **Node.js**: `retryWrites=true` in the connection string.
        - **Java**: Use `MongoClientOptions.builder().retryWrites(true)`.
1. **Throttling Considerations**
     -Monitor HTTP 429 errors (Too Many Requests) and adjust the retry interval dynamically based on the `Retry-After` header.    

## Handling Common Errors
1. **HTTP 429: Too Many Requests**
    - **Cause:** Exceeding provisioned RUs.
    - **Solution:** Implement exponential backoff and monitor RU consumption.
        ```javascript
        if (error.code === 429) {
        const retryAfter = error.response.headers['retry-after-ms'];
        await new Promise(res => setTimeout(res, retryAfter));
        }
        ```

1. **Network Errors**
    - **Cause:** Connectivity issues or DNS resolution failures.
    - **Solution:** Retry with exponential backoff and verify network configurations.
1. **Query Errors**
    - **Cause:** Invalid syntax, unsupported operations, or mismatched schema.
    - **Solution:** Validate queries before execution and use schema validation for structured data.


## Monitoring and Alerts

1. **Azure Monitor Integration**

    - Enable monitoring for your Cosmos DB instance to track errors and performance metrics.
1. **Custom Alerts**

    - Configure alerts for specific error types, such as high 429 rates or network errors.

1. **Application Insights**

    - Use Azure Application Insights to capture detailed telemetry on database interactions and error occurrences.

## Examples

### Example 1: Handling Transient Errors

```javascript
const mongoose = require('mongoose');

const connectWithRetry = () => {
  mongoose.connect('mongodb://your-cosmosdb-url', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    retryWrites: true
  })
  .then(() => console.log('Connected to Cosmos DB'))
  .catch((error) => {
    console.error('Connection failed, retrying...', error);
    setTimeout(connectWithRetry, 5000); // Retry after 5 seconds
  });
};

connectWithRetry();
```

### Example 2: Handling Query Errors

```javascript
try {
  const result = await db.collection('users').find({ age: { $gte: '30' } }).toArray();
} catch (error) {
  if (error.code === 2) {
    console.error('Invalid query syntax:', error.message);
  } else {
    console.error('Unexpected error:', error);
  }
}
```

Effective error handling and retry logic are essential for building resilient applications on Azure Cosmos DB for MongoDB vCore. By classifying errors, implementing exponential backoff, and using built-in retry mechanisms, you can ensure your application is robust, scalable, and user-friendly.

