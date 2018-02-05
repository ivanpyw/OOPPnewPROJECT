import time
from datetime import datetime


class CreateRequest:
    def __init__(self, drinks, food, assistance, other, DatePublished, NRIC, status, emergency):
        self.__pubid =''
        self.__emergency= emergency
        self.__NRIC= NRIC
        self.__status =status
        self.__DatePublished = DatePublished
        self.__drinks = drinks
        self.__food = food
        self.__assistance = assistance
        self.__other = other

    def set_emergency(self,emergency):
        self.__emergency = emergency

    def set_pubid(self, pubid):
        self.__pubid = pubid

    def set_status(self, status):
        self.__status= status

    def get_emergency(self):
        return self.__emergency

    def get_status(self):
        return self.__status

    def get_pubid(self):
        return self.__pubid

    def set_drinks(self, drinks):
        self.__drinks = drinks

    def set_food(self, food):
        self.__food = food

    def set__assistance(self, assistance):
        self.__assistance = assistance

    def set_other(self, other):
        self.__other = other

    def get_NRIC(self):
        return self.__NRIC

    def get_DatePublished(self):
        return self.__DatePublished

    def get_drinks(self):
        return self.__drinks

    def get_food(self):
        return self.__food

    def get_assistance(self):
        return self.__assistance

    def get_other(self):
        return self.__other