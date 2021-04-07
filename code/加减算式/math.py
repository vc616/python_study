import math
import os
import random

# print(math.pi)
a = b = c = 0
# print(math.floor(random.random()*10))
r = {}
# print(r["1"])
for i in range(100000):
    a = random.random() * 10
    q = math.floor(a)
    # print(a,q)
    s = str(q)
    if s in r:
        r[s] = r[s] + 1
    else:
        r[s] = 1
t = 0
for i, k in r.items():
    t = t + k
print(r)
print(t)
