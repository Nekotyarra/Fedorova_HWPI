import helper

data = []
with open('data.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            data.append(helper.parse_line_shlex(line))

print(data)
