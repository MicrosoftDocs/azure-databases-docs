---
title: How to query, interpret and apply index recommendations
description: This article describes how to query, interpret, and apply the recommendations produced by index tuning feature in Azure Database for PostgreSQL - Flexible Server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 11/06/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: how-to
---
# Use index recommendations produced by index tuning in Azure Database for PostgreSQL - Flexible Server

Index tuning persists the recommendations it makes in a set of tables located under the `intelligentperformance` schema in the `azure_sys` database.

Currently, that information can be read using the Azure portal page build for this purpose or by executing queries to retrieve data from two views available inside the `intelligent performance` of the `azure_sys` database.

## Consume index recommendations through the Azure portal

1. Sign in to the Azure portal and select your Azure Database for PostgreSQL flexible server instance.
1. Select **Index tuning** in the **Intelligent Performance** section of the menu.

   - If the feature is enabled but no recommendations are produced yet, the screen looks like this:

     :::image type="content" source="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-page-when-enabled-and-no-recommendations.png" alt-text="Screenshot that shows the aspect of 'Index tuning' page when the feature is enabled but there aren't recommendations." lightbox="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-page-when-enabled-and-no-recommendations.png":::

   - If the feature is currently disabled and it never produced recommendations in the past, the screen looks like this:

     :::image type="content" source="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-page-when-disabled-and-no-recommendations.png" alt-text="Screenshot that shows the aspect of 'Index tuning' page when the feature is disabled and there aren't recommendations." lightbox="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-page-when-disabled-and-no-recommendations.png":::

   - If the feature is enabled and no recommendations are produced yet, the screen looks like this:

     :::image type="content" source="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-page-when-enabled-and-no-recommendations.png" alt-text="Screenshot that shows the aspect of 'Index tuning' page when the feature is enabled and there aren't recommendations." lightbox="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-page-when-enabled-and-no-recommendations.png":::

   - If the feature is disabled but it ever produced recommendations, the screen looks like this:

     :::image type="content" source="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-page-when-disabled-and-has-recommendations.png" alt-text="Screenshot that shows the aspect of 'Index tuning' page when the feature is disabled and there are recommendations." lightbox="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-page-when-disabled-and-has-recommendations.png":::

1. If there are recommendations available, select on the **View index recommendations** summarization to access to the full list:

     :::image type="content" source="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-page-access-full-list-via-summarization-card.png" alt-text="Screenshot that shows the aspect of 'Index tuning' page when there are recommendations, and the way to get to the full list." lightbox="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-page-access-full-list-via-summarization-card.png":::

1. The list shows all available recommendations with some details for each of them. By default, the list is sorted by **Last recommended** in descending order, showing the most recent recommendations at the top. However, you can sort by any other column and can use the filtering box to reduce the list of items shown to those items whose database, schema, or table names contain the text that is provided:

     :::image type="content" source="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-index-recommendations-page.png" alt-text="Screenshot that shows the aspect of 'Index recommendations' page with several recommendations." lightbox="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-index-recommendations-page.png":::

1. To see further information about any specific recommendation, select on the name of that recommendation, and the **Index recommendation details** pane opens on the right side of the screen to surface all available details about the recommendation:

     :::image type="content" source="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-index-recommendation-details-page.png" alt-text="Screenshot that shows the aspect of 'Index recommendation details' pane for one particular recommendation." lightbox="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-index-recommendation-details-page.png":::

## Consume index recommendations through views available in azure_sys database

1. Connect to the `azure_sys` database available in your server with any role that has permission to connect to the instance. Members of the `public` role can read from these views.
1. Execute queries on the `sessions` view to retrieve the details about recommendation sessions.
1. Execute queries on the `recommendations` view to retrieve the recommendations produced by index tuning for CREATE INDEX and DROP INDEX.

### Views

Views in the `azure_sys` database provide a convenient way to access and retrieve index recommendations generated by index tuning. Specifically, the `createindexrecommendations` and `dropindexrecommendations` views contain detailed information about CREATE INDEX and DROP INDEX recommendations, respectively. These views expose data such as the session ID, database name, advisor type, start and stop times of the tuning session, recommendation ID, recommendation type, reason for the recommendation, and other relevant details. By querying these views, users can easily access and analyze the index recommendations produced by index tuning.

#### intelligentperformance.sessions

The `sessions` view exposes all the details for all index tuning sessions.

| column name | data type | Description |
| --- | --- | --- |
| session_id | uuid | Globally Unique Identifier assigned to every new tuning session that is initiated. |
| database_name | varchar(64) | Name of the database in whose context the index tuning session was executed. |
| session_type | intelligentperformance.recommendation_type | Indicates the types of recommendations this index tuning session could produce. Possible values are: `CreateIndex`, `DropIndex`. Sessions of `CreateIndex` type can produce recommendations of `CreateIndex` type. Sessions of `DropIndex` type can produce recommendations of `DropIndex` or `ReIndex` types. |
| run_type | intelligentperformance.recommendation_run_type | Indicates the way in which this session was initiated. Possible values are: `Scheduled`. Sessions automatically executed as per the value of `index_tuning.analysis_interval`, are assigned a run type of `Scheduled`. |
| state | intelligentperformance.recommendation_state | Indicates the current state of the session. Possible values are: `Error`, `Success`, `InProgress`. Sessions whose execution failed are set as `Error`. Sessions that completed their execution correctly, whether or not they generated recommendations, are set as `Success`. Sessions which are still executing are set as `InProgress`. |
| start_time | timestamp without timezone | Timestamp at which the tuning session that produced this recommendation was started. |
| stop_time | timestamp without timezone | Timestamp at which the tuning session that produced this recommendation was started. NULL if the session is in progress or was aborted due to some failure. |
| recommendations_count | integer | Total number of recommendations produced in this session. |

#### intelligentperformance.recommendations

The `recommendations` view exposes all the details for all recommendations generated on any tuning session whose data is still available in the underlying tables.

| column name | data type | Description |
| --- | --- | --- |
| recommendation_id | integer | Number that uniquely identifies a recommendation in the whole server. |
| last_known_session_id | uuid | Every index tuning session is assigned a Globally Unique Identifier. The value in this column represents that of the session which most recently produced this recommendation. |
| database_name | varchar(64) | Name of the database in whose context was produced the recommendation. |
| recommendation_type | intelligentperformance.recommendation_type | Indicates the type of the recommendation produced. Possible values are: `CreateIndex`, `DropIndex`, `ReIndex`. |
| initial_recommended_time | timestamp without timezone | Timestamp at which the tuning session that produced this recommendation was started. |
| last_recommended_time | timestamp without timezone | Timestamp at which the tuning session that produced this recommendation was started. |
| times_recommended | integer | Timestamp at which the tuning session that produced this recommendation was started. |
| reason | text | Reason justifying why this recommendation was produced. |
| recommendation_context | json | Contains the list of query identifiers for the queries that are affected by the recommendation, the type of index being recommended, the name of the schema and the name of the table on which the index is being recommended, the index columns, the index name, and the estimated size in bytes of the recommended index. |

##### Reasons for create index recommendations

When index tuning recommends the creation of an index, it does add at least one of the following reasons:

| Reason |
| ------ |
| `Column <column> appear in Join On clause(s) in query <queryId>` |
| `Column <column> appear in Equal Predicate clause(s) in query <queryId>` |
| `Column <column> appear in Non-Equal Predicate clause(s) in query <queryId>` |
| `Column <column> appear in Group By clause(s) in query <queryId>` |
| `Column <column> appear in Order By clause(s) in query <queryId>` |

##### Reasons for drop index recommendations

When index tuning identifies any indexes which are marked as invalid, it proposes to drop it with the following reason:

`The index is invalid and the recommended recovery method is to reindex.`

 To learn more about why and when indexes are marked as invalid, refer to the [REINDEX](https://www.postgresql.org/docs/current/sql-reindex.html#DESCRIPTION) in PostgreSQL official documentation.

##### Reasons for drop index recommendations

When index tuning detects an index which is unused for, at least, the number of days set in `index_tuning.unused_min_period`, it proposes to drop it with the following reason:

`The index is unused in the past <days_unused> days.`

When index tuning detects duplicate indexes, one of the duplicates survives, and it proposes to drop the remaining. The reason provided always has the following starting text:

`Duplicate of <surviving_duplicate>.` 

Followed by another text which explains the reason why each of the duplicates have been chosen for drop:

| Reason |
| ------ |
| `The equivalent index "<surviving_duplicate>" is a Primary key, while "<droppable_duplicate>" is not.` |
| `The equivalent index "<surviving_duplicate>" is a unique index, while "<droppable_duplicate>" is not.` |
| `The equivalent index "<surviving_duplicate>" is a constraint, while "<droppable_duplicate>" is not.` |
| `The equivalent index "<surviving_duplicate>" is a valid index, while "<droppable_duplicate>" is not.` |
| `The equivalent index "<surviving_duplicate>" has been chosen as replica identity, while "<droppable_duplicate>" is not.` |
| `The equivalent index "<surviving_duplicate>" was used to cluster the table, while "<droppable_duplicate>" was not.` |
| `The equivalent index "<surviving_duplicate>" has a smaller estimated size compared to "<droppable_duplicate>".` |
| `The equivalent index "<surviving_duplicate>" has more tuples compared to "<droppable_duplicate>".` |
| `The equivalent index "<surviving_duplicate>" has more index scans compared to "<droppable_duplicate>".` |
| `The equivalent index "<surviving_duplicate>" has been fetched more times compared to "<droppable_duplicate>".` |
| `The equivalent index "<surviving_duplicate>" has been read more times compared to "<droppable_duplicate>".` |
| `The equivalent index "<surviving_duplicate>" has a shorter length compared to "<droppable_duplicate>".` |
| `The equivalent index "<surviving_duplicate>" has a smaller oid compared to "<droppable_duplicate>".` |

If the index not only is removable due to duplication, but also is unused for, at least, the number of days set in `index_tuning.unused_min_period`, the following text is appended to the reason:

`Also, the index is unused in the past <days_unused> days.`

## Apply index recommendations

Index recommendations contain the SQL statement that you can execute to implement the recommendation.

The following sections will demonstrate how this statement can be obtained for a particular recommendation.

Once you have the statement, you can use any PostgreSQL client of your preference to connect to your server and apply the recommendation. 

### Obtain SQL statement through **Index tuning** page in Azure portal

1. Sign in to the Azure portal and select your Azure Database for PostgreSQL flexible server instance.
1. Select **Index tuning** in the **Intelligent Performance** section of the menu.
1. Assuming index tuning has already produced recommendations, select the **View index recommendations** summarization to access the list of available recommendations.

     :::image type="content" source="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-page-access-full-list-via-summarization-card.png" alt-text="Screenshot that shows the aspect of 'Index tuning' page when there are recommendations, and the way to get to the full list." lightbox="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-page-access-full-list-via-summarization-card.png":::

1. From the list of recommendations, either:

    - Select the ellipsis to the right of the recommendation for which you want to obtain the SQL statement, and select **Copy SQL script**. 

       :::image type="content" source="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-index-recommendations-copy-sql-script.png" alt-text="Screenshot that shows how to copy SQL statement from 'Index recommendations' page." lightbox="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-index-recommendations-page.png":::

    - Or select the name of the recommendation to show its **Index recommendation details**, and select the  copy to clipboard icon in the **SQL script** text box to copy the SQL statement.

       :::image type="content" source="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-index-recommendation-details-copy-sql-script.png" alt-text="Screenshot that shows how to copy SQL statement from 'Index recommendation details' page." lightbox="media/how-to-get-and-apply-recommendations-from-index-tuning/index-tuning-index-recommendation-details-copy-sql-script.png":::

## Related content

- [Index tuning in Azure Database for PostgreSQL - Flexible Server](concepts-index-tuning.md)
- [Configure index tuning in Azure Database for PostgreSQL - Flexible Server](how-to-configure-index-tuning.md)
- [Monitor performance with Query Store](concepts-query-store.md)
- [Usage scenarios for Query Store - Azure Database for PostgreSQL - Flexible Server](concepts-query-store-scenarios.md)
- [Best practices for Query Store - Azure Database for PostgreSQL - Flexible Server](concepts-query-store-best-practices.md)
- [Query Performance Insight for Azure Database for PostgreSQL - Flexible Server](concepts-query-performance-insight.md)
