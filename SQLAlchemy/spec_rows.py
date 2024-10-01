# Variable performing the SQL Query: SELECT * FROM UserData WHERE ID <= 30. 
# Effectively choosing the first 30 rows.
spec_rows = session.query(UserData).filter(UserData.id <= 30).all()

spec_rows2 = session.query(UserData).filter(UserData.username.in_(["happysoul123", "petlover222", "gardeningenthusiast999"]))

# Converting SQLAlchemy schema into a list of dictionaries.
spec_dict = [x.__dict__ for x in spec_rows]

# Iterate through every column in the dictionary, removing the SQLAlchemy instance from each element.
for col in spec_dict:
    col.pop("_sa_instance_stance", None)

# Converting result from a list of dictionarys into a DataFrame, showing columns "id" & "username".
df = pd.DataFrame(spec_dict, columns= ["id", "username"])

# Viewing result
print(df)
