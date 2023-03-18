class ValidationHelper:
    @staticmethod
    def validobj(o, o_type):
        if o is None or not isinstance(o, o_type):
            return False
        return True

    @staticmethod
    def validstr(s):
        if s is None or type(s) is not str or s == "":
            return False
        return True
