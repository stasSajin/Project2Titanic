#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier
import numpy as np
import pandas as pd

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list= ['poi','salary',
 'deferral_payments',
 'total_payments',
 'exercised_stock_options',
 'bonus',
 'restricted_stock',
 'restricted_stock_deferred',
 'total_stock_value',
 'expenses',
 'loan_advances',
 'other',
 'director_fees',
 'deferred_income',
 'long_term_incentive',
 'missingFinancial',
 'stockTotalPaymentRatio']

financial_features = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 
                      'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
                      'exercised_stock_options', 'other', 
                      'long_term_incentive', 'restricted_stock', 'director_fees']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
df = pd.DataFrame.from_dict(data_dict, orient='index')

### Task 2: Remove outliers
#drop TOTAL and THE TRAVEL AGENCY IN THE PARK
df = df.drop(['TOTAL', 'THE TRAVEL AGENCY IN THE PARK'])

#Correct the values for BELFER ROBERT and BHATNAGAR SANJAY using the numbers from enron61702insiderpay.pdf
#BELFER ROBERT
df.set_value('BELFER ROBERT', 'salary', 'NaN')
df.set_value('BELFER ROBERT', 'bonus', 'NaN')
df.set_value('BELFER ROBERT', 'total_payments', 3285)
df.set_value('BELFER ROBERT', 'exercised_stock_options', 'NaN')
df.set_value('BELFER ROBERT', 'restricted_stock', 44093)
df.set_value('BELFER ROBERT', 'restricted_stock_deferred', -44093)
df.set_value('BELFER ROBERT', 'total_stock_value', 'NaN')
df.set_value('BELFER ROBERT', 'other', 'NaN')
df.set_value('BELFER ROBERT', 'director_fees', 102500)
df.set_value('BELFER ROBERT', 'deferred_income', -102500)
df.set_value('BELFER ROBERT', 'long_term_incentive', 'NaN')

#BHATNAGAR SANJAY
df.set_value('BHATNAGAR SANJAY', 'salary', 'NaN')
df.set_value('BHATNAGAR SANJAY', 'bonus', 'NaN')
df.set_value('BHATNAGAR SANJAY', 'total_payments', 137864)
df.set_value('BHATNAGAR SANJAY', 'exercised_stock_options', 15456290)
df.set_value('BHATNAGAR SANJAY', 'restricted_stock', 2604490)
df.set_value('BHATNAGAR SANJAY', 'restricted_stock_deferred', -2604490)
df.set_value('BHATNAGAR SANJAY', 'total_stock_value', 15456290)
df.set_value('BHATNAGAR SANJAY', 'other', 'NaN')
df.set_value('BHATNAGAR SANJAY', 'director_fees', 'NaN')
df.set_value('BHATNAGAR SANJAY', 'deferred_income',  'NaN')
df.set_value('BHATNAGAR SANJAY', 'long_term_incentive', 'NaN')
df.set_value('BHATNAGAR SANJAY', 'expenses', 137864)

#Identify NaN
df = df.replace('NaN', np.nan)

### Task 3: Create new feature(s)
#find the proportion of financial features that are missing for each person
missingFinancial=df[financial_features].isnull().sum(axis=1)/14

#add missingFinancial to the original dataframe
df['missingFinancial']= missingFinancial.astype(float)

#first, fill out the missing values in financial features with 0
df[financial_features] = df[financial_features].fillna(0)

#create ratio between exercised_stock_options and total_compensation
df['stockTotalPaymentRatio'] = df['exercised_stock_options']/(df['total_payments']+df['exercised_stock_options'])

#there are some inf values because some individuals did not have any compensation except for their stock options. It is very 
#likely that these individuals are not as involved inside the organization, so I will replace the inf values with 0. 
df=df.replace([np.inf], np.nan)
df.loc[df['stockTotalPaymentRatio'].isnull()] = 0



### Store to my_dataset for easy export below.
my_dataset = df.to_dict('index')


### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

#See the classifiers that have been tried in the python notebook.


### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import cross_val_score, StratifiedShuffleSplit
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import AdaBoostClassifier

clf=Pipeline(steps=[('minmaxer', MinMaxScaler(copy=True, feature_range=(0, 1))),
                    ('model', AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None, learning_rate=1,
          n_estimators=50, random_state=42))])

test_classifier(clf, my_dataset, features_list)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)