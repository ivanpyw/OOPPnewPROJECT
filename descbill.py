class Descbill:
    def __init__(self, product,quantity,price):
        self.__pubid = ""
        self.__product = product
        self.__quantity = quantity
        self.__price = price

    def get_product(self):
        return self.__product

    def get_quantity(self):
        return self.__quantity

    def get_price(self):
        return self.__price

    def set_product(self, product):
        self.__product = product

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_price(self, price):
        self.__price = price

    def get_pubid(self):
        return self.__pubid

    def set_pubid(self, pubid):
        self.__pubid = pubid