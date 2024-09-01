# This is the class of tokens, it is the smallest units of meaning in programming language.

class Token:
    def __init__(self,type_, value):
        self.type = type_
        self.value = value
        
        
        
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
        