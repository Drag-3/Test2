from lexer import tokens
import ply.yacc as yacc

# Parsing rules
def p_program(p):
    '''program : declaration_list'''

def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list declaration'''

def p_declaration(p):
    '''declaration : var_declaration
                        | const_declaration
                      | fun_declaration
                     | statement'''


def p_var_declaration(p):
    '''var_declaration : VAR IDENTIFIER type_specifier_opt ASSIGN expression SEMICOLON'''

def p_const_declaration(p):
    '''const_declaration : CONST IDENTIFIER type_specifier_opt ASSIGN expression SEMICOLON'''

def p_type_specifier_opt(p):
    '''type_specifier_opt : TYPEHINTCOLON type_specifier
                          | empty'''

def p_type_specifier(p):
    '''type_specifier : INT
                      | FLOAT
                      | STRING
                      | TRUE
                        | FALSE
                      | STREAM
                      | EVENT'''

def p_fun_declaration(p):
    '''fun_declaration : FN IDENTIFIER LPAREN params RPAREN compound_stmt'''

def p_params(p):
    '''params : param_list
              | empty'''

def p_param_list(p):
    '''param_list : param
                  | param_list COMMA param'''

def p_param(p):
    '''param : IDENTIFIER type_specifier_opt'''


def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''

def p_statement(p):
    '''statement : expression_stmt
                    | compound_stmt
                    | selection_stmt
                    | iteration_stmt
                    | return_stmt'''

def p_expression_stmt(p):
    '''expression_stmt : expression SEMICOLON'''

def p_selection_stmt(p):
    '''selection_stmt : IF LPAREN expression RPAREN statement
                      | IF LPAREN expression RPAREN statement ELSE statement'''

def p_iteration_stmt(p):
    '''iteration_stmt : WHILE LPAREN expression RPAREN statement
                      | FOR LPAREN expression_stmt expression_stmt expression RPAREN statement'''

def p_return_stmt(p):
    '''return_stmt : RETURN expression SEMICOLON'''

def p_expression(p):
    '''expression : assignment_expression
          | simple_expression'''

def p_simple_expression(p):
    '''simple_expression : additive_expression
                         | simple_expression relational_operator additive_expression'''

def p_relational_operator(p):
    '''relational_operator : LE
                           | LT
                           | GT
                           | GE
                           | EQUALS
                           | NE'''

def p_additive_expression(p):
    '''additive_expression : multiplicative_expression
                           | additive_expression additive_operator multiplicative_expression'''

def p_additive_operator(p):
    '''additive_operator : PLUS
                         | MINUS'''


def p_multiplicative_expression(p):
    '''multiplicative_expression : unary_expression
                                 | multiplicative_expression multiplicative_operator unary_expression'''

def p_multiplicative_operator(p):
    '''multiplicative_operator : MULTIPLY
                               | DIVIDE'''

def p_unary_expression(p):
    '''unary_expression : postfix_expression
                        | unary_operator unary_expression'''

def p_postfix_expression(p):
    '''postfix_expression : primary_expression
                          | postfix_expression LPAREN expression_list RPAREN
                          | postfix_expression LBRACE expression RBRACE'''

def p_primary_expression(p):
    '''primary_expression : IDENTIFIER
                          | LPAREN expression RPAREN'''


def p_unary_operator(p):
    '''unary_operator : PLUS
                      | MINUS
                      | NOT'''

def p_assignment_expression(p):
    '''assignment_expression : postfix_expression ASSIGN expression
                             | postfix_expression ASSIGN STREAM expression'''

def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''

def p_compound_stmt(p):
    '''compound_stmt : LBRACE declaration_list statement_list RBRACE'''

def p_empty(p):
    '''empty :'''
    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

# Test it out
data = '''
var x : int = 5;
'''

# Parse
output = parser.parse(data, tracking=True, debug=True)
print("Parsing done!")

# Print the output
print(output)
