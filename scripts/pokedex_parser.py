# We want a list of all Pokemon and some of their basic data, including type/attack/defense/stamina/move lists
# We also need to account for variations of the same Pokemon, with Name and FullName headings.
# Data source: https://pokemondb.net/go/pokedex

from bs4 import BeautifulSoup
import requests
import csv
import re
from csv_functions import write_to_csv
from csv_functions import reset_csv

tdPattern = re.compile(r"</?td[^<>]*>")
spanPattern = re.compile(r"</?span[^<>]*>")
parenPattern = re.compile(r"\s\(.*\)")

generaldataCSV = "pokeData/Pokemon Stats.csv"

def pokeScraper():
    pokedexEntries = requests.get('https://pokemondb.net/go/pokedex')
    pokedexSoup = BeautifulSoup(pokedexEntries.content, 'html.parser', from_encoding='utf8')
    pokeTable = pokedexSoup.find("main", class_ = "main-content grid-container")
    pokeChunks = pokeTable.find_all("tr")

    write_to_csv(generaldataCSV, ['#','Name','FullName','Type 1','Type 2','Attack','Defense','Stamina','Catch','Flee','Fast Moves','Charge Moves'])
    index = 0

    for pokemon in pokeChunks:
        # Get Pokemon Names
        pokeFind = pokemon.find("a", class_ = "ent-name")
        if pokeFind is not None:
            pokeName = pokeFind.text
            pokeFullName = pokeName # Missing both Nidoran because of male/female symbol, fix TBD
        else:
            continue
        pokeAltNameSearch = pokemon.find("small", class_ = "text-muted")
        # Account for alternative versions of the same Pokemon, same of them can have different move options
        if pokeAltNameSearch is not None:
            pokeAltName = pokeAltNameSearch.text
            pokeFullName = pokeName + " (" + pokeAltName + ")"

        # Get pokemon element for strengths/weaknesses
        pokeTypeList = pokemon.find_all("a", class_ = "type-icon")
        if len(pokeTypeList) > 0:
            #pokeTypes = ";".join(pokeTypeList[i].text for i in range(len(pokeTypeList)))
            pokeType1 = pokeTypeList[0].text
            if len(pokeTypeList) == 2:
                pokeType2 = pokeTypeList[1].text
        else:
            continue

        # Get Pokemon Number, Attack, Defense, Stamina, and Catch/Flee rates
        pokeStatList = pokemon.find_all("td", class_ = "cell-num")
        if len(pokeStatList) > 0: 
            pokeNumber = pokeStatList[0].text
            pokeAttack = pokeStatList[1].text
            pokeDefense =pokeStatList[2].text
            pokeStamina = pokeStatList[3].text
            pokeCatch = pokeStatList[4].text
            pokeFlee = pokeStatList[5].text
        else:
            continue

        pokeMoveList = pokemon.find_all("td", class_ = "text-small")
        if len(pokeMoveList) > 0:
            pokeFastMoves = str(pokeMoveList[0])
            pokeChargeMoves = str(pokeMoveList[1])
            pokeFastMoves = pokeFastMoves.replace("<br/>", ";")[:-1]
            pokeChargeMoves = pokeChargeMoves.replace("<br/>", ";")[:-1]
            if re.match(tdPattern, pokeFastMoves):
                pokeFastMoves = re.sub(tdPattern, "", pokeFastMoves)
                pokeFastMoves = re.sub(spanPattern, "", pokeFastMoves)
                pokeFastMoves = re.sub(parenPattern, "", pokeFastMoves).strip()
            if re.match(tdPattern, pokeChargeMoves):
                pokeChargeMoves = re.sub(tdPattern, "", pokeChargeMoves)
                pokeChargeMoves = re.sub(spanPattern, "", pokeChargeMoves)
                pokeChargeMoves = re.sub(parenPattern, "", pokeChargeMoves).strip()
        else:
            continue
        
        index += 1
        write_to_csv(generaldataCSV, [pokeNumber, pokeName, pokeFullName, pokeType1, pokeType2, pokeAttack, pokeDefense, pokeStamina, pokeCatch, pokeFlee, pokeFastMoves, pokeChargeMoves])

reset_csv(generaldataCSV)
pokeScraper()
