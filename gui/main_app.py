"""Главное окно приложения."""

import tkinter as tk
import datetime
from tkinter import ttk, messagebox
from classes import MeterReading
from file_parser import file_open
from data_manager import add_record, delete_record
from gui.adddata_app import AddDialog


class App(tk.Toplevel):
    """Главное окно приложения."""

    def __init__(self, filename, menu):
        super().__init__()
        self.menu = menu

        self.title('Учёт показаний счётчиков')
        self.geometry('600x400')
        self.filename = filename
        self.data = file_open(filename)

        self.center_window()

        self.create_widgets()
        self.refresh_table()

        # При закрытии окна через крестик - возвращаемся в меню
        self.protocol("WM_DELETE_WINDOW", self.go_back)

    def center_window(self):
        """Размещает окно по центру экрана."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _format_date(self, date: datetime.date) -> str:
        """Преобразует date в строку для отображения в таблице."""
        return date.strftime('%d-%m-%Y')

    def create_widgets(self):
        """Создаёт элементы интерфейса."""
        # Создаём фрейм-контейнер для таблицы и скроллбара
        table_frame = ttk.Frame(self)
        table_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5)

        columns = ('resource', 'date', 'value')

        # Таблица занимает левую часть и расширяется
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        self.tree.pack(side='left', fill='both', expand=True)

        self.tree.heading('resource', text='Ресурс')
        self.tree.heading('date', text='Дата')
        self.tree.heading('value', text='Значение')
        self.tree.column('resource', width=200)
        self.tree.column('date', width=100)
        self.tree.column('value', width=100)

        # Скроллбар справа, заполняет по вертикали
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')

        self.tree.configure(yscrollcommand=scrollbar.set)

        # Далее идёт код для панели кнопок и поиска
        btn_frame = ttk.Frame(self)
        btn_frame.pack(side='bottom', fill='x', padx=5, pady=5)

        ttk.Button(btn_frame, text='Добавить', command=self.add_record).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Удалить', command=self.delete_record).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Обновить из файла', command=self.reload_from_file).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Назад', command=self.go_back).pack(side='left', padx=5)

        ttk.Label(btn_frame, text='Поиск:').pack(side='right', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)
        ttk.Entry(btn_frame, textvariable=self.search_var, width=15).pack(side='right', padx=5)

    def refresh_table(self, data_to_show=None):
        """Обновляет отображение таблицы в соответствии с текущими данными.
        Args:
            data_to_show: Если указан, отображает этот список, иначе self.data.
        """
        for row in self.tree.get_children():
            self.tree.delete(row)

        display_data = data_to_show if data_to_show is not None else self.data

        for reading in display_data:
            self.tree.insert('', 'end', values=(reading.resource, reading.date, reading.value))

    def go_back(self):
        """Возврат в главное меню."""
        self.destroy()  # Закрываем рабочее окно
        if self.menu:
            self.menu.app = None
            self.menu.deiconify()  # Показываем главное меню

    def add_record(self):
        """Открывает диалог добавления и обновляет данные."""
        dlg = AddDialog(self)
        if dlg.result:
            resource, date, value = dlg.result
            self.data = add_record(self.data, resource, date, value)
            self.refresh_table()

    def delete_record(self):
        """Удаляет выделенную в таблице запись."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Предупреждение', 'Выберите запись для удаления')
            return

        # Подтверждение удаления
        if not messagebox.askyesno('Подтверждение', 'Удалить выбранную запись?'):
            return

        # Получаем индекс выбранной строки
        item = selected[0]
        index = self.tree.index(item)
        self.data = delete_record(self.data, index)
        self.refresh_table()

    def reload_from_file(self):
        """Перезагружает данные из исходного файла."""
        if messagebox.askyesno('Подтверждение',
                               'Перезагрузить данные из файла? Несохранённые изменения будут потеряны.'):
            self.data = file_open(self.filename)
            self.refresh_table()

    def on_search(self, *args):
        search_text = self.search_var.get().strip().lower()
        if not search_text:
            self.refresh_table(self.data)
            return

        filtered = []
        for reading in self.data:
            # Поиск по ресурсу (без изменений)
            if search_text in reading.resource.lower():
                filtered.append(reading)
                continue

            # Поиск по дате в формате ГГГГ-ММ-ДД
            date_iso = reading.date.strftime('%Y-%m-%d')
            if search_text in date_iso:
                filtered.append(reading)
                continue

            date_iso2 = reading.date.strftime('%Y.%m.%d')
            if search_text in date_iso2:
                filtered.append(reading)
                continue

        self.refresh_table(filtered)