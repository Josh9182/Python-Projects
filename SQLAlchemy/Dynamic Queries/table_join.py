import pandas as pd
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Float

# CSV imports
df = pd.read_csv("C:\\Users\\joshlewis\\Downloads\\ShinyApp\\user_data.csv")
odf = pd.read_csv("C:\\Users\\joshlewis\\Downloads\\ShinyApp\\occupation_data.csv")

# Accessing column names for both files imports
user_columns = df.columns
occ_columns = odf.columns

# Accessing data types for both DataFrames
user_dtypes = df.dtypes
occ_dtypes = odf.dtypes

# Dictionary associating CSV dtype keys to SQLAlchemy dtype values
dtypes_dict = {
    "object": String, 
    "int64": Integer,
    "float64": Float}

# Foundation for class modeling
Dbase = declarative_base()

# "user_data" & "occupational_data" tables built upon the "Dbase"
class UserData(Dbase):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True)
    occupations = relationship("OccData", back_populates="user") # back_populates, allowing for bidirectional links between tables

class OccData(Dbase):
    __tablename__ = "occ_data"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_data.id')) # utilizing ForeignKey to merge tables based on primary_key value
    user = relationship("UserData", back_populates="occupations")

# Loop to convert CSV data types into ORM dtype and add into tables seperately
for col in user_columns:
    str_dtype = str(user_dtypes[col])
    col_type = dtypes_dict.get(str_dtype, String)
    setattr(UserData, col, Column(col_type))

for ocol in occ_columns:
    str_dtype = str(occ_dtypes[ocol])
    col_type = dtypes_dict.get(str_dtype, String)
    setattr(OccData, ocol, Column(col_type))

# Initiate SQLite engine for database connection
engine = create_engine("sqlite:///data_base.db")

# Error proofing engine, dropping any previous tables.
Dbase.metadata.drop_all(engine)
Dbase.metadata.create_all(engine) # Tables created, built off base and SQLite engine

# Session creation for this specific engine
smaker = sessionmaker(bind=engine)
session = smaker() # Variable initiating engine, allowing for table manipulation

# Convert "df" into list of dictionaries where each row is a dictionary. Key: Column, Value: Row Info
ud_dict = df.to_dict(orient="records")
session.bulk_insert_mappings(UserData, ud_dict) # Insert ud_dict into "UserData" table

# Due to ForeignKey constraint, "OccData" must be manually merged into "UserData" utilizing a for loop
od_dict = []
for _, row in df.iterrows():
    user_occupations = odf[odf['username'] == row['username']]  # Find matching occupations
    for _, occ_row in user_occupations.iterrows():
        occ_entry = {
            'username': occ_row['username'],
            'name': occ_row['name'],
            'occupation': occ_row['occupation'],
            'user_id': session.query(UserData.id).filter(UserData.username == occ_row['username']).scalar()}
        od_dict.append(occ_entry)

# Insert list of dictionaries into "OccData" table
session.bulk_insert_mappings(OccData, od_dict)

# Save progress
session.commit()

# joint_table variable housing a join query based off table ids
joint_table = session.query(UserData, OccData).join(OccData, UserData.id == OccData.user_id).all()

# Utilizing a dictionary, organize all information and iterate throughout
join_data = [
    {
        "user_id": user.id,
        "username": user.username,
        "platform": user.platform,
        "caption": user.caption,
        "likes": user.likes,
        "comments": user.comments,
        "shares": user.shares,
        "timestamp": user.timestamp,
        "occ_id": occupation.id,
        "name": occupation.name,
        "occupation": occupation.occupation,
        "occ_user_id": occupation.user_id}
    for user, occupation in joint_table]

# Convert dictionary into DataFrame
df = pd.DataFrame(join_data)

# Visualize DataFrame
print(df)
