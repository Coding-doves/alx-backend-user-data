"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ add new user """
        if isinstance(email, str):
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            
            return user

    def find_user_by(self, **kwargs) -> User:
        ''' find user by filter'''
        user = self._session.query(User)
        for key, val in kwargs.items():
            if key not in User.__dict__:
                raise InvalidRequestError
            for person in user:
                if getattr(person, key) == val:
                    return person
                raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        ''' update user '''
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        updat = {}
        for key, val in kwargs.items():
            if hasattr(User, key):
                updat[getattr(User, key)] = val
            else:
                raise ValueError()
        self._session.query(User).filter(
            User.id == user_id).update(
                updat, synchronize_session=False,)
        self._session.commit()
