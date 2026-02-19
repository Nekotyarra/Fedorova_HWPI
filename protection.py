def newqwe(mass):
    c=0
    for i in mass:
        if i%2==0:
            c+=1
    return c

print(newqwe([1, 2, 3, 4]))