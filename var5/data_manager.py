import csv
from datetime import datetime
from models import Order

class DataManager:
    DELIVERY_COST = 500
    
    @staticmethod
    def calculate_sum(price: float, quantity: int) -> float:
        return price * quantity + DataManager.DELIVERY_COST
    
    @staticmethod
    def calculate_average_sum(orders, data_model):
        if not orders:
            return 0
        total = 0
        for order in orders:
            product = next((p for p in data_model.products if p.id == order.product_id), None)
            if product:
                total += product.price * order.quantity + DataManager.DELIVERY_COST
        return total / len(orders)
    
    @staticmethod
    def calculate_deviation(order_sum, average_sum):
        return order_sum - average_sum
    
    @staticmethod
    def save_orders_to_csv(filename, orders, data_model):
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            for order in orders:
                customer = next((c for c in data_model.customers if c.id == order.customer_id), None)
                product = next((p for p in data_model.products if p.id == order.product_id), None)
                
                if customer and product:
                    writer.writerow([
                        order.id, order.customer_id, customer.last_name, customer.first_name,
                        customer.email, order.product_id, product.name, product.category,
                        product.price, order.quantity, order.delivery_address, order.status,
                        product.price * order.quantity + DataManager.DELIVERY_COST
                    ])
    
    @staticmethod
    def load_orders_from_csv(filename, data_model):
        orders = []
        if not os.path.exists(filename):
            return orders
        
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            max_id = 0
            for row in reader:
                if len(row) >= 13:
                    try:
                        customer_exists = any(c.id == int(row[1]) for c in data_model.customers)
                        product_exists = any(p.id == int(row[5]) for p in data_model.products)
                        
                        if customer_exists and product_exists:
                            order = Order(
                                id=int(row[0]),
                                customer_id=int(row[1]),
                                product_id=int(row[5]),
                                quantity=int(row[9]),
                                delivery_address=row[10],
                                status=row[11],
                                order_date=datetime.now().strftime("%Y-%m-%d"),
                                sum=float(row[12])
                            )
                            orders.append(order)
                            max_id = max(max_id, order.id)
                    except (ValueError, IndexError):
                        continue
        return orders, max_id
