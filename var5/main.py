from auth import AuthWindow
from main_window import MainWindow

def main():
    def start_main_app(user_name):
        app = MainWindow(user_name)
        app.run()
    
    auth = AuthWindow(start_main_app)
    auth.run()

if __name__ == "__main__":
    main()
