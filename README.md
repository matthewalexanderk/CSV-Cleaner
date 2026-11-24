# CSV Cleaner
CSV cleaner takes a CSV file and optionally: 
- removes whitespaces
- pads rows
- fills missing values
- removes duplicate rows
    - users can define composite keys by column name or index to remove duplicate entries

## How to run CSV Cleaner within the CLI
```python3 cleaner.py path/to/input.csv path/to/output.csv```

### To get help
```python3 cleaner.py --help```
