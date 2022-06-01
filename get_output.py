from unique_tokens import unique_tokens
import re

def getSanatizedArray(word):
    sanatizedWord = word
    especialCharacters = ['+', '*', '/', '[', ']', '(', ')', ':=', ':', '=', '>', '>=', '<', '<=', '<>', ',', ';', '.', '..']

    if '..' in sanatizedWord:
        especialCharacters.pop(especialCharacters.index('.'))

    if ':=' in sanatizedWord:
        especialCharacters.pop(especialCharacters.index(':'))
        especialCharacters.pop(especialCharacters.index('='))
    
    if '>=' in sanatizedWord:
        especialCharacters.pop(especialCharacters.index('>'))
        especialCharacters.pop(especialCharacters.index('='))
    
    if '<=' in sanatizedWord:
        especialCharacters.pop(especialCharacters.index('<'))
        especialCharacters.pop(especialCharacters.index('='))
    
    if '<>' in sanatizedWord:
        especialCharacters.pop(especialCharacters.index('<'))
        especialCharacters.pop(especialCharacters.index('>'))

    for character in especialCharacters:
        if character in word:
            sanatizedWord = sanatizedWord.replace(character, f" {character} ")   

    return sanatizedWord.split()

def is_integer(token):
    try:
        if token == '0':
            return '0'
        return int(token)
    except:
        return False

def is_reserved(token):
    for key, value in unique_tokens.items():
        if value.upper() == token.upper():
            return token,value, key

    return token, unique_tokens.get(25), '25'

def define_type(token, line):
    integer_token = is_integer(token)
    if integer_token:
        return(f"{integer_token}%%%%{unique_tokens.get(26)}%%%%26%%%%{line}")

    reserved_word = is_reserved(token)
    return(f"{reserved_word[0]}%%%%{reserved_word[1]}%%%%{reserved_word[2]}%%%%{line}")

def generate_output(filePath):
    isComment = False
    tokens = []
    tokens_types = []
    file = open(filePath)

    for index, line in enumerate(file):
        for word in line.split():
            if "(*" in word:
                if "*)" in word:
                    continue
                isComment = True
                continue
            if "*)" in word:
                isComment = False
                continue
            if isComment == True:
                continue
            if re.search("[+\-*/.,;[\]():=><]", word):
                sanatizedArray = getSanatizedArray(word)

                for sanatizedWord in sanatizedArray:
                    tokens.append([(index + 1), sanatizedWord])

                continue
            tokens.append([(index + 1), word])

    for token in tokens:
       tokens_types.append(define_type(token[1], token[0]))

    file.close()
    return tokens_types