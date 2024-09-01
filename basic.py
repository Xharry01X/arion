# Constants
DIGITS = '0123456789'  # String containing all digit characters

### Custom error class
class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name  # Name of the error
        self.details = details        # Details about the error
        
    def as_string(self):
        # Returns the error name and details as a formatted string
        result = f'{self.error_name}: {self.details}'
        return result
    
class IllegalCharError(Error):
    def __init__(self, details):
        # Initialize the parent class with a specific error name
        super().__init__('Illegal Character', details)

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
    def __init__(self, text):
        self.text = text  # Input text to be processed
        self.pos = -1     # Position in the input text (initialized to -1)
        self.current_char = None  # Current character under examination
        self.advance()  # Advance to the first character in the text
        
    def advance(self):
        # Move to the next character in the input text
        self.pos += 1
        # Update current_char to the next character if within bounds, otherwise set to None
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        
    def make_tokens(self):
        tokens = []  # List to store generated tokens
        
        # Loop through all characters in the input text
        while self.current_char is not None:
            if self.current_char in ' \t':
                # Ignore whitespace characters
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
                char = self.current_char
                self.advance()
                return [], IllegalCharError("'" + char + "'")
                
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
        
        
        # Parser class to turn tokens into an abstraction sysntax tree
class Parser:
    def __init__(self,tokens):
        self.tokens = tokens # List of tokens from the lexer
        self.token_idx = -1  #current position in the token list
        self.advance()
        
    def advance(self):
        self.token_idx +=1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        else:
            self.current_token = None
            
    def parse(self):
        return self.expr() # Start parsing with the expression
    
    def factor(self):
        token = self.current_token
        if token.type in (TT_INT,TT_FLOAT):
            self.advance()
            return token  #return the number token as factor
        
    def term(self):
        result = self.factor()
        
        while self.current_token is not None and self.current_token.type in (TT_MUL,TT_DIV):
            token = self.current_token
            self.advance()
            if token.type == TT_MUL:
                result = Token(TT_INT,result.value * self.factor().value)
            elif token.type == TT_DIV:
                result = Token(TT_INT,result.value / self.factor().value)
        
        return result
        

# Run function to initialize the lexer and generate tokens from the input text
def run(text):
    lexer = Lexer(text)  # Create a lexer object with the input text
    tokens, error = lexer.make_tokens()  # Generate tokens from the lexer
    
    return tokens, error  # Return the list of tokens and any error encountered



