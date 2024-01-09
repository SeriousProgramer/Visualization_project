import pandas as pd

#replace <path on you computer to file, e.g. C:\....> with the path to the file 
df = pd.read_csv(
    "C:\\Users\\20221498\\Downloads\\all_data.csv", delimiter=";", on_bad_lines="skip"
)
print(df)

def cell_value():
    return df.iat[0,0]

print(cell_value())
print(df.columns)
df.head()
# Get the counts of each unique value in the 'Customer_ID' column
# Write the first few rows of the DataFrame to an Excel file at a specific location
df.head().to_excel('C:\\Users\\20221498\\Documents\\first.xlsx', index=False)