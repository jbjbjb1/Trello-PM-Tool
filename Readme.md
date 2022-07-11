# Readme

## Purpose
The purpose of this app is to be able to extract reports from checklist items on cards on a Trello board and filter it all in Excel.

This will be done by extracting every checklist item out of every card in a Trello board and adding it as a line on a Excel sheet. The format of the sheet will be:

| Card title  | Members | Checklist Group | Checklist entry | Completed | Assigned to | Assigned to |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| abc | abc | abc | abc | Y/N | abc | date |

## Up to
* I started itterating through building up the required data. I am going to hit my API rate limit. I need to re-organise to get ALL cards, lists, checklists etc. from the board upfront then work with that.

## References
* Trello api reference: https://developer.atlassian.com/cloud/trello/rest/api-group-actions/