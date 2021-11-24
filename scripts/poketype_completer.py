# Turns three letter abbreviated types into their full word format

# Could have been done with a dictionary. See team_mapping in rogersheu/All-Star-Predictions.

from csv_functions import reset_csv, write_to_csv
import csv

fileName = "fulltypes.csv"


def typecompleter():

    types = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", 
             "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", 
             "Dark", "Dragon", "Steel", "Fairy"]

    truncTypes = []
    for i in types:
        truncTypes.append(i[0:3]) #not sure why it won't let me use list comprehension instead, tried truncTypes = [oneType[:3] for oneType in types]
    
    reset_csv(fileName)
    with open("types_pretransform.csv", newline='') as csvfile:
        typeCSV = csv.reader(csvfile, delimiter = ',')
        typeList = list(typeCSV)
        completedTypes = []
        for currType in typeList:
            for onlyType in currType:
                completedTypes.append(truncTypes.index(onlyType))
                write_to_csv(fileName, [types[truncTypes.index(onlyType)]])


typecompleter()