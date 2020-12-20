

class Utils:

    @classmethod
    def convert_to_int(cls, value, default=0):
        try:
            x = int(value)
            return x
        except Exception:
            return default

    @classmethod
    def convert_to_float(cls, value, default=0.0):
        try:
            x = float(value)
            return x
        except ValueError:
            return default
