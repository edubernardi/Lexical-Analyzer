#Alunos: Eduardo Bernardi e Marco Donini Jr.
import ply.lex as lex

def validate(tokens):
    if len(tokens) < 1:
        return True
    if tokens[0] == 'FUNCTION_NAME':
        if not validate_function(tokens):
            return False
    return True
    

def validate_function(tokens):
    expected_next = "FUNCTION_NAME"
    arguments_section = False
    parenthesis_count = 0
    for token in tokens:
        if token == 'FUNCTION_NAME':
            if expected_next == "FUNCTION_NAME":
                expected_next = "OPEN_PARENTHESIS"
            else:
                return False
        
        elif arguments_section:
            if token == 'COMMA' and expected_next == 'COMMA_OR_CLOSE' or token == 'OPERATOR' and expected_next == 'COMMA_OR_CLOSE':
                expected_next = "VARIABLE"
            elif token == 'CLOSE_PARENTHESIS':
                parenthesis_count -= 1
                expected_next = "COMMA_OR_CLOSE"
                if parenthesis_count == 0:
                    expected_next = "SEMICOLON"
                    arguments_section = False
            elif token == 'VARIABLE':
                expected_next = "COMMA_OR_CLOSE"
            elif token == 'OPEN_PARENTHESIS':
                parenthesis_count += 1
                expected_next = 'VARIABLE'
            else:
                return False

        elif token == 'OPEN_PARENTHESIS':
            if expected_next == "OPEN_PARENTHESIS":
                parenthesis_count += 1
                expected_next = "FORMAT_STRING"
            else:
                return False
        
        elif token == 'FORMAT_STRING':
            if expected_next == "FORMAT_STRING":   
                expected_next = "COMMA_OR_CLOSE"
            else:
                return False
        
        elif expected_next == "COMMA_OR_CLOSE":
            if token == 'COMMA' or token == 'OPERATOR':
                expected_next = "VARIABLE"
                arguments_section = True
            elif token == 'CLOSE_PARENTHESIS':
                parenthesis_count -= 1
                expected_next = "SEMICOLON"
                if parenthesis_count == 0:
                    arguments_section = False
            elif token == 'SEMICOLON' and parenthesis_count == 0:
                return True
            else:
                return False

        elif expected_next == "VARIABLE":
            if token in ['VARIABLE', 'NUMBER', 'FORMAT_STRING']:
                expected_next = "COMMA_OR_CLOSE"
            else:
                return False
                  
        elif expected_next == "SEMICOLON":
            if token == 'SEMICOLON':
                index = tokens.index(token)
                validate(tokens[index + 1:])
                print(f"Tokens: {tokens[:index + 1]}")
                print("Pertence à gramática!")
                return True
            else:
                return False

tokens = (
    'FUNCTION_NAME',
    'OPEN_PARENTHESIS',
    'CLOSE_PARENTHESIS',
    'FORMAT_STRING',
    'COMMA',
    'VARIABLE',
    'SEMICOLON',
    'OPERATOR'
)

t_OPEN_PARENTHESIS = r'\('
t_CLOSE_PARENTHESIS = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_OPERATOR = r'[-+*/]'

def t_FUNCTION_NAME(t):
    r'printf'
    return t

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_FORMAT_STRING(t):
    r'"([^"\\]*(\\.[^"\\]*)*)"'
    return t

# Ignorar espaço
t_ignore = ' '

# Ignorar quebra de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Gerenciamento dos erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)
    return 'error'

# Inicializando o lexer
lexer = lex.lex()


f = open('input.txt')
lines = f.readlines()

invalid = False
tokens_list = []
for line in lines:
    command = line
    lexer.input(command)
    print(f"\n{command[0: -1]}")
    invalid = False
    while True:
        tok = lexer.token()
        if tok == 'error':
           print("Não pertence à gramática.")
           invalid = True
           break
        if not tok:
            break 
        tokens_list.append(tok)
if not invalid:  
    tokens = [tok.type for tok in tokens_list]
    if not validate(tokens):
        print("Não pertence à gramática.")
        print(f"Tokens: {tokens}")