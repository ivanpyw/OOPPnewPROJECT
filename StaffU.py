class StaffU:
    def __init__(self, staffid, password, type):

        self.__staffid = staffid
        self.__password = password
        self.__type = type

    def get_type(self):
        return self.__type

    def get_staffid(self):
        return self.__staffid

    def get_password(self):
        return self.__password

    def set_type(self, type):
        self.__type = type


    def set_staffid(self, staffid):
        self.__staffid = staffid

    def set_password(self, password):
        self.__password = password

