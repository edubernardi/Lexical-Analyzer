import ply.lex as lex
from ply.lex import TOKEN

# Inicializando listas e dicionários para armazenar tokens lidos, símbolos e erros
read_tokens = [] # Armazena os tokens lidos
symbols = []     # Armazena os símbolos identificados
errors = {}      # Armazena os erros encontrados por linha


# Definindo palavras reservadas da linguagem
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

# Lista de tokens
tokens = [
   'IDENTIFICADOR',
   'NUMERO_INTEIRO',
   'NUMERO_REAL',
   'COMENTARIO'
] + list(reserved.values()) # Incluindo as palavras reservadas na lista de tokens

# Expressões regulares para os diferentes tipos de tokens
t_COMENTARIO     = r'^//.*$' # Expressão para identificar comentários

# Definição de expressões regulares auxiliares
digit            = r'([0-9])' # Define um dígito
nondigit         = r'([A-Za-z])' # Define um não-dígito
identifier       = r'^(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)$'  # Identifica nomes válidos de identificadores

# Expressões regulares para números
constant_decimal = r'^(((' + digit + ' ) | (' + digit + digit + ')) \\. (' + digit + digit + '))$'
constant_whole   = r'^((' + digit + digit + ') | (' + digit + ' ))$'



# Definição de tokens e ações associadas
@TOKEN(identifier)
def t_IDENTIFICADOR(t):
    t.type = reserved.get(t.value,'IDENTIFICADOR')    # Verifica se o identificador é uma palavra reservada
    return t

@TOKEN(constant_decimal)
def t_NUMERO_REAL(t):
    t.value = float(t.value) # Converte o valor para float
    return t

@TOKEN(constant_whole)
def t_NUMERO_INTEIRO(t):
    t.value = int(t.value)  # Converte o valor para inteiro
    return t

# Regra para rastrear números de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres a serem ignorados (espaços e tabulações)
t_ignore  = ' \t'

# Regra para tratamento de erros
def t_error(t):
    t.lexer.skip(1)
    return 'error'

# Construir o analisador léxico
lexer = lex.lex()

# Lendo o arquivo de entrada
f = open('input.text', 'r')

lines = f.readlines()

line_counter = 0 # Contador de linhas

for line in lines:
    line_counter += 1
    lexer.input(line)
    tok = lexer.token()

    # Se houver erro, armazena a linha com erro
    if tok == "error":
        errors[line_counter] = line[:-1]
    else:
        # Armazena os tokens lidos 
        if tok is not None:
            tok.lineno = line_counter
            read_tokens.append(tok)
            if tok.value not in symbols and tok.value not in reserved.keys() and tok.type != "COMENTARIO":
                symbols.append(tok.value)

# Inicializa arquivo de saída
output = open('output.txt', 'w')

# Prints da saída
print('\nTokens de Entrada')
output.write('Tokens de Entrada\n')
for token in read_tokens:
    if token.value not in reserved.keys() and token.type != "COMENTARIO":    
        symbol_id = symbols.index(token.value) + 1
    else:
        symbol_id = ""
    print(f'[{token.lineno}] {token.type} {symbol_id}')
    output.write(f'[{token.lineno}] {token.type} {symbol_id}\n')

print('\nTabela de símbolos')
output.write('\nTabela de símbolos\n')
i = 0
for symbol in symbols:
    i += 1
    print(f'[{i}] {symbol}')
    output.write(f'[{i}] {symbol}\n')

print('\nErros nas linhas')
output.write('\nErros nas linhas\n')
for line in errors.keys():
    print(f'{line} ({errors[line]})')
    output.write(f'{line} ({errors[line]})\n')