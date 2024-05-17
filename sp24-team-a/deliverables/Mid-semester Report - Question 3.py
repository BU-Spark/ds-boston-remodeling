#!/usr/bin/env python
# coding: utf-8

# <font size="5"><strong>Mid-Semester Report - Remodeling Group A (Question 3)

# With the building permits data, we'll answer the question: **Where are housing remodels and renovation happening?**<br>
# The data will be visualized by `year`, `zip`, and `worktypes` based on the data following the steps:<br><br>
# **Extract Relevent Data**: focus on extracting data related to `issued_date`, `zip`, `worktype`. For `issued_date`, we'll extract year from its Format: "%Y-%m-%d %H:%M:%S". We'll also categorize the `worktype` to group similar types of renovations and remodels together.<br><br>
# **Visualization Plan**: <br>
# 1. A time series showing the number of permits issued for housing remodels and renovations over the years<br>
# 2. Breakdowns by zip to see geographical trends<br>
# 3. Breakdowns by worktype to understand what kinds of remodels and rennovations are most common
# 

# <font size="3"><strong>Load the Data

# In[2]:


#Load the data
import pandas as pd

file_path = 'approved_building_permits.csv'
df = pd.read_csv(file_path)


# <font size="3"><strong>Data Cleaning and Transformation

# In[3]:


#Data Cleaning and Transformation

#Convert `issued_date` to datetime format
df['issued_date'] = pd.to_datetime(df['issued_date'])

#Extract year from `issued_date` for easier analysis by year
df['year'] = df['issued_date'].dt.year

#Convert `declared_valuation` to a numeric format
df['declared_valuation'] = df['declared_valuation'].replace('[\$,]', '', regex=True).astype(float)

#Drop rows where 'zip', 'worktype', or 'issued_date' is missing (for convenience)
df.dropna(subset=['zip', 'worktype', 'issued_date'], inplace=True)

df.head()


# In[6]:


#Check the unqiue values of 'year' column (For future visualization)
unique_years = df['year'].unique()
unique_years.sort()
print(unique_years)


# In[10]:


#Check the unique values of 'zip' column
unique_zips = df['zip'].unique()
print(unique_zips)


# In[4]:


#Clean the 'zip' column

#Step 0: Transform 'zip' column to string format, ensuring it's 5 digits
df['zip'] = df['zip'].astype(str).apply(lambda x: x.split('.')[0])
df['zip'] = df['zip'].astype(str).apply(lambda x: x.split('-')[0]) #only for '02126-1616'
df['zip'] = df['zip'].astype(str).str.zfill(5)

print(df['zip'].unique())


# In[5]:


#Reference to which zip belongs to which city
neighborhood_zip_codes = {
    "Allston/Brighton": ["02134", "02135", "02163"],
    "Back Bay/Beacon Hill": ["02108", "02116", "02117","02123", "02133", "02199", "02216", "02217", "02295"],
    "Central Boston": ["02101", "02102", "02103", "02104", "02105", "02106", "02107", "02109", "02110", "02111", "02112", "02113", "02114", "02196", "02201", "02202", "02203", "02204", "02205", "02206", "02207", "02208", "02209", "02211", "02212", "02222", "02293"],
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

#Step 1: Match zip codes and assign neighborhood names
def assign_neighborhood(zip_code):
    for neighborhood, zip_codes in neighborhood_zip_codes.items():
        if zip_code in zip_codes:
            return neighborhood
    return None

df['neighborhood'] = df['zip'].apply(assign_neighborhood)
#Drop rows with neighborhood missing
df.dropna(subset=['neighborhood'], inplace=True)

print(df[['zip', 'neighborhood']].head())


# In[20]:


#Check the unique values for worktype
unique_worktypes = df['worktype'].unique()
print(unique_worktypes)


# In[5]:


#Clean the 'worktype' column

#Step 1: Convert all to uppercase
df['worktype'] = df['worktype'].str.upper()

print(df['worktype'].unique())


# In[6]:


#Based on the description, consolidate into broader categories for simplicity and clearer analysis
worktype_categories = {
    'INTEXT': 'Renovations', 
    'COB': 'Municipal', 
    'OTHER': 'Other', 
    'EXTREN': 'Renovations', 
    'INTREN': 'Renovations', 
    'VIOL': 'Compliance', 
    'ADDITION': 'Additions', 
    'EXTDEM': 'Renovations', 
    'FA': 'Safety Systems', 
    'SPRINK': 'Safety Systems', 
    'SIGNES': 'Signage', 
    'CELL': 'Infrastructure', 
    'NEWCON': 'New Construction', 
    'ERECT': 'New Construction', 
    'SPRNK9': 'Safety Systems', 
    'SITE': 'Site Work', 
    'ROOF': 'Roofing', 
    'FSTTRK': 'Other',
    'PLUMBING': 'Plumbing', 
    'CHGOCC': 'Compliance',
    'SOL': 'Green Energy', 
    'SPCEVE': 'Temporary Structures', 
    'INTDEM': 'Demolition', 
    'GENERAL': 'Other', 
    'CANP': 'Outdoor Structures', 
    'AWNING': 'Outdoor Structures',
    'TCOO': 'Compliance', 
    'FENCE2': 'Fencing', 
    'INSUL': 'Renovations', 
    'GEN': 'Infrastructure', 
    'GARAGE': 'New Construction', 
    'SD': 'Site Work', 
    'LVOLT': 'Electrical', 
    'SIDE': 'Renovations', 
    'SIGNS': 'Signage',
    'RESPAR': 'Infrastructure', 
    'ELECTRICAL': 'Electrical', 
    'DRIVE': 'Site Work', 
    'NROCC': 'Compliance', 
    'MAINT': 'Maintenance', 
    'TEMTRL': 'Temporary Structures', 
    'INDBLR': 'Infrastructure', 
    'SPFT': 'Other',
    'RNWSIG': 'Signage', 
    'COMPAR': 'Infrastructure', 
    'AWNRNW': 'Outdoor Structures', 
    'AWNRET': 'Outdoor Structures', 
    'CANPRN': 'Outdoor Structures', 
    'RAZE': 'Demolition', 
    'TMPSER': 'Temporary Structures', 
    'HOLVEN': 'Temporary Structures',
    'OSEAT': 'Outdoor Structures', 
    'FENCE': 'Fencing', 
    'TMPUSOC': 'Compliance', 
    'FLAM': 'Safety Systems', 
    'CONVRT': 'Other', 
    'REPAIR': 'Maintenance', 
    'SRVCHG': 'Electrical', 
    'TVTRK': 'Temporary Structures',
    'BFCHMDECMA': 'Renovations', 
    'SERVICE': 'Maintenance', 
    'MAIN': 'Maintenance', 
    'TRENCH': 'Site Work', 
    'GAS': 'Plumbing', 
    'NEW': 'New Construction', 
    'INDFUR': 'Infrastructure', 
    'BFCHMTENT': 'Temporary Structures',
    'BFCHMFLOOR': 'Renovations', 
    'BFCHMINFIN': 'Renovations', 
    'BFCHMTEMPE': 'Temporary Structures', 
    'FENCING': 'Fencing', 
    'SPECEVENT': 'Temporary Structures', 
    'BFCHMMATTR': 'Renovations',
    'DUMPSTERS': 'Site Work', 
    'STAGING': 'Site Work', 
    'SPEEVENTS': 'Temporary Structures'
}
#Step 2: Apply the mapping to consolidate work types
df['worktype_category'] = df['worktype'].map(worktype_categories).fillna('Other')

print(df['worktype_category'].unique())


# <font size="3"><strong>Data Aggregation & Visualization

# In[7]:


import matplotlib.pyplot as plt


# <font size="3">1. The trend of the number of permits issued each year

# In[8]:


# Count the number of permits issued each year
filtered_df = df[(df['year'] >= 2010) & (df['year'] <= 2023)]
permits_by_year = filtered_df.groupby('year').size()

#Plot
plt.figure(figsize=(10, 6))
permits_by_year.plot(kind='line', marker='o', linestyle='-', color='blue')
plt.title('Trend of Permits Issued vs. Year')
plt.xlabel('Year')
plt.ylabel('Number of Permits Issued')
plt.grid(True)
plt.show()


# <font size="3">2. How the number of permits changes over years for each neighborhood

# In[9]:


#Count the number of permits issued each year for each neighborhood
permits_by_year_neighborhood = filtered_df.groupby(['year', 'neighborhood']).size().unstack(fill_value=0)

#Plot
plt.figure(figsize=(14, 8))
for neighborhood in permits_by_year_neighborhood.columns:
    plt.plot(permits_by_year_neighborhood.index, permits_by_year_neighborhood[neighborhood], marker='o', label=neighborhood)

plt.title('Numer of Permits Issued by Year and Neighborhood')
plt.xlabel('Year')
plt.ylabel('Number of Permits Issued')
plt.legend(title='Neighborhood', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()


# In[11]:


renovations_df = filtered_df[(filtered_df['worktype_category'] == 'Renovations')]

permits_by_year_neighborhood = renovations_df.groupby(['year', 'neighborhood']).size().unstack(fill_value=0)
                             
                        
# Plot
plt.figure(figsize=(14, 8))
for neighborhood in permits_by_year_neighborhood.columns:
    # Plot only if the neighborhood has at least one renovation permit
    if permits_by_year_neighborhood[neighborhood].sum() > 0:
        plt.plot(permits_by_year_neighborhood.index, 
                 permits_by_year_neighborhood[neighborhood], 
                 marker='o', 
                 linestyle='-', 
                 label=neighborhood)

plt.title('Number of "Renovations" Permits Issued by Year and Neighborhood (2010-2023)')
plt.xlabel('Year')
plt.ylabel('Number of "Renovations" Permits Issued')
plt.legend(title='Neighborhood', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.xticks(range(2010, 2024))  # Ensure x-ticks cover the range from 2010 to 2023
plt.tight_layout()  # Adjust layout for legend
plt.show()


# In[12]:


included_neighborhoods = ['Dorchester', 'Central Boston', 'Back Bay/Beacon Hill', 'South Boston', 'Fenway/Kenmore']
renovations_df = filtered_df[(filtered_df['worktype_category'] == 'Renovations') &
                            filtered_df['neighborhood'].isin(included_neighborhoods)]

permits_by_year_neighborhood = renovations_df.groupby(['year', 'neighborhood']).size().unstack(fill_value=0)
                             
                        
# Plot
plt.figure(figsize=(14, 8))
for neighborhood in permits_by_year_neighborhood.columns:
    # Plot only if the neighborhood has at least one renovation permit
    if permits_by_year_neighborhood[neighborhood].sum() > 0:
        plt.plot(permits_by_year_neighborhood.index, 
                 permits_by_year_neighborhood[neighborhood], 
                 marker='o', 
                 linestyle='-', 
                 label=neighborhood)

plt.title('Number of "Renovations" Permits Issued by Year and Neighborhood (2010-2023)')
plt.xlabel('Year')
plt.ylabel('Number of "Renovations" Permits Issued')
plt.legend(title='Neighborhood', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.xticks(range(2010, 2024))  # Ensure x-ticks cover the range from 2010 to 2023
plt.tight_layout()  # Adjust layout for legend
plt.show()


# <font size="3">3. How the number of permits for each worktype category changes over the years

# In[20]:


#Count the number of permits issued each year for each worktype category
permits_by_year_worktype = filtered_df.groupby(['year', 'worktype_category']).size().unstack(fill_value=0)

#Plot
plt.figure(figsize=(14, 8))
for worktype_category in permits_by_year_worktype.columns:
    plt.plot(permits_by_year_worktype.index, permits_by_year_worktype[worktype_category], marker='o', linestyle='-', label=worktype_category)
    
plt.title('Number of Permits Issued by Year and Worktype Category')
plt.xlabel('Year')
plt.ylabel('Number of permits Issued')
plt.legend(title='Worktype Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()


# In[21]:


#Plot (Exclude Plumbing, Renovations, Electrical, for a clearer visualzation)
plt.figure(figsize=(14, 8))
for worktype in permits_by_year_worktype.columns:
    if worktype != 'Plumbing' and worktype != 'Renovations' and worktype != 'Electrical':
        plt.plot(permits_by_year_worktype.index, permits_by_year_worktype[worktype], marker='o', linestyle='-', label=worktype)
    
plt.title('Number of Permits Issued by Year and Worktype Category (Exclude Plumbing, Renovations, Electrical)')
plt.xlabel('Year')
plt.ylabel('Number of permits Issued')
plt.legend(title='Worktype Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()


# <font size="3">4. Distribution of permits by worktype categories for each year and each neighborhood

# In[40]:


years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020,
 2021, 2022, 2023]
neighborhoods = ["Allston/Brighton", "Back Bay/Beacon Hill", "Central Boston", "Charlestown", "Chestnut Hill",
                 "Dedham", "Dorchester", "East Boston", "Fenway/Kenmore", "Hyde Park",
                 "Jamaica Plain", "Mattapan", "Newton", "Readville", "Roslindale", "Roxbury",
                 "Roxbury Crossing", "South Boston", "South End", "West Roxbury"]

for y in years:
    df_selected_year = filtered_df[filtered_df['year'] == y]
    
    #List of unique neighborhoods
    unique_neighborhoods = df_selected_year['neighborhood'].unique()
    
    #Number of unique neighborhoods
    n_neighborhoods = len(unique_neighborhoods)
    
    #Set up matplotlib figure
    fig, axes = plt.subplots(nrows=n_neighborhoods, ncols=1, figsize=(14, 4*n_neighborhoods))
    
    if n_neighborhoods == 1:
        axes = [axes]
    
    #Loop through each neighborhood and plot a histogram for it
    for i, neighborhood in enumerate(unique_neighborhoods):
        #Filter data
        neighborhood_data = df_selected_year[df_selected_year['neighborhood'] == neighborhood]
        #Count the permits by worktype category
        permit_counts = neighborhood_data.groupby('worktype_category').size()
        
        #Plot the histogram
        axes[i].bar(permit_counts.index, permit_counts.values)
        axes[i].set_title(f'Permit Distribution by Worktype Category - {neighborhood} ({y})')
        axes[i].set_xlabel('Worktype Category')
        axes[i].set_ylabel('Number of Permits')
        axes[i].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()


# 5. For each neighborhood, the number of permits changes by year for each worktype category

# In[24]:


neighborhoods = ["Allston/Brighton", "Back Bay/Beacon Hill", "Central Boston", "Charlestown", "Chestnut Hill",
                 "Dedham", "Dorchester", "East Boston", "Fenway/Kenmore", "Hyde Park",
                 "Jamaica Plain", "Mattapan", "Newton", "Readville", "Roslindale", "Roxbury",
                 "Roxbury Crossing", "South Boston", "South End", "West Roxbury"]

permit_count_neighborhood_worktype = filtered_df.groupby(['neighborhood', 'worktype_category', 'year']).size()

for n in neighborhoods:
    neighborhood_df = filtered_df[filtered_df['neighborhood'] == n]
    neighborhood_worktype_categories = neighborhood_df['worktype_category'].unique()
    plt.figure(figsize=(14, 8))
    #print(f'For {n}:')
    
    for w in neighborhood_worktype_categories:
        yearly_counts = permit_count_neighborhood_worktype.loc[n].loc[w].reindex(range(2010, 2024), fill_value=0)
        #print(f'{w}: {dict(yearly_counts)}')
        plt.plot(yearly_counts.index, yearly_counts.values, label=w, marker='o')
    
    plt.title(f'Permit Counts for {n} (2010-2024)')
    plt.xlabel('Year')
    plt.ylabel('Number of Permits')
    plt.legend(title='Worktype Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# <font size="3"><strong>Statistics

# <font size="3">1. Number of permits issued by years

# In[43]:


total_permits_by_year = df.groupby('year').size()
for year, total_permits in total_permits_by_year.iteritems():
    print(f"For year {year}, {total_permits} permits were issued.")


# In[44]:


year_max_permits = total_permits_by_year.idxmax()
max_permits = total_permits_by_year.max()
year_min_permits = total_permits_by_year.idxmin()
min_permits = total_permits_by_year.min()
print(f"{year_max_permits} has the maximum permits which is: {max_permits} permits")
print(f"{year_min_permits} has the minimum permits which is: {min_permits} permits")


# <font size="3">2. Percentage Growth

# In[49]:


growth_percentage = total_permits_by_year.pct_change() * 100
print("\nGrowth percentage between each two consecutive years:")
for year, growth in growth_percentage.iteritems():
    if pd.notnull(growth) and year != 2009 and year != 2024:
        print(f"From {year-1} to {year}: {growth: .2f}%")


# In[51]:


print("2009-2010 has the maximum percentage growth which is: 3531.96%")
print("2019-2020 has the minimum percentage growth which is: -28.71%")


# <font size="3">3. Number of Permits by Worktype Category for each year

# In[56]:


years = [2006, 2007, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020,
 2021, 2022, 2023, 2024]
for y in years:
    print(f"For year {y}")
    df_selected_year = df[df['year'] == y]
    unique_worktypes = df_selected_year['worktype_category'].unique()
    for worktype in unique_worktypes:
        worktype_data = df_selected_year[df_selected_year['worktype_category'] == worktype]
        permit_counts = len(worktype_data)
        print(f"There are {permit_counts} permits for {worktype}")
    print("\n")


# <font size="3">3.1 Top 3 and Min Permits by Worktype Category for each year

# In[60]:


for y in years:
    print(f"For year {y}")
    df_selected_year = df[df['year'] == y]
    unique_worktypes = df_selected_year['worktype_category'].unique()
    # Initialize a dictionary to hold worktype as key and permit counts as value
    permit_counts_by_worktype = {}

    for worktype in unique_worktypes:
        worktype_data = df_selected_year[df_selected_year['worktype_category'] == worktype]
        permit_counts = len(worktype_data)
        permit_counts_by_worktype[worktype] = permit_counts

    if permit_counts_by_worktype:  # Check if the dictionary is not empty
        # Sort the worktype by permit counts in descending order and take the top 3
        sorted_worktypes = sorted(permit_counts_by_worktype.items(), key=lambda x: x[1], reverse=True)
        top_3_worktypes = sorted_worktypes[:3]
        min_worktype = sorted_worktypes[-1]  # The worktype with the minimum permits

        print("    Top 3 worktypes with most permits:")
        for worktype, count in top_3_worktypes:
            print(f"        {worktype}: {count} permits")
        
        print(f"    Worktype with fewest permits: {min_worktype[0]} ({min_worktype[1]} permits)\n")
    else:
        print("    No permit data available for this year.")


# <font size="3">4. Neighborhoods with the top 3 and fewest permits for each year

# In[61]:


for y in years:
    print(f"For year {y}:")
    df_selected_year = df[df['year'] == y]
    permit_counts_by_neighborhood = df_selected_year.groupby('neighborhood').size().sort_values(ascending=False)
    
    # Check if there are neighborhoods data available for the year
    if not permit_counts_by_neighborhood.empty:
        # Get the top 3 neighborhoods
        top_3_neighborhoods = permit_counts_by_neighborhood.head(3)
        print("    Top 3 neighborhoods with most permits:")
        for neighborhood, count in top_3_neighborhoods.iteritems():
            print(f"        {neighborhood}: {count} permits")

        # Get the neighborhood with the fewest permits, excluding neighborhoods with 0 permits
        fewest_permits_neighborhood = permit_counts_by_neighborhood[permit_counts_by_neighborhood > 0].tail(1)
        neighborhood_name = fewest_permits_neighborhood.index[0]
        permits_count = fewest_permits_neighborhood.values[0]
        print(f"    Neighborhood with fewest permits: {neighborhood_name} ({permits_count} permits)\n")
    else:
        print("    No permit data available for this year.")


# <font size="3">4.1 Top 3 Worktype Categories for the top 3 neighborhoods with the most permits

# In[62]:


for y in years:
    print(f"For year {y}:")
    df_selected_year = df[df['year'] == y]
    permit_counts_by_neighborhood = df_selected_year.groupby('neighborhood').size().sort_values(ascending=False)

    # Check if there are neighborhoods data available for the year
    if not permit_counts_by_neighborhood.empty:
        # Get the top 3 neighborhoods
        top_3_neighborhoods = permit_counts_by_neighborhood.head(3).index

        for neighborhood in top_3_neighborhoods:
            print(f"    In {neighborhood}, the top 3 worktype categories with most permits:")
            # Filter the data for the selected neighborhood
            df_neighborhood = df_selected_year[df_selected_year['neighborhood'] == neighborhood]
            # Count permits by worktype category within the neighborhood
            permit_counts_by_worktype = df_neighborhood.groupby('worktype_category').size().sort_values(ascending=False).head(3)
            
            for worktype, count in permit_counts_by_worktype.iteritems():
                print(f"        {worktype}: {count} permits")
            print("\n")
    else:
        print("    No permit data available for this year.")


# In[ ]:




