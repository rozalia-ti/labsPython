class UserCurrency():
    def __init__(self, id: int, user_id: int):
        self.__id: int = id;
        self.__user_id: int = user_id;

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def  id(self, id: int):
        if type(id) is int:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании id')
    
    @property
    def user_id(self):
        return self.__user_id
    
    @user_id.setter
    def  id(self, user_id: int):
        if type(user_id) is int:
            self.__user_id = user_id
        else:
            raise ValueError('Ошибка при задании user_id')