from file_parser import file_open
from gui import MeterApp
from gui import MenuApp
from classes import MeterModel, MeterValidationError
import logging
import tkinter as tk
filename = "data.txt"
data = file_open(filename)

print(data)
for i in data:
    if i.value > 100:
        print(i.resource, i.date, i.value)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('readings.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    model = MeterModel("data.txt")
    app = MenuApp()
    app.mainloop()