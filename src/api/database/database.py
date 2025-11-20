from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
from sqlalchemy import Column, Integer, Float, String
from datetime import datetime

class CreditRiskPrediction(Base):
    __tablename__ = "credit_risk_predictions"

    id = Column(Integer, primary_key=True, index=True)
    Total_TL = Column(Integer)
    Tot_Closed_TL = Column(Integer)
    Tot_Active_TL = Column(Integer)
    pct_tl_open_L6M = Column(Float)
    pct_closed_tl = Column(Float)
    pct_tl_open_L12M = Column(Float)
    pct_active_tl = Column(Float)
    Home_TL = Column(Integer)
    Age_Oldest_TL = Column(Integer)
    Other_TL = Column(Integer)
    Secured_TL = Column(Integer)
    enq_L3m = Column(Integer)
    PL_enq_L6m = Column(Integer)
    num_std = Column(Float)
    num_std_12mts = Column(Float)
    num_std_6mts = Column(Float)
    AGE = Column(Integer)
    CC_enq_L6m = Column(Integer)
    PL_enq = Column(Integer)
    CC_enq_L12m = Column(Integer)
    tot_enq = Column(Integer)
    PL_enq_L12m = Column(Integer)
    enq_L12m = Column(Integer)
    time_since_recent_enq = Column(Integer)
    enq_L6m = Column(Integer)
    pct_of_active_TLs_ever = Column(Float)
    pct_PL_enq_L6m_of_ever = Column(Float)
    Credit_Score = Column(Integer)
    pct_PL_enq_L6m_of_L12m = Column(Float)
    pct_CC_enq_L6m_of_L12m = Column(Float)
    MARITALSTATUS = Column(String)
    EDUCATION = Column(String)
    last_prod_enq2 = Column(String)
    first_prod_enq2 = Column(String)
    prediction = Column(String)  # Store predicted label
    created_at = Column(String, default=datetime.utcnow().isoformat())  # timestamp

