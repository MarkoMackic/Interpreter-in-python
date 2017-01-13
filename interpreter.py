from __future__ import division
#from collection import deque
import operator


#Token types
#
#EOF (end of file) token is used to indicate that
#there is no more input left for lexical analysis

INTEGER,PLUS,EOF,MINUS,MULTYPLY,DIVIDE = 'INTEGER','PLUS','EOF','MINUS','MULTYPLY','DIVIDE'

ops = {
        '+':operator.add,
        '-':operator.sub,
        '*':operator.mul,
        '/':lambda x,y: x/y
      }

class Token(object):
    def __init__(self,type,value):
        #token type : INTEGER PLUS OR EOf
        self.type = type
        #token value is a single digit number, or '+', or None
        self.value = value;

    def __str__(self):
        """ String representation of the class instance.

        Examples:
            Token(INTEGER,3)
            Token(PLUS,'+')
            **when we end reading of the input**
            Token(EOF,None)

        """

        return 'Token({type},{value})'.format(
            type = self.type,
            value = repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self,inp):
        #client string input, e.g. "3+5"
        self.inp = inp
        self.position = 0
        self.current_token = None

    def error(self,recursion=False):
        error_message = "Error parsing input"
        if recursion:
            error_message += " maximum recursion depth reached"

        raise Exception(error_message)

    def integer(self):
        result = '';
        while self.position < len(self.inp)  and self.inp[self.position].isdigit():
            result += self.inp[self.position]
            self.position += 1
            
        return int(result);
    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        
        This method is responsible for breaking a sentence
         apart into tokens.One token at a time.

        """
        inp = self.inp;

        #if self.pos index past the end of the self.inp
        #if so then return EOF token because there is no
        #input left to convert into tokens
  
        if self.position > len(inp) - 1:
            return Token(EOF,None);

        current_char = inp[self.position]

        if current_char.isdigit():
            token = Token(INTEGER,self.integer())
            return token
        elif current_char == '+':
            token = Token(PLUS,"+")
            self.position += 1
            return token
        elif current_char == '-':
            token = Token(MINUS,"-")
            self.position += 1
            return token
        elif current_char == '*':
            token = Token(MULTYPLY,"*")
            self.position += 1
            return token
        elif current_char == '/':
            token = Token(DIVIDE,"/")
            self.position += 1
            return token



        self.error()

    def consume_whitespace(self):
        #because we add one, and we don't 
        while self.position < len(self.inp)  and self.inp[self.position] == ' ' :
            self.position += 1
    


    def assign(self,token,token_type):
        if token.type == token_type:
            return token.value
        else:
            self.error()

    def eat(self, token_type):
        #compare the current token type with the passed list of
        #token types and if it is inside than 'eat' the current token
        #and assign the next token to the self.current_token
        #otherwise return false;
        

        if self.current_token.type in token_type:
            self.consume_whitespace()
            self.current_token = self.get_next_token();
            return True
        else:
            return False

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""

        #add support for SPACES INTEGER SPACES SIGN SPACES INTEGER SPACES...
        self.consume_whitespace()

        #set current token to the first token taken from input
        self.current_token = self.get_next_token()
        tokens = []
        while self.current_token.type != EOF:
            token = self.current_token;
            tokens.append(token)
            self.eat(token.type)
        
        #print tokens

        counter = 0
        max_recursion = 200
        result = 0
        while counter < max_recursion:
            if len(tokens) == 1 and tokens[0].type == INTEGER:
                result = tokens[0]
                break 
            remove_indexes = None
            temp_token = None
            for i,token in enumerate(tokens):
                if token.type in [PLUS,MINUS]:
                    if i != 0 and i != len(tokens)-1:
                        #print i
                        #print token.value
                        if tokens[i+1].type == INTEGER and tokens[i-1].type == INTEGER:
                            temp_token = Token(INTEGER,
                                                ops[token.value](
                                                    tokens[i-1].value,
                                                    tokens[i+1].value
                                                    )
                                                )
                                          
                            #print tokens
                            remove_indexes=[i+1,i,i-1]
                            break;
                        else:
                            self.error()
                    else:
                        self.error()
            if remove_indexes:
                for i in remove_indexes:
                    #print i
                    del tokens[i]
            if temp_token:
                tokens.insert(0, temp_token)

            #recursion counter
            counter +=1
        
        if counter == max_recursion:
            self.error(recursion=True)
        else:
            return result.value

        

#our program main entry point
def main():
    while True:
        try:
          
            inp = raw_input('calc > ')
        except EOFError:     
            """exception EOFError
      
            Raised when one of the built-in functions
            (input() or raw_input()) hits an end-of-file condition (EOF)
            without reading any data. 
            (N.B.: the file.read() and file.readline() methods return an empty string 
            when they hit EOF.)

            """
            break;
        
        except KeyboardInterrupt:
            """User exited program  """

            print("\nBye bye")
            break;

        if not inp:
            continue

        #after we ashured we have some input we can init our
        #interpreter
        
        interpreter = Interpreter(inp)
        
        # Chekc for parsing errors 
        try:
            result = interpreter.expr()
        #If we end up here, we're cool :) 
            print(result)
        except Exception as e:
            #We'll print the exception
            print(str(e))
        

"""
For python3 change raw_input to input .. 
"""

if __name__ == '__main__':
    main()
