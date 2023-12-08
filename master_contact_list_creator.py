# Dependencies
import pandas as pd
import numpy as np
from datetime import date

# Open CSVs
print('--Opening deployment_users.csv--')
try:
    df_users = pd.read_csv('deployment_users.csv')
    print(df_users.head())
    print('--Successful--')
except:
    print('ERROR: File not found')

print('--Opening affiliations.csv--')
try:
    df_contacts = pd.read_csv('affiliations.csv')
    print(df_contacts.head())
    print('--Successful--')
except:
    print('ERROR: File not found')

# Normalize columns between both dataframes
print('--Normalizing columns between both files--')

print('-- Adding contacts columns to users--')
for (column) in df_contacts:
    print(f'Reviewing {column}')
    if column in df_users.columns:
        print(f'- Already present')
        continue
    else:
        print(f'- Not present.  Adding it')
        df_users[column] = 0
print('--Complete--')

print('-- Adding users columns to contacts--')
for (column) in df_users:
    print(f'Reviewing {column}')
    if column in df_contacts.columns:
        print(f'- Already present')
        continue
    else:
        print(f'- Not present.  Adding it')
        df_contacts[column] = 0
print('--Complete--')

# Fill empty fields that aren't the email address
print(f'--Replacing empty values in df_contacts--')
for (column) in df_contacts:
    if column == 'email':
        print(f'Skipping {column}')
        continue
    else:
        print(f'Replacing NULL values in: {column}')
        df_contacts[column].fillna(0, inplace=True)
print(f'--Complete--')
print(df_contacts.head())

print(f'--Replacing empty values in df_users--')
for (column) in df_users:
    if column == 'email':
        print(f'Skipping {column}')
        continue
    else:
        print(f'Replacing NULL values in: {column}')
        df_users[column].fillna(0, inplace=True)
print(f'--Complete--')
print(df_users.head())

# Drop empty rows
print(f'--Dropping empty rows from df_users--')
print(f'Original rows: {len(df_users)}')
df_users.dropna(inplace=True)
print(f'After dropping: {len(df_users)}')
print(f'--Complete--')

print(f'--Dropping empty rows from df_contacts--')
print(f'Original rows: {len(df_contacts)}')
df_contacts.dropna(inplace=True)
print(f'After dropping: {len(df_contacts)}')
print(f'--Complete--')

# Combine dataframes
df_combined = pd.DataFrame()

for (column) in df_contacts:
    combined_list = df_contacts[column].tolist()
    combined_list.extend(df_users[column].tolist())
    df_combined[column] = combined_list

# Sort the df by the email address for easier duplicate comparison
df_combined.sort_values(by=['email'], inplace=True)

# Export the df to CSV
today = date.today().strftime("%Y-%B-%d")
filename = f'master_contact_list_{today}.csv'
df_combined.to_csv(filename, index=False)
print(f'Cleaned and combined data exported to {filename}')
