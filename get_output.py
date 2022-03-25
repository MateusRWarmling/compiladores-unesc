from unique_tokens import unique_tokens

def is_interger(token):
    try:
        return int(token)
    except:
        return False

def is_reserved(token):
    for key, value in unique_tokens.items():
        if value == token:
            return value, key

    return unique_tokens.get(25), token

def define_type(token):
    interger_token = is_interger(token)
    if interger_token:
        return(f"{interger_token} --- {unique_tokens.get(26)}")

    reserved_word = is_reserved(token)
    return(f"{reserved_word[1]} --- {reserved_word[0]}")

def generate_output(filePath):
    tokens = []
    tokens_types = []
    file = open(filePath)

    for line in file:
        for word in line.split():
            tokens.append(word)

    for token in tokens:
       tokens_types.append(define_type(token))
    
    file.close()
    return tokens_types