import pandas as pd
import numpy as np
import re

ssn_pattern = re.compile('^\d{3}-\d{2}-\d{4}$')

# Returns whether a value is acceptable or should be replaced
def isValidItem(value, column):
    if(column == 'Name'):
        return isinstance(value, str) and value != None
    elif(column == 'Age'):
        return (isinstance(value, int) and value != None) and (0 <= value and value <= 140)
    elif(column == 'Occupation'):
       return isinstance(value, str) and value != None and value != "_______"
    elif(column == 'SSN'):
       return isinstance(value, str) and value != None and bool(ssn_pattern.match(value))
    elif(column == 'Num_of_Loan'):
        return (isinstance(value, int) and value != None) and (0 <= value and value <= 50)
    elif(column == 'Monthly_Inhand_Salary'):
        return (isinstance(value, float) and value != None) 
    elif(column == 'Payment_Behaviour'):
        return (isinstance(value, float) and value != None) 
    else:
        return True

def fill_based_on_group(row, column):
    group = row['Customer_ID']
    next_value_in_group = df.loc[(df['Customer_ID'] == group) & (df.index > row.name), column].first_valid_index()
    last_value_in_group = df.loc[(df['Customer_ID'] == group) & (df.index < row.name), column].last_valid_index()

    if isValidItem(pd.notna(row[column]), column):
        # If the specified column is not missing, return the value unchanged
        return row[column]
    elif pd.notna(next_value_in_group):
        # If the specified column is missing but the next value in the same group is available, fill with forward fill
        return df[column].ffill().loc[next_value_in_group]
    elif pd.notna(last_value_in_group):
        # If the specified column is missing but the last value in the same group is available, fill with backward fill
        return df[column].bfill().loc[last_value_in_group]
    else:
        # If both the specified column and group-specific values are missing, return NaN
        return pd.NA

def turn_into_num(row, column):
    if(column == 'Age'):
        return int(row[column].strip("_").replace(",", "."))
    else:
        return float(str(row[column]).strip("_").replace(",", "."))
    
df = pd.read_csv("C:\\Users\\20221051\\Downloads\\all_data.csv",delimiter=';', on_bad_lines='skip')

test_df = df.head(50)

# List of columns to attempt to fill missing values
columns_to_fill = ['Name', 'Age', 'SSN', 'Occupation', 'Num_of_Loan', 'Monthly_Inhand_Salary', 'Payment_Behaviour']

# List of columns to attempt to clean erroneous data
columns_to_clean = ['Age', 'Annual_Income', 'Monthly_Balance', 'Total_EMI_per_month', 'Amount_invested_monthly']

# Loop over columns and apply custom functions

cleaned = test_df.copy()

for column in columns_to_fill:
    cleaned[column] = cleaned.apply(fill_based_on_group, axis=1, column=column)

for column in columns_to_clean:
    cleaned[column] = cleaned.apply(turn_into_num, axis=1, column=column)

print(test_df.head(15))
print(cleaned.head(15))