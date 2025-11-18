import pandas as pd
import numpy as np
import os
from sklearn.feature_selection import f_classif, chi2
from sklearn.preprocessing import LabelEncoder
        
class Feature_Engineering:
    def __init__(self, input_dataset_path='Data/Process/preprocess_data_version1.xlsx', output_path='Data/Process'):
        self.dataset_path = input_dataset_path
        self.output_path = output_path
                
        
    def feature_engineering(self):
        try:
            print('Entering the feature_engineering function...')
            
            df = pd.read_excel(self.dataset_path)
            
            # Separating the numerical and categorical columns
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()


            # --------------
            # ANNOVA testing
            # --------------
            
            y = df['Approved_Flag']
            X_num = df[numeric_cols]
            F_values, p_values = f_classif(X_num, y)

            anova_results = pd.DataFrame({
                'Feature': X_num.columns,
                'F_value': F_values,
                'p_value': p_values
                
            })

            # Keep numeric features with p-value < 0.05
            selected_numeric = (anova_results.sort_values('p_value').head(30)['Feature'].tolist())

            # -------------------
            # Chi-Square testing
            # -------------------

            # Feature selection for categorical columns (Chi-Square)
            X_cat = df[categorical_cols].copy()

            # Encoding categorical features and target
            le_target = LabelEncoder()
            y_encoded = le_target.fit_transform(y)

            for col in X_cat.columns:
                X_cat[col] = LabelEncoder().fit_transform(X_cat[col])

            chi_scores, p_values = chi2(X_cat, y_encoded)
            chi_results = pd.DataFrame({
                'Feature': X_cat.columns,
                'Chi2': chi_scores,
                'p_value': p_values
            })

            # Keep categorical features with p-value < 0.05
            selected_categorical = chi_results[chi_results['p_value'] < 0.05]['Feature'].tolist()
            if 'Approved_Flag' in selected_categorical:
                selected_categorical.remove('Approved_Flag')
            
            # ------------------------------------------------------
            # Selecting the best columns after applying the testing
            # ------------------------------------------------------

            # Combine selected features + target
            selected_features = selected_numeric + selected_categorical

            df = df[selected_features + ['Approved_Flag']]

            print("The dataset shape after feature engineering: ", df.shape)
            print('The columns in the dataset are : \n',df.columns)
            
            os.makedirs(self.output_path, exist_ok=True)
            output_save_path = os.path.join(self.output_path, 'preprocess_data_version2.xlsx')
            
            df.to_excel(output_save_path, index=False)
            print('Successfully saving the data after feature_engineering')
        except Exception as e:
            print(f'Error: {e}')    
        
if __name__=='__main__':
    fe = Feature_Engineering()
    fe.feature_engineering()       
                