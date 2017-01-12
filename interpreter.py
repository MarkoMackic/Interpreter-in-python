#Token types
#
#EOF (end of file) token is used to indicate that
#there is no more input left for lexical analysis

INTEGER,PLUS,EOF = 'INTEGER','PLUS','EOF'

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
    def __init__(self):
        #client string input, e.g. "3+5"
        self.inp = text
        self.position = 0
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        
        This method is responsible for breaking a sentence
         apart into tokens.One token at a time.

        """
        inp = self.inp;

        #if self.pos index past the end of the self.inp
        #if so then return EOF token because there is no
        #input left to convert into tokens
  
        if self.position > len(text) - 1:
            return Token(EOF,None);

        current_char = inp[self.position]

        if current_char.isdigit():
            token = Token(INTEGER,int(current_char))
            self.pos += 1
            return token
        elif current_char == '+':
            token = Token(PLUS,"+")
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        #compare the current token type with the passed 
        #token type and if they match than 'eat' the current token
        #and assign the next token to the self.current_token
        #otherwise raise exception;

        if self.current_token.type == token_type:
            self.current_token = self.get_next_token();
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        #set current token to the first token taken from input
        self.current_token = self.get_next_token()

        #we expect a single digit number
        left = self.current_token
        self.eat(INTEGER)
        #then the operation sign
        operation = self.current_token
        self.eat(PLUS)
        #and then again single digit number
        right = self.current_token
        self.eat(INTEGER)

         #After this we have our self.current_token equal to EOF 

         #at this point INTEGER PLUS INTEGER sequence of tokens
         #has been successfully found and the method can jus
         #return the result of adding two integers, thus
         #effectivly interpreting client inptu

         result = left.value + right.value
         print(result)

#our program main entry point
def main()
    while 1:
        try:
            #no inp ?
            inp = raw_input('calc > ')
        except EOFError:
            break;

        if not inp:
            continue

        #after we ashured we have some input we can init our
        #interpreter
        interpreter = Interpreter(inp)
        result = Interpreter.expr()
        print(result)