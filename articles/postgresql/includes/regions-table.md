---
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 12/22/2025
ms.service: azure-database-postgresql
ms.topic: include
---
| Region | Intel Compute | AMD Compute | Confidential Compute | Zone-Redundant HA | Same-Zone HA | Geo-Redundant backup |
| --- | --- | --- | --- | --- | --- | --- |
| Australia Central | :white_check_mark: (v3/v4/v5) | :x: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| Australia Central 2 * | :white_check_mark: (v3/v4/v5) | :x: | :x: | :x: | :white_check_mark: | :x: |
| Australia East | :white_check_mark: (v3/v4/v5/v6) | :white_check_mark: (v5) | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Australia Southeast | :white_check_mark: (v3/v4/v5) | :x: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| Austria East | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5) | :x: | :white_check_mark: | :white_check_mark: | :x: |
| Belgium Central | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5) | :x: | :white_check_mark: | :white_check_mark: | :x: |
| Brazil South | :white_check_mark: (v3/v4/v5) | :x: | :x: | :white_check_mark: $ | :white_check_mark: | :x: |
| Brazil Southeast * | :white_check_mark: (v3/v4/v5) | :x: | :x: | :x: | :white_check_mark: | :x: |
| Canada Central | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5) | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Canada East | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5) | :x: | :x: | :white_check_mark: | :white_check_mark: |
| Central India | :white_check_mark: (v3/v4/v5) | :x: | :x: | :white_check_mark: $ | :white_check_mark: | :white_check_mark: |
| Central US | :white_check_mark: (v3/v4/v5) | :x: | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Chile Central | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5) | :x: | :white_check_mark: | :white_check_mark: | :x: |
| China East 2 | :white_check_mark: (v3/v4) | :x: | :x: | :x: | :white_check_mark: | :x: |
| China East 3 | :white_check_mark: (v3/v4) | :x: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| China North 2 | :white_check_mark: (v3/v4) | :x: | :x: | :x: | :white_check_mark: | :x: |
| China North 3 | :white_check_mark: (v3/v4/v5) | :x: | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| East Asia | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v6) | :x: | :white_check_mark: $ ** | :white_check_mark: | :white_check_mark: |
| East US | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5) | :x: | :white_check_mark: $ | :white_check_mark: | :white_check_mark: |
| East US 2 | :white_check_mark: (v3/v4) | :x: | :x: | :white_check_mark: $ | :white_check_mark: | :white_check_mark: |
| France Central | :white_check_mark: (v3/v4/v5) | :x: | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| France South | :white_check_mark: (v3/v4/v5) | :x: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| Germany North * | :white_check_mark: (v3/v4/v5) | :x: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| Germany West Central | :white_check_mark: (v3/v4/v5) | :x: | :x: | :white_check_mark: $ | :white_check_mark: | :white_check_mark: |
| Indonesia Central | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5/v6) | :x: | :white_check_mark: | :white_check_mark: | :x: |
| Israel Central | :white_check_mark: (v3/v4) | :x: | :x: | :white_check_mark: | :white_check_mark: | :x: |
| Italy North | :white_check_mark: (v3/v4/v5) | :x: | :x: | :white_check_mark: | :white_check_mark: | :x: |
| Japan East | :white_check_mark: (v3/v4) | :x: | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Japan West | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v6) | :x: | :x: | :white_check_mark: | :white_check_mark: |
| Jio India Central | :white_check_mark: (v3) | :x: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| Jio India West | :white_check_mark: (v3) | :x: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| Korea Central | :white_check_mark: (v3/v4/v5) | :x: | :x: | :white_check_mark: ** | :white_check_mark: | :white_check_mark: |
| Korea South | :white_check_mark: (v3/v4/v5) | :x: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| Malaysia West | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5/v6) | :x: | :white_check_mark: | :white_check_mark: | :x: |
| Mexico Central | :white_check_mark: (v3/v4) | :x: | :x: | :white_check_mark: $ | :white_check_mark: | :x: |
| New Zealand North | :white_check_mark: (v3/v4/v5) | :x: | :x: | :white_check_mark: | :white_check_mark: | :x: |
| North Central US | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5) | :x: | :x: | :white_check_mark: | :white_check_mark: |
| North Europe | :white_check_mark: (v3/v4/v5) | :x: | :white_check_mark: (v5) | :white_check_mark: $ | :white_check_mark: | :white_check_mark: |
| Norway East * | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5) | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Norway West | :white_check_mark: (v3/v4/v5) | :x: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| Poland Central | :white_check_mark: (v3/v4) | :x: | :x: | :white_check_mark: | :white_check_mark: | :x: |
| Qatar Central | :white_check_mark: (v3/v4) | :x: | :x: | :white_check_mark: $ | :white_check_mark: | :x: |
| South Africa North | :white_check_mark: (v3/v4/v5) | :x: | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| South Africa West * | :white_check_mark: (v3/v4/v5) | :x: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| South Central US | :white_check_mark: (v3/v4) | :x: | :x: | :white_check_mark: $ | :white_check_mark: | :white_check_mark: |
| South India | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v6) | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Southeast Asia | :white_check_mark: (v3/v4) | :x: | :x: | :white_check_mark: $ | :white_check_mark: | :white_check_mark: |
| Spain Central | :white_check_mark: (v3/v4) | :x: | :x: | :white_check_mark: | :white_check_mark: | :x: |
| Sweden Central | :white_check_mark: (v3/v4/v5) | :x: | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Switzerland North | :white_check_mark: (v3/v4/v5) | :x: | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Switzerland West * | :white_check_mark: (v3/v4/v5) | :x: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| UAE Central * | :white_check_mark: (v3/v4/v5) | :x: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| UAE North | :white_check_mark: (v3/v4/v5) | :x: | :white_check_mark: (v5) | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| UK South | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5) | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| UK West | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5) | :x: | :x: | :white_check_mark: | :white_check_mark: |
| US Gov Arizona | :white_check_mark: (v3/v4) | :x: | :x: | :x: | :white_check_mark: | :x: |
| US Gov Texas | :white_check_mark: (v3/v4) | :x: | :x: | :x: | :white_check_mark: | :x: |
| US Gov Virginia | :white_check_mark: (v3/v4) | :x: | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| West Central US | :white_check_mark: (v3/v4/v5) | :x: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| West Europe | :white_check_mark: (v3/v4/v5) | :x: | :white_check_mark: (v5) | :white_check_mark: $ | :white_check_mark: | :white_check_mark: |
| West US | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5) | :x: | :x: | :white_check_mark: | :white_check_mark: |
| West US 2 | :white_check_mark: (v3/v4) | :x: | :x: | :white_check_mark: $ | :white_check_mark: | :white_check_mark: |
| West US 3 | :white_check_mark: (v3/v4/v5) | :white_check_mark: (v5) | :x: | :white_check_mark: ** | :white_check_mark: | :x: |
