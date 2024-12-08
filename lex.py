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
    elif tokens[0] == 'FOR':
        tokens = validate_for(tokens)
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
                expected_next = "CLOSE_PARENTHESIS"
            else:
                return False
        elif tokens[i] == 'CLOSE_PARENTHESIS':
            if expected_next == 'CLOSE_PARENTHESIS':
                i += 1
                expected_next = "OPEN_BRACKETS"
        elif tokens[i] == "OPEN_BRACKETS":
            if expected_next == "OPEN_BRACKETS":
                tokens = validate(tokens[i + 1:])
                i = 0
                if tokens is None:
                    return None
                expected_next = "CLOSE_BRACKETS"
        elif tokens[i] == "CLOSE_BRACKETS":
            if expected_next == "CLOSE_BRACKETS":
                tokens = validate(tokens[i + 1:])
                return tokens
            return None
        
def validate_for(tokens):
    expected_next = "FOR"
    condition = False
    i = 0 
    while i < len(tokens):
        if tokens[i] == "FOR":
            if expected_next == 'FOR':
                expected_next = "OPEN_PARENTHESIS"
                i += 1
            else:
                return False
        elif tokens[i] == "OPEN_PARENTHESIS":
            if expected_next == "OPEN_PARENTHESIS":
                tokens = validate_attribution(tokens[i + 1:])
                i = 0
                if tokens is None:
                    return None
                expected_next = "SEMICOLON"
            else:
                return False
        elif tokens[i] == "SEMICOLON":
            if expected_next == "SEMICOLON":
                if not condition:
                    tokens = validate_condition(tokens[i + 1:])
                    condition = True
                    expected_next = "SEMICOLON"
                else:
                    tokens = validate_increment(tokens[i + 1:])
                    expected_next = "OPEN_BRACKETS"
                i = 0
                if tokens is None:
                    return None
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
                tokens = validate(tokens[i + 1:])
                return tokens
            return None
        

def validate_condition(tokens):
    expected_next = ["VARIABLE", "NUMBER"]
    for i in range(0, len(tokens)):
        if tokens[i] == "NUMBER":
            if tokens[i] in expected_next:
                expected_next = ["SEMICOLON", "COMPARISON", "CLOSE_PARENTHESIS"]
            else:
                return None
        elif tokens[i] == "VARIABLE":
            if tokens[i] in expected_next:
                expected_next = ["SEMICOLON", "COMPARISON", "CLOSE_PARENTHESIS"]
            else:
                return None
        elif tokens[i] == "COMPARISON":
            if tokens[i] in expected_next:
                expected_next = ["VARIABLE", "NUMBER"]
            else:
                return None
        elif tokens[i] in ["SEMICOLON", "CLOSE_PARENTHESIS"]:
            if tokens[i] in expected_next:
                return tokens[i:]
            else:
                return None
    

def validate_attribution(tokens):
    expected_next = ["VARIABLE"]
    attribution = False
    for i in range(0, len(tokens)):
        if tokens[i] == "NUMBER" or tokens[i] == "FORMAT_STRING":
            if tokens[i] in expected_next:
                expected_next = ["SEMICOLON"]
            else:
                return None
        elif tokens[i] == "VARIABLE":
            if tokens[i] in expected_next:
                if not attribution:
                    expected_next = ["ATTRIBUTION"]
                else:
                    expected_next = ["SEMICOLON"]
            else:
                return None
        elif tokens[i] == "ATTRIBUTION":
            if tokens[i] in expected_next:
                expected_next = ["VARIABLE", "NUMBER", "FORMAT_STRING"]
            else:
                return None
        elif tokens[i] == "SEMICOLON":
            if tokens[i] in expected_next:
                return tokens[i:]
            else:
                return None

def validate_increment(tokens):
    expected_next = ["VARIABLE"]
    operator = False
    for i in range(0, len(tokens)):
        if tokens[i] == "NUMBER" or tokens[i] == "FORMAT_STRING":
            if tokens[i] in expected_next:
                expected_next = ["CLOSE_PARENTHESIS"]
            else:
                return None
        elif tokens[i] == "VARIABLE":
            if tokens[i] in expected_next:
                if not operator:
                    expected_next = ["ATTRIBUTION", "INCREMENT"]
                else:
                    expected_next = ["CLOSE_PARENTHESIS"]
            else:
                return None
        elif tokens[i] == "ATTRIBUTION":
            if tokens[i] in expected_next:
                expected_next = ["VARIABLE", "NUMBER"]
                operator = True
            else:
                return None
        elif tokens[i] == "INCREMENT":
            if tokens[i] in expected_next:
                expected_next = ["CLOSE_PARENTHESIS"]
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
    i = 0
    while i < len(tokens):
        if tokens[i] == 'FUNCTION_NAME':
            if expected_next == "FUNCTION_NAME":
                expected_next = "OPEN_PARENTHESIS"
            else:
                return None
        
        elif arguments_section:
            if tokens[i] == 'COMMA' and expected_next == 'COMMA_OR_CLOSE' or tokens[i] == 'OPERATOR' and expected_next == 'COMMA_OR_CLOSE':
                expected_next = "VARIABLE"
            elif tokens[i] == 'CLOSE_PARENTHESIS':
                parenthesis_count -= 1
                expected_next = "COMMA_OR_CLOSE"
                if parenthesis_count == 0:
                    expected_next = "SEMICOLON"
                    arguments_section = False
            elif tokens[i] == 'VARIABLE':
                expected_next = "COMMA_OR_CLOSE"
            elif tokens[i] == 'OPEN_PARENTHESIS':
                parenthesis_count += 1
                expected_next = 'VARIABLE'
            else:
                return None

        elif tokens[i] == 'OPEN_PARENTHESIS':
            if expected_next == "OPEN_PARENTHESIS":
                parenthesis_count += 1
                expected_next = "FORMAT_STRING"
            else:
                return None
        
        elif tokens[i] == 'FORMAT_STRING':
            if expected_next == "FORMAT_STRING":   
                expected_next = "COMMA_OR_CLOSE"
            else:
                return None
        
        elif expected_next == "COMMA_OR_CLOSE":
            if tokens[i] == 'COMMA' or tokens[i] == 'OPERATOR':
                expected_next = "VARIABLE"
                arguments_section = True
            elif tokens[i] == 'CLOSE_PARENTHESIS':
                parenthesis_count -= 1
                expected_next = "SEMICOLON"
                if parenthesis_count == 0:
                    arguments_section = False
            elif tokens[i] == 'SEMICOLON' and parenthesis_count == 0:
                index = tokens.index(tokens[i])
                return index
            else:
                return None

        elif expected_next == "VARIABLE":
            if tokens[i] in ['VARIABLE', 'NUMBER', 'FORMAT_STRING']:
                expected_next = "COMMA_OR_CLOSE"
            else:
                return None
                  
        elif expected_next == "SEMICOLON":
            if tokens[i] == 'SEMICOLON':
                tokens = validate(tokens[i + 1:])
                return tokens
            else:
                return None
            
        i += 1

tokens = (
    'FUNCTION_NAME',
    'OPEN_PARENTHESIS',
    'CLOSE_PARENTHESIS',
    'FORMAT_STRING',
    'COMMA',
    'VARIABLE',
    'SEMICOLON',
    'WHILE',
    'FOR',
    'NUMBER',
    'OPEN_BRACKETS',
    'CLOSE_BRACKETS',
    'COMPARISON',
    'ATTRIBUTION',
    'ARITHMETIC',
    'INCREMENT'
)

t_OPEN_PARENTHESIS = r'\('
t_CLOSE_PARENTHESIS = r'\)'
t_OPEN_BRACKETS = r'\{'
t_CLOSE_BRACKETS = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'

def t_FUNCTION_NAME(t):
    r'printf'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_FOR(t):
    r'for'
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

def t_ATTRIBUTION(t):
    r'=|\+=|-=|\*=|/=|%='
    return t

def t_INCREMENT(t):
    r'\+\+|--'
    return t

def t_ARITHMETIC(t):
    r'\+|-|\*|/'
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


f = open('for.txt')
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