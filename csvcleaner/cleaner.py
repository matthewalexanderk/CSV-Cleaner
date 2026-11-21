import csv
import argparse

def strip_whitespace(rows):
    # looks at the first cell of each row and removes any leading or trailing whitespace from the cell
    # flow is this: you get a row from the csv file, then you get the first cell of that row, then you strip the whitespace from that cell, then you return the row with the stripped cell
    return [[item.strip() for item in cell] for cell in rows]
            

def pad_rows(rows):
    
    # looks at the first cell of each row and pads the row with empty strings until it is the same length as the longest row
    
    longest_cell = 0
    for cell in rows:
        length = len(cell)
        if length >= longest_cell:
                longest_cell = length
    for cell in rows:
        rows_needed = longest_cell - len(cell)
        cell.extend([""]*rows_needed)
    return rows
             
def fill_missing(rows, placeholder='N/A'):
    missing_values = {
        '', 'none', 'null', 'nan', 'undefined', 'nil', 'n/a',
        'unknown', 'missing'
    }
    for row in rows:
        for index, item in enumerate(row):
            if item is None:
                row[index] = placeholder
            elif str(item).strip().lower() in missing_values:
                row[index] = placeholder
    return rows

def remove_duplicates(rows):
    unique_rows = []
    for row in rows:
        if row not in unique_rows:
            unique_rows.append(row)
    return unique_rows

    
            
parser = argparse.ArgumentParser(description='Enter the path to your CSV file')
parser.add_argument('input_file', help='Path to the input CSV file')
parser.add_argument('output_file', help='Path to the output CSV file')
args = parser.parse_args()
with open(args.input_file.strip(), newline='') as file:
    reader = csv.reader(file)
    rows = list(reader)
choice = input("Do you want to strip whitespaces from the cells? (y/n): ")
if choice.lower() in ['y', 'yes']:
    rows = strip_whitespace(rows)
choice = input("Do you want pad rows to the same length as the longest row? (y/n): ")
if choice.lower() in ['y', 'yes']:
    rows = pad_rows(rows)
choice = input("Do you want to fill missing values with a placeholder? (y/n): ")
if choice.lower() in ['y', 'yes']:
    placeholder = input("Enter the placeholder value (default is 'N/A'): ")
    if placeholder.strip() == '':
        placeholder = 'N/A'
    rows = fill_missing(rows, placeholder)
choice = input("Do you want to remove duplicate rows? (y/n): ")
if choice.lower() in ['y', 'yes']:
    rows = remove_duplicates(rows)

with open(args.output_file.strip(), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print(f"Cleaned CSV file has {len(rows)} rows and has been saved to {args.output_file.strip()}")

        

