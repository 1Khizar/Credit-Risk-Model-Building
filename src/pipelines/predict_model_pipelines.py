from src.utils import load_obj
import pandas as pd

class Predict_Pipeline:
    def __init__(self, model_path='src/models/model.pkl', label_encoder="src/models/label_encoder.pkl"):
        self.model_path = model_path
        self.label_encoder=label_encoder
    
    def predict(self, input_data):
        
        model = load_obj(self.model_path)
        label_encoder = load_obj(self.label_encoder)
        
        y_pred = model.predict(input_data)
        
        y_pred_decoded = label_encoder.inverse_transform(y_pred)
        
        print('Prediction: ', y_pred_decoded)
        
        return y_pred_decoded

if __name__ == "__main__":
    import pandas as pd
    
    # Each key is a column name; values are lists for each row
    input_data = pd.DataFrame({
        'Total_TL': [5],
        'Tot_Closed_TL': [2],
        'Tot_Active_TL': [3],
        'pct_tl_open_L6M': [0.2],
        'pct_closed_tl': [0.4],
        'pct_tl_open_L12M': [0.3],
        'pct_active_tl': [0.6],
        'Home_TL': [1],
        'Age_Oldest_TL': [10],
        'Other_TL': [0],
        'Secured_TL': [1],
        'enq_L3m': [1],
        'PL_enq_L6m': [0],
        'num_std': [0.5],
        'num_std_12mts': [0.4],
        'num_std_6mts': [0.3],
        'AGE': [35],
        'CC_enq_L6m': [1],
        'PL_enq': [0],
        'CC_enq_L12m': [2],
        'tot_enq': [3],
        'PL_enq_L12m': [1],
        'enq_L12m': [2],
        'time_since_recent_enq': [12],
        'enq_L6m': [1],
        'pct_of_active_TLs_ever': [0.5],
        'pct_PL_enq_L6m_of_ever': [0.2],
        'Credit_Score': [700],
        'pct_PL_enq_L6m_of_L12m': [0.3],
        'pct_CC_enq_L6m_of_L12m': [0.1],
        'MARITALSTATUS': ['Single'],
        'EDUCATION': ['Graduate'],
        'last_prod_enq2': [0],
        'first_prod_enq2': [1]
    })
    
    pp = Predict_Pipeline()
    predictions = pp.predict(input_data)
    print(predictions)
