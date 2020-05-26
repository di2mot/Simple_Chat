from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///mydatabase.db', echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)

    def __init__(self, login, password, port):
        self.login = login
        self.password = password
        self.port = port

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.id, self.login, self.password)

    def cr_engine():
        # Создание таблицы
        Base.metadata.create_all(engine)
        metadata = Base.metadata
        Session = sessionmaker(bind=engine)
        session = Session()

# Создание таблицы
Base.metadata.create_all(engine)
metadata = Base.metadata

Session = sessionmaker(bind=engine)
session = Session()

# newUser = User("vasia", "vasia2000")
# session.add(newUser)
# session.commit()
#
# getUer = session.query(User).filter_by(login="vasia").first()
#
# print(f'getUser: {getUser.login}')s
#
