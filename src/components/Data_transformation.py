import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from src.utils import save_obj
import os
class Data_Transformation:
    def __init__(self, input_path='Data/Process/preprocess_data_version2.xlsx', output_path='Data/Process', train_data_path='Data/Process', test_data_path='Data/Process'):
        self.input_path = input_path
        self.output_path = output_path
        self.train_data_path = train_data_path
        self.test_data_path = test_data_path
    
    def transformation(self):
        try:
            print('\nEntering the transformation function...')
            df = pd.read_excel(self.input_path)
            
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

            # Remove target if inside categorical
            if 'Approved_Flag' in categorical_cols:
                categorical_cols.remove('Approved_Flag')
            
            numeric_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
            ])

            categorical_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown="ignore"))
            ])

            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numeric_pipeline, numeric_cols),
                    ('cat', categorical_pipeline, categorical_cols)]
            )
            
            
            # Saving the preprocessor
            save_obj('src/models/preprocessor.pkl', preprocessor)
            print('Preprocessor is saved.')
            
            train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)
            
            # --------------
            # Label encoding
            # --------------
            le = LabelEncoder()
                    
            train_data['Approved_Flag'] = le.fit_transform(train_data['Approved_Flag'])
            test_data['Approved_Flag'] = le.transform(test_data['Approved_Flag'])

            # Saving the label encoder 
            save_obj('src/models/label_encoder.pkl', le)
            print('Label encoder is saved.')
            
            os.makedirs(self.output_path, exist_ok=True)
            
            preprocess_data_path = os.path.join(self.output_path, 'final_preprocess_data.xlsx')
            df.to_excel(preprocess_data_path, index=False)
            print('The final preprocess data is saved.')
            
            preprocess_train_data_path = os.path.join(self.output_path, 'train_preprocess_data.xlsx')
            train_data.to_excel(preprocess_train_data_path, index=False)
            print('The train preprocess data is saved.')
            
            preprocess_test_data_path = os.path.join(self.output_path, 'test_preprocess_data.xlsx')
            test_data.to_excel(preprocess_test_data_path, index=False)
            print('The test preprocess data is saved.')
        except Exception as e:
            print(f'Error: {str(e)}')

if __name__ == '__main__':
    dt = Data_Transformation()
    dt.transformation()