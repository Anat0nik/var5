import os
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Frame
from models import User

class AuthWindow:
    def __init__(self, on_login_success):
        self.window = Tk()
        self.window.title("Авторизация")
        self.window.geometry("400x350")
        self.window.resizable(False, False)
        self.window.configure(bg="#FFFFFF")
        
        # Центрирование окна
        self.window.eval('tk::PlaceWindow . center')
        
        self.on_login_success = on_login_success
        self.users = self.load_users()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Заголовок
        title_label = Label(self.window, text="Интернет-магазин", 
                           font=("Arial", 18, "bold"), bg="#FFFFFF", fg="#1A237E")
        title_label.pack(pady=30)
        
        subtitle_label = Label(self.window, text="Вход в систему", 
                               font=("Arial", 12), bg="#FFFFFF", fg="#666666")
        subtitle_label.pack(pady=(0, 30))
        
        # Форма
        frame = Frame(self.window, bg="#FFFFFF")
        frame.pack(pady=10, padx=40, fill="both")
        
        Label(frame, text="Логин:", font=("Arial", 11), bg="#FFFFFF", 
              anchor="w").grid(row=0, column=0, pady=10, sticky="w")
        self.login_var = StringVar()
        Entry(frame, textvariable=self.login_var, font=("Arial", 11), width=25).grid(row=0, column=1, pady=10, padx=10)
        
        Label(frame, text="Пароль:", font=("Arial", 11), bg="#FFFFFF", 
              anchor="w").grid(row=1, column=0, pady=10, sticky="w")
        self.password_var = StringVar()
        Entry(frame, textvariable=self.password_var, show="*", font=("Arial", 11), width=25).grid(row=1, column=1, pady=10, padx=10)
        
        # Кнопки
        btn_frame = Frame(self.window, bg="#FFFFFF")
        btn_frame.pack(pady=30)
        
        Button(btn_frame, text="Войти", command=self.login, 
               bg="#FF5722", fg="white", font=("Arial", 11, "bold"), 
               padx=30, pady=8, cursor="hand2").pack(side="left", padx=10)
        Button(btn_frame, text="Выход", command=self.window.quit, 
               bg="#FF5722", fg="white", font=("Arial", 11, "bold"), 
               padx=30, pady=8, cursor="hand2").pack(side="left", padx=10)
    
    def load_users(self):
        users = []
        if os.path.exists("users.txt"):
            with open("users.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(";")
                        if len(parts) == 3:
                            users.append(User(parts[0], parts[1], parts[2]))
        else:
            # Создаем файл с тестовыми пользователями
            users.append(User("admin", "admin123", "Иванов Иван"))
            users.append(User("user1", "pass123", "Петров Петр"))
            with open("users.txt", "w", encoding="utf-8") as f:
                f.write("admin;admin123;Иванов Иван\n")
                f.write("user1;pass123;Петров Петр\n")
        return users
    
    def login(self):
        login = self.login_var.get()
        password = self.password_var.get()
        
        for user in self.users:
            if user.login == login and user.password == password:
                self.window.destroy()
                self.on_login_success(user.full_name)
                return
        
        messagebox.showerror("Ошибка", "Неверный логин или пароль!")
    
    def run(self):
        self.window.mainloop()
