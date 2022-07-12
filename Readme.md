# Readme

## Purpose
The purpose of this app is to be able to extract reports from checklist items on cards on a Trello board and filter it all in Excel. After starting on this script I came across the Blue Cat Reports plugin for Trello which does this. However, when I saw that after my 7 day trial I would have to pay AUD$600/year (AUD$60/member/year) I decided to continue on with this project. 

This will be done by extracting every checklist item out of every card in a Trello board and adding it as a line on a Excel sheet. The format of the sheet will be (ordered by date, decending order):

| Card title  | Card Link | List | Checklist | Name | Due | Member | Priority |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| abc | url | abc | abc | abc| date | abc | num |

## Up to
* trello_calls.py - simplify so script is first just saving data from api then is loading that data into a (trello_structure.py)
* trello_export.py - loop over a to export as required

## Work done
* I started itterating through building up the required data. I am going to hit my API rate limit. I need to re-organise to get ALL cards, lists, checklists etc. from the board upfront then work with that.

## References
* Trello api reference: https://developer.atlassian.com/cloud/trello/rest/api-group-actions/