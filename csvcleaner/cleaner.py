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

def remove_duplicates(rows, ignore_first_col=False):
    unique_rows = []
    seen = []

    for row in rows:
        fingerprint = row[1:] if ignore_first_col else row
        if fingerprint not in seen:
            seen.append(fingerprint)
            unique_rows.append(row)
    return unique_rows

parser = argparse.ArgumentParser(description='Enter the path to your CSV file')
parser.add_argument('input_file', help='Path to the input CSV file')
parser.add_argument('output_file', help='Path to the output CSV file')
args = parser.parse_args()

with open(args.input_file.strip(), newline='') as file:
    reader = csv.reader(file)
    rows = list(reader)

choice = input("Does your CSV file have a header row? (y/n): ")
if choice.lower() in ['y', 'yes']:
    header = rows[0]
    header = strip_whitespace([header])[0]  # Strip whitespace from header
    data = rows[1:]
else:
    data = rows
    header = None
    print("No header row detected. Proceeding without a header.")

choice = input("Do you want to strip whitespaces from the cells? (y/n): ")
if choice.lower() in ['y', 'yes']:
    data = strip_whitespace(data)
else:
    print("Skipping whitespace stripping.")

should_pad = False
choice = input("Do you want pad rows to the same length as the longest row? (y/n): ")
if choice.lower() in ['y', 'yes']:
    data = pad_rows(data)
    should_pad = True
else: 
    print("Skipping row padding.")

choice = input("Do you want to fill missing values with a placeholder? (y/n): ")
if choice.lower() in ['y', 'yes']:
    placeholder = input("Enter the placeholder value (default is 'N/A'): ")
    if placeholder.strip() == '':
        placeholder = 'N/A'
    data = fill_missing(data, placeholder)
else:
    print("Skipping missing value filling.")

choice = input("Do you want to remove duplicate rows? (y/n): ")
if choice.lower() in ['y', 'yes']:
    ignore_first_col = input("Do you want to ignore the first column when checking for duplicates? (y/n): ")
    ignore_first_col = ignore_first_col.lower() in ['y', 'yes']
    if ignore_first_col:
        print("Duplicates will be removed based on all columns except the first one.")
        data = remove_duplicates(data, ignore_first_col=True)
    else:
        print("Duplicates will be removed based on all columns.")
        data = remove_duplicates(data)
else:
    print("Skipping duplicate row removal.")

rows = [header] + data if header else data
if should_pad:
    rows = pad_rows(rows)

with open(args.output_file.strip(), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print(f"Cleaned CSV file has {len(rows)} rows and has been saved to {args.output_file.strip()}")

        

