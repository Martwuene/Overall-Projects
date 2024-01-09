#Import the required libraries
import streamlit as st

# Import libraries
import pandas as pd
import numpy as np
import Data
from termcolor import colored as cl

# Required modules for machine learning approach
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

# For visualisation
import Visualize 
import BivariatePlotting
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')


st.set_page_config(layout="wide")

# Functions for each of the pages
def home():

    # Add a title and intro text
    st.write('### Machine Learning Approach to Credit Scoring Algorithm (*"Classification"*)')
    st.write('')
    st.markdown(
    """
    *"Credit scoring algorithms, which make a guess at the probability of default, are 
    the method banks use to determine whether or not a loan should be granted. This 
    competition requires participants to improve on the state of the art in credit scoring,
    by predicting the probability that somebody will experience financial distress in the 
    next two years."*

    This was a ten-year-old competition on the Kaggle platform aimed at assisting 
    borrowers in making the best financial decisions possible using a developed machine
    learning model to predict deliquency, which may lead to default, which is the 
    probability of default (PD), one of the credit risk drivers using historical data
    from over 250 000 borrowers.

    For more details on the competition, https://www.kaggle.com/competitions/GiveMeSomeCredit/overview/description

    """
) 
    st.write('')
    st.write('')
    st.image('https://i.ytimg.com/vi/jAz2gsc0ubc/maxresdefault.jpg')


def data_load():
    st.subheader('Data Dictionary')
    st.write('The following shows a data dictionary list the variable \
        names with its discriptions and data type.')
    # Maximize column width to display all information on the DataFrame.
    pd.set_option('max_colwidth', None)
    # Print the data dictionary
    dictionary = pd.read_excel('data/Data Dictionary.xls', header=1)
    st.write(dictionary)
    st.write('')
    st.write('')
    st.subheader('Raw Data')
    st.write('Data that has not been processed and is ready to be used for an ML approach.')
    st.write(df.head(8))

# Sidebar setup
st.sidebar.title('Content')
upload_file = st.sidebar.file_uploader('Upload a file of training set only')
if upload_file is None:
    st.markdown("""
                    # HI, WELCOME!

                   # I AM MACHINE LEARNING AUTO APP

                Please read the App guide before you upload the training data set, so that you do not miss anything !!!

                    ## App Guide
                    ## Navigate

                    **Select**
                    - Overview
                    - Data Preview
                    - Bivariate Analyis: <Type> (Data Exploration)
                                         [Numerical - Numerical]
                                         [Categorical - Numerical]
                                         [Categorical - Categorical]

                    - Model Evaluation:  <Model Type>  
                                         [Logistic Regression]
                                         [Decision Tree Classifier]

        """)
    st.write('')

    
# Sidebar navigation
st.sidebar.title('Navigation')
options = st.sidebar.selectbox('Select what you want to display', 
    ['Overview', 'Data Preview','Bivariate Analysis', 'Model Evaluation'])


# Check if file has been uploaded
if upload_file is not None:
    df = pd.read_csv(upload_file, index_col = 'Unnamed: 0')

#############################################################################################
############################ Exploratory Data Analysis     ##################################

    # Make a copy of train_data and create a new variable "data"
    data = df.copy()
    # Remove NA values
    data = data.dropna()
    # Making "SeriousDlqin2yrs" a data type category
    data['SeriousDlqin2yrs'] = data['SeriousDlqin2yrs'].astype('category')
    # Converting "NumberOfDependents" to an integer data type
    data['NumberOfDependents'] = data['NumberOfDependents'].astype('int64')
    # Changing column names to simple, readable names
    data.columns = ['Delinquency', 'RULOC', 'Age', '30DaysLate', 
                    'DebtRatio', 'MonthlyIncome', 'OpenLoansAndLOC', '90DaysLate',
                    'HELOC', '60DaysLate', 'Dependents']
    # Identifying and separating numerical data types
    numerical = data.select_dtypes(include=['float64','Int64'])[:]

##############################################################################################
############################        Preprocessing          ###################################

    # A cleaning procedure for converting unclean data into usable data
    clean_train_df = Data.cleaning(df)
    # Divide the dataset into features and target variables
    X = clean_train_df.drop(['Delinquency'], axis=1) # Features
    y = clean_train_df['Delinquency'] # Target variable
    # Make a list of the column names for predictors
    features = X.columns.values
    # Set the minimum and maximum scalers
    scaler = MinMaxScaler(feature_range = (0,1))
    # Fit scaler
    scaler.fit(X)
    # Transformation of data and dataframe 
    X = pd.DataFrame(scaler.transform(X))
    # Change the names of the columns. 
    X.columns = features
    # Split X and Y into training and testing sets
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)

############################################################################################## 

    # Navigation options
    if options == 'Overview':
        home()

    elif options == 'Data Preview':
        data_load() 

    elif options == 'Bivariate Analysis':
        select = st.sidebar.selectbox('Type', ['Numerical-Numerical','Categorical-Numerical',
        'Categorical-Categorical'])
        if select == 'Numerical-Numerical':
            st.write('### Bivariate Analysis: Numerical & Numerical')
            st.write('The aim is to examine the relationship between the independent variables \
                so that they may be used in preprocessing and feature engineering.')
            st.write('')
            st.write('Below is an illustration, a table of how we changed the names of variables \
                from old to new. As a result, we perform better in data visualization.')
            st.write('')
            df = pd.DataFrame({'Old Variable Name':df.columns.values, 'New Variable Name':data.columns.values})
            st.table(df)
            st.write('#### Heatmap')
            st.markdown("""
                The heatmap will help us to visually see the main correlations between variables \
                and filter out the non-essential factors, reducing the number of variables we have \
                to deal with in the scatter plots.

                We will draw the heatmaps using three techniques for computing the correlation in order \
                to get diverse viewpoints on the correlation of the independent variables. 

                1. Pearson Correlation
                2. Kendal Rank Correlation
                3. Spearman Correlation

                """)
            # Plotting heatmaps for all numerical variables using all techniques (pearson, kendall, spearman) 
            fig = plt.figure(figsize=(39,14), dpi=140)
            for j,i in enumerate(['pearson','kendall','spearman']):
                plt.subplot(1,3,j+1)
                correlation = numerical.corr(method=i)
                heatmap = sns.heatmap(correlation, linewidth = 2, annot=True, annot_kws={"size":11})
                heatmap.set_xticklabels(heatmap.get_xmajorticklabels(), fontsize = 15)
                heatmap.set_yticklabels(heatmap.get_ymajorticklabels(), fontsize = 15)
                plt.title(i, fontsize=35)
            st.pyplot(fig)
            st.markdown("""
                __Interpretation:__

                - With the exception of a slight difference in correlation magnitude, Kendall and \
                Spearman correlation appear to have a fairly similar pattern.

                - Many variables show a very weak or insignificant association between them, depending \
                on the strength of the relationship.

                - On pearson, the days past due (DPD) variables 30DaysLate, 60DaysLate, and 90DaysLate \
                have a very strong positive relationship, as does the positive moderate correlation \
                between OpenLoansAndLOC and HELOC.

                """)
            st.write('#### Scatterplot')
            st.write('We went on to look for a filtered strong relationship between the independent \
                variables.')
            # Combining variables in groups
            pdp_variables = ['30DaysLate', '60DaysLate', '90DaysLate']
            # Scatterplot of DPD variables
            fig = sns.pairplot(numerical[pdp_variables])
            st.pyplot(fig)

            st.markdown("""

                __Interpretation:__

                Due to the existence of outliers, the scatter plot is meaningless. Let's use Boxplot to \
                visualize the sense variable, and then use the appropriate strategy to moderate the outliers.

                """)
            st.write('#### Boxplot')
            st.write("""
                A boxplot is a standardized method of depicting data distributions using a five-number \
                summary ("minimum," first quartile (Q1)), median, third quartile (Q3), and "maximum"). It \
                can give you information about your outliers and their values. It can also determine if your \
                data is symmetrical, how closely your data is packed, and whether or not your data is skewed. 

                """)
            # Boxplot for DPD variables
            fig = plt.figure(figsize=(10,4))
            numerical[pdp_variables].boxplot()
            st.pyplot(fig)
            st.markdown("""

            __Interpretation:__

            The spread of outliers, as seen in the boxplot above, appears to be difficult to manage, and \
            the interquartile range is not observable, making the Box Transformation approach ineffective \
            since it produces misleading data points. We picked the logarithmic transformation since it \
            appears to be effective in reducing the impact of outliers.

            """)
            # The DPD variables logarithmic transformation scatterplot
            fig = sns.pairplot(numerical[pdp_variables].apply(lambda x: np.log(x)))
            st.pyplot(fig)
            st.markdown("""

                __Interpretation:__

                This confirms the strong correlation between the days past due (PDP) variables, which might \
                be beneficial during the preprocessing step and improve model performance.

                """)
        elif select == 'Categorical-Numerical':
            st.write('### Bivariate Analysis: Categorical & Numerical')
            st.write('In this part, we will look at the relationship between the dependent variable \
                "Delinquency" and the independent numerical variables. ')
            # Plotting a countplot for the target variable
            BivariatePlotting.target_plot(data, 'Delinquency')
            st.write('Most of the borrowers involved had not encountered significant delinquency in 2 years.')
            st.write('')
            st.write('')
            st.write('##### The effect of revolving utilizing an unsecured list of credit on serious delinquency in 2 years')
            # Plotting barplot, kdeplot, and boxplot of "Delinquency" vs. "RULOC" variables
            BivariatePlotting.Category_Numerical(data, 'Delinquency', 'RULOC', 1)
            st.markdown("""
                __Interpretation:__

                We can see from the illustrations above that the categorical distribution of kdeplot and boxplot \
                did not turn out as anticipated, and the illustrations are irrelevant. Furthermore, borrowers with \
                unsecured revolving credit are less likely to fall behind on their payments for 90 days or later.
                """)
            st.write('')
            st.write('')
            st.write('##### The effect of debt ratio on serious delinquency in 2 years')
            # Plotting barplot, kdeplot, and boxplot of "Delinquency" vs "DebtRatio" variables
            BivariatePlotting.Category_Numerical(data, 'Delinquency', 'DebtRatio', 1)
            st.markdown("""

                __Interpretation:__

                Related to the odd results of kdeplot and boxplot seen above, however, it appears that borrowers \
                with a high debt ratio are more likely to fall behind on their payments after 90 days, but those \
                with a low debt ratio are not. Even if the number of borrowers with low debt ratios is significantly \
                higher, the bar chart demonstrates that there are more borrowers with high debt ratios.

                """)
        elif select == 'Categorical-Categorical':
            st.write('### Bivariate Analysis: Categorical & Categorical')
            st.write('In this section, we will look at the relationship between the dependent categorical \
                variable "delinquency" and the independent categorical variables. In addition, we will use \
                the chi-square test to examine our hypotheses. When you have two categorical variables from \
                a population group, the Chi-Square Test is used. It is used to see if the two variables have \
                a statistically significant relationship.')
            st.write('')
            st.markdown("""

                ##### The respondent experienced serious delinquency in 2 years according to qualified ages of \
                borrowers

                For the age group, the following would be appropriate:

                1. For `Young` would be a person under the age of 18.
                2. For `Adult` would be a person aged between 18 and 59.
                3. For `Senior Citizen` would be a person aged between 60 and 79.
                4. For `Very Old` would be a person aged 80 or older.

                For the sake of data analysis, we would check to see if a youthful group exists, despite the fact \
                that we already know they don't qualify to borrow or be a borrower.

                """)
            st.write('')
            # Categorizing borrowers based on their age 
            deli_age = Data.age_group(data, 'Delinquency', 'Age')
            # Countplot plotting and hypothesis conclusion of delinquency and age group
            BivariatePlotting.Category_Category(deli_age, 'Delinquency', 'age_group')
            st.write('')
            st.markdown("""

                __Interpretation:__

                - __Young:__ It shows that there are no borrowers since minors are not eligible. But, just to be \
                sure, we would double-check.
                - __Adult:__ Because there is so much going on in the adulting age group that necessitates finances, \
                the rate of borrowers encountering delinquency is expected to be greater than in other age groups.
                - __Senior Citizen:__ Few borrowers will default, and assuming that some will receive a pension, the \
                credit will be covered or fully paid.
                - __Very Old:__ There will be no delinquency among borrowers of that age.

                """)
            st.write('')
            st.markdown("""

                ##### The respondent experienced serious delinquency in 2 years according to the borrower's monthly \
                income classes

                The following are the monthly income classes:

                1. Lower income
                2. Middle income
                3. Upper income

                We will not be evaluating the income classes using the country's economic class structure. \
                The 25th percentile of the box portion from the box plot, which is delineated by two lines at \
                the 25th and 75th percentiles, will be used. The value at which 25% of the data values are below \
                this number is known as the 25th percentile. As a result, the center half of the data values lies \
                between the 25th and 75th percentiles.

                The `lower income` range is less than the 25th percentile income, the `middle income` range is between \
                the 25th and 75th percentile income, and the `higher income` range is more than the 75th percentile \
                income.

                """)
            st.write('')
            # Categorizing borrowers into monthly income classes
            deli_income = Data.income_class(data, 'Delinquency', 'MonthlyIncome')
            # Countplot plotting and hypothesis conclusion of delinquency and monthly income classes
            BivariatePlotting.Category_Category(deli_income, 'Delinquency', 'income_class')
            st.write('')
            st.markdown("""

                __Interpretation:__

                In the above plot, we can see that the chances of delinquency are low among upper-income borrowers, \
                implying that the majority of borrowers are able to repay or cover the credit, followed by lower-income \
                borrowers, implying that they have access to or qualify for specific credit with specific credit limits. \
                Even though middle-income borrowers have access to most or all credit, a large percentage of borrowers \
                experience delinquency.

                """)
            st.write('')
            st.markdown("""

                ##### The respondent serious delinquency in 2 years according to the borrower's number of dependents

                The following would be the dependent category:

                1. Single
                2. Small family
                3. Large family
                4. Joint family

                """)
            st.write('')
            # Grouping borrowers into categories based on their dependents 
            deli_dep = Data.dep_group(data, 'Delinquency', 'Dependents')
            # Countplot plotting and hypothesis conclusion of delinquency and dependent group
            BivariatePlotting.Category_Category(deli_dep, 'Delinquency', 'dep_group')
            st.write('')
            st.markdown("""

                __Interpretation:__

                In the plot above, we can see that small families have a higher percentage of borrowers missing \
                payments or being delinquent, assuming or implying that they have a lot of responsibilities and no \
                other monthly income, followed by single people, who may be doing a lot of things at once in their \
                lives, resulting in a lot of credit accounts. Large families tend to have a limited number of borrowers, \
                resulting in a low delinquency rate, while joint families have a small number of borrowers.

                """)

    elif options == 'Model Evaluation':
        select = st.sidebar.selectbox('Model type', ['Logistic Regression', 'Decision Tree Classifier'])
        st.write('## Model Evaluation') 
        st.write("A confusion matrix is a table that is used to measure a classification model's \
            performance. An algorithm's performance can also be seen. The number of right and wrong \
            guesses are totaled class-by-class in a confusion matrix. ")

        if select == 'Logistic Regression':
            # Create an instance of the model (using the default parameters)
            logreg = LogisticRegression()
            # Fit the model with data
            logreg.fit(X_train,y_train)
            # Generate prediction
            logreg_prediction = logreg.predict(X_test)

            # Generating a confusion matrix
            cf_matrix = metrics.confusion_matrix(y_test, logreg_prediction)
            # Define labels and categories
            labels = ['True Negative','False Positive','False Negative','True Positive']
            categories = ['non-delinquency', 'delinquency'] # Equivalent to [0, 1]

            # Using a Heatmap to visualize the Confusion Matrix
            Visualize.confusion_matrix(cf_matrix, labels, categories)
            st.write('')
            st.write('#### Confusion Matrix Evaluation Metrics')
            st.write("Let's evaluate the model using model evaluation metrics such \
                as accuracy, precision, and recall.")

            # Display model performance
            df = pd.DataFrame({'Metrics':['Accuracy','Precision','Recall'],
                'Performance':[metrics.accuracy_score(y_test, logreg_prediction),
                metrics.precision_score(y_test, logreg_prediction),
                metrics.recall_score(y_test, logreg_prediction)]})
            st.table(df)

            st.write('__Accuracy:__ A classification rate of 93% is considered good accuracy.')
            st.write('__Precision:__ When a Logistic Regression model predicts that borrowers \
                will experience financial distress in the next two years, borrowers have \
                58% of the time.')
            st.write('__Recall:__ The Logistic Regression model can identify borrowers in \
                financial distress 0.9% of the time if the test set contains them.')
            st.write('')
            # Plotting ROC Curve
            st.write('#### ROC Curve')
            st.write("The true positive rate vs. the false positive rate is plotted on the \
                Receiver Operating Characteristic (ROC) curve. It demonstrates the sensitivity \
                vs. specificity tradeoff. The Area Under the Curve (AUC) is a summary of the \
                ROC curve that measures a classifier's ability to distinguish between classes. \
                The AUC indicates how well the model distinguishes between positive and negative \
                classes. The higher the AUC, the better.")
            st.write('')
            Visualize.roc_curve(logreg, X_test, y_test)
            st.write('')
            st.markdown("""

                The area under the ROC curve (AUC) results were considered:

                - `Excellent` for AUC values between 0.9-1.
                - `Good` for AUC values between 0.8-0.9.
                - `Fair` for AUC values between 0.7-0.8.
                - `Poor` for AUC values between 0.6-0.7.
                - `Failed` for AUC values between 0.5-0.6.

                """)
            st.write('')
            st.write('We conclude that the AUC score for the case is 0.66. An AUC score represents a \
                poor classifier.')

        elif select == 'Decision Tree Classifier':
            # Create Decision Tree classifier object
            clf = DecisionTreeClassifier()
            # Train Decision Tree Classifier
            clf = clf.fit(X_train,y_train)
            # Predict the response for test dataset
            clf_prediction = clf.predict(X_test)

            # Generating a confusion matrix
            cf_matrix = metrics.confusion_matrix(y_test, clf_prediction)
            # Define labels and categories
            labels = ['True Negative','False Positive','False Negative','True Positive']
            categories = ['non-delinquency', 'delinquency'] # Equivalent to [0, 1]

            # Using a Heatmap to visualize the Confusion Matrix
            Visualize.confusion_matrix(cf_matrix, labels, categories)
            st.write('')
            # Display model performance
            df = pd.DataFrame({'Metrics':['Accuracy','Precision','Recall'],
                'Performance':[metrics.accuracy_score(y_test, clf_prediction),
                metrics.precision_score(y_test, clf_prediction),
                metrics.recall_score(y_test, clf_prediction)]})
            st.table(df)

            st.write('__Accuracy:__ A classification rate of 89% is considered good accuracy.')
            st.write('__Precision:__ When a Logistic Regression model predicts that borrowers \
                will experience financial distress in the next two years, borrowers have \
                25% of the time.')
            st.write('__Recall:__ The Logistic Regression model can identify borrowers in \
                financial distress 29% of the time if the test set contains them.')
            st.write('')
            # Plotting ROC Curve
            st.write('#### ROC Curve')
            st.write("The true positive rate vs. the false positive rate is plotted on the \
                Receiver Operating Characteristic (ROC) curve. It demonstrates the sensitivity \
                vs. specificity tradeoff. The Area Under the Curve (AUC) is a summary of the \
                ROC curve that measures a classifier's ability to distinguish between classes. \
                The AUC indicates how well the model distinguishes between positive and negative \
                classes. The higher the AUC, the better.")
            st.write('')
            Visualize.roc_curve(clf, X_test, y_test)
            st.write('')
            st.markdown("""

                The area under the ROC curve (AUC) results were considered:

                - `Excellent` for AUC values between 0.9-1.
                - `Good` for AUC values between 0.8-0.9.
                - `Fair` for AUC values between 0.7-0.8.
                - `Poor` for AUC values between 0.6-0.7.
                - `Failed` for AUC values between 0.5-0.6.

                """)
            st.write('')
            st.write('We conclude that the AUC score for the case is 0.61. An AUC score represents a \
                poor classifier.')