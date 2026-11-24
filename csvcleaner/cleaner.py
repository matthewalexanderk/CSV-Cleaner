"""
CSV Cleaner is an interactive CLI tool that allows users to clean and preprocess CSV files.
"""
import csv
import argparse

def strip_whitespace(rows: list[list[str]]) -> list[list[str]]:
    """Strips whitespaces from each item in a row.

    Args: 
        rows (list[list[str]]): A 2D table of CSV formatted data.
    Returns:
        An updated table with whitespaces stripped.
    """
    return [[item.strip() for item in row] for row in rows]


def pad_rows(rows: list[list[str]]) -> list[list[str]]:
    """Pads rows to the same length as the longest row in the table

    Args:
        rows (list[list[str]]): A 2D table of CSV formatted data.
    Returns:
        An updated table with all rows of the same length as the longest row
    """
    longest_row = 0
    for row in rows:
        length = len(row)
        if length >= longest_row:
            longest_row = length
    for row in rows:
        rows_needed = longest_row - len(row)
        row.extend([""]*rows_needed)
    return rows

             
def fill_missing(rows: list[list[str]], placeholder: str = 'N/A') -> list[list[str]]:
    """Fills rows with missing values with a placeholder.

    Args:
        rows (list[list[str]]): A 2D table of CSV formatted data.
        placeholder (default='N/A'): A place holder for missing values, can be changed to any string.
    Returns:
        rows (list[list[str]]): The new table with missing values filled with the specified placeholder.
    """
    # common values for missing data
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


def remove_duplicates(rows: list[list[str]], key_cols: list[int] | None = None) -> list[list[str]]:
    """Removes row duplicates.

    Args:
        rows (list[list[str]]): A 2D table of CSV formatted data.
        key_cols (list[int] | None):  Column indexes to identify unique rows. If None, all columns are used to identify duplicates.
    Returns:
        list[list[str]]: A new table with duplicates removed.
    """
    unique_rows = []
    seen = set()

    for row in rows:
        fingerprint = tuple(row[i] for i in key_cols) if key_cols else tuple(row)
        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_rows.append(row)
    return unique_rows


def main() -> None:
    """Main function to run the CSV Cleaner CLI tool."""

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
        lower_header = [col.lower() for col in header]
        data = rows[1:]
    else:
        data = rows
        header = None
        lower_header = None
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

        choice = input("Do you want to use column-based or index-based keys to uniquely identify rows? (y/n): ")
        if choice.lower() in ['y', 'yes']:
            key_type = input("Enter 'column' for column-based keys or 'index' for index-based keys: ")
            if key_type.lower() == 'column':
                if not lower_header:
                    print("No header row detected. Cannot use column-based keys. Moving onto index-based keys.")
                else:
                    key_columns = input("Enter the names of the columns separated by commas to create a unique key: ").strip().lower()
                    keys_cols = []
                    valid = True
                    for col in key_columns.split(','):
                        col = col.strip()
                        if col in lower_header:
                            keys_cols.append(lower_header.index(col))
                        else:
                            valid = False
                            print(f"Column '{col}' not found in header. Skipping duplicate removal.")
                            break
                    if valid:
                        data = remove_duplicates(data, key_cols=keys_cols)

            elif key_type.lower() == 'index':
                try:
                    key_index = input("Enter the index of the column separated by commas to use as a key (0-based): ").strip()

                    keys_index = []
                    for key in key_index.split(','):
                        keys_index.append(int(key.strip()))

                    data = remove_duplicates(data, key_cols=keys_index)
                except (ValueError, IndexError):
                    print("One or more invalid indices provided. Skipping duplicate removal.")
            else:
                print("Invalid index.")
        else:
            data = remove_duplicates(data)
            print("Duplicates will be removed based on all columns.")
    else:
        print("Skipping duplicate row removal.")

    rows = [header] + data if header else data
    if should_pad:
        rows = pad_rows(rows)

    with open(args.output_file.strip(), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

    print(f"Cleaned CSV file has {len(rows)} rows and has been saved to {args.output_file.strip()}")

if __name__ == "__main__":
    main()

        

