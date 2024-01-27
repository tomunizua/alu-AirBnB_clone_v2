#!/usr/bin/python3
"""This is the file storage class for AirBnB"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns a dictionary
        Args:
            cls: Name of class to list
        Return:
            returns a dictionary of __object
        """
        if cls:
            dict_store = {}
            for obj_id in self.__objects:
                obj_cls = self.__objects[obj_id].__class__
                if cls is obj_cls:
                    dict_store[obj_id] = self.__objects[obj_id]
            return dict_store
        else:
            return self.__objects

    def new(self, obj):
        """sets __object to given obj
        Args:
            obj: given object
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """serialize the file path to JSON file path
        """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """serialize the file path to JSON file path
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass
        except Exception as e:
            pass

    def delete(self, obj=None):
        """ Delete obj from __objects
        Args:
            obj: Object to delete
        """
        if obj:
            remove_key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects.pop(remove_key, 0)
            self.save()

    def close(self):
        """call reload() method for deserializing the JSON objects
        """
        self.reload()
