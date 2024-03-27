######### calculate the label   ############

class Labeling:
    def __init__(self,df):
        self.df = df


    def returnLabeleddf(self):
        df              = self.df
        labelFields     = df[['likely_to_recomend','encoded_satisfaction', 'encoded_responsiveness']]        # Get required fields
        weights         = [100,10,10]

        # Scale the field values
        for col,w in zip(labelFields.columns,weights):
            labelFields[col] =  labelFields[col]*w/(labelFields[col].max() - labelFields[col].min())
        likely_to_recomend  =   labelFields['likely_to_recomend']
        satisfaction        =   labelFields['encoded_satisfaction']
        responsiveness      =   labelFields['encoded_responsiveness']

        df['healthScore'] = likely_to_recomend - ( (satisfaction.max()  -  satisfaction ) +( responsiveness.max()  -  responsiveness) )
        return df