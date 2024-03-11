import ply.yacc as yacc
from lexer import tokens, lexer



# Comments are handled in the lexer, so they're not part of the parser rules.

# Program Structure
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

# A statement is a single line of code that performs an action
# It can be a declaration, an expression, or a control flow statement
def p_statement(p):
    '''statement : declaration
                | expression'''
    p[0] = p[1]  # declaration


def p_statement_list(p):
    '''statement_list : statement SEMICOLON
                      | statement_list statement SEMICOLON
                      | statement_list NEWLINE statement SEMICOLON'''
    if len(p) == 2:  # single statement
        p[0] = [p[1]]
    else:  # statement list
        p[0] = p[1] + (p[2],)  # append new statement


def p_function_call(p):
    '''function_call : IDENTIFIER LPAREN opt_arg_list RPAREN'''
    p[0] = ('function_call', p[1], p[3])  # function name, arguments


def p_opt_arg_list(p):
    '''opt_arg_list : arg_list
                    | empty'''
    p[0] = p[1]  # list of arguments or None


def p_arg_list(p):
    '''arg_list : expression
                | arg_list COMMA expression'''
    if len(p) == 2:  # single argument
        p[0] = [p[1]]
    else:  # argument list
        p[0] = p[1] + [p[3]]  # append new argument


# Function Definitions
def p_function_definition(p):
    '''function_definition : FN IDENTIFIER LPAREN opt_param_list RPAREN LBRACE statement_list RETURN statement RBRACE
                           | FN IDENTIFIER LPAREN opt_param_list RPAREN typehint LBRACE statement_list RETURN statement RBRACE'''
    # Handling optional return type
    if len(p) == 9:
        p[0] = ('function_definition', p[2], p[4], None, p[7])
    else:
        p[0] = ('function_definition', p[2], p[4], p[6], p[8])


def p_function_body(p):
    '''function_body : LBRACE statement_list RBRACE'''
    p[0] = p[2]  # statements

def p_return_statement(p):
    '''return_statement : RETURN expression'''
    p[0] = ('return', p[2])  # return statement


def p_lambda_function(p):
    '''lambda_function : FN LPAREN opt_param_list RPAREN LAMBDA LBRACE statement_list RBRACE
                       | FN LPAREN opt_param_list RPAREN typehint LAMBDA LBRACE statement_list RBRACE
                       | LPAREN opt_param_list RPAREN LAMBDA LBRACE statement_list RBRACE
                       | LPAREN opt_param_list RPAREN typehint LAMBDA LBRACE statement_list RBRACE'''
    # Handling lambda functions similarly
    if len(p) == 8:
        p[0] = ('lambda_function', p[3], None, p[6])
    else:
        p[0] = ('lambda_function', p[3], p[5], p[7])


def p_opt_param_list(p):
    '''opt_param_list : param_list
                      | empty'''
    p[0] = p[1]  # list of parameters or None


def p_param_list(p):
    '''param_list : param
                  | param_list COMMA param'''
    if len(p) == 2:  # single param
        p[0] = [p[1]]
    else:  # param list
        p[0] = p[1] + [p[3]]  # append new param


def p_param(p):
    '''param : IDENTIFIER
             | IDENTIFIER typehint'''
    if len(p) == 2:
        p[0] = (p[1], None)
    else:
        p[0] = (p[1], p[3])  # parameter name, type

# A declaration is a statement that declares a variable or constant
def p_declaration(p):
    '''declaration : VAR declaration_base
                    | CONST declaration_base
                    | function_definition'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('declaration', p[1], p[2])  # var/const, declaration


# Variable Declaration
def p_declaration_base(p):
    '''declaration_base : IDENTIFIER
                        | IDENTIFIER ASSIGN expression
                        | IDENTIFIER typehint
                        | IDENTIFIER typehint ASSIGN expression
                        '''
    if len(p) == 2:
        p[0] = ('declaration_base', p[1], None, None)  # name
    elif len(p) == 3:
        p[0] = ('declaration_base', p[1], p[2], None)  # name, type
    elif len(p) == 4:
        p[0] = ('declaration_base', p[1], None, p[3])  # name, expression
    else:
        p[0] = ('declaration_base', p[1], p[2], p[3])  # name, type, expression

# Typehint
def p_typehint(p):
    '''typehint : TYPEHINTCOLON type'''
    p[0] = p[2]  # type


# Types
def p_type(p):
    '''type : SINT
            | SFLOAT
            | SSTRING
            | SBOOL
            | SSTREAM
            | SEVENT'''
    p[0] = p[1]

def p_primative_type(p):
    '''ptype : INT
            | FLOAT
            | STRING
            | TRUE
            | FALSE'''
    p[0] = p[1]

# Expressions. An Expression is a line that yields a value.
# Some examples are function calls, arithmetic operations, etc.

def p_binary_arithmetic_operation(p):
    '''binary_arithmetic_operation : expression binary_arithmetic_operation_rest
                        | expression binary_arithmetic_operation_rest
                        | expression binary_arithmetic_operation_rest
                        | expression binary_arithmetic_operation_rest

    '''

    p[0] = (p[2], p[1], p[3])

def p_binary_arithmetic_operation_rest(p):
    '''binary_arithmetic_operation_rest : PLUS expression
                        | MINUS expression
                        | MULTIPLY expression
                        | DIVIDE expression
    '''
    p[0] = (p[1], p[2])

def p_unary_arithmetic_operation(p):
    '''unary_arithmetic_operation : MINUS expression
                        | PLUS expression
    '''
    p[0] = (p[1], p[2])

def p_binary_logic_operation(p):
    '''binary_logic_operation : expression binary_logic_operation_rest
                        | ptype binary_logic_operation_rest

    '''
    p[0] = (p[2][0], p[1], p[2][1])


def p_binary_logic_operation_rest(p):
    '''binary_logic_operation_rest : EQUALS ptype
                        | GT ptype
                        | LT ptype
                        | GE ptype
                        | LE ptype
                        | AND ptype
                        | OR ptype
                        |  EQUALS expression
                        | GT expression
                        | LT expression
                        | GE expression
                        | LE expression
                        | AND expression
                        | OR expression
    '''
    p[0] = (p[1], p[2])
def p_unary_logic_operation(p):
    '''unary_logic_operation : NOT expression
    '''
    p[0] = (p[1], p[2])

def p_logic_expression(p):
    '''logic_expression : binary_logic_operation
                        | unary_logic_operation
    '''
    p[0] = p[1]

def p_function_call_expression(p):
    '''function_call_expression : function_call
    '''
    p[0] = p[1]

def p_object_call_expression(p):
    '''object_call_expression : expression CALL expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_stream_operation(p):
    '''stream_operation : unary_stream_operation
                        | binary_stream_operation
                        | special_stream_operation
    '''
    p[0] = p[1]

def p_unary_stream_operation(p):
    '''unary_stream_operation : IDENTIFIER TO_STREAM

    '''
    p[0] = (p[2], p[1])

def p_binary_stream_operation(p):
    '''binary_stream_operation : IDENTIFIER CHAIN IDENTIFIER
                        | IDENTIFIER STREAMSPLIT IDENTIFIER
                        | IDENTIFIER STREAMMERGE IDENTIFIER
                        | IDENTIFIER FEEDBACK IDENTIFIER
    '''
    p[0] = (p[2], p[1], p[3])

def p_special_stream_operation(p):
    '''special_stream_operation : IDENTIFIER FILTEROP LPAREN logic_expression RPAREN
                        | IDENTIFIER MAP LPAREN logic_expression RPAREN
                        | IDENTIFIER REDUCE LPAREN logic_expression RPAREN
    '''
    p[0] = (p[2], p[1], p[4])



def p_simple_expression(p):
    '''simple_expression : ptype
                        | type
                        | IDENTIFIER
                        | LPAREN expression RPAREN
                        | lambda_function
                        | control_flow
    '''
    p[0] = p[1]

def p_complex_expression(p):
    '''complex_expression : binary_arithmetic_operation
                        | unary_arithmetic_operation
                        | logic_expression
                        | function_call_expression
                        | object_call_expression
                        | stream_operation
    '''
    p[0] = p[1]

def p_expression(p):
    '''expression : simple_expression
                | complex_expression
    '''

def p_control_flow(p):
    '''control_flow : conditional
                    | loop'''
    p[0] = p[1]

# Conditional Statements
def p_conditional(p):
    '''conditional : IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE'''
    p[0] = ('if-else', p[3], p[6], p[10])  # condition, if statements, else statements

def p_conditional_no_else(p):
    '''conditional : IF LPAREN expression RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('if', p[3], p[6])  # condition, if statements

# Loops
def p_loop(p):
    '''loop : FOR LPAREN declaration SEMICOLON expression SEMICOLON expression RPAREN LBRACE statement_list RBRACE
            | WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE'''
    if len(p) == 8:  # while loop
        p[0] = ('while', p[3], p[6])  # condition, statements
    else:  # for loop
        p[0] = ('for', p[3], p[5], p[7], p[10])  # declaration, condition, increment, statements



# Empty Rule
def p_empty(p):
    'empty :'
    pass


def p_error(p):
    global parser, string_lines
    if p:
        print(f"Unexpected token {p.value} at line {p.lineno}")
        print("-" * 20)
        print("Context:")
        # Determine the line number of the error
        line_num = p.lineno

        # Gen Line numbers of the context
        l_bound = line_num - 2 if line_num - 2 > 0 else 0
        u_bound = line_num + 2 if line_num + 2 < len(string_lines) else len(string_lines)

        # Print the context lines
        for i in range(l_bound, u_bound):
            if i == line_num:
                print(f"{i}: {string_lines[i]} <---")
            else:
                print(f"{i}: {string_lines[i]}")

        # Skip ahead to the next line
        while True:
            tok = parser.token()  # Get the next token
            if not tok or tok.type == 'NEWLINE': break
        parser.errok()
    else:
        print("Syntax error at EOF")





# Section: Parser Configuration
parser = yacc.yacc(debug=True)


# Section: Parsing Function
def parse(data, lexer=lexer):
    global string_lines
    string_lines = data.splitlines()
    return parser.parse(data, lexer=lexer)


# Section: Testing and Debugging (Optional)
if __name__ == "__main__":
    # Example test code to parse a string
    string_lines = []
    simple_test_string = """
    // This is a comment
    fn main() {
        var x: int = 5;
        var y = 6;
        var z = x + y;
        if (z > 10) {
            return true;
        } else {
            return false;
        }
    }
    """
    test_string = '''
var dataStream = socket.toStream(); // Create a stream from a socket
var output = dataStream.filter((data) => data > 0); // Filter out negative data

fn processData(input: int): int {
    return (input - 32) * 5 / 9; // Convert Fahrenheit to Celsius
}
/*
Convert on each data entry
*/
dataStream.onEntry(processData); // Process each data entry as they arrive

dataStream ? (data => data > 0) $ (data => data * 2) ^ (data => data + 1); // Filter, map, and reduce
dataStream >> output; // Chain the output stream
/*
First process the data (events are handled before filters)
Then we apply any filters maps and more the order they are attached
Finally we reduce the data to a single value
Then we chain the output to the next stream
/* 
    This code above is equivalent to the following:
    var output = dataStream.filter((data) => data > 0).map((data) => data * 2).reduce((data) => data + 1);
*/

// This is not equivalent to the following:
dataStream >> output $ (data => data * 2) ^ (data => data + 1); // Chain the output stream
// In the above code the original dataStream is chained to the output stream before the filters are applied therefore
// the filters are applied only on the output stream and not the original dataStream

//This however should allow some pretty cool one liners such as

socket.toStream() ? (data => data > 0)>> output $ (data => data * 2) ^ (data => data + 1);

// Multiple streams can be merged into one
var mergedStream = dataStream ++ output;
// Or if you have many streams
var mergedStream = dataStream1 ++ dataStream2 ++ dataStream3 ++ output; // This will merge all the streams into one
// Or you can split a stream into multiple streams
var lower50;
var upper50;
dataStream | (data => data < 50) ++ lower50 | (data => data > 50) ++ upper50; // Split the stream into two streams
// Any Data not split stays in the original stream. Therefore after the above code the original dataStream will only
// contain data that is exactly 50
// 

// Feedback loops can be created using the << operator
// This will create a feedback loop that will feed the output of the output stream back into the input of the dataStream
//The following code will read sensor data and change parameters of the sensor based on the data
var sensorData = sensor.toStream();
sensorData << output.onEntry(fn (data) => {adjustSensor(data)});

//The feedback operator will take a stream defined on the left, chain it to the stream defined on the right and then
//chain the output of the right stream to the left stream. This will create a feedback loop that will feed the output
// The above code implicitly defines the following feedback loop. Output is implicitly defined as the output of the sensor,
But a more explicit way to define the feedback loop would be:
var sensorData = sensor.toStream();
var output = sensorData.onEntry((data) => {adjustSensor(data)});  // Explicitly define the output stream
output >> sensorData;  // Chain the output to the input
// This will create the same feedback loop as the following code
sensorData >> output << sensorData; //Feedback implicitly defines the output stream and chains it to the input stream
'''
    string_lines = simple_test_string.splitlines()
    result = parse(simple_test_string, lexer)
    print(result)
