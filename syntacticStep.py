from uniqueTokens import uniqueTokens , invalidTerminals, derivations
from lexicalStep import defineTerminalType

def getTokenCode(token):
    try:
        invalidTerminal = list(invalidTerminals.keys())[list(invalidTerminals.values()).index(token)]
        return invalidTerminal
    except:
        tokenCode = defineTerminalType(token)

        if tokenCode != None:
            return tokenCode

        raise Exception("Token Invalido")

def syntacticStep(tokenList):
    tokenListClone = list(tokenList)
    actualDerivationCodes = [52]
   
    while len(tokenListClone) > 0:
        [inputedValue, _, tokenCode, line ] = tokenListClone[0].split("%%%%")

        if actualDerivationCodes[0] < 52:
            if actualDerivationCodes[0] == int(tokenCode):
                actualDerivationCodes.pop(0)
                tokenListClone.pop(0)
                continue
            else:
                raise Exception(f'Erro ao analisar os terminais, linha: {line} no valor digitado: {inputedValue}, era esperado um token do tipo {actualDerivationCodes[0]}-({uniqueTokens.get(actualDerivationCodes[0])})')

        key = f'{actualDerivationCodes[0]},{tokenCode}'
        derivation = derivations.get(key)
        actualDerivationCodes.pop(0)

        if derivation == None:
            raise Exception(f"A derivação[{key}] '{derivations.get(actualDerivationCodes[0])}' não foi encontrada na tabela parsing. linha: {line}")

        splittedDerivation = []
        try:
            splittedDerivation = reversed(derivation.split('|'))
        except:
            raise Exception(f"Declaração incorreta de bloco, elemento faltante: {uniqueTokens.get(actualDerivationCodes[0])}.")


        for derivationKeyPart in splittedDerivation:
            if derivationKeyPart == "NULL":
                continue

            token_code = getTokenCode(derivationKeyPart)
            actualDerivationCodes.insert(0, token_code)
    return