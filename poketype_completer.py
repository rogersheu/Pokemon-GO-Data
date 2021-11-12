import csv

fullTypeCSV = "fulltypes.csv"


def typecompleter():

    types = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dark", "Dragon", "Steel", "Fairy"]

    truncTypes = []
    for i in types:
        truncTypes.append(i[0:3]) #not sure why it won't let me use list comprehension instead, tried truncTypes = [oneType[:3] for oneType in types]
    
    tobeDeleted = open(fullTypeCSV, 'r+')
    tobeDeleted.truncate(0) # need '0' when using r+

    with open("types_pretransform.csv", newline='') as csvfile:
        typeCSV = csv.reader(csvfile, delimiter = ',')
        typeList = list(typeCSV)
        completedTypes = []
        for currType in typeList:
            for onlyType in currType:
                completedTypes.append(truncTypes.index(onlyType))
                write_to_csv([types[truncTypes.index(onlyType)]])

    

def write_to_csv(list_input):
    try:
        with open(fullTypeCSV, 'a', newline='') as fopen:  # Open the csv.
            csv_writer = csv.writer(fopen)
            csv_writer.writerow(list_input)
    except:
        return False


typecompleter()