#!/usr/bin/python3

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    __file_path = "file.json"
    __objects = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'City': City,
        'State': State,
        'Amenity': Amenity,
        'Review': Review
    }

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        obj_dict = {}
        for key, obj in self.__objects.items():
            if key not in obj_dict:
                obj_dict[key] = {}
            obj_dict[key] = obj.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    class_name, obj_id = key.split('.')
                    cls = self.__objects[class_name]
                    self.__objects[key] = cls(**value)
        except FileNotFoundError:
            pass

