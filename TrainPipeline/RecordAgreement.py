# calculate the agreement of duplicate responses
import krippendorff as kd
import pandas as pd


'''
Here in Fleiss Kappa and Krippendorff's alpha what we are doing is if we have multiple raters in our scenario multiple responders,
we measure the agreement between multiple responses.

'''
''' 
If we remove low agreement records we might loose lots of data records
But in this dataset(nps-survey 2023) most of records have atleast average agreement between multiple responds
'''



class RecordAgreement:

    def __init__(self, df):
        self.df = df

    # Funtion to get survey list of encoded df
    def getencodedSURVEYS(self,df):
        encoded_surveys =[]
        survey_dates = list(df['Survey Campaign'].unique())

        for date in survey_dates:
            d1 = df[(df['Survey Campaign'] == date)]
            encoded_surveys.append(d1)
        return encoded_surveys



    # Function to get Kippendorff Alpha Values
    def getKippendroffAlphaValues(self):
        Krippendorff_dic    = dict()                           # dictionary to store Krippendorff's alpha values
        index               = 2022
        encoded_surveys     = self.getencodedSURVEYS(self.df)    # get the encoded surveys        

        for survey in encoded_surveys:                                                                         # add survey no as key
            accs                = survey['Account Name']
            duplicated_acc_list = list(survey[accs.isin(accs[accs.duplicated()])]['Account Name'].to_list())   # get names of account names which are duplicated
            temp_dic            = dict()
            
            
            for account in set(duplicated_acc_list):
                df = survey[(survey['Account Name']==account)][['likely_to_recomend','encoded_satisfaction','encoded_responsiveness']]
                df = df.fillna(-1)

                if len(df)==0:continue
                table               = df.values.tolist()
                Krippendorff        = kd.alpha(table,level_of_measurement='ordinal')          # calculating Krippendorff's alpha
                temp_dic[account]   = Krippendorff                                            # add Krippendorff to tempary dict
            
            Krippendorff_dic[index] = temp_dic                                                # assign Krippendorff alpha of accounts in each survey
            index+=1 
        return Krippendorff_dic,encoded_surveys  
    
    
    # Function to get records with high agreement levels                                
    def gethighAgreementSurveys(self):

        Krippendorff_dic,encoded_surveys = self.getKippendroffAlphaValues()

        keys = Krippendorff_dic.keys()
        high_agreement_surveys = []
        for key,survey in zip(keys,encoded_surveys):
            k_values        = Krippendorff_dic[key].values()       # getting Krippendorff alpha values of each multi responses
            k_account       =    Krippendorff_dic[key].keys()     # getting country of each multi responses
            for k,acc in zip(k_values,k_account):
                if k<0.6:
                    duplicates = survey[(survey['Account Name']==acc)]
                    survey = survey.drop(survey[(survey['Account Name']==acc)].index)           # drop low agreement response
            high_agreement_surveys.append(survey)

        # concat the surveys 
        merged_surveys = high_agreement_surveys[0]
        for id in range(1,len(high_agreement_surveys)):
            merged_surveys = pd.concat([merged_surveys,high_agreement_surveys[id]] , axis=0)

        return merged_surveys
