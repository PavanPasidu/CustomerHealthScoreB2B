# import libraries
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# get the input dataset
input_data = pd.read_csv('E:/Research/WebApp/input.csv')

# load the model
rfc = joblib.load('E:/Research/Models/Classifiers/random_forest_classifier_model.pkl')

# change the headers to ease of use
header_map = {
    "How likely are you to recommend WSO2 to a friend_ or colleague on a scale from 0 to 10? [0 being not at all likely and 10 being extremely likely]":'likely_to_recomend',
    "How satisfied are you with the support given by the WSO2 team?":'satisfaction',
    "Which response best captures the main impact of our product?":'product_impact',
    "How responsive have we been to your questions or concerns about our products?":'responsiveness'
}
input_data.rename(columns=header_map,inplace=True)

# select the necessary features
input_data = input_data[['ResponseID','likely_to_recomend','satisfaction','responsiveness','product_impact','Account Name','Sales Region']]
input_data.dropna(inplace=True)

# ordinal encoding on features
h1_map = {"Excellent":5,"Good":4,"Okay":3,"Bad":2,"Terrible":1}
h2_map = {"Excellent":4,"Good":3,"OK":2,"Slow":1}
h3_map = {"Many of the above":9,"High Quality":8,"Scalable":7,"Value for Money":6,"Useful":5,"Reliable":4,"Secure":3,"Unique":2,"None of the above":1}
# --- satisfaction ----
input_data['encoded_satisfaction'] = input_data.satisfaction.map(h1_map)
input_data = input_data.drop(['satisfaction'],axis=1)
# --- responsiveness ---
input_data['encoded_responsiveness'] = input_data.responsiveness.map(h2_map)
input_data = input_data.drop(['responsiveness'],axis=1)
# --- product_impact ----
input_data['encoded_product_impact'] = input_data.product_impact.map(h3_map)
input_data = input_data.drop(['product_impact'],axis=1)

# one-hot encoding for string values
encoded_new_d = pd.get_dummies(input_data,columns=['encoded_product_impact'],dtype=int)
input_data = encoded_new_d

# prediction
input = input_data.drop(['ResponseID','Account Name','Sales Region'],axis=1)
y_pred = rfc.predict(input)

# assign prediction to dataset
input_data['-        Health        -'] = y_pred 

print(input_data)