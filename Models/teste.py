import random

a = [random.randint(0, 210), random.randint(0, 210), random.randint(0, 210), random.randint(0, 210)]

x = [430 - a[0], 430 - a[1], 430 - a[2], 430 - a[3]]
y = [0 - a[0], 0 - a[1], 0 - a[2], 0 - a[3]]

tube = [tube1, tube2, tube3, tube4]

for x in range(0, 4):
    if tube[x] == 860:
        tube[x] = 0
