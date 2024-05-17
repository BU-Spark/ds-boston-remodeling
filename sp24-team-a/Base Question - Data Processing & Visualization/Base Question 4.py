#!/usr/bin/env python
# coding: utf-8

# <font size="5"><strong>Base Question 4

# <font size="3"><strong>Load the Data

# In[2]:


data_url = {
    2004 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/d3be93ad-7939-4425-8b3b-73b69a747fa4/download/data2004-lite.txt',
    2005 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/5bfe4ca0-71c0-4751-bdcf-dad4d58445e0/download/data2005-lite.txt',
    2006 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/327af2fd-e386-4822-8a7f-aaab6d4d2c62/download/data2006lite.txt',
    2007 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/b3862082-216b-4a24-9f31-f47782079c3c/download/data2007-lite.txt',
    2008 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/81f34da8-ec6d-45f6-8d6c-65c57e71023e/download/property-assessment-fy08.csv',
    2009 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/1a374bd0-1ff9-4d1a-8727-ddfc201254fe/download/property-assessment-fy09.csv',
    2010 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/738ece37-5ae0-4f04-bf69-eca3ae1940b2/download/property-assessment-fy10.csv',
    2011 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/110e8ded-d7cd-40d2-a72c-e4f3c7e9c541/download/property-assessment-fy11.csv',
    2012 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/4326ca95-09ec-42e0-8cee-f048e00e6728/download/property-assessment-fy12.csv',
    2013 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/425fd527-e26b-49c9-853c-1c4d3d2bdd97/download/property-assessment-fy13.csv',
    2014 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/7190b0a4-30c4-44c5-911d-c34f60b22181/download/property-assessment-fy2014.csv',
    2015 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/bdb17c2b-e9ab-44e4-a070-bf804a0e1a7f/download/property-assessment-fy2015.csv',
    2016 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/cecdf003-9348-4ddb-94e1-673b63940bb8/download/property-assessment-fy2016.csv',
    2017 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/062fc6fa-b5ff-4270-86cf-202225e40858/download/property-assessment-fy2017.csv',
    2018 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/fd351943-c2c6-4630-992d-3f895360febd/download/ast2018full.csv',
    2019 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/695a8596-5458-442b-a017-7cd72471aade/download/fy19fullpropassess.csv',
    2020 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/8de4e3a0-c1d2-47cb-8202-98b9cbe3bd04/download/data2020-full.csv',
    2021 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/c4b7331e-e213-45a5-adda-052e4dd31d41/download/data2021-full.csv',
    2022 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/4b99718b-d064-471b-9b24-517ae5effecc/download/fy2022pa-4.csv',
    2023 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/1000d81c-5bb5-49e8-a9ab-44cd042f1db2/download/fy2023-property-assessment-data.csv',
    2024 : 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/a9eb19ad-da79-4f7b-9e3b-6b13e66f8285/download/fy2024-property-assessment-data_1_5_2024.csv'
}


# <font size="3"><strong>Data Cleaning/Processing

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt

def load_data_for_year(year, url):
    df = pd.read_csv(url)
    
    #rename the PID column for consistency
    if year == 2014:
        df.rename(columns={'Parcel_ID': 'PID'}, inplace=True)
    
    #eliminate any special character in PID column
    df['PID'] = df['PID'].astype(str)
    df['PID'] = df['PID'].str.replace(r'\D', '', regex=True)
    df['PID'] = df['PID'].astype(int)
    
    #transform LU column to lowercase for consistency
    df['LU'] = df['LU'].str.upper()
    return df

def compare_years(df_year1, df_year2):
    #extract the PID column from two consecutive years
    pid_year1 = set(df_year1['PID'])
    pid_year2 = set(df_year2['PID'])
    
    #compare the PID columns from two years
    lost_units = pid_year1 - pid_year2
    new_units = pid_year2 - pid_year1
    
    return lost_units, new_units

#category of LU column
valid_lu_values = ['A', 'AH', 'C', 'CC', 'CD', 'CL', 'CM', 'CP', 'E', 'EA', 'I', 'R1', 'R2', 'R3', 'R4', 'RC', 'RL']

def group_and_count_by_lu(df, pids):
    #check if any of the column does not have a valid LU format
    df = df[df['LU'].isin(valid_lu_values)]
    filtered_df = df[df['PID'].isin(pids)]
    
    #grouped by the category of LU for graph
    grouped = filtered_df.groupby('LU').size()
    return grouped

def find_and_record_lu_changes(df_year1, df_year2):
    # Filter both dataframes for valid LU values before identifying common PIDs
    df_year1 = df_year1[df_year1['LU'].isin(valid_lu_values)]
    df_year2 = df_year2[df_year2['LU'].isin(valid_lu_values)]
    
    common_pids = set(df_year1['PID']) & set(df_year2['PID'])
    
    # Filter dataframes to only include common PIDs
    df_common_year1 = df_year1[df_year1['PID'].isin(common_pids)]
    df_common_year2 = df_year2[df_year2['PID'].isin(common_pids)]
    
    # Merge the two dataframes on PID to compare LU values
    merged = pd.merge(df_common_year1[['PID', 'LU']], df_common_year2[['PID', 'LU']], on='PID', suffixes=('_BEFORE', ''))
    
    # Identify rows where LU has changed
    changed_lu = merged[merged['LU_BEFORE'] != merged['LU']]
    
    return changed_lu


# <font size="3"><strong>Statistics & Visualization

# **1. "LU" change from 2004-2024**

# In[6]:


import pandas as pd
import matplotlib.pyplot as plt
lost_units_yearly = {}
new_units_yearly = {}

for year, url in data_url.items():  # Exclude the last year for comparison purposes
    #Load data
    if year < 2024:
        df_year1 = load_data_for_year(year, url)
        df_year2 = load_data_for_year(year + 1, data_url[year + 1])
    
        #find out lost units and new units and record the length in dictionaries for graph later
        lost_units, new_units = compare_years(df_year1, df_year2)
        lost_units_yearly[year+1] = len(lost_units)
        new_units_yearly[year+1] = len(new_units)
    
        #group the data for graphs
        lost_units_grouped = group_and_count_by_lu(df_year1, lost_units)
        new_units_grouped = group_and_count_by_lu(df_year2, new_units)
    
        print(f"From {year} to {year + 1}, {len(lost_units)} units were lost\n")
        print(f"From {year} to {year + 1}, {len(new_units)} units were newly built\n")
    
        #Identify all the remaining units that have conflict LU type
        changed_lu = find_and_record_lu_changes(df_year1, df_year2)
    
        if not changed_lu.empty:
            # Group by LU_BEFORE and LU, and count
            changes_grouped = changed_lu.groupby(['LU_BEFORE', 'LU']).size().reset_index(name='Count')
        
            for _, row in changes_grouped.iterrows():
                print(f"From {year} to {year + 1}, {row['Count']} number of {row['LU_BEFORE']} properties were remodeled to {row['LU']}")
        else:
            print(f"No LU changes from {year} to {year + 1}")
    
        # Plotting
        fig, axs = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
        fig.suptitle(f'Land Use Distribution for Lost and New Units: {year}-{year + 1}')
    
        lost_units_grouped.plot(kind='bar', ax=axs[0], color='red')
        axs[0].set_title('Lost Units')
        axs[0].set_xlabel('Land Use Code')
        axs[0].set_ylabel('Number of Units')
    
        new_units_grouped.plot(kind='bar', ax=axs[1], color='green')
        axs[1].set_title('New Units')
        axs[1].set_xlabel('Land Use Code')
    
        plt.show()

# Calculating average units lost per year
average_lost_units = sum(lost_units_yearly.values()) / len(lost_units_yearly)
print(f"Average housing units lost per year: {average_lost_units}")


# **2. Change in Number of Lost/New Units from 2004-2024**

# In[7]:


# Prepare data for plotting
years = list(lost_units_yearly.keys())
lost_units = list(lost_units_yearly.values())
new_units = list(new_units_yearly.values())

# Plotting the change in number of lost units
plt.figure(figsize=(10, 4))
plt.plot(years, lost_units, marker='o', linestyle='-', color='red')
plt.title('Change in Number of Lost Units (2004-2024)')
plt.xlabel('Year')
plt.ylabel('Number of Lost Units')
plt.grid(True)
plt.xticks(years[::2])  # Show every other year for clarity
plt.tight_layout()
plt.show()

# Plotting the change in number of new units
plt.figure(figsize=(10, 4))
plt.plot(years, new_units, marker='o', linestyle='-', color='green')
plt.title('Change in Number of New Units (2004-2024)')
plt.xlabel('Year')
plt.ylabel('Number of New Units')
plt.grid(True)
plt.xticks(years[::2])  # Show every other year for clarity
plt.tight_layout()
plt.show()


# **3. "LU" Type Focus**

# 3.1 Total Number of Units Downgraded for "LU" Type: A, R4, R3, R2, R1 from 2004-2024

# In[10]:


import pandas as pd
import matplotlib.pyplot as plt

#category of LU column
valid_lu_values = ['A', 'R1', 'R2', 'R3', 'R4']
occupancy_order = {'A': 5, 'R4': 4, 'R3': 3, 'R2': 2, 'R1': 1}

def find_downgrades(df_year1, df_year2, occupancy_order):
    # Find common PIDs and their LU values
    common_pids = set(df_year1['PID']) & set(df_year2['PID'])
    df_common_year1 = df_year1[df_year1['PID'].isin(common_pids)][['PID', 'LU']]
    df_common_year2 = df_year2[df_year2['PID'].isin(common_pids)][['PID', 'LU']]

    # Merge on 'PID' to compare LU values
    merged = pd.merge(df_common_year1, df_common_year2, on='PID', suffixes=('_before', '_after'))
    
    # Only consider rows where both LU_before and LU_after are in the occupancy_order dictionary
    valid_merge = merged[(merged['LU_before'].isin(occupancy_order.keys())) & (merged['LU_after'].isin(occupancy_order.keys()))]

    # Calculate changes in LU, considering only downgrades within the specified types
    valid_merge['downgrade'] = valid_merge.apply(lambda row: occupancy_order[row['LU_before']] - occupancy_order[row['LU_after']], axis=1)
    downgrades = valid_merge[valid_merge['downgrade'] > 0]
    return downgrades

# Initialize a dictionary to hold the total number of downgrades per year
total_downgrades_by_year = {year: 0 for year in range(2005, 2024)}

# Initialize a dictionary to hold the downgrades per LU type for each year
downgrades_by_lu_type = {year: {} for year in range(2005, 2024)}

# Process the data for each pair of consecutive years
for year, url in data_url.items():  # Exclude the last year for comparison purposes
    if year < 2024:
        df_year1 = load_data_for_year(year, url)
        df_year2 = load_data_for_year(year + 1, data_url[year + 1])

        downgrades = find_downgrades(df_year1, df_year2, occupancy_order)
        total_downgrades_by_year[year + 1] = len(downgrades)
    
        # Group by the original LU type and count the downgrades
        downgrades_by_lu_type[year + 1] = downgrades.groupby('LU_before').size().to_dict()

# Plot the total number of downgrades per year
plt.figure(figsize=(10, 6))
plt.plot(list(total_downgrades_by_year.keys()), list(total_downgrades_by_year.values()), marker='o', linestyle='-')
plt.title('Total Number of Buildings Downgraded (2005-2023)')
plt.xlabel('Year')
plt.ylabel('Number of Downgrades')
plt.grid(True)
plt.xticks(range(2005, 2024))
plt.show()


# 3.2 Number of downgraded units by "LU" type for every consecutive years

# In[11]:


# Plot downgrades per LU type for each pair of consecutive years
for year, lu_downgrades in downgrades_by_lu_type.items():
    plt.figure(figsize=(10, 6))
    # Ensure lu_downgrades is a dictionary here
    if isinstance(lu_downgrades, dict):
        plt.bar(lu_downgrades.keys(), lu_downgrades.values())
    else:
        # Handle unexpected data types
        print(f"Data for year {year} is not a dictionary.")
    plt.title(f'Building Downgrades from {year-1} to {year}')
    plt.xlabel('Original LU Type')
    plt.ylabel('Number of Downgrades')
    plt.grid(True)
    plt.show()


# 3.3 Total Number of downgraded units by "LU" type from 2004-2024

# In[12]:


# Initialize a dictionary to aggregate downgrades by LU type
total_downgrades_by_lu_type = {}

# Sum up downgrades across all years
for _, lu_downgrades in downgrades_by_lu_type.items():
    if isinstance(lu_downgrades, dict):
        for lu_type, count in lu_downgrades.items():
            if lu_type in total_downgrades_by_lu_type:
                total_downgrades_by_lu_type[lu_type] += count
            else:
                total_downgrades_by_lu_type[lu_type] = count

# Now, plot the total number of downgrades VS. original LU type
plt.figure(figsize=(10, 6))
plt.bar(total_downgrades_by_lu_type.keys(), total_downgrades_by_lu_type.values(), color='skyblue')
plt.title('Total Number of Building Downgrades by Original LU Type (2004-2024)')
plt.xlabel('Original LU Type')
plt.ylabel('Number of Downgrades')
plt.grid(axis='y')
plt.show()


# **4. Community/Neighborhood Focus**

# In[13]:


#Define the "Community/Neighborhood"
neighborhood_zip_codes = {
    "Allston/Brighton": ["02134", "02135", "02163"],
    "Back Bay/Beacon Hill": ["02108", "02116", "02117","02123", "02133", "02199", 
                             "02216", "02217", "02295"],
    "Central Boston": ["02101", "02102", "02103", "02104", "02105", "02106", "02107", 
                       "02109", "02110", "02111", "02112", "02113", "02114", "02196", 
                       "02201", "02202", "02203", "02204", "02205", "02206", "02207", 
                       "02208", "02209", "02211", "02212", "02222", "02293"],
    "Charlestown": ["02129"],
    "Chestnut Hill": ["02467"],
    "Dedham": ["02026"],
    "Dorchester": ["02122", "02124", "02125"],
    "East Boston": ["02128", "02228"],
    "Fenway/Kenmore": ["02115", "02215"],
    "Hyde Park": ["02136"],
    "Jamaica Plain": ["02130"],
    "Mattapan": ["02126"],
    "Newton": ["02458"],
    "Readville": ["02137"],
    "Roslindale": ["02131"],
    "Roxbury": ["02119", "02121"],
    "Roxbury Crossing": ["02120"],
    "South Boston": ["02127", "02210"],
    "South End": ["02118"],
    "West Roxbury": ["02132"]
}

#Need for later visualization
neighborhood_zip_code_combinations = []
for neighborhood, zip_codes in neighborhood_zip_codes.items():
    for zip_code in zip_codes:
        combination = f"{neighborhood} ({zip_code})"
        neighborhood_zip_code_combinations.append(combination)


# In[48]:


def zip_to_neighborhood(zip_code):
    for neighborhood, zips in neighborhood_zip_codes.items():
        if zip_code in zips:
            return neighborhood
    return None

def process_csv(year, url, neighborhood_zip_codes):
    df = pd.read_csv(url)
    
    #rename the PID column for consistency
    if year == 2014:
        df.rename(columns={'Parcel_ID': 'PID'}, inplace=True)
    
    #eliminate any special character in PID column
    df['PID'] = df['PID'].astype(str)
    df['PID'] = df['PID'].str.replace(r'\D', '', regex=True)
    df['PID'] = df['PID'].astype(int)
    
    #transform LU column to lowercase for consistency
    df['LU'] = df['LU'].str.upper()
    
    if year == 2005:
        df['ZIPCODE'] = df['PTYPE']
        
    if year == 2023:
        df['ZIPCODE'] = df['ZIP_CODE']
        
    if year == 2024:
        df['ZIPCODE'] = df['ZIP_CODE']
        
    #Fix some of the zip codes
    df['ZIPCODE'] = df['ZIPCODE'].astype(str).apply(lambda x: x.split('.')[0])
    df['ZIPCODE'] = df['ZIPCODE'].str.replace('_', '')
    df['ZIPCODE'] = df['ZIPCODE'].astype(str).str.zfill(5) 
    
    #filter the data (leave only data in city of Boston)
    all_zips = [zip_code for zip_list in neighborhood_zip_codes.values() for zip_code in zip_list]
    df = df[df['ZIPCODE'].isin(all_zips)]
    df['neighborhood'] = df['ZIPCODE'].apply(zip_to_neighborhood)

    
    return df

#category of LU column
valid_lu_values = ['A', 'R1', 'R2', 'R3', 'R4']
occupancy_order = {'A': 5, 'R4': 4, 'R3': 3, 'R2': 2, 'R1': 1}

def find_downgrades(df_year1, df_year2, occupancy_order):
    # Find common PIDs and their LU values
    common_pids = set(df_year1['PID']) & set(df_year2['PID'])
    if not common_pids:  # Check if there are any common PIDs
        return pd.DataFrame()  # Return an empty DataFrame if no common PIDs
    df_common_year1 = df_year1[df_year1['PID'].isin(common_pids)][['PID', 'LU', 'neighborhood']]
    df_common_year2 = df_year2[df_year2['PID'].isin(common_pids)][['PID', 'LU', 'neighborhood']]

    # Merge on 'PID' to compare LU values
    merged = pd.merge(df_common_year1, df_common_year2, on='PID', suffixes=('_before', '_after'))
    
    # Only consider rows where both LU_before and LU_after are in the occupancy_order dictionary
    valid_merge = merged[(merged['LU_before'].isin(occupancy_order.keys())) & (merged['LU_after'].isin(occupancy_order.keys()))]

    # Calculate changes in LU, considering only downgrades within the specified types
    valid_merge['downgrade'] = valid_merge.apply(lambda row: occupancy_order[row['LU_before']] - occupancy_order[row['LU_after']], axis=1)
    downgrades = valid_merge[valid_merge['downgrade'] > 0]
    return downgrades


# In[51]:


#Processed Data
processed_data = {}
years = list(range(2004, 2025))  # Include 2024 for processing up to 2023-2024

for year in years:
    processed_data[year] = process_csv(year, data_url[year], neighborhood_zip_codes)


# 4.1 Number of Units Downgraded by Community/Neighborhood from 2004-2024

# In[55]:


# Initialize a dictionary to hold the downgrades by neighborhood for each year
neighborhoods = ['Allston/Brighton', 'Back Bay/Beacon Hill', 'Central Boston', 
                'Charlestown', 'Chestnut Hill', 'Dedham', 'Dorchester', 'East Boston', 
                'Fenway/Kenmore', 'Hyde Park', 'Jamaica Plain', 'Mattapan', 'Newton', 
                'Readville', 'Roslindale', 'Roxbury', 'Roxbury Crossing', 'South Boston', 
                'South End', 'West Roxbury']
downgrades_by_neighborhood = {neighborhood: [] for neighborhood in neighborhoods}

for year in range(2004, 2024):
    if year + 1 in processed_data:
        df_year1 = processed_data[year]
        df_year2 = processed_data[year + 1]
        downgrades = find_downgrades(df_year1, df_year2, occupancy_order)
        neighborhood_downgrades = downgrades.groupby('neighborhood_after').size()

        # Append the number of downgrades for each neighborhood to the corresponding list in the dictionary
        for neighborhood in neighborhoods:
            downgrades_by_neighborhood[neighborhood].append(neighborhood_downgrades.get(neighborhood, 0))


# In[56]:


# Plot the data
plt.figure(figsize=(14, 8))
years = range(2005, 2025)  # From year after 2004 to 2024
for n in neighborhoods:
    yearly_downgrades = downgrades_by_neighborhood[n]
    plt.plot(years, yearly_downgrades, marker='o', label=n)

plt.title('Number of Buildings Downgraded by Neighborhood (2004-2024)')
plt.xlabel('Year')
plt.ylabel('Number of Downgrades')
plt.legend(title='Neighborhood', loc='upper left', bbox_to_anchor=(1.05, 1))
plt.grid(True)
plt.tight_layout()
plt.show()


# 4.2 Total number of units downgraded by Community/Neighborhood

# In[59]:


# Calculate the total number of downgrades for each neighborhood over the years
total_downgrades_by_neighborhood = {neighborhood: sum(downgrades) for neighborhood, downgrades in downgrades_by_neighborhood.items()}

# Sort the dictionary by total downgrades in descending order
sorted_downgrades = dict(sorted(total_downgrades_by_neighborhood.items(), key=lambda item: item[1]))

# Set up the plot
plt.figure(figsize=(14, 8))

# Data preparation for plotting
neighborhoods = list(sorted_downgrades.keys())
totals = list(sorted_downgrades.values())

# Create a horizontal bar plot
plt.barh(neighborhoods, totals, color='blue')

# Adding plot labels and title
plt.ylabel('Neighborhood')
plt.xlabel('Total Number of Downgrades')
plt.title('Total Number of Units Downgraded by Neighborhood (2004-2023)')
plt.tight_layout()

# Show the plot
plt.show()


# In[ ]:




