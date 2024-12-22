import main, secret
import unittest, random

class TestMain(unittest.TestCase):
    def test1(self):
        r = random.random()
        float(eval("main"+f"()"*random.randint(10, 99))==r)==r**3 or 1/0

if __name__ == "__main__":
    result = unittest.main(exit = False)

    if result.result.wasSuccessful():
        print(secret.flag)