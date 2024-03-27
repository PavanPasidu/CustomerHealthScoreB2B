# Get datasets 
import pandas as pd
import numpy as np
import Preprocessing.RecordAgreement as ra
import Preprocessing.RemoveOutliers as outlier
import Preprocessing.FillingMissingVlaues as fmv
import Preprocessing.Labeling as lb
import Preprocessing.Encoder as en
import warnings
import Constant as const
import Servicenow.GetServicenowData as snd
import Preprocessing.ConverttoCSV as csv
import Merging.MergingDatasets as mg
import ModelTrain.ModelTraining as mt
import pickle
import os

warnings.filterwarnings('ignore')
constant    =   const.Constant()
servicenow  =   snd.GetServicenowData(const=constant,url='https://wso2sndev.service-now.com/oauth_token.do')
csv         =   csv.ConverttoCSV(constant=constant,servicenow=servicenow)

filepath        = 'E:/Research/Datasets/WSO2/Healthscore_dataset'       # Replace this path with path/to/NPSsurvey.csv
nps             = pd.read_csv(filepath + '/NPS.csv')

caseData,accountData  = csv.getData()
print('\n',nps,'\n\n',caseData,'\n\n',accountData,'\n\n')

# Get encoded dataframe
adj     = en.Encoder(nps)
temp_d2 =  adj.adjustingDataset()
encode  = en.Encoder(temp_d2)
temp_d3 =   encode.customEncoder()


# Dropping duplicates
duplicateSUM = temp_d3.duplicated().sum()
if duplicateSUM!=0:
    temp_d3 = temp_d3.drop_duplicates()
else: None



# Now i need to measure consensus(agreement) between records of duplicate account name 
# Here I am using Krippendorff's alpha method
''' 
Here I am considering low agreement data records as outliers. Since I can not decide which record is the outlier from multiple responses
from single account, I am going to drop all the responses belongs to that account name.
'''

agreement       = ra.RecordAgreement(temp_d3)                             # create an object of RecordAgreement class
highAgreementdf =  agreement.gethighAgreementSurveys()                    # get dataset with reocrds which have high agreement between multiple responses



# Removing outliers
'''
Here I am considering differnce between mode and other values of likely to recommend us as the removing criteria of outliers.
'''
temp_df1    = highAgreementdf
outlierObj  =  outlier.RemoveOutliers(temp_df1)
filtered_df = outlierObj.removeOutliers()



# Filling missing values
temp_df2    = filtered_df
fm          = fmv.FillingMissingValues(temp_df2)
filled_df   = fm.getFilledDataset()



# Labeling nps dataset
labeling        =  lb.Labeling(filled_df)
labeledDataset  =  labeling.returnLabeleddf()
print('Maximum healthscore: ',labeledDataset['healthScore'].max(),'\nMinimum healthscore: ',labeledDataset['healthScore'].min())


# merging the datasets
merger          =   mg.MergingDatasets(nps=nps,caseData=caseData,accountData=accountData)
merged_dataset  =   merger.mergeDataset()

# Train a model
'''Here we asssume that this data does not have any missing values(Need to check this). And also all the data we give as input and output are float/int'''
modelObj       =   mt.ModelTraining(merged_dataset)
model          =    modelObj.modelTrain()

# Save the model
filename      = os.listdir('../Models/Version_New')
if len(filename)   ==1:
    version   = int(filename[0].split('_')[1])  + 1
    path      = '../Models/Version_New/customerhealthscoremodel_' + filename[0]
    os.remove(path)                                                                             # remove the existing file
elif len(filename) == 0:
    version   = 0
else:print('There can not be more than 1 file in this directory')


file_path_new = '../Models/Version_New/customerhealthscoremodel_' + str(version) + '_v' + '.pkl'    # save the new version
with open(file_path_new, 'wb') as f:
    pickle.dump((model), f)
file_path_old = '../Models/Version_Old/customerhealthscoremodel_' + str(version) + '_v' + '.pkl'    # All the older versions reside here
pickle.dump(model, open(file_path_old, 'wb'))


# re-assign the varibles with None
for var_name in dir():
    if not var_name.startswith('__'):  
        globals()[var_name] = None

print('\n\n\n',caseData,'\n\n\n',accountData)