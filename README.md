# Budget Creation Script README

## Overview

This script automates the creation of AWS budgets based on a CSV file input. It allows you to specify multiple linked accounts and planned budget amounts for each month. The budgets are created in the main payer account but are filtered to only apply to the specified linked accounts.

## Requirements

- Python 3.x
- AWS CLI configured with the necessary permissions

## CSV File Format

The CSV file should have the following format:
```
Budget_Name,Accounts,1722470400,1725148800,1727740800,1730419200,1733011200,1735689600,1738368000,1740787200,1743465600,1746057600,1748736000,1751328000
"Example Budget 1","123456789012,234567890123",100,200,300,400,500,600,700,800,900,1000,1100,1200
"Example Budget 2","345678901234,456789012345",150,250,350,450,550,650,750,850,950,1050,1150,1250
```


### CSV Columns

- **Budget_Name**: The name of the budget. Account names cannot exceed 100 characters.
- **Accounts**: A comma-separated list of account numbers (12 digits each).
- **Epoch Time Columns**: Unix timestamps representing the first of each month for which the budget is planned. The amounts are specified in USD.  If you don't know what Unix epoch timestamps are, please read up: https://www.epochconverter.com/

## Instructions

1. **Install Python and AWS CLI**:
    - Ensure you have Python 3.x installed on your system.
    - Install and configure AWS CLI with the necessary permissions to create budgets.

2. **Prepare the CSV File**:
    - Create a CSV file following the format described above.
    - Ensure account names do not exceed 100 characters.
    - Ensure account numbers are exactly 12 digits.
    - Remove any extra lines at the end of the CSV to avoid errors.

3. **Place the Script and CSV in the Same Directory**:
    - Ensure the CSV file and the Python script (`create_budget.py`) are in the same directory.

4. **Run the Script**:
    - Open a terminal and navigate to the directory containing the script and CSV file.
    - Execute the script using Python:
      ```bash
      python3 create_budget.py
      ```

## Error Handling

### Common Errors

- **DuplicateRecordException**: This error occurs if a budget with the same name already exists. Modify the budget name in the CSV to create a new budget.
- **Parameter validation failed**: This error can occur if:
  - The budget name is empty or exceeds 100 characters.
  - The account numbers are not *exactly* 12 digits.
  - Extra lines are present in the CSV file. Remove any extra lines to avoid this error.

### Example Error Message
Parameter validation failed:
Invalid length for parameter Budget.BudgetName, value: 0, valid min length: 1

This indicates that an empty budget name was encountered, possibly due to extra lines in the CSV file.

## Conclusion

This script simplifies the process of creating AWS budgets for multiple linked accounts. By leveraging a CSV file, you can easily manage and update budget configurations. Make sure to follow the instructions carefully and validate your CSV file to avoid common errors.

