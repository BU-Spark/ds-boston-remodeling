#!/usr/bin/env python
# coding: utf-8

# **Questions that will be answered:**<br>
# What communities are building more housing units?<br>
# Which ones are losing housing units?<br> 
# <br>
# **Method**<br>
# Take in all the data from Property assessments (2004-2024). For each year, group the data by its zip code, count the housing units within that code area. Compare the growth for each area within 20 years.<br>
# <br>

# **Load Data**

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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


# **Data Cleaning + Processing**

# In[3]:


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


# In[4]:


#Preprocess the given data
processed_data_dict = {}

def zip_to_neighborhood(zip_code):
    for neighborhood, zips in neighborhood_zip_codes.items():
        if zip_code in zips:
            return f"{neighborhood} ({zip_code})"
    return None

def process_csv(file_path, neighborhood_zip_codes):
    #read in csv file
    df = pd.read_csv(file_path)
    
    #Handle 2005 data individually (since it has mismatched column)
    if url == 'https://data.boston.gov/dataset/e02c44d2-3c64-459c-8fe2-e1ce5f38a035/resource/5bfe4ca0-71c0-4751-bdcf-dad4d58445e0/download/data2005-lite.txt':
        #df['ZIPCODE'] = np.nan
        df['ZIPCODE'] = df['PTYPE']
    #Rename columns to "MAIL_ZIP" if variations are found
    col_names_to_check = ['ZIPCODE', 'ZIP_CODE']
    for col_name in col_names_to_check:
        if col_name in df.columns:
            df.rename(columns={col_name: 'ZIPCODE'}, inplace=True)
            break
            
            
    #Fix some of the zip codes
    df['ZIPCODE'] = df['ZIPCODE'].astype(str).apply(lambda x: x.split('.')[0])
    df['ZIPCODE'] = df['ZIPCODE'].str.replace('_', '')
    df['ZIPCODE'] = df['ZIPCODE'].astype(str).str.zfill(5) 
    
    #filter the data (leave only data in city of Boston)
    all_zips = [zip_code for zip_list in neighborhood_zip_codes.values() for zip_code in zip_list]
    df = df[df['ZIPCODE'].isin(all_zips)]
    df['neighborhood'] = df['ZIPCODE'].apply(zip_to_neighborhood)
    
    #group the data
    grouped_data = df.groupby('neighborhood').size()
    
    return df, grouped_data


# **Save Pre-processed Data**

# In[5]:


def save_processed_data(year, df):
    # Define a file name
    filename = f"property_assessment_processed_Q1_Q2_{year}.csv"
    # Save the Dataframe to CSV
    df.to_csv(filename, index=False)
    print(f"Data for {year} saved.")
    
for year, url in data_url.items():
    df, grouped_data = process_csv(url, neighborhood_zip_codes)
    save_processed_data(year, df)


# **Visualization**

# In[7]:


#Create a new dictionary
#key = combination of neighborhood and zip code (ex. Central Boston (02101))
#items = number of housing units from 2004-2024
neighborhood_zip_code_changes = {}

for combination in neighborhood_zip_code_combinations:
    changes = []
    
    neighborhood, zip_code = combination.split('(')
    zip_code = zip_code[:-1]
    
    for year in range(2004, 2025):
        #get corresponding data from processed_data_dict
        data = processed_data_dict.get(year, [])
            
        #find matching item
        units = 0
        for item in data:
            if item[0] in combination:
                units = item[1]
                #add to list
                changes.append(units)
                break
        else:
            #dealing with unmatched case
            changes.append(units)
            
            
                
    neighborhood_zip_code_changes[combination] = changes


# Number of Housing Units Changes from 2004-2024 for each Community/Neighborhood

# In[8]:


#Plot a graph for each neighborhood 
#(same neighborhood but different zip codes count in one graph)
years = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018,
            2019, 2020, 2021, 2022, 2023, 2024]

for neighborhood in neighborhood_zip_codes:
    #Create a graph for each neighborhood
    plt.figure(figsize=(18, 9))
    
    for combination in neighborhood_zip_code_changes:
        current_neighborhood, zip_code = combination.rsplit(' ', 1)
        zip_code = zip_code.strip('()')
        
        #Check if the neighborhood of current combination matches current neighborhood
        if current_neighborhood == neighborhood:
            #Retrieve data and plot
            data = neighborhood_zip_code_changes[combination]    
            plt.plot(years, data, marker='o', label=f"{neighborhood} ({zip_code})")
            
    #label the graph and show
    plt.xlabel('Years')
    plt.ylabel('Number of Housing Units')
    plt.title(f'Number of Housing Units Changes from 2004-2024 in {neighborhood}')
    plt.grid(True)
    plt.legend()
    plt.show()
  


# Number of Housing Units Change from 2004-2024 for specific zip code (For Final Report Visualization)

# In[11]:


#For final report visualization
# Specific neighborhood and ZIP code to plot
specific_neighborhood = ["South Boston", "East Boston", "Allston/Brighton", "Central Boston"]
specific_zip_code = [["02127"], ["02128"], ["02135"], ["02102", "02103", "02104", "02107", "02211"]]

# Iterate over each neighborhood and its corresponding ZIP codes
for index, neighborhood in enumerate(specific_neighborhood):
    plt.figure(figsize=(18, 9))
    for zip_code in specific_zip_code[index]:
        combination_key = f"{neighborhood} ({zip_code})"
        if combination_key in neighborhood_zip_code_changes:
            data = neighborhood_zip_code_changes[combination_key]
            plt.plot(years, data, marker='o', label=f"{zip_code}")

    # Label the graph
    plt.title(f'Number of Housing Units Changes from 2004-2024 in {neighborhood}')
    plt.xlabel('Years', fontsize=12)
    plt.ylabel('Number of Housing Units', fontsize=12)
    plt.legend(title='ZIP Code')
    plt.grid(True)
    plt.show()


# Number of Housing Units by Zip Code from 2004-2024 (Not used in Final Report)

# In[6]:


#plot the graph (2004-2024)
for year, url in data_url.items():
    
    df, grouped_data = process_csv(url, neighborhood_zip_codes)
    
    #store the data for further analysis
    stored_data = df.groupby('neighborhood').size().reset_index(name='units')
    processed_data_dict[year] = stored_data.values.tolist()

    plt.figure(figsize=(18, 9))
    plt.bar(grouped_data.index, grouped_data.values)
    plt.xlabel('Zip Code', fontsize=12)
    plt.ylabel('Number of Housing Units', fontsize=12)
    plt.title(f'Number of Housing Units by Zip Code ({year})', fontsize=14)
    plt.xticks(rotation=90, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.show()


# **Statistics**

# Unit Gain/Loss for each Zip Code

# In[25]:


#Calculate the growth of each neighborhood (zip code) combination
all_changes = []
for combination in neighborhood_zip_code_changes:
    changes = neighborhood_zip_code_changes[combination][-1] - neighborhood_zip_code_changes[combination][0]
    all_changes.append([combination, changes])
    if changes >= 0:
        print(f"{combination} is building {changes} more housing units from 2004 to 2024")
    else:
        print(f"{combination} is losing {np.abs(changes)} housing units from 2004 to 2024")


# Unit Loss in Roxbury Crossing 2012-2014

# In[27]:


# Specific combination to check
specific_combination = "Roxbury Crossing (02120)"

# Accessing the data for Roxbury Crossing from 2012 and 2014
# Assuming the data is stored with each year as an index from 0 for 2004 to 20 for 2024
data_2012 = neighborhood_zip_code_changes[specific_combination][8]  # Year 2012 is the 9th element (index 8)
data_2014 = neighborhood_zip_code_changes[specific_combination][10]  # Year 2014 is the 11th element (index 10)

# Calculate the change in housing units from 2012 to 2014
change_2012_to_2014 = data_2014 - data_2012

# Output the result
if change_2012_to_2014 >= 0:
    print(f"{specific_combination} built {change_2012_to_2014} more housing units from 2012 to 2014")
else:
    print(f"{specific_combination} lost {abs(change_2012_to_2014)} housing units from 2012 to 2014")


# Zip Code with Most Gain/Loss

# In[75]:


#Find out the community with the most housing units built/lost
max_building_units = 0
max_losing_units = 0
max_build_neighborhood = ''
max_lose_neighborhood = ''

for neighborhood, units in all_changes:
    if units >= 0:
        if units > max_building_units:
            max_building_units = units
            max_build_neighborhood = neighborhood
        else:
            continue
    else:
        if units < max_losing_units:
            max_losing_units = units
            max_lose_neighborhood = neighborhood
        else:
            continue
            
print(f"From 2004 to 2024, {max_build_neighborhood} is building the most housing units ({max_building_units} units)")
print(f"From 2004 to 2024, {max_lose_neighborhood} is losing the most housing units ({np.abs(max_losing_units)} units)")

