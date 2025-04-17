import numpy as np
import pandas as pd

# parse the date column when reading the csv file

# first import a library that deals with date, time and datetime object ->  datetime library
from datetime import datetime

# create a function that returns a datetime object from a string; in our case the string format of the date is dd.mm.yyyy
def customer_date_parser(x):
    return datetime.strptime(x, "%d.%m.%Y")

# a lambda representation of the function customer_date_parser
# custom_date_parser = lambda x: datetime.strptime(x, "%d.%m.%Y")

#when reading the csv, use params: parse_dates and date_parser as displayed below:
sal = pd.read_csv(filepath_or_buffer='Salaries_with_nulls.csv', sep=';', parse_dates=['Date'], date_parser=customer_date_parser)

sal.info()

sal.shape

sal.info()

sal.head()

# Missing Data

# functions that check for missing values 
# 1.1
pd.isnull(np.nan)   #vs. pd.notnull()

pd.notnull(sal)

# functions that check for missing values 
# 1.2
pd.isnull(None)  # null @ Pandas -> DB (None)

sal.isna().sum()

sal.isna().count()

# function that ckech or missgn values
# 2.1
pd.isna(None)  #vs. pd.notna()

# function that ckech or missgn values
# 2.2
pd.isna(np.nan)

# check how many non missing values there are in the columns
pd.notnull(sal).sum()

# thsi also works 
sal.isna()  #method

# create a function to calculate missing values for each column in the df
def table_view_of_missing_values(df):
    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total,percent], axis=1 , keys=['Total', 'Percent'])
    return missing_data[missing_data['Total'] > 0]   

#def table_view_of_missing_values(df):
#    total = df.isnull().sum().sort_values(ascending=False)
#    percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
#    missing_data = pd.concat([total,percent], axis=1, keys=['Total','Percent'])
#    return missing_data[missing_data['Total'] > 0]

table_view_of_missing_values(sal)

# fill the missing valeus with 0
sal.fillna(0)

# Dates 

Medium Article:   Demystifying the Python datetime MOdule With Examples (Esther Vaati)

# from datetime import date
from datetime import datetime 
#current date time
datetime.now()

# custom date time
datetime(2022, 5, 20)

# How to convert Strings into Datetime
# Python strptime() is a method in the datetime module. 
#This is the syntax:
# dateobj = datetime.strptime(date_string, format)
# Python date time format: https://strftime.org/
d= datetime.strptime('01.3.2011',"%d.%m.%Y")
d

# Operations and Functions 

# to get the unique values of a column in an array
sal['JobTitle'].unique()

# getting a length of an array
sal['JobTitle'].nunique()

# the 2nd option for it
len(sal['JobTitle'].unique())

# commonly used:
sal['JobTitle'].value_counts().head()



sal.mean()

sal.max()

sal.head()

def get_first_name(input_string)
    return input_string.split()[0]

def get_last_name(input_string)
    if len(input_string.split()) > 1:
        return input_string.split()[1]
    else:
        return input_string.split()[0]

sal['EmployeeName'].apply(get_first_name)

sal['EmployeeName'].apply(get_last_name)

sal['FirstName'] = sal['EmployeeName'].apply(get_first_name)

sal['LastName'] = sal['EmployeeName'].apply(get_last_name)

sal.head()

Accessor Object 

# Accessor Object
# Works with the STRIN G
# FInd the employee that hold a 'CAPITAN' in their job title, with a basePay > 200 000
sal[(sal['JobTitle'].str.contains('CAPTAIN')) & (sal['BasePay']>200000)]

sal['Date'].dt.year

# Accessor object
# Work with the DATETIME
sal['year'] = sal['Date'].dt.year

sal.head()

# Merge 

sal_ret = pd.read_csv('retirement_age.csv',sep=';')

sal_ret.head()

pd.merge(sal, sal_ret, on='JobTitle') # default how = 'inner'

pd.merge(sal, sal_ret, on='JobTitle', how='left').shape

sal.shape

# we can also call merge method on the df itself
# notice that we can also use 'left_on' and 'right_on' parameters, not just 'on'
sal.merge(sal_ret, left_on='JobTitle', right_on='JobTitle')

# Business Question:

OPTIONAL

We are interested in the Job Positions: CHIEF, CAPTAIN and LIEUTENANT.

For these Job Positions, please calculate the min, max and mean BasePay, as well as the max OtherPay, throughout the years.

How did the salaries develop over the years? (Can we explain why?)

job_titles_dictionary = sal['JobTitle'].value_counts().to_dict()

mapping_dictionary = {}

for key in job_titles_dictionary.keys():
    #print(key)
    if 'chief' in key.lower():
        mapping_dictionary[key] = 'CHIEF'
    elif 'captain' in key.lower():
        mapping_dictionary[key] = 'CAPTAIN'
    elif 'lieutenant' in key.lower():
        mapping_dictionary[key] = 'LIEUTENANT'
    else:
        mapping_dictionary[key] = 'Irrelevant_for_research'

job_titles_dictionary = sal['JobTitle'].value_counts().to_dict()

mapping_dictionary = {}

for key in job_titles_dictinary.keys():
    #print(key)
    if 'chief' in key.lower():
        mapping_dictionary[key]= 'CHIEF'
    elif 'captain' in key.lower():
        mapping_dictionary[key] = 'CAPTAIN'
    elif 'lieutenant' in key.lower():
        mapping_dictionary[key] = 'LIEUTENANT'
    else:
        mapping_dictionary[key] = 'Irrelevant_for_research'

# HOMEWORK:
# Can we do the same thing with .apply() ?

job_title_dictionary.head()

# another way to apply a fuction
sal['JobTitleMainGroup'] = sal['JobTitle'].map(mapping_dictionary)

sal.head()

pd.options.display.float_format = '${:,.2f}'.format
sal.groupby(['JobTitleMainGroup', 'year']).agg({'BasePay': ['mean', 'min', 'max'], 'OtherPay': ['max'] }) #.drop('Irrelevant_for_research', axis=0)

plot_df = sal.groupby(['JobTitleMainGroup','year']).agg({'BasePay': ['mean','min','max'], 'OtherPay':['max']}).drop('Irrelevant_for_research', axis=0)['BasePay']

plot_df = plot_df.reset_index()[['JobTitleMainGroup',	'year',	'mean']].pivot(index='year', columns='JobTitleMainGroup')

import matplotlib.pyplot as plt
# documentation: https://matplotlib.org/
# default fig size: 6.4,  4.8 inches
plt.rcParams["figure.figsize"] = (12 ,8)
import seaborn as sns
sns.set_theme()
plot_df.plot(marker="s", ms=10, xticks=[2011, 2012, 2013, 2014]);

Save excel

OPTIONAL

sal_for_excel = sal.groupby(['JobTitleMainGroup','year']).agg({'BasePay': ['mean','min','max'], 'OtherPay': ['max'] }).drop('Irrelevant_for_research', axis=0)

sal_for_excel.to_excel('group_by_job_title_year.xlsx')

Save csv

sal.to_csv('modified_salaries.csv', sep=';')

# Did we miss something?
# BasePay has 609 missing values which were ignored and OtherPay has 4 missing values, which were also ignored!
