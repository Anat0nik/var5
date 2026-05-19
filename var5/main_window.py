import os
from datetime import datetime
from tkinter import Tk, Menu, filedialog, messagebox, ttk, Frame, Label, Button
from tkinter import StringVar
from tkinter.ttk import Notebook, Treeview, Scrollbar
from models import DataModel, Customer, Product, Order
from data_manager import DataManager
from dialogs import CustomerDialog, ProductDialog, OrderDialog

class MainWindow:
    DELIVERY_COST = 500
    
    def __init__(self, user_name):
        self.window = Tk()
        self.window.title("Интернет-магазин: учет заказов")
        self.window.geometry("980x820")
        self.window.resizable(False, False)
        self.window.configure(bg="#FFFFFF")
        
        try:
            self.window.iconbitmap("icon.ico")
        except:
            pass
        
        self.data_model = DataModel()
        self.user_name = user_name
        
        self.setup_ui()
        self.update_customers_table()
        self.update_products_table()
        self.update_orders_table()
    
    def setup_ui(self):
        # Меню
        menubar = Menu(self.window)
        self.window.config(menu=menubar)
        
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="💾 Сохранить заказы как...", command=self.save_orders)
        file_menu.add_command(label="📂 Открыть заказы...", command=self.load_orders)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Выход", command=self.window.quit)
        
        # Логотип (простой символ)
        self.add_logo()
        
        # Вкладки
        style = ttk.Style()
        style.configure("TNotebook", background="#FFFFFF", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Arial", 11), padding=[20, 8])
        style.map("TNotebook.Tab", background=[("selected", "#1A237E")], 
                  foreground=[("selected", "#FFD54F"), ("!selected", "#1A237E")])
        
        self.notebook = Notebook(self.window)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(10, 5))
        
        self.orders_frame = Frame(self.notebook, bg="#FFFFFF")
        self.notebook.add(self.orders_frame, text="📦 Заказы")
        self.setup_orders_tab()
        
        self.customers_frame = Frame(self.notebook, bg="#FFFFFF")
        self.notebook.add(self.customers_frame, text="👥 Покупатели")
        self.setup_customers_tab()
        
        self.products_frame = Frame(self.notebook, bg="#FFFFFF")
        self.notebook.add(self.products_frame, text="📱 Товары")
        self.setup_products_tab()
        
        self.status_bar = Label(self.window, text=f"👤 Пользователь: {self.user_name}", 
                                bd=1, relief="sunken", anchor="w", bg="#1A237E", 
                                fg="#FFD54F", font=("Arial", 9), padx=5)
        self.status_bar.pack(side="bottom", fill="x")
    
    def add_logo(self):
        """Логотип из символов (не требует файлов)"""
        logo_frame = Frame(self.window, width=140, height=80, bg="#1A237E", 
                          highlightbackground="#FF5722", highlightthickness=2)
        logo_frame.place(x=830, y=10)
        logo_frame.pack_propagate(False)
        
        # Главный символ
        Label(logo_frame, text="🖥️", font=("Segoe UI Emoji", 40), 
              bg="#1A237E", fg="#FFD54F").pack(expand=True, pady=(5, 0))
        Label(logo_frame, text="TECH", font=("Arial", 9, "bold"), 
              bg="#1A237E", fg="#FFD54F").pack()
    
    def setup_customers_tab(self):
        btn_frame = Frame(self.customers_frame, bg="#FFFFFF")
        btn_frame.pack(pady=10)
        Button(btn_frame, text="➕ Добавить покупателя", command=self.add_customer,
               bg="#FF5722", fg="white", font=("Arial", 10), padx=20, pady=5,
               cursor="hand2").pack()
        
        frame = Frame(self.customers_frame, bg="#FFFFFF")
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        scroll_y = Scrollbar(frame)
        scroll_y.pack(side="right", fill="y")
        
        self.customers_tree = Treeview(frame, columns=("last_name", "first_name", "email", "phone", "city"),
                                       show="headings", yscrollcommand=scroll_y.set,
                                       height=25, selectmode="browse")
        scroll_y.config(command=self.customers_tree.yview)
        
        self.customers_tree.heading("last_name", text="Фамилия")
        self.customers_tree.heading("first_name", text="Имя")
        self.customers_tree.heading("email", text="Email")
        self.customers_tree.heading("phone", text="Телефон")
        self.customers_tree.heading("city", text="Город")
        
        self.customers_tree.column("last_name", width=150)
        self.customers_tree.column("first_name", width=150)
        self.customers_tree.column("email", width=220)
        self.customers_tree.column("phone", width=120)
        self.customers_tree.column("city", width=150)
        
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 9))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
        self.customers_tree.pack(fill="both", expand=True)
        
        self.customers_menu = Menu(self.customers_tree, tearoff=0)
        self.customers_menu.add_command(label="✏️ Редактировать", command=self.edit_customer)
        self.customers_menu.add_command(label="🗑️ Удалить", command=self.delete_customer)
        self.customers_menu.add_command(label="📋 Дублировать", command=self.duplicate_customer)
        self.customers_tree.bind("<Button-3>", self.show_customers_menu)
    
    def setup_products_tab(self):
        btn_frame = Frame(self.products_frame, bg="#FFFFFF")
        btn_frame.pack(pady=10)
        Button(btn_frame, text="➕ Добавить товар", command=self.add_product,
               bg="#FF5722", fg="white", font=("Arial", 10), padx=20, pady=5,
               cursor="hand2").pack()
        
        frame = Frame(self.products_frame, bg="#FFFFFF")
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        scroll_y = Scrollbar(frame)
        scroll_y.pack(side="right", fill="y")
        
        self.products_tree = Treeview(frame, columns=("name", "category", "price", "weight"),
                                      show="headings", yscrollcommand=scroll_y.set,
                                      height=25, selectmode="browse")
        scroll_y.config(command=self.products_tree.yview)
        
        self.products_tree.heading("name", text="Наименование")
        self.products_tree.heading("category", text="Категория")
        self.products_tree.heading("price", text="Цена (руб.)")
        self.products_tree.heading("weight", text="Вес (кг)")
        
        self.products_tree.column("name", width=300)
        self.products_tree.column("category", width=150)
        self.products_tree.column("price", width=120)
        self.products_tree.column("weight", width=100)
        
        self.products_tree.pack(fill="both", expand=True)
        
        self.products_menu = Menu(self.products_tree, tearoff=0)
        self.products_menu.add_command(label="✏️ Редактировать", command=self.edit_product)
        self.products_menu.add_command(label="🗑️ Удалить", command=self.delete_product)
        self.products_menu.add_command(label="📋 Дублировать", command=self.duplicate_product)
        self.products_tree.bind("<Button-3>", self.show_products_menu)
    
    def setup_orders_tab(self):
        btn_frame = Frame(self.orders_frame, bg="#FFFFFF")
        btn_frame.pack(pady=10)
        Button(btn_frame, text="➕ Добавить заказ", command=self.add_order,
               bg="#FF5722", fg="white", font=("Arial", 10), padx=20, pady=5,
               cursor="hand2").pack()
        
        frame = Frame(self.orders_frame, bg="#FFFFFF")
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        scroll_y = Scrollbar(frame)
        scroll_y.pack(side="right", fill="y")
        
        self.orders_tree = Treeview(frame, columns=("id", "customer", "product", "quantity", 
                                                     "address", "status", "sum", "deviation"),
                                    show="headings", yscrollcommand=scroll_y.set,
                                    height=20, selectmode="browse")
        scroll_y.config(command=self.orders_tree.yview)
        
        self.orders_tree.heading("id", text="ID")
        self.orders_tree.heading("customer", text="Покупатель")
        self.orders_tree.heading("product", text="Товар")
        self.orders_tree.heading("quantity", text="Кол-во")
        self.orders_tree.heading("address", text="Адрес доставки")
        self.orders_tree.heading("status", text="Статус")
        self.orders_tree.heading("sum", text="Сумма (руб.)")
        self.orders_tree.heading("deviation", text="Отклонение от среднего")
        
        self.orders_tree.column("id", width=50)
        self.orders_tree.column("customer", width=140)
        self.orders_tree.column("product", width=140)
        self.orders_tree.column("quantity", width=60)
        self.orders_tree.column("address", width=160)
        self.orders_tree.column("status", width=100)
        self.orders_tree.column("sum", width=100)
        self.orders_tree.column("deviation", width=150)
        
        self.orders_tree.pack(fill="both", expand=True)
        
        self.orders_menu = Menu(self.orders_tree, tearoff=0)
        self.orders_menu.add_command(label="✏️ Редактировать", command=self.edit_order)
        self.orders_menu.add_command(label="🗑️ Удалить", command=self.delete_order)
        self.orders_menu.add_command(label="📋 Дублировать", command=self.duplicate_order)
        self.orders_tree.bind("<Button-3>", self.show_orders_menu)
    
    def update_customers_table(self):
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
        for customer in self.data_model.customers:
            self.customers_tree.insert("", "end", values=(
                customer.last_name, customer.first_name, customer.email,
                customer.phone, customer.city
            ))
    
    def update_products_table(self):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        for product in self.data_model.products:
            self.products_tree.insert("", "end", values=(
                product.name, product.category, f"{product.price:.2f}", f"{product.weight:.3f}"
            ))
    
    def calculate_average_sum(self):
        if not self.data_model.orders:
            return 0
        total = 0
        for order in self.data_model.orders:
            product = next((p for p in self.data_model.products if p.id == order.product_id), None)
            if product:
                total += product.price * order.quantity + self.DELIVERY_COST
        return total / len(self.data_model.orders)
    
    def update_orders_table(self):
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        average_sum = self.calculate_average_sum()
        for order in self.data_model.orders:
            customer = next((c for c in self.data_model.customers if c.id == order.customer_id), None)
            product = next((p for p in self.data_model.products if p.id == order.product_id), None)
            if customer and product:
                order_sum = product.price * order.quantity + self.DELIVERY_COST
                deviation = order_sum - average_sum
                address_display = order.delivery_address[:25] + "..." if len(order.delivery_address) > 25 else order.delivery_address
                self.orders_tree.insert("", "end", values=(
                    order.id, f"{customer.last_name} {customer.first_name}", product.name,
                    order.quantity, address_display, order.status, 
                    f"{order_sum:.2f}", f"{deviation:+.2f}"
                ))
    
    def show_customers_menu(self, event):
        item = self.customers_tree.identify_row(event.y)
        if item:
            self.customers_tree.selection_set(item)
            self.customers_menu.post(event.x_root, event.y_root)
    
    def show_products_menu(self, event):
        item = self.products_tree.identify_row(event.y)
        if item:
            self.products_tree.selection_set(item)
            self.products_menu.post(event.x_root, event.y_root)
    
    def show_orders_menu(self, event):
        item = self.orders_tree.identify_row(event.y)
        if item:
            self.orders_tree.selection_set(item)
            self.orders_menu.post(event.x_root, event.y_root)
    
    def add_customer(self):
        dialog = CustomerDialog(self.window, self.data_model)
        self.window.wait_window(dialog.dialog)
        if dialog.result:
            self.data_model.customers.append(dialog.result)
            self.data_model.next_customer_id += 1
            self.update_customers_table()
    
    def edit_customer(self):
        selected = self.customers_tree.selection()
        if selected:
            values = self.customers_tree.item(selected[0])['values']
            customer = next((c for c in self.data_model.customers 
                           if c.last_name == values[0] and c.first_name == values[1]), None)
            if customer:
                dialog = CustomerDialog(self.window, self.data_model, customer)
                self.window.wait_window(dialog.dialog)
                if dialog.result:
                    idx = self.data_model.customers.index(customer)
                    self.data_model.customers[idx] = dialog.result
                    self.update_customers_table()
    
    def delete_customer(self):
        selected = self.customers_tree.selection()
        if selected and messagebox.askyesno("Подтверждение", "Удалить покупателя?"):
            values = self.customers_tree.item(selected[0])['values']
            self.data_model.customers = [c for c in self.data_model.customers 
                                        if not (c.last_name == values[0] and c.first_name == values[1])]
            self.update_customers_table()
            self.update_orders_table()
    
    def duplicate_customer(self):
        selected = self.customers_tree.selection()
        if selected:
            values = self.customers_tree.item(selected[0])['values']
            customer = next((c for c in self.data_model.customers 
                           if c.last_name == values[0] and c.first_name == values[1]), None)
            if customer:
                new_customer = Customer(
                    id=self.data_model.next_customer_id,
                    last_name=customer.last_name + " (копия)",
                    first_name=customer.first_name,
                    email=customer.email,
                    phone=customer.phone,
                    city=customer.city
                )
                self.data_model.customers.append(new_customer)
                self.data_model.next_customer_id += 1
                self.update_customers_table()
    
    def add_product(self):
        dialog = ProductDialog(self.window, self.data_model)
        self.window.wait_window(dialog.dialog)
        if dialog.result:
            self.data_model.products.append(dialog.result)
            self.data_model.next_product_id += 1
            self.update_products_table()
    
    def edit_product(self):
        selected = self.products_tree.selection()
        if selected:
            values = self.products_tree.item(selected[0])['values']
            product = next((p for p in self.data_model.products 
                          if p.name == values[0]), None)
            if product:
                dialog = ProductDialog(self.window, self.data_model, product)
                self.window.wait_window(dialog.dialog)
                if dialog.result:
                    idx = self.data_model.products.index(product)
                    self.data_model.products[idx] = dialog.result
                    self.update_products_table()
    
    def delete_product(self):
        selected = self.products_tree.selection()
        if selected and messagebox.askyesno("Подтверждение", "Удалить товар?"):
            values = self.products_tree.item(selected[0])['values']
            self.data_model.products = [p for p in self.data_model.products 
                                       if p.name != values[0]]
            self.update_products_table()
    
    def duplicate_product(self):
        selected = self.products_tree.selection()
        if selected:
            values = self.products_tree.item(selected[0])['values']
            product = next((p for p in self.data_model.products 
                          if p.name == values[0]), None)
            if product:
                new_product = Product(
                    id=self.data_model.next_product_id,
                    name=product.name + " (копия)",
                    category=product.category,
                    price=product.price,
                    weight=product.weight
                )
                self.data_model.products.append(new_product)
                self.data_model.next_product_id += 1
                self.update_products_table()
    
    def add_order(self):
        if not self.data_model.customers:
            messagebox.showwarning("Предупреждение", "Сначала добавьте покупателей!")
            return
        if not self.data_model.products:
            messagebox.showwarning("Предупреждение", "Сначала добавьте товары!")
            return
        dialog = OrderDialog(self.window, self.data_model)
        self.window.wait_window(dialog.dialog)
        if dialog.result:
            self.data_model.orders.append(dialog.result)
            self.data_model.next_order_id += 1
            self.update_orders_table()
            messagebox.showinfo("Успех", "Заказ успешно создан!")
    
    def edit_order(self):
        selected = self.orders_tree.selection()
        if selected:
            values = self.orders_tree.item(selected[0])['values']
            order_id = values[0]
            order = next((o for o in self.data_model.orders if o.id == order_id), None)
            if order:
                dialog = OrderDialog(self.window, self.data_model, order)
                self.window.wait_window(dialog.dialog)
                if dialog.result:
                    idx = self.data_model.orders.index(order)
                    self.data_model.orders[idx] = dialog.result
                    self.update_orders_table()
                    messagebox.showinfo("Успех", "Заказ успешно обновлен!")
    
    def delete_order(self):
        selected = self.orders_tree.selection()
        if selected and messagebox.askyesno("Подтверждение", "Удалить заказ?"):
            values = self.orders_tree.item(selected[0])['values']
            order_id = values[0]
            self.data_model.orders = [o for o in self.data_model.orders if o.id != order_id]
            self.update_orders_table()
    
    def duplicate_order(self):
        selected = self.orders_tree.selection()
        if selected:
            values = self.orders_tree.item(selected[0])['values']
            order_id = values[0]
            order = next((o for o in self.data_model.orders if o.id == order_id), None)
            if order:
                new_order = Order(
                    id=self.data_model.next_order_id,
                    customer_id=order.customer_id,
                    product_id=order.product_id,
                    quantity=order.quantity,
                    delivery_address=order.delivery_address,
                    status="Оформлен",
                    order_date=datetime.now().strftime("%Y-%m-%d"),
                    sum=order.sum
                )
                self.data_model.orders.append(new_order)
                self.data_model.next_order_id += 1
                self.update_orders_table()
                messagebox.showinfo("Успех", "Заказ дублирован!")
    
    def save_orders(self):
        if not self.data_model.orders:
            messagebox.showwarning("Предупреждение", "Нет заказов для сохранения!")
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Сохранить заказы"
        )
        if filename:
            DataManager.save_orders_to_csv(filename, self.data_model.orders, self.data_model)
            messagebox.showinfo("Успех", f"Заказы сохранены в файл {filename}")
    
    def load_orders(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Открыть заказы"
        )
        if filename:
            try:
                orders, max_id = DataManager.load_orders_from_csv(filename, self.data_model)
                if orders:
                    self.data_model.orders = orders
                    self.data_model.next_order_id = max_id + 1
                    self.update_orders_table()
                    messagebox.showinfo("Успех", f"Загружено {len(orders)} заказов!")
                else:
                    messagebox.showwarning("Предупреждение", "Не найдено подходящих заказов для загрузки")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при загрузке файла: {str(e)}")
    
    def run(self):
        self.window.mainloop()
