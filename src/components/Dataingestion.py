import pandas as pd
import os
import sys

class Dataingestion:
    def __init__(self, input_dataset1_path='test_data/case_study1.xlsx', input_dataset2_path='test_data/case_study2.xlsx',output_path='Data/Raw'):
        
        self.input_dataset1_path = input_dataset1_path
        self.input_dataset2_path = input_dataset2_path
        self.output_path = output_path

    def read_data(self):
        try:
            print("Reading the dataset...")
                
            df1 = pd.read_excel(self.input_dataset1_path)
            df2 = pd.read_excel(self.input_dataset2_path)
                
            print("Done reading dataset")
                
            return df1, df2
            
        except Exception as e:
            print(f"Error while reading datasets: {e}")
            sys.exit(1)  # Stop execution in CI
            
    def save_data(self, df1, df2):
        try: 
            print("Entering the save_data function to save the data...")
                
            # Merging the two input datasets
            if not isinstance(df1, pd.DataFrame) or not isinstance(df2, pd.DataFrame):
                raise ValueError("Input data must be pandas DataFrames")
            
            # Check if merge column exists
            if 'PROSPECTID' not in df1.columns or 'PROSPECTID' not in df2.columns:
                raise KeyError("'PROSPECTID' column not found in input files")

            # Merge datasets
            df = pd.merge(df1, df2, how='inner', on='PROSPECTID')
            
            print("Done merging")
            
            os.makedirs(self.output_path, exist_ok=True)
            save_raw_data_path = os.path.join(self.output_path, 'raw_data.xlsx')
            df.to_excel(save_raw_data_path, index=False)
                
            print(f"The data is saved successfully at {save_raw_data_path}")
            
        except Exception as e: 
                
            print(f"Error while saving data: {e}")
            sys.exit(1)  # Stop execution in CI

if __name__ == "__main__":
    di = Dataingestion()
    df1,df2 = di.read_data()
    di.save_data(df1, df2)        
                        