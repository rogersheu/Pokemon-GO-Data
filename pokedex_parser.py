from bs4 import BeautifulSoup
import requests
import csv
import re

tdPattern = re.compile(r"</?td[^<>]*>")
spanPattern = re.compile(r"</?span[^<>]*>")
parenPattern = re.compile(r"\(.*\)")

csvName = "Pokemon Stats.csv"

def pokeScraper():
    pokedexEntries = requests.get('https://pokemondb.net/go/pokedex')
    pokedexSoup = BeautifulSoup(pokedexEntries.content, 'html.parser', from_encoding='utf8')
    pokeTable = pokedexSoup.find("main", class_ = "main-content grid-container")
    pokeChunks = pokeTable.find_all("tr")

    write_to_csv(['Name','FullName','Type','Catch','Flee','Fast Moves','Charge Moves'])

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
            pokeTypes = ";".join(pokeTypeList[i].text for i in range(len(pokeTypeList)))
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
            pokeFastMoves = str(pokeMoveList[0]) # Find a way to convert this to a string
            pokeChargeMoves = str(pokeMoveList[1])
            pokeFastMoves = pokeFastMoves.replace("<br/>", ";")
            pokeChargeMoves = pokeChargeMoves.replace("<br/>", ";")
            if re.match(tdPattern, pokeFastMoves):
                pokeFastMoves = re.sub(tdPattern, "", pokeFastMoves)
                pokeFastMoves = re.sub(spanPattern, "", pokeFastMoves)
                pokeFastMoves = re.sub(parenPattern, "", pokeFastMoves)
            if re.match(tdPattern, pokeChargeMoves):
                pokeChargeMoves = re.sub(tdPattern, "", pokeChargeMoves)
                pokeChargeMoves = re.sub(spanPattern, "", pokeChargeMoves)
                pokeChargeMoves = re.sub(parenPattern, "", pokeChargeMoves)
        else:
            continue
        
        write_to_csv([pokeName, pokeFullName, pokeTypes, pokeCatch, pokeFlee, pokeFastMoves, pokeChargeMoves])
    

def write_to_csv(list_input):
    try:
        with open(csvName, 'a', newline='') as fopen:  # Open the csv.
            csv_writer = csv.writer(fopen)
            csv_writer.writerow(list_input)
    except:
        return False

def reset_csv():
    try:
        tobeDeleted = open(csvName, 'r+')
        tobeDeleted.truncate(0) # need '0' when using r+

    except:
        return False

reset_csv()
pokeScraper()