# Variable performing the SQL Query: SELECT username, comments FROM UserData
spec_cols = session.query(UserData.username, UserData.comments).all()

# Converting result from a list of dictionarys into a DataFrame
df = pd.DataFrame(spec_cols)

# Viewing result
print(df)
