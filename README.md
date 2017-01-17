I'm learning basics on intepreter implementatinos and practicing git

Here's a tutorial https://ruslanspivak.com/lsbasi-part1/

I'd recommend it, if you want to know more about how compilers and interpreters
work. It's a great tutorial :) 

##My code 

My code is contained in `interpreter.py` file and it's created by me doing homework from tutorial. It runs braces evaluation using token level dictonary , and then evaluates each level starting from the top down. After final brace is closed it's appended to basic expression variable.It does a unary operators parsing, and basic expression parsing. My solving methods modify tokens list, and there are insertion to list at specific indexes, so method is slower then the code from the tutorial. But it was my logic, and I've done it without exact plan. 

##Tutorial code 

Tutorial code is currently in `interpreter_ast.py` and it's based on tutorial. At current stage, it builds up AST (Abstract syntax tree) from expression with sequential applying of syntax grammer rules, and evaluates it with NodeVisitor, recursively bulding result. It currently doesn't support unary operators, but it's easy to implement.


##Tests

Tests are done in `test.py` file, currently it passes all of them.
If you find a bug please create new issue with a bug description, and
modify test file for failing condition if you want.

Now I ran a few speed tests to compare AST vs my parser

Input was `(18/2)*(((9 * 9 - 1)/ 2)-(5 * 20 - (7 * 9 - 2)))`

Tests of AST syntax parser

```

marko@DevLaptop:~/Radna površ/InterpreterTutorial$ python test_ast.py 
.......
Timing for 1000 runs of interpretation is 204.503059387ms

.
----------------------------------------------------------------------
Ran 8 tests in 0.206s

OK

```

Tests of my parser

```

marko@DevLaptop:~/Radna površ/InterpreterTutorial$ python test.py 
.......
Timing for 1000 runs of interpretation is 355.632066727ms

..
----------------------------------------------------------------------
Ran 9 tests in 0.358s

OK

```

##Conclusion

So in conclusion comparing best cases from a couple of test ran on my comuter.
AST can be twice faster. But for creating the algorithms from my head, I'm very proud of my interpreter :) 




##Contribution

Now I'm looking forward to implement math functions like sin,cos,tan,etc. 
If you want to help, be free to open pull requests for anything you add/remove from
the code :) 
Porting this interpreter to JS wouldn't be bad idea.


