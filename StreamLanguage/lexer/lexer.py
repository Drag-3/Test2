from ply import lex


class Lexer:
    # Reserved words mapping
    reserved = {
        'fn': 'FN',
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'return': 'RETURN',
        'true': 'TRUE',
        'false': 'FALSE',
        r'<stream>': 'STREAM',
        r'<event>': 'EVENT',
        'var': 'VAR',
        'const': 'CONST',
        'int': 'SINT',
        'float': 'SFLOAT',
        'string': 'SSTRING',
        'event': 'SEVENT',
        'stream': 'SSTREAM',
        'boolean': 'SBOOL',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        # Add other reserved words here
    }

    DATA_TYPES = ('INT', 'FLOAT', 'STRING')
    RESERVED = tuple(reserved.values())
    OPERATORS = (
        'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULUS', 'EQUALS', 'GT', 'LT', 'GE', 'LE', 'AND', 'OR', 'NOT', 'NE')

    SPECIFIC_OPERATORS = ('TO_STREAM', 'CHAIN', 'ATTACH', 'CALL', 'FILTEROP', 'MAP', 'REDUCE', 'LAMBDA',
                          'STREAMSPLIT', 'STREAMMERGE', 'FEEDBACK', 'ASSIGN')

    STRUCTURE = ('LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA',
                 'SEMICOLON', 'TYPEHINTCOLON', 'NEWLINE', 'LBRACKET', 'RBRACKET')

    tokens = DATA_TYPES + RESERVED + OPERATORS + SPECIFIC_OPERATORS + STRUCTURE + ('IDENTIFIER', 'EOF')

    states = (
        ('MULTILINECOMMENT', 'exclusive'),
        ('COMMENT', 'exclusive'),
    )

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'/'
    t_MODULUS = r'%'
    t_EQUALS = r'=='
    t_NE = r'!='
    t_GT = r'>'
    t_LT = r'<'
    t_GE = r'>='
    t_LE = r'<='
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_TO_STREAM = r'\.toStream\(\)'
    t_CHAIN = r'>>'
    t_ATTACH = r'->'
    t_TYPEHINTCOLON = r':'
    t_NEWLINE = r'\n'
    t_CALL = r'\.'
    t_FILTEROP = r'\?'
    t_MAP = r'\$'
    t_LAMBDA = r'=>'
    t_REDUCE = r'\^'
    t_STREAMSPLIT = r'\|'
    t_STREAMMERGE = r'\+\+'
    t_FEEDBACK = r'<<'
    t_ASSIGN = r'='

    def t_STRING(self, t):
        r'\"[^\"]*\"'  # Match a sequence of characters enclosed in double quotes TODO: escape sequences (Use a state with special characters)
        t.value = t.value[1:-1]
        return t

    def t_FLOAT(self, t):
        r'\d+\.\d+'  # Match a sequence of one or more digits, a dot, and one or more digits
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r'\d+'  # Match a sequence of one or more digits
        t.value = int(t.value)
        return t

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'  # Match a sequence of letters, digits, and underscores not starting with a digit
        t.type = self.reserved.get(t.value, 'IDENTIFIER')  # Set Type to a Reserved value, else default to identifier
        return t

    def t_COMMENT(self, t):
        r'//.*'  # Match a sequence of characters starting with // and ending with a newline
        t.lexer.begin('COMMENT')

    def t_COMMENT_error(self, t):
        t.lexer.skip(1)

    t_COMMENT_ignore = ' \t'

    def t_COMMENT_end(self, t):
        r'\n'  # Match a newline character
        t.lexer.begin('INITIAL')  # Return to the initial state

    def t_newline(self, t):  #Track line numbers
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_MULTILINECOMMENT(self, t):
        r'/\*'  # Match a sequence of characters starting with /*
        t.lexer.begin('MULTILINECOMMENT')

    def t_MULTILINECOMMENT_newline(self, t):
        r'\n+'  # Match a sequence of newline characters
        t.lexer.lineno += len(t.value)

    def t_MULTILINECOMMENT_error(self, t):
        t.lexer.skip(1)

    t_MULTILINECOMMENT_ignore = ' \t'

    def t_MULTILINECOMMENT_end(self, t):
        r'\*/'  # Match a sequence of characters ending with */
        t.lexer.begin('INITIAL')  # Return to the initial state

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def t_eof(self, t):
        return None

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()

    def tokenize(self, data):
        self.input(data)
        tokens = []
        while True:
            tok = self.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens


if __name__ == '__main__':

    # Test it outst cases. However, consider adding support
    data = '''
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
    '''

    data2 = '''
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
    lexer = Lexer()
    tokens = lexer.tokenize(data2)
    for token in tokens:
        print(token)
    print("Done")
