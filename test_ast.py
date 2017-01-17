import unittest
from interpreter_ast import *
import unittest
import time

class TestInterpreter(unittest.TestCase):

    def makeInterpreter(self, text):
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        return interpreter

    def test_simple_expr(self):
        interpreter = self.makeInterpreter("5*5")
        result = interpreter.interpret()
        self.assertEqual(float(result),25.0)

    def test_space_skipping(self):
 
        interpreter = self.makeInterpreter("5   *  7     ")
        result = interpreter.interpret()
        self.assertEqual(float(result),35.0)

    def test_order_of_operations(self):

        interpreter = self.makeInterpreter("5*7/5*5+2-2/2+5")
        result = interpreter.interpret()
        self.assertEqual(float(result),41.0)

        interpreter = self.makeInterpreter("5-5+5")
        result = interpreter.interpret()
        self.assertEqual(float(result),5.0)

    def test_braces_reduction(self):

        interpreter = self.makeInterpreter("(((((((((((((((5-5+5)))))))))))))))")
        result = interpreter.interpret()
        self.assertEqual(float(result),5.0)

    def test_brace_calculation(self):

        interpreter = self.makeInterpreter("6*3+(5+4)/3*4")
        result = interpreter.interpret()
        self.assertEqual(float(result),30.0)

    def test_nested_brace_calculation(self):

        interpreter = self.makeInterpreter("5*(((4+3*(3-4)/(3-4))*2))")
        result = interpreter.interpret()
        self.assertEqual(float(result),70.0)

    '''
    def test_unary_operators(self):
        doesn't support this yet
        interpreter = Interpreter("--2++3-----2+1")
        result = interpreter.interpret()
        self.assertEqual(float(result),4.0)
     
    
    
    '''
    def test_expected_parse_faulire(self):

        interpreter = self.makeInterpreter("(((((((((5-5+5)))))))))))))))")
        with self.assertRaises(Exception) as cm:
            print(interpreter.interpret())
        self.assertEqual(str(cm.exception), 'Invalid syntax')

        interpreter = self.makeInterpreter("+123 + * 4")
        with self.assertRaises(Exception) as cm:
            print(interpreter.interpret())
        
    def test_speed(self):
        
        sample_number = 1000

        start = time.time()
        for _ in range(sample_number):
            interpreter = self.makeInterpreter("(18/2)*(((9 * 9 - 1)/ 2)-(5 * 20 - (7 * 9 - 2)))")
            result = interpreter.interpret()

        self.assertEqual(result,9.0)
        print('\nTiming for {num_runs} runs of interpretation is {ttime}ms\n'.format(
             num_runs = 1000,
             ttime = (time.time() - start)*1000))   
       
        

if __name__ == "__main__":
    unittest.main()

