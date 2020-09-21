import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid
import re

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
    
def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("А теперь пол: ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    birthdate = input("А теперь дату рождения (в формате гггг-мм-дд): ")
    height = input("А теперь рост: ")
    # генерируем идентификатор пользователя и сохраняем его строковое представление
#     bit_size = 64
    user_id = str(uuid.uuid4())
    # создаем нового пользователя
    user = User(
#         id = user_id,
        first_name = first_name,
        last_name = last_name,
        gender = gender,
        email = email,
        birthdate = birthdate,
        height= height
    )
    # возвращаем созданного пользователя
    return user
    
class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)
    
    
def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # запрашиваем данные пользоватлея
    user = request_data()    
    # добавляем нового пользователя в сессию
    query_checker = session.query(User).filter(User.first_name == user.first_name).filter(User.last_name == user.last_name).filter(User.gender == user.gender).filter(User.email == user.email).filter(User.birthdate == user.birthdate).filter(User.height == user.height).first()
    if query_checker:
        print("Пользователь с такими параметрами уже существует попробуйте заново")
    elif re.match(r'\d{4}-\d{2}-\d{2}', user.birthdate)==None:
        print("Дата введена некорректно, попробуйте заново")
    else:   
        session.add(user)
        # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
        session.close()


if __name__ == "__main__":
    main()