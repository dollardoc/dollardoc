from dollar.dollarexception import DollarException
from dollar.dollarobject import DollarObject
from dollar.helper.validationhelper import ValidationHelper


class DollarObjectIdMap:

    id_map = {}

    @classmethod
    def get(cls, dollar_object_id):
        if not ValidationHelper.valid_str(dollar_object_id):
            raise DollarException(
                    "Id must be a valid string")
        if dollar_object_id not in cls.id_map:
            raise DollarException("Id " + dollar_object_id + " does not exist")
        return cls.id_map[dollar_object_id]

    @classmethod
    def add(cls, dollar_object: DollarObject):
        if not ValidationHelper.valid_obj(dollar_object, DollarObject):
            raise DollarException("Object is not a valid DollarObject")
        if not ValidationHelper.valid_str(dollar_object.get_id()):
            raise DollarException("Id must be a valid string")
        if dollar_object.get_id() in cls.id_map:
            raise DollarException("Id " + dollar_object.get_id() + " already exists")
        cls.id_map[dollar_object.get_id()] = dollar_object

    @classmethod
    def clean(cls):
        cls.id_map = {}
