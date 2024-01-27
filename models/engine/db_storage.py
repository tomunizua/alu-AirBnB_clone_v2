#!/usr/bin/python3
""" Module: DBStorage
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """ Class DBStorage for manage DataBase Transactions
    """

    __engine = None
    __session = None
    __tables = [
        State,
        City,
        User,
        Place,
        Review,
        Amenity
    ]

    def __init__(self):
        """ Configure init instance
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv("HBNB_MYSQL_USER"),
            getenv("HBNB_MYSQL_PWD"),
            getenv("HBNB_MYSQL_HOST"),
            getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Show all records depending of class name
        Args:
            cls: Name of class
        Return:
            returns a dictionary of objects
        """
        obj_store = {}
        if cls:
            query = self.__session.query(cls)
            for row in query.all():
                key = "{}.{}".format(cls.__name__, row.id)
                obj_store[key] = row
        else:
            for table in self.__tables:
                query = self.__session.query(table)
                for row in query.all():
                    key = "{}.{}".format(table.__name__, row.id)
                    obj_store[key] = row

        return obj_store

    def new(self, obj):
        """Add the object to the current database session
        Args:
            obj: given object
        """
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Remove the object to the current database session
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and
            create the current database session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Call remove() on the private session attribute self.__session
        """
        self.__session.close()
