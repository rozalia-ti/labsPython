class Currency:
    def __init__(self, id: str, num_code: str, char_code: str, nominal: str, name: str, value: str, rate: str):
        self.__id = id
        self.__num_code = num_code
        self.__char_code = char_code
        self.__name = name
        self.__value = float(value.replace(',', '.'))
        self.__nominal = int(nominal)
        self.__rate = float(rate.replace(',', '.'))

    @property
    def id(self) -> str:
        return self.__id

    @property
    def num_code(self) -> str:
        return self.__num_code

    @property
    def char_code(self) -> str:
        return self.__char_code

    @property
    def name(self) -> str:
        return self.__name

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = float(value.replace(',', '.'))

    @property
    def nominal(self) -> int:
        return self.__nominal

    @property
    def rate(self) -> float:
        return self.__rate

    def __repr__(self):
        return f"Currency({self.char_code}: {self.value} руб.)"