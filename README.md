I'm learning basics on intepreter implementatinos and practicing git

Here's a tutorial https://ruslanspivak.com/lsbasi-part1/

I'd recommend it, if you want to know more about how compilers and interpreters
work. It's a great tutorial :) 

##My code 

My code is contained in `interpreter.py` file and it's created by me doing homework from tutorial. It runs braces evaluation using token level dictonary , and then evaluates each level starting from the top down. After final brace is closed it's appended to basic expression variable.It does a unary operators parsing, and basic expression parsing. My solving methods modify tokens list, and there are insertion to list at specific indexes, so method is slower then the code from the tutorial. But it was my logic, and I've done it without exact plan. My code might be a bit more understandable as it's well commented, and explained to it's every part.

##Tests

Tests are done in `test.py` file, currently it passes all of them.
If you find a bug please create new issue with a bug description, and
modify test file for failing condition if you want.

##Tutorial code 

Tutorial code is currently in `interpreter_ast.py` and it's based on tutorial. At current stage, it builds up AST (Abstract syntax tree) from expression, and evaluates it with NodeVisitor, recursively bulding result. It currently doesn't support unary operators, but it's easy to implement.

##Contribution

Now I'm looking forward to implement math functions like sin,cos,tan,etc. 
If you want to help, be free to open pull requests for anything you add/remove from
the code :) 
Porting this interpreter to JS wouldn't be bad idea.


