from dataclasses import dataclass
from typing import List

@dataclass
class User:
    login: str
    password: str
    full_name: str

@dataclass
class Customer:
    id: int
    last_name: str
    first_name: str
    email: str
    phone: str
    city: str

@dataclass
class Product:
    id: int
    name: str
    category: str
    price: float
    weight: float

@dataclass
class Order:
    id: int
    customer_id: int
    product_id: int
    quantity: int
    delivery_address: str
    status: str
    order_date: str
    sum: float = 0.0

class DataModel:
    def __init__(self):
        self.customers: List[Customer] = []
        self.products: List[Product] = []
        self.orders: List[Order] = []
        self.next_customer_id = 1
        self.next_product_id = 1
        self.next_order_id = 1
        self.load_test_data()
    
    def load_test_data(self):
        # Тестовые покупатели
        self.customers.append(Customer(1, "Иванов", "Иван", "ivan@test.ru", "89123456789", "Москва"))
        self.customers.append(Customer(2, "Петров", "Петр", "petr@test.ru", "89234567890", "Санкт-Петербург"))
        self.customers.append(Customer(3, "Сидорова", "Анна", "anna@test.ru", "89345678901", "Новосибирск"))
        self.next_customer_id = 4
        
        # Тестовые товары
        self.products.append(Product(1, "iPhone 15 Pro", "Смартфоны", 99990, 0.187))
        self.products.append(Product(2, "Samsung Galaxy S24", "Смартфоны", 89990, 0.196))
        self.products.append(Product(3, "MacBook Pro 14", "Ноутбуки", 199990, 1.6))
        self.products.append(Product(4, "Sony WH-1000XM5", "Наушники", 34990, 0.25))
        self.products.append(Product(5, "iPad Air", "Планшеты", 69990, 0.462))
        self.next_product_id = 6
        
        # Тестовые заказы
        self.orders.append(Order(1, 1, 1, 1, "Москва, ул. Тверская 15", "Оформлен", 
                                "2024-01-10", 100490))
        self.orders.append(Order(2, 2, 3, 1, "СПб, Невский пр. 25", "В сборке", 
                                "2024-01-12", 200490))
        self.orders.append(Order(3, 1, 4, 2, "Москва, ул. Арбат 10", "Доставлен", 
                                "2024-01-08", 70480))
        self.next_order_id = 4
