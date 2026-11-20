class Product:

    VAT_RATE = 0.15

def _init_(self, code, name, price):
    self.code = code
    self.name = name

    if price < 0:
        raise ValueError("Price cannot be negative.")

    self.price = price

def _str_(self):
    return f"{self.code} - {self.name}: R{self.price:.2f}"

def calc_vat(self):
    return self.price * self.VAT_RATE

def price_including_vat(self):
    return self.price + self.calc_vat()

def apply_discount(self, percentage):
    discount = self.price * percentage / 100
    return self.price - discount


def update_price(self, new_price):
    if new_price < 0:
        raise ValueError("New price cannot be negative.")

    self.price = new_price
    return self.price


def main():

    product1 = Product("P001", "Keyboard", 450.00)
    product2 = Product("P002", "Mouse", 250.00)

    print(product1)
    print(product2)

    print("VAT:", product1.calc_vat())

    print("Price including VAT:",
          product1.price_including_vat())

    print("Price after 10% discount:",
          product1.apply_discount(10))

   
    print("Updated price:",
          product1.update_price(500.00))

    print("Updated product details:")
    print(product1)


main()
