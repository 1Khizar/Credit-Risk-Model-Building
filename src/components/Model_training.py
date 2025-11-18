from sklearn.ensemble  import RandomForestClassifier
from src.utils import load_obj, save_obj
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import pandas as pd

class Model_Training:
    def __init__(self, train_data_path='Data/Process/train_preprocess_data.xlsx', test_data_path='Data/Process/test_preprocess_data.xlsx', model_save_path='src/models'):
        self.train_data_path=train_data_path
        self.test_data_path=test_data_path
        self.model_save_path=model_save_path
    
    def model_training(self):
        print('Entering the model training function...')
        train_data = pd.read_excel(self.train_data_path)
        test_data = pd.read_excel(self.test_data_path)
        
        preprocessor = load_obj("src/models/preprocessor.pkl")
        model_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])

        X_train = train_data.drop(['Approved_Flag'], axis=1)
        y_train = train_data['Approved_Flag']
        
        X_test = test_data.drop(['Approved_Flag'], axis=1)
        y_test = test_data['Approved_Flag']
        
        # Train model
        model = model_pipeline.fit(X_train, y_train)
        
        save_obj('src/models/model.pkl', model)
        print('Model is saved successfully.')
        
    
if __name__=='__main__':
    mt=Model_Training()
    mt.model_training()

        