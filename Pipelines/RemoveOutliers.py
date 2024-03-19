class RemoveOutliers:
    def __init__(self,df):
        self.df = df

    # Define function to filter records based on likelihood to recommend mode
    def filter_records(self,group):
        mode = group['likely_to_recomend'].mode()
        median = group['likely_to_recomend'].median()
        if len(mode) == 1:  
            group['diff_to_mode'] = abs(group['likely_to_recomend'] - mode[0])
            return group[group['diff_to_mode'] <= 5]
        else:
            group['diff_to_mode'] = abs(group['likely_to_recomend'] - median)
            return group[group['diff_to_mode'] <= 5]


    # Function to remove outliers
    def removeOutliers(self):
        filtered_df = self.df.groupby('Account Name').apply(self.filter_records)   # Apply the function to each group
        filtered_df = filtered_df.drop(columns=['diff_to_mode']).reset_index(drop=True)     # Remove extra columns
        return filtered_df