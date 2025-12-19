class Author():
    def __init__(self, name: str, group: str):
        self.__name = name
        self.__group = group

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Имя автора должно быть строкой от 2 символов')

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, group: str):
        if isinstance(group, str) and len(group) > 5:
            self.__group = group
        else:
            raise ValueError('Группа должна быть строкой от 6 символов')