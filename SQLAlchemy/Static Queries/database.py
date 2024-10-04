import pandas as pd
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, String, Integer

# Foundation for class modeling
Dbase = declarative_base()

# Define the UserData table and empty rows
class UserData(Dbase):
    __tablename__ = "user_data"
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String)
    score = Column(Integer)

# Initiate SQLite engine for database connection
engine = create_engine("sqlite:///user_data.db")

# Error proofing engine, dropping any previous tables
# Tables created, built off base and SQLite engine
Dbase.metadata.drop_all(engine)
Dbase.metadata.create_all(engine)

# Session creation for this specific engine
smaker = sessionmaker(bind=engine)
session = smaker() # Variable initiating engine, allowing for table manipulation

# Data to be imported into the "UserData" table
user_data1 = UserData(username="Marshmallow34", score=765)
user_data2 = UserData(username="RaceCarrrrr88", score=362)
user_data3 = UserData(username="KiLLeRCroc676", score=1087)

# Add all data inside the UserData table
session.add_all([user_data1, user_data2, user_data3])

# Finalizing SQL transaction
session.commit()
