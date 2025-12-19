from .author import Author

class App():
    def __init__(self, name: str, version: str, author: Author):
        self.__name = name
        self.__version = version
        self.__author = author

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Имя приложения должно быть строкой от 2 символов')

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version: str):
        if isinstance(version, str):
            self.__version = version
        else:
            raise ValueError('Версия должна быть строкой')

    @property
    def author(self):
        return self.__author