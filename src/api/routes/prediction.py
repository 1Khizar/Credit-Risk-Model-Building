from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import pandas as pd
from src.api.schema.dataschema import PredictionRequest
from src.pipelines.predict_model_pipelines import Predict_Pipeline
from src.api.database.database import SessionLocal, CreditRiskPrediction,Base, engine
app=FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done!")

@app.get("/")
def home():
    return "Welcome to Credit Risk Model Building:"

@app.post('/predict')
def predict(input_data:PredictionRequest, db: Session = Depends(get_db)):
    
    input_df=pd.DataFrame([input_data.dict()])
    pp = Predict_Pipeline()
    y_pred = pp.predict(input_df)[0]
    
    # Save to database
    db_prediction = CreditRiskPrediction(**input_data.dict(), prediction=y_pred)
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
   
    return {"prediction": y_pred, "id": db_prediction.id}
  