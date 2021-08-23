from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Float, LargeBinary
# для определения таблицы и модели
from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from datetime import datetime
from logger import logger
logger = logger('DB')

Base = declarative_base()

engine = create_engine('sqlite:///User-list.db', connect_args={'check_same_thread': False})


class User(Base):
    """Таблица пользователей"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    name = Column(String(100))
    phone = Column(String(100))
    subscribe_due = Column(DateTime)
    registration_datetime = Column(DateTime)
    money_count = Column(Integer, default=0)
    is_banned = Column(Boolean, default=False)
    current_state = Column(String(30), default='/start')

    def ban_user(self):
        self.is_banned = True
        session.commit()

    def change_subscription_datetime(self, new_datetime: datetime):
        self.subscribe_due = new_datetime
        session.commit()

    def get_state(self):
        return self.current_state

    def set_state(self, new_state):
        self.current_state = new_state
        session.commit()


def register_user(telegram_id, name, phone, current_state):
    new_obj = User(telegram_id=telegram_id, name=name, phone=phone, current_state=current_state,
                   subscribe_due=None, registration_datetime=datetime.now())

    try:
        session.add(new_obj)
        session.commit()
        logger.debug('User successfully created.')
    except Exception as e:
        session.rollback()
        logger.error(f'Exception on creating object: {e}')
        raise


Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()
