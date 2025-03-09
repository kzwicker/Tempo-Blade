n = 1

while(n <= 80):
    print(n)
    n += 1
print(f"\033[{n}F\033[J", end="\r")