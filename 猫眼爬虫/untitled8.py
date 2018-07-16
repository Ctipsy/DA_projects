
def fib(max):
    a, b = 1, 1
    while a < max:
        yield a
        a, b = b, a+b
 
for n in fib(15):
    print(n)
 
m = fib(13)
print(m)
print("测试")
print(next(m))
print(next(m))
print(next(m))
print(next(m))
print(next(m))
