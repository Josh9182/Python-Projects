# Variable performing the SQL Query: SELECT * FROM UserData WHERE ID BETWEEN 1 AND 30 ORDER BY id DESC 
spec_rows = session.query(UserData).filter(UserData.id.between(1,30)).order_by(UserData.id.desc()).all()

# EXAMPLE variable performing the SQL Query: SELECT * FROM UserData WHERE username IN ("happysoul123", "petlover222", "gardeningenthusiast999"). 
spec_rows2 = session.query(UserData).filter(UserData.username.in_(["happysoul123", "petlover222", "gardeningenthusiast999"])) 

# Converting SQLAlchemy schema into a list of dictionaries.
spec_dict = [x.__dict__ for x in spec_rows]

# Iterate through every column in the dictionary, removing the SQLAlchemy instance from each element.
for col in spec_dict:
    col.pop("_sa_instance_state", None)

# Converting result from a list of dictionarys into a DataFrame, showing columns "id" & "username".
df = pd.DataFrame(spec_dict)

# Viewing result
print(df)
