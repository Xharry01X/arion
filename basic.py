# This is the class of tokens, it is the smallest units of meaning in programming language.


# Constants
DIGITS = '0123456789'


### Custom error class
class Error:
    def __init__(self,error_name, details):
        self.error_name = error_name
        self.details = details
        
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result
    
class IllegalCharError(Error):
    def __init__(self,details):
        super().__init__('Illegal Characters',details)
        
        
        

# Defining few constant type for tokens
TT_INT = 'TT_INT'   # Integer token type
TT_FLOAT = 'TT_FLOAT' # Float token type
TT_PLUS = 'TT_PLUS'  # Plus sign token type
TT_MINUS = 'TT_MINUS'  # Minus sign token type
TT_MUL = 'TT_MUL'   # Multiplication sign token type
TT_DIV = 'TT_DIV'   # Division sign token type
TT_LPAREN = 'TT_LPAREN'  # Left parenthesis token type
TT_RPAREN = 'TT_RPAREN'  # Right parenthesis token type

class Token:
    def __init__(self,type_, value = None):
        self.type = type_ #Type of the token
        self.value = value #Value of the token
        
        
        
    def __repr__(self):
        # If the token has value, represent it as 'Type:VALUE'
        if self.value: return f'{self.type}:{self.value}'
        #otherwise, just represent it as 'TYPE'
        return f'{self.type}'
        
        
# Lexer class to process the input text and generate tokens

class Lexer:
    def __init__(self,text):
        self.text = text  # Input text to be processed
        self.pos = -1    # Position in the input text (initialized to -1)
        self.current_char = None   # Current character under examination
        self.advance(self)   # Advance to the first character in the text
        
    def advance(self):
        # Move to the next character in the input text
        self.pos += 1
         # Update current_char to the next character if within bounds, otherwise set to None
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        
        
        
    def make_tokens(self):
        tokens = []
        
        while self.current_char !=None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                 tokens.append(Token(TT_LPAREN))
                 self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                # return some custom errors for better debugging
                char = self.current_char
                self.advance()
                return [], IllegalCharError("'" + char + "'")
                
                
        return tokens,None
    
    ## THis all logic for creating float logic in my custom language.
    
    def make_number(self):
        num_str = ''
        dot_count = 0
        
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count +=1
                num_str += '.'
            else:
                num_str += self.current_char
                
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))
            
            
            
## Run function 
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_token()
    
    return tokens, error