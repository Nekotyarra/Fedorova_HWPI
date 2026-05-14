"""Главное окно приложения."""

import tkinter as tk
import datetime
from tkinter import ttk, messagebox, filedialog
from classes import MeterReading, MeterModel, MeterValidationError
from file_parser import file_open
from data_manager import add_record, delete_record
from gui.adddata_app import AddDialog

import logging
from command_processor import CommandProcessor

logger = logging.getLogger(__name__)


class ErrorLogger:
    """Виджет для отображения лога ошибок."""

    def __init__(self):
        self.text_widget = None

    def initialize(self, parent: tk.Frame) -> None:
        """Создаёт виджет лога."""
        frame = tk.LabelFrame(parent, text="Лог ошибок")
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.text_widget = tk.Text(frame, height=6, wrap=tk.WORD)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=scrollbar.set)

    def log_error(self, error_msg: str, context: dict = None) -> None:
        """Добавляет сообщение об ошибке в лог."""
        import datetime
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        msg = f'[{timestamp}] {error_msg}'
        if context:
            msg += f' | Данные: {context}'
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.see(tk.END)


class MeterApp:
    def __init__(self, filename: str, parent=None):
        """
        Args:
            filename: путь к файлу с данными
            parent: родительское окно (MenuApp)
        """
        self.parent = parent

        # Скрываем родительское окно (меню)
        if parent:
            parent.withdraw()

        # Создаём новое окно
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title("Учёт показаний счётчиков")
        self.root.geometry("800x600")

        # При закрытии окна возвращаемся в меню
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.model = MeterModel(filename)
        self.processor = CommandProcessor(self.model)

        self.error_logger = ErrorLogger()
        self._create_table()
        self._create_buttons()

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.error_logger.initialize(bottom_frame)

        self._refresh_table()

    def on_closing(self):
        """Обработка закрытия окна - возврат в меню."""
        if self.parent:
            self.parent.deiconify()  # Показываем меню
        self.root.destroy()

    def _create_table(self) -> None:
        frame = tk.Frame(self.root)
        frame.pack(pady=8, padx=15, fill=tk.BOTH, expand=True)

        columns = ('resource', 'date', 'value', 'quality')
        self.table = ttk.Treeview(frame, columns=columns, show='headings')

        self.table.heading('resource', text='Ресурс')
        self.table.heading('date', text='Дата')
        self.table.heading('value', text='Значение')
        self.table.heading('quality', text='Качество')

        self.table.column('resource', width=200, anchor='center')
        self.table.column('date', width=120, anchor='center')
        self.table.column('value', width=100, anchor='center')
        self.table.column('quality', width=100, anchor='center')

        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _create_buttons(self) -> None:
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="[ Добавить показание ]",
                  command=self.add_record).pack(side=tk.LEFT, padx=5)  # убрали скобки

        tk.Button(frame, text="[ Удалить выбранное ]",
                  command=self._on_delete).pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="[ Выполнить команды ]",
                  command=self._on_run_commands).pack(side=tk.LEFT, padx=5)

    def refresh_table(self, data_to_show=None):
        """Обновляет отображение таблицы в соответствии с текущими данными.
        Args:
            data_to_show: Если указан, отображает этот список, иначе self.data.
        """
        for row in self.tree.get_children():
            self.tree.delete(row)

        display_data = data_to_show if data_to_show is not None else self.data

        for reading in display_data:
            self.tree.insert('', 'end', values=(reading.resource, reading.date, reading.value, reading.quality))

    def _refresh_table(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)

        for reading in self.model.get_all():
            self.table.insert('', tk.END, values=(
                reading.resource,
                reading.date,
                reading.value,
                reading.quality
            ))

    def add_record(self):
        """Открывает диалог добавления записи."""
        from gui.adddata_app import AddDialog
        dlg = AddDialog(self.root)
        if dlg.result:
            resource, date_obj, value, quality = dlg.result  # date_obj - это datetime.date
            try:
                # Преобразуем datetime.date в строку
                date_str = date_obj.strftime('%Y.%m.%d')
                self.model.add_reading(resource, date_str, value, quality)
                self._refresh_table()
            except MeterValidationError as e:
                messagebox.showerror("Ошибка валидации", str(e))

    def _on_delete(self) -> None:
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("", "Выберите запись!")
            return

        index = self.table.index(selected[0])
        try:
            self.model.delete_reading(index)
            self._refresh_table()
        except IndexError as e:
            messagebox.showerror("Ошибка", str(e))

    def _on_run_commands(self) -> None:
        filename = filedialog.askopenfilename(
            title="Выберите файл команд",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not filename:
            return

        self.processor.run_file(filename)
        self._refresh_table()
        messagebox.showinfo(
            "Готово",
            f"Команды выполнены.\nСм. лог для деталей."
        )


