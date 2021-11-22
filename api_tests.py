import pysmashgg
import time
import datetime

import pysmashgg

smash = pysmashgg.SmashGG('cdf44206c53568bd509e4799561332af')
minEntrants = 50
# 1 -> Melee
# 1386 -> Super Smash Bros. Ultimate
videogameId = 1386
maxPage = 100
startDate = "01/01/2021"
endDate = "01/01/2022"
startStamp = 1609459200 # time.mktime(datetime.datetime.strptime(startDate, "%d/%m/%Y").timetuple())
endStamp = 1640995200 # time.mktime(datetime.datetime.strptime(endDate, "%d/%m/%Y").timetuple())

players1 = [
    {
        'id': 1,
        'name': 'one',
        'placement': 1
    },
    {
        'id': 2,
        'name': 'two',
        'placement': 2
    },
    {
        'id': 3,
        'name': 'three',
        'placement': 3
    },
]

players2 = [
    {
        'id': 1,
        'name': 'one',
        'placement': 1
    },
    {
        'id': 4,
        'name': 'four',
        'placement': 2
    },
    {
        'id': 5,
        'name': 'five',
        'placement': 3
    },
]

tournaments = [players1, players2]
playerDB = {}

for tournament in tournaments:
    results = tournament
    for entrant in results:
        if entrant['id'] in playerDB:
            print("I found a repeated player!")
            playerDB[entrant['id']] = {
                'name': entrant['name'],
                'sumPlacement':  playerDB[entrant['id']]['sumPlacement'] + entrant['placement'],
                'amountJoined': playerDB[entrant['id']]['amountJoined'] + 1
            }
        else:
            playerDB[entrant['id']] = {
                'name': entrant['name'],
                'sumPlacement': entrant['placement'],
                'amountJoined': 1
            }



sortedIds = sorted(playerDB, key = lambda id: playerDB[id]['amountJoined'])
print(playerDB[sortedIds[-1]])
