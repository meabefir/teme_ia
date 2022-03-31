def f(a, *x):
    print(a)
    for el in x:
        print(el)

f(1, 2, 3)