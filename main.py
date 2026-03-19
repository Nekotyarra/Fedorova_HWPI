from file_parser import file_open
from gui import App
from gui.menu import MenuApp
filename = "data.txt"
data = file_open(filename)

print(data)
for i in data:
    if i.value > 100:
        print(i.resource, i.date, i.value)

app = MenuApp()
app.mainloop()