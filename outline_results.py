#!/usr/bin/env python
# coding: utf-8

# # COVID-19 RELATED DATA ANALYSIS

# In[2]:


import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px 
from matplotlib import pyplot as plt
import pygal
from IPython.display import SVG, display
# get_ipython().run_line_magic('matplotlib', 'notebook')


# In[3]:


#pip install pygal_maps_world
#!pip install cairosvg
#!pip install  plotly.express
#!pip install pygal
#import sys
#!conda install --yes --prefix {sys.prefix} plotly


# ## PROJECT OVERVIEW

# Current days the entire world has the same goals: define the reasons of COVID-19 pandemic starting, propogate coronavirus vaccination and analyze all the factors which can make COVID-19 cases to go to zero. As those goals look rather impressive they can be achived through the regular analysis of COVID-19 statistics including new cases, fatality. testing etc. 
# The goal of this project is analysis of real-life COVID-19 data, defining factors which are important for virus propogation, hospitality and fatality rates.

# ## DATA DESCRIPTION

# As COVID pandemic became the biggest problem of 2020, there are lot of data sources, which collects and organizes different statistics relevant coronavirus disease. This project uses different datsets collected by Epidemic Intelligence team based on different authorized reports [1]. Therefore ECDC's data keep worlwide data on daily and weekly basis, the most complete statistics provided for the European Union (EU) with 7-days frequency. That happens because every week a team of epidemiologists screen up to 500 relevant sources to collect the latest figures for publication [2]. 
# Datasource includes lot of COVID-related parameters, among them testing, new cases, hospitality, fatality etc. Current project uses 3 datasets: hospitality statistics [3], testing statistics [4] and new cases statistics [5]. Each of the links provided here keeps data link and data glossary also. 
# All files  available at csv format have been downloaded to the locally storage. Statistics describes 2020 year, each country started data gathering as far as first episodes appeared. Data heads for all three files are described below.
# 

# In[4]:


cases = pd.read_csv('cases_death.csv')
tests = pd.read_csv('testing_rate.csv')
hospitality = pd.read_csv('hospitality.csv')
print(cases.head())
print(tests.head())
print(hospitality.head())


# ## CLEANING PROCESS

# Cleaning process described below includes lot of steps oriented to the merging provided csv files, removing observations with lower sample size, filtering out part of the data to get statistics in the same time range for the different countries.
# The first part of the cleaning procedure described at the chunk below. Datafile hospitality includes both daily and weekly statistics. As other files describe COVID cases and tests by week, then hospitality daily data have been filtered out. Besides that information about data source is not used at the next part of the project, so some columns should be also removed.
# After all transormations hospitality dataset has columns: country, indicator, year_week and value.

# In[5]:


hospitality_weekly = hospitality[hospitality['indicator'].str.contains('Weekly')]#select weekly statistics

hospitality_weekly = hospitality_weekly[['country', 'indicator', 'year_week', 'value']] #select needed columns only

print(hospitality_weekly.head())


# Based on the data description above hospitality subset has long format, so it will be reshaped to wide form. For that all rows with NaN values have been removed and hospitlity dataset now includes wekkly new ICU admission per 100k population and weekly new hospital admissions per 100k population.

# In[6]:


hospitality_weekly = hospitality_weekly.dropna()

hospitality_weekly = pd.pivot_table(hospitality_weekly,  index=['country', 'year_week'], columns = ['indicator'], values='value')#reshape data from long to wide

hospitality_weekly.head(20)#check data


# As hospitality dataset now includes two different parameters by each week per countries, then hospitality could be easy merged with tests dataset by columns country and year of the week. Testing dataset also includes column testing_data_source, which is useless for the further analysis. So, it will be droped. First few rows of the merged dataset are provided below.
# After merging each week per country includes weekly hospitality parameters (Hospital admission and ICU admission), new_cases, tests_done, testing_rate and positivity_rate. Last two parameters have been calculated as 100 x Number
# of new confirmed cases divided per population and number of tests done per week respectively. Merged dataset also keeps population information and country code.

# In[7]:


hospitality_weekly = hospitality_weekly.merge(tests, left_on=['country', 'year_week'], right_on=['country', 'year_week'])#merge with testingrate


hospitality_weekly = hospitality_weekly.drop(['testing_data_source'], axis=1)#remove testing data source
#modified 
#hospitality_weekly = hospitality_weekly.drop([['testing_data_source','testing_rate','positivity_rate']], axis=1)#remove testing data source

hospitality_weekly.head()#view head


# The last dataset from proposed called cases includes some columns which also can be dropped. That's why features have been filtered before merging. There is also a need to rename some columns before merging to avoid duplicating. Format of the year_week column also should be changed. All those manipulations described at the chunk below.

# In[8]:


cases = cases[['dateRep', 'year_week', 'cases_weekly', 'deaths_weekly', 'countriesAndTerritories', 'geoId']]#remove useless columns

cases = cases.rename(columns={"countriesAndTerritories": "country", "geoId": "country_code"})#rename columns

hospitality_weekly['year_week'] = hospitality_weekly['year_week'].str.replace('W', '')#change date format

hospitality_weekly.head()#view head


# Using merging once again all three csv files have been combined to the single dataset. First few lines of the final dataset provided here describe that all columns have appropriate format and meaningfull names. Therefore columns new-cases and cases_weekly have the same information. So, one of them will be omitted.

# In[9]:


hospitality_weekly = hospitality_weekly.merge(cases, left_on=['country', 'country_code', 'year_week'], right_on=['country', 'country_code','year_week'])#merge with another data

print(hospitality_weekly.head())#view data

hospitality_weekly.drop(['new_cases'], axis=1, inplace=True)#drop duplicated column


# To make comparison between countries sophisticated we should check if theydescribe the same time periods. Checking number of observations per country we found that they have absolutely different statistics. Using this fact only countries with more than 40 observations have been selected for the further analysis. as almost all countries between 40 : 48

# In[10]:


count_by_countries = hospitality_weekly.groupby(['country_code']).size()#observations by country

#print(count_by_countries)#view stat
plt.figure(figsize=(8,2))
plt.bar(count_by_countries.index,count_by_countries)
subset = count_by_countries[count_by_countries >40].to_frame()#select contries with more than 40 observations

countries = subset.index.to_list()#create list of countries


# Thus all next steps are provided for the subset of 8 european countries, which have enough observations.

# In[11]:


print(countries)

countries_subset = hospitality_weekly.loc[hospitality_weekly['country_code'].isin(countries)]#selection of countries with many observations


# It is also important to check observations per week. Table below describes that removing observations for the initial 4 weeks of the dataset we got identical data ranges form 14: 15 . also throght theses 4 initial weeks the virus wasn't spread so much so if we consider them with analysis will affect the observation 

# In[12]:


count_by_weeks = countries_subset.groupby(['year_week']).size()#observations by country
print(count_by_weeks)#view counts


# Now we deal with subset of 15 countries by identical data ranges. 

# In[13]:


countries_subset = countries_subset.loc[~countries_subset['year_week'].isin(['2020-06', '2020-07', '2020-08', '2020-09'])]#remove observations with lower sample size


# It is also important to check data for missing values and to impute them if possible. as almost all the null values come from  "Weekly new hospital admissions per 100k" and "Weekly new ICU admissions per 100k"

# In[16]:


print(countries_subset.shape)
countries_subset.isnull().sum()


# Based on above analysi so we will drop these two columns
# * Weekly new ICU admissions per 100k       ........       232
# * Weekly new hospital admissions per 100k   .....     94

# In[17]:


check2 = countries_subset[countries_subset.columns[countries_subset.columns.str.contains('Weekly')].to_list()].isnull()#check for rows without nan

rows_with_nan = countries_subset[check2.any(axis = 1)]#create subset

rows_with_nan.groupby(['country']).size()#view countries


# Using chunk of the code above there were found that two columns of the final dataset with the names starting from 'Weekly' keeps NaN values across most of the rows. This kind of statistics can not be imputed through other columns, so they will be removed.

# In[18]:


countries_subset = countries_subset.drop(countries_subset.columns[countries_subset.columns.str.contains('Weekly')].to_list(), axis=1)#remove columns with null


countries_subset.head()#view head


# check the data if any null still exist 

# In[19]:


countries_subset.isnull().sum()





