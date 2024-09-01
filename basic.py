# Constants
DIGITS = '0123456789'  # String containing all digit characters (used for identifying numbers)

# Custom error classes
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        # Initialize the error with start position, end position, error name, and details
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        # Return a string representation of the error, including filename and line number
        return f'{self.error_name}: {self.details} in {self.pos_start.fn}, line {self.pos_start.ln + 1}'

# Subclass of Error for handling illegal characters
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        # Initialize with 'Illegal Character' as the error name
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

# Position class to track the current position in the input text
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        # Initialize position with index, line number, column number, filename, and full text
        self.idx = idx    # Current index in the input text
        self.ln = ln      # Current line number
        self.col = col    # Current column number
        self.fn = fn      # File name (for error reporting)
        self.ftxt = ftxt  # Full text of the input

    def advance(self, current_char):
        # Move to the next character in the input text
        self.idx += 1
        self.col += 1

        if current_char == '\n':  # Handle newline character
            self.ln += 1
            self.col = 0

        return self  # Return the updated position

    def copy(self):
        # Return a copy of the current position
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

# Token types as string constants
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

# Token class to represent individual tokens
class Token:
    def __init__(self, type_, value=None):
        # Initialize token with type and optional value
        self.type = type_
        self.value = value
        
    def __repr__(self):
        # Return a string representation of the token, including its value if present
        return f'{self.type}:{self.value}' if self.value is not None else f'{self.type}'

# Lexer class to perform lexical analysis
class Lexer:
    def __init__(self, fn, text):
        # Initialize lexer with filename and input text
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)  # Initialize position at the start
        self.current_char = None  # Initialize the current character as None
        self.advance()  # Advance to the first character
        
    def advance(self):
        # Advance to the next character in the input text
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        
    def make_tokens(self):
        # Generate a list of tokens from the input text
        tokens = []
        
        while self.current_char is not None:  # Loop until the end of the input
            if self.current_char in ' \t':  # Skip whitespace
                self.advance()
            elif self.current_char in DIGITS:  # Check for digits
                tokens.append(self.make_number())
            elif self.current_char == '+':  # Handle plus operator
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':  # Handle minus operator
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':  # Handle multiplication operator
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':  # Handle division operator
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':  # Handle left parenthesis
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':  # Handle right parenthesis
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:  # Handle illegal characters
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")
                
        return tokens, None  # Return the list of tokens and no error
    
    def make_number(self):
        # Generate a token for a number (integer or float)
        num_str = ''
        dot_count = 0
        
        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:  # Only allow one decimal point
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
                
        if dot_count == 0:  # Return an integer token if no decimal point
            return Token(TT_INT, int(num_str))
        else:  # Return a float token if there's a decimal point
            return Token(TT_FLOAT, float(num_str))

# Parser class to perform syntactic analysis
class Parser:
    def __init__(self, tokens):
        # Initialize parser with a list of tokens
        self.tokens = tokens
        self.token_idx = -1  # Initialize token index at -1
        self.advance()  # Advance to the first token
        
    def advance(self):
        # Advance to the next token
        self.token_idx += 1
        self.current_token = self.tokens[self.token_idx] if self.token_idx < len(self.tokens) else None
            
    def parse(self):
        # Parse the tokens starting from the expression level
        return self.expr()
    
    def factor(self):
        # Parse a factor (a number in this case)
        token = self.current_token
        if token.type in (TT_INT, TT_FLOAT):  # Check if token is an integer or float
            self.advance()  # Advance to the next token
            return token  # Return the number token
    
    def term(self):
        # Parse a term (handles multiplication and division)
        result = self.factor()  # Parse the first factor
        
        while self.current_token and self.current_token.type in (TT_MUL, TT_DIV):
            token = self.current_token  # Get the current token
            self.advance()  # Advance to the next token
            if token.type == TT_MUL:
                result = self.create_number_token(result.value * self.factor().value)
            elif token.type == TT_DIV:
                result = self.create_number_token(result.value / self.factor().value)
        
        return result  # Return the result of the term
    
    def expr(self):
        # Parse an expression (handles addition and subtraction)
        result = self.term()  # Parse the first term
        
        while self.current_token and self.current_token.type in (TT_PLUS, TT_MINUS):
            token = self.current_token  # Get the current token
            self.advance()  # Advance to the next token
            if token.type == TT_PLUS:
                result = self.create_number_token(result.value + self.term().value)
            elif token.type == TT_MINUS:
                result = self.create_number_token(result.value - self.term().value)

        return result  # Return the result of the expression

    def create_number_token(self, value):
        """Create a token with the appropriate type (INT or FLOAT) based on the value."""
        if isinstance(value, int):  # Check if the value is an integer
            return Token(TT_INT, value)  # Return an integer token
        elif isinstance(value, float):  # Check if the value is a float
            return Token(TT_FLOAT, value)  # Return a float token
        else:
            raise ValueError(f"Unexpected value type: {type(value)}")  # Raise an error for unexpected types

# Function to run the lexer and parser on the given input
def run(fn, text):
    # Initialize lexer and generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    
    if error:  # Check for any lexical errors
        return None, error
    
    # Parse tokens
    parser = Parser(tokens)
    result = parser.parse()  # Parse the tokens into an expression
    
    return result, None  # Return the result and no error
