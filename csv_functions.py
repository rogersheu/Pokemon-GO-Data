import csv

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
