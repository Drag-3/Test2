import ply.yacc as yacc

from StreamLanguage.ast.nodes.flow_control import IfNode, WhileNode, ForNode, BreakNode, ContinueNode
from StreamLanguage.ast.nodes.base import ParserNode
from StreamLanguage.ast.nodes.expressions import IdentifierNode, BinaryOperationNode, UnaryOperationNode
from StreamLanguage.ast.nodes.functions import FunctionCallNode, FunctionNode, ReturnNode
from StreamLanguage.ast.nodes.node_types import PrimitiveDataNode, PrimitiveBoolNode, PrimitiveIntNode, \
    PrimitiveFloatNode, PrimitiveStringNode
from StreamLanguage.ast.nodes.structure import ProgramNode, VariableDeclarationNode
from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
from StreamLanguage.sl_types.data_instances.primatives.float import SLFloat
from StreamLanguage.sl_types.data_instances.primatives.integer import SLInteger
from StreamLanguage.sl_types.data_instances.primatives.string import SLString
from StreamLanguage.sl_types.type_registry import TypeRegistry
from StreamLanguage.lexer.lexer import Lexer




class Parser:

    tokens = Lexer.tokens
    precedence = (  # This needed to be defined in this and NOT in the lexer This caused so many problems that a simple google search could have fixed...
        ('left', 'FEEDBACK'),       # '<<'
        ('left', 'STREAMMERGE'),    # '++'
        ('left', 'CHAIN'),          # '>>'
        ('left', 'STREAMSPLIT'),    # '|'
        ('left', 'OR'),             # '||'
        ('left', 'AND'),            # '&&'
        ('nonassoc', 'EQUALS', 'NE', 'GT', 'LT', 'GE', 'LE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE'),
        ('right', 'NOT'),
        ('right', 'UMINUS', 'UPLUS'),
    )

    # Comments are handled in the lexer, so they're not part of the parser rules.

    # Program Structure
    def p_program(self, p):
        '''program : statement_list'''
        p[0] = ProgramNode(p[1])  # program

    # A statement is a single line of code that performs an action
    # It can be a declaration, an expression, or a control flow statement
    def p_statement(self, p):
        '''statement : declaration
                    | expression SEMICOLON
                    | return_statement SEMICOLON
                    | control_flow
                    | assignment SEMICOLON'''
        p[0] = p[1]  # declaration


    def p_statement_list(self, p):
        '''statement_list : statement
                          | statement_list statement'''
        if len(p) == 2:  # single statement
            p[0] = [p[1]]  # Create a list with the single statement
        else:  # multiple statements
            p[0] = p[1] + [p[2]]  # Append the new statement to the list



    def p_function_call(self, p):
        '''function_call : IDENTIFIER LPAREN opt_arg_list RPAREN'''
        p[0] = FunctionCallNode(IdentifierNode(p[1]), p[3])



    def p_opt_arg_list(self, p):
        '''opt_arg_list : arg_list
                        | empty'''
        if p[1] is None:
            p[0] = []
        else:
            p[0] = p[1]  # list of arguments or None


    def p_arg_list(self, p):
        '''arg_list : expression
                    | arg_list COMMA expression'''
        if len(p) == 2:  # single argument
            p[0] = [p[1]]
        else:  # multiple arguments
            p[0] = p[1] + [p[3]]  # append new argument


    # Function Definitions
    def p_function_definition(self, p):
        '''function_definition : FN IDENTIFIER LPAREN opt_param_list RPAREN block_statement
                               | FN IDENTIFIER LPAREN opt_param_list RPAREN typehint block_statement'''
        function_name = IdentifierNode(p[2])
        params = p[4]  # List of parameters (param, None/Type)
        parameters, type_hints = [], []

        if params:
            for param in params:
                parameters.append(param[0])
                type_hints.append(param[1])

        if len(p) == 7:
            body = p[6]  # Function body
            p[0] = FunctionNode(function_name, parameters, body)
        else:
            return_type = p[6]  # Type hint
            body = p[7]
            p[0] = FunctionNode(function_name, parameters, body, return_type=return_type)


    def p_return_statement(self, p):
        '''return_statement : RETURN expression'''
        p[0] = ReturnNode(p[2])  # return statement

    def p_block_statement(self, p):
        '''block_statement : LBRACE statement_list RBRACE'''
        p[0] = p[2]  # statements


    def p_lambda_function(self, p):
        '''lambda_function : FN LPAREN opt_param_list RPAREN LAMBDA block_statement
                           | FN LPAREN opt_param_list RPAREN typehint LAMBDA block_statement
                           | LPAREN opt_param_list RPAREN LAMBDA block_statement
                           | LPAREN opt_param_list RPAREN typehint LAMBDA block_statement
                           | LPAREN opt_param_list RPAREN LAMBDA expression'''
        # Handling lambda functions similarly
        if len(p) == 7:
            if p[1] == 'fn':
                p[0] = ('lambda_function', p[3], None, p[6])
            else:
                p[0] = ('lambda_function', p[2], p[4], p[6])
        elif len(p) == 8:
            p[0] = ('lambda_function', p[3], p[5], p[7])
        elif len(p) == 6:
            p[0] = ('lambda_function', p[2], None, p[5])
        else:
            p[0] = ('lambda_function', p[3], p[5], p[7])


    def p_opt_param_list(self, p):
        '''opt_param_list : param_list
                          | empty'''
        p[0] = p[1]  # list of parameters or None


    def p_param_list(self, p):
        '''param_list : param
                      | param_list COMMA param'''
        if len(p) == 2:  # single param
            p[0] = [p[1]]
        else:  # multiple params
            p[0] = p[1] + [p[3]]  # append new param

    def p_param(self, p):
        '''param : IDENTIFIER
                 | IDENTIFIER typehint'''
        identifier = IdentifierNode(p[1])
        if len(p) == 2:
            p[0] = [identifier, None]
        else:
            p[0] = [identifier, p[2]]  # parameter name, type hint

    # A declaration is a statement that declares a variable or constant
    def p_declaration(self, p):
        '''declaration : VAR declaration_base SEMICOLON
                       | CONST declaration_base SEMICOLON
                       | function_definition'''
        if isinstance(p[1], FunctionNode):
            p[0] = p[1]  # This is a function definition
        else:
            identifier = IdentifierNode(p[2][0])
            type_hint = p[2][1]
            value = p[2][2]
            p[0] = VariableDeclarationNode(identifier, type_hint, value)



    # Variable Declaration
    def p_declaration_base(self, p):
        '''declaration_base : IDENTIFIER
                            | IDENTIFIER ASSIGN expression
                            | IDENTIFIER typehint
                            | IDENTIFIER typehint ASSIGN expression'''
        identifier = p[1]
        if len(p) == 2:
            p[0] = (identifier, None, None)
        elif len(p) == 3:
            # Either IDENTIFIER ASSIGN expression or IDENTIFIER typehint
            if p[2] == '=':
                p[0] = (identifier, None, p[3])
            else:
                p[0] = (identifier, p[2], None)
        elif len(p) == 4:
            # IDENTIFIER ASSIGN expression
            p[0] = (identifier, None, p[3])
        else:
            # IDENTIFIER typehint ASSIGN expression
            p[0] = (identifier, p[2], p[4])


    # Typehint
    def p_typehint(self, p):
        '''typehint : TYPEHINTCOLON type'''
        type_string = p[2]  # type
        meta_type = TypeRegistry.get_meta_type_by_name(type_string)
        p[0] = meta_type



    # Types
    def p_type(self, p):
        '''type : SINT
                | SFLOAT
                | SSTRING
                | SBOOL
                | SSTREAM
                | SEVENT'''
        p[0] = p[1]

    def p_primitive_type(self, p):
        '''ptype : INT
                 | FLOAT
                 | STRING
                 | TRUE
                 | FALSE'''
        if isinstance(p[1], int):
            p[0] = PrimitiveIntNode(p[1])
        elif isinstance(p[1], float):
            p[0] = PrimitiveFloatNode(p[1])
        elif isinstance(p[1], str):
            p[0] = PrimitiveStringNode(p[1])
        elif p[1] == 'true':
            p[0] = PrimitiveBoolNode(True)
        elif p[1] == 'false':
            p[0] = PrimitiveBoolNode(False)


    # Expressions. An Expression is a line that yields a value.
    # Some examples are function calls, arithmetic operations, etc.
    # With the precedence working I can use a single rule for all binary operations :)

    def p_expression_binop(self, p):
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression MULTIPLY expression
                      | expression DIVIDE expression
                      | expression EQUALS expression
                      | expression NE expression
                      | expression GT expression
                      | expression LT expression
                      | expression GE expression
                      | expression LE expression
                      | expression AND expression
                      | expression OR expression
                      | expression CHAIN expression
                      | expression STREAMSPLIT expression
                      | expression STREAMMERGE expression
                      | expression FEEDBACK expression
        '''
        operator = p[2]
        left = p[1]
        right = p[3]


        p[0] = BinaryOperationNode(operator, left, right)

    def p_expression_unary(self, p): # Unary minus The %prec just applies the precedence to the rule UMINUS is not a tokren
        '''expression : MINUS expression %prec UMINUS
                      | PLUS expression %prec UPLUS
                      | NOT expression
        '''
        operator = p[1]
        operand = p[2]
        p[0] = UnaryOperationNode(operator, operand)


    def p_control_flow(self, p):
        '''control_flow : conditional
                        | loop'''
        p[0] = p[1]

    def p_expression_group(self, p):
        '''expression : LPAREN expression RPAREN'''
        p[0] = p[2]

    def p_expression_number(self, p):
        '''expression : INT
                      | FLOAT'''
        if isinstance(p[1], int):
            p[0] = PrimitiveIntNode(SLInteger(p[1]))
        else:
            p[0] = PrimitiveFloatNode(SLFloat(p[1]))

    def p_expression_string(self, p):
        '''expression : STRING'''
        p[0] = PrimitiveStringNode(SLString(p[1]))

    def p_expression_boolean(self, p):
        '''expression : TRUE
                      | FALSE'''
        value = True if p[1] == 'TRUE' else False
        p[0] = PrimitiveBoolNode(SLBoolean(value))

    def p_expression_identifier(self, p):
        '''expression : IDENTIFIER'''
        p[0] = IdentifierNode(p[1])

    def p_expression_function_call(self, p):
        '''expression : function_call'''
        p[0] = p[1]

    #def p_expression_object_call(p):
    #    '''expression : expression CALL function_call'''
    # I do not have classes yet so I will not implement this yet

    def p_expression_to_stream(self, p):
        '''expression : expression TO_STREAM'''
        p[0] = UnaryOperationNode('to_stream', p[1])


    def p_expression_lambda(self, p):
        '''expression : lambda_function'''
        p[0] = p[1]


    # Conditional Statements
    def p_conditional(self, p):
        '''conditional : IF LPAREN expression RPAREN block_statement ELSE block_statement
                       | IF LPAREN expression RPAREN block_statement'''
        if len(p) == 6:  # if without else
            p[0] = IfNode(p[3], p[5])
        else:  # if with else
            p[0] = IfNode(p[3], p[5], p[7])


    # Loops
    def p_loop(self, p):
        '''loop : FOR LPAREN declaration SEMICOLON expression SEMICOLON expression RPAREN block_statement
                | WHILE LPAREN expression RPAREN block_statement'''
        if len(p) == 8:  # while loop
            p[0] = WhileNode(p[3], p[5])  # condition, body
        else:  # for loop
            p[0] = ForNode(p[3], p[5], p[7], p[9])  # initializer, condition, increment, body

    def p_assignment(self, p):
        '''assignment : IDENTIFIER ASSIGN expression'''
        p[0] = ('assignment', p[1], p[3])  # variable, expression



    # Empty Rule
    def p_empty(self, p):
        'empty :'
        p[0] = None  # Return None


    def p_error(self, p):  # This works but isnt how I like it
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
                tok = self.parser.token()  # Get the next token
                if not tok or tok.type == 'NEWLINE': break
            self.parser.errok()
        else:
            print("Syntax error at EOF")


    def __init__(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        self.lexer = Lexer()

    def parse(self, data, lexer=None, debug=False):
        if lexer is None:
            lexer = self.lexer
        return self.parser.parse(data, lexer=lexer, debug=debug)

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
    
    //main();
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

dataStream ? ((data) => data > 0) $ ((data) => data * 2) ^ ((data) => data + 1); // Filter, map, and reduce
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
    parser = Parser()
    result = parser.parse(test_string)
    print(result)
    #print(result.evaluate(Context()))

# I need to add special rules that determine how the stream expressions work. IE filters, maps need a condition etc