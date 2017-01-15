from __future__ import division
import pprint

INT = 'int'
PLUS = 'plus'
MINUS = 'minus'
MUL = 'mul'
DIV = 'div'
OB = 'ob'
CB = 'cb'
EOF = 'EOF'


DEBUG =  False
class AST(object):
	"""Abstract syntax tree"""
	pass

class BinOp(AST):
	def __init__(self,left,op,right):
		self.left = left
		self.op = op
		self.right = right
	def __str__(self):
		"""
			String representation  of the class
		"""
		return "BinOP({left}-{op}-{right})".format(
				left = self.left,
				op = self.op,
				right = self.right
			)
	def __repr__(self):
		"""
			Representation of the class
		"""
		return self.__str__()
class Num(AST):
	def __init__(self,token):
		self.token = token
		self.value = token.value
		

class Token(object):

	def __init__(self,token_type,value):
		"""
			Token is object that has type
			and value.
		"""
		self.type = token_type
		self.value = value

	def __str__(self):
		"""
			String representation  of the class
		"""
		return "Token({tip},{vrijednost})".format(
				tip  = self.type,
				vrijednost = self.value
			)
	def __repr__(self):
		"""
			Representation of the class
		"""
		return self.__str__()

	def __eq__(self,other):
		return self.type == other.type

single_token_mapper={
	'+':Token(PLUS,'+'),
	'-':Token(MINUS,'-'),
	'*':Token(MUL,'*'),
	'/':Token(DIV,'/'),
	'(':Token(OB,'('),
	')':Token(CB,')')
}

ops = {
	'+':lambda x,y:x+y,
	'-':lambda x,y:x-y,
	'*':lambda x,y:x*y,
	'/':lambda x,y:x/y
}

class ParsingError(Exception):
	""" Error while parsing"""
	def __init__(self,message):
	    super(ParsingError, self).__init__(message)

class Parser(object):
	"""
		Our arithmethic expression calculator
	"""
	def __init__(self,inp):

		self.inp = inp
		self.pos = 0
		self.current_char = inp[0]
		self.current_token = self.getNextToken()


	def error(self,message = "Error in parsing"):
		print message
		raise ParsingError(message)

	def advance(self):
		if self.pos < len(self.inp)-1:
			self.pos += 1
			self.current_char = self.inp[self.pos]
			if DEBUG:
				print(r"""Advancing to position {pos}
and setting current char to {char}""".format(
				         	pos = self.pos,
				         	char = self.current_char
				     ))
		else:
			self.current_char = ""
			
	def skip_whitespace(self):
		while self.current_char.isspace():
			self.advance()

	def getNextToken(self):

	
		if self.current_char == ' ':
			self.skip_whitespace()
		if self.current_char.isdigit():
			token = Token(INT,self.number())
			return token
		if self.current_char in single_token_mapper:
			token = single_token_mapper[self.current_char]
			self.advance()
			return token
		if self.pos > len(self.inp) - 1 or not self.current_char:
			token = Token(EOF,None)
			return token

		self.error()

	def factor(self):
		token = self.current_token
		if token.type == INT:
			self.eat([INT])
			return Num(token)
		elif token.type == OB:
			self.eat([OB])
			node = self.expr()
			self.eat([CB])
			return node
		
	

	def term(self):
		node = self.factor()
		#print "In term current token is %s"%self.current_token
		while self.current_token.type in (DIV,MUL):
				token = self.current_token
				self.eat([DIV,MUL])
				node = BinOp(node,token,self.factor())
		return node
				
			
			

	def eat(self, TokenType):
		"""
			Check that TokenType is 
			current_token.type, if not
			raise Exception.
		"""
		if self.current_token.type in TokenType:
			self.current_token = self.getNextToken()
			
		else:
			self.error()
	def expr(self):
		"""

			expr = term (PLUS|MINUS) term
			term = factor (*|/) factor
			factor = int | ob[(] expr cb[)]
		"""
		node = self.term()
		while self.current_token.type in (PLUS,MINUS):
			token = self.current_token
			self.eat([PLUS,MINUS])
			node = BinOp(node,token,self.term())
			

		return node



	def number(self):
		result = ''
		while (self.current_char.isdigit() or
			   self.current_char == '.'):
			if DEBUG:
				print("Appending to int token {digit}".format(
						digit = self.current_char
					))
			result += self.current_char
			self.advance()
		return float(result)

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
    	#here we have our full tree
        return self.visit(self.tree)

def main():

	while True:

		inp = raw_input("expr > ")
		if inp:
			parser = Parser(inp)
			try:
				result = parser.expr()
				interpreter = Interpreter(result)
				print(interpreter.interpret())
			except ParsingError as e:
				print(str(e))
		else:
			print("Please enter a valid ")



if __name__ == '__main__':
	main()