# Compiles a list of fast moves and charge moves, along with their power and energy stats.

from bs4 import BeautifulSoup
import requests
import csv
import re
from csv_functions import write_to_csv
from csv_functions import reset_csv

fastmoveCSV = "pokeData/fastmoves.csv"
chargemoveCSV = "pokeData/chargemoves.csv"

parenPattern = re.compile(r".*\s\(.*\)")

def fastmove_parser():
    moveEntries = requests.get('https://gamepress.gg/pokemongo/pvp-fast-moves')
    moveSoup = BeautifulSoup(moveEntries.content, 'html.parser', from_encoding='utf8')
    moveTable = moveSoup.find('table', id = "sort-table")#  cols-7 finished-loading")
    moveChunks = moveTable.find_all('tr')

    write_to_csv(fastmoveCSV, ['Name','Type','Power','Turns','Energy'])
    for move in moveChunks:
        moveFields = move.find_all('td')
        if len(moveFields) != 0:
            moveName = moveFields[0].text.strip()
            moveType = move['class'][0]
            movePower = moveFields[1].text
            moveTurns = str(int(moveFields[2].text) + 1)
            moveEnergy = moveFields[3].text
            write_to_csv(fastmoveCSV, [moveName, moveType, movePower, moveTurns, moveEnergy])
        else:
            continue


# Find a convenient way to mark debuffing moves
def chargemove_parser():
    moveEntries = requests.get('https://gamepress.gg/pokemongo/pvp-charge-moves')
    moveSoup = BeautifulSoup(moveEntries.content, 'html.parser', from_encoding='utf8')
    moveTable = moveSoup.find('table', id = "sort-table")
    moveChunks = moveTable.find_all('tr')

    write_to_csv(chargemoveCSV, ['Name','Type','Power','Energy'])
    for move in moveChunks:
        moveFields = move.find_all('td')
        if len(moveFields) != 0 and (re.match(parenPattern, moveFields[0].text) is None or moveFields[0].text.strip() == "Techno Blast (Burn)"):
            moveName = moveFields[0].text.strip()
            moveType = move['class'][0]
            movePower = moveFields[1].text
            moveEnergy = moveFields[2].text
            write_to_csv(chargemoveCSV, [moveName, moveType, movePower, moveEnergy])
        else:
            continue

reset_csv(fastmoveCSV)
fastmove_parser()
reset_csv(chargemoveCSV)
chargemove_parser()