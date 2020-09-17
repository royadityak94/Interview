def func(x, y):
    x = y
    y = y+x
    return x
def foobar():
    x, y = 0, 1
    return func(x, y)

def main():
    f = foobar()
    for i in range(10):
        if i%2 == 0:
            print(f, end="")

main()
