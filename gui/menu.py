import tkinter as tk
from tkinter import ttk, messagebox
import sys
from gui.main_app import App
# from gui.help_app import HelpApp


class MenuApp(tk.Tk):
    """Главное меню приложения."""
    
    def __init__(self):
        super().__init__()
        self.app = None


        self.title('Учёт показаний счётчиков - Главное меню')
        self.geometry('300x200')
        self.resizable(False, False)
        
        # Центрируем окно
        self.center_window()
        
        self.create_widgets()
    
    def center_window(self):
        """Размещает окно по центру экрана."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Создаёт элементы интерфейса главного меню."""
        # Заголовок
        title_label = ttk.Label(
            self, 
            text='Программа учёта показаний счётчиков',
            font=('Arial', 12, 'bold')
        )
        title_label.pack(pady=20)
        
        # Фрейм для кнопок
        btn_frame = ttk.Frame(self)
        btn_frame.pack(expand=True)
        
        # Кнопки
        ttk.Button(btn_frame, text='Работать', command=self.go_main, width=20).pack(side='top', pady=5)
        
        ttk.Button(btn_frame, text='Помощь', command=self.go_help, width=20).pack(side='top', pady=5)
        
        ttk.Button(btn_frame, text='Выход', command=self.go_exit, width=20).pack(side='top', pady=5)
    
    def go_main(self):
        """Открывает главное рабочее окно с таблицей."""
        # Создаём рабочее окно
        if self.app == None:
            self.app = App('data.txt', self)

    def go_help(self):
        """Открывает окно справки."""
        pass
        # HelpApp()

    def go_exit(self):
        """Завершает работу приложения."""
        if messagebox.askyesno('Подтверждение', 'Вы действительно хотите выйти?'):
            self.quit()
            sys.exit(0)
