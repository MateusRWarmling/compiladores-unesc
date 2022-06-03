from uniqueTokens import uniqueTokens
import re

# analise lexica

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

def isInteger(token):
    try:
        if token == '0':
            return '0'
        return int(token)
    except:
        return False

def isReserved(token):
    for key, value in uniqueTokens.items():
        if value.upper() == token.upper():
            return token,value, key

    return token, uniqueTokens.get(25), '25'

def defineType(token, line):
    integer_token = isInteger(token)
    if integer_token:
        return(f"{integer_token}%%%%{uniqueTokens.get(26)}%%%%26%%%%{line}")

    reserved_word = isReserved(token)
    return(f"{reserved_word[0]}%%%%{reserved_word[1]}%%%%{reserved_word[2]}%%%%{line}")

def defineTerminalType(token):
    integer_token = isInteger(token)
    if integer_token:
        return 26

    reserved_word = isReserved(token)
    return reserved_word[2]

def lexicalStep(filePath):
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
       tokens_types.append(defineType(token[1], token[0]))

    file.close()
    return tokens_types