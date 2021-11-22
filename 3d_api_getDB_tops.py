import pysmashgg
import time
import datetime
import csv
import pysmashgg

smash = pysmashgg.SmashGG('API KEY')
minEntrants = 50
# 1 -> Super Smash Bros. Melee
# 1386 -> Super Smash Bros. Ultimate
videogameId = 1386
# Max query is up to 10,000th element, pre size filtering. 32 tournaments per page. 310 = 9,920 elements.
maxPage = 15
startDate = "22/5/2021" # 1609459200
endDate = "22/11/2021" # 1640995200
startStamp = 1621727723 # time.mktime(datetime.datetime.strptime(startDate, "%d/%m/%Y").timetuple())
endStamp = 1637628923 # time.mktime(datetime.datetime.strptime(endDate, "%d/%m/%Y").timetuple())
# If you only want to consider the créme-de-la-créme
onlyTop = 50

tournaments = []
totalTournaments = 0
playerDB = {}
csv_columns = ['name', 'sumPlacement', 'amountJoined', 'amountTopped']
csv_file = '3dPlayerDBTops.csv'

requestCounter = 0

start = time.time()

for i in range(1, maxPage+1):
    print("iteration: ", i)
    try:
        tournaments = (smash.tournament_show_event_by_game_size_dated(minEntrants, videogameId, startStamp, endStamp, i))
        requestCounter += 1
        if requestCounter >= 58:
            print("API limit sleep")
            time.sleep(60)
            requestCounter = 0
    except Exception as e:
        print("End of tournament block.")
        print(e)
        pass # i+=1

    print("Tournaments found: ", len(tournaments))
    totalTournaments += len(tournaments)

    for tournament in tournaments:
        if isinstance(tournament, list):
            # This means it's a multi-event tournament, and it can be discarded.
            print("I am list")
        else:
            eventId = tournament['eventId']
            numAttendees = tournament['numEntrants']
            topRequirement = 16 if (numAttendees > 100) else 8
            maxPage = (numAttendees // 64) + 1
            for j in range(1, maxPage + 1):
                try:
                    results = smash.event_show_lightweight_results(eventId, 1)
                    requestCounter += 1
                    if requestCounter >= 58:
                        print("API limit sleep")
                        time.sleep(60)
                        requestCounter = 0
                    if results != []:
                        for entrant in results:
                            if entrant['name'] in playerDB and entrant['placement'] <= onlyTop:
                                playerDB[entrant['name']] = {
                                    'name': entrant['name'],
                                    'sumPlacement':  playerDB[entrant['name']]['sumPlacement'] + entrant['placement'],
                                    'amountJoined': playerDB[entrant['name']]['amountJoined'] + 1,
                                    'amountTopped': playerDB[entrant['name']]['amountTopped'] + (1 if (entrant['placement'] <= topRequirement) else 0)
                                }
                            elif entrant['placement'] <= onlyTop:
                                playerDB[entrant['name']] = {
                                'name': entrant['name'],
                                'sumPlacement': entrant['placement'],
                                'amountJoined': 1,
                                'amountTopped': 1 if (entrant['placement'] <= topRequirement) else 0
                            }
                            else:
                                break
                except:
                    print("End of participant list")
                    break

sortedIds = sorted(playerDB, key = lambda id: playerDB[id]['amountJoined'])
print(playerDB[sortedIds[-1]])

try:
    with open(csv_file, 'w', newline='',  encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for key in playerDB:
            writer.writerow(playerDB[key])
except IOError:
    print("I/O error")

end = time.time()
totalTime = end - start

f = open("3d_tops_DB_build_log.txt", "w")
f.write("Player 3D standings database logs\n")
f.write("Start date: " + str(startDate) + "\n")
f.write("End date: " + str(endDate) + "\n")
f.write("Minimum participants: " + str(minEntrants) + "\n")
f.write("Game: " + ('Melee\n' if (videogameId == 1) else 'Ultimate\n'))
f.write("Tournaments queried: " + str(maxPage*32) + "\n")
f.write("Distinct players: " + str(len(playerDB)) + "\n")
f.write("Only take Top: " + str(onlyTop) + "\n")
f.write("Tournaments after filters: " + str(totalTournaments) + "\n")
f.write("Time elapsed to build: " + str(totalTime) + "\n")
f.close()