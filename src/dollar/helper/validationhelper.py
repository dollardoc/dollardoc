class ValidationHelper:
    @staticmethod
    def valid_obj(o, o_type):
        if o is None or not isinstance(o, o_type):
            return False
        return True

    @staticmethod
    def valid_str(s):
        if s is None or type(s) is not str or s == "":
            return False
        return True
