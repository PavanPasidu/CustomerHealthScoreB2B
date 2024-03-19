# Get datasets
import pandas as pd
import numpy as np
import RecordAgreement as ra
import RemoveOutliers as outlier
import FillingMissingVlaues as fmv
import Labeling as lb
import Encoder as en
import warnings

warnings.filterwarnings('ignore')

filepath        = 'E:/Research/Datasets/WSO2/Healthscore_dataset'
nps             = pd.read_csv(filepath + '/NPS.csv')
caseDetails     = ''
accountDetails  = ''

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
