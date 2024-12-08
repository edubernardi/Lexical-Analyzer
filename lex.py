#Alunos: Eduardo Bernardi e Marco Donini Jr.
import ply.lex as lex

def validate(tokens):
    if len(tokens) < 1:
        return tokens
    if tokens[0] == 'FUNCTION_NAME':
        tokens = validate_function(tokens) 
        if tokens is None:
            return None
    elif tokens[0] == 'WHILE':
        tokens = validate_while(tokens)
        if tokens is None:
            return None
    return tokens

def validate_while(tokens):
    expected_next = "WHILE"
    i = 0 
    while i < len(tokens):
        if tokens[i] == 'WHILE':
            if expected_next == 'WHILE':
                expected_next = "OPEN_PARENTHESIS"
                i += 1
            else:
                return False
        elif tokens[i] == "OPEN_PARENTHESIS":
            if expected_next == "OPEN_PARENTHESIS":
                tokens = validate_condition(tokens[i + 1:])
                i = 0
                if tokens is None:
                    return None
                expected_next = "OPEN_BRACKETS"
            else:
                return False
        elif tokens[i] == "OPEN_BRACKETS":
            if expected_next == "OPEN_BRACKETS":
                tokens = validate(tokens[i + 1:])
                i = 0
                if tokens is None:
                    return None
                expected_next = "CLOSE_BRACKETS"
        elif tokens[i] == "CLOSE_BRACKETS":
            if expected_next == "CLOSE_BRACKETS":
                return tokens[i + 1:]
            return None

def validate_condition(tokens):
    expected_next = ["VARIABLE", "NUMBER"]
    for i in range(0, len(tokens)):
        if tokens[i] == "NUMBER":
            if tokens[i] in expected_next:
                expected_next = ["CLOSE_PARENTHESIS", "COMPARISON"]
            else:
                return None
        elif tokens[i] == "VARIABLE":
            if tokens[i] in expected_next:
                expected_next = ["CLOSE_PARENTHESIS", "COMPARISON"]
            else:
                return None
        elif tokens[i] == "COMPARISON":
            if tokens[i] in expected_next:
                expected_next = ["VARIABLE", "NUMBER"]
            else:
                return None
        elif tokens[i] == "CLOSE_PARENTHESIS":
            if tokens[i] in expected_next:
                return tokens[i + 1:]
            else:
                return None
    
def validate_function(tokens):
    expected_next = "FUNCTION_NAME"
    arguments_section = False
    parenthesis_count = 0
    for token in tokens:
        if token == 'FUNCTION_NAME':
            if expected_next == "FUNCTION_NAME":
                expected_next = "OPEN_PARENTHESIS"
            else:
                return None
        
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
                return None

        elif token == 'OPEN_PARENTHESIS':
            if expected_next == "OPEN_PARENTHESIS":
                parenthesis_count += 1
                expected_next = "FORMAT_STRING"
            else:
                return None
        
        elif token == 'FORMAT_STRING':
            if expected_next == "FORMAT_STRING":   
                expected_next = "COMMA_OR_CLOSE"
            else:
                return None
        
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
                index = tokens.index(token)
                return index
            else:
                return None

        elif expected_next == "VARIABLE":
            if token in ['VARIABLE', 'NUMBER', 'FORMAT_STRING']:
                expected_next = "COMMA_OR_CLOSE"
            else:
                return None
                  
        elif expected_next == "SEMICOLON":
            if token == 'SEMICOLON':
                index = tokens.index(token)
                tokens = validate(tokens[index + 1:])
                return tokens
            else:
                return None

tokens = (
    'FUNCTION_NAME',
    'OPEN_PARENTHESIS',
    'CLOSE_PARENTHESIS',
    'FORMAT_STRING',
    'COMMA',
    'VARIABLE',
    'SEMICOLON',
    'OPERATOR',
    'WHILE',
    'NUMBER',
    'OPEN_BRACKETS',
    'CLOSE_BRACKETS',
    'COMPARISON'
)

t_OPEN_PARENTHESIS = r'\('
t_CLOSE_PARENTHESIS = r'\)'
t_OPEN_BRACKETS = r'\{'
t_CLOSE_BRACKETS = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_OPERATOR = r'[-+*/]'

def t_FUNCTION_NAME(t):
    r'printf'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_FORMAT_STRING(t):
    r'"([^"\\]*(\\.[^"\\]*)*)"'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'  # Inteiros e float com n casas decimais
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_COMPARISON(t):
    r'==|!=|<=|>=|<|>'
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


f = open('while.txt')
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
    print(f"Tokens: {tokens}")
    result = validate(tokens)
    if result == None:
        print("Não pertence à gramática.")
    elif len(result) == 0:
        print("Pertence à gramática.")
    else:
        print("Não pertence à gramática.")