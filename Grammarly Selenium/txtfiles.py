import os
import pandas as pd
from tqdm import tqdm

df_kickstarter = pd.read_csv('./Hans/Hans/kickstarter.csv')
# Filter rows based on column: 'project_country'
df_kickstarter = df_kickstarter[df_kickstarter['project_country'] == "US"]
# Filter rows based on column: 'project_currency'
df_kickstarter = df_kickstarter[df_kickstarter['project_currency'] == "USD"]
# Drop rows with missing data in column: 'project_title'
df_kickstarter = df_kickstarter.dropna(subset=['project_title'])
# Drop rows with missing data in column: 'project_description'
df_kickstarter = df_kickstarter.dropna(subset=['project_description'])

# Get the total number of rows
total_rows = len(df_kickstarter)

# Create a progress bar
progress_bar = tqdm(total=total_rows, unit='row')

# Specify the folder path to save the text files
output_folder = './txtfiles'  # Replace with the desired folder path
# Iterate over each row
for index, row in df_kickstarter.iterrows():
    # Extract the desired column value
    project_description = row['project_description']  # Replace 'column_name' with the actual column name
    
    # Create the complete file path
    filename = os.path.join(output_folder, f'{index}.txt')
    
    # Save the column value to the text file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(project_description)
    
    progress_bar.update(1)

progress_bar.close()