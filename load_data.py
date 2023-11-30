import pandas as pd

#replace <path on you computer to file, e.g. C:\....> with the path to the file 
df = pd.read_csv("C:\\Users\\20221051\\Downloads\\all_data.csv",delimiter=';', on_bad_lines='skip')
print(df)

def cell_value():
    return df.iat[0,0]

print(cell_value())
print(df.columns)
df.head()