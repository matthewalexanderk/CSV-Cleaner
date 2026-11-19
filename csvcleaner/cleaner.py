import csv

def strip_whitespace(rows):
    return [[item.strip() for item in cell] for cell in rows]
            

def pad_rows(rows):

    longest_cell = 0
    for cell in rows:
        length = len(cell)
        if length >= longest_cell:
                longest_cell = length
    for cell in rows:
        rows_needed = longest_cell - len(cell)
        cell.extend([""]*rows_needed)
    return rows
             
def fill_missing(rows):
    for cell in rows:
        for index, item in enumerate(cell):
            if item in ['', ' ']:
                cell[index] = 'N/A'
    return rows

def remove_duplicates(rows):
    unique_rows = []
    for row in rows:
        if row not in unique_rows:
            unique_rows.append(row)
    return unique_rows

    
            

with open('/workspaces/machine-learning-projects/csvcleaner/sampledata/dirty.csv', newline='') as file:
    reader = csv.reader(file)
    rows = list(reader)
print(rows)
rows = strip_whitespace(rows)
rows = pad_rows(rows)
rows = fill_missing(rows)
rows = remove_duplicates(rows)
print(rows)

with open('/workspaces/machine-learning-projects/csvcleaner/sampledata/clean.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

        

