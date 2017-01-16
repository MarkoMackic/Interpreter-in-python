
'''
Support float division for py2
'''

from __future__ import division
import sys

'''
    DEBUG_LEVEL

    0 -> NO_LOGGING
    1 -> IMPORTANT
    2 -> INFO 
'''

DEBUG_LEVEL = 1


'''
    Define tokens types that we can
    use in our parser
'''

NUMBER = 'NUMBER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTYPLY = 'MULTYPLY'
DIVIDE = 'DIVIDE'
OB = 'OB'
CB = 'CB'
EOF = 'EOF'

'''
    Function returns result
    for operations between numbers
    x, y

    @param x Number token value
    @param y Number token value
'''
ops = {
        '+':lambda x,y: x+y,
        '-':lambda x,y: x-y,
        '*':lambda x,y: x*y,
        '/':lambda x,y: x/y
      }



'''
    Logger function
    Checks if level is less or equal
    to current DEBUG_LEVEL, and prints
    output to console
    
    @param level Integer of level
    @param message A message to be print
'''
def lprint(message, level):
    if level <=  DEBUG_LEVEL:
        print(message)


class Token(object):
    '''
        Class constructor

        @param t_type Some of the above mentioned token types
        @param value Value of that token
    '''
    def __init__(self,t_type,value):
        '''
            Assing type and value to new object instance
        '''
        self.type = t_type
        self.value = value

    def __eq__(self, other):
        '''
            We'll compare tokens by their type
            Then if we need we can compare the values
        '''
        return self.type == other.type

    def __str__(self):
        '''
            String representation of the class
            This is called when we print token out

            @return string Token(type,value)
        '''

        return 'Token({type},{value})'.format(
            type = self.type,
            value = repr(self.value)
        )

    def __repr__(self):
        '''
            Class representation 

            @return String representation of class
        '''
        return self.__str__()


'''
    Map for single char tokens
'''
sct = {
    '(' : Token(OB,'('),
    ')' : Token(CB,')'),
    '+' : Token(PLUS,'+'),
    '-' : Token(MINUS,'-'),
    '/' : Token(DIVIDE,'/'),
    '*' : Token(MULTYPLY,'*')
}

class ParsingError(Exception):
    '''
        Error while parsing
    '''
    def __init__(self,message):
        super(ParsingError, self).__init__(message)


class Interpreter(object):
    '''
        Finds tokens in stream of
        input
    '''

    def __init__(self,inp):
        '''
            Constructor function
            
            @parm inp contains user input
        '''
        self.inp = inp
        self.position = 0
        self.current_token = None
        self.current_char = self.inp[self.position]
        
        lprint('Initializing interpreter with {u_inp}'.format(
            u_inp = inp
            ), 2)

    def error(self):
        '''
            Error handler for our interpreter
        '''
        error_message = 'Error parsing input'
        raise ParsingError(error_message)


    def advance(self):
        '''
            Advance position of cursor, and
            set current_char, if we eneded
            reading stream then set it to None
        '''

        self.position += 1

        if self.position > len(self.inp) - 1:
            self.current_char = None
        else:
            self.current_char = self.inp[self.position]

    def number(self):
        '''
            Parse number in format 
            x | x.y where x,y are 
            integers 

        '''
        result = '';
        
        while(
            self.current_char is not None and
            self.current_char.isdigit() or
            self.current_char == '.'
            ):

            result += self.current_char
            self.advance()
            
        return float(result);

    def get_next_token(self):
        '''
            This method extracts the
            next token from user input
            string. If token is invalid
            error() is called.

            @return Token

        '''

        # If we ended the stream return End of file token
        if self.position > len(self.inp) - 1:
            return Token(EOF,None);

        # Number token
        if self.current_char.isdigit():
            token = Token(NUMBER,self.number())
            return token

        #Single char token 
        elif self.current_char in sct:
            token = sct[self.current_char]
            self.advance()
            return token

        self.error()

    def consume_whitespace(self):
        '''
            Skip the whitespace characters
        '''
        while self.current_char == ' ' :
            self.advance()

    def eat(self, token_type):
        '''
            Eat function is used to confirm
            the integrity of current token
            and load the next token
        '''
        
        if self.current_token.type in token_type:

            self.consume_whitespace()
            self.current_token = self.get_next_token();
        else:
            self.error()

    def unaryOperators(self,tokenList):
        '''
            Filter token list to recognize
            unary operators. 
            
            Each char or (chars) in example 
            represents value of token:
            
            @params tokenList List of tokens where
            unary reducton should occur

            tokenList      = result

            ---+2+----(23) = (-2)+(23)
            ---*2+(32)     = error
            ---2*(23)      = (-2)*(23)

        '''

        #list for filtered tokens
        result = [] 


        #last token must be number
        if tokenList[len(tokenList)-1].type == NUMBER:
            #operators list
            operators = []
            #go through each token
            for index,token in enumerate(tokenList):
                if token.type in (PLUS,MINUS):
                    '''
                        If current token is + or -
                        append current token to
                        operators
                    '''
                    operators.append(token)
                else:
                    '''
                        If not, we check if our 
                        oprators list is not empty
                    '''
                    if operators:
                        #we can start with + sign
                        sign =  Token(PLUS,'+')
                        '''
                            If we have uneven number
                            of - tokens in list. We can
                            assume operation is -
                        '''
                        if operators.count(
                            Token(MINUS,'-')
                        ) % 2 == 1:
                            sign = Token(MINUS,'-')

                        '''
                            After combination of +|- tokens
                            we must have a number
                        '''
                        if token.type == NUMBER:
                            if not result:
                                '''
                                    Since we can't have -|+ before 
                                    expression to solve it by our 
                                    methods append that minus directly
                                    to the first number value itself
                                '''
                                token.value = float(sign.value +
                                                    str(token.value))
                                result.append(token)
                            else:
                                '''
                                    For all other values 
                                    append sign and number token
                                '''
                                result.append(sign)
                                result.append(token)
                        else:
                            self.error()

                        #clear operators list
                        operators = []
                    else:
                        '''
                            Since we have no + - operatiors
                            defined before non +|- token, we
                            just append that token to the 
                            result.
                            Input '4*5' is example where this
                            occurs for each token. 
                        '''
                        result.append(token)
        else:
            self.error()

        return result

    def doOperations(self,tokenList,operationToken):
            '''
                Find first instance of opration token
                in given list. Check indexes because
                tokens can't be at beggining and end 
                of basic expressions. Check nearby
                tokens for integers, so we don't have
                situation like // ++ or +( or anything
                like that. Do operations on numbers,
                insert at a place of the left number 
                in list, then delete tokens used including
                both integers and operation sign from right
                to left, so we don't have problems with
                indexes, and finish up.If anything is blown
                raise Exception. 
                We don't need to return anything since
                we're activly modifiying the current list
                tokenList.

                @params tokenList Token list where operation should
                be done
                @params operation Operation token

                Current tokenList is beeing modified, so this
                function has no return value
            '''
            index = tokenList.index(operationToken)
            if index != 0 and index != len(tokenList)-1:
                a = tokenList[index-1]
                b = tokenList[index+1]
                if a.type == NUMBER and b.type==NUMBER:
                    result = ops[tokenList[index].value](
                                a.value,
                                b.value
                            )  
                    tokenList.insert(index-1,Token(NUMBER,result))
                    for i in range(index+2,index-1,-1):
                        del tokenList[i]          
                    lprint('Token list after operation {tokenl}'.format(
                            tokenl = tokenList
                        ), 2)
                else:
                    self.error()
            else:
                self.error()


    def calculateExpression(self,tokens):
        '''
            Do operations on tokens list
            First do multiplication and division, 
            and do them in order.
            Then we can do addition and subtraction.
            Since we pass tokens list to doOperations, after
            all processes are finished we should have
            a single token list, so we can just return
            tokens[0], if we don't have a single token
            raise Exception.

            @params tokens Token list on which 
            operation should be done
        '''       
        #PARSE UNARY OPERATORS
        tokens = self.unaryOperators(tokens)
        
        while (Token(MULTYPLY,'*') in tokens or
               Token(DIVIDE,'/') in tokens):
            m_index = len(tokens)
            d_index = len(tokens)
            if Token(MULTYPLY,'*') in tokens:
                m_index = tokens.index(Token(MULTYPLY,'*'))
            if Token(DIVIDE,'/') in tokens:
                d_index = tokens.index(Token(DIVIDE,'/'))
            
            if m_index > d_index:
                self.doOperations(tokens,Token(DIVIDE,'/'))
            else:
                self.doOperations(tokens,Token(MULTYPLY,'*'))

        while (Token(PLUS,'+') in tokens or
               Token(MINUS,'-') in tokens):
            p_index = len(tokens)
            m_index = len(tokens)
            if Token(PLUS,'+') in tokens:
                p_index = tokens.index(Token(PLUS,'+'))
            if Token(MINUS,'-') in tokens:
                m_index = tokens.index(Token(MINUS,'-'))
            
            if p_index > m_index:
                self.doOperations(tokens,Token(MINUS,'-'))
            else:
                self.doOperations(tokens,Token(PLUS,'+'))
     

        if len(tokens) == 1:
            return tokens[0]
        else:
            self.error();

    def expr(self):
        

        self.consume_whitespace()

        self.current_token = self.get_next_token()

        tokens = []

        #parse all tokens from the input stream
        while self.current_token:
            token = self.current_token
            self.eat(self.current_token.type)
            if token.type == EOF:
                break
            tokens.append(token)
    
        
        '''
            Now we have digged a bit deeper.
            Our so called 'calculator' interpreter
            can accept braces. We have baseexpr 
            list, and it serves to hold level 0 
            tokens. Token level is defined by
            number of parent braces like this
            0 (1 (2 ( 3 (4 (5) 4) 3) 2) 1) 0 (1) (1(2)1) 0
            So at the end of our parsing we must have our
            current level set to 0. 
            We go through each token, if token is opening 
            brace we increase current level, and continue
            because we don't want it to be added to baseexpr
            list. If token is closing bracket, we check
            if there is a tree formed by bracketing. Tree
            is a dict containg level : expr for each level
            that has something in it. So if we have a formed
            tree, we calculate expression at the highest level
            because it has to be non malformed expression,
            then append the result to level before it. After 
            we get to level 1 we have the final result of brackets
            calulations.
            Let's take for example
            1+(2+3+(5*((3)+3)))
            
            Since 1 and + are level 0 token it is appended
            to baseexpr, then we are at level 1, we append
            2,+,3,+ tokens to level 1 so tree looks like
            {
                1:[2,+,3,+]
            }
            then we go to next level where tree looks like
            {
                1:[2,+,3,+],
                2:[5,*]
            }
            we go to next level, since it has no tokens yet, it's
            not created, and we go to our final level
            {
                1:[2,+,3,+],
                2:[5,*],
                4:[3]
            }
            now we start closing braces
            on brace closed, the expression of highest level is
            executed, and result is appended to previous level,
            if previous level isn't created, then we'll create
            it at this moment.
            After level 4 brace is closed:
            {
                1:[2,+,3,+],
                2:[5,*],
                3:[3]
            }
            then we get our + and 3 appended to third level, and
            before level 3 brace is closed we have
            {
              1:[2,+,3,+],
              2:[5,*],
              3:[3+3]   
            }
            now we evaluate and append to previous, and so on,
            when we have our first level brace closed, we append
            executed result to baseexpr, after that we have baseexpr
            containg simple operations that can be executed with
            calculateExpression.
        '''

        baseexpr = []
        tree = {}
        level = 0


        for token in tokens:
            if token == Token('OB','('):
                level += 1
                continue
            elif token == Token('CB',')'):
                if tree:
        
                    keys = sorted(tree.keys(),reverse=True)
                    result = self.calculateExpression(tree[keys[0]])
                    if level > 0:
                        if (level-1) in tree:
                            tree[level-1].append(result)
                        else:
                            tree[level-1] = [result]
             
                        del tree[level]
                   
                    else:
                        lprint('Failing on braces evaluation',1)
                        self.error()
    
                if level == 1:
                    baseexpr.append(result)
                    tree.clear()

                level -= 1
                continue

            if level == 0:
                baseexpr.append(token)
                continue

            if level not in tree:
                tree[level]=[token]
            else:
                tree[level].append(token)


        if level != 0:
            self.error()

        result = self.calculateExpression(baseexpr).value
        lprint('Result from interpretation is {res}'.format(
            res=result), 3)
        return result


def main():
    '''
        Our program main entry point
    '''
    while True:
        try:
            v_major = sys.version_info.major
            inp = ''
            if v_major == 3:
                inp = input('calc > ')
            elif v_major == 2:
                inp = raw_input('calc > ')
            else:
                raise Exception("Python version not supported")
        except EOFError:     
            '''
            exception EOFError
      
            Raised when one of the built-in functions
            (input() or raw_input()) hits an end-of-file condition (EOF)
            without reading any data. 
            (N.B.: the file.read() and file.readline() methods return an empty string 
            when they hit EOF.)
            '''
            break;
        
        except KeyboardInterrupt:
            '''User exited program  '''

            print('\nBye bye')
            break;

        if not inp:
            continue

        #after we ashured we have some input we can init our
        #interpreter
        
        interpreter = Interpreter(inp)
    
        # Check for parsing errors 
        try:
            result = interpreter.expr()
            #If we end up here, we're cool :) 
            print(result)
        except ParsingError as e:
            #We'll print the exception
            print(str(e))
        

if __name__ == '__main__':
    main()