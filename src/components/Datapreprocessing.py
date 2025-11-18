import pandas as pd
import os
import numpy as np

class Data_Preprocessing:
    def __init__(self, input_path='Data/Raw/raw_data.xlsx', output_path='Data/Process'):
        self.input_path = input_path
        self.output_path = output_path
    
    def preprocess(self):
        print('\n Entering the preprocess function for processing the data...')
        
        df = pd.read_excel(self.input_path)
        # The columns that have missing more than 79%
        df = df.drop(['CC_utilization', 'PL_utilization', 'time_since_recent_deliquency', 'max_delinquency_level', 'time_since_first_deliquency'], axis=1)
        
        # The column in final dataset that have missing values
        missing_percentage = (df[df == -99999].count() / len(df)) * 100

        # Get columns that have missing values
        missing_columns = missing_percentage[missing_percentage > 0].index
        
        df.replace(-99999, np.nan, inplace=True)
        
        # Filing the numeric columns with the mean
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

        # Fill missing values in numeric columns with mean
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        
        os.makedirs(self.output_path, exist_ok=True)
        
        save_preprocess_data_path = os.path.join(self.output_path, 'preprocess_data_version1.xlsx')
        
        df.to_excel(save_preprocess_data_path, index=False)
        
        print('Done saving preprocess data')
        
if __name__ =='__main__':
    dp = Data_Preprocessing()
    dp.preprocess()
        