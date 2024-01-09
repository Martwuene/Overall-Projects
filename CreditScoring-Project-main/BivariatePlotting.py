#!/usr/bin/env python
# coding: utf-8

# import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from scipy.stats import chi2
from termcolor import colored as cl
import streamlit as st

# Visualizing deliquency versus non-delinquency
def target_plot(data, variable):
    
    """ Visualizing countplot for dependent variable to its size of each category 0 and 1."""

    # Serious Delinquency in 2 years Count
    print(cl('Target Variable', attrs = ['bold']))
    print('------------------')
    print(data.groupby([variable]).Delinquency.count())

    # Target Variable Countplot
    fig = plt.figure(figsize = (13,4.7))

    # count plot on single categorical variable
    sns.countplot(x = variable, data = data, palette='Set2')
    plt.title('Delinquency vs Non-Delinquency', fontsize=19, fontname="Times New Roman")
    plt.xlabel('Delinquency', fontsize=13)
    plt.ylabel('No. of Borrowers', fontsize=13)
    st.pyplot(fig)
    
    

# Visualizing the relationship between categorical and numerical variables
def Category_Numerical(data, categorical, numerical, category):
    
    """ 
        Visualizing the barplot, kdeplot and boxplot to view the relationship between 
        dependent category variable and independent numerical variable if there is high 
        impact for the probability of deliquency.
    """
    
    # Creating 2 samples
    x1 = data[numerical][~(data[categorical]==category)][:]
    x2 = data[numerical][data[categorical]==category][:]
  
    # Calculating descriptives
    m1, m2 = x1.mean(), x2.mean()
    
    # Table
    table = pd.pivot_table(data=data, values=numerical, columns=categorical, aggfunc = np.mean)

    #plotting
    fig = plt.figure(figsize = (20,5.5), dpi=140)
  
    #barplot
    plt.subplot(1,3,1)
    sns.barplot([str(1-category),'{}'.format(category)], [m1, m2], palette='Set2')
    plt.ylabel('mean {}'.format(numerical))
    plt.xlabel(categorical)
    plt.title('{}'.format(table), fontsize=15, fontname="Times New Roman", fontweight="bold")

    # category-wise distribution
    plt.subplot(1,3,2)
    sns.kdeplot(x1, shade= False, color='green', label = 'non-deliquency', linewidth = 1)
    sns.kdeplot(x2, shade= True, color='blue', label = 'delinquency')
    plt.title('Categorical Distribution', fontsize=19, fontname="Times New Roman", fontweight="bold")
    
    # boxplot
    plt.subplot(1,3,3)
    sns.boxplot(x=categorical, y=numerical, data=data)
    plt.title('Categorical Boxplot', fontsize=19, fontname="Times New Roman", fontweight="bold")
    
    st.pyplot(fig)

    
# Visualizing the relationship between respondent category and independent category    
def Category_Category(data, respondent, predictor):
    
    """
        Visualizing the barplot, kdeplot and boxplot to view the relationship between 
        dependent category variable and independent numerical variable if there is high 
        impact or significant association with the probability of deliquency. As well as performing
        hypotheses test with appropriate chi-squared test.
    """
    
    # Plotting countplot
    fig = plt.figure(figsize=(13,4.7))
    sns.countplot(x=predictor, hue=respondent, data=data, palette='Set2')
    plt.ylabel('No. of Borrowers', fontsize=11)
    
    if predictor == 'age_group':
        plt.xlabel('Age Group', fontsize=12.8)
        plt.title('The relationship between delinquency and age group', fontsize=19, fontname="Times New Roman")
        
    elif predictor == 'income_class':
        plt.xlabel('Monthly Income Classes', fontsize=12.8)
        plt.title('The relationship between delinquency and income classes', fontsize=19, fontname="Times New Roman")
        
    elif predictor == 'dep_group':
        plt.xlabel('Dependents Group', fontsize=12.8)
        plt.title('The relationship between delinquency and dependents group', fontsize=19, fontname="Times New Roman")
           
    # Put the legend out of the figure
    plt.legend(title='Delinquency', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=13)
    
    st.pyplot(fig)
    
    # Contigence table
    table = pd.crosstab(data[respondent],data[predictor]).values
    
    # Performing chi-square test
    test_statistic, p_value, dof, expected = chi2_contingency(table)
    
    # Critical value
    alpha = 0.05                   # Significance level
    critical_value = chi2.ppf(q=1-alpha, df = dof)
 
    # Set up hypotheses and determine level of significance
    st.write('')
    st.write('__Hypotheses and determine level of significance__')
    st.write('__H0:__ Assumes there is no association between the two variables')
    st.write('__H1:__ Assumes there is association between the two variables.     α=0.05')
    st.write('')

    # Set up decision rule.  
    st.text('Here we have degree of freedom = {0} and a 5% level of significance. '
          'The appropriate critical \nvalue is {1:2.2f} and the decision rule is as follows: '
          'Reject H0 if χ2  >  {1:2.2f}.'.format(dof, critical_value))
    st.write('')
    
    # Compute the test statistic
    st.text('The test statistic is computed as χ2 = {0:2.2f}'.format(test_statistic))
    st.write('')
    
    # Conclusion  
    if test_statistic>=critical_value:
          st.text('We reject H0 because {0:2.2f} > {1:2.2f}. We have statistically significant'
                'evidence at α=0.05 to \nshow that H0 is false or that we assume that '
                'there is a relationship between response \nvariable and predictor variable. '
                'The p-value = {2:2.2f} is less than or equal to significance '
                '\nlevel (i.e., p <= 0.05).'.format(test_statistic, critical_value, p_value))
          
    else:  
          st.texr('We fail to reject H0. The results show that are not statistically '
                'significant which assumes that there is no association between two variables. '
                'The p-value = {0.2.2f} is greater than significance level (i.e., p > 0.05).'.format(p_value))