# FILEPATH: /d:/Programming/Phitron/Restaurent_Managemt_system/users.py

from abc import ABC, abstractmethod
from datetime import date

class User(ABC):
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        
class Customer(User):
    def __init__(self, name: str, phone: str, email: str, address: str):
        super().__init__(name, phone, email, address)
        self.cart = []

    def view_menu(self, restaurant: 'Restaurant'):
        restaurant.menu.display_menu()

    def add_to_cart(self, restaurant: 'Restaurant', item_name: str, quantity: int = 1):
        item = restaurant.menu.find_item(item_name)
        if item:
            cart_item = next((i for i in self.cart if i.name == item.name), None)
            if cart_item:
                cart_item.quantity += quantity
            else:
                new_item = FoodItem(item.name, item.price, quantity)
                self.cart.append(new_item)
            print(f"{quantity} {item.name}(s) added to cart")
        else:
            print(f"{item_name} not found in the menu")

    def view_cart(self):
        if self.cart:
            print("Cart:")
            total = 0
            for item in self.cart:
                item_total = item.price * item.quantity
                print(f"- {item.name}: ${item.price:.2f} x {item.quantity} = ${item_total:.2f}")
                total += item_total
            print(f"Total: ${total:.2f}")
        else:
            print("Cart is empty.")

    def place_order(self, restaurant: 'Restaurant'):
        if not self.cart:
            print("Your cart is empty. Cannot place an order.")
        else:
            total = sum(item.price * item.quantity for item in self.cart)
            print(f"Order placed successfully. Total amount: ${total:.2f}")
            self.cart.clear()
            
class Order:
    def __init__(self):  
        self.items = {}  

    def add_item(self, item):
        if item.name in self.items:
            self.items[item.name].quantity += item.quantity
        else:
            self.items[item.name] = item
        print(f"{item.quantity} {item.name}(s) added to order")

    def remove_item(self, item_name):
        if item_name in self.items:
            del self.items[item_name]
            print(f"{item_name} removed from order")
        else:
            print(f"{item_name} not found in order")
            
    def total_price(self):
        return sum(item.price * item.quantity for item in self.items.values())

    def clear_order(self):  # Renamed from clear_cart for consistency
        self.items.clear()
        print("Order cleared")

    def display_order(self):
        if not self.items:
            print("The order is empty.")
        else:
            print("Order Items:")
            total = 0
            for item in self.items.values():
                item_total = item.price * item.quantity
                print(f"- {item.name}: ${item.price:.2f} x {item.quantity} = ${item_total:.2f}")
                total += item_total
            print(f"Total: ${total:.2f}")


      

class Employee(User):
    def __init__(self, name: str, phone: str, email: str, address: str, 
                 salary: float, starting_date: date, department: str):
        super().__init__(name, phone, email, address)
        self.salary = salary
        self.starting_date = starting_date
        self.department = department

class FoodItem:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

class Menu:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"{item.name} added to menu")

    def find_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def remove_item(self, item_name):
        item = self.find_item(item_name)
        if item:
            self.items.remove(item)
            print(f"{item_name} removed from menu")
        else:
            print(f"{item_name} not found in menu")

    def display_menu(self):
        if not self.items:
            print("The menu is empty.")
        else:
            print("Menu Items:")
            for item in self.items:
                print(f"- {item.name}: ${item.price:.2f}")

class Restaurant:
    def __init__(self, name):
        self.name = name
        self.employees = []
        self.menu = Menu()

    def add_employee(self, employee: Employee):
        self.employees.append(employee)
        print(f"{employee.name} added to {self.name}'s employees")
    
    def view_employees(self):
        print("Employees:")
        for employee in self.employees:
            print(employee.name, employee.phone, employee.email, employee.address, employee.salary, employee.starting_date, employee.department)

class Admin(User):
    def __init__(self, name: str, phone: str, email: str, address: str):
        super().__init__(name, phone, email, address)
    
    def add_employee(self, restaurant: 'Restaurant', employee: Employee):
        restaurant.add_employee(employee)
    
    def view_employees(self, restaurant: 'Restaurant'):
        restaurant.view_employees()
    
    def add_menu_item(self, restaurant: 'Restaurant', item: FoodItem):
        if hasattr(restaurant, 'menu'):
            restaurant.menu.add_item(item)
        else:
            print("Error: Restaurant does not have a menu attribute.")
    
    def remove_menu_item(self, restaurant: 'Restaurant', item_name: str):
        if hasattr(restaurant, 'menu'):
            restaurant.menu.remove_item(item_name)
        else:
            print("Error: Restaurant does not have a menu attribute.")

# Example usage
# FILEPATH: /d:/Programming/Phitron/Restaurent_Managemt_system/users.py

# ... (previous code remains unchanged)

def setup_restaurant():
    name = input("Enter restaurant name: ")
    return Restaurant(name)

def setup_admin():
    print("Set up admin account:")
    name = input("Enter admin name: ")
    phone = input("Enter admin phone: ")
    email = input("Enter admin email: ")
    address = input("Enter admin address: ")
    return Admin(name, phone, email, address)

def admin_interface(admin: Admin, restaurant: Restaurant):
    while True:
        print("\nAdmin Menu:")
        print("1. Add menu item")
        print("2. Remove menu item")
        print("3. View menu")
        print("4. Add employee")
        print("5. View employees")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            quantity = int(input("Enter item quantity: "))
            admin.add_menu_item(restaurant, FoodItem(name, price, quantity))
        elif choice == '2':
            name = input("Enter item name to remove: ")
            admin.remove_menu_item(restaurant, name)
        elif choice == '3':
            restaurant.menu.display_menu()
        elif choice == '4':
            name = input("Enter employee name: ")
            phone = input("Enter employee phone: ")
            email = input("Enter employee email: ")
            address = input("Enter employee address: ")
            salary = float(input("Enter employee salary: "))
            start_date = input("Enter employee start date (YYYY-MM-DD): ")
            department = input("Enter employee department: ")
            new_employee = Employee(name, phone, email, address, salary, date.fromisoformat(start_date), department)
            admin.add_employee(restaurant, new_employee)
        elif choice == '5':
            admin.view_employees(restaurant)
        elif choice == '6':
            print("Exiting admin interface.")
            break
        else:
            print("Invalid choice. Please try again.")

def customer_interface(restaurant: Restaurant):
    print(f"Welcome to {restaurant.name}!")
    name = input("Please enter your name: ")
    phone = input("Please enter your phone number: ")
    email = input("Please enter your email: ")
    address = input("Please enter your address: ")

    customer = Customer(name, phone, email, address)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. View menu")
        print("2. Add item to cart")
        print("3. View cart")
        print("4. Place order")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            customer.view_menu(restaurant)
        elif choice == '2':
            item_name = input("Enter the name of the item you want to add: ")
            quantity = int(input("Enter the quantity: "))
            customer.add_to_cart(restaurant, item_name, quantity)
        elif choice == '3':
            customer.view_cart()
        elif choice == '4':
            customer.place_order(restaurant)
        elif choice == '5':
            print("Thank you for visiting! Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def main_interface():
    restaurant = setup_restaurant()
    admin = setup_admin()

    while True:
        print("\nWelcome to the Restaurant Management System")
        print("1. Admin Interface")
        print("2. Customer Interface")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            admin_interface(admin, restaurant)
        elif choice == '2':
            customer_interface(restaurant)
        elif choice == '3':
            print("Thank you for using the Restaurant Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Example usage
if __name__ == "__main__":
    main_interface()



