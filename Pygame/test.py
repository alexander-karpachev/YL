a = 2
b = 3
s = 1
e = 20

all = [i for i in range(s, e+1)]
l1 = [i for i in all if i % a == 0 and i % b > 0]
l2 = [i for i in all if i % b == 0 and i % a > 0]
l3 = [i for i in all if i % b == 0 and i % a == 0]
l4 = [i for i in all if i not in l1 + l2 + l3]

print(l1)
print(l2)
print(l3)
print(l4)
