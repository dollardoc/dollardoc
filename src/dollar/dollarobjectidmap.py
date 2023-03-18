from dollar.dollarexecutionexception import DollarExecutionException
from dollar.dollarobject import DollarObject
from dollar.validationhelper import ValidationHelper


class DollarObjectIdMap:

    id_map = {}

    @classmethod
    def get(cls, dollar_object_id):
        if not ValidationHelper.validstr(dollar_object_id):
            raise DollarExecutionException("Id must be a valid string")
        if dollar_object_id not in cls.id_map:
            raise DollarExecutionException("Id " + dollar_object_id + " does not exist")
        return cls.id_map[dollar_object_id]

    @classmethod
    def add(cls, dollar_object: DollarObject) -> bool:
        if not ValidationHelper.validobj(dollar_object, DollarObject):
            raise DollarExecutionException("Object is not a valid DollarObject")
        if not ValidationHelper.validstr(dollar_object.getid()):
            raise DollarExecutionException("Id must be a valid string")
        if dollar_object.getid() in cls.id_map:
            raise DollarExecutionException("Id " + dollar_object.getid() + " already exists")
        cls.id_map[dollar_object.getid()] = dollar_object
