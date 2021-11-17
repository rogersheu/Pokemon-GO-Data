import csv
import math
from csv_functions import write_to_csv
from csv_functions import reset_csv

moveCombinationCSV = "pokeData/Pokemon Move Combinations.csv"
moveStats = "pokeData/Pokemon Move Stats.csv"

def dps_calculation():
    write_to_csv(moveStats, ['ID','Name','Full Name','Type 1','Type 2','Fast Move','Fast Move Type',
        'Fast Move Power','Turns','Energy Generated','Charge Move','Charge Move Type','Charge Move Power','Energy Spent','Charge Time','Fast DPS','Charge DPS','Total DPS'])

    with open(moveCombinationCSV,'r',newline='') as currFile:
        pokemonMoveCombinations = csv.reader(currFile)
        next(pokemonMoveCombinations, None)
        for uniquePokemon in pokemonMoveCombinations:
            try: 
                pokeID = uniquePokemon[0]
                pokeName = uniquePokemon[1]
                pokeFullName = uniquePokemon[2]
                pokeType1 = uniquePokemon[3]
                pokeType2 = uniquePokemon[4]
                currFastMove = uniquePokemon[5]
                currChargeMove = uniquePokemon[6]
                with open("pokeData/fastmoves.csv",'r',newline='') as fastmovesFile:
                    fastmoveReader = csv.reader(fastmovesFile)
                    for fastMove in fastmoveReader:
                        if currFastMove == fastMove[0]:
                            fastMoveType = fastMove[1]
                            fastPower = fastMove[2]
                            fastTurns = fastMove[3]
                            fastEnergy = fastMove[4]
                            break
                with open("pokeData/chargemoves.csv",'r',newline='') as chargemovesFile:
                    chargemoveReader = csv.reader(chargemovesFile)
                    for chargeMove in chargemoveReader:
                        if currChargeMove == chargeMove[0]:
                            chargeMoveType = chargeMove[1]
                            chargePower = chargeMove[2]
                            chargeEnergy = -1 * int(chargeMove[3])
                            chargeEnergy = str(chargeEnergy)
                            break
                with open("pokeData/ultraleaguestats.csv",'r',newline='') as basestatsFile:
                    basestatsReader = csv.reader(basestatsFile)
                    next(basestatsReader, None)
                    for pokemon in basestatsReader:
                        if pokeName == pokemon[0]:
                            pokeAttack = pokemon[3]
                            pokeDefense = pokemon[4]
                            pokeStamina = pokemon[5]
                            break
                
                if fastMoveType == (pokeType1 or pokeType2):
                    sametypeattackbonus_fast = 1.2
                else:
                    sametypeattackbonus_fast = 1

                if chargeMoveType == (pokeType1 or pokeType2):
                    sametypeattackbonus_charge = 1.2
                else:
                    sametypeattackbonus_charge = 1

                # Weather attack bonus?
                # Friendship attack bonus?'
                turnTime = int(fastTurns) * 0.5
                fastDPS = round(math.floor(0.5* (int(fastPower) * float(pokeAttack) / 100 * sametypeattackbonus_fast) + 1) / turnTime, 2)
                fastmovesforfullcharge = int(chargeEnergy) / int(fastEnergy)
                chargeTime = math.ceil(fastmovesforfullcharge) * turnTime
                chargeDPS = round(math.floor(0.5* (int(chargePower) * float(pokeAttack) / 100 * sametypeattackbonus_charge) + 1) / (chargeTime),2)

                totalDPS = fastDPS + chargeDPS

                write_to_csv(moveStats, [pokeID, pokeName, pokeFullName, pokeType1, pokeType2, currFastMove, fastMoveType, fastPower, fastTurns,
                    fastEnergy, currChargeMove, chargeMoveType, chargePower, chargeEnergy, chargeTime, fastDPS, chargeDPS, totalDPS])

            except:
                continue

reset_csv(moveStats)
dps_calculation()