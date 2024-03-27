import pandas as pd


class MergingDatasets:
    def __init__(self,nps,caseData,accountData):
        self.caseData   =   caseData
        self.accountData=   accountData
        self.nps        =   nps


    def mergeDataset(self,start,end):
        account_n_case  =   pd.merge(self.caseData,self.accountData,how='left',left_on='account_name',right_on='name')

        # Getting chunks of dataset by created date of cases
        filtered_df     =   self.getChunkofData(df=account_n_case,start=start,end=end)

        # Combine them account wise 
        grouped_data    = filtered_df.groupby('Account Name').agg({
            'agent_reassignment_count': 'mean', 
            'time_to_resolve': 'mean',
            'reopen_count': 'mean',
            'is_fcr': lambda x: (x.sum() / filtered_df['is_fcr'].sum()) * 100, 
            'incorporated_on':'',
        })

        # Concatanate the combined data


    def getChunkofData(self,df,start='2022-02-01',end='2022-08-01'):
        # Convert the datetime column to datetime data type
        df['sys_created_on'] = pd.to_datetime(df['sys_created_on'], format='%m/%d/%Y %H:%M')

        # Define start date and end date
        start_date  = pd.to_datetime(start)
        end_date    = pd.to_datetime(end)

        # Filter the DataFrame based on start date and end date
        filtered_df = df[(df['sys_created_on'] >= start_date) & (df['sys_created_on'] <= end_date)]
        return filtered_df
    
    def getAccountwiseData(self):
        
        pass
    


