# K-Means SSBU/M Player Power Ranking

## Introduction

This is a k-means approach to tiering players that compete often and consistently place in the top ranks.

The goal for this solution is to create a handy method of generating dately power rankings for seeding tournaments, amusement, and strategizing.

---

## Used Technologies

Most importantly, this algorithm is fed from smash.gg's GraphQL API that's open for 3rd party developers. [Link](https://developer.smash.gg/docs/intro/) (named SGA onwards)

Used [JeremySkalla's Wrapper](https://github.com/JeremySkalla/pysmashgg) for quicker use of requests and calls to the API.

SciKit-Learn's Toolkit, as the framework to run the clustering algorithms with.

Python 3.9

Jupyter Notebook

## Preproduction

Using this tool, we want to create a tier list that can tell us how consistent a player is at ranking in the top spots, specifically in Super Smash Bros. Ultimate or Super Smash Bros. Melee.  
In order to obtain this, we need to select what we will be ranking the players against.  
In order to have useful placement data, it was decided to only use tournaments with at least 50 confirmed participants. This will provide the system the possibility for less variance, a standarized minimum, and leave out small local, outlying tournaments.  
Due to restrictions on querying SGA, all responses are paginated, with a limit of 10,000 elements. So if we query for ALL tournaments ever created on the platform, we would only be able to work with the most recent (or oldest) 10,000.  
Therefore, we also have date delimiters. We give the query a start and end date to search for tournaments.  

## Building the Dataset

Calls to the SGA is limited to specific filters, schemas, and object types.  
In order to get the necessary dataset to run 