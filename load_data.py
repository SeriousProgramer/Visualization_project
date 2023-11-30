import pandas as pd
import numpy as np

# replace <path on you computer to file, e.g. C:\....> with the path to the file
df = pd.read_csv(
    "C:\\Users\\20221498\\Desktop\\Visualization\\all_data.csv",
    delimiter=";",
    on_bad_lines="skip",
)
print(df)


def cell_value():
    return df.iat[0, 0]


print(cell_value())
print(df.columns)


def count_freq_and_describe():
    for column in df.columns:
        print(df[column].value_counts())
        print(df[column].describe())


def findMissing():
    for column in df.columns:
        print(df[column].isna().sum() + column)

def is_valid_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def wrongAge():
    for i in df['Age']:
        if not is_valid_int(i) or int(i) < 10 or int(i) > 100:
            print(i)
# wrongAge()

def badName():
    for i in df['Name']:
        if not i.isalpha():
            print(i)
            
def count_consecutive_nans():
    # Create a boolean series where True represents NaN values
    is_nan = df['Name'].isna()

    # Initialize count of four consecutive NaNs
    count = 0

    # Iterate over the boolean series with a sliding window of size 4
    for i in range(len(is_nan) - 3):
        # If all four values in the window are True (NaN), increment the count
        if is_nan[i] and is_nan[i+1] and is_nan[i+2] and is_nan[i+3]:
            count += 1

    print(f'Number of times four consecutive NaN values occur: {count}')

# count_consecutive_nans()
print(df['Credit_Score'].isna().sum())
