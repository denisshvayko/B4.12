import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid
import re
import users
from users import User
# import import_ipynb
# import B4.12
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()
    
class Athlets(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.INTEGER, primary_key=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.TEXT)
    weight = sa.Column(sa.REAL)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.TEXT)
    country = sa.Column(sa.TEXT)
    
def find(_id, session):
    """
    Производит поиск пользователя в таблице user по заданному id
    """
    # находим все записи в таблице User, у которых поле User.first_name совпадает с параметром name
    query = session.query(User).filter(User.id == _id).first()
    # подсчитываем количество таких записей в таблице с помощью метода .count()
    if query:
        atl_height = session.query(Athlets).filter(Athlets.height > 0).order_by(sa.func.abs(Athlets.height - query.height)).first()
        atl_birthdate = session.query(Athlets).order_by(sa.func.abs(sa.func.julianday(Athlets.birthdate) - sa.func.julianday(query.birthdate))).first()
        return(atl_height, atl_birthdate)
    else:    
        return(None, None)
        
def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # выбран режим поиска, запускаем его
    _id = input("Введи id пользователя для поиска: ")
    # вызываем функцию поиска по имени
    atl_height, atl_birthdate = find(_id, session)
    if atl_height==None and atl_birthdate==None:
        print("User с таким id нет, попробуйте заново")
    else:
        print(f"Близкий по дате атлет: id:{atl_birthdate.id}, age:{atl_birthdate.age}, birthdate:{atl_birthdate.birthdate}, gender:{atl_birthdate.gender}, height:{atl_birthdate.height}, name:{atl_birthdate.name}, weight:{atl_birthdate.weight}, gold_medals:{atl_birthdate.gold_medals}, silver_medals:{atl_birthdate.silver_medals}, bronze_medals:{atl_birthdate.bronze_medals}, total_medals:{atl_birthdate.total_medals}, sport:{atl_birthdate.sport}, country:{atl_birthdate.country}")
        print(f"Близкий по возрасту атлет: id:{atl_height.id}, age:{atl_height.age}, birthdate:{atl_height.birthdate}, gender:{atl_height.gender}, height:{atl_height.height}, name:{atl_height.name}, weight:{atl_height.weight}, gold_medals:{atl_height.gold_medals}, silver_medals:{atl_height.silver_medals}, bronze_medals:{atl_height.bronze_medals}, total_medals:{atl_height.total_medals}, sport:{atl_height.sport}, country:{atl_height.country}")
    session.close()
if __name__ == "__main__":
    main()