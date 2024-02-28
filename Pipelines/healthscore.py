# import libraries
import pandas as pd
from sklearn import preprocessing 
import pickle

# get the input dataset
input = pd.read_csv('E:/Research/WebApp/input.csv')
input_data = input

# change the headers to ease of use
header_map = {
    "How likely are you to recommend WSO2 to a friend_ or colleague on a scale from 0 to 10? [0 being not at all likely and 10 being extremely likely]":'likely_to_recomend',
    "How satisfied are you with the support given by the WSO2 team?":'satisfaction',
    "Which response best captures the main impact of our product?":'product_impact',
    "How responsive have we been to your questions or concerns about our products?":'responsiveness'
}
input_data.rename(columns=header_map,inplace=True)

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

# # one-hot encoding for string values
# encoded_new_d = pd.get_dummies(input_data,columns=['encoded_product_impact'],dtype=int)
# input_data = encoded_new_d

# label encoding for categorical features
features = ['Sub Region','Account Name','Account Manager Name','Segment','Sales Region','completion']
label_encoder = preprocessing.LabelEncoder() 
for feature in features:
    input_data[feature] = label_encoder.fit_transform(input_data[feature])

# inference
X = input_data[['completion', 'Sales Region', 'Sub Region', 'Account Manager Name','Segment', 'encoded_product_impact']]
X.dropna(inplace=True)

# load the model
filename = 'E:\Research\Models/GradientBoostingRegressorModel2.pkl'
model = pickle.load(open(filename, 'rb'))

# predict 
y = model.predict(X)

# assign health score to dataset 
healthscore_dataset = input_data[['ResponseID','completion', 'Sales Region', 'Sub Region', 'Account Manager Name','Segment', 'encoded_product_impact']]
healthscore_dataset.dropna(inplace=True)
healthscore_dataset['Health_Score'] = y

# save dataset with health
d1 = input[['ResponseID','Account Name','Account Manager Name','Sales Region','ARR','dateTime']]
d2 = healthscore_dataset[['ResponseID','Health_Score']]

final_dataset = pd.merge(d2,d1,how='right',on='ResponseID')

print(final_dataset)