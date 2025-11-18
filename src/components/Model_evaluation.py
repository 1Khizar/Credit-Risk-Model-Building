from src.utils import load_obj
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import os
import json
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import seaborn as sns
from sklearn.preprocessing import label_binarize

class Model_Evaluation:
    def __init__(self, model_file_path="src/models/model.pkl", test_data_path='Data/Process/test_preprocess_data.xlsx', result_dir="src/Results"):
        self.model_file_path=model_file_path
        self.test_data_path=test_data_path
        self.result_dir=result_dir
        
    def evaluation(self):
        print('Entering the model evalaution function...')
        model = load_obj(self.model_file_path)
        
        test_data = pd.read_excel(self.test_data_path)
        
        X_test = test_data.drop(['Approved_Flag'], axis=1)
        y_test = test_data['Approved_Flag']
        
        y_pred = model.predict(X_test)
                
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        conf_matrix = confusion_matrix(y_test, y_pred)
        
        os.makedirs(self.result_dir, exist_ok=True)
        
        # ----- Save Accuracy & Classification Report -----
        metrics_file = os.path.join(self.result_dir, 'metrics.json')
        metrics_data = {
            "accuracy": accuracy,
            "classification_report": report
        }
        with open(metrics_file, 'w') as f:
            json.dump(metrics_data, f, indent=4)
        print(f"Metrics saved to {metrics_file}")
        
        # ----- Save Confusion Matrix -----
        conf_matrix_file = os.path.join(self.result_dir, 'confusion_matrix.csv')
        pd.DataFrame(conf_matrix).to_csv(conf_matrix_file, index=False)
        print(f"Confusion matrix saved to {conf_matrix_file}")
        
        plt.figure(figsize=(6,5))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix')
        conf_matrix_img = os.path.join(self.result_dir, 'confusion_matrix.png')
        plt.savefig(conf_matrix_img)
        plt.close()
        print(f"Confusion matrix plot saved to {conf_matrix_img}")
        
        # Binarize labels
        y_test_bin = label_binarize(y_test, classes=[0,1,2,3])  # replace 0,1,2,3 with your actual categories
        n_classes = y_test_bin.shape[1]

        if hasattr(model, "predict_proba"):
            y_score = model.predict_proba(X_test)  # shape: (n_samples, n_classes)
            
            # ----- ROC Curve -----
            plt.figure()
            for i in range(n_classes):
                fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
                roc_auc = auc(fpr, tpr)
                plt.plot(fpr, tpr, label=f'Class {i} (AUC = {roc_auc:.2f})')
            plt.plot([0,1], [0,1], 'k--')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('Multi-class ROC Curve')
            plt.legend(loc='lower right')
            plt.savefig(os.path.join(self.result_dir, 'ROC_Curve.png'))
            plt.close()
            
            # ----- Precision-Recall Curve -----
            plt.figure()
            for i in range(n_classes):
                precision, recall, _ = precision_recall_curve(y_test_bin[:, i], y_score[:, i])
                plt.plot(recall, precision, label=f'Class {i}')
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title('Multi-class Precision-Recall Curve')
            plt.legend(loc='best')
            plt.savefig(os.path.join(self.result_dir, 'Precision_Recall_Curve.png'))
            plt.close()

        
        print("\nEvaluation Complete!")
        print(f"Accuracy: {accuracy:.4f}")
        
if __name__=="__main__":
    me=Model_Evaluation()
    me.evaluation()      
        
        
        