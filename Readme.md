# Readme

## Purpose
The purpose of this app is to be able to extract reports from checklist items on cards on a Trello board and filter it all in Excel. After starting on this script I came across the Blue Cat Reports plugin for Trello which does this. However, when I saw that after my 7 day trial I would have to pay AUD$600/year (AUD$60/member/year) I decided to continue on with this project. 

This will be done by extracting every checklist item out of every card in a Trello board and adding it as a line on a Excel sheet. The format of the sheet will be (ordered by date, decending order):

| Card title  | Card Link | List | Checklist | Name | Due | Member |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| abc | url | abc | abc | abc| date | abc |

## Improvements
* trello_exports dataframe needs to be saved back to something global so it can be used for graphical reports
* Export Excel with tab for each person and unassigned
* Generate reports of quantities of items under each person by date range

## Work done
* 16/7/22 First revision to main branch of working code.

## References
* Trello api reference: https://developer.atlassian.com/cloud/trello/rest/api-group-actions/