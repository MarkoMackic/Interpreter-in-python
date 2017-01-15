import unittest
from interpreter import *

class TestInterpreter(unittest.TestCase):
    def test_expr(self):
        #test simple expression
        interpreter = Interpreter("5*5")
        result = interpreter.expr()
        self.assertEqual(float(result),25.0)
        #test space skipping
        interpreter = Interpreter("5   *  7     ")
        result = interpreter.expr()
        self.assertEqual(float(result),35.0)
        #testing order of operations on simple expression
        interpreter = Interpreter("5*7/5*5+2-2/2+5")
        result = interpreter.expr()
        self.assertEqual(float(result),41.0)
        #testing order of operations on simple expression
        interpreter = Interpreter("5-5+5")
        result = interpreter.expr()
        self.assertEqual(float(result),5.0)
        #testing braces reduction
        interpreter = Interpreter("(((((((((((((((5-5+5)))))))))))))))")
        result = interpreter.expr()
        self.assertEqual(float(result),5.0)
        #testing simple braces calculation
        interpreter = Interpreter("6*3+(5+4)/3*4")
        result = interpreter.expr()
        self.assertEqual(float(result),30.0)
        #testing nested braces calculation
        interpreter = Interpreter("5*(((4+3*(3-4)/(3-4))*2))")
        result = interpreter.expr()
        self.assertEqual(float(result),70.0)
        #Expected parse faulire
        interpreter = Interpreter("(((((((((5-5+5)))))))))))))))")
        with self.assertRaises(Exception) as cm:
            print(interpreter.expr())

        excp = cm.exception
        self.assertEqual(str(excp), "Error parsing input")
        #Expected parse faulire
        interpreter = Interpreter("+123 + 4")
        with self.assertRaises(Exception) as cm:
            print(interpreter.expr())

        excp = cm.exception
        self.assertEqual(str(excp), "Error parsing input")
       
        

if __name__ == "__main__":
    unittest.main()