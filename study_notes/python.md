* 在计算机内存中，统一使用Unicode编码，当需要保存到硬盘或者需要传输的时候，就转换为UTF-8编码
* 列表生成器: [f(i) for i in iterable if ...]
* 列表生成方法构造生成器(generator): (f(i) for i in iterable if ...)
* function to generator: return --> yield
    - 最难理解的就是generator和函数的执行流程不一样。函数是顺序执行，遇到return语句或者最后一行函数语句就返回。而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。
    - 但是用for循环调用generator时，发现拿不到generator的return语句的返回值。如果想要拿到返回值，必须捕获StopIteration错误，返回值包含在StopIteration的value中
* 生成器都是Iterator对象，但list、dict、str虽然是Iterable，却不是Iterator?
    - 把list、dict、str等Iterable变成Iterator可以使用iter()函数
    - 因为Python的Iterator对象表示的是一个数据流，Iterator对象可以被next()函数调用并不断返回下一个数据，直到没有数据时抛出StopIteration错误。可以把这个数据流看做是一个有序序列，但我们却不能提前知道序列的长度，只能不断通过next()函数实现按需计算下一个数据，所以Iterator的计算是惰性的，只有在需要返回下一个数据时它才会计算。
    - Iterator甚至可以表示一个无限大的数据流，例如全体自然数。而使用list是永远不可能存储全体自然数的。
* 高阶函数：既然变量可以指向函数，函数的参数能接收变量，那么一个函数就可以接收另一个函数作为参数
    * map/reduce:
        - map(func, iterable): 将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回
        - reduce(func, iterable): reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
    * filter(func, iterable): filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素。
```python
# 求素数
def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n

def _not_divisible(n):
    return lambda x: x % n > 0

def primes():
    yield 2
    it = _odd_iter() # 初始序列
    while True:
        n = next(it) # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it) # 构造新序列

# 打印1000以内的素数:
for n in primes():
    if n < 1000:
        print(n)
    else:
        break

```

* 闭包: 包含有环境变量取值的函数对象, 环境变量被保存在函数对象的`__closure__`属性中
*返回闭包时牢记一点：返回函数不要引用任何循环变量，或者后续会发生变化的变量。*
```python
def line_conf():
    b = 15
    def line(x):
        return 2*x + b
    return line

b = 5
my_line = line_conf()
print(my_line.__closure__)
print(my_line(5))    # 25
```
* lambda x: f(x) --> lambda表示匿名函数，只能有一个表达式，不用写return    

* functools.partial: 定义偏函数, 作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单


