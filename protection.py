def newqwe(mass):
    c=0
    for i in mass:
        if i%2==0:
            c+=1
    return c

print(newqwe([1, 2, 3, 4]))


def sum_func(a, b, c):
    try:
        a = int(a) if not isinstance(a, int) else a
        b = int(b) if not isinstance(b, int) else b
        c = int(c) if not isinstance(c, int) else c

        return a + b - 2*c
    except (ValueError, TypeError):
        print("Ошибка: аргументы должны быть int")
        return None
print(sum_func(20,23,15))