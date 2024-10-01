# Variable performing the SQL Query: SELECT username, comments FROM UserData
spec_cols = session.query(UserData.username, UserData.comments).all()

# Converting result from a list of dictionarys into a DataFrame
df = pd.DataFrame(spec_cols)

# Viewing result
print(df)


# Variable performing the SQL Query: SELECT * FROM UserData WHERE ID <= 30. 
# Effectively choosing the first 30 rows.
spec_rows = session.query(UserData).filter(UserData.id <= 30).all()

# Converting result from a list of dictionarys into a DataFrame
df = pd.DataFrame(spec_rows)

# Viewing result
print(df)
