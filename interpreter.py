from __future__ import division
#from collection import deque
import operator

#Token types
#
#EOF (end of file) token is used to indicate that
#there is no more input left for lexical analysis

INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTYPLY = 'MULTYPLY'
DIVIDE = 'DIVIDE'
OB = 'OB'
CB = 'CB'
EOF = 'EOF'

ops = {
        '+':operator.add,
        '-':operator.sub,
        '*':lambda x,y: x*y,
        '/':lambda x,y: x/y
      }

class Token(object):
    def __init__(self,type,value):
        #some of token types of above
        #this will be used for __eq__ method
        #so we can easily search and compare tokens
        self.type = type

        #token value is defined in get_next_token
        self.value = value;

    #this is neat thing I didn't know about before..
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
        print("Initializing interpreter with %s"%inp)

    def error(self):
        error_message = "Error parsing input"
        print error_message
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
        elif current_char == '(':
            self.advance()
            token = Token(OB,'(')
            return token
        elif current_char == ')':
            self.advance()
            token = Token(CB,')')
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
           # print("Eating {token}".format(
           #     token=self.current_token
           #    ))
            self.consume_whitespace()
            self.current_token = self.get_next_token();
        else:
            self.error()

    def doOperations(self,tokenList,operationToken):
            """
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

            """
            index = tokenList.index(operationToken)
            if index != 0 and index != len(tokenList)-1:
                a = tokenList[index-1]
                b = tokenList[index+1]
                if a.type == INTEGER and b.type==INTEGER:
                    result = ops[tokenList[index].value](
                                int(a.value),
                                int(b.value)
                            )  
                    tokenList.insert(index-1,Token(INTEGER,result))
                    for i in range(index+2,index-1,-1):
                        del tokenList[i]          
                    #print tokenList
                else:
                    self.error()
            else:
                self.error()


    def calculateExpression(self,tokens):
        """
            Do operations on tokens list
            First do multiplication and division, 
            and do them in order.
            Then we can do addition and subtraction
            with order too (without order it may
            use first subtraction, and then addition
            which may cause undesired effeects)
            on token list.Since we
            pass tokens list to doOperations, after
            all processes are finished we should have
            a single token list, so we can just return
            tokens[0], if we don't have a single token
            raise Exception.

        """
        while (Token(MULTYPLY,"*") in tokens or
               Token(DIVIDE,"/") in tokens):
            m_index = len(tokens)+100
            d_index = len(tokens)+100
            if Token(MULTYPLY,'*') in tokens:
                m_index = tokens.index(Token(MULTYPLY,'*'))
            if Token(DIVIDE,'/') in tokens:
                d_index = tokens.index(Token(DIVIDE,'/'))
            
            if m_index > d_index:
                self.doOperations(tokens,Token(DIVIDE,'/'))
            else:
                self.doOperations(tokens,Token(MULTYPLY,'*'))

        while (Token(PLUS,"+") in tokens or
               Token(MINUS,"-") in tokens):
            p_index = len(tokens)+100
            m_index = len(tokens)+100
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

        """
        baseexpr = []
        tree = {}
        level = 0


        for token in tokens:
            if token == Token('OB','('):
                level += 1
                continue
            elif token == Token('CB',')'):
                if tree:
                    #print "HERE IS A TREE - %r"%tree
                    keys = sorted(tree.keys(),reverse=True)
                    result = self.calculateExpression(tree[keys[0]])
                    if level > 0:
                        #print tree
                        if (level-1) in tree:
                            tree[level-1].append(result)
                        else:
                            tree[level-1] = [result]
             
                        del tree[level]
                   
                    else:
                        print "FAILING"
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
        #print baseexpr
        result = self.calculateExpression(baseexpr).value
        print("Result from interpretation is %s"%result)
        return result

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
        print(result)
        #except Exception as e:
            #We'll print the exception
        #    print(str(e))
        

"""
For python3 change raw_input to input .. 
"""

if __name__ == '__main__':
    main()
