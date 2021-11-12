from bs4 import BeautifulSoup
import requests
import csv
import re

tdPattern = re.compile(r"</?td[^<>]*>")
spanPattern = re.compile(r"</?span[^<>]*>")
parenPattern = re.compile(r"\s\(.*\)")

generaldataCSV = "Pokemon Stats.csv"
movecombosCSV = "Pokemon Move Combinations.csv"


def pokeScraper():
    pokedexEntries = requests.get('https://pokemondb.net/go/pokedex')
    pokedexSoup = BeautifulSoup(pokedexEntries.content, 'html.parser', from_encoding='utf8')
    pokeTable = pokedexSoup.find("main", class_ = "main-content grid-container")
    pokeChunks = pokeTable.find_all("tr")

    write_to_csv(generaldataCSV, ['ID','Name','FullName','TypeA','TypeB','Catch','Flee','Fast Moves','Charge Moves'])
    index = 0

    for pokemon in pokeChunks:
        # Get Pokemon Names
        pokeFind = pokemon.find("a", class_ = "ent-name")
        if pokeFind is not None:
            pokeName = pokeFind.text
            pokeFullName = pokeName
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
            pokeTypeA = pokeTypeList[0].text
            if len(pokeTypeList) == 2:
                pokeTypeB = pokeTypeList[1].text
        else:
            continue
        # Get Catch and Flee rates, HP/Def/Stamina can be found in a different spreadsheet
        pokeStatList = pokemon.find_all("td", class_ = "cell-num")
        if len(pokeStatList) > 0: 
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
        write_to_csv(generaldataCSV, [index, pokeName, pokeFullName, pokeTypeA, pokeTypeB, pokeCatch, pokeFlee, pokeFastMoves, pokeChargeMoves])
    

def write_to_csv(fileName,list_input):
    try:
        with open(fileName, 'a', newline='') as fopen:  # Open the csv.
            csv_writer = csv.writer(fopen)
            csv_writer.writerow(list_input)
    except:
        return False

def reset_csv(fileName):
    try:
        tobeDeleted = open(fileName, 'r+')
        tobeDeleted.truncate(0) # need '0' when using r+

    except:
        return False


def move_combinations():
    pokedexEntries = requests.get('https://pokemondb.net/go/pokedex')
    pokedexSoup = BeautifulSoup(pokedexEntries.content, 'html.parser', from_encoding='utf8')
    pokeTable = pokedexSoup.find("main", class_ = "main-content grid-container")
    pokeChunks = pokeTable.find_all("tr")

    write_to_csv(movecombosCSV, ['ID','Name','Full Name','Fast Move','Charge Move'])
    index = 0

    for pokemon in pokeChunks:
        # Get Pokemon Names
        pokeFind = pokemon.find("a", class_ = "ent-name")
        if pokeFind is not None:
            pokeName = pokeFind.text
            pokeFullName = pokeName
        else:
            continue
        pokeAltNameSearch = pokemon.find("small", class_ = "text-muted")
        # Account for alternative versions of the same Pokemon, same of them can have different move options
        if pokeAltNameSearch is not None:
            pokeAltName = pokeAltNameSearch.text
            pokeFullName = pokeName + " (" + pokeAltName + ")"


        pokeMoveList = pokemon.find_all("td", class_ = "text-small")
        if len(pokeMoveList) > 0:
            pokeFastMoves = str(pokeMoveList[0])
            pokeChargeMoves = str(pokeMoveList[1])
            # Cleaning extractions
            if re.match(tdPattern, pokeFastMoves):
                pokeFastMoves = re.sub(tdPattern, "", pokeFastMoves)
                pokeFastMoves = re.sub(spanPattern, "", pokeFastMoves)
                pokeFastMoves = re.sub(parenPattern, "", pokeFastMoves).strip()
            if re.match(tdPattern, pokeChargeMoves):
                pokeChargeMoves = re.sub(tdPattern, "", pokeChargeMoves)
                pokeChargeMoves = re.sub(spanPattern, "", pokeChargeMoves)
                pokeChargeMoves = re.sub(parenPattern, "", pokeChargeMoves).strip()
            pokeFastMoveList = pokeFastMoves.split("<br/>")[:-1]
            pokeChargeMoveList = pokeChargeMoves.split("<br/>")[:-1]

        if pokeFastMoveList is not None and pokeChargeMoveList is not None:
            for fastMove in pokeFastMoveList:
                for chargeMove in pokeChargeMoveList:
                    index += 1
                    if fastMove is not None and chargeMove is not None:
                        write_to_csv(movecombosCSV, [index, pokeName, pokeFullName, fastMove, chargeMove])
        else:
            continue

reset_csv(movecombosCSV)
move_combinations()