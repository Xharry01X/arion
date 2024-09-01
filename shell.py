import basic


while True:
        text = input("calc > ")
        if text.lower() == 'exit':
            break
        result, error = basic.run("<stdin>", text)
        if error:
            print(error.as_string())
        else:
            print(result)