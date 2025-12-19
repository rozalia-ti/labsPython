class UserCurrency():
    def __init__(self, id: str, user_id: int):
        self.__id = id
        self.__user_id = user_id

    @property
    def id(self):
        return self.__id

    @property
    def user_id(self):
        return self.__user_id

    def __repr__(self):
        return f"UserCurrency(user_id={self.user_id}, currency_id={self.id})"