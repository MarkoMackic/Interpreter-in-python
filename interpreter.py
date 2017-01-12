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
			Token(EOF,None)

		"""

		return 'Token({type},{value})'.format(
			type = self.type,
            value = repr(self.value)
		)

    def __repr__(self):
        return self.__str__()

