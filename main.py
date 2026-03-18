from file_parser import file_open
from gui import App


filename = "data.txt"
data = file_open(filename)

print(data)
for i in data:
    if i.value > 100:
        print(i.resource, i.date, i.value)

app = App(filename)
app.mainloop()