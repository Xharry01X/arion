import basic  # Make sure that your code is saved as basic.py and located in the same directory

while True:
    text = input('basic > ')  # Prompt the user for input
    if text.strip() == "":  # Skip empty input
        continue
    result, error = basic.run(text)  # Run the input through the lexer, parser, and interpreter
    
    if error: 
        print(error.as_string())  # Print the error if one occurs
    else:
        print(result)  # Print the result of the expression
