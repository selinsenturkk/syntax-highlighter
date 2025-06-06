class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.error_line = None

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def match(self, expected_type, expected_value=None):
        token = self.current_token()
        if token and token[0] == expected_type:
            if expected_value is None or token[1] == expected_value:
                self.pos += 1
                return True
        return False

    def parse(self):
        self.pos = 0
        self.error_line = None 
        while self.pos < len(self.tokens):
            token = self.current_token()

            if token and token[0] == "COMMENT":
                self.pos += 1
                continue

            if not self.statement():
                token = self.current_token()
                if token and len(token) >= 4:
                    self.error_line = token[3] 
                else:
                    self.error_line = 1
                return False
        return True

    def statement(self):
        return (
            self.if_statement() or
            self.while_statement() or
            self.assignment() or
            self.return_statement()
        )

    def if_statement(self):
        start = self.pos
        if self.match("KEYWORD", "if"):
            if self.match("DELIMITER", "(") and self.condition() and self.match("DELIMITER", ")"):
                if self.statement_block():
                    if self.match("KEYWORD", "else"):
                        if not self.statement_block():
                            self.pos = start
                            return False
                    return True
        self.pos = start
        return False

    def while_statement(self):
        start = self.pos
        if self.match("KEYWORD", "while"):
            if self.match("DELIMITER", "(") and self.condition() and self.match("DELIMITER", ")"):
                return self.statement_block()
        self.pos = start
        return False

    def assignment(self):
        start = self.pos
        if self.match("IDENTIFIER") and self.match("OPERATOR", "=") and self.expression() and self.match("DELIMITER", ";"):
            return True
        self.pos = start
        return False

    def return_statement(self):
        start = self.pos
        if self.match("KEYWORD", "return") and self.expression() and self.match("DELIMITER", ";"):
            return True
        self.pos = start
        return False

    def condition(self):
        start = self.pos
        if (self.match("IDENTIFIER") or self.match("NUMBER")):
            if self.match("OPERATOR", "==") or self.match("OPERATOR", "!=") or \
            self.match("OPERATOR", "<") or self.match("OPERATOR", ">") or \
            self.match("OPERATOR", "<=") or self.match("OPERATOR", ">="):
                if self.match("IDENTIFIER") or self.match("NUMBER"):
                    return True
        self.pos = start
        return False

    def expression(self):
        if self.match("IDENTIFIER") or self.match("NUMBER"):
            while True:
                start = self.pos
                if self.match("OPERATOR"):
                    if not (self.match("IDENTIFIER") or self.match("NUMBER")):
                        self.pos = start
                        break
                else:
                    break
            return True
        return False

    def statement_block(self):
        if not self.match("DELIMITER", "{"):
            return False
        while True:
            token = self.current_token()
            if token is None:
                return False  # kapatma parantezi yok
            if token[0] == "DELIMITER" and token[1] == "}":
                self.pos += 1
                return True
            if not self.statement():
                return False
