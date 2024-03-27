'''
Here I am using trained model and predict the healthscore.And 
also I will get sentiment value through an API and combine it
with healthscore. Combining sentiment to healthscore will be 
done dailybasis.

'''
import pandas as pd
import pickle
import warnings

from ..TrainPipelines.Constant import Constant as const
from ..TrainPipelines.Servicenow.GetServicenowData import GetServicenowData as snd
from ..TrainPipelines.Preprocessing.ConverttoCSV import ConverttoCSV as csv
from ..TrainPipelines.Merging.MergingDatasets import MergingDatasets as mg


# load the model
filename   = ''
filepath   = f'../Version_New/{filename}'
load_model = pickle.load(open(filepath, 'rb')) 

# load the dataset
warnings.filterwarnings('ignore')
constant    =   const.Constant()
servicenow  =   snd.GetServicenowData(const=constant,url='https://wso2sndev.service-now.com/oauth_token.do')
csv         =   csv.ConverttoCSV(constant=constant,servicenow=servicenow)

caseData,accountData  = csv.getData()

# preprocessing
caseData.dropna(inplace=True)
accountData.dropna(inplace=True)

# merging the datasets
merger            =   mg.MergingDatasets(nps='None',caseData=caseData,accountData=accountData)
_,merged_dataset  =   merger.mergeDataset()

# predicting healthscore
X_test = merged_dataset.drop([''],axis=1)
y_pred = load_model.predict(X_test) 

# Assign the healthscore to the dataset
merged_dataset['healthscore']  =  y_pred

# Save the dataset in Servicenow


'''Healthscore will change according to sentiment coming from sentiment model (throughout the 6 months).
   Once in six month healthscore will be overridden by runing this pipeline   
'''