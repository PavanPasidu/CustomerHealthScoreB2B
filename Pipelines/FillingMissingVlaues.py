class FillingMissingValues:
    def __init__(self,df):
        self.df =  df

    # Filling missing values of encoded_product_impact,encoded_responsiveness,encoded_satisfaction with mode,median

    # function to fill missing values with mode, excluding multiple modes
    def fill_missing(self,group):
        for col in group[['encoded_satisfaction', 'encoded_responsiveness',
        'encoded_product_impact']].columns:  
            mode_values = group[col].mode()
            median_values = group[col].median()
            
            if len(mode_values) == 1:                               # Only fill if there's a single mode
                group[col] = group[col].fillna(mode_values[0])
            elif len(mode_values)==2 and col!='encoded_product_impact':
                group[col] = group[col].fillna(mode_values.mean())
            elif len(mode_values)>=3 and col!='encoded_product_impact':
                group[col] = group[col].fillna(mode_values.median())
            else:
                if col!='encoded_product_impact':
                    group[col] = group[col].fillna(median_values)   
        return group

    # Apply the function to each group
    def getFilledDataset(self):
        filled_df = self.df.groupby('Account Name').apply(self.fill_missing).reset_index(drop=True)
        filled_df = filled_df.fillna(-1)
        return filled_df