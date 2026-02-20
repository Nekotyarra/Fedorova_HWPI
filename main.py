from file_parser import file_open

data = file_open()

print(data)
for i in data:
    if i.value > 100:
        print(i.resource, i.date, i.value)
