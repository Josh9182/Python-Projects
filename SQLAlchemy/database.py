import pandas as pd
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine, ForeignKey, Column, Float, String, Integer

# CSV imports
df = pd.read_csv("C:\\Users\\joshlewis\\Downloads\\ShinyApp\\user_data.csv")
odf = pd.read_csv("C:\\Users\\joshlewis\\Downloads\\ShinyApp\\occupation_data.csv")

# Accessing column names for both files imports
columns = df.columns
Ocolumns = odf.columns

dtypes = df.dtypes
Odtypes = odf.dtypes

# Dictionary associating CSV dtype keys to SQLAlchemy dtype values  
dtypes_dict = {
    "object": String, 
    "int64": Integer,
    "float64": Float}

# Foundation for class modeling
Dbase = declarative_base()

# "user_data" & "occupational_data" tables built upon the "Dbase"
# featuring dynamic row numbers and the ability to join via ForeignKey and relationship
class UserData(Dbase):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key= True, autoincrement= True)
    occupations = relationship("OccData", back_populates= "users")

class OccData(Dbase):
    __tablename__ = "occ_data"
    id = Column(Integer, primary_key= True, autoincrement= True)
    user_id = Column(Integer, ForeignKey('user_data.id'))
    users = relationship("UserData", back_populates= "occupations")

# Loop to convert CSV data types into ORM dtype and add into tables seperately
for col in columns:
    str_dtype = str(dtypes[col])
    col_type = dtypes_dict.get(str_dtype, String)
    setattr(UserData, col, Column(col_type))

    
for ocol in Ocolumns:
    str_dtype = str(Odtypes[ocol])
    col_type = dtypes_dict.get(str_dtype, String)
    setattr(OccData, ocol, Column(col_type))

# Initiate SQLite engine for database connection
engine = create_engine("sqlite:///data_base.db")

# Tables created, built off base and SQLite engine
Dbase.metadata.create_all(engine)

# Session creation for this specific engine, allowing for 
# database interaction and manipulation
smaker = sessionmaker(bind=engine)
session = smaker()

# Convert "df" & "odf" into list of dictionaries where each row is a dictionary. Key: Column, Value: Row Info
ud_dict = df.to_dict(orient="records")
od_dict = odf.to_dict(orient="records")

# Insert dictionary list into "UserData" & "OccupationalData" table, filling in schema
session.bulk_insert_mappings(UserData, ud_dict)
session.bulk_insert_mappings(OccData, od_dict)

# Finalizing SQL transaction
session.commit()
