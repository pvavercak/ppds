
class Fibonacci():
    def __init__(self, N):
        self.a = 0
        self.b = 1
        self.cnt = 1
        self.N = N

    def __iter__(self):
        return self

    def __next__(self):
        if self.cnt > self.N:
            raise StopIteration

        if self.cnt > 1:
            self.a, self.b = self.b, self.a + self.b
        self.cnt += 1
        return self.b


def fib(N):
    i = 1
    a, b = 0, 1
    while True:
        if i > N:
            break
        yield b
        a, b = b, a+b
        i += 1


for i in Fibonacci(5):
    print(i)


print()

for i in fib(5):
    print(i)
