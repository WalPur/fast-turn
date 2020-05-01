n = int(input())
m = int(input())
d = m // n
e = m % n
print(int(n // m + e // (e - 0.1)))