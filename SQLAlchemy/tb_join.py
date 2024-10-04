import pandas as pd
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Float

# Load data from CSV
df = pd.read_csv("C:\\Users\\joshlewis\\Downloads\\ShinyApp\\user_data.csv")
odf = pd.read_csv("C:\\Users\\joshlewis\\Downloads\\ShinyApp\\occupation_data.csv")

# Get column names and data types from DataFrames
user_columns = df.columns
occ_columns = odf.columns

user_dtypes = df.dtypes
occ_dtypes = odf.dtypes

# Data type mappings for SQLAlchemy
dtypes_dict = {
    "object": String, 
    "int64": Integer,
    "float64": Float}

Dbase = declarative_base()

# Create dynamic columns for UserData
class UserData(Dbase):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True)
    occupations = relationship("OccData", back_populates="user")

# Create dynamic columns for OccData
class OccData(Dbase):
    __tablename__ = "occ_data"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_data.id'))  # Foreign key linking to UserData
    user = relationship("UserData", back_populates="occupations")

# Dynamically add columns to UserData
for col in user_columns:
    str_dtype = str(user_dtypes[col])
    col_type = dtypes_dict.get(str_dtype, String)
    setattr(UserData, col, Column(col_type))

# Dynamically add columns to OccData
for ocol in occ_columns:
    str_dtype = str(occ_dtypes[ocol])
    col_type = dtypes_dict.get(str_dtype, String)
    setattr(OccData, ocol, Column(col_type))

# Create engine and tables
engine = create_engine("sqlite:///data_base.db")

Dbase.metadata.drop_all(engine)  # Drop tables to avoid conflicts with previous schemas
Dbase.metadata.create_all(engine)  # Create tables

# Create a session
smaker = sessionmaker(bind=engine)
session = smaker()

# Insert data into UserData
ud_dict = df.to_dict(orient="records")
session.bulk_insert_mappings(UserData, ud_dict)

# Insert data into OccData and link by username
od_dict = []
for col, row in df.iterrows():
    user_occupations = odf[odf['username'] == row['username']]  # Find matching occupations
    for col, occ_row in user_occupations.iterrows():
        occ_entry = {
            'username': occ_row['username'],
            'name': occ_row['name'],
            'occupation': occ_row['occupation'],
            'user_id': session.query(UserData.id).filter(UserData.username == occ_row['username']).scalar()}
        od_dict.append(occ_entry)

session.bulk_insert_mappings(OccData, od_dict)

# Commit the session to save the data
session.commit()

# Perform a join query
joint_table = session.query(UserData, OccData).join(OccData, UserData.id == OccData.user_id).all()

# Extract and print the results
data = [(user.username, occupation.occupation) for user, occupation in joint_table]
df_result = pd.DataFrame(data, columns=['Username', 'Occupation'])

print(df_result)
