#-------------------------------------------------------------------------------
# Name:        interpreter.py
# Purpose:     Attempt to parse simple expressions of the form p+q
#
# Author:      Akshay
#
# Created:     15-08-2015
#-------------------------------------------------------------------------------

def is_operator(char):
    return char in '*+/-%'

def valid_tokens(tokens):
    assert len(tokens) == 3, "Invalid expression"
    if not is_operator(tokens[0]):
        return False

    if isinstance(tokens[1], list):
        if not valid_tokens(tokens[1]):
            return False
    else:
        if not tokens[1].isdigit():
            return False

    if isinstance(tokens[2], list):
        if not valid_tokens(tokens[2]):
            return False
    else:
        if not tokens[2].isdigit():
            return False


    return True

def valid_expr(expr):
    return True
def tokenize(expr):
    """
    Break up the complex string expression into a list of [operator, expr, expr].
    Preconditions: Expr is a valid, bracketed infix expression containing numerals and +-*/ only.
    Return: List of [Operator, Expr, Expr] where Expr is either another [O, E, E] list or a string numeral.

    >>> tokenize('(34+46)')
    ['+', '34', '46']

    >>> tokenize('((45*66)+(66*11))')
    ['+', ['*', '45', '66'], ['*', '66', '11']]

    """
    tokens = [None, None, None]
    n = 0
    expr = expr[1:-1] #remove brackets
    i = 0
    if expr[0] == '(':
        #find brackets
        n += 1
        i += 1
        while n != 0 and i < len(expr):
            if expr[i] == '(':
                n += 1

            if expr[i] == ')':
                n -= 1

            i += 1
        tokens[1] = tokenize(expr[:i]) #recursively tokenize the expr
    else:
        #this is an int.
        while expr[i].isdigit():
            i += 1
        tokens[1] = expr[:i]
        assert tokens[1].isdigit(), "Error in parsing expression. Wanted number, found {}".format(token[1])

    while expr[i].isspace() and i < len(expr): #ignore white_space
        i+=1

    tokens[0] = expr[i] #operator
    assert is_operator(tokens[0]), "Error in parsing expression. Wanted operator, found {}".format(tokens[0])

    i += 1

    while expr[i].isspace() and i < len(expr): #ignore white_space
        i+=1

    if expr[i] == '(':
        tokens[2] = tokenize(expr[i:])
    else:
        tokens[2] = expr[i:]
        assert tokens[2].isdigit(), "Error in parsing expression. Wanted number, found {}".format(token[2])
    return tokens

def perform_operation(o, a, b):
    """Perform (o a b). Assume o is +, /, *, -."""
    #print('Performing operation ({} {} {})'.format(o,a,b))
    if o == '+':
        return a + b

    if o == '-':
        return a - b

    if o == '*':
        return a*b

    if not b:
        raise ValueError('Cannot divide by zero')

    if o == '%':
        return a%b

    if o == '/':
        return a/b

    raise ValueError('Could not interpret operator: {}'.format(o))


def perform_calc(tokens):
    """tokens is of the form ['+', p, q]"""
    operator = tokens[0]
    first_arg = tokens[1]
    second_arg = tokens[2]
    if isinstance(first_arg, list):
        first_arg = perform_calc(first_arg)

    if isinstance(second_arg, list):
        second_arg = perform_calc(second_arg)

    #print('second arg == {} type(second arg == {} repr(second arg) === {}'.format(second_arg, type(second_arg), repr(second_arg)))
    return perform_operation(operator, int(first_arg), int(second_arg))


def add_brackets(expression):
    """TODO"""
    if expression[0] != '(':
        return '('+expression+')'

    return expression

def parse(expression):
    """Parse arithmetic expression of the form p+q, p-q, p*q, p/q."""
    #if not valid_expr(expression):
        #raise ValueError('Could not parse the expression')

    #print('expression = {}'.format(expression))
    expression = add_brackets(expression)

    try:
        tokens = tokenize(expression)
    except IndexError as e:
        raise ValueError("Error in parsing expression {}".format(expression))

    if not valid_tokens(tokens):
        raise ValueError('Error parsing expression, tokens = {}'.format(tokens))
    #print("In parse: expression = {}".format(expression))

    return perform_calc(tokens)

def convert_to_lisp(tokens):
    """Convert the output of tokenize into a bracketed prefix operation."""
    res = '('+tokens[0]
    if isinstance(tokens[1], list):
        res += ' ' + convert_to_lisp(tokens[1])
    else:
        res += ' ' + tokens[1]

    if isinstance(tokens[2], list):
        res += ' ' + convert_to_lisp(tokens[2])
    else:
        res += ' ' + tokens[2]

    res += ')'

    return res


def test():
    assert parse('(3+4)') == 7, "Failed test: parse('3+4') == 7, got value: {}".format(parse('(3+4)'))
    assert parse('(5+6)') == 11, "Failed test: parse('5+6') == 7, got value: {}".format(parse('(5+6)'))
    assert parse('(81-4)') == 77, "Failed test: parse('81-4') == 77, got value: {}".format(parse('(81-4)'))
    assert parse('(46-46)') == 0, "Failed test: parse('46-46') == 0, got value: {}".format(parse('(46-46)'))

def main():
    test()
    print('All tests passed!')

if __name__ == '__main__':
    main()
