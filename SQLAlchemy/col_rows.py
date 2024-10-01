# Variable performing the SQL Query: SELECT username, comments FROM UserData
spec_cols = session.query(UserData.username, UserData.comments).all()

# Converting result from a list of dictionarys into a DataFrame
df = pd.DataFrame(spec_cols)

# Viewing result
print(df)


# Variable performing the SQL Query: SELECT * FROM UserData WHERE ID <= 30. 
# Effectively choosing the first 30 rows.
spec_rows = session.query(UserData).filter(UserData.id <= 30).all()

# Converting SQLAlchemy schema into a list of dictionaries.
spec_dict = [x.__dict__ for x in spec_rows]

# Iterate through every column in the dictionary, removing the SQLAlchemy instance from each element.
for col in spec_dict:
    col.pop("_sa_instance_stance", None)

# Converting result from a list of dictionarys into a DataFrame
df = pd.DataFrame(spec_dict)

# Viewing result
print(df)
