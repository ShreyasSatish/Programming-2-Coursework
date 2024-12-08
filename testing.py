import random

rgbs = []
rows = 5
cols = 5
for i in range(rows):
    row = []
    for j in range(cols):
        rgb = ["R", "G", "B"]
        row.append(rgb)
    rgbs.append(row)
print(rgbs)