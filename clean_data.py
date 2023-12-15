import pandas as pd
import numpy as np
import re

# Three important notes for future debuggers:
# Cleaning is fairly heavy-handed, I might be removing extreme values

ssn_pattern = re.compile('^\d{3}-\d{2}-\d{4}$')

# Returns whether a value is acceptable or should be replaced
def isValidItem(value, column):
    if(column == 'Name'):
        # Occasionally is NaN, sometimes there's a psuedonym but that's pretty hard to tell
        return isinstance(value, str) and (value is not None)
    elif(column == 'Age'):
        # Occasionally NaN
        return (isinstance(value, int) and (value is not None)) and (0 <= value and value <= 140)
    elif(column == 'Occupation'):
        # Strange error values here, occasionally has a bunch of underscores instead of a name
        return isinstance(value, str) and value != None and value != "_______"
    elif(column == 'SSN'):
        # Occasionally NaN
        return isinstance(value, str) and (value is not None) and bool(ssn_pattern.match(value))
    elif(column == 'Num_of_Loan'):
        # Occasionally NaN, occasionally there's also unrealistic numbers (negative or > 100)
        return (isinstance(value, int) and (value is not None)) and (0 <= value and value <= 100)
    elif(column == 'Monthly_Inhand_Salary'):
        # Occasionally NaN
        return (isinstance(value, float) and (value is not None)) 
    elif(column == 'Payment_Behaviour'):
        # Occasionally NaN
        return (isinstance(value, float) and (value is not None)) 
    elif(column == 'Interest_Rate'):
        # Occasionally there's unrealistic numbers that change month-to-month (negative or > 1000)
        # WARNING: I'm not 100% sure these values are erroneous
        return (isinstance(value, int) and (value is not None)) and (0 <= value and value <= 1000)
    elif(column == 'Type_of_Loan'):
        # Occasionally NaN, often can't be filled in either but we try
        return (isinstance(value, str) and (value is not None))
    elif(column == 'Num_of_Delayed_Payment'):
        # Occasionally there's unrealistic negative numbers
        return (isinstance(value, int) and (value is not None)) and (0 <= value and value < 100)
    elif(column == 'Delay_from_due_date'):
        # Occasionally there's unrealistic negative numbers
        return (isinstance(value, int) and (value is not None))
    elif(column == 'Changed_Credit_Limit'):
        # Occasionally there's underscores
        return (isinstance(value, float) and (value is not None) and value != "_")
    elif(column == 'Num_Credit_Inquiries'):
        # Occasionally has unrealistic values
        return (isinstance(value, int) and (value is not None) and (0 <= value and value <= 1000))
    elif(column == 'Credit_Mix'):
        # Occasionally there's underscores
        return (isinstance(value, str) and (value is not None) and value != "_")
    elif(column == 'Credit_History_Age'):
        # Occasionally there's underscores
        return (isinstance(value, str) and (value is not None))
    elif(column == 'Payment_of_Min_Amount'):
        # Occasionally there's 'Not mentioned' values
        return (isinstance(value, str) and (value is not None) and value != "NM")
    else:
        return True

# BUG: Only fills in null values, not invalid ones like it should
def fill_based_on_group(row, column):
    group = row['Customer_ID']
    current_index = row.name

    if isValidItem(row[column], column):
        # If the specified column is valid, return the value unchanged
        return row[column]

    # Find the next and last valid indices in the same group
    next_valid_index = df.loc[(df['Customer_ID'] == group) & (df.index > current_index) & (df[column].notna()), column].first_valid_index()
    last_valid_index = df.loc[(df['Customer_ID'] == group) & (df.index < current_index) & (df[column].notna()), column].last_valid_index()

    if isValidItem(next_valid_index, column):
        # If the next valid value in the same group is available, fill with forward fill
        return df.loc[next_valid_index, column]
    elif isValidItem(last_valid_index, column):
        # If the last valid value in the same group is available, fill with backward fill
        return df.loc[last_valid_index, column]
    elif pd.notna(next_valid_index):
        # If the next valid value in the same group is not null, fill with forward fill
        return df.loc[next_valid_index, column]
    elif pd.notna(last_valid_index):
        # If the last valid value in the same group is not null, fill with backward fill
        return df.loc[last_valid_index, column]
    else:
        # If both the specified column and group-specific values are missing, return NaN
        return pd.NA

# Simple as, turns something that should be convertable into a number, into a number
def turn_into_num(row, column):
    if row[column] != None:
        return float(str(row[column]).strip("_").replace(",", "."))
    return row[column]

# List of columns to attempt to fill missing values
columns_to_fill = ['Name', 'Age', 'SSN', 'Occupation', 'Num_of_Loan', 'Interest_Rate',
                   'Monthly_Inhand_Salary', 'Payment_Behaviour', 'Type_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment',
                   'Changed_Credit_Limit', 'Num_Credit_Inquiries', 'Credit_Mix', 'Credit_History_Age', 'Payment_of_Min_Amount', 'Credit_Score']

# List of columns to attempt to clean erroneous data
columns_to_clean = ['Age', 'Annual_Income', 'Monthly_Balance', 'Num_of_Loan', 'Total_EMI_per_month', 'Amount_invested_monthly',
                    'Num_of_Delayed_Payment', 'Outstanding_Debt']

fill_depth = 2

# Returns a random selection of range number of customers from the given data frame
# NOT DONE
def getCleanedInRange(df, r):
    selected_df = df.head(r) # This is where we pick a random selection of names
    
    cleaned = df.head(r).copy()

    # Loop over columns and apply custom functions
    for x in range(fill_depth):
        for column in columns_to_fill:
            cleaned[column] = cleaned.apply(fill_based_on_group, axis=1, column=column)

    for column in columns_to_clean:
        cleaned[column] = cleaned.apply(turn_into_num, axis=1, column=column)
    
    #print sample
    print('\nBefore: \n')
    print(selected_df[selected].head(r))
    print('\nAfter: \n')
    print(cleaned[selected].head(r))
    
    return cleaned



df = pd.read_csv("C:\\Users\\20221051\\Downloads\\all_data.csv", delimiter=';', on_bad_lines='skip')

#answer = input("Enter the number of names to clean")

selected = ['Name', 'Credit_Score']

print(df.columns)

cleaned = getCleanedInRange(df, 50)


