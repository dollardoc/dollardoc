import copy

from dollar.dollarexception import DollarException
from dollar.dollarobject import DollarObject
from dollar.helper.validationhelper import ValidationHelper


class DollarObjectIdMapDiff:
    def __init__(self, added, changed, removed):
        self.added = added
        self.changed = changed
        self.removed = removed

    def is_changed(self):
        return (len(self.added) + len(self.changed) + len(self.removed)) != 0


class DollarObjectIdMap:

    def __init__(self):
        self.id_map = {}

    def get(self, dollar_object_id) -> DollarObject:
        if not ValidationHelper.valid_str(dollar_object_id):
            raise DollarException(
                    "Id must be a valid string")
        if dollar_object_id not in self.id_map:
            raise DollarException("Id " + dollar_object_id + " does not exist")
        return self.id_map[dollar_object_id]

    def has_id(self, dollar_object_id):
        return dollar_object_id in self.id_map

    def remove__with_path(self, path: str):
        for key in self.id_map:
            if self.id_map[key].get_path() == path:
                del self.id_map[key]

    def get_map(self):
        return self.id_map

    def add(self, dollar_object: DollarObject):
        if not ValidationHelper.valid_obj(dollar_object, DollarObject):
            raise DollarException("Object is not a valid DollarObject")
        if not ValidationHelper.valid_str(dollar_object.get_id()):
            raise DollarException("Id must be a valid string")
        if dollar_object.get_id() in self.id_map:
            raise DollarException("Id " + dollar_object.get_id() + " already exists")
        self.id_map[dollar_object.get_id()] = dollar_object

    def add__force(self, dollar_object: DollarObject):
        if not ValidationHelper.valid_obj(dollar_object, DollarObject):
            raise DollarException("Object is not a valid DollarObject")
        if not ValidationHelper.valid_str(dollar_object.get_id()):
            raise DollarException("Id must be a valid string")
        self.id_map[dollar_object.get_id()] = dollar_object

    def diff(self, dollar_object_id_map):
        added = []
        changed = []
        removed = []
        checked_keys = []
        for key in self.id_map:
            checked_keys.append(key)
            if key not in dollar_object_id_map.id_map:
                removed.append(self.id_map[key])
            elif not self.id_map[key].equals(dollar_object_id_map.id_map[key]):
                changed.append(dollar_object_id_map.id_map[key])
        for key in dollar_object_id_map.id_map:
            if key in checked_keys:
                continue
            added.append(dollar_object_id_map.id_map[key])
        return DollarObjectIdMapDiff(added, changed, removed)

    def copy(self):
        return copy.deepcopy(self)
