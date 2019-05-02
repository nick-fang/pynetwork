
def outer(func):
    """time_it装饰器"""
    def inner(*args, **kwargs):
        import time
        start=time.perf_counter()
        result=func(*args, **kwargs)
        end=time.perf_counter()
        print(f'function <{func.__name__}> consumed {end-start:.3f} secs.')
        return result
    return inner

@outer
def add(a, b):
    """一个耗时1秒的函数"""
    import time
    result=a+b
    time.sleep(1)
    return result

add(2, 3)



def main():
    return "-".join(str(i) for i in range(20))

import timeit
timer=timeit.Timer('"-".join(str(i) for i in range(20))')
timer.timeit()
timer.timeit(10000)
timer2=timeit.Timer(main)
timer2.timeit()
timer2.timeit(10000)

timer.autorange()
timer.repeat(number=10000)
min(timer.repeat(10, 10000))




import timeit
timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
timeit.timeit('"-".join([str(n) for n in range(100)])', number=10000)
timeit.timeit('"-".join(map(str, range(100)))', number=10000)

timeit.repeat('"-".join(str(n) for n in range(100))', number=10000)
min(timeit.repeat('"-".join(str(n) for n in range(100))', number=10000))
min(timeit.repeat('"-".join([str(n) for n in range(100)])', number=10000))
min(timeit.repeat('"-".join(map(str, range(100)))', number=10000))




import timeit

def mklist_1():
    """使用for循环添加元素，构建列表"""
    result=[]
    for value in range(1000):
        result.append(str(value))
    return result

def mklist_2():
    """使用列表推导式构建列表"""
    return [str(value) for value in range(1000)]

def mklist_3():
    """使用map()函数构建列表"""
    return list(map(str, range(1000)))

for func in mklist_1, mklist_2, mklist_3:
    print(func.__name__, 'consumed:', timeit.repeat(func, repeat=3, number=10000))






from string import capwords
import unittest

def just_do_it(text):
    sub_texts=text.split('\"') #把引号作为分隔符拆分成若干子串，后者的首字符不会再被引号保护，从而能够被capwords函数正常转换
    cap_texts=[capwords(sub, ' ') for sub in sub_texts]
    return '\"'.join(cap_texts) #将转换后的字串拼接回包含引号的字符串

class TestCap(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_one_word(self):
        text='duck'
        result=just_do_it(text)
        self.assertEqual(result, 'Duck')
    def test_multiple_words(self):
        text='a veritable flock of ducks'
        result=just_do_it(text)
        self.assertEqual(result, 'A Veritable Flock Of Ducks')
    def test_words_with_apostrophes(self):
        text="I'm fresh out of ideas"
        result=just_do_it(text)
        self.assertEqual(result, "I'm Fresh Out Of Ideas")
    def test_words_with_quotes(self):
        text="\"You're despicable,\" said Daffy Duck"
        result=just_do_it(text)
        self.assertEqual(result, "\"You're Despicable,\" Said Daffy Duck")

if __name__=="__main__":
    unittest.main()





"""各种测试方法简介"""
import unittest

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        string='hello world'
        self.assertEqual(string.split(), ['hello', 'world'])
        with self.assertRaises(TypeError): #断言with块中的语句会触发特定异常
            string.split(2)

if __name__=="__main__":
    unittest.main()



"""使用expectedFailure装饰器"""
import unittest
class ExpectedFailureTestCase(unittest.TestCase):
    @unittest.expectedFailure
    def test_fail(self):
        self.assertEqual(1, 0, 'broken') #断言1==0失败，本应无法通过测试，但是由【预期失败】装饰器修饰后，情况就反转过来，视作测试成功
if __name__=="__main__":
    unittest.main()


"""使用测试夹具（setUp/tearDown）和测试套件（unittest.TestSuite）"""
import unittest
from file_to_test import Widget

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget=Widget('the widget')

    def test_default_widget_size(self):
        self.assertEqual(self.widget.size(), (50, 50), 'incorrect default size')

    def test_widget_resize(self):
        self.widget.resize(100, 150)
        self.assertEqual(self.widget.size(), (100, 150), 'wrong size after resize')

    def tearDown(self):
        self.widget.dispose()

if __name__=="__main__":
    suite=unittest.TestSuite() #创建一个自定义的测试套件
    #将任意测试用例的任意测试，添加进该测试套件中
    suite.addTest(WidgetTestCase('test_default_widget_size'))
    suite.addTest(WidgetTestCase('test_widget_resize'))
    runner=unittest.TextTestRunner()
    runner.run(suite) #执行该测试套件


"""使用skipxx装饰器"""
import unittest

class MyTestCase(unittest.TestCase):
    @unittest.skip('demonstrating skipping')
    def test_nothing(self):
        """无条件略过的测试"""
        pass

    @unittest.skipIf(mylib.__version__ < (1, 3), 'not supported in this library version')
    def test_format(self):
        """高级版本的新功能的测试"""
        pass

    @unittest.skipUnless(sys.platform.startswith('win'), 'requires Windowns')
    def test_windows_support(self):
        """Windows系统的相关测试"""
        pass

@unittest.skip('showing class skipping')
class MySkippedTestCase(unittest.TestCase):
    """被略过的测试用例"""
    def test_not_run(self):
        pass



"""在for迭代中使用子测试上下文管理器"""
import unittest
class NumberTest(unittest.TestCase):
    def test_even(self): #一个测试方法
        for i in range(0, 6):
            self.assertEqual(i%2, 0) #将断言语句置于for循环内，相当于该测试方法中有6条断言语句；只要有1条失败，那么该测试方法就会中断并跳出

if __name__=="__main__":
    unittest.main()

import unittest
class NumberTest(unittest.TestCase):
    def test_even(self):
        for i in range(0, 6):
            with self.subTest(i=i): #参数i=i会作为迭代间的区分标记，出现在测试结果中
                self.assertEqual(i%2, 0) #对循环中的每一个i，断言i是偶数

if __name__=="__main__":
    unittest.main()




import doctest
from string import capwords
def just_do_it(text):
    """
    >>> just_do_it('duck')
    'Duck'
    >>> just_do_it('a veritable flock of ducks')
    'A Veritable Flock Of Ducks'
    >>> just_do_it("I'm fresh out of ideas")
    "I'm Fresh Out Of Ideas"
    """
    return capwords(text)

if __name__=="__main__":
    doctest.testmod()

