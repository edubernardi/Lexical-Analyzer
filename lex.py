import ply.lex as lex
from ply.lex import TOKEN

read_tokens = []
symbols = []
errors = {}

reserved = {
   'int' : 'INT',
   'double' : 'DOUBLE',
   'float' : 'FLOAT',
   'real' : 'REAL',
   'break' : 'BREAK',
   'case' : 'CASE',
   'char' : 'CHAR',
   'const' : 'CONST',
   'continue' : 'CONTINUE',
}

# List of token names.   This is always required
tokens = [
   'IDENTIFICADOR',
   'NUMERO_INTEIRO',
   'NUMERO_REAL',
   'COMENTARIO'
] + list(reserved.values())

# Regular expression rules
t_COMENTARIO     = r'^//.*$'


digit            = r'([0-9])'
nondigit         = r'([A-Za-z])'
identifier       = r'^(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)$'

constant_decimal = r'^(((' + digit + ' ) | (' + digit + digit + ')) \\. (' + digit + digit + '))$'
constant_whole   = r'^((' + digit + digit + ') | (' + digit + ' ))$'



# A regular expression rule with some action code
@TOKEN(identifier)
def t_IDENTIFICADOR(t):
    t.type = reserved.get(t.value,'IDENTIFICADOR')    # Check for reserved words
    return t

@TOKEN(constant_decimal)
def t_NUMERO_REAL(t):
    t.value = float(t.value)
    return t

@TOKEN(constant_whole)
def t_NUMERO_INTEIRO(t):
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    t.lexer.skip(1)
    return 'error'

# Build the lexer
lexer = lex.lex()

f = open('input.text', 'r')

lines = f.readlines()

line_counter = 0
for line in lines:
    line_counter += 1
    lexer.input(line)
    tok = lexer.token()

    if tok == "error":
        errors[line_counter] = line[:-1]
    else:
        if tok is not None:
            tok.lineno = line_counter
            read_tokens.append(tok)
            if tok.value not in symbols and tok.value not in reserved.keys() and tok.type != "COMENTARIO":
                symbols.append(tok.value)

print('\nTokens de Entrada')
for token in read_tokens:
    if token.value not in reserved.keys() and token.type != "COMENTARIO":    
        symbol_id = symbols.index(token.value) + 1
    else:
        symbol_id = ""
    print(f'[{token.lineno}] {token.type} {symbol_id}')

print('\nTabela de símbolos')
i = 0
for symbol in symbols:
    i += 1
    print(f'[{i}] {symbol}')

print('\nErros nas linhas')
for line in errors.keys():
    print(f'{line} ({errors[line]})')

