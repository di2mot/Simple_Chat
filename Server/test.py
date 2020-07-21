import dbase as db

newUser = db.User("Dima", "Pupkin")

db.session.add(newUser)
db.session.commit()
#
getUser = db.session.query(db.User).filter_by(login="Dima").first()
#
print(f'getUser: {getUser.login}')

