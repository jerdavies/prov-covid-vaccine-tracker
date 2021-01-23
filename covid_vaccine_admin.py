import requests
import json
import pandas as pd
from pandas import json_normalize
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

# set parameters
parameters = {"stat": "avaccine",
              "loc": "prov"}

# Make a get request with the parameters.
url = "https://api.opencovid.ca/timeseries"
response = requests.get(url, params=parameters)

# Print the content of the responses (the data the server returns)
# print(response.content)

# Store the API response in a Python object (dictionary).
available_data = response.json()

# Extract the value from the "outer nest" key, "avaccine" (discretionary step).
data = available_data["avaccine"]

# Normalize semi-structured JSON data into a flat table (pandas method).
df_raw = json_normalize(data)

# Inspect raw data
# print(df_raw.head())

# Create new column with date formatted to datetime


def to_datetime(rev_date_str):
    date_str = rev_date_str[-4:] + "-" + \
        rev_date_str[3:5] + "-" + rev_date_str[:2]
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')


date_col = df_raw['date_vaccine_administered'].apply(to_datetime)

# Add new date column to dataframe
df = df_raw
df['date'] = date_col
print(df)

# Add Canada (total by day) rows to df
#!!!

# Save as csv file (just for fun!)
df.to_csv('avaccine.csv')

# Keep only data rows from AB, BC, ON, QC
df_focus = df[(df['province'] == "Alberta") | (df['province'] == "BC") | (
    df['province'] == "Ontario") | (df['province'] == "Quebec")]

# Pivot the dataframe to a wide-form representation
df_focus_wide = df_focus.pivot("date",
                               "province", "cumulative_avaccine")
print(df_focus_wide.head())

# Use plt.subplots() to return a tuple and unpack the tuple into the variable fig and ax
fig, ax = plt.subplots()

# Create timeseries lineplot of administered vaccinations over time by province
sns.lineplot(data=df_focus_wide, ax=ax)

# put the labels at 45deg since they tend to be too long
fig.autofmt_xdate()

# add title and resize
plt.title("# of Vaccines Administered by Province")
fig.set_size_inches(7, 4)

# plot
plt.show()

# save image
fig.savefig("vaccines_by_prov.png")
