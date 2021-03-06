import unittest
from interpreter import *
import time
from math import *

sample_number = 1000

class TestInterpreter(unittest.TestCase):


    def test_simple_expr(self):

        interpreter = Interpreter("5*5")
        result = interpreter.expr()
        self.assertEqual(float(result),25.0)

    def test_space_skipping(self):
 
        interpreter = Interpreter("5   *  7     ")
        result = interpreter.expr()
        self.assertEqual(float(result),35.0)

    def test_order_of_operations(self):

        interpreter = Interpreter("5*7/5*5+2-2/2+5")
        result = interpreter.expr()
        self.assertEqual(float(result),41.0)

        interpreter = Interpreter("5-5+5")
        result = interpreter.expr()
        self.assertEqual(float(result),5.0)

    def test_braces_reduction(self):

        interpreter = Interpreter("(((((((((((((((5-5+5)))))))))))))))")
        result = interpreter.expr()
        self.assertEqual(float(result),5.0)

    def test_brace_calculation(self):

        interpreter = Interpreter("6*3+(5+4)/3*4")
        result = interpreter.expr()
        self.assertEqual(float(result),30.0)

    def test_nested_brace_calculation(self):

        interpreter = Interpreter("5*(((4+3*(3-4)/(3-4))*2))")
        result = interpreter.expr()
        self.assertEqual(float(result),70.0)

    def test_unary_operators(self):

        interpreter = Interpreter("--2++3-----2+1")
        result = interpreter.expr()
        self.assertEqual(float(result),4.0)

    def test_expected_parse_faulire(self):

        interpreter = Interpreter("(((((((((5-5+5)))))))))))))))")
        with self.assertRaises(Exception) as cm:
            print(interpreter.expr())
        self.assertEqual(str(cm.exception), "Error parsing input")

        interpreter = Interpreter("+123 + * 4")
        with self.assertRaises(Exception) as cm:
            print(interpreter.expr())
        self.assertEqual(str(cm.exception), "Error parsing input")
       
    def test_speed_expression(self):
   

        start = time.time()
        for _ in range(sample_number):
             interpreter = Interpreter("(18/2)*(((9 * 9 - 1)/ 2)-(5 * 20 - (7 * 9 - 2)))")
             result = interpreter.expr()
        self.assertEqual(result,9.0)
        print('\nTiming for {num_runs} runs of interpretation is {ttime}ms\n'.format(
            num_runs = 1000,
            ttime = (time.time() - start)*1000))   
       
    def test_speed_math_functions(self):
   

        start = time.time()
        for _ in range(sample_number):
             interpreter = Interpreter("sin(2) * sin(2) -- sin   5    +  10 * 11")
             result = interpreter.expr()
        self.assertEqual(round(result,5),round(109.867897536,5))
        print('\nTiming for {num_runs} runs of interpretation is {ttime}ms\n'.format(
            num_runs = 1000,
            ttime = (time.time() - start)*1000))   
if __name__ == "__main__":
    unittest.main()

