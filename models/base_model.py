#!/usr/bin/python3
"""
Parent class that other classes will inherit from
"""
import uuid
from datetime import datetime
from models import storage

class BaseModel:
    """
    Defines all common attributes/methods
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes all attributes
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)
        else:
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, date_format)
                if key != '__class__':
                    setattr(self, key, value)

    def __str__(self):
        """
        Returns class name, id, and attribute dictionary
        """
        class_name = "[" + self.__class__.__name__ + "]"
        dct = {k: v for (k, v) in self.__dict__.items() if v is not None}
        return class_name + " (" + self.id + ") " + str(dct)

    def save(self):
        """
        Updates last update time
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        Creates a new dictionary, adding a key and returning
        datetimes converted to strings
        """
        new_dict = {}

        for key, value in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                new_dict[key] = value.strftime("%Y-%m-%dT%H:%M:%S.%f")
            else:
                if value is not None:
                    new_dict[key] = value
        new_dict['__class__'] = self.__class__.__name__

        return new_dict

