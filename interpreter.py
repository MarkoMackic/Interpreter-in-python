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
        '*':lambda x,y: x*y,
        '/':lambda x,y: x/y
      }

token_indexer = 0

class Token(object):
    def __init__(self,type,value):
        global token_indexer
        #token type : INTEGER PLUS OR EOf
        self.type = type
        #token value is a single digit number, or '+', or None
        self.value = value;

        self.index = token_indexer

        token_indexer += 1
    #this is neat thing I didn't know about..
    def __eq__(self, other):
        return self.type == other.type

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
        self.current_char = self.inp[self.position]

    def error(self,recursion=False):
        error_message = "Error parsing input"
        if recursion:
            error_message += " maximum recursion depth reached"

        raise Exception(error_message)


    def advance(self):
        """ Advance the `position` pointer and set current_char variable"""
        self.position += 1
        if self.position > len(self.inp) - 1:
            self.current_char = None
        else:
            self.current_char = self.inp[self.position]

    def integer(self):
        result = '';
        while self.current_char is not None  and self.current_char.isdigit():
            result += self.current_char
            self.advance()
            
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
            self.advance()
            token = Token(PLUS,"+")
            return token
        elif current_char == '-':
            token = Token(MINUS,"-")
            self.advance()
            return token
        elif current_char == '*':
            token = Token(MULTYPLY,"*")
            self.advance()
            return token
        elif current_char == '/':
            token = Token(DIVIDE,"/")
            self.advance()
            return token



        self.error()

    def consume_whitespace(self):
        #because we add one, and we don't 
        while self.current_char == ' ' :
            self.advance()

        #print("After consuming whitespaces I have character {character}".format(
        #        character = self.current_char
        #    ))
    


    def term(self):
        """RETURN INTEGER TOKEN  VALUE """
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def eat(self, token_type):
        #compare the current token type with the passed list of
        #token types and if it is inside than 'eat' the current token
        #and assign the next token to the self.current_token
        #otherwise return false;
        
        if self.current_token.type in token_type:
            print("Eating {token}".format(
                token=self.current_token
               ))
            self.consume_whitespace()
            self.current_token = self.get_next_token();
        else:
            self.error()

    def calculate(self,tokenList,operationToken):
            index = tokenList.index(operationToken)
            if index != 0 and index != len(tokenList)-1:
                a = tokenList[index-1]
                b = tokenList[index+1]
                if a.type == INTEGER and b.type==INTEGER:
                    result = ops[tokenList[index].value](
                                float(a.value),
                                float(b.value)
                            )  
                    tokenList.insert(index-1,Token(INTEGER,result))
                    for i in range(index+2,index-1,-1):
                        del tokenList[i]          
                    print tokenList
                else:
                    self.error()
            else:
                self.error()

    def expr(self):
        """Yay. This can now be calles arithmetic expression parser/interpreter """

        #add support for SPACES INTEGER SPACES SIGN SPACES INTEGER SPACES...
        self.consume_whitespace()


        self.current_token = self.get_next_token()
        tokens = []
        #set current token to the first token taken from input
        while self.current_token:
            token = self.current_token
            self.eat(self.current_token.type)
            if token.type == EOF:
                break
            tokens.append(token)
    
        """
            Analyze */ first, and then we'll do +-

        """
        temp_result = None
        result = None
        has_multiply = False
        #Order of operations
        while (Token(MULTYPLY,"*") in tokens or
               Token(DIVIDE,"*") in tokens):
           for token in tokens:
                if(token == Token(MULTYPLY,"*") or
                   token == Token(DIVIDE,"/")):
                   self.calculate(tokens,token)

        while Token(PLUS,'+') in tokens:
           self.calculate(tokens,Token(PLUS,'+'))
        while Token(MINUS,'-') in tokens:
           self.calculate(tokens,Token(MINUS,'-'))
        
        print tokens





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
        #try:
        result = interpreter.expr()
        #If we end up here, we're cool :) 
        #print(result)
        #except Exception as e:
            #We'll print the exception
        #    print(str(e))
        

"""
For python3 change raw_input to input .. 
"""

if __name__ == '__main__':
    main()
