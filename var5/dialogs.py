import re
from datetime import datetime
from tkinter import Toplevel, Label, Entry, Button, StringVar, messagebox, Frame
from tkinter import ttk
from models import Customer, Product, Order
from data_manager import DataManager

class CustomerDialog:
    def __init__(self, parent, data_model, customer=None):
        self.dialog = Toplevel(parent)
        self.dialog.title("Покупатель")
        self.dialog.geometry("450x500")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg="#FFFFFF")
        
        self.data_model = data_model
        self.customer = customer
        self.result = None
        
        self.setup_ui()
        
    def setup_ui(self):
        title = Label(self.dialog, text="Данные покупателя", font=("Arial", 14, "bold"),
                     bg="#FFFFFF", fg="#1A237E")
        title.pack(pady=20)
        
        main_frame = Frame(self.dialog, bg="#FFFFFF")
        main_frame.pack(padx=30, pady=10, fill="both", expand=True)
        
        Label(main_frame, text="Фамилия:", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=0, column=0, pady=8, sticky="w")
        self.last_name_var = StringVar(value=self.customer.last_name if self.customer else "")
        Entry(main_frame, textvariable=self.last_name_var, font=("Arial", 10), width=30).grid(row=0, column=1, pady=8, padx=10)
        
        Label(main_frame, text="Имя:", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=1, column=0, pady=8, sticky="w")
        self.first_name_var = StringVar(value=self.customer.first_name if self.customer else "")
        Entry(main_frame, textvariable=self.first_name_var, font=("Arial", 10), width=30).grid(row=1, column=1, pady=8, padx=10)
        
        Label(main_frame, text="Email:", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=2, column=0, pady=8, sticky="w")
        self.email_var = StringVar(value=self.customer.email if self.customer else "")
        Entry(main_frame, textvariable=self.email_var, font=("Arial", 10), width=30).grid(row=2, column=1, pady=8, padx=10)
        
        Label(main_frame, text="Телефон (11 цифр, с 8):", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=3, column=0, pady=8, sticky="w")
        self.phone_var = StringVar(value=self.customer.phone if self.customer else "")
        Entry(main_frame, textvariable=self.phone_var, font=("Arial", 10), width=30).grid(row=3, column=1, pady=8, padx=10)
        
        Label(main_frame, text="Город:", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=4, column=0, pady=8, sticky="w")
        self.city_var = StringVar(value=self.customer.city if self.customer else "")
        Entry(main_frame, textvariable=self.city_var, font=("Arial", 10), width=30).grid(row=4, column=1, pady=8, padx=10)
        
        btn_frame = Frame(self.dialog, bg="#FFFFFF")
        btn_frame.pack(pady=20)
        
        Button(btn_frame, text="Сохранить", command=self.save,
               bg="#FF5722", fg="white", font=("Arial", 10, "bold"),
               padx=20, pady=5, cursor="hand2").pack(side="left", padx=10)
        Button(btn_frame, text="Отмена", command=self.dialog.destroy,
               bg="#FF5722", fg="white", font=("Arial", 10, "bold"),
               padx=20, pady=5, cursor="hand2").pack(side="left", padx=10)
    
    def validate_phone(self, phone):
        return len(phone) == 11 and phone.isdigit() and phone[0] == '8'
    
    def validate_email(self, email):
        return '@' in email and '.' in email.split('@')[-1]
    
    def save(self):
        last_name = self.last_name_var.get().strip()
        first_name = self.first_name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        city = self.city_var.get().strip()
        
        if not last_name or not first_name:
            messagebox.showerror("Ошибка", "Заполните фамилию и имя!")
            return
        
        if not self.validate_phone(phone):
            messagebox.showerror("Ошибка", "Телефон должен содержать 11 цифр и начинаться с 8!")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Ошибка", "Email должен содержать @ и точку после него!")
            return
        
        self.result = Customer(
            id=self.customer.id if self.customer else self.data_model.next_customer_id,
            last_name=last_name,
            first_name=first_name,
            email=email,
            phone=phone,
            city=city
        )
        self.dialog.destroy()

class ProductDialog:
    def __init__(self, parent, data_model, product=None):
        self.dialog = Toplevel(parent)
        self.dialog.title("Товар")
        self.dialog.geometry("450x480")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg="#FFFFFF")
        
        self.data_model = data_model
        self.product = product
        self.result = None
        self.categories = ["Смартфоны", "Ноутбуки", "Планшеты", "Наушники", "Аксессуары", "Умные часы"]
        
        self.setup_ui()
    
    def setup_ui(self):
        title = Label(self.dialog, text="Данные товара", font=("Arial", 14, "bold"),
                     bg="#FFFFFF", fg="#1A237E")
        title.pack(pady=20)
        
        main_frame = Frame(self.dialog, bg="#FFFFFF")
        main_frame.pack(padx=30, pady=10, fill="both", expand=True)
        
        Label(main_frame, text="Наименование:", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=0, column=0, pady=8, sticky="w")
        self.name_var = StringVar(value=self.product.name if self.product else "")
        Entry(main_frame, textvariable=self.name_var, font=("Arial", 10), width=30).grid(row=0, column=1, pady=8, padx=10)
        
        Label(main_frame, text="Категория:", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=1, column=0, pady=8, sticky="w")
        self.category_var = StringVar(value=self.product.category if self.product else self.categories[0])
        ttk.Combobox(main_frame, textvariable=self.category_var, values=self.categories, 
                    state="readonly", width=27, font=("Arial", 10)).grid(row=1, column=1, pady=8, padx=10)
        
        Label(main_frame, text="Цена (руб.):", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=2, column=0, pady=8, sticky="w")
        self.price_var = StringVar(value=str(self.product.price) if self.product else "")
        Entry(main_frame, textvariable=self.price_var, font=("Arial", 10), width=30).grid(row=2, column=1, pady=8, padx=10)
        
        Label(main_frame, text="Вес (кг):", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=3, column=0, pady=8, sticky="w")
        self.weight_var = StringVar(value=str(self.product.weight) if self.product else "")
        Entry(main_frame, textvariable=self.weight_var, font=("Arial", 10), width=30).grid(row=3, column=1, pady=8, padx=10)
        
        btn_frame = Frame(self.dialog, bg="#FFFFFF")
        btn_frame.pack(pady=20)
        
        Button(btn_frame, text="Сохранить", command=self.save,
               bg="#FF5722", fg="white", font=("Arial", 10, "bold"),
               padx=20, pady=5, cursor="hand2").pack(side="left", padx=10)
        Button(btn_frame, text="Отмена", command=self.dialog.destroy,
               bg="#FF5722", fg="white", font=("Arial", 10, "bold"),
               padx=20, pady=5, cursor="hand2").pack(side="left", padx=10)
    
    def save(self):
        try:
            name = self.name_var.get().strip()
            price = float(self.price_var.get())
            weight = float(self.weight_var.get())
            
            if not name:
                messagebox.showerror("Ошибка", "Введите наименование товара!")
                return
            
            if price <= 0:
                messagebox.showerror("Ошибка", "Цена должна быть положительной!")
                return
            
            if weight <= 0:
                messagebox.showerror("Ошибка", "Вес должен быть положительным!")
                return
            
            self.result = Product(
                id=self.product.id if self.product else self.data_model.next_product_id,
                name=name,
                category=self.category_var.get(),
                price=price,
                weight=weight
            )
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Ошибка", "Цена и вес должны быть числами!")

class OrderDialog:
    DELIVERY_COST = 500
    
    def __init__(self, parent, data_model, order=None):
        self.dialog = Toplevel(parent)
        self.dialog.title("Заказ")
        self.dialog.geometry("550x650")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg="#FFFFFF")
        
        self.data_model = data_model
        self.order = order
        self.result = None
        self.statuses = ["Оформлен", "В сборке", "В пути", "Доставлен", "Отменён"]
        
        self.setup_ui()
    
    def setup_ui(self):
        title = Label(self.dialog, text="Данные заказа", font=("Arial", 14, "bold"),
                     bg="#FFFFFF", fg="#1A237E")
        title.pack(pady=20)
        
        main_frame = Frame(self.dialog, bg="#FFFFFF")
        main_frame.pack(padx=30, pady=10, fill="both", expand=True)
        
        Label(main_frame, text="Покупатель:", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=0, column=0, pady=10, sticky="w")
        self.customer_var = StringVar()
        customer_values = [f"{c.id} - {c.last_name} {c.first_name} ({c.city})" for c in self.data_model.customers]
        self.customer_combo = ttk.Combobox(main_frame, textvariable=self.customer_var, 
                                           values=customer_values, state="readonly", width=40,
                                           font=("Arial", 10))
        self.customer_combo.grid(row=0, column=1, pady=10, padx=10)
        if self.order:
            customer = next((c for c in self.data_model.customers if c.id == self.order.customer_id), None)
            if customer:
                self.customer_combo.set(f"{customer.id} - {customer.last_name} {customer.first_name} ({customer.city})")
        
        Label(main_frame, text="Товар:", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=1, column=0, pady=10, sticky="w")
        self.product_var = StringVar()
        product_values = [f"{p.id} - {p.name} ({p.price:.2f} руб.)" for p in self.data_model.products]
        self.product_combo = ttk.Combobox(main_frame, textvariable=self.product_var, 
                                          values=product_values, state="readonly", width=40,
                                          font=("Arial", 10))
        self.product_combo.grid(row=1, column=1, pady=10, padx=10)
        self.product_combo.bind('<<ComboboxSelected>>', self.calculate_sum)
        if self.order:
            product = next((p for p in self.data_model.products if p.id == self.order.product_id), None)
            if product:
                self.product_combo.set(f"{product.id} - {product.name} ({product.price:.2f} руб.)")
        
        Label(main_frame, text="Количество (1-100):", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=2, column=0, pady=10, sticky="w")
        self.quantity_var = StringVar(value=str(self.order.quantity) if self.order else "1")
        self.quantity_entry = Entry(main_frame, textvariable=self.quantity_var, font=("Arial", 10), width=38)
        self.quantity_entry.grid(row=2, column=1, pady=10, padx=10)
        self.quantity_var.trace('w', lambda *args: self.calculate_sum())
        
        Label(main_frame, text="Дата заказа:", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=3, column=0, pady=10, sticky="w")
        self.date_var = StringVar(value=self.order.order_date if self.order else datetime.now().strftime("%Y-%m-%d"))
        Entry(main_frame, textvariable=self.date_var, font=("Arial", 10), width=38).grid(row=3, column=1, pady=10, padx=10)
        
        Label(main_frame, text="Адрес доставки:", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=4, column=0, pady=10, sticky="w")
        self.address_var = StringVar(value=self.order.delivery_address if self.order else "")
        Entry(main_frame, textvariable=self.address_var, font=("Arial", 10), width=38).grid(row=4, column=1, pady=10, padx=10)
        
        Label(main_frame, text="Статус:", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=5, column=0, pady=10, sticky="w")
        self.status_var = StringVar(value=self.order.status if self.order else self.statuses[0])
        ttk.Combobox(main_frame, textvariable=self.status_var, values=self.statuses, 
                    state="readonly", width=37, font=("Arial", 10)).grid(row=5, column=1, pady=10, padx=10)
        
        Label(main_frame, text="Сумма (руб.):", font=("Arial", 10), bg="#FFFFFF", 
              anchor="w").grid(row=6, column=0, pady=10, sticky="w")
        self.sum_var = StringVar(value="0.00")
        sum_entry = Entry(main_frame, textvariable=self.sum_var, state="readonly", 
                          font=("Arial", 10, "bold"), width=38, readonlybackground="#F0F0F0")
        sum_entry.grid(row=6, column=1, pady=10, padx=10)
        
        btn_frame = Frame(self.dialog, bg="#FFFFFF")
        btn_frame.pack(pady=30)
        
        Button(btn_frame, text="✅ Сохранить", command=self.save,
               bg="#FF5722", fg="white", font=("Arial", 10, "bold"),
               padx=25, pady=8, cursor="hand2").pack(side="left", padx=15)
        Button(btn_frame, text="❌ Отмена", command=self.dialog.destroy,
               bg="#FF5722", fg="white", font=("Arial", 10, "bold"),
               padx=25, pady=8, cursor="hand2").pack(side="left", padx=15)
        
        self.calculate_sum()
    
    def calculate_sum(self, *args):
        try:
            product_text = self.product_combo.get()
            quantity_str = self.quantity_var.get()
            
            if product_text and quantity_str:
                quantity = int(quantity_str) if quantity_str.isdigit() else 0
                
                if 1 <= quantity <= 100:
                    price_match = re.search(r'\((\d+\.?\d*)\s*руб', product_text)
                    if price_match:
                        price = float(price_match.group(1))
                        total = price * quantity + self.DELIVERY_COST
                        self.sum_var.set(f"{total:.2f}")
                        return
            self.sum_var.set("0.00")
        except:
            self.sum_var.set("0.00")
    
    def save(self):
        if not self.customer_combo.get():
            messagebox.showerror("Ошибка", "Выберите покупателя!")
            return
        
        if not self.product_combo.get():
            messagebox.showerror("Ошибка", "Выберите товар!")
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity < 1 or quantity > 100:
                messagebox.showerror("Ошибка", "Количество должно быть от 1 до 100!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть целым числом!")
            return
        
        if not self.address_var.get().strip():
            messagebox.showerror("Ошибка", "Введите адрес доставки!")
            return
        
        try:
            customer_id = int(self.customer_combo.get().split(" - ")[0])
            product_id = int(self.product_combo.get().split(" - ")[0])
        except:
            messagebox.showerror("Ошибка", "Ошибка при определении ID!")
            return
        
        self.result = Order(
            id=self.order.id if self.order else self.data_model.next_order_id,
            customer_id=customer_id,
            product_id=product_id,
            quantity=quantity,
            delivery_address=self.address_var.get().strip(),
            status=self.status_var.get(),
            order_date=self.date_var.get(),
            sum=float(self.sum_var.get())
        )
        self.dialog.destroy()
