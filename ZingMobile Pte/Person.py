class Person:
    def __init__(self, name, age, mobile):
        self.name = name
        self.age = age
        self.mobile = mobile
    
    def display_info(self):
        print("Name:", self.name)
        print("Age:", self.age)
        print("Mobile:", self.mobile)

# Usage
name = input("Enter name: ")
age = input("Enter age: ")
mobile = input("Enter mobile number: ")

person = Person(name, age, mobile)
person.display_info()
