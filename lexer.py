import re

# Token tanımları
TOKEN_TYPES = [
    ('COMMENT',    r'//[^\n]*'),                               # Yorumlar
    ('KEYWORD',    r'\b(if|else|while|return)\b'),             # Anahtar kelimeler
    ('NUMBER',     r'\b\d+(\.\d+)?\b'),                        # Sayılar
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),             # Değişken/adlar
    ('OPERATOR',   r'==|!=|<=|>=|[=+\-*/<>]'),                 # Operatörler
    ('DELIMITER',  r'[(){},;]'),                               # Ayraçlar
    ('WHITESPACE', r'\s+'),                                    # Boşluklar
]

# Regex birleştirme
TOKEN_REGEX = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES))

def tokenize(code):
    tokens = []
    pos = 0
    line = 1
    line_start = 0

    while pos < len(code):
        match = TOKEN_REGEX.match(code, pos)
        if match:
            kind = match.lastgroup
            value = match.group()
            col = pos - line_start

            if kind != "WHITESPACE":
                tokens.append((kind, value, pos, line, col))

            if '\n' in value:
                line += value.count('\n')
                line_start = match.end()

            pos = match.end()
        else:
            pos += 1

    return tokens
