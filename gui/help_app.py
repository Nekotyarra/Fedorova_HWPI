import tkinter as tk
from tkinter import ttk, messagebox
import sys

# from gui.menu import MenuApp


class HelpApp(tk.Toplevel):
    """Справка приложения."""
    def __init__(self):
        super().__init__()
        self.title('Справка')
        self.geometry('400x600')
        self.resizable(True, True)

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
        ttk.Button(
            btn_frame,
            text='Назад',
            command=self.go_away,
            width=20
        ).pack(side='top', pady=5)

    def go_away(self):
        """Завершает работу в текущем окне, возвращает в меню"""
        if messagebox.askyesno('Подтверждение', 'Вы действительно хотите выйти?'):
            self.quit()
            MenuApp()
