# Constants
DIGITS = '0123456789'  # String containing all digit characters (used for identifying numbers)

### Custom error class
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start  # Starting position of the error
        self.pos_end = pos_end      # Ending position of the error
        self.error_name = error_name  # Name of the error
        self.details = details        # Details about the error

    def as_string(self):
        # Returns the error name and details as a formatted string along with the file and line number
        result = f'{self.error_name}: {self.details}'
        result += f' in {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

# A specific error class for illegal characters
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        # Initialize the parent class with a specific error name
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

# Position class to track the current position in the input text
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx    # Current index in the input text
        self.ln = ln      # Current line number
        self.col = col    # Current column number
        self.fn = fn      # File name (used for error reporting)
        self.ftxt = ftxt  # Full text of the input (used for error reporting)

    def advance(self, current_char):
        self.idx += 1  # Move to the next character in the input text
        self.col += 1  # Move to the next column

        if current_char == '\n':  # If the current character is a newline
            self.ln += 1      # Move to the next line
            self.col = 0      # Reset column to the start of the line

        return self  # Return the updated position object

    def copy(self):
        # Create and return a copy of the current position
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

# Defining a few constant types for tokens
TT_INT = 'TT_INT'      # Integer token type
TT_FLOAT = 'TT_FLOAT'  # Float token type
TT_PLUS = 'TT_PLUS'    # Plus sign token type
TT_MINUS = 'TT_MINUS'  # Minus sign token type
TT_MUL = 'TT_MUL'      # Multiplication sign token type
TT_DIV = 'TT_DIV'      # Division sign token type
TT_LPAREN = 'TT_LPAREN'  # Left parenthesis token type
TT_RPAREN = 'TT_RPAREN'  # Right parenthesis token type

# Token class to represent each token with a type and an optional value
class Token:
    def __init__(self, type_, value=None):
        self.type = type_  # Type of the token
        self.value = value  # Value of the token (optional)
        
    def __repr__(self):
        # If the token has a value, represent it as 'TYPE:VALUE'
        if self.value: 
            return f'{self.type}:{self.value}'
        # Otherwise, just represent it as 'TYPE'
        return f'{self.type}'

# Lexer class to process the input text and generate tokens
class Lexer:
    def __init__(self, fn, text):
        self.fn = fn  # File name (used for error reporting)
        self.text = text  # Input text to be processed
        self.pos = Position(-1, 0, -1, fn, text)  # Initialize position (-1 so advance() sets to 0)
        self.current_char = None  # Current character under examination
        self.advance()  # Advance to the first character in the text
        
    def advance(self):
        # Move to the next character in the input text
        self.pos.advance(self.current_char)
        # Update current_char to the next character if within bounds, otherwise set to None
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        
    def make_tokens(self):
        tokens = []  # List to store generated tokens
        
        # Loop through all characters in the input text
        while self.current_char is not None:
            if self.current_char in ' \t':
                # Ignore whitespace characters (space and tab)
                self.advance()
            elif self.current_char in DIGITS:
                # If current character is a digit, create a number token
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))  # Create a plus token
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))  # Create a minus token
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))  # Create a multiplication token
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))  # Create a division token
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))  # Create a left parenthesis token
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))  # Create a right parenthesis token
                self.advance()
            else:
                # Handle illegal characters
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
                
        # Return the list of tokens and no error
        return tokens, None
    
    # Logic for creating number tokens, supporting both integers and floats
    def make_number(self):
        num_str = ''  # String to store the number being formed
        dot_count = 0  # Counter for the number of dots encountered (for floats)
        
        # Loop to build the number as long as it's a digit or a dot
        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break  # Only one dot allowed in a float
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()  # Move to the next character
                
        # Determine if the number is an integer or a float
        if dot_count == 0:
            return Token(TT_INT, int(num_str))  # Create an integer token
        else:
            return Token(TT_FLOAT, float(num_str))  # Create a float token
        
# Parser class to turn tokens into an abstract syntax tree (AST)
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # List of tokens from the lexer
        self.token_idx = -1  # Current position in the token list (initialized to -1)
        self.advance()  # Advance to the first token
        
    def advance(self):
        # Move to the next token in the list
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]  # Update the current token
        else:
            self.current_token = None  # No more tokens left
            
    def parse(self):
        # Start parsing with the expression (root of the AST)
        return self.expr()
    
    def factor(self):
        # Handle numbers (both integers and floats) as factors
        token = self.current_token
        if token.type in (TT_INT, TT_FLOAT):
            self.advance()
            return token  # Return the number token as a factor
    
    def term(self):
        # Handle multiplication and division operations
        result = self.factor()  # Start with a factor
        
        while self.current_token is not None and self.current_token.type in (TT_MUL, TT_DIV):
            token = self.current_token
            self.advance()
            if token.type == TT_MUL:
                # Multiply the result by the next factor
                result = Token(TT_INT, result.value * self.factor().value)
            elif token.type == TT_DIV:
                # Divide the result by the next factor
                result = Token(TT_INT, result.value / self.factor().value)
        
        return result
    
    def expr(self):
        # Handle addition and subtraction operations
        result = self.term()  # Start with a term
        
        while self.current_token is not None and self.current_token.type in (TT_PLUS, TT_MINUS):
            token = self.current_token
            self.advance()
            if token.type == TT_PLUS:
                # Add the result to the next term
                result = Token(TT_INT, result.value + self.term().value)
            elif token.type == TT_MINUS:
                # Subtract the next term from the result
                result = Token(TT_INT, result.value - self.term().value)

        return result
        
# Run function to initialize the lexer, generate tokens, and parse them
def run(fn, text):
    lexer = Lexer(fn, text)  # Create a lexer object with the input text
    tokens, error = lexer.make_tokens()  # Generate tokens from the lexer
    
    if error:
        return None, error  # Return the error if there's any
    
    parser = Parser(tokens)  # Create a parser object with the generated tokens
    result = parser.parse()  # Parse the tokens to produce the AST (or result in this case)
    
    return result, None  # Return the final result and no error
