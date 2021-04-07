
import random
for i in range(200):
    a = random.randint(0, 9)
    b = random.randint(0, 9)
    c = random.randint(0, 9)
    s1 = random.randint(0, 1)
    s2 = random.randint(0, 1)
    if a <= b:
        s1 = 0
        if a + b <= c:
            s2 = 0
    else:
        if s1 == 0:
            if a + b < c:
                s2 = 0
        else:
            if a - b < c:
                s2 = 0
    # print(s1, s2)
    if s1 == 0:
        d1 = "+"
        ab = a + b
    else:
        d1 = "-"
        ab = a - b
    # print(ab,a,b)
    if s2 == 0:
        d2 = "+"
        abc = ab + c
    else:
        d2 = "-"
        abc = ab - c
    # print(a,b,c)

    # print("(" + str(i) + ")、" + str(a) + d1 + str(b) + d2 + str(c) + " = " + str(abc))
    print(str(a) + d1 + str(b) + d2 + str(c) + "=")
