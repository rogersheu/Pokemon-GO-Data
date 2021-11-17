from bs4 import BeautifulSoup
import requests
import csv
import re
from csv_functions import write_to_csv
from csv_functions import reset_csv

tdPattern = re.compile(r"</?td[^<>]*>")
spanPattern = re.compile(r'(<span class=\"text-muted\">|</span>)')
parenPattern = re.compile(r'\s\((legacy|Shadow|Community Day)\)')
#spanPattern = re.compile(r"</?span[^<>]*>")
#parenPattern = re.compile(r"\s\(.*\)")

movecombosCSV = "pokeData/Pokemon Move Combinations.csv"

def move_combinations():
    pokedexEntries = requests.get('https://pokemondb.net/go/pokedex')
    pokedexSoup = BeautifulSoup(pokedexEntries.content, 'html.parser', from_encoding='utf8')
    pokeTable = pokedexSoup.find("main", class_ = "main-content grid-container")
    pokeChunks = pokeTable.find_all("tr")

    write_to_csv(movecombosCSV, ['ID','Name','Full Name','Type 1','Type 2','Fast Move','Charge Move'])
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

        # Get pokemon element for strengths/weaknesses; important for STAB (same type ability bonus)
        pokeTypeList = pokemon.find_all("a", class_ = "type-icon")
        if len(pokeTypeList) > 0:
            pokeType1 = pokeTypeList[0].text
            if len(pokeTypeList) == 2:
                pokeType2 = pokeTypeList[1].text
        else:
            continue

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
                        write_to_csv(movecombosCSV, [index, pokeName, pokeFullName, pokeType1, pokeType2, fastMove, chargeMove])
        else:
            continue


reset_csv(movecombosCSV)
move_combinations()