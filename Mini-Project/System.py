class Car:
    def __init__(self, car_id, make, model, year, price_per_day):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.price_per_day = price_per_day
        self.is_rented = False

    def __str__(self):
        return f"{self.make} {self.model} ({self.year}) - ${self.price_per_day}/day"

    def to_string(self):
        return f"{self.car_id},{self.make},{self.model},{self.year},{self.price_per_day},{self.is_rented}\n"


class Customer:
    def __init__(self, customer_id, name, license_number):
        self.customer_id = customer_id
        self.name = name
        self.license_number = license_number
        self.rental_history = []

    def to_string(self):
        return f"{self.customer_id},{self.name},{self.license_number}\n"

    def add_rental(self, rental):
        self.rental_history.append(rental)

    def view_rental_history(self):
        if not self.rental_history:
            return "No rental history."
        
        history = []
        for rental in self.rental_history:
            car_info = f"{rental.car.make} {rental.car.model} for {rental.days} days - Total cost: ${rental.total_cost()}"
            history.append(car_info)
        
        return "\n".join(history)


class Rental:
    def __init__(self, car, customer, days):
        self.car = car
        self.customer = customer
        self.days = days

    def total_cost(self):
        return self.days * self.car.price_per_day


class RentalSystem:
    def __init__(self):
        self.cars = []
        self.customers = []
        self.rentals = []
        self.load_data()

    def add_car(self, car):
        self.cars.append(car)
        self.save_cars()

    def add_customer(self, customer):
        self.customers.append(customer)
        self.save_customers()

    def rent_car(self, car_id, customer_id, days):
        car = None
        for c in self.cars:
            if c.car_id == car_id and not c.is_rented:
                car = c
                break
        
        customer = None
        for cust in self.customers:
            if cust.customer_id == customer_id:
                customer = cust
                break

        if car and customer:
            rental = Rental(car, customer, days)
            self.rentals.append(rental)
            car.is_rented = True
            customer.add_rental(rental)
            print(f"Car rented: {car} to {customer.name} for {days} days. Total cost: ${rental.total_cost()}")
        else:
            if not car:
                print("Car not available or does not exist.")
            if not customer:
                print("Customer not found.")

    def return_car(self, car_id, customer_id):
        rental = None
        for r in self.rentals:
            if r.car.car_id == car_id and r.customer.customer_id == customer_id:
                rental = r
                break
        
        if rental:
            self.rentals.remove(rental)
            rental.car.is_rented = False
            print(f"Car returned: {rental.car} from {rental.customer.name}.")
        else:
            print("Rental not found.")

    def list_available_cars(self):
        available_cars = []
        for car in self.cars:
            if not car.is_rented:
                available_cars.append(car)
        
        if available_cars:
            print("Available Cars:")
            for car in available_cars:
                print(car)
        else:
            print("No cars available.")

    def save_cars(self):
        with open('cars.txt', 'w') as f:
            for car in self.cars:
                f.write(car.to_string())

    def save_customers(self):
        with open('customers.txt', 'w') as f:
            for customer in self.customers:
                f.write(customer.to_string())

    def load_data(self):
        try:
            with open('cars.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    parts = line.split(',')
                    car_id = parts[0]
                    make = parts[1]
                    model = parts[2]
                    year = int(parts[3])
                    price_per_day = float(parts[4])
                    is_rented = parts[5] == 'True'
                    car = Car(car_id, make, model, year, price_per_day)
                    car.is_rented = is_rented
                    self.cars.append(car)
        except FileNotFoundError:
            pass

        try:
            with open('customers.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    parts = line.split(',')
                    customer_id = parts[0]
                    name = parts[1]
                    license_number = parts[2]
                    customer = Customer(customer_id, name, license_number)
                    self.customers.append(customer)
        except FileNotFoundError:
            pass


rental_system = RentalSystem()

menu_options = {
    '1': "Add Car",
    '2': "Add Customer",
    '3': "Rent Car",
    '4': "Return Car",
    '5': "List Available Cars",
    '6': "View Rental History",
    '7': "Exit"
}

while True:
    print("\nCar Rental System Menu:")
    for key in menu_options:
        print(f"{key}. {menu_options[key]}")

    choice = input("Enter your choice: ")

    if choice == '1':
        car_id = input("Enter car ID: ")
        make = input("Enter car make: ")
        model = input("Enter car model: ")
        year = int(input("Enter car year: "))
        price_per_day = float(input("Enter price per day: "))
        car = Car(car_id, make, model, year, price_per_day)
        rental_system.add_car(car)
        print("Car added successfully.")

    elif choice == '2':
        customer_id = input("Enter customer ID: ")
        name = input("Enter customer name: ")
        license_number = input("Enter license number: ")
        customer = Customer(customer_id, name, license_number)
        rental_system.add_customer(customer)
        print("Customer added successfully.")

    elif choice == '3':
        car_id = input("Enter car ID to rent: ")
        customer_id = input("Enter customer ID: ")
        days = int(input("Enter number of days to rent: "))
        rental_system.rent_car(car_id, customer_id, days)

    elif choice == '4':
        car_id = input("Enter car ID to return: ")
        customer_id = input("Enter customer ID: ")
        rental_system.return_car(car_id, customer_id)

    elif choice == '5':
        rental_system.list_available_cars()

    elif choice == '6':
        customer_id = input("Enter customer ID to view rental history: ")
        customer = None
        for c in rental_system.customers:
            if c.customer_id == customer_id:
                customer = c
                break
        if customer:
            print(customer.view_rental_history())
        else:
            print("Customer not found.")

    elif choice == '7':
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please try again.") 
