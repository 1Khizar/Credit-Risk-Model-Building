import pandas as pd

from src.components.Dataingestion import Dataingestion
from src.components.Datapreprocessing import Data_Preprocessing
from src.components.Feature_engineering import Feature_Engineering
from src.components.Data_transformation import Data_Transformation
from src.components.Model_training import Model_Training

di = Dataingestion()
df1,df2 = di.read_data()
di.save_data(df1, df2)

dp = Data_Preprocessing()
dp.preprocess()

fe = Feature_Engineering()
fe.feature_engineering()
    
dt = Data_Transformation()
dt.transformation()

mt=Model_Training()
mt.model_training()

