from typing import Self


class MutableString:
    def __init__(self, string: str | Self = ''):
        self.__string = string.__str__()
        self.__get__ = lambda: self.__string

    def __str__(self):
        return self.__get__()

    def __repr__(self):
        return self.__get__()

    def __set__(self, instance, value):
        self.__string = value

    def format(self, *args, **kwargs):
        return self.__string.format(*args, **kwargs)


class DynamicString:
    def __init__(self, string: str | MutableString | Self = '', **formats: dict[str, str | MutableString | Self]):
        self._string = MutableString(string)
        self._formats = formats
        self.__get__ = lambda: self._string.format(**formats)

    def __str__(self):
        return self.__get__()

    def __repr__(self):
        return self.__get__()

