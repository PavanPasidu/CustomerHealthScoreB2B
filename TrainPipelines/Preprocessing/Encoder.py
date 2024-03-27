import numpy as np

class Encoder:
    def __init__(self,df):
        self.df  = df

    def adjustingDataset(self):
        nps = self.df

        # change feature names for ease of use
        header_map = {
            "How likely are you to recommend WSO2 to a friend_ or colleague on a scale from 0 to 10? [0 being not at all likely and 10 being extremely likely]":'likely_to_recomend',
            "How satisfied are you with the support given by the WSO2 team?":'satisfaction',
            "Which response best captures the main impact of our product?":'product_impact',
            "How responsive have we been to your questions or concerns about our products?":'responsiveness'
        }
        nps.rename(columns=header_map,inplace=True)


        # drop the columns that have many null values
        temp_d1 = nps[['Account Name', 'Account Manager Name', 'UserName',
                'UserID', 'ResponseID',  'timeStamp',
            'dateTime',  'country',  'completion',
            'likely_to_recomend',
            'satisfaction',
            'responsiveness',
            'product_impact',
            'Sales Region', 'Sub Region', 'Survey Campaign', 'Segment']]


        # Filling missing values in Sales Region
        temp_d2 = temp_d1
        RegionMAP = np.load('./Data/Region_Map.npy',allow_pickle='TRUE').item()           # Region Map
        temp_d2['Sales Region'] = temp_d2['Sales Region'].fillna(temp_d2['Sub Region'].map(RegionMAP))
        return temp_d2


    # encode dataset
    def customEncoder(self):
        d1      =   self.df

        # ordinal encoding on features
        encoder_map_satisfaction    = {"Excellent":5,"Good":4,"Okay":3,"Bad":2,"Terrible":1}
        encoder_map_response        = {"Excellent":4,"Good":3,"OK":2,"Slow":1}
        encoder_map_impact          = {"Many of the above":9,"High Quality":8,"Scalable":7,"Value for Money":6,"Useful":5,"Reliable":4,"Secure":3,"Unique":2,"None of the above":1}

        # --- satisfaction ----
        d1['encoded_satisfaction']  = d1.satisfaction.map(encoder_map_satisfaction)
        d1                          = d1.drop(['satisfaction'],axis=1)

        # --- responsiveness ---
        d1['encoded_responsiveness'] = d1.responsiveness.map(encoder_map_response)
        d1                           = d1.drop(['responsiveness'],axis=1)

        # --- product_impact ----
        d1['encoded_product_impact'] = d1.product_impact.map(encoder_map_impact)
        d1                           = d1.drop(['product_impact'],axis=1)
        return d1