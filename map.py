map = []
temp = []
for j in range(40):
    temp.append('x')
map.append(temp)
for i in range(21):
    temp = ['x']
    for j in range(38):
        temp.append(' ')
    temp.append('x')
    map.append(temp)
temp = []
for j in range(40):
    temp.append('x')
map.append(temp)

print("[", end="")
for i in map:
    print(i, ",\n")

print("]", end="")