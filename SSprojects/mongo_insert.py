import pandas as pd
import glob
import os
from pymongo import MongoClient

path = r"Marchweek4/StirShaken_Samples"

# Get a list of all CSV files in the directory
all_files = glob.glob(os.path.join(path, "*.csv"))

# Create an empty list to store the DataFrames
dfs = []

# Read each CSV file, add a 'source_file' column, and append it to the list
for file in all_files:
    df = pd.read_csv(file)
    df['source_file'] = os.path.basename(file)
    dfs.append(df)

# Concatenate all the DataFrames into a single DataFrame
df= pd.concat(dfs, ignore_index=True)

data = df.to_dict(orient='records')


client = MongoClient('localhost', 27017)  # Connect to MongoDB server
db = client['dbanalytics_test']  # Choose the database
collection = db['StirShakengroups_noc']  # Choose the collection
collection.insert_many(data)


