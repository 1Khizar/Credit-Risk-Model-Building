from sklearn.ensemble  import RandomForestClassifier
from src.utils import load_obj, save_obj
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pandas as pd
import mlflow
import dagshub
from urllib.parse import urlparse
# dagshub.init(repo_owner='1Khizar', repo_name='Credit-Risk-Model-Building', mlflow=True)
# mlflow.set_tracking_uri('https://dagshub.com/1Khizar/Credit-Risk-Model-Building.mlflow')
# mlflow.set_registry_uri("https://dagshub.com/1Khizar/Credit-Risk-Model-Building.mlflow")


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
        
        y_pred= model.predict(X_test)
        
        accuracy= accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        save_obj('src/models/model.pkl', model)
        print('Model is saved successfully.')
        
        # try:
        #     tracking_url_type_store=urlparse(mlflow.get_tracking_uri()).scheme
        #     with mlflow.start_run(run_name='Random_Forest_Model'):
        #         print("Logging metrics, parameters, artifacts, and model to MLflow...")   
            
        #         if tracking_url_type_store != "file":
        #             mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name='Random_Forest')
        #         else:
        #             mlflow.sklearn.log_model(model, artifact_path="model")
        #         # Log Model Parameters
        #         mlflow.log_param("n_estimators", 100)
        #         mlflow.log_param("random_state", 42)
        #         mlflow.log_param("model_type", "RandomForestClassifier")
                
        #         #log metrics
        #         mlflow.log_metric('accuracy', accuracy)
                
        #         # Save and log classification report
        #         with open("classification_report.txt", "w") as f:
        #             f.write(report)
        #         mlflow.log_artifact("classification_report.txt")
                
        #         # Save and log confusion matrix
        #         conf_df = pd.DataFrame(conf_matrix)
        #         conf_df.to_csv("confusion_matrix.csv", index=False)
        #         mlflow.log_artifact("confusion_matrix.csv")
                            
        #         # Register Model in MLflow Model Registry
        #         # mlflow.sklearn.log_model(model, artifact_path="models")
        #         print("Model successfully registered in MLflow Model Registry.")
        # except Exception as e:
        #     print('Error: ',str(e))
    
if __name__=='__main__':
    mt=Model_Training()
    mt.model_training()

        