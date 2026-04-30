"""Диалоговые окна приложения."""

import tkinter as tk
import datetime
from tkinter import ttk, messagebox
from file_parser import parse_date

class AddDialog(tk.Toplevel):
    """Диалоговое окно для добавления новой записи."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title('Добавить показание')
        self.resizable(False, False)
        self.result = None

        # Поля ввода
        ttk.Label(self, text='Ресурс:').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.resource_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.resource_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text='Дата (гггг.мм.дд):').grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.date_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.date_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text='Значение:').grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.value_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.value_var, width=30).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text='Качество:').grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.quality_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.quality_var, width=30).grid(row=3, column=1, padx=5, pady=5)

        # Кнопки
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text='OK', command=self.ok_click).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Отмена', command=self.cancel_click).pack(side='left')

        # Центрируем окно относительно родителя
        self.transient(parent)
        self.grab_set()
        self.wait_window()

    def ok_click(self):
        """Обработчик нажатия OK: проверка ввода и сохранение результата."""
        resource = self.resource_var.get().strip()
        date_str = self.date_var.get().strip()
        value_str = self.value_var.get().strip()
        quality = self.quality_var.get().strip()

        if not resource or not date_str or not value_str:
            messagebox.showerror('Ошибка', 'Все поля должны быть заполнены')
            return

        try:
            date = parse_date(date_str)
        except ValueError as e:
            messagebox.showerror('Ошибка', str(e))
            return
        try:
            value = float(value_str)
        except ValueError:
            messagebox.showerror('Ошибка', 'Значение должно быть числом')
            return

        self.result = (resource, date, value, quality)
        self.destroy()

    def cancel_click(self):
        """Обработчик отмены."""
        self.result = None
        self.destroy()