import csv

def strip_whitespace(row):
            return [cell.strip() for cell in row]

with open('/workspaces/machine-learning-projects/csvcleaner/sampledata/dirty.csv', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        print(strip_whitespace(row))
        

        

