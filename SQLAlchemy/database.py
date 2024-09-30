# Accessing Pandas & SQLAlchemy ORM library functions 
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Reading the sample CSV file, converting into DataFrame
df = pd.read_csv("C:\\Users\\joshlewis\\Downloads\\ShinyApp\\user_data.csv")

# Accessing column names 
columns = df.columns

# Accessing underlying data type for each column
dtypes = df.dtypes

# Dictionary associating CSV dtype keys to SQLAlchemy dtype values  
dtypes_dict = {
    "object": String, 
    "int64": Integer,
    "float64": Float}

# Foundation for class modeling
Dbase = declarative_base()

# "user_data" table build upon the "Dbase", featuring row numbers
class UserData(Dbase):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key= True, autoincrement= True)

# Loop to convert CSV dtype into ORM dtype and add into "user_data" table
for col in columns:
    str_dtype = str(dtypes[col])
    col_type = dtypes_dict.get(str_dtype, String)
    setattr(UserData, col, Column(col_type))

# Initiate SQLite engine for database connection
engine = create_engine("sqlite:///database.db")

# Table creation built off base and SQLite engine
Dbase.metadata.create_all(engine)

# Session creation for this specific engine, allowing for 
# database interaction and manipulation
smaker = sessionmaker(bind=engine)
session = smaker()

# Convert "df" into list of dictionaries where each row is a dictionary. Key: Column, Value: Row Info
ud_dict = df.to_dict(orient='records')

# Insert dictionary list into "UserData" table, filling in schema
session.bulk_insert_mappings(UserData, ud_dict)

# Finalizing SQL transaction
session.commit()
