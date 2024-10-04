# SELECT *, MIN(id) FROM UserData
agg_data1 = session.query(func.min(UserData.id)).scalar() # scalar() is used to make result into a single value as opposed to a list. 

# SELECT *, MAX(id) FROM UserData
agg_data2 = session.query(func.max(UserData.id)).scalar()

# SELECT *, username, COUNT(platform) * FROM UserData GROUP BY username 
agg_data3 = session.query(UserData.username, func.count(UserData.platform)).group_by(UserData.username).all()

# SELECT *, AVG(id) FROM UserData
agg_data4 = session.query(func.avg(UserData.id)).scalar()

# Viewing results
print(agg_data1,agg_data2, agg_data3, agg_data4)
