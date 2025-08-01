---
title: Model and Partition Data using a Real-World Example
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to model and partition data using a real-world example scenario and Azure Cosmos DB for NoSQL.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 07/11/2025
ms.devlang: javascript
ms.custom: sfi-image-nochange
---

# How to model and partition data using a real-world example

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

This article builds on several Azure Cosmos DB concepts like [data modeling](../modeling-data.md), [partitioning](../partitioning-overview.md), and [provisioned throughput](../request-units.md) to demonstrate how to tackle a real-world data design exercise.

If you usually work with relational databases, you've probably developed habits for designing data models. Because of the specific constraints, but also the unique strengths of Azure Cosmos DB, most of these best practices don't translate well and might drag you into suboptimal solutions. The goal of this article is to guide you through the complete process of modeling a real-world use case on Azure Cosmos DB, from item modeling to entity colocation and container partitioning.

For an example that illustrates the concepts in this article, download or view this [community-generated source code](https://github.com/jwidmer/AzureCosmosDbBlogExample).

> [!IMPORTANT]
> A community contributor contributed this code example. The Azure Cosmos DB team doesn't support its maintenance.

## The scenario

For this exercise, we're going to consider the domain of a blogging platform where *users* can create *posts*. Users can also *like* and add *comments* to those posts.

> [!TIP]
> Some words are highlighted in *italic* to identify the kind of "things" that our model manipulates.

Adding more requirements to our specification:

- A front page displays a feed of recently created posts.
- We can fetch all posts for a user, all comments for a post and all likes for a post.
- Posts are returned with the username of their authors and a count of how many comments and likes they have.
- Comments and likes are also returned with the username of the users who created them.
- When displayed as lists, posts only have to present a truncated summary of their content.

## Identify the main access patterns

To start, we give some structure to our initial specification by identifying our solution's access patterns. When designing a data model for Azure Cosmos DB, it's important to understand which requests our model has to serve to make sure that the model serves those requests efficiently.

To make the overall process easier to follow, we categorize those different requests as either commands or queries, borrowing some vocabulary from [command query responsibility segregation (CQRS)](https://en.wikipedia.org/wiki/Command_Query_Responsibility_Segregation). In CQRS, commands are write requests (that is, intents to update the system) and queries are read-only requests.

Here's the list of requests that our platform exposes:

- **[C1]** Create or edit a user
- **[Q1]** Retrieve a user
- **[C2]** Create or edit a post
- **[Q2]** Retrieve a post
- **[Q3]** List a user's posts in short form
- **[C3]** Create a comment
- **[Q4]** List a post's comments
- **[C4]** Like a post
- **[Q5]** List a post's likes
- **[Q6]** List the *x* most recent posts created in short form (feed)

At this stage, we haven't thought about the details of what each entity (user, post, etc.) contains. This step is usually among the first ones to be tackled when designing against a relational store. We start with this step first because we have to figure out how those entities translate in terms of tables, columns, foreign keys, and so on. It's much less of a concern with a document database that doesn't enforce any schema at write.

It's important to identify our access patterns from the beginning because this list of requests is going to be our test suite. Every time we iterate over our data model, we go through each of the requests and check its performance and scalability. We calculate the request units (RU) consumed in each model and optimize them. All these models use the default indexing policy and you can override it by indexing specific properties, which can further improve the RU consumption and latency.

## V1: A first version

We start with two containers: `users` and `posts`.

### Users container

This container only stores user items:

```json
{
    "id": "<user-id>",
    "username": "<username>"
}
```

We partition this container by `id`, which means that each logical partition within that container only contains one item.

### Posts container

This container hosts entities such as posts, comments, and likes:

```json
{
    "id": "<post-id>",
    "type": "post",
    "postId": "<post-id>",
    "userId": "<post-author-id>",
    "title": "<post-title>",
    "content": "<post-content>",
    "creationDate": "<post-creation-date>"
}

{
    "id": "<comment-id>",
    "type": "comment",
    "postId": "<post-id>",
    "userId": "<comment-author-id>",
    "content": "<comment-content>",
    "creationDate": "<comment-creation-date>"
}

{
    "id": "<like-id>",
    "type": "like",
    "postId": "<post-id>",
    "userId": "<liker-id>",
    "creationDate": "<like-creation-date>"
}
```

We partition this container by `postId`, which means that each logical partition within that container contains one post, all the comments for that post and all the likes for that post.

We've introduced a `type` property in the items stored in this container to distinguish between the three types of entities that this container hosts.

Also, we chose to reference related data instead of embedding it because:

- There's no upper limit to how many posts a user can create.
- Posts can be arbitrarily long.
- There's no upper limit to how many comments and likes a post can have.
- We want to be able to add a comment or a like to a post without having to update the post itself.

To learn more about these concepts, see [Data modeling in Azure Cosmos DB](modeling-data.md).

## How well does our model perform?

It's now time to assess the performance and scalability of our first version. For each of the requests previously identified, we measure its latency and how many request units it consumes. This measurement is done against a dummy data set containing 100,000 users with 5 to 50 posts per user, and up to 25 comments and 100 likes per post.

### [C1] Create or edit a user

This request is straightforward to implement as we just create or update an item in the `users` container. The requests nicely spread across all partitions thanks to the `id` partition key.

:::image type="content" source="./media/model-partition-example/V1-C1.png" alt-text="Diagram of writing a single item to the users container.":::

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `7` ms | `5.71` RU | ✅ |

### [Q1] Retrieve a user

Retrieving a user is done by reading the corresponding item from the `users` container.

:::image type="content" source="./media/model-partition-example/V1-Q1.png" alt-text="Diagram of retrieving a single item from the users container.":::

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `2` ms | `1` RU | ✅ |

### [C2] Create or edit a post

Similarly to **[C1]**, we just have to write to the `posts` container.

:::image type="content" source="./media/model-partition-example/V1-C2.png" alt-text="Diagram of writing a single post item to the posts container.":::

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `9` ms | `8.76` RU | ✅ |

### [Q2] Retrieve a post

We start by retrieving the corresponding document from the `posts` container. But that's not enough, as per our specification, we also have to aggregate the username of the post's author, counts of comments, and counts of likes for the post. The aggregations listed require three more SQL queries to be issued.

:::image type="content" source="./media/model-partition-example/V1-Q2.png" alt-text="Diagram of retrieving a post and aggregating additional data.":::

Each of the queries filters on the partition key of its respective container, which is exactly what we want to maximize performance and scalability. But we eventually have to perform four operations to return a single post, so we'll improve that in a next iteration.

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `9` ms | `19.54` RU | ⚠ |

### [Q3] List a user's posts in short form

First, we have to retrieve the desired posts with a SQL query that fetches the posts corresponding to that particular user. But we also have to issue more queries to aggregate the author's username and the counts of comments and likes.

:::image type="content" source="./media/model-partition-example/V1-Q3.png" alt-text="Diagram of retrieving all posts for a user and aggregating their additional data.":::

This implementation presents many drawbacks:

- The queries that aggregate the counts of comments and likes must be issued for each post returned by the first query.
- The main query doesn't filter on the partition key of the `posts` container, leading to a fan-out and a partition scan across the container.

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `130` ms | `619.41` RU | ⚠ |

### [C3] Create a comment

A comment is created by writing the corresponding item in the `posts` container.

:::image type="content" source="./media/model-partition-example/V1-C2.png" alt-text="Diagram of writing a single comment item to the posts container.":::

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `7` ms | `8.57` RU | ✅ |

### [Q4] List a post's comments

We start with a query that fetches all the comments for that post and once again, we also need to aggregate usernames separately for each comment.

:::image type="content" source="./media/model-partition-example/V1-Q4.png" alt-text="Diagram of retrieving all comments for a post and aggregating their additional data.":::

Although the main query does filter on the container's partition key, aggregating the usernames separately penalizes the overall performance. We improve that later on.

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `23` ms | `27.72` RU | ⚠ |

### [C4] Like a post

Just like **[C3]**, we create the corresponding item in the `posts` container.

:::image type="content" source="./media/model-partition-example/V1-C2.png" alt-text="Diagram of writing a single (like) item to the posts container.":::

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `6` ms | `7.05` RU | ✅ |

### [Q5] List a post's likes

Just like **[Q4]**, we query the likes for that post, then aggregate their usernames.

:::image type="content" source="./media/model-partition-example/V1-Q5.png" alt-text="Diagram of retrieving all likes for a post and aggregating their additional data.":::

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `59` ms | `58.92` RU | ⚠ |

### [Q6] List the x most recent posts created in short form (feed)

We fetch the most recent posts by querying the `posts` container sorted by descending creation date, then aggregate usernames and counts of comments and likes for each of the posts.

:::image type="content" source="./media/model-partition-example/V1-Q6.png" alt-text="Diagram of retrieving most recent posts and aggregating their additional data.":::

Once again, our initial query doesn't filter on the partition key of the `posts` container, which triggers a costly fan-out. This one is even worse as we target a larger result set and sort the results with an `ORDER BY` clause, which makes it more expensive in terms of request units.

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `306` ms | `2063.54` RU | ⚠ |

## Reflect on the performance of V1

Looking at the performance issues we faced in the previous section, we can identify two main classes of problems:

- Some requests require multiple queries to be issued in order to gather all the data we need to return.
- Some queries don't filter on the partition key of the containers they target, leading to a fan-out that impedes our scalability.

Let's resolve each of those problems, starting with the first one.

<a id="v2-introducing-denormalization-to-optimize-read-queries">

## V2: Introduce denormalization to optimize read queries

The reason why we have to issue more requests in some cases is because the results of the initial request don't contain all the data we need to return. Denormalizing data solves this kind of issue across our data set when working with a nonrelational data store like Azure Cosmos DB.

In our example, we modify post items to add the username of the post's author, the count of comments and the count of likes:

```json
{
    "id": "<post-id>",
    "type": "post",
    "postId": "<post-id>",
    "userId": "<post-author-id>",
    "userUsername": "<post-author-username>",
    "title": "<post-title>",
    "content": "<post-content>",
    "commentCount": <count-of-comments>,
    "likeCount": <count-of-likes>,
    "creationDate": "<post-creation-date>"
}
```

We also modify comment and like items to add the username of the user who created them:

```json
{
    "id": "<comment-id>",
    "type": "comment",
    "postId": "<post-id>",
    "userId": "<comment-author-id>",
    "userUsername": "<comment-author-username>",
    "content": "<comment-content>",
    "creationDate": "<comment-creation-date>"
}

{
    "id": "<like-id>",
    "type": "like",
    "postId": "<post-id>",
    "userId": "<liker-id>",
    "userUsername": "<liker-username>",
    "creationDate": "<like-creation-date>"
}
```

### Denormalize comment and like counts

What we want to achieve is that every time we add a comment or a like, we also increment the `commentCount` or the `likeCount` in the corresponding post. As `postId` partitions our `posts` container, the new item (comment or like), and its corresponding post sit in the same logical partition. As a result, we can use a [stored procedure](stored-procedures-triggers-udfs.md) to perform that operation.

When you create a comment (**[C3]**), instead of just adding a new item in the `posts` container, we call the following stored procedure on that container:

```javascript
function createComment(postId, comment) {
  var collection = getContext().getCollection();

  collection.readDocument(
    `${collection.getAltLink()}/docs/${postId}`,
    function (err, post) {
      if (err) throw err;

      post.commentCount++;
      collection.replaceDocument(
        post._self,
        post,
        function (err) {
          if (err) throw err;

          comment.postId = postId;
          collection.createDocument(
            collection.getSelfLink(),
            comment
          );
        }
      );
    })
}
```

This stored procedure takes the ID of the post and the body of the new comment as parameters, then:

- retrieves the post.
- increments the `commentCount`.
- replaces the post.
- adds the new comment.

As stored procedures are executed as atomic transactions, the value of `commentCount` and the actual number of comments always stays in sync.

We obviously call a similar stored procedure when adding new likes to increment the `likeCount`.

### Denormalize usernames

Usernames require a different approach as users not only sit in different partitions, but in a different container. When we have to denormalize data across partitions and containers, we can use the source container's [change feed](../change-feed.md).

In our example, we use the change feed of the `users` container to react whenever users update their usernames. When that happens, we propagate the change by calling another stored procedure on the `posts` container:

:::image type="content" source="./media/model-partition-example/denormalization-1.png" alt-text="Diagram of denormalizing usernames into the posts container.":::

```javascript
function updateUsernames(userId, username) {
  var collection = getContext().getCollection();
  
  collection.queryDocuments(
    collection.getSelfLink(),
    `SELECT * FROM p WHERE p.userId = '${userId}'`,
    function (err, results) {
      if (err) throw err;

      for (var i in results) {
        var doc = results[i];
        doc.userUsername = username;

        collection.upsertDocument(
          collection.getSelfLink(),
          doc);
      }
    });
}
```

This stored procedure takes the ID of the user and the user's new username as parameters, then:

- fetches all items matching the `userId` (which can be posts, comments, or likes).
- for each of those items:
  - replaces the `userUsername`.
  - replaces the item.

> [!IMPORTANT]
> This operation is costly because it requires this stored procedure to be executed on every partition of the `posts` container. We assume that most users choose a suitable username during sign-up and won't ever change it, so this update runs very rarely.

## What are the performance gains of V2?

Let's talk about some of the performance gains of V2.

### [Q2] Retrieve a post

Now that our denormalization is in place, we only have to fetch a single item to handle that request.

:::image type="content" source="./media/model-partition-example/V2-Q2.png" alt-text="Diagram of retrieving a single item from the denormalized posts container.":::

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `2` ms | `1` RU | ✅ |

### [Q4] List a post's comments

Here again, we can spare the extra requests that fetched the usernames and end up with a single query that filters on the partition key.

:::image type="content" source="./media/model-partition-example/V2-Q4.png" alt-text="Diagram of retrieving all comments for a denormalized post.":::

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `4` ms | `7.72` RU | ✅ |

### [Q5] List a post's likes

Exact same situation when listing the likes.

:::image type="content" source="./media/model-partition-example/V2-Q5.png" alt-text="Diagram of retrieving all likes for a denormalized post.":::

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `4` ms | `8.92` RU | ✅ |

## V3: Make sure all requests are scalable

There are still two requests that we haven't fully optimized when looking at our overall performance improvements. These requests are **[Q3]** and **[Q6]**. They're the requests involving queries that don't filter on the partition key of the containers they target.

### [Q3] List a user's posts in short form

This request already benefits from the improvements introduced in V2, which spares more queries.

:::image type="content" source="./media/model-partition-example/V2-Q3.png" alt-text="Diagram that shows the query to list a user's denormalized posts in short form.":::

But the remaining query is still not filtering on the partition key of the `posts` container.

The way to think about this situation is simple:

- This request *has* to filter on the `userId` because we want to fetch all posts for a particular user.
- It doesn't perform well because it's executed against the `posts` container, which doesn't have `userId` partitioning it.
- Stating the obvious, we would solve our performance problem by executing this request against a container partitioned with `userId`.
- It turns out that we already have such a container: the `users` container!

So we introduce a second level of denormalization by duplicating entire posts to the `users` container. By doing that, we effectively get a copy of our posts, only partitioned along a different dimension, making them way more efficient to retrieve by their `userId`.

The `users` container now contains two kinds of items:

```json
{
    "id": "<user-id>",
    "type": "user",
    "userId": "<user-id>",
    "username": "<username>"
}

{
    "id": "<post-id>",
    "type": "post",
    "postId": "<post-id>",
    "userId": "<post-author-id>",
    "userUsername": "<post-author-username>",
    "title": "<post-title>",
    "content": "<post-content>",
    "commentCount": <count-of-comments>,
    "likeCount": <count-of-likes>,
    "creationDate": "<post-creation-date>"
}
```

In this example:

- We've introduced a `type` field in the user item to distinguish users from posts.
- We've also added a `userId` field in the user item, which is redundant with the `id` field but is required as the `users` container is now partitioned with `userId` (and not `id` as previously).

To achieve that denormalization, we once again use the change feed. This time, we react on the change feed of the `posts` container to dispatch any new or updated post to the `users` container. And because listing posts doesn't require to return their full content, we can truncate them in the process.

:::image type="content" source="./media/model-partition-example/denormalization-2.png" alt-text="Diagram of denormalizing posts into the users' container.":::

We can now route our query to the `users` container, filtering on the container's partition key.

:::image type="content" source="./media/model-partition-example/V3-Q3.png" alt-text="Diagram of retrieving all posts for a denormalized user.":::

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `4` ms | `6.46` RU | ✅ |

### [Q6] List the x most recent posts created in short form (feed)

We have to deal with a similar situation here: even after sparing the more queries left unnecessary by the denormalization introduced in V2, the remaining query doesn't filter on the container's partition key:

:::image type="content" source="./media/model-partition-example/V2-Q6.png" alt-text="Diagram that shows the query to list the x most recent posts created in short form.":::

Following the same approach, maximizing this request's performance and scalability requires that it only hits one partition. Only hitting a single partition is conceivable because we only have to return a limited number of items. In order to populate our blogging platform's home page, we just need to get the 100 most recent posts, without the need to paginate through the entire data set.

So to optimize this last request, we introduce a third container to our design, entirely dedicated to serving this request. We denormalize our posts to that new `feed` container:

```json
{
    "id": "<post-id>",
    "type": "post",
    "postId": "<post-id>",
    "userId": "<post-author-id>",
    "userUsername": "<post-author-username>",
    "title": "<post-title>",
    "content": "<post-content>",
    "commentCount": <count-of-comments>,
    "likeCount": <count-of-likes>,
    "creationDate": "<post-creation-date>"
}
```

The `type` field partitions this container, which is always `post` in our items. Doing that ensures that all the items in this container will sit in the same partition.

To achieve the denormalization, we just have to hook on the change feed pipeline we have previously introduced to dispatch the posts to that new container. One important thing to bear in mind is that we need to make sure that we only store the 100 most recent posts; otherwise, the content of the container might grow beyond the maximum size of a partition. This limitation can be implemented by calling a [post-trigger](stored-procedures-triggers-udfs.md#triggers) every time a document is added in the container:

:::image type="content" source="./media/model-partition-example/denormalization-3.png" alt-text="Diagram of denormalizing posts into the feed container.":::

Here's the body of the post-trigger that truncates the collection:

```javascript
function truncateFeed() {
  const maxDocs = 100;
  var context = getContext();
  var collection = context.getCollection();

  collection.queryDocuments(
    collection.getSelfLink(),
    "SELECT VALUE COUNT(1) FROM f",
    function (err, results) {
      if (err) throw err;

      processCountResults(results);
    });

  function processCountResults(results) {
    // + 1 because the query didn't count the newly inserted doc
    if ((results[0] + 1) > maxDocs) {
      var docsToRemove = results[0] + 1 - maxDocs;
      collection.queryDocuments(
        collection.getSelfLink(),
        `SELECT TOP ${docsToRemove} * FROM f ORDER BY f.creationDate`,
        function (err, results) {
          if (err) throw err;

          processDocsToRemove(results, 0);
        });
    }
  }

  function processDocsToRemove(results, index) {
    var doc = results[index];
    if (doc) {
      collection.deleteDocument(
        doc._self,
        function (err) {
          if (err) throw err;

          processDocsToRemove(results, index + 1);
        });
    }
  }
}
```

The final step is to reroute our query to our new `feed` container:

:::image type="content" source="./media/model-partition-example/V3-Q6.png" alt-text="Diagram of retrieving the most recent posts.":::

| **Latency** | **Request Units** | **Performance** |
| --- | --- | --- |
| `9` ms | `16.97` RU | ✅ |

## Conclusion

Let's have a look at the overall performance and scalability improvements we've introduced over the different versions of our design.

| | V1 | V2 | V3 |
| --- | --- | --- | --- |
| **[C1]** | `7` ms / `5.71` RU | `7` ms / `5.71` RU | `7` ms / `5.71` RU |
| **[Q1]** | `2` ms / `1` RU | `2` ms / `1` RU | `2` ms / `1` RU |
| **[C2]** | `9` ms / `8.76` RU | `9` ms / `8.76` RU | `9` ms / `8.76` RU |
| **[Q2]** | `9` ms / `19.54` RU | `2` ms / `1` RU | `2` ms / `1` RU |
| **[Q3]** | `130` ms / `619.41` RU | `28` ms / `201.54` RU | `4` ms / `6.46` RU |
| **[C3]** | `7` ms / `8.57` RU | `7` ms / `15.27` RU | `7` ms / `15.27` RU |
| **[Q4]** | `23` ms / `27.72` RU | `4` ms / `7.72` RU | `4` ms / `7.72` RU |
| **[C4]** | `6` ms / `7.05` RU | `7` ms / `14.67` RU | `7` ms / `14.67` RU |
| **[Q5]** | `59` ms / `58.92` RU | `4` ms / `8.92` RU | `4` ms / `8.92` RU |
| **[Q6]** | `306` ms / `2063.54` RU | `83` ms / `532.33` RU | `9` ms / `16.97` RU |

### We've optimized a read-heavy scenario

You might notice that we've concentrated our efforts towards improving the performance of read requests (queries) at the expense of write requests (commands). In many cases, write operations now trigger subsequent denormalization through change feeds, which makes them more computationally expensive and longer to materialize.

We justify this focus on read performance by the fact that a blogging platform, like most social apps, is read-heavy. A read-heavy workload indicates that the amount of read requests it has to serve is usually orders of magnitude higher than the number of write requests. So it makes sense to make write requests more expensive to execute in order to let read requests be cheaper and better performing.

If we look at the most extreme optimization we've done, **[Q6]** went from 2000+ RUs to just 17 RUs; we've achieved that by denormalizing posts at a cost of around 10 RUs per item. As we would serve a lot more feed requests than creation or updates of posts, the cost of this denormalization is negligible considering the overall savings.

### Denormalization can be applied incrementally

The scalability improvements we've explored in this article involve denormalization and duplication of data across the data set. It should be noted that these optimizations don't have to be put in place on day one. Queries that filter on partition keys perform better at scale, but cross-partition queries can be acceptable if they're called rarely or against a limited data set. If you're just building a prototype, or launching a product with a small and controlled user base, you can probably spare those improvements for later. What's important then is to [monitor your model's performance](../use-metrics.md) so you can decide if and when it's time to bring them in.

The change feed that we use to distribute updates to other containers store all those updates persistently. This persistence makes it possible to request all updates since the creation of the container and bootstrap denormalized views as a one-time catch-up operation even if your system already has many data.

## Next steps

After this introduction to practical data modeling and partitioning, you might want to check the following articles to review the concepts:

- [Databases, containers, and items in Azure Cosmos DB](../resource-model.md)
- [Partitioning and horizontal scaling in Azure Cosmos DB](../partitioning-overview.md)
- [Change feed in Azure Cosmos DB](../change-feed.md)
