class Users:
    def __init__(self, nric, fullname,dob, gender,password):
        self.__nric = nric
        self.__fullname = fullname
        self.__dob = dob
        self.__gender = gender
        self.__password = password



    def get_gender(self):
        return self.__gender

    def get_dob(self):
        return self.__dob

    def get_fullname(self):
        return self.__fullname

    def get_nric(self):
        return self.__nric

    def get_password(self):
        return self.__password

    def set_gender(self, gender):
        self.__gender = gender

    def set_fullname(self, fullname):
        self.__fullname = fullname

    def set_nric(self, nric):
        self.__nric = nric

    def set_password(self, password):
        self.__password = password

    def set_dob(self, dob):
        self.__dob = dob

