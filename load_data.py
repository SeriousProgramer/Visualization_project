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
        print(df[column].isna().sum())


findMissing()
