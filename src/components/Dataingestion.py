import pandas as pd
import os

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
            return "Error while reading dataset ",(e)
            
    def save_data(self, df1, df2):
        try: 
            print("Entering the dave_data function to save the data...")
                
            # Merging the two input datasets
            df = pd.merge(df1, df2, how='inner', on='PROSPECTID')
            
            print("Done merging")
            os.makedirs(self.output_path, exist_ok=True)
            save_raw_data_path = os.path.join(self.output_path, 'raw_data.xlsx')
            df.to_excel(save_raw_data_path, index=False)
                
            print(f"The data is saved sucessfully.")
            
        except Exception as e: 
                
            print(f"Error: {str(e)}")
            return None, None

if __name__ == "__main__":
    di = Dataingestion()
    df1,df2 = di.read_data()
    di.save_data(df1, df2)        
                        