#!/usr/bin/env python
# coding: utf-8

# Import libraries
import pandas as pd


# Segregating borrowers into age category
def age_group(df, target, predictor):
    
    deli_age = df[[target, predictor]]
    deli_age['age_group'] = 'str'
    deli_age['age_group'][deli_age[predictor]>=80] = 'very old'
    deli_age['age_group'][(deli_age[predictor]<80) & (deli_age[predictor]>=60)] = 'senior citizen'
    deli_age['age_group'][(deli_age[predictor]<60) & (deli_age[predictor]>=18)] = 'adult'
    deli_age['age_group'][deli_age[predictor]<18] = 'young'
    
    return deli_age


# Segregating borrowers into monthly income class
def income_class(df, target, predictor):
    
    # Compute 25th and 75th percentile
    p_25 = df[predictor].quantile(0.25)
    p_75 = df[predictor].quantile(0.75)

    deli_income = df[[target,predictor]]
    deli_income['income_class'] = 'str'
    deli_income['income_class'][deli_income[predictor]>p_75] = 'upper income'
    deli_income['income_class'][(deli_income[predictor]<=p_75) &\
                            (deli_income[predictor]>=p_25)] = 'middle income'
    deli_income['income_class'][deli_income[predictor]<p_25] = 'lower income'
    
    return deli_income


# Segregating borrowers into dependents categories
def dep_group(df, target, predictor):

    deli_dep = df[[target,predictor]]
    deli_dep['dep_group'] = None
    deli_dep['dep_group'][deli_dep[predictor]==0] = 'single'
    deli_dep['dep_group'][(deli_dep[predictor]>=1) & (deli_dep[predictor]<=3)] = 'small family'
    deli_dep['dep_group'][(deli_dep[predictor]>=4) & (deli_dep[predictor]<=9)] = 'large family'
    deli_dep['dep_group'][deli_dep[predictor]>=10] = 'joint family'
    
    return deli_dep


# Function for cleaning a data
def cleaning(data):
    
    """ This function generate a cleaned data or turn unstructured data into clean data """
    
    # Remove NA values
    data = data.dropna()

    # Converting "NumberOfDependents" to an integer data type
    data['NumberOfDependents'] = data['NumberOfDependents'].astype('int64')

    # Changing column names to simple, readable names
    data.columns = ['Delinquency', 'RULOC', 'Age', '30DaysLate', 
                'DebtRatio', 'MonthlyIncome', 'OpenLoansAndLOC', '90DaysLate',
                'HELOC', '60DaysLate', 'Dependents']

    # Drop 65696 row for age zero
    data.drop(index = data.index[65696], axis=0, inplace=True)
    
    return data