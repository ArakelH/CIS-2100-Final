import random
from datetime import datetime, timedelta
import pandas as pd



class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} ({self.price})"


class Order:
    def __init__(self, order_id, products, customer_id, store_id):
        self.order_id = order_id
        self.products = products
        self.customer_id = customer_id
        self.store_id = store_id
        self.timestamp = datetime.now() - timedelta(
            days=random.randint(0, 6),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

    def total_price(self):
        return sum(product.price for product in self.products)


class Customer:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.orders = []

    def create_order(self, products_list, store_id):
        order_id = random.randint(1000, 9999)
        num_products = random.randint(1, len(products_list))
        selected_products = random.sample(products_list, num_products)
        order = Order(order_id, selected_products, self.customer_id, store_id)
        self.orders.append(order)
        return order


class Store:
    def __init__(self, store_id):
        self.store_id = store_id
        self.orders = []

    def record_order(self, customer, products):
        order = customer.create_order(products, self.store_id)
        self.orders.append(order)
        return order

    def get_total_sales(self):
        return round(sum(order.total_price() for order in self.orders), 2)


class Corporation:
    def __init__(self, name):
        self.name = name
        self.stores = []

    def add_store(self, store):
        self.stores.append(store)

    def generate_sales_report(self):
        all_orders = []
        for store in self.stores:
            for order in store.orders:
                date_str = order.timestamp.strftime("%Y-%m-%d")
                time_str = order.timestamp.strftime("%H:%M:%S")
                product_info = [str(product) for product in order.products]
                all_orders.append((
                    order.timestamp,
                    date_str,
                    time_str,
                    order.store_id,
                    order.customer_id,
                    order.order_id,
                    product_info,
                    round(order.total_price(), 2),
                ))

        all_orders.sort(key=lambda x: x[0], reverse=True)

        # Create a Pandas DataFrame from the order data and assign it to df
        global df  # Declare df as a global variable
        df = pd.DataFrame(
            all_orders,
            columns=[
                "Timestamp",
                "Date",
                "Time",
                "StoreID",
                "CustomerID",
                "OrderID",
                "Products",
                "Total",
            ],
        )
        print(df)

        for store in self.stores:
            print(f"Store {store.store_id} Total Sales: ${store.get_total_sales()}")

        total_corp_sales = round(
            sum(store.get_total_sales() for store in self.stores), 2
        )
        print(f"Total Corporation Sales: ${total_corp_sales}")


if __name__ == "__main__":
    corp = Corporation("Global Corp")
    for i in range(1, 201):  # Increased to 200 stores
        corp.add_store(Store(i))

    top_15_electronic_brands = [
        "Samsung",
        "Apple",
        "Sony",
        "LG",
        "Panasonic",
        "Dell",
        "HP",
        "Microsoft",
        "Lenovo",
        "Asus",
        "Acer",
        "Xiaomi",
        "Huawei",
        "TCL",
        "Intel",
    ]
    top_15_electronic_items_with_pricing = [
        ("Smartphone", 700),
        ("Laptop", 1200),
        ("Tablet", 350),
        ("Smart TV", 800),
        ("Headphones", 150),
        ("Wireless Earbuds", 120),
        ("Smartwatch", 250),
        ("Gaming Console", 400),
        ("Digital Camera", 600),
        ("Desktop Computer", 1000),
        ("Bluetooth Speaker", 80),
        ("External Hard Drive", 100),
        ("Printer", 150),
        ("Router", 80),
        ("Power Bank", 40),
    ]

    generated_products = [
        Product(
            f"{random.choice(top_15_electronic_brands)} {item}",
            round(price * (1 + random.uniform(-0.1, 0.1)), 2),
        )
        for _ in range(20)
        for item, price in [random.choice(top_15_electronic_items_with_pricing)]
    ]

    customers = [Customer(i) for i in range(1001, 1501)]  # Increased to 500 customers

    for _ in range(500):  # Increased to 500 transactions
        store = random.choice(corp.stores)
        customer = random.choice(customers)
        store.record_order(customer, generated_products)

    corp.generate_sales_report()
